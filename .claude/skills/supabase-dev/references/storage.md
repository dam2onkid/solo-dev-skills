# Supabase Storage

## Bucket Management

### Create Bucket (Admin)
```typescript
const { data, error } = await supabaseAdmin.storage.createBucket('avatars', {
  public: false,
  fileSizeLimit: 1024 * 1024 * 2, // 2MB
  allowedMimeTypes: ['image/png', 'image/jpeg', 'image/webp']
})
```

### List Buckets
```typescript
const { data, error } = await supabase.storage.listBuckets()
```

## File Operations

### Upload
```typescript
const { data, error } = await supabase.storage
  .from('avatars')
  .upload(`${userId}/avatar.png`, file, {
    cacheControl: '3600',
    upsert: true
  })
```

### Upload from Base64
```typescript
const base64 = 'iVBORw0KGgoAAAANSUhEUg...'
const { data, error } = await supabase.storage
  .from('avatars')
  .upload('path/file.png', decode(base64), {
    contentType: 'image/png'
  })
```

### Download
```typescript
const { data, error } = await supabase.storage
  .from('avatars')
  .download(`${userId}/avatar.png`)

if (data) {
  const url = URL.createObjectURL(data)
}
```

### Get Public URL
```typescript
const { data } = supabase.storage
  .from('public-bucket')
  .getPublicUrl('path/to/file.png')

console.log(data.publicUrl)
```

### Get Signed URL (Private)
```typescript
const { data, error } = await supabase.storage
  .from('private-bucket')
  .createSignedUrl('path/to/file.png', 3600) // 1 hour

console.log(data?.signedUrl)
```

### List Files
```typescript
const { data, error } = await supabase.storage
  .from('avatars')
  .list(userId, {
    limit: 100,
    offset: 0,
    sortBy: { column: 'created_at', order: 'desc' }
  })
```

### Move/Rename
```typescript
const { data, error } = await supabase.storage
  .from('avatars')
  .move('old/path.png', 'new/path.png')
```

### Copy
```typescript
const { data, error } = await supabase.storage
  .from('avatars')
  .copy('source/path.png', 'dest/path.png')
```

### Delete
```typescript
const { data, error } = await supabase.storage
  .from('avatars')
  .remove(['path/to/file1.png', 'path/to/file2.png'])
```

## Image Transformations

```typescript
const { data } = supabase.storage
  .from('avatars')
  .getPublicUrl('avatar.png', {
    transform: {
      width: 200,
      height: 200,
      resize: 'cover',
      quality: 80,
      format: 'webp'
    }
  })
```

## Storage Policies (RLS)

### Policy: Users upload to own folder
```sql
CREATE POLICY "Users can upload to own folder"
ON storage.objects FOR INSERT
TO authenticated
WITH CHECK (
  bucket_id = 'avatars' AND
  (storage.foldername(name))[1] = auth.uid()::text
);
```

### Policy: Users read own files
```sql
CREATE POLICY "Users can read own files"
ON storage.objects FOR SELECT
TO authenticated
USING (
  bucket_id = 'avatars' AND
  (storage.foldername(name))[1] = auth.uid()::text
);
```

### Policy: Public bucket read
```sql
CREATE POLICY "Public read access"
ON storage.objects FOR SELECT
TO anon, authenticated
USING (bucket_id = 'public');
```

## React File Upload Component

```typescript
function AvatarUpload({ userId }: { userId: string }) {
  const [uploading, setUploading] = useState(false)

  async function handleUpload(e: React.ChangeEvent<HTMLInputElement>) {
    const file = e.target.files?.[0]
    if (!file) return

    setUploading(true)
    const { error } = await supabase.storage
      .from('avatars')
      .upload(`${userId}/${file.name}`, file, { upsert: true })

    if (error) console.error(error)
    setUploading(false)
  }

  return <input type="file" onChange={handleUpload} disabled={uploading} />
}
```
