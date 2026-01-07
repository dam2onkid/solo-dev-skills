# Supabase CLI

## Installation

```bash
npm install -g supabase
```

## Authentication

```bash
supabase login
supabase logout
```

## Project Setup

### Initialize Project

```bash
supabase init
```

Creates `supabase/` directory with config.toml

### Link to Remote Project

```bash
supabase link --project-ref <project-id>
```

Required for: `db push`, `db pull`, `db dump`

## Local Development

### Start Local Stack

```bash
supabase start
```

Starts: Postgres, Auth, Storage, Realtime, Edge Functions, Studio

### Stop Local Stack

```bash
supabase stop
supabase stop --no-backup  # Don't backup db
```

### Status

```bash
supabase status
```

Shows URLs and keys for local services

### Reset Database

```bash
supabase db reset
```

Recreates db, runs migrations and seed

## Database Migrations

### Create Migration

```bash
supabase migration new <name>
```

Creates `supabase/migrations/<timestamp>_<name>.sql`

### List Migrations

```bash
supabase migration list
```

### Push to Remote

```bash
supabase db push
supabase db push --dry-run  # Preview only
```

### Pull from Remote

```bash
supabase db pull
```

Creates migration from remote schema changes

### Diff Local vs Remote

```bash
supabase db diff
supabase db diff --linked  # Compare with remote
supabase db diff -f <name> # Save as migration
```

### Dump Schema

```bash
supabase db dump -f schema.sql
supabase db dump --data-only -f data.sql
```

## Seed Data

Create `supabase/seed.sql`:

```sql
INSERT INTO profiles (id, name) VALUES
  ('uuid-1', 'Alice'),
  ('uuid-2', 'Bob');
```

Applied on `db reset` or:

```bash
supabase db reset --linked
```

## Edge Functions

### Create Function

```bash
supabase functions new <name>
```

### Serve Locally

```bash
supabase functions serve
supabase functions serve <name> --env-file .env.local
```

### Deploy

```bash
supabase functions deploy <name>
supabase functions deploy  # All functions
supabase functions deploy <name> --no-verify-jwt
```

### Delete

```bash
supabase functions delete <name>
```

## Secrets

```bash
supabase secrets set KEY=value
supabase secrets set KEY1=val1 KEY2=val2
supabase secrets list
supabase secrets unset KEY
```

## Type Generation

```bash
supabase gen types typescript --local > types/supabase.ts
supabase gen types typescript --linked > types/supabase.ts
```

Use in code:

```typescript
import { Database } from "./types/supabase";

const supabase = createClient<Database>(url, key);
```

## Config (supabase/config.toml)

```toml
[api]
port = 54321

[db]
port = 54322

[studio]
port = 54323

[auth]
site_url = "http://localhost:3000"
redirect_urls = ["http://localhost:3000/auth/callback"]

[auth.external.google]
enabled = true
client_id = "env(GOOGLE_CLIENT_ID)"
secret = "env(GOOGLE_CLIENT_SECRET)"
```

## CI/CD

```yaml
# GitHub Actions
- name: Setup Supabase CLI
  uses: supabase/setup-cli@v1

- name: Link project
  run: supabase link --project-ref $PROJECT_ID
  env:
    SUPABASE_ACCESS_TOKEN: ${{ secrets.SUPABASE_ACCESS_TOKEN }}
    SUPABASE_DB_PASSWORD: ${{ secrets.SUPABASE_DB_PASSWORD }}

- name: Push migrations
  run: supabase db push
```

## Common Workflows

### New Feature with Migration

```bash
supabase migration new add_posts_table
# Edit migration file
supabase db reset  # Test locally
supabase db push   # Deploy to remote
```

### Pull Remote Changes

```bash
supabase db pull
supabase db reset  # Apply locally
```

### Generate Types After Schema Change

```bash
supabase db reset
supabase gen types typescript --local > types/supabase.ts
```
