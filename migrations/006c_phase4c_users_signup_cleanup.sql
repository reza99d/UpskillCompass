-- Phase 4c: clean up legacy signup/DELETE grants on public.users.
--
-- Pre-state (confirmed via live query 2026-04-11 after Phase 3):
--   public.users still had an "Allow public signup" INSERT policy
--   (USING WITH CHECK(true)) and both anon + authenticated held
--   INSERT and DELETE table grants. These are dead code: the current
--   signup path is the `handle_new_auth_user` SECURITY DEFINER trigger
--   on auth.users (owned by postgres, bypasses RLS/grants), and the
--   frontend has no DELETE-user code path at all.
--
-- This migration:
--   1. Drops the "Allow public signup" legacy policy.
--   2. REVOKEs INSERT + DELETE on public.users from anon + authenticated.
--   3. Leaves the column-level SELECT grant from Phase 2 and the
--      "Users update own row" policy from Phase 2 intact.
--
-- Trigger safety:
--   handle_new_auth_user is SECURITY DEFINER owned by postgres, so it
--   doesn't rely on these grants at all. New signups will continue to
--   auto-create their public.users row.
--
-- Safe to re-run.

BEGIN;

-- ---------------------------------------------------------------------
-- 1. Drop the legacy "Allow public signup" policy.
-- ---------------------------------------------------------------------
DROP POLICY IF EXISTS "Allow public signup" ON public.users;


-- ---------------------------------------------------------------------
-- 2. REVOKE the unused INSERT + DELETE grants.
-- ---------------------------------------------------------------------
REVOKE INSERT, DELETE ON public.users FROM anon, authenticated;

NOTIFY pgrst, 'reload schema';


-- ---------------------------------------------------------------------
-- 3. Verify.
-- ---------------------------------------------------------------------
SELECT 'users table privs (INSERT/DELETE should NOT appear for anon/authenticated)' AS section,
       grantee, privilege_type
  FROM information_schema.table_privileges
 WHERE table_schema='public' AND table_name='users'
   AND grantee IN ('anon','authenticated')
 ORDER BY grantee, privilege_type;

SELECT 'users policies remaining' AS section, policyname, cmd
  FROM pg_policies
 WHERE schemaname='public' AND tablename='users'
 ORDER BY policyname;

SELECT 'handle_new_auth_user trigger still present + SECURITY DEFINER' AS section,
       t.tgname, t.tgrelid::regclass AS table_on, p.proname, p.prosecdef
  FROM pg_trigger t
  JOIN pg_proc p ON p.oid = t.tgfoid
 WHERE t.tgname = 'on_auth_user_created';

COMMIT;
