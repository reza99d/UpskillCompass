-- Phase 4a: activate_membership RPC + column-level users UPDATE + memberships lockdown.
--
-- Pre-state (confirmed via live query 2026-04-11 after Phase 3):
--   H1: users table had a wide table-level UPDATE grant for authenticated,
--       so any signed-in client could PATCH their own is_premium,
--       premium_tier, and premium_expires_at via devtools (auth.uid()
--       restriction in the Phase-2 policy only limits WHICH row, not
--       WHICH columns).
--   H2: memberships had:
--         Policy  "Users insert own memberships"  USING(true) / CHECK(true)
--         Policy  "Users read own memberships"    USING(true)
--         Grants: anon + authenticated both full CRUD (INSERT/UPDATE/DELETE
--                 /SELECT) including the default anon SELECT leak.
--       So any signed-in client could POST arbitrary membership rows for
--       any user_id with any amount/plan/expiration.
--
-- This migration:
--   1. Adds activate_membership(tier) — the ONLY way a client can flip
--      premium flags. Server-side tier→amount mapping, server-side expiry
--      (now + 1 year), client cannot supply either.
--   2. Tightens memberships policies: rewrites the SELECT policy to check
--      ownership via users.auth_id, drops the wide-open INSERT policy,
--      revokes direct writes and the anon SELECT leak.
--   3. Revokes the wide users UPDATE grant and re-grants column-level
--      UPDATE on just the profile-edit fields, so H1 devtools attacks
--      on is_premium / premium_tier / premium_expires_at fail at the
--      PostgREST layer before RLS is even consulted.
--
-- After this migration the only code path that can set is_premium=true,
-- premium_tier, premium_expires_at, or INSERT into memberships is the
-- activate_membership RPC (SECURITY DEFINER, owned by postgres, bypasses
-- grants). A signed-in user can still call that RPC and get free premium
-- — that's H1/H2 reduced to "call the RPC directly" which is the same
-- outcome as pressing the Subscribe button. A future phase with real
-- Stripe verification will close that remaining gap.
--
-- Safe to re-run.

BEGIN;

-- ---------------------------------------------------------------------
-- 1. activate_membership(tier) — the one way to flip premium flags.
-- ---------------------------------------------------------------------
CREATE OR REPLACE FUNCTION activate_membership(p_tier text)
RETURNS json
LANGUAGE plpgsql
SECURITY DEFINER
SET search_path = public
AS $$
DECLARE
  v_user_id  int;
  v_amount   numeric;
  v_expires  timestamptz := now() + interval '1 year';
BEGIN
  IF auth.uid() IS NULL THEN
    RAISE EXCEPTION 'not_authenticated';
  END IF;

  IF p_tier NOT IN ('premium','premium_plus','premium_pro') THEN
    RAISE EXCEPTION 'invalid_tier'
      USING HINT = 'Tier must be premium, premium_plus, or premium_pro.';
  END IF;

  -- Server-side tier → amount mapping. Client cannot supply this.
  v_amount := CASE p_tier
    WHEN 'premium_pro'  THEN 3588
    WHEN 'premium_plus' THEN 2388
    ELSE 1188
  END;

  SELECT id INTO v_user_id FROM users WHERE auth_id = auth.uid();
  IF v_user_id IS NULL THEN
    RAISE EXCEPTION 'user_row_missing'
      USING HINT = 'Sign out and back in.';
  END IF;

  -- 1. Record the membership row.
  INSERT INTO memberships (user_id, plan, amount, status, expires_at)
  VALUES (v_user_id, 'yearly', v_amount, 'active', v_expires);

  -- 2. Flip the user's premium flags (SECURITY DEFINER bypasses column GRANTs).
  UPDATE users
     SET is_premium         = true,
         premium_tier       = p_tier,
         premium_expires_at = v_expires,
         updated_at         = now()
   WHERE id = v_user_id;

  -- 3. Feature all the user's claimed courses (what /membership/subscribe
  --    used to do via a direct courses PATCH; now consolidated).
  UPDATE courses
     SET is_featured = true,
         updated_at  = now()
   WHERE claimed_auth_id = auth.uid();

  RETURN json_build_object(
    'ok', true,
    'tier', p_tier,
    'amount', v_amount,
    'expires_at', v_expires
  );
END
$$;

GRANT EXECUTE ON FUNCTION activate_membership(text) TO authenticated;


-- ---------------------------------------------------------------------
-- 2. Tighten memberships: revoke direct writes, tighten SELECT policy.
-- ---------------------------------------------------------------------
DROP POLICY IF EXISTS "Users insert own memberships" ON public.memberships;
DROP POLICY IF EXISTS "Users read own memberships"   ON public.memberships;

CREATE POLICY "Users read own memberships"
  ON public.memberships
  FOR SELECT
  USING (
    EXISTS (
      SELECT 1 FROM users u
       WHERE u.id = memberships.user_id
         AND u.auth_id = auth.uid()
    )
  );

REVOKE INSERT, UPDATE, DELETE ON public.memberships FROM anon, authenticated;
REVOKE SELECT              ON public.memberships FROM anon;  -- only signed-in users see their own


-- ---------------------------------------------------------------------
-- 3. Column-level UPDATE on users: whitelist the profile-edit columns,
--    revoke the wide UPDATE, so H1 devtools attacks fail.
-- ---------------------------------------------------------------------
REVOKE UPDATE ON public.users FROM authenticated;
GRANT  UPDATE (first_name, last_name, company, bio, title, avatar_url, updated_at)
       ON public.users TO authenticated;

NOTIFY pgrst, 'reload schema';


-- ---------------------------------------------------------------------
-- 4. Verify.
-- ---------------------------------------------------------------------
SELECT 'users UPDATE column privs (must NOT include is_premium/premium_tier/premium_expires_at)' AS section,
       grantee, privilege_type, column_name
  FROM information_schema.column_privileges
 WHERE table_schema='public' AND table_name='users'
   AND privilege_type='UPDATE'
   AND grantee IN ('anon','authenticated')
 ORDER BY grantee, column_name;

SELECT 'memberships table privs (should be SELECT only, authenticated only)' AS section,
       grantee, privilege_type
  FROM information_schema.table_privileges
 WHERE table_schema='public' AND table_name='memberships'
   AND grantee IN ('anon','authenticated')
 ORDER BY grantee, privilege_type;

SELECT 'memberships policies' AS section, policyname, cmd
  FROM pg_policies
 WHERE schemaname='public' AND tablename='memberships'
 ORDER BY policyname;

SELECT 'activate_membership RPC present + SECURITY DEFINER' AS section,
       proname, prosecdef
  FROM pg_proc WHERE proname='activate_membership';

COMMIT;
