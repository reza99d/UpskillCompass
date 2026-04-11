-- Phase 4d: narrow the column-level SELECT grant on public.users so that
-- email and premium metadata stop leaking across users.
--
-- Pre-state (confirmed via live query 2026-04-11 after Phase 4a/b/c):
--   Phase 2 left public.users with a permissive SELECT policy and a wide
--   column-level SELECT grant that included every column except
--   password_hash. That was fine for column-level filtering (password_hash
--   stayed blocked) but it meant any authenticated client could GET
--   /rest/v1/users?select=id,email&id=neq.<self> and enumerate every
--   registered user's email address. Verified today by issuing that exact
--   request with a valid user JWT and getting a 200 with three seeded
--   users' emails in the response body.
--
-- This migration:
--   1. Revokes the wide column-level SELECT grant on public.users.
--   2. Re-grants column-level SELECT on ONLY the truly public profile
--      fields needed for cross-user display on the catalog, course cards,
--      instructor profile, and search results:
--          id, first_name, last_name, role, company, bio, title,
--          avatar_url, premium_tier, auth_id
--      Every other column (email, is_premium, premium_expires_at,
--      created_at, updated_at, password_hash) becomes unreadable via
--      direct PostgREST SELECT for BOTH anon and authenticated.
--
--      auth_id (UUID) is kept in the public grant because two RLS
--      policies reference it in their USING / WITH CHECK expressions:
--         - "Users read own memberships" on public.memberships does
--           EXISTS(SELECT 1 FROM users u WHERE u.auth_id = auth.uid())
--         - "Users update own row" on public.users does
--           auth_id = auth.uid()
--      PostgreSQL evaluates those expressions in the security context
--      of the calling role, so the role needs column-level SELECT on
--      auth_id or every memberships SELECT and users UPDATE 42501's.
--      Exposing auth_id cross-user is not a net new leak: courses.
--      claimed_auth_id is already public via the wide courses SELECT
--      grant, so any attacker who cares can already enumerate the
--      users.id ↔ auth.uid() mapping via the courses table.
--   3. Adds get_my_profile() — a SECURITY DEFINER RPC that returns the
--      full profile row for the calling user (auth.uid()). This is the
--      replacement code path for loadPublicUser() / /auth/me /
--      /membership/status — anywhere the frontend needs the caller's own
--      email/is_premium/premium_expires_at.
--
-- Why column revoke + RPC (Option 2) instead of tightening the SELECT
-- RLS policy to auth_id = auth.uid() (Option 3):
--   The catalog, course cards, instructor profile page, and search
--   results all read OTHER users' rows (embedded via
--   users!courses_instructor_id_fkey(first_name,last_name,premium_tier)
--   or via explicit users?role=eq.instructor filters). If we tightened
--   the SELECT policy to self-only, every one of those joins would go
--   dark. Keeping the policy permissive and narrowing the column grant
--   is the cheapest surgical fix: public display fields remain joinable,
--   private fields are only reachable through the RPC that checks
--   auth.uid() server-side.
--
-- Frontend coupling (must ship in the same deploy or before):
--   index.html must call rpc('get_my_profile') from:
--     - loadPublicUser()                  (line ~800)
--     - /auth/me handler                  (line ~1061, currently dead code)
--     - /membership/status handler        (line ~1218)
--   and the /instructors/:id handler at line ~998 must drop created_at
--   from its column projection (it's no longer in the public grant and
--   the renderer at line ~1986 never displays it anyway).
--
-- Safe to re-run.

BEGIN;

-- ---------------------------------------------------------------------
-- 1. Narrow the column-level SELECT grant on public.users.
--    Drop the Phase 2 wide grant and re-grant only the public subset.
-- ---------------------------------------------------------------------
REVOKE SELECT ON public.users FROM anon, authenticated;

GRANT SELECT (
  id,
  first_name,
  last_name,
  role,
  company,
  bio,
  title,
  avatar_url,
  premium_tier,
  auth_id            -- needed by memberships + users UPDATE RLS policies; already public via courses.claimed_auth_id
) ON public.users TO anon, authenticated;


-- ---------------------------------------------------------------------
-- 2. get_my_profile() — SECURITY DEFINER, returns the full profile row
--    for auth.uid()'s user. This is the ONLY code path that can read
--    email / is_premium / premium_expires_at / created_at / updated_at
--    from PostgREST after this migration.
-- ---------------------------------------------------------------------
CREATE OR REPLACE FUNCTION get_my_profile()
RETURNS json
LANGUAGE plpgsql
SECURITY DEFINER
SET search_path = public
AS $$
DECLARE
  v_user users%ROWTYPE;
BEGIN
  IF auth.uid() IS NULL THEN
    RAISE EXCEPTION 'not_authenticated';
  END IF;

  SELECT * INTO v_user FROM users WHERE auth_id = auth.uid();
  IF NOT FOUND THEN
    RAISE EXCEPTION 'user_row_missing'
      USING HINT = 'Sign out and back in.';
  END IF;

  RETURN json_build_object(
    'id',                 v_user.id,
    'email',              v_user.email,
    'first_name',         v_user.first_name,
    'last_name',          v_user.last_name,
    'role',               v_user.role,
    'company',            v_user.company,
    'bio',                v_user.bio,
    'title',              v_user.title,
    'avatar_url',         v_user.avatar_url,
    'is_premium',         v_user.is_premium,
    'premium_tier',       v_user.premium_tier,
    'premium_expires_at', v_user.premium_expires_at,
    'created_at',         v_user.created_at,
    'updated_at',         v_user.updated_at
  );
END
$$;

GRANT EXECUTE ON FUNCTION get_my_profile() TO authenticated;

NOTIFY pgrst, 'reload schema';


-- ---------------------------------------------------------------------
-- 3. Verify: print the final column-level SELECT grant and confirm the
--    RPC is registered + SECURITY DEFINER.
-- ---------------------------------------------------------------------
SELECT 'users SELECT column privs (should list only the 9 public fields for anon+authenticated)' AS section,
       grantee, privilege_type, column_name
  FROM information_schema.column_privileges
 WHERE table_schema='public' AND table_name='users'
   AND privilege_type='SELECT'
   AND grantee IN ('anon','authenticated')
 ORDER BY grantee, column_name;

SELECT 'get_my_profile RPC present + SECURITY DEFINER' AS section,
       proname, prosecdef
  FROM pg_proc WHERE proname='get_my_profile';

COMMIT;
