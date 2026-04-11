-- =====================================================================
-- UpskillCompass — Phase 1 migration (ADDITIVE, safe to run on live site)
--
-- Adds:
--   • users.auth_id  — links legacy integer-keyed users to Supabase Auth
--   • courses.source_url / source_domain / claim_email / claimed_auth_id / claimed_at
--   • users_public   — safe view that excludes password_hash
--   • handle_new_auth_user() trigger — auto-creates users row on signup
--   • claim_course(p_course_id)          — SECURITY DEFINER
--   • claim_all_in_domain(p_course_ids)  — SECURITY DEFINER
--   • release_claimed_course(p_course_id)— SECURITY DEFINER
--   • list_claimable_in_domain()         — SECURITY DEFINER
--
-- This file does NOT drop any existing policies.
-- It does NOT drop users.password_hash.
-- Existing signup/signin with the custom bcrypt scheme keeps working.
-- Apply Phase 2 (002_tighten_rls.sql) only AFTER the new index.html is deployed.
-- =====================================================================

BEGIN;

-- ---------------------------------------------------------------------
-- 1. users.auth_id — link to auth.users
-- ---------------------------------------------------------------------
ALTER TABLE users
  ADD COLUMN IF NOT EXISTS auth_id UUID UNIQUE REFERENCES auth.users(id) ON DELETE SET NULL;
CREATE INDEX IF NOT EXISTS idx_users_auth_id ON users(auth_id);

-- Make password_hash nullable so new Supabase-Auth users don't need one
ALTER TABLE users ALTER COLUMN password_hash DROP NOT NULL;


-- ---------------------------------------------------------------------
-- 2. courses: source + claim tracking columns
-- ---------------------------------------------------------------------
ALTER TABLE courses
  ADD COLUMN IF NOT EXISTS source_url      TEXT,
  ADD COLUMN IF NOT EXISTS source_domain   TEXT,
  ADD COLUMN IF NOT EXISTS claim_email     TEXT,
  ADD COLUMN IF NOT EXISTS claimed_auth_id UUID REFERENCES auth.users(id) ON DELETE SET NULL,
  ADD COLUMN IF NOT EXISTS claimed_at      TIMESTAMPTZ;
CREATE INDEX IF NOT EXISTS idx_courses_source_domain ON courses(lower(source_domain));
CREATE INDEX IF NOT EXISTS idx_courses_claimed_auth  ON courses(claimed_auth_id);
CREATE INDEX IF NOT EXISTS idx_courses_claim_email   ON courses(lower(claim_email));


-- ---------------------------------------------------------------------
-- 3. users_public view (safe columns only — never password_hash)
-- ---------------------------------------------------------------------
-- Re-create the view even if it exists so column list stays in sync
DROP VIEW IF EXISTS users_public;
CREATE VIEW users_public AS
  SELECT
    id,
    first_name,
    last_name,
    role,
    title,
    bio,
    avatar_url,
    company,
    created_at
  FROM users;
GRANT SELECT ON users_public TO anon, authenticated;


-- ---------------------------------------------------------------------
-- 4. Trigger: on auth.users INSERT, create matching public.users row
-- ---------------------------------------------------------------------
CREATE OR REPLACE FUNCTION handle_new_auth_user()
RETURNS trigger
LANGUAGE plpgsql
SECURITY DEFINER
SET search_path = public
AS $$
DECLARE
  v_first text := COALESCE(NULLIF(NEW.raw_user_meta_data->>'first_name',''), split_part(NEW.email,'@',1));
  v_last  text := COALESCE(NULLIF(NEW.raw_user_meta_data->>'last_name',''), '');
  v_role  text := COALESCE(NULLIF(NEW.raw_user_meta_data->>'role',''), 'learner');
BEGIN
  -- If a row with this email already exists (legacy/seed), link it.
  -- Otherwise insert a new row. The 'instructor' role is applied on first claim,
  -- not here, so default new signups to 'learner'.
  INSERT INTO users (email, auth_id, first_name, last_name, role, created_at, updated_at)
  VALUES (NEW.email, NEW.id, v_first, v_last, v_role, now(), now())
  ON CONFLICT (email) DO UPDATE
    SET auth_id    = EXCLUDED.auth_id,
        updated_at = now()
    WHERE users.auth_id IS NULL;  -- don't overwrite if already linked
  RETURN NEW;
END
$$;

DROP TRIGGER IF EXISTS on_auth_user_created ON auth.users;
CREATE TRIGGER on_auth_user_created
  AFTER INSERT ON auth.users
  FOR EACH ROW
  EXECUTE FUNCTION handle_new_auth_user();


-- ---------------------------------------------------------------------
-- 5. claim_course(int) — claim a single course
-- ---------------------------------------------------------------------
CREATE OR REPLACE FUNCTION claim_course(p_course_id INT)
RETURNS json
LANGUAGE plpgsql
SECURITY DEFINER
SET search_path = public
AS $$
DECLARE
  v_email text := lower(auth.jwt()->>'email');
  v_verified text := auth.jwt()->>'email_verified';
  v_course courses%ROWTYPE;
  v_domain text;
  v_user_id int;
BEGIN
  IF v_email IS NULL OR v_email = '' THEN
    RAISE EXCEPTION 'not_authenticated' USING HINT = 'You must be signed in to claim a course.';
  END IF;

  -- Require verified email. Supabase sets email_verified=true once the user clicks the confirmation link.
  IF v_verified IS NULL OR v_verified NOT IN ('true','t','1') THEN
    RAISE EXCEPTION 'email_not_verified' USING HINT = 'Please confirm your email address first.';
  END IF;

  SELECT * INTO v_course FROM courses WHERE id = p_course_id;
  IF NOT FOUND THEN
    RAISE EXCEPTION 'course_not_found';
  END IF;

  IF v_course.claimed_auth_id IS NOT NULL THEN
    IF v_course.claimed_auth_id = auth.uid() THEN
      RETURN json_build_object('ok', true, 'course_id', p_course_id, 'note', 'already_yours');
    END IF;
    RAISE EXCEPTION 'already_claimed';
  END IF;

  v_domain := lower(split_part(v_email, '@', 2));

  IF NOT (
       (v_course.claim_email   IS NOT NULL AND lower(v_course.claim_email)   = v_email)
    OR (v_course.source_domain IS NOT NULL AND lower(v_course.source_domain) = v_domain)
  ) THEN
    RAISE EXCEPTION 'email_not_authorized'
      USING HINT = 'Your email address does not match this course. Contact hello@upskillcompass.com for help.';
  END IF;

  SELECT id INTO v_user_id FROM users WHERE auth_id = auth.uid();
  IF v_user_id IS NULL THEN
    RAISE EXCEPTION 'user_row_missing' USING HINT = 'Sign out and sign back in, then try again.';
  END IF;

  -- Bump user role to instructor so dashboard/manage-courses works
  UPDATE users SET role = 'instructor', updated_at = now()
   WHERE id = v_user_id AND role = 'learner';

  UPDATE courses SET
    claimed_auth_id = auth.uid(),
    claimed_at      = now(),
    instructor_id   = v_user_id,
    updated_at      = now()
  WHERE id = p_course_id;

  RETURN json_build_object('ok', true, 'course_id', p_course_id);
END
$$;

GRANT EXECUTE ON FUNCTION claim_course(int) TO authenticated;


-- ---------------------------------------------------------------------
-- 6. claim_all_in_domain(int[]) — claim many courses at once
-- If p_course_ids is NULL, claims every unclaimed course that matches
-- the caller's email / domain. If provided, restricts to that set.
-- ---------------------------------------------------------------------
CREATE OR REPLACE FUNCTION claim_all_in_domain(p_course_ids INT[] DEFAULT NULL)
RETURNS json
LANGUAGE plpgsql
SECURITY DEFINER
SET search_path = public
AS $$
DECLARE
  v_email text := lower(auth.jwt()->>'email');
  v_verified text := auth.jwt()->>'email_verified';
  v_domain text;
  v_user_id int;
  v_claimed_count int;
BEGIN
  IF v_email IS NULL OR v_email = '' THEN
    RAISE EXCEPTION 'not_authenticated';
  END IF;
  IF v_verified IS NULL OR v_verified NOT IN ('true','t','1') THEN
    RAISE EXCEPTION 'email_not_verified';
  END IF;

  v_domain := lower(split_part(v_email, '@', 2));

  SELECT id INTO v_user_id FROM users WHERE auth_id = auth.uid();
  IF v_user_id IS NULL THEN
    RAISE EXCEPTION 'user_row_missing';
  END IF;

  UPDATE users SET role = 'instructor', updated_at = now()
    WHERE id = v_user_id AND role = 'learner';

  WITH to_claim AS (
    SELECT id FROM courses
    WHERE claimed_auth_id IS NULL
      AND (
        (claim_email   IS NOT NULL AND lower(claim_email)   = v_email)
        OR (source_domain IS NOT NULL AND lower(source_domain) = v_domain)
      )
      AND (p_course_ids IS NULL OR id = ANY(p_course_ids))
  ),
  upd AS (
    UPDATE courses SET
      claimed_auth_id = auth.uid(),
      claimed_at      = now(),
      instructor_id   = v_user_id,
      updated_at      = now()
    WHERE id IN (SELECT id FROM to_claim)
    RETURNING id
  )
  SELECT count(*) INTO v_claimed_count FROM upd;

  RETURN json_build_object('ok', true, 'claimed_count', v_claimed_count);
END
$$;

GRANT EXECUTE ON FUNCTION claim_all_in_domain(int[]) TO authenticated;


-- ---------------------------------------------------------------------
-- 7. release_claimed_course(int) — owner gives up a claim
-- ---------------------------------------------------------------------
CREATE OR REPLACE FUNCTION release_claimed_course(p_course_id INT)
RETURNS json
LANGUAGE plpgsql
SECURITY DEFINER
SET search_path = public
AS $$
BEGIN
  IF auth.uid() IS NULL THEN
    RAISE EXCEPTION 'not_authenticated';
  END IF;

  UPDATE courses
     SET claimed_auth_id = NULL,
         claimed_at      = NULL,
         updated_at      = now()
   WHERE id = p_course_id
     AND claimed_auth_id = auth.uid();

  IF NOT FOUND THEN
    RAISE EXCEPTION 'not_owner';
  END IF;

  RETURN json_build_object('ok', true);
END
$$;

GRANT EXECUTE ON FUNCTION release_claimed_course(int) TO authenticated;


-- ---------------------------------------------------------------------
-- 8. list_claimable_in_domain() — what the signed-in user could claim
-- ---------------------------------------------------------------------
CREATE OR REPLACE FUNCTION list_claimable_in_domain()
RETURNS TABLE(
  id int,
  slug text,
  title text,
  source_domain text,
  match_type text
)
LANGUAGE plpgsql
SECURITY DEFINER
SET search_path = public
AS $$
DECLARE
  v_email text := lower(auth.jwt()->>'email');
  v_domain text;
BEGIN
  IF v_email IS NULL OR v_email = '' THEN RETURN; END IF;
  v_domain := lower(split_part(v_email, '@', 2));

  RETURN QUERY
    SELECT
      c.id,
      c.slug,
      c.title,
      c.source_domain,
      CASE
        WHEN c.claim_email IS NOT NULL AND lower(c.claim_email) = v_email THEN 'email'
        WHEN c.source_domain IS NOT NULL AND lower(c.source_domain) = v_domain THEN 'domain'
        ELSE NULL
      END AS match_type
    FROM courses c
    WHERE c.claimed_auth_id IS NULL
      AND (
        (c.claim_email   IS NOT NULL AND lower(c.claim_email)   = v_email)
        OR (c.source_domain IS NOT NULL AND lower(c.source_domain) = v_domain)
      )
    ORDER BY c.title;
END
$$;

GRANT EXECUTE ON FUNCTION list_claimable_in_domain() TO authenticated;


-- ---------------------------------------------------------------------
-- 9. update_claimed_course(int, jsonb) — owner-only course patch
-- Accepts a jsonb patch limited to editable columns. Silently ignores
-- unknown keys so callers can't sneak in claimed_auth_id etc.
-- ---------------------------------------------------------------------
CREATE OR REPLACE FUNCTION update_claimed_course(p_course_id INT, p_patch JSONB)
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

GRANT EXECUTE ON FUNCTION update_claimed_course(int, jsonb) TO authenticated;


-- ---------------------------------------------------------------------
-- 10. delete_claimed_course(int) — owner hard-delete
-- ---------------------------------------------------------------------
CREATE OR REPLACE FUNCTION delete_claimed_course(p_course_id INT)
RETURNS json
LANGUAGE plpgsql
SECURITY DEFINER
SET search_path = public
AS $$
DECLARE
  v_owner UUID;
BEGIN
  IF auth.uid() IS NULL THEN RAISE EXCEPTION 'not_authenticated'; END IF;

  SELECT claimed_auth_id INTO v_owner FROM courses WHERE id = p_course_id;
  IF v_owner IS NULL OR v_owner <> auth.uid() THEN
    RAISE EXCEPTION 'not_owner';
  END IF;

  -- Cascade-delete dependencies that don't have ON DELETE CASCADE yet
  DELETE FROM enrollments WHERE course_id = p_course_id;
  DELETE FROM wishlist    WHERE course_id = p_course_id;
  DELETE FROM reviews     WHERE course_id = p_course_id;
  DELETE FROM orders      WHERE course_id = p_course_id;
  -- modules/lessons already cascade via FK
  DELETE FROM courses WHERE id = p_course_id;

  RETURN json_build_object('ok', true);
END
$$;

GRANT EXECUTE ON FUNCTION delete_claimed_course(int) TO authenticated;


COMMIT;
