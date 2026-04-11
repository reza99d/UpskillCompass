-- Backfill courses.claim_email per course, discovered from research on source pages
-- on 2026-04-11. Emails are the best-effort per-course organizer address (instructor
-- where possible, otherwise the org-level inbox on the same domain).
-- See agent-a3c7e74eac5ec9bfd.jsonl for the full provenance table.
--
-- Safe to re-run: only sets values where not already set.

BEGIN;

UPDATE courses SET claim_email='dennis.lind@wenell.se'               WHERE id=162 AND claim_email IS NULL;
UPDATE courses SET claim_email='info@hjartum.se'                     WHERE id=163 AND claim_email IS NULL;
UPDATE courses SET claim_email='rebecca.cameron@advantumkompetens.se' WHERE id=164 AND claim_email IS NULL;
UPDATE courses SET claim_email='info@hjartum.se'                     WHERE id=165 AND claim_email IS NULL;
UPDATE courses SET claim_email='dennis.lind@wenell.se'               WHERE id=166 AND claim_email IS NULL;
UPDATE courses SET claim_email='info@berghs.se'                      WHERE id=167 AND claim_email IS NULL;
UPDATE courses SET claim_email='kurs@foretagsuniversitetet.se'       WHERE id=168 AND claim_email IS NULL;
UPDATE courses SET claim_email='elisabet.ek@ihm.se'                  WHERE id=169 AND claim_email IS NULL;
UPDATE courses SET claim_email='kristina.rosen@wenell.se'            WHERE id=170 AND claim_email IS NULL;
UPDATE courses SET claim_email='hakan.froden@wenell.se'              WHERE id=171 AND claim_email IS NULL;
UPDATE courses SET claim_email='kurs@foretagsuniversitetet.se'       WHERE id=172 AND claim_email IS NULL;
UPDATE courses SET claim_email='kurs@foretagsuniversitetet.se'       WHERE id=173 AND claim_email IS NULL;
UPDATE courses SET claim_email='info@hjartum.se'                     WHERE id=174 AND claim_email IS NULL;
UPDATE courses SET claim_email='info@canea.se'                       WHERE id=175 AND claim_email IS NULL;
UPDATE courses SET claim_email='info@chefakademin.se'                WHERE id=176 AND claim_email IS NULL;
UPDATE courses SET claim_email='kurs@foretagsuniversitetet.se'       WHERE id=177 AND claim_email IS NULL;
UPDATE courses SET claim_email='malin.borg@efl.se'                   WHERE id=178 AND claim_email IS NULL;
UPDATE courses SET claim_email='malin.borg@efl.se'                   WHERE id=179 AND claim_email IS NULL;
UPDATE courses SET claim_email='info@berghs.se'                      WHERE id=180 AND claim_email IS NULL;
UPDATE courses SET claim_email='dante.wester@hhs.se'                 WHERE id=181 AND claim_email IS NULL;
UPDATE courses SET claim_email='didrik.reutersward@hhs.se'           WHERE id=182 AND claim_email IS NULL;
UPDATE courses SET claim_email='ulf.anggard@es.kth.se'               WHERE id=183 AND claim_email IS NULL;

-- 176: Chefakademin uses chefakademin.se for org email despite URL being chef.se.
--      Update source_domain so @chefakademin.se staff still match via domain.
UPDATE courses SET source_domain='chefakademin.se'
 WHERE id=176 AND source_domain='chef.se';

-- Verification
SELECT id, source_domain, claim_email
  FROM courses
 WHERE id BETWEEN 162 AND 183
 ORDER BY id;

COMMIT;
