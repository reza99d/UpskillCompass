# UpskillCompass

Leadership-and-certification training discovery platform. Single-file
SPA backed by Supabase Cloud, served as a static site behind nginx.

Live: <https://upskillcompass.com>

## Stack

- **Frontend:** a single `index.html` (~2,580 lines). Vanilla JS, no bundler,
  vendored Supabase JS client and bcryptjs from CDN. i18n in four languages
  (en / sv / de / fr) via the `T` table near the top of the inline script.
- **Backend (prod):** Supabase Cloud — Postgres, Auth, Storage, RLS-locked
  REST + SECURITY DEFINER RPCs. The browser talks to Supabase directly.
- **Backend (local dev only):** `app.py` Flask + SQLite. Not deployed.
- **Hosting:** nginx static-SPA on a Hetzner box, `/var/www/upskillcompass/`.

## Layout

```
index.html              # the entire frontend
app.py                  # local-dev Flask backend (not deployed)
schema.sql              # canonical Postgres schema for Supabase
supabase_client.py      # thin Python wrapper around Supabase REST
seed_data.py            # original Python seed (early prototype)
migrations/             # numbered SQL migrations (auth, RLS, RPCs)
seeds/                  # SQL data seeds (real provider courses)
wireframes.html         # design reference
```

`migrations/` are schema changes (added columns, RLS policies, RPCs).
`seeds/` are data-only `INSERT`s, idempotent via `ON CONFLICT DO NOTHING`.

## Local dev

```bash
# Static preview (hits production Supabase Cloud — read-only data is fine)
python3 -m http.server 3457
open http://localhost:3457
```

Auth flows that send email (signup confirmation, magic link) require
Supabase Cloud's SMTP and won't fully complete from `localhost:3457`
unless the redirect URLs are added to the Supabase project's allow-list.

## Apply a migration or seed

`DATABASE_URL` lives in `.env` (gitignored). With `psql`:

```bash
psql "$DATABASE_URL" -f migrations/008_whatever.sql
```

Without `psql`, use `psycopg2`:

```bash
python3 -c "
import os, psycopg2
url = next(l.split('=',1)[1].strip() for l in open('.env') if l.startswith('DATABASE_URL='))
conn = psycopg2.connect(url)
conn.cursor().execute(open('seeds/courses_v2.sql').read())
conn.commit()"
```

## Deploy

`index.html` is the only artifact:

```bash
TS=$(date -u +%Y%m%d-%H%M%S)
ssh root@<server> "cp /var/www/upskillcompass/index.html /var/www/upskillcompass/index.html.bak.${TS}"
scp index.html root@<server>:/var/www/upskillcompass/index.html
```

No nginx restart needed.

## CI

`.github/workflows/syntax-check.yml` extracts the inline `<script>` from
`index.html` and runs `node --check` on it. This catches the class of bug
where a top-level `const` / `let` collision (or any parse error) would
silently break the entire page — the static header still renders but
nothing JS-driven appears.
