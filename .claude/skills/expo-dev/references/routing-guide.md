# Expo Router Guide

File-based routing for React Native with Expo Router.

## File Conventions

| File | Purpose |
|------|---------|
| `_layout.tsx` | Layout wrapper (navigation container) |
| `index.tsx` | Index route (`/`) |
| `[param].tsx` | Dynamic route (`/123`) |
| `[...rest].tsx` | Catch-all route (`/a/b/c`) |
| `+not-found.tsx` | 404 page |
| `+html.tsx` | Custom HTML wrapper (web) |
| `(group)/` | Route group (no URL segment) |

## Basic Setup

```typescript
// app/_layout.tsx
import { Stack } from 'expo-router';

export default function RootLayout() {
  return (
    <Stack>
      <Stack.Screen name="index" options={{ title: 'Home' }} />
      <Stack.Screen name="(tabs)" options={{ headerShown: false }} />
    </Stack>
  );
}

// app/index.tsx
import { View, Text } from 'react-native';

export default function HomeScreen() {
  return (
    <View>
      <Text>Home</Text>
    </View>
  );
}
```

## Tab Navigation

```typescript
// app/(tabs)/_layout.tsx
import { Tabs } from 'expo-router';
import { Ionicons } from '@expo/vector-icons';

export default function TabLayout() {
  return (
    <Tabs
      screenOptions={{
        tabBarActiveTintColor: '#007AFF',
        headerShown: false,
      }}
    >
      <Tabs.Screen
        name="index"
        options={{
          title: 'Home',
          tabBarIcon: ({ color, size }) => <Ionicons name="home" size={size} color={color} />,
        }}
      />
      <Tabs.Screen
        name="explore"
        options={{
          title: 'Explore',
          tabBarIcon: ({ color, size }) => <Ionicons name="search" size={size} color={color} />,
        }}
      />
      <Tabs.Screen
        name="profile"
        options={{
          title: 'Profile',
          tabBarIcon: ({ color, size }) => <Ionicons name="person" size={size} color={color} />,
        }}
      />
    </Tabs>
  );
}
```

## Stack Navigation

```typescript
// app/(auth)/_layout.tsx
import { Stack } from 'expo-router';

export default function AuthLayout() {
  return (
    <Stack screenOptions={{ headerBackTitle: 'Back' }}>
      <Stack.Screen name="login" options={{ title: 'Login' }} />
      <Stack.Screen name="register" options={{ title: 'Register' }} />
      <Stack.Screen name="forgot-password" options={{ title: 'Reset Password' }} />
    </Stack>
  );
}
```

## Drawer Navigation

```bash
npx expo install @react-navigation/drawer react-native-gesture-handler react-native-reanimated
```

```typescript
// app/_layout.tsx
import { Drawer } from 'expo-router/drawer';
import { GestureHandlerRootView } from 'react-native-gesture-handler';

export default function Layout() {
  return (
    <GestureHandlerRootView style={{ flex: 1 }}>
      <Drawer>
        <Drawer.Screen name="index" options={{ title: 'Home' }} />
        <Drawer.Screen name="settings" options={{ title: 'Settings' }} />
      </Drawer>
    </GestureHandlerRootView>
  );
}
```

## Dynamic Routes

```typescript
// app/user/[id].tsx
import { useLocalSearchParams } from 'expo-router';

export default function UserScreen() {
  const { id } = useLocalSearchParams<{ id: string }>();
  return <Text>User: {id}</Text>;
}

// app/[...rest].tsx (catch-all)
import { useLocalSearchParams } from 'expo-router';

export default function CatchAll() {
  const { rest } = useLocalSearchParams<{ rest: string[] }>();
  return <Text>Path: {rest?.join('/')}</Text>;
}
```

## Navigation API

```typescript
import { router, Link, useRouter, useLocalSearchParams, useSegments, usePathname } from 'expo-router';

// Imperative navigation
router.push('/user/123');                    // Push to stack
router.push({ pathname: '/user/[id]', params: { id: '123' } });
router.replace('/home');                     // Replace current
router.back();                               // Go back
router.canGoBack();                          // Check if can go back
router.dismiss();                            // Dismiss modal
router.dismissAll();                         // Dismiss all modals

// Hook-based
const router = useRouter();
router.push('/details');

// Get params
const { id, query } = useLocalSearchParams<{ id: string; query?: string }>();

// Get current segments
const segments = useSegments(); // ['(tabs)', 'home']

// Get current pathname
const pathname = usePathname(); // '/home'

// Declarative navigation
<Link href="/about">About</Link>
<Link href={{ pathname: '/user/[id]', params: { id: '123' } }}>User</Link>
<Link href="/details" asChild>
  <Pressable><Text>Details</Text></Pressable>
</Link>
```

## Modal Routes

```typescript
// app/_layout.tsx
export default function RootLayout() {
  return (
    <Stack>
      <Stack.Screen name="(tabs)" options={{ headerShown: false }} />
      <Stack.Screen
        name="modal"
        options={{
          presentation: 'modal',
          headerShown: false,
        }}
      />
    </Stack>
  );
}

// app/modal.tsx
export default function ModalScreen() {
  return (
    <View>
      <Text>Modal Content</Text>
      <Button title="Close" onPress={() => router.dismiss()} />
    </View>
  );
}
```

## Protected Routes

```typescript
// app/(auth)/_layout.tsx
import { Redirect, Stack } from 'expo-router';
import { useAuth } from '@/hooks/useAuth';

export default function AuthLayout() {
  const { user, isLoading } = useAuth();

  if (isLoading) return <LoadingScreen />;
  if (!user) return <Redirect href="/login" />;

  return <Stack />;
}
```

## Shared Routes (Groups)

```typescript
// File structure:
// app/
// ├── (app)/
// │   ├── _layout.tsx    # Stack with auth check
// │   ├── home.tsx
// │   └── profile.tsx
// ├── (public)/
// │   ├── _layout.tsx    # Stack without auth
// │   ├── login.tsx
// │   └── register.tsx
// └── _layout.tsx        # Root - wraps everything
```

## Screen Options

```typescript
// Static options
<Stack.Screen
  name="details"
  options={{
    title: 'Details',
    headerShown: true,
    headerBackTitle: 'Back',
    headerLargeTitle: true,
    headerTransparent: false,
    presentation: 'card', // 'modal', 'transparentModal', 'containedModal'
    animation: 'slide_from_right', // 'fade', 'slide_from_bottom', 'none'
  }}
/>

// Dynamic options in component
import { Stack } from 'expo-router';

export default function DetailsScreen() {
  return (
    <>
      <Stack.Screen options={{ title: 'Dynamic Title' }} />
      <View>{/* Content */}</View>
    </>
  );
}
```

## Deep Linking

```json
// app.json
{
  "expo": {
    "scheme": "myapp",
    "web": {
      "bundler": "metro"
    }
  }
}
```

```typescript
// Handle incoming links
import * as Linking from 'expo-linking';

// Open deep link
Linking.openURL('myapp://user/123');

// Universal links (iOS)
// Configure in apple-app-site-association file
```

## Navigation Events

```typescript
import { useNavigation, useFocusEffect } from 'expo-router';
import { useCallback } from 'react';

export default function Screen() {
  const navigation = useNavigation();

  // Run on focus
  useFocusEffect(
    useCallback(() => {
      console.log('Screen focused');
      return () => console.log('Screen blurred');
    }, [])
  );

  // Listen to events
  useEffect(() => {
    const unsubscribe = navigation.addListener('beforeRemove', (e) => {
      // Prevent going back
      if (hasUnsavedChanges) {
        e.preventDefault();
        Alert.alert('Discard changes?', '', [
          { text: 'Stay', style: 'cancel' },
          { text: 'Discard', onPress: () => navigation.dispatch(e.data.action) },
        ]);
      }
    });
    return unsubscribe;
  }, [navigation, hasUnsavedChanges]);
}
```

## TypeScript

```typescript
// types/navigation.ts
import { Href } from 'expo-router';

declare module 'expo-router' {
  export namespace ExpoRouter {
    export interface __routes<T extends string = string> {
      '/(tabs)': undefined;
      '/(tabs)/home': undefined;
      '/user/[id]': { id: string };
      '/search': { query?: string };
    }
  }
}

// Usage with type safety
router.push({ pathname: '/user/[id]', params: { id: '123' } });
```
