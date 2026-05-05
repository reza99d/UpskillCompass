-- =====================================================================
-- UpskillCompass — Seed batch v2: real executive-ed & certification
-- programs from public provider pages, all in the 1-20 day window
-- and well above the >$50/day threshold.
--
-- Pattern (consistent with phase 1 claim flow in 001_*):
--   • One "ghost" instructor user per provider (e.g. faculty@ccl.org)
--     with NULL auth_id and NULL password_hash. The trigger
--     handle_new_auth_user() will link a real signup to this row when
--     someone signs up with the same email; until then the listing is
--     attributed to the provider in a generic way.
--   • Each course has source_url / source_domain / claim_email set so
--     the existing claim_course / claim_all_in_domain SECURITY DEFINER
--     functions can match an instructor at that domain.
--
-- All descriptions paraphrase public marketing copy, never copy-paste.
-- All prices and durations come from the providers' own program pages
-- as of 2026-05; courses fall in the 1-20 day window per the spec.
--
-- Idempotent: ON CONFLICT DO NOTHING on email / slug, so re-running
-- this migration is safe.
-- =====================================================================

BEGIN;

-- ---------------------------------------------------------------------
-- 1. Ghost instructor users (one per provider)
-- ---------------------------------------------------------------------
INSERT INTO users (email, first_name, last_name, role, company, title, bio, created_at, updated_at)
VALUES
  ('faculty@ccl.org', 'CCL', 'Faculty', 'instructor',
    'Center for Creative Leadership',
    'Executive Coaches & Faculty',
    'Center for Creative Leadership has run research-driven leadership development since 1970. Its flagship Leadership Development Program has over 100,000 alumni worldwide and is consistently ranked among the top open-enrollment leadership programs.',
    now(), now()),
  ('faculty@imd.org', 'IMD', 'Faculty', 'instructor',
    'IMD Lausanne',
    'Executive Education Faculty',
    'IMD is a top-ranked Swiss business school for executive education, recognized in particular for its work on leadership transformation, high-performance teams, and business simulations.',
    now(), now()),
  ('faculty@insead.edu', 'INSEAD', 'Faculty', 'instructor',
    'INSEAD',
    'Executive Education Faculty',
    'INSEAD is a global business school with campuses in Fontainebleau, Singapore, Abu Dhabi and San Francisco, offering open-enrollment and custom executive programmes across leadership, strategy, and product.',
    now(), now()),
  ('exec-ed@stanford.edu', 'Stanford GSB', 'Exec Ed', 'instructor',
    'Stanford Graduate School of Business',
    'Executive Education Faculty',
    'Stanford GSB Executive Education delivers research-driven leadership programs at the intersection of business, technology, and innovation, drawing on the school''s Silicon Valley faculty and alumni network.',
    now(), now()),
  ('info@dalecarnegie.com', 'Dale Carnegie', 'Faculty', 'instructor',
    'Dale Carnegie & Associates',
    'Senior Trainers',
    'Dale Carnegie has trained over nine million professionals worldwide since 1912. Its ACCET-accredited programs cover communication, presentation skills, leadership and customer relations.',
    now(), now()),
  ('info@franklincovey.com', 'FranklinCovey', 'Faculty', 'instructor',
    'FranklinCovey',
    'Master Facilitators',
    'FranklinCovey is the home of The 7 Habits of Highly Effective People. The firm runs leadership academies and behavior-change programs in over 150 countries, with both live workshops and self-paced certificates.',
    now(), now()),
  ('info@coachingfederation.org', 'ICF', 'Accredited Trainers', 'instructor',
    'International Coaching Federation',
    'ICF-Accredited Coach Trainers',
    'The International Coaching Federation is the global standard-setter for professional coaching. ICF-accredited training programs lead to ACC, PCC and MCC credentials and follow ICF''s core competency framework.',
    now(), now()),
  ('info@scrumalliance.org', 'Scrum Alliance', 'Trainers', 'instructor',
    'Scrum Alliance',
    'Certified Trainers (CST / CAL Educator)',
    'Scrum Alliance is one of the largest agile certification bodies, with over a million Certified ScrumMasters worldwide. It accredits the Certified Agile Leader (CAL) track for executives leading agile transformations.',
    now(), now()),
  ('info@prosci.com', 'Prosci', 'Faculty', 'instructor',
    'Prosci',
    'Change Management Practitioners',
    'Prosci is the originator of the ADKAR change management model and runs the most widely recognized change-practitioner certification, used by Fortune 500 transformation teams.',
    now(), now()),
  ('info@uglkurser.se', 'UGL', 'Handledare', 'instructor',
    'Försvarshögskolan / UGL-arrangörer',
    'Certifierade UGL-handledare',
    'UGL (Utveckling av Grupp och Ledare) ägs av Försvarshögskolan och är Sveriges mest etablerade ledarskapskurs sedan 1981. Kursen genomförs som internat under fem sammanhängande dagar av certifierade handledare hos kvalitetssäkrade arrangörer.',
    now(), now())
ON CONFLICT (email) DO NOTHING;


-- ---------------------------------------------------------------------
-- 2. Courses (18 entries, all 1-20 days, all >$50/day equivalent)
-- ---------------------------------------------------------------------
INSERT INTO courses
  (instructor_id, category_id, title, slug, description, short_description,
   price, currency, level, format, duration_hours,
   status, is_featured, is_bestseller,
   source_url, source_domain, claim_email,
   created_at, updated_at)
SELECT u.id, c.id,
       t.title, t.slug, t.description, t.short_description,
       t.price, t.currency, t.level, t.format, t.duration_hours,
       'published', t.is_featured, t.is_bestseller,
       t.source_url, t.source_domain, t.claim_email,
       now(), now()
FROM (VALUES
  -- ── Executive Leadership (cat slug: executive-leadership) ────────
  ('faculty@ccl.org', 'executive-leadership',
    'Leadership Development Program (LDP)®',
    'ccl-leadership-development-program',
    'CCL''s flagship 5-day in-person program for mid-level leaders, run on a Sunday-evening to Friday cadence with 10 weeks of pre-work. Includes 360-degree assessments, peer feedback, the Looking Glass-style business simulation, and 1:1 sessions with an executive coach. Awards 3.5 CEUs in partnership with National University.',
    'CCL flagship: 5-day cohort with 360s, simulation, and an executive coach. 100,000+ alumni.',
    8250.00, 'USD', 'advanced', 'live', 40,
    true, true,
    'https://www.ccl.org/leadership-programs/leadership-development-program/', 'ccl.org', 'info@ccl.org'),

  ('faculty@ccl.org', 'executive-leadership',
    'Leading for Organizational Impact',
    'ccl-leading-for-organizational-impact',
    '5-day senior-leader program built around CCL''s Looking Glass, Inc.® business simulation. 3 months of pre-work including 360-degree feedback, self-assessments and an executive-coach debrief, followed by the on-site intensive on cross-boundary leadership and strategic perspective.',
    'Senior-leader 5-day intensive with the Looking Glass simulation and 360 feedback.',
    10950.00, 'USD', 'executive', 'live', 40,
    false, false,
    'https://www.ccl.org/leadership-programs/leading-organizational-impact-executive-training/', 'ccl.org', 'info@ccl.org'),

  ('faculty@imd.org', 'executive-leadership',
    'High Performance Leadership',
    'imd-high-performance-leadership',
    'IMD''s 6-day program for experienced leaders building high-performing teams. Combines leadership assessment, individual coaching, and applied team-dynamics exercises in Lausanne. Multiple cohorts run each year between April and December.',
    'IMD Lausanne 6-day program on leading high-performing teams. CHF 14,900.',
    14900.00, 'CHF', 'advanced', 'live', 48,
    true, false,
    'https://www.imd.org/leadership/hpl/leadership-training/admission/', 'imd.org', 'info@imd.org'),

  ('faculty@imd.org', 'executive-leadership',
    'Breakthrough Program for Senior Executives',
    'imd-breakthrough-program-for-senior-executives',
    'IMD''s 10-day senior-executive program designed to unlock breakthrough thinking on strategy, innovation and personal leadership. Delivered in Lausanne with the next cohort opening 09 June 2026.',
    'IMD 10-day program for senior executives focused on breakthrough strategic thinking.',
    25500.00, 'CHF', 'executive', 'live', 80,
    false, false,
    'https://www.imd.org/management/bpse/executive-leadership-program/', 'imd.org', 'info@imd.org'),

  ('faculty@insead.edu', 'executive-leadership',
    'High Impact Leadership Programme',
    'insead-high-impact-leadership-programme',
    'INSEAD''s 5-day Singapore-based programme for managers with 3-6 years of leadership experience. Delivered multiple times per year across April, May, September and November 2026 cohorts. Focus on personal leadership style, influence, and team performance.',
    'INSEAD 5-day Singapore programme for emerging leaders. Multiple 2026 cohorts.',
    16200.00, 'SGD', 'intermediate', 'live', 40,
    true, false,
    'https://www.insead.edu/executive-education/leadership/high-impact-leadership-programme/dates-fees', 'insead.edu', 'info@insead.edu'),

  ('exec-ed@stanford.edu', 'executive-leadership',
    'Executive Leadership Development',
    'stanford-executive-leadership-development',
    'Stanford GSB''s one-week residential program for senior executives. Curriculum spans business acumen, innovation, and leadership; the 2026 cohort runs the week of 19 July. Delivered on Stanford''s Knight Management Center campus.',
    'Stanford GSB 1-week residential on leadership, innovation, and business acumen.',
    17000.00, 'USD', 'executive', 'live', 40,
    false, false,
    'https://www.gsb.stanford.edu/exec-ed/programs/executive-leadership-development', 'stanford.edu', 'exec-ed@stanford.edu'),

  -- ── Communication (cat slug: communication) ──────────────────────
  ('info@dalecarnegie.com', 'communication',
    'Dale Carnegie Course',
    'dale-carnegie-course',
    'The flagship Dale Carnegie Course: 8 weekly sessions of roughly 3 hours each, focused on communication, human relations, and confidence under pressure. Live cohort format, ACCET-accredited, with optional ACE college-credit recommendation.',
    'Dale Carnegie''s flagship: 8 weekly sessions on communication and human relations.',
    2395.00, 'USD', 'intermediate', 'live', 24,
    false, true,
    'https://www.dalecarnegie.com/en', 'dalecarnegie.com', 'info@dalecarnegie.com'),

  ('info@franklincovey.com', 'communication',
    'The 7 Habits of Highly Effective People® Workshop',
    'franklincovey-7-habits-workshop',
    '2-day live workshop based on Stephen R. Covey''s framework. Covers proactivity, prioritization, win-win thinking, empathic listening, synergy, and renewal. Delivered in Benelux at €1,595 ex. VAT; equivalent live workshops run in dozens of countries.',
    'FranklinCovey 7 Habits live 2-day workshop. €1,595 ex. VAT.',
    1595.00, 'EUR', 'beginner', 'live', 16,
    true, false,
    'https://www.franklincovey-benelux.com/en/public-workshops/the-7-habits-of-highly-effective-people/', 'franklincovey.com', 'info@franklincovey.com'),

  -- ── Strategic Thinking (cat slug: strategic-thinking) ────────────
  ('faculty@insead.edu', 'strategic-thinking',
    'Product Leadership Programme',
    'insead-product-leadership-programme',
    'INSEAD''s 5-day programme on Fontainebleau campus for product leaders moving from execution to strategy. Next cohort: 29 June 2026. Covers product strategy, organization design, and leadership of cross-functional product teams.',
    'INSEAD 5-day programme for product leaders moving from execution to strategy.',
    9200.00, 'EUR', 'advanced', 'live', 40,
    false, false,
    'https://www.insead.edu/executive-education/partner-programmes/product-leadership-programme/dates-fees', 'insead.edu', 'info@insead.edu'),

  -- ── Team Building (cat slug: team-building) ──────────────────────
  ('info@uglkurser.se', 'team-building',
    'UGL — Utveckling av Grupp och Ledare',
    'ugl-utveckling-av-grupp-och-ledare',
    '5-dagars internatkurs ägd av Försvarshögskolan, genomförd av kvalitetssäkrade arrangörer i hela Sverige. Fokus på gruppdynamik, ledarskap, kommunikation och självkännedom; 8-12 deltagare per kurs. Pris varierar mellan arrangörer; angivet pris är typiskt och inkluderar kursavgift, material, kost och logi (exkl. moms).',
    'Sveriges mest etablerade ledarskapskurs: 5-dagars internat med 8-12 deltagare.',
    35000.00, 'SEK', 'intermediate', 'live', 40,
    true, true,
    'https://www.uglkurser.se/', 'uglkurser.se', 'info@uglkurser.se'),

  -- ── Change Management (cat slug: change-management) ──────────────
  ('info@prosci.com', 'change-management',
    'Prosci Change Management Certification (Online)',
    'prosci-change-management-certification-online',
    'Prosci''s flagship change-practitioner certification, online format. 3-5 days at roughly 8 hours of dedicated class time per day, plus ~1 hour of self-study on days 1 and 2. Includes ADKAR-based course materials and renewable digital toolkit.',
    'Prosci ADKAR certification, online: 3-5 days plus self-study and renewable toolkit.',
    4500.00, 'USD', 'intermediate', 'live', 32,
    true, false,
    'https://www.prosci.com/solutions/training-programs/change-management-certification-program', 'prosci.com', 'info@prosci.com'),

  ('info@prosci.com', 'change-management',
    'Prosci Change Management Certification (In-Person)',
    'prosci-change-management-certification-in-person',
    'In-person version of Prosci''s change-practitioner certification. 3-5 days, breakfast and lunch included, with the same ADKAR curriculum and renewable digital tools as the online format.',
    'Prosci ADKAR certification, in-person: 3-5 days with meals included.',
    4850.00, 'USD', 'intermediate', 'live', 32,
    false, false,
    'https://www.prosci.com/solutions/training-programs/change-management-certification-program', 'prosci.com', 'info@prosci.com'),

  -- ── Coaching & Mentoring (cat slug: coaching-mentoring) ──────────
  ('info@coachingfederation.org', 'coaching-mentoring',
    'ICF Associate Certified Coach (ACC) Training Path',
    'icf-associate-certified-coach-training',
    'ICF-accredited training pathway to the ACC credential: 60+ hours of training plus 10 hours of mentor coaching, performance evaluation, and the credentialing exam. Delivered by ICF-accredited providers (e.g. Co-Active, Coacharya, ICA) with hybrid live + asynchronous components.',
    'ICF-accredited path to the Associate Certified Coach credential. 60+ hours.',
    4305.00, 'USD', 'intermediate', 'hybrid', 60,
    true, true,
    'https://coachingfederation.org/credentialing/icf-credentials-overview/acc/', 'coachingfederation.org', 'info@coachingfederation.org'),

  ('info@coachingfederation.org', 'coaching-mentoring',
    'ICF Professional Certified Coach (PCC) Training Path',
    'icf-professional-certified-coach-training',
    'ICF-accredited training pathway to the PCC credential: 125+ hours of training and 10+ hours of mentor coaching, with performance evaluation and credentialing exam. Designed for coaches advancing past ACC into the PCC tier.',
    'ICF-accredited path to the Professional Certified Coach credential. 125+ hours.',
    7700.00, 'USD', 'advanced', 'hybrid', 125,
    false, false,
    'https://coachingfederation.org/credentialing/icf-credentials-overview/pcc/', 'coachingfederation.org', 'info@coachingfederation.org'),

  -- ── Innovation & Digital (cat slug: innovation-digital) ──────────
  ('info@scrumalliance.org', 'innovation-digital',
    'Certified Agile Leader 1 (CAL 1)',
    'scrum-alliance-certified-agile-leader-1',
    'Scrum Alliance''s entry-level executive credential for leaders driving agile transformation. 16 hours of live time with a Scrum Alliance-certified CAL educator (virtual or in-person), plus a digital badge and 2-year Scrum Alliance membership.',
    'Scrum Alliance CAL 1 — 16-hour executive agile-leadership credential.',
    2200.00, 'EUR', 'intermediate', 'live', 16,
    true, true,
    'https://www.scrumalliance.org/get-certified/agile-leader/cal-1', 'scrumalliance.org', 'info@scrumalliance.org'),

  ('info@scrumalliance.org', 'innovation-digital',
    'Certified Agile Leader 2 (CAL 2)',
    'scrum-alliance-certified-agile-leader-2',
    'CAL 2 builds on CAL 1 with deeper applied work on leading change, organizational design, and sustaining agile transformation. Typically delivered as a 3-day cohort by Scrum Alliance-approved CAL educators.',
    'Scrum Alliance CAL 2 — applied 3-day program building on CAL 1.',
    2700.00, 'EUR', 'advanced', 'live', 24,
    false, false,
    'https://www.scrumalliance.org/get-certified/agile-leader-track/cal-2', 'scrumalliance.org', 'info@scrumalliance.org'),

  ('faculty@insead.edu', 'innovation-digital',
    'Developing Emerging Leaders (Online)',
    'insead-developing-emerging-leaders-online',
    'INSEAD''s online programme for emerging leaders, delivered across 5 content weeks of asynchronous + live sessions. 2026 cohorts on 23 February and 4 May. Suited for first-time managers who can''t take a week off campus.',
    'INSEAD online emerging-leader programme — 5 content weeks asynchronous + live.',
    2050.00, 'EUR', 'intermediate', 'self-paced', 25,
    false, false,
    'https://www.insead.edu/executive-education/open-online-programmes/developing-emerging-leaders/dates-fees', 'insead.edu', 'info@insead.edu'),

  -- ── Personal Development (cat slug: personal-development) ────────
  ('info@franklincovey.com', 'personal-development',
    'The 7 Habits of Highly Effective People® Online + Knowledge Certificate',
    'franklincovey-7-habits-online-knowledge-certificate',
    'Self-paced version of the 7 Habits course (~30 hours of content) with the Knowledge Certificate awarded on passing the post-course exam. Lifetime access to the FranklinCovey Academy materials, suitable for individuals not enrolled via an employer.',
    'FranklinCovey 7 Habits self-paced course + Knowledge Certificate. ~30 hours.',
    899.00, 'USD', 'beginner', 'self-paced', 30,
    false, false,
    'https://www.franklincoveyacademy.com/courses/seven-habits-of-highly-effective-people/', 'franklincovey.com', 'info@franklincovey.com')

) AS t(inst_email, cat_slug,
       title, slug, description, short_description,
       price, currency, level, format, duration_hours,
       is_featured, is_bestseller,
       source_url, source_domain, claim_email)
JOIN users u      ON u.email = t.inst_email
JOIN categories c ON c.slug  = t.cat_slug
ON CONFLICT (slug) DO NOTHING;

COMMIT;
