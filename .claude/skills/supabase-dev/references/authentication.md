# Supabase Authentication

## Sign Up

```typescript
const { data, error } = await supabase.auth.signUp({
  email: 'user@example.com',
  password: 'secure-password',
  options: {
    data: { full_name: 'John Doe' }
  }
})
```

## Sign In

### Email/Password
```typescript
const { data, error } = await supabase.auth.signInWithPassword({
  email: 'user@example.com',
  password: 'password'
})
```

### Magic Link
```typescript
const { error } = await supabase.auth.signInWithOtp({
  email: 'user@example.com',
  options: { emailRedirectTo: 'https://yourapp.com/auth/callback' }
})
```

### OAuth
```typescript
const { data, error } = await supabase.auth.signInWithOAuth({
  provider: 'google',
  options: { redirectTo: 'https://yourapp.com/auth/callback' }
})
```

### Phone OTP
```typescript
const { error } = await supabase.auth.signInWithOtp({
  phone: '+1234567890'
})

const { data, error } = await supabase.auth.verifyOtp({
  phone: '+1234567890',
  token: '123456',
  type: 'sms'
})
```

## Session Management

### Get Session
```typescript
const { data: { session } } = await supabase.auth.getSession()
```

### Get User (Verified)
```typescript
const { data: { user } } = await supabase.auth.getUser()
```

### Listen to Auth Changes
```typescript
supabase.auth.onAuthStateChange((event, session) => {
  if (event === 'SIGNED_IN') console.log('User signed in:', session?.user)
  if (event === 'SIGNED_OUT') console.log('User signed out')
})
```

### Refresh Session
```typescript
const { data, error } = await supabase.auth.refreshSession()
```

## Update User

```typescript
const { data, error } = await supabase.auth.updateUser({
  email: 'new@example.com',
  password: 'new-password',
  data: { full_name: 'Jane Doe' }
})
```

## Password Reset

```typescript
const { error } = await supabase.auth.resetPasswordForEmail(
  'user@example.com',
  { redirectTo: 'https://yourapp.com/reset-password' }
)
```

## Sign Out

```typescript
const { error } = await supabase.auth.signOut()
```

## Next.js Integration

### Middleware (Route Protection)
```typescript
import { createServerClient } from '@supabase/ssr'
import { NextResponse, type NextRequest } from 'next/server'

export async function middleware(request: NextRequest) {
  const response = NextResponse.next()
  const supabase = createServerClient(
    process.env.SUPABASE_URL!,
    process.env.SUPABASE_ANON_KEY!,
    {
      cookies: {
        getAll: () => request.cookies.getAll(),
        setAll: (cookies) => cookies.forEach(({ name, value, options }) =>
          response.cookies.set(name, value, options))
      }
    }
  )
  const { data: { user } } = await supabase.auth.getUser()
  if (!user && request.nextUrl.pathname.startsWith('/dashboard')) {
    return NextResponse.redirect(new URL('/login', request.url))
  }
  return response
}
```

### Auth Callback Route
```typescript
import { createServerClient } from '@supabase/ssr'
import { cookies } from 'next/headers'
import { NextResponse } from 'next/server'

export async function GET(request: Request) {
  const { searchParams } = new URL(request.url)
  const code = searchParams.get('code')
  if (code) {
    const supabase = createServerClient(
      process.env.SUPABASE_URL!,
      process.env.SUPABASE_ANON_KEY!,
      { cookies: { getAll: () => cookies().getAll() } }
    )
    await supabase.auth.exchangeCodeForSession(code)
  }
  return NextResponse.redirect(new URL('/dashboard', request.url))
}
```

## React Native (Expo)

```typescript
import 'react-native-url-polyfill/auto'
import AsyncStorage from '@react-native-async-storage/async-storage'
import { createClient } from '@supabase/supabase-js'

const supabase = createClient(SUPABASE_URL, SUPABASE_ANON_KEY, {
  auth: {
    storage: AsyncStorage,
    autoRefreshToken: true,
    persistSession: true,
    detectSessionInUrl: false
  }
})
```
