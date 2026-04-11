-- Backfill courses.source_url and courses.source_domain from known mappings.
-- Data derived from /tmp/upskill-img-venv/out/_report.json (22 courses with real source URLs).
-- Safe to re-run: only sets values where not already set.

BEGIN;

UPDATE courses SET source_url='https://www.wenell.se/utbildning/ledarskap/ny-som-chef',                                                        source_domain='wenell.se'              WHERE id=162 AND source_url IS NULL;
UPDATE courses SET source_url='https://www.hjartum.se/kurs/ledarskapsutbildning/ny-som-chef',                                                  source_domain='hjartum.se'             WHERE id=163 AND source_url IS NULL;
UPDATE courses SET source_url='https://www.advantumkompetens.se/oppna-utbildningar/ledarskap/ny-som-chef/',                                    source_domain='advantumkompetens.se'   WHERE id=164 AND source_url IS NULL;
UPDATE courses SET source_url='https://www.hjartum.se/kurs/ledarskapsutbildning/att-leda-utan-att-vara-chef',                                  source_domain='hjartum.se'             WHERE id=165 AND source_url IS NULL;
UPDATE courses SET source_url='https://www.wenell.se/utbildning/ledarskap/coachande-ledarskap',                                                source_domain='wenell.se'              WHERE id=166 AND source_url IS NULL;
UPDATE courses SET source_url='https://www.berghs.se/kurs/ai-for-framtidens-ledare-kurs-dagtid-berghs/',                                       source_domain='berghs.se'              WHERE id=167 AND source_url IS NULL;
UPDATE courses SET source_url='https://www.foretagsuniversitetet.se/oeppna-kurser/kompetensutveckling/Ledarskap/UGL-utveckling-grupp-och-ledare', source_domain='foretagsuniversitetet.se' WHERE id=168 AND source_url IS NULL;
UPDATE courses SET source_url='https://www.ihm.se/utbildningar/management/utvecklande-ledarskap/',                                             source_domain='ihm.se'                 WHERE id=169 AND source_url IS NULL;
UPDATE courses SET source_url='https://www.wenell.se/utbildning/ledarskap/ledarskap-och-kommunikation',                                        source_domain='wenell.se'              WHERE id=170 AND source_url IS NULL;
UPDATE courses SET source_url='https://www.wenell.se/utbildning/ledarskap/leda-genom-andra-chefer',                                            source_domain='wenell.se'              WHERE id=171 AND source_url IS NULL;
UPDATE courses SET source_url='https://www.foretagsuniversitetet.se/oeppna-kurser/kompetensutveckling/Ledarskap/Konflikthantering-och-svaara-samtal', source_domain='foretagsuniversitetet.se' WHERE id=172 AND source_url IS NULL;
UPDATE courses SET source_url='https://www.foretagsuniversitetet.se/oeppna-kurser/kompetensutveckling/Ledarskap/Kommunikation-i-ledarskapet', source_domain='foretagsuniversitetet.se' WHERE id=173 AND source_url IS NULL;
UPDATE courses SET source_url='https://www.hjartum.se/kurs/ledarskapsutbildning/certifierad-ledare',                                           source_domain='hjartum.se'             WHERE id=174 AND source_url IS NULL;
UPDATE courses SET source_url='https://www.canea.se/utbildningar/forandringsledning-forandringsledarskap',                                     source_domain='canea.se'               WHERE id=175 AND source_url IS NULL;
UPDATE courses SET source_url='https://chef.se/chefakademin/ledarskapsutbildningar/leda-utan-att-vara-chef/',                                  source_domain='chef.se'                WHERE id=176 AND source_url IS NULL;
UPDATE courses SET source_url='https://www.foretagsuniversitetet.se/oeppna-kurser/kompetensutveckling/Ledarskap/Ledarskap-i-praktiken',       source_domain='foretagsuniversitetet.se' WHERE id=177 AND source_url IS NULL;
UPDATE courses SET source_url='https://www.efl.se/program/affarsmannaskap/efl-ledarskap-i-organisationer/',                                    source_domain='efl.se'                 WHERE id=178 AND source_url IS NULL;
UPDATE courses SET source_url='https://www.efl.se/program/affarsmannaskap/leading-change-framgangsrikt-forandringsledarskap/',                 source_domain='efl.se'                 WHERE id=179 AND source_url IS NULL;
UPDATE courses SET source_url='https://www.berghs.se/kurs/ai-for-forandringsledare-professional-dagtid/',                                      source_domain='berghs.se'              WHERE id=180 AND source_url IS NULL;
UPDATE courses SET source_url='https://www.exedsse.se/program/chef-och-ledare/',                                                               source_domain='exedsse.se'             WHERE id=181 AND source_url IS NULL;
UPDATE courses SET source_url='https://www.exedsse.se/program/executive-leadership-program/',                                                  source_domain='exedsse.se'             WHERE id=182 AND source_url IS NULL;
UPDATE courses SET source_url='https://kthexecutiveschool.se/executive-program-in-industrial-management-2026-spring/',                         source_domain='kthexecutiveschool.se'  WHERE id=183 AND source_url IS NULL;

-- Verification
SELECT source_domain, count(*) AS courses
  FROM courses
 WHERE source_domain IS NOT NULL
 GROUP BY source_domain
 ORDER BY courses DESC, source_domain;

COMMIT;
