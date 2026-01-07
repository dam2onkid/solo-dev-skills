# Supabase Edge Functions

## CLI Setup

```bash
npm install -g supabase
supabase login
supabase init  # if not already initialized
```

## Create Function

```bash
supabase functions new my-function
```

Creates `supabase/functions/my-function/index.ts`

## Function Template

```typescript
import { serve } from "https://deno.land/std@0.168.0/http/server.ts";
import { createClient } from "https://esm.sh/@supabase/supabase-js@2";

const corsHeaders = {
  "Access-Control-Allow-Origin": "*",
  "Access-Control-Allow-Headers":
    "authorization, x-client-info, apikey, content-type",
};

serve(async (req) => {
  if (req.method === "OPTIONS") {
    return new Response("ok", { headers: corsHeaders });
  }

  try {
    const supabase = createClient(
      Deno.env.get("SUPABASE_URL")!,
      Deno.env.get("SUPABASE_ANON_KEY")!,
      {
        global: {
          headers: { Authorization: req.headers.get("Authorization")! },
        },
      }
    );

    const {
      data: { user },
    } = await supabase.auth.getUser();
    if (!user) throw new Error("Unauthorized");

    const { name } = await req.json();

    return new Response(
      JSON.stringify({ message: `Hello ${name}!`, user_id: user.id }),
      { headers: { ...corsHeaders, "Content-Type": "application/json" } }
    );
  } catch (error) {
    return new Response(JSON.stringify({ error: error.message }), {
      status: 400,
      headers: { ...corsHeaders, "Content-Type": "application/json" },
    });
  }
});
```

## Deploy

```bash
supabase functions deploy my-function

supabase functions deploy my-function --no-verify-jwt
```

## Invoke from Client

```typescript
const { data, error } = await supabase.functions.invoke("my-function", {
  body: { name: "World" },
});
```

## Secrets Management

```bash
supabase secrets set MY_API_KEY=xxx

supabase secrets list

supabase secrets unset MY_API_KEY
```

Access in function:

```typescript
const apiKey = Deno.env.get("MY_API_KEY");
```

## Local Development

```bash
supabase start

supabase functions serve my-function --env-file .env.local
```

Test locally:

```bash
curl -i --request POST 'http://localhost:54321/functions/v1/my-function' \
  --header 'Authorization: Bearer SUPABASE_ANON_KEY' \
  --header 'Content-Type: application/json' \
  --data '{"name":"World"}'
```

## Database Access

```typescript
serve(async (req) => {
  const supabaseAdmin = createClient(
    Deno.env.get("SUPABASE_URL")!,
    Deno.env.get("SUPABASE_SERVICE_ROLE_KEY")!
  );

  const { data, error } = await supabaseAdmin
    .from("posts")
    .insert({ title: "From Edge Function" })
    .select()
    .single();

  return new Response(JSON.stringify(data), {
    headers: { "Content-Type": "application/json" },
  });
});
```

## Webhook Handler

```typescript
serve(async (req) => {
  const payload = await req.json();
  const signature = req.headers.get("x-webhook-signature");

  if (!verifySignature(payload, signature)) {
    return new Response("Invalid signature", { status: 401 });
  }

  // Process webhook
  console.log("Webhook received:", payload);

  return new Response("OK");
});
```

## Scheduled Functions (Cron)

Use pg_cron extension + database webhooks:

```sql
SELECT cron.schedule(
  'daily-cleanup',
  '0 0 * * *',
  $$
  SELECT net.http_post(
    url := 'https://your-project.supabase.co/functions/v1/cleanup',
    headers := '{"Authorization": "Bearer YOUR_ANON_KEY"}'::jsonb
  )
  $$
);
```

## Common Patterns

### Send Email (Resend)

```typescript
const RESEND_API_KEY = Deno.env.get("RESEND_API_KEY");

const res = await fetch("https://api.resend.com/emails", {
  method: "POST",
  headers: {
    Authorization: `Bearer ${RESEND_API_KEY}`,
    "Content-Type": "application/json",
  },
  body: JSON.stringify({
    from: "noreply@yourdomain.com",
    to: email,
    subject: "Hello",
    html: "<p>Hello World</p>",
  }),
});
```

### Stripe Webhook

```typescript
import Stripe from "https://esm.sh/stripe@13?target=deno";

const stripe = new Stripe(Deno.env.get("STRIPE_SECRET_KEY")!, {
  apiVersion: "2023-10-16",
});

serve(async (req) => {
  const body = await req.text();
  const sig = req.headers.get("stripe-signature")!;

  const event = stripe.webhooks.constructEvent(
    body,
    sig,
    Deno.env.get("STRIPE_WEBHOOK_SECRET")!
  );

  switch (event.type) {
    case "checkout.session.completed":
      // Handle successful payment
      break;
  }

  return new Response("OK");
});
```
