---
name: supabase-dev
description: Build applications with Supabase backend-as-a-service. Use when implementing authentication (email/password, OAuth, magic links, phone OTP), database operations with Row Level Security (RLS), file storage (upload, download, signed URLs), realtime subscriptions (Postgres changes, broadcast, presence), or Edge Functions. Covers client initialization, security policies, and common patterns for React, Next.js, React Native, and Node.js applications.
---

# Supabase Dev

Open-source Firebase alternative providing Postgres database, authentication, storage, realtime, and edge functions.

## Client Initialization

```typescript
import { createClient } from "@supabase/supabase-js";

const supabase = createClient(
  process.env.SUPABASE_URL!,
  process.env.SUPABASE_ANON_KEY!
);
```

Server-side (with service role):

```typescript
const supabaseAdmin = createClient(
  process.env.SUPABASE_URL!,
  process.env.SUPABASE_SERVICE_ROLE_KEY!
);
```

## Core Features

### Authentication

- Email/password, magic links, phone OTP
- OAuth providers (Google, GitHub, Discord, etc.)
- Session management with JWT
- Reference: [references/authentication.md](references/authentication.md)

### Database

- Full Postgres with auto-generated REST API
- Row Level Security (RLS) for authorization
- Realtime subscriptions on table changes
- Reference: [references/database.md](references/database.md)
- Performance: [references/performance.md](references/performance.md)

### Storage

- File uploads with access control
- Signed URLs for private files
- Image transformations
- Reference: [references/storage.md](references/storage.md)

### Realtime

- Postgres Changes (INSERT/UPDATE/DELETE)
- Broadcast (pub/sub messaging)
- Presence (online status)
- Reference: [references/realtime.md](references/realtime.md)

### Edge Functions

- Deno-based serverless functions
- Deploy via Supabase CLI
- Reference: [references/edge-functions.md](references/edge-functions.md)

### CLI

- Local development, migrations, type generation
- Reference: [references/cli.md](references/cli.md)

## Environment Variables

Required in `.env`:

```
SUPABASE_URL=https://your-project.supabase.co
SUPABASE_ANON_KEY=your-anon-key
SUPABASE_SERVICE_ROLE_KEY=your-service-role-key  # Server-side only
```

## Common Patterns

### Protected Routes (React)

```typescript
const {
  data: { session },
} = await supabase.auth.getSession();
if (!session) redirect("/login");
```

### Server Components (Next.js)

```typescript
import { createServerClient } from "@supabase/ssr";
import { cookies } from "next/headers";

const supabase = createServerClient(
  process.env.SUPABASE_URL!,
  process.env.SUPABASE_ANON_KEY!,
  { cookies: { getAll: () => cookies().getAll() } }
);
```

### Error Handling

```typescript
const { data, error } = await supabase.from("table").select();
if (error) throw new Error(error.message);
```

## Security Best Practices

1. Always enable RLS on tables
2. Use `auth.uid()` in policies for user-specific access
3. Never expose service role key to client
4. Validate inputs before database operations
5. Use prepared statements (built into client)
