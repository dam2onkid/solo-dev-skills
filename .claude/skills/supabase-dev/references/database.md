# Supabase Database

## CRUD Operations

### Select
```typescript
const { data, error } = await supabase
  .from('posts')
  .select('*')

const { data } = await supabase
  .from('posts')
  .select('id, title, author:users(name, avatar)')
  .eq('status', 'published')
  .order('created_at', { ascending: false })
  .limit(10)
```

### Insert
```typescript
const { data, error } = await supabase
  .from('posts')
  .insert({ title: 'Hello', content: 'World', user_id: userId })
  .select()
  .single()

const { data, error } = await supabase
  .from('posts')
  .insert([
    { title: 'Post 1', user_id: userId },
    { title: 'Post 2', user_id: userId }
  ])
  .select()
```

### Update
```typescript
const { data, error } = await supabase
  .from('posts')
  .update({ title: 'Updated Title' })
  .eq('id', postId)
  .select()
  .single()
```

### Upsert
```typescript
const { data, error } = await supabase
  .from('posts')
  .upsert({ id: postId, title: 'Upserted' })
  .select()
```

### Delete
```typescript
const { error } = await supabase
  .from('posts')
  .delete()
  .eq('id', postId)
```

## Filters

```typescript
.eq('column', 'value')        // equals
.neq('column', 'value')       // not equals
.gt('column', value)          // greater than
.gte('column', value)         // greater than or equal
.lt('column', value)          // less than
.lte('column', value)         // less than or equal
.like('column', '%pattern%')  // LIKE
.ilike('column', '%pattern%') // case-insensitive LIKE
.is('column', null)           // IS NULL
.in('column', [1, 2, 3])      // IN array
.contains('array_col', ['a']) // array contains
.or('col1.eq.a,col2.eq.b')    // OR condition
```

## Row Level Security (RLS)

### Enable RLS
```sql
ALTER TABLE posts ENABLE ROW LEVEL SECURITY;
```

### Policy: Users read own data
```sql
CREATE POLICY "Users can read own posts"
ON posts FOR SELECT
TO authenticated
USING (auth.uid() = user_id);
```

### Policy: Users insert own data
```sql
CREATE POLICY "Users can create posts"
ON posts FOR INSERT
TO authenticated
WITH CHECK (auth.uid() = user_id);
```

### Policy: Users update own data
```sql
CREATE POLICY "Users can update own posts"
ON posts FOR UPDATE
TO authenticated
USING (auth.uid() = user_id)
WITH CHECK (auth.uid() = user_id);
```

### Policy: Users delete own data
```sql
CREATE POLICY "Users can delete own posts"
ON posts FOR DELETE
TO authenticated
USING (auth.uid() = user_id);
```

### Policy: Public read access
```sql
CREATE POLICY "Anyone can read published posts"
ON posts FOR SELECT
TO anon, authenticated
USING (status = 'published');
```

### Policy: Role-based access
```sql
CREATE POLICY "Admins can do anything"
ON posts FOR ALL
TO authenticated
USING (
  EXISTS (
    SELECT 1 FROM profiles
    WHERE profiles.id = auth.uid()
    AND profiles.role = 'admin'
  )
);
```

## Foreign Key Relations

```typescript
const { data } = await supabase
  .from('posts')
  .select(`
    id,
    title,
    author:users!posts_user_id_fkey(id, name),
    comments(id, content, user:users(name))
  `)
```

## Aggregations

```typescript
const { count } = await supabase
  .from('posts')
  .select('*', { count: 'exact', head: true })

const { data } = await supabase
  .rpc('get_post_stats', { user_id: userId })
```

## Stored Procedures (RPC)

```sql
CREATE OR REPLACE FUNCTION get_post_stats(user_id uuid)
RETURNS TABLE(total_posts int, total_views int) AS $$
BEGIN
  RETURN QUERY
  SELECT COUNT(*)::int, SUM(views)::int
  FROM posts WHERE posts.user_id = $1;
END;
$$ LANGUAGE plpgsql;
```

```typescript
const { data, error } = await supabase.rpc('get_post_stats', {
  user_id: userId
})
```

## Transactions

Use database functions for transactions:
```sql
CREATE OR REPLACE FUNCTION transfer_credits(
  from_user uuid, to_user uuid, amount int
) RETURNS void AS $$
BEGIN
  UPDATE profiles SET credits = credits - amount WHERE id = from_user;
  UPDATE profiles SET credits = credits + amount WHERE id = to_user;
END;
$$ LANGUAGE plpgsql;
```
