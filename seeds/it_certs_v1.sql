-- =====================================================================
-- UpskillCompass — IT & Certification seed (v1)
--
-- Adds 3 new categories (Project Management, Agile & Scrum, IT &
-- Cybersecurity), 7 ghost instructor users, and 11 real certification
-- training programs from public provider pages. All durations 1-20 days
-- and well above the >$50/day threshold.
--
-- Also moves CAL 1 / CAL 2 from "Innovation & Digital" to the new
-- "Agile & Scrum" category, where they belong.
--
-- Idempotent: ON CONFLICT DO NOTHING for slugs/emails; conditional
-- WHERE-clauses on the CAL re-categorization. Safe to re-run.
-- =====================================================================

BEGIN;

-- ---------------------------------------------------------------------
-- 1. New categories
-- ---------------------------------------------------------------------
INSERT INTO categories (name, slug, icon, description) VALUES
  ('Project Management', 'project-management', '📋',
   'PMP, PRINCE2, and Lean Six Sigma — the credentials project leaders earn to run regulated, high-stakes programs.'),
  ('Agile & Scrum', 'agile-scrum', '⚡',
   'Scrum Master, Product Owner, and agile-leadership credentials from Scrum Alliance, Scrum.org, and the broader agile community.'),
  ('IT & Cybersecurity', 'it-cybersecurity', '🔐',
   'Cloud, infrastructure, and security certifications from AWS, ISC2, CompTIA, PeopleCert and other major bodies.')
ON CONFLICT (slug) DO NOTHING;


-- ---------------------------------------------------------------------
-- 2. Re-categorize CAL 1 / CAL 2 into Agile & Scrum
-- (they were placed in innovation-digital in the prior seed batch)
-- ---------------------------------------------------------------------
UPDATE courses
   SET category_id = (SELECT id FROM categories WHERE slug = 'agile-scrum'),
       updated_at  = now()
 WHERE slug IN ('scrum-alliance-certified-agile-leader-1',
                'scrum-alliance-certified-agile-leader-2')
   AND category_id = (SELECT id FROM categories WHERE slug = 'innovation-digital');


-- ---------------------------------------------------------------------
-- 3. New ghost instructor users (one per cert body / training network)
-- ---------------------------------------------------------------------
INSERT INTO users (email, first_name, last_name, role, company, title, bio, created_at, updated_at)
VALUES
  ('training@pmi.org', 'PMI', 'ATP Network', 'instructor',
    'Project Management Institute (Authorized Training Partners)',
    'PMI Authorized Training Partner Instructors',
    'The Project Management Institute is the global cert body behind the PMP credential. From July 2026, all 35 contact-hour PMP training must come from PMI Authorized Training Partners (ATPs) such as PMTI, PMLG, Training Camp, and 4PMTI.',
    now(), now()),

  ('info@peoplecert.org', 'PeopleCert', 'Accredited Trainers', 'instructor',
    'PeopleCert',
    'PeopleCert-Accredited Training Organisations',
    'PeopleCert administers the PRINCE2 and ITIL 4 frameworks (acquired from AXELOS in 2021). Training is delivered by PeopleCert-accredited training organisations worldwide.',
    now(), now()),

  ('info@iassc.org', 'IASSC', 'Approved Trainers', 'instructor',
    'International Association for Six Sigma Certification',
    'IASSC-Accredited Training Providers',
    'IASSC is a vendor-neutral Lean Six Sigma certification body whose Green Belt and Black Belt exams are recognized internationally. The certification is exam-only; training is delivered by IASSC-accredited partners.',
    now(), now()),

  ('training@asq.org', 'ASQ', 'Faculty', 'instructor',
    'American Society for Quality',
    'ASQ Master Trainers',
    'ASQ has set the standard for quality and Six Sigma certifications since 1946. Its Certified Six Sigma Green Belt (CSSGB) requires three years of relevant experience in addition to the exam.',
    now(), now()),

  ('info@scrum.org', 'Scrum.org', 'Professional Scrum Trainers', 'instructor',
    'Scrum.org',
    'Professional Scrum Trainers (PSTs)',
    'Scrum.org was founded by Scrum co-creator Ken Schwaber in 2009 and runs the Professional Scrum Master (PSM) and Professional Scrum Product Owner (PSPO) credential tracks.',
    now(), now()),

  ('aws-training@amazon.com', 'AWS', 'Training & Certification', 'instructor',
    'Amazon Web Services',
    'AWS Authorized Instructors',
    'AWS Training and Certification offers official learning paths leading to credentials such as Solutions Architect (Associate, Professional), Cloud Practitioner, and Security. Boot camps are delivered by AWS Authorized Training Partners.',
    now(), now()),

  ('info@isc2.org', 'ISC2', 'Authorized Trainers', 'instructor',
    'ISC2',
    'ISC2 Authorized Instructors',
    'ISC2 is the cert body behind CISSP, CCSP, SSCP, and other senior cybersecurity credentials. CISSP is widely held by security architects, CISOs, and government cyber roles.',
    now(), now()),

  ('info@comptia.org', 'CompTIA', 'Authorized Partners', 'instructor',
    'CompTIA',
    'CompTIA Authorized Training Partners',
    'CompTIA runs vendor-neutral entry-to-mid-level IT certifications including Security+, Network+, A+, Cloud+, and CySA+. Security+ is approved under DoD 8140 for many U.S. federal cybersecurity roles.',
    now(), now())
ON CONFLICT (email) DO NOTHING;


-- ---------------------------------------------------------------------
-- 4. New courses
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

  -- ── Project Management ────────────────────────────────────────
  ('training@pmi.org', 'project-management',
    'PMP® Exam Prep Boot Camp (35 PDU / PMI ATP)',
    'pmp-exam-prep-boot-camp',
    'Intensive 4-day classroom or virtual boot camp covering PMI''s PMBOK 7 content, predictive + agile + hybrid approaches. Delivers the 35 contact hours PMI requires for the PMP application and is delivered exclusively by PMI Authorized Training Partners as of July 2026. Exam voucher and pass guarantees vary by ATP.',
    '4-day PMP boot camp meeting PMI''s 35 contact-hour requirement (ATP-delivered).',
    1795.00, 'USD', 'advanced', 'live', 35,
    true, true,
    'https://www.4pmti.com/pmp-boot-camp/', '4pmti.com', 'training@pmi.org'),

  ('info@peoplecert.org', 'project-management',
    'PRINCE2® Foundation + Practitioner (Combined)',
    'prince2-foundation-practitioner-combined',
    'Combined PRINCE2 Foundation and Practitioner training, typically 3-5 days of instructor-led delivery (~32 hours). Covers PRINCE2 7th-edition principles, themes and processes; both Foundation and Practitioner exam vouchers usually included. Delivered by PeopleCert-accredited training organisations.',
    'PRINCE2 Foundation + Practitioner combo, 3-5 days, both exams included.',
    1499.00, 'USD', 'intermediate', 'live', 32,
    false, true,
    'https://www.prince2.com/usa/training/prince2/foundation-practitioner', 'prince2.com', 'info@peoplecert.org'),

  ('info@iassc.org', 'project-management',
    'IASSC Lean Six Sigma Green Belt — Training & Exam',
    'iassc-lean-six-sigma-green-belt',
    '5-day instructor-led IASSC-accredited Lean Six Sigma Green Belt program (~40 hours). Covers Define, Measure, Analyze, Improve and Control phases plus Lean process improvement. IASSC has no prerequisite to sit the exam; price typically bundles training and the $395 exam fee.',
    '5-day IASSC-accredited Lean Six Sigma Green Belt with exam included.',
    1500.00, 'USD', 'intermediate', 'live', 40,
    false, false,
    'https://www.iassc.org/six-sigma-certification/lean-six-sigma-green-belt-certification/', 'iassc.org', 'info@iassc.org'),

  ('training@asq.org', 'project-management',
    'ASQ Certified Six Sigma Green Belt (CSSGB)',
    'asq-certified-six-sigma-green-belt',
    'ASQ''s Six Sigma Green Belt credential, requiring three years of relevant experience plus the CSSGB exam. ASQ-led prep courses run roughly 5 days / 40 hours; exam fee is $469 for non-members and $369 for ASQ members.',
    'ASQ Six Sigma Green Belt with 3-year experience prereq. 5-day prep + exam.',
    1800.00, 'USD', 'advanced', 'live', 40,
    false, false,
    'https://asq.org/cert/six-sigma-green-belt', 'asq.org', 'training@asq.org'),

  -- ── Agile & Scrum ─────────────────────────────────────────────
  ('info@scrumalliance.org', 'agile-scrum',
    'Certified ScrumMaster® (CSM)',
    'scrum-alliance-certified-scrummaster',
    'Scrum Alliance''s flagship entry-level Scrum credential. 14-16 hours of live training (typically 2 days, virtual or in-person) delivered by a Certified Scrum Trainer (CST), followed by a 50-question online exam. Course fee includes two exam attempts and a 2-year Scrum Alliance membership.',
    '2-day Scrum Alliance CSM with CST trainer, exam, and 2-year membership.',
    1295.00, 'USD', 'beginner', 'live', 16,
    true, true,
    'https://www.scrumalliance.org/get-certified/scrum-master-track/certified-scrummaster', 'scrumalliance.org', 'info@scrumalliance.org'),

  ('info@scrumalliance.org', 'agile-scrum',
    'Certified Scrum Product Owner® (CSPO)',
    'scrum-alliance-certified-scrum-product-owner',
    'Scrum Alliance''s product-owner credential. 14-16 hours of CST-led training (typically 2 days) on backlog management, stakeholder collaboration, and product strategy in a Scrum context. Includes a 2-year Scrum Alliance membership.',
    '2-day Scrum Alliance CSPO for product owners. CST-led with 2-year membership.',
    1295.00, 'USD', 'intermediate', 'live', 16,
    false, false,
    'https://www.scrumalliance.org/get-certified/product-owner-track/certified-scrum-product-owner', 'scrumalliance.org', 'info@scrumalliance.org'),

  ('info@scrum.org', 'agile-scrum',
    'Professional Scrum Master™ I (PSM I) Training',
    'scrum-org-professional-scrum-master-i',
    'Scrum.org''s 2-day Professional Scrum Master I training, delivered by Professional Scrum Trainers (PSTs). Covers the Scrum Guide, servant leadership, and applied facilitation. Course fee usually includes a PSM I exam attempt; the credential never expires.',
    'Scrum.org 2-day PSM I with PST-delivered curriculum and lifetime credential.',
    1295.00, 'USD', 'beginner', 'live', 16,
    false, false,
    'https://www.scrum.org/courses/professional-scrum-master-training', 'scrum.org', 'info@scrum.org'),

  -- ── IT & Cybersecurity ────────────────────────────────────────
  ('aws-training@amazon.com', 'it-cybersecurity',
    'AWS Certified Solutions Architect — Associate Boot Camp',
    'aws-certified-solutions-architect-associate-boot-camp',
    '3-day intensive boot camp preparing for the AWS SAA-C03 exam, covering AWS core services, well-architected design, security, and cost optimization. Delivered by AWS Authorized Training Partners; package typically includes the $150 AWS exam voucher and a hands-on lab environment.',
    'AWS Solutions Architect Associate 3-day boot camp with hands-on labs and voucher.',
    2495.00, 'USD', 'intermediate', 'live', 24,
    true, true,
    'https://aws.amazon.com/certification/certified-solutions-architect-associate/', 'aws.amazon.com', 'aws-training@amazon.com'),

  ('info@isc2.org', 'it-cybersecurity',
    'CISSP® Certification Boot Camp',
    'cissp-certification-boot-camp',
    '6-day intensive boot camp covering all eight CISSP CBK domains (Security & Risk, Asset Security, Architecture, Comms & Network Security, IAM, SecAssess & Testing, SecOps, Software Dev Security). Delivered by ISC2 Authorized Instructors; pass rates of 92-96% advertised by leading providers. Typically bundled with the $749 exam voucher and onsite VUE testing.',
    '6-day CISSP boot camp covering all 8 ISC2 CBK domains with exam voucher.',
    4495.00, 'USD', 'advanced', 'live', 48,
    true, false,
    'https://www.isc2.org/Certifications/CISSP', 'isc2.org', 'info@isc2.org'),

  ('info@comptia.org', 'it-cybersecurity',
    'CompTIA Security+ (SY0-701) Boot Camp',
    'comptia-security-plus-boot-camp',
    '5-day instructor-led boot camp aligned to the SY0-701 objectives: threats & vulnerabilities, architecture, security operations, governance & risk. Boot-camp packages typically include the $425 exam voucher and a free second attempt. Approved under DoD 8140 for many U.S. federal cybersecurity roles.',
    '5-day Security+ boot camp aligned to SY0-701 with exam voucher and retake.',
    2495.00, 'USD', 'intermediate', 'live', 40,
    false, true,
    'https://www.comptia.org/certifications/security', 'comptia.org', 'info@comptia.org'),

  ('info@peoplecert.org', 'it-cybersecurity',
    'ITIL® 4 Foundation',
    'itil-4-foundation',
    'Entry-level ITIL 4 certification covering the service value system, four dimensions of service management, and 34 ITIL practices. 16 hours of training plus a 60-minute, 40-question exam (26 correct to pass). Delivered as a 2-3 day instructor-led course or self-paced; PeopleCert-accredited providers worldwide.',
    'ITIL 4 Foundation: 2-3 day course, 16 training hours, exam included.',
    999.00, 'USD', 'beginner', 'live', 16,
    false, false,
    'https://www.peoplecert.org/browse-certifications/it-governance-and-service-management/ITIL-1/itil-4-foundation-2565', 'peoplecert.org', 'info@peoplecert.org')

) AS t(inst_email, cat_slug,
       title, slug, description, short_description,
       price, currency, level, format, duration_hours,
       is_featured, is_bestseller,
       source_url, source_domain, claim_email)
JOIN users u      ON u.email = t.inst_email
JOIN categories c ON c.slug  = t.cat_slug
ON CONFLICT (slug) DO NOTHING;

COMMIT;
