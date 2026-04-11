-- Phase 3: close direct write access to public.courses.
--
-- After Phase 1 (additive) and Phase 2 (users RLS tightened) the courses
-- table still has three wide-open write policies (see schema.sql lines
-- 247-249). Any authenticated PostgREST client can INSERT/UPDATE/DELETE
-- any course row; ownership is only checked client-side in index.html,
-- which is trivially bypassable.
--
-- Phase 3:
--   0. Backfills claimed_auth_id from instructor_id for legacy courses
--      so update_claimed_course / delete_claimed_course still work on
--      them after the REVOKE.
--   1. Adds create_course(payload jsonb) RPC (SECURITY DEFINER).
--   2. Extends update_claimed_course whitelist to include category_id.
--   3. Adds set_my_courses_featured(boolean) RPC so /membership/subscribe
--      can still toggle featured status without direct UPDATE rights.
--   4. Drops the three wide-open courses write policies.
--   5. REVOKEs INSERT/UPDATE/DELETE on courses from anon + authenticated.
--
-- Safe to re-run.

BEGIN;

-- ---------------------------------------------------------------------
-- 0. Backfill claimed_auth_id for legacy instructor-owned courses.
-- ---------------------------------------------------------------------
UPDATE courses
   SET claimed_auth_id = u.auth_id,
       claimed_at      = COALESCE(courses.claimed_at, now())
  FROM users u
 WHERE courses.instructor_id = u.id
   AND courses.claimed_auth_id IS NULL
   AND u.auth_id IS NOT NULL;


-- ---------------------------------------------------------------------
-- 1. create_course(jsonb) — create a brand-new course as the caller.
-- ---------------------------------------------------------------------
CREATE OR REPLACE FUNCTION create_course(p_payload jsonb)
RETURNS json
LANGUAGE plpgsql
SECURITY DEFINER
SET search_path = public
AS $$
DECLARE
  v_user_id    int;
  v_is_premium boolean;
  v_category   int  := NULLIF(p_payload->>'category_id','')::int;
  v_title      text := COALESCE(NULLIF(p_payload->>'title',''), 'Untitled course');
  v_slug       text;
  v_free_count int;
  v_course_id  int;
BEGIN
  IF auth.uid() IS NULL THEN
    RAISE EXCEPTION 'not_authenticated'
      USING HINT = 'You must be signed in to create a course.';
  END IF;

  SELECT id, COALESCE(is_premium,false)
    INTO v_user_id, v_is_premium
    FROM users
   WHERE auth_id = auth.uid();
  IF v_user_id IS NULL THEN
    RAISE EXCEPTION 'user_row_missing'
      USING HINT = 'Sign out and back in.';
  END IF;

  IF v_category IS NULL THEN
    RAISE EXCEPTION 'category_required'
      USING HINT = 'Please choose a category for this course.';
  END IF;

  -- Enforce the 5-course free-tier limit (mirrors the old client-side check).
  IF NOT v_is_premium THEN
    SELECT count(*) INTO v_free_count
      FROM courses
     WHERE claimed_auth_id = auth.uid();
    IF v_free_count >= 5 THEN
      RAISE EXCEPTION 'course_limit_reached'
        USING HINT = 'Free accounts are limited to 5 courses. Upgrade to add more.';
    END IF;
  END IF;

  -- Promote learner → instructor on first create.
  UPDATE users SET role = 'instructor', updated_at = now()
   WHERE id = v_user_id AND role = 'learner';

  -- Compute slug: slugify the title, fall back to 'course', append epoch if taken.
  v_slug := regexp_replace(lower(v_title), '[^a-z0-9]+', '-', 'g');
  v_slug := regexp_replace(v_slug, '(^-+|-+$)', '', 'g');
  IF v_slug = '' OR v_slug IS NULL THEN
    v_slug := 'course';
  END IF;
  IF EXISTS (SELECT 1 FROM courses WHERE slug = v_slug) THEN
    v_slug := v_slug || '-' || extract(epoch from now())::bigint;
  END IF;

  INSERT INTO courses (
    title, slug, short_description, description,
    category_id, instructor_id,
    price, original_price, currency,
    level, format, duration_hours, image_url,
    course_language, delivery, location, timezone_info,
    start_date, end_date, status,
    claimed_auth_id, claimed_at, created_at, updated_at
  ) VALUES (
    v_title,
    v_slug,
    NULLIF(p_payload->>'short_description',''),
    NULLIF(p_payload->>'description',''),
    v_category,
    v_user_id,
    COALESCE(NULLIF(p_payload->>'price','')::numeric, 0),
    NULLIF(p_payload->>'original_price','')::numeric,
    COALESCE(NULLIF(p_payload->>'currency',''), 'USD'),
    COALESCE(NULLIF(p_payload->>'level',''), 'intermediate'),
    COALESCE(NULLIF(p_payload->>'format',''), 'self-paced'),
    COALESCE(NULLIF(p_payload->>'duration_hours','')::numeric, 0),
    NULLIF(p_payload->>'image_url',''),
    NULLIF(p_payload->>'course_language',''),
    COALESCE(NULLIF(p_payload->>'delivery',''), 'online'),
    NULLIF(p_payload->>'location',''),
    NULLIF(p_payload->>'timezone_info',''),
    NULLIF(p_payload->>'start_date','')::date,
    NULLIF(p_payload->>'end_date','')::date,
    COALESCE(NULLIF(p_payload->>'status',''), 'draft'),
    auth.uid(),
    now(),
    now(),
    now()
  )
  RETURNING id INTO v_course_id;

  RETURN json_build_object('ok', true, 'course_id', v_course_id, 'slug', v_slug);
END
$$;

GRANT EXECUTE ON FUNCTION create_course(jsonb) TO authenticated;


-- ---------------------------------------------------------------------
-- 2. Extend update_claimed_course to cover category_id.
--    Body is identical to migration 001 except for the extra line in
--    the UPDATE list. GRANT is already in place from Phase 1.
-- ---------------------------------------------------------------------
CREATE OR REPLACE FUNCTION update_claimed_course(p_course_id int, p_patch jsonb)
RETURNS json
LANGUAGE plpgsql
SECURITY DEFINER
SET search_path = public
AS $$
DECLARE
  v_course courses%ROWTYPE;
BEGIN
  IF auth.uid() IS NULL THEN
    RAISE EXCEPTION 'not_authenticated';
  END IF;

  SELECT * INTO v_course FROM courses WHERE id = p_course_id;
  IF NOT FOUND THEN RAISE EXCEPTION 'course_not_found'; END IF;
  IF v_course.claimed_auth_id IS NULL OR v_course.claimed_auth_id <> auth.uid() THEN
    RAISE EXCEPTION 'not_owner';
  END IF;

  UPDATE courses SET
    title             = COALESCE(p_patch->>'title',             title),
    short_description = COALESCE(p_patch->>'short_description', short_description),
    description       = COALESCE(p_patch->>'description',       description),
    category_id       = COALESCE(NULLIF(p_patch->>'category_id','')::int, category_id),
    price             = COALESCE((p_patch->>'price')::numeric,  price),
    original_price    = COALESCE((p_patch->>'original_price')::numeric, original_price),
    currency          = COALESCE(p_patch->>'currency',          currency),
    level             = COALESCE(p_patch->>'level',             level),
    format            = COALESCE(p_patch->>'format',            format),
    duration_hours    = COALESCE((p_patch->>'duration_hours')::numeric, duration_hours),
    image_url         = COALESCE(p_patch->>'image_url',         image_url),
    course_language   = COALESCE(p_patch->>'course_language',   course_language),
    delivery          = COALESCE(p_patch->>'delivery',          delivery),
    location          = COALESCE(p_patch->>'location',          location),
    timezone_info     = COALESCE(p_patch->>'timezone_info',     timezone_info),
    start_date        = COALESCE(NULLIF(p_patch->>'start_date','')::date, start_date),
    end_date          = COALESCE(NULLIF(p_patch->>'end_date','')::date,   end_date),
    status            = COALESCE(p_patch->>'status',            status),
    source_url        = COALESCE(p_patch->>'source_url',        source_url),
    updated_at        = now()
  WHERE id = p_course_id;

  RETURN json_build_object('ok', true);
END
$$;


-- ---------------------------------------------------------------------
-- 3. set_my_courses_featured(boolean) — /membership/subscribe callback.
-- ---------------------------------------------------------------------
CREATE OR REPLACE FUNCTION set_my_courses_featured(p_is_featured boolean)
RETURNS json
LANGUAGE plpgsql
SECURITY DEFINER
SET search_path = public
AS $$
DECLARE
  v_count int;
BEGIN
  IF auth.uid() IS NULL THEN
    RAISE EXCEPTION 'not_authenticated';
  END IF;

  WITH upd AS (
    UPDATE courses
       SET is_featured = p_is_featured,
           updated_at  = now()
     WHERE claimed_auth_id = auth.uid()
    RETURNING id
  )
  SELECT count(*) INTO v_count FROM upd;

  RETURN json_build_object('ok', true, 'updated_count', v_count);
END
$$;

GRANT EXECUTE ON FUNCTION set_my_courses_featured(boolean) TO authenticated;


-- ---------------------------------------------------------------------
-- 4. Drop the three wide-open courses write policies.
--    Keep "Public read published courses" — the catalog must stay public.
-- ---------------------------------------------------------------------
DROP POLICY IF EXISTS "Instructors insert courses"     ON public.courses;
DROP POLICY IF EXISTS "Instructors update own courses" ON public.courses;
DROP POLICY IF EXISTS "Instructors delete own courses" ON public.courses;


-- ---------------------------------------------------------------------
-- 5. REVOKE direct table writes + reload PostgREST schema cache.
-- ---------------------------------------------------------------------
REVOKE INSERT, UPDATE, DELETE ON public.courses FROM anon, authenticated;

NOTIFY pgrst, 'reload schema';


-- ---------------------------------------------------------------------
-- 6. Verify: printed during apply.
-- ---------------------------------------------------------------------
SELECT 'courses table privs (INSERT/UPDATE/DELETE should NOT appear for anon/authenticated)' AS section,
       grantee, privilege_type
  FROM information_schema.table_privileges
 WHERE table_schema='public' AND table_name='courses'
   AND grantee IN ('anon','authenticated')
 ORDER BY grantee, privilege_type;

SELECT 'courses policies remaining' AS section, policyname, cmd
  FROM pg_policies
 WHERE schemaname='public' AND tablename='courses'
 ORDER BY policyname;

SELECT 'Phase-3 RPCs present' AS section, proname
  FROM pg_proc
 WHERE proname IN ('create_course','update_claimed_course','set_my_courses_featured')
 ORDER BY proname;

COMMIT;
