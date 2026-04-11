-- Phase 4b: write-lockdown for public.modules and public.lessons.
--
-- Pre-state (confirmed via live query 2026-04-11 after Phase 3):
--   modules + lessons each had 3 wide-open write policies
--   (Insert/Update/Delete) with USING(true) / WITH CHECK(true), and
--   anon + authenticated both held INSERT/UPDATE/DELETE table grants.
--   A grep of index.html showed the frontend only READS these tables
--   (course detail renderer, lines 974 + 980). No write paths exist.
--
-- This migration:
--   1. Drops the six wide-open write policies.
--   2. REVOKEs INSERT/UPDATE/DELETE from anon + authenticated.
--   3. Keeps the `Public read modules` / `Public read lessons` SELECT
--      policies intact so the public course catalog keeps working.
--
-- When a course-builder UI is actually built, Phase 5 will add
-- add_module / add_lesson / update_lesson / ... RPCs that verify
-- ownership via the parent course's claimed_auth_id.
--
-- Safe to re-run.

BEGIN;

-- ---------------------------------------------------------------------
-- 1. Drop the six wide-open write policies.
-- ---------------------------------------------------------------------
DROP POLICY IF EXISTS "Insert modules" ON public.modules;
DROP POLICY IF EXISTS "Update modules" ON public.modules;
DROP POLICY IF EXISTS "Delete modules" ON public.modules;
DROP POLICY IF EXISTS "Insert lessons" ON public.lessons;
DROP POLICY IF EXISTS "Update lessons" ON public.lessons;
DROP POLICY IF EXISTS "Delete lessons" ON public.lessons;


-- ---------------------------------------------------------------------
-- 2. REVOKE direct writes. SELECT stays intact for the public catalog.
-- ---------------------------------------------------------------------
REVOKE INSERT, UPDATE, DELETE ON public.modules FROM anon, authenticated;
REVOKE INSERT, UPDATE, DELETE ON public.lessons FROM anon, authenticated;

NOTIFY pgrst, 'reload schema';


-- ---------------------------------------------------------------------
-- 3. Verify.
-- ---------------------------------------------------------------------
SELECT 'modules/lessons table privs (INSERT/UPDATE/DELETE should NOT appear)' AS section,
       table_name, grantee, privilege_type
  FROM information_schema.table_privileges
 WHERE table_schema='public' AND table_name IN ('modules','lessons')
   AND grantee IN ('anon','authenticated')
 ORDER BY table_name, grantee, privilege_type;

SELECT 'modules/lessons policies remaining (should be Public read only)' AS section,
       tablename, policyname, cmd
  FROM pg_policies
 WHERE schemaname='public' AND tablename IN ('modules','lessons')
 ORDER BY tablename, policyname;

COMMIT;
