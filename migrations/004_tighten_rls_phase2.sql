-- Phase 2: tighten RLS after the Supabase-Auth-based index.html is live.
--
-- Scope is intentionally VERY CONSERVATIVE:
--   (a) password_hash is never exposed via PostgREST.
--   (b) users.UPDATE is restricted to the user's own row.
--
-- Everything else (wide-open courses INSERT/UPDATE/DELETE via PostgREST,
-- wide-open users SELECT of non-sensitive columns, etc.) is LEFT IN PLACE
-- for this phase so the legacy instructor dashboard and catalog keep
-- working. Phase 3 will introduce a create_course RPC and then revoke
-- direct write access on courses.
--
-- Safe to re-run.

BEGIN;

-- ---------------------------------------------------------------------
-- 1. password_hash is never exposed via PostgREST.
-- ---------------------------------------------------------------------
-- In PostgreSQL, table-level SELECT covers every column. Column-level
-- REVOKE only works AFTER the table-level SELECT is removed and then
-- re-granted column by column (minus the one we want to hide).
REVOKE SELECT             ON public.users FROM anon, authenticated;
REVOKE SELECT (password_hash) ON public.users FROM anon, authenticated;  -- belt+braces
GRANT  SELECT (
  id, email, first_name, last_name, role, company, bio, title,
  avatar_url, created_at, updated_at, is_premium, premium_expires_at,
  premium_tier, auth_id
) ON public.users TO anon, authenticated;

-- PostgREST also stores a schema cache; this forces it to reload.
NOTIFY pgrst, 'reload schema';

-- ---------------------------------------------------------------------
-- 2. Users can only UPDATE their own row.
-- ---------------------------------------------------------------------
-- Old policy was USING(true) which let any authenticated client PATCH
-- any row (including flipping is_premium=true on somebody else).
DROP POLICY IF EXISTS "Users update own profile" ON public.users;
DROP POLICY IF EXISTS "Users update own row"     ON public.users;
CREATE POLICY "Users update own row"
  ON public.users
  FOR UPDATE
  USING      (auth_id = auth.uid())
  WITH CHECK (auth_id = auth.uid());

-- Also forbid anonymous UPDATE entirely (belt-and-braces).
REVOKE UPDATE ON public.users FROM anon;

-- ---------------------------------------------------------------------
-- 3. Verify: print the surviving column privileges + user policies.
-- ---------------------------------------------------------------------
SELECT 'users column privileges (password_hash should show NOTHING)' AS section,
       grantee, privilege_type, column_name
  FROM information_schema.column_privileges
 WHERE table_schema='public' AND table_name='users'
   AND grantee IN ('anon','authenticated')
   AND column_name='password_hash'
 ORDER BY grantee;

SELECT 'users policies' AS section, policyname, cmd
  FROM pg_policies
 WHERE schemaname='public' AND tablename='users'
 ORDER BY policyname;

COMMIT;
