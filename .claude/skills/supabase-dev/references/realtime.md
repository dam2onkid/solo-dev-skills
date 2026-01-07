# Supabase Realtime

## Postgres Changes

### Subscribe to INSERT
```typescript
const channel = supabase
  .channel('posts-insert')
  .on(
    'postgres_changes',
    { event: 'INSERT', schema: 'public', table: 'posts' },
    (payload) => console.log('New post:', payload.new)
  )
  .subscribe()
```

### Subscribe to UPDATE
```typescript
const channel = supabase
  .channel('posts-update')
  .on(
    'postgres_changes',
    { event: 'UPDATE', schema: 'public', table: 'posts' },
    (payload) => console.log('Updated:', payload.old, '->', payload.new)
  )
  .subscribe()
```

### Subscribe to DELETE
```typescript
const channel = supabase
  .channel('posts-delete')
  .on(
    'postgres_changes',
    { event: 'DELETE', schema: 'public', table: 'posts' },
    (payload) => console.log('Deleted:', payload.old)
  )
  .subscribe()
```

### Subscribe to All Changes
```typescript
const channel = supabase
  .channel('posts-all')
  .on(
    'postgres_changes',
    { event: '*', schema: 'public', table: 'posts' },
    (payload) => console.log('Change:', payload.eventType, payload)
  )
  .subscribe()
```

### Filter by Column
```typescript
const channel = supabase
  .channel('user-posts')
  .on(
    'postgres_changes',
    {
      event: '*',
      schema: 'public',
      table: 'posts',
      filter: `user_id=eq.${userId}`
    },
    (payload) => console.log('My posts changed:', payload)
  )
  .subscribe()
```

## Broadcast (Pub/Sub)

### Send Message
```typescript
const channel = supabase.channel('room-1')

channel.subscribe((status) => {
  if (status === 'SUBSCRIBED') {
    channel.send({
      type: 'broadcast',
      event: 'cursor-move',
      payload: { x: 100, y: 200 }
    })
  }
})
```

### Receive Message
```typescript
const channel = supabase
  .channel('room-1')
  .on('broadcast', { event: 'cursor-move' }, (payload) => {
    console.log('Cursor moved:', payload)
  })
  .subscribe()
```

## Presence (Online Status)

### Track User
```typescript
const channel = supabase.channel('room-1')

channel
  .on('presence', { event: 'sync' }, () => {
    const state = channel.presenceState()
    console.log('Online users:', state)
  })
  .on('presence', { event: 'join' }, ({ key, newPresences }) => {
    console.log('User joined:', newPresences)
  })
  .on('presence', { event: 'leave' }, ({ key, leftPresences }) => {
    console.log('User left:', leftPresences)
  })
  .subscribe(async (status) => {
    if (status === 'SUBSCRIBED') {
      await channel.track({
        user_id: userId,
        online_at: new Date().toISOString()
      })
    }
  })
```

### Untrack User
```typescript
await channel.untrack()
```

## Unsubscribe

```typescript
await supabase.removeChannel(channel)

await supabase.removeAllChannels()
```

## React Hook Example

```typescript
function useRealtimePosts(userId: string) {
  const [posts, setPosts] = useState<Post[]>([])

  useEffect(() => {
    supabase.from('posts').select().eq('user_id', userId)
      .then(({ data }) => setPosts(data || []))

    const channel = supabase
      .channel('user-posts')
      .on(
        'postgres_changes',
        { event: '*', schema: 'public', table: 'posts', filter: `user_id=eq.${userId}` },
        (payload) => {
          if (payload.eventType === 'INSERT') {
            setPosts((prev) => [payload.new as Post, ...prev])
          } else if (payload.eventType === 'UPDATE') {
            setPosts((prev) =>
              prev.map((p) => (p.id === payload.new.id ? payload.new as Post : p))
            )
          } else if (payload.eventType === 'DELETE') {
            setPosts((prev) => prev.filter((p) => p.id !== payload.old.id))
          }
        }
      )
      .subscribe()

    return () => { supabase.removeChannel(channel) }
  }, [userId])

  return posts
}
```

## Enable Realtime (SQL)

```sql
ALTER PUBLICATION supabase_realtime ADD TABLE posts;
```

Disable:
```sql
ALTER PUBLICATION supabase_realtime DROP TABLE posts;
```
