# Supabase Performance Optimization

## Indexing

### Create Index

```sql
CREATE INDEX idx_posts_user_id ON posts(user_id);
CREATE INDEX idx_posts_created_at ON posts(created_at DESC);
CREATE INDEX idx_posts_status_created ON posts(status, created_at DESC);
```

### Unique Index

```sql
CREATE UNIQUE INDEX idx_profiles_email ON profiles(email);
```

### Partial Index

```sql
CREATE INDEX idx_posts_published ON posts(created_at DESC)
WHERE status = 'published';
```

### GIN Index (Full-text, JSONB, Arrays)

```sql
CREATE INDEX idx_posts_tags ON posts USING GIN(tags);
CREATE INDEX idx_posts_metadata ON posts USING GIN(metadata);
CREATE INDEX idx_posts_fts ON posts USING GIN(to_tsvector('english', title || ' ' || content));
```

### Check Missing Indexes

```sql
SELECT schemaname, relname, seq_scan, idx_scan,
  CASE WHEN seq_scan > 0 THEN round(100.0 * idx_scan / (seq_scan + idx_scan), 2)
  ELSE 100 END AS idx_ratio
FROM pg_stat_user_tables
WHERE seq_scan > 1000
ORDER BY seq_scan DESC;
```

## Query Optimization

### Select Only Needed Columns

```typescript
// Bad
const { data } = await supabase.from("posts").select("*");

// Good
const { data } = await supabase.from("posts").select("id, title, created_at");
```

### Use Pagination

```typescript
const { data } = await supabase.from("posts").select("id, title").range(0, 9); // First 10 rows

// Cursor-based (better for large datasets)
const { data } = await supabase
  .from("posts")
  .select("id, title")
  .gt("id", lastId)
  .order("id")
  .limit(10);
```

### Limit Nested Queries

```typescript
// Bad - fetches all comments
const { data } = await supabase.from("posts").select("*, comments(*)");

// Good - limit nested
const { data } = await supabase
  .from("posts")
  .select("*, comments(id, content).limit(5)");
```

### Use Count Efficiently

```typescript
// Get count without fetching data
const { count } = await supabase
  .from("posts")
  .select("*", { count: "exact", head: true });
```

### EXPLAIN ANALYZE

```sql
EXPLAIN ANALYZE SELECT * FROM posts WHERE user_id = 'uuid' ORDER BY created_at DESC LIMIT 10;
```

## Connection Pooling

### Supavisor (Built-in)

Use transaction mode for serverless:

```
# Connection string
postgres://user:pass@db.project.supabase.co:6543/postgres?pgbouncer=true
```

### Client-side Pooling

```typescript
const supabase = createClient(url, key, {
  db: {
    schema: "public",
  },
  global: {
    headers: { "x-connection-pool": "true" },
  },
});
```

## RLS Performance

### Optimize Policy Functions

```sql
-- Bad: subquery in every row check
CREATE POLICY "slow" ON posts FOR SELECT
USING (user_id IN (SELECT user_id FROM team_members WHERE team_id = current_setting('app.team_id')::uuid));

-- Good: use auth.uid() directly
CREATE POLICY "fast" ON posts FOR SELECT
USING (auth.uid() = user_id);
```

### Use Security Definer Functions

```sql
CREATE OR REPLACE FUNCTION get_user_team_ids()
RETURNS uuid[] AS $$
  SELECT array_agg(team_id) FROM team_members WHERE user_id = auth.uid();
$$ LANGUAGE sql SECURITY DEFINER STABLE;

CREATE POLICY "team_access" ON posts FOR SELECT
USING (team_id = ANY(get_user_team_ids()));
```

### Bypass RLS for Admin Operations

```typescript
// Use service role client (bypasses RLS)
const supabaseAdmin = createClient(url, serviceRoleKey);
const { data } = await supabaseAdmin.from("posts").select();
```

## Caching

### Client-side Caching (React Query)

```typescript
import { useQuery } from "@tanstack/react-query";

function usePosts(userId: string) {
  return useQuery({
    queryKey: ["posts", userId],
    queryFn: () => supabase.from("posts").select().eq("user_id", userId),
    staleTime: 5 * 60 * 1000, // 5 minutes
  });
}
```

### Edge Function Caching

```typescript
return new Response(JSON.stringify(data), {
  headers: {
    "Content-Type": "application/json",
    "Cache-Control": "public, max-age=60, s-maxage=300",
  },
});
```

## Materialized Views

```sql
CREATE MATERIALIZED VIEW post_stats AS
SELECT user_id, COUNT(*) as total_posts, SUM(views) as total_views
FROM posts GROUP BY user_id;

CREATE UNIQUE INDEX idx_post_stats_user ON post_stats(user_id);

-- Refresh periodically
REFRESH MATERIALIZED VIEW CONCURRENTLY post_stats;
```

## Batch Operations

### Bulk Insert

```typescript
const { data, error } = await supabase
  .from("posts")
  .insert(posts) // Array of objects
  .select();
```

### Bulk Upsert

```typescript
const { data, error } = await supabase
  .from("posts")
  .upsert(posts, { onConflict: "id" })
  .select();
```

## Database Functions for Complex Queries

```sql
CREATE OR REPLACE FUNCTION get_feed(p_user_id uuid, p_limit int DEFAULT 20)
RETURNS TABLE(id uuid, title text, author_name text) AS $$
BEGIN
  RETURN QUERY
  SELECT p.id, p.title, u.name
  FROM posts p
  JOIN users u ON p.user_id = u.id
  WHERE p.user_id IN (SELECT following_id FROM follows WHERE follower_id = p_user_id)
  ORDER BY p.created_at DESC
  LIMIT p_limit;
END;
$$ LANGUAGE plpgsql STABLE;
```

```typescript
const { data } = await supabase.rpc("get_feed", {
  p_user_id: userId,
  p_limit: 20,
});
```

## Monitoring

### Slow Query Log

```sql
ALTER SYSTEM SET log_min_duration_statement = 1000;  -- Log queries > 1s
SELECT pg_reload_conf();
```

### Table Statistics

```sql
SELECT relname, n_live_tup, n_dead_tup, last_vacuum, last_autovacuum
FROM pg_stat_user_tables ORDER BY n_dead_tup DESC;
```

### Index Usage

```sql
SELECT indexrelname, idx_scan, idx_tup_read, idx_tup_fetch
FROM pg_stat_user_indexes ORDER BY idx_scan DESC;
```
