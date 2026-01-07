---
name: expo-dev
description: Build universal native apps (Android, iOS, web) using Expo framework with React Native. Use when creating new Expo projects, configuring Expo Router navigation (tabs, stacks, drawers), using Expo SDK packages (camera, notifications, storage, location), building with EAS Build, deploying to app stores, handling app configuration (app.json/app.config.js), implementing deep linking, or managing development workflows with Expo CLI.
---

# Expo Dev

Build universal native apps from a single TypeScript/JavaScript codebase.

## Quick Reference

### Project Setup

```bash
# Create new project
npx create-expo-app@latest my-app
cd my-app

# Start development
npx expo start

# Install SDK packages
npx expo install expo-camera expo-notifications expo-location
```

### Project Structure (Expo Router)

```
app/
├── _layout.tsx          # Root layout (navigation container)
├── index.tsx            # Home screen (/)
├── [id].tsx             # Dynamic route (/123)
├── (tabs)/              # Tab group
│   ├── _layout.tsx      # Tab navigator config
│   ├── index.tsx        # First tab
│   └── settings.tsx     # Second tab
└── (auth)/              # Route group (no URL segment)
    ├── _layout.tsx
    ├── login.tsx
    └── register.tsx
```

## Expo Router Navigation

### Stack Navigator

```typescript
import { Stack } from "expo-router";

export default function RootLayout() {
  return (
    <Stack screenOptions={{ headerStyle: { backgroundColor: "#f4511e" } }}>
      <Stack.Screen name="index" options={{ title: "Home" }} />
      <Stack.Screen name="details" options={{ title: "Details" }} />
    </Stack>
  );
}
```

### Tab Navigator

```typescript
import { Tabs } from "expo-router";
import { MaterialIcons } from "@expo/vector-icons";

export default function TabLayout() {
  return (
    <Tabs>
      <Tabs.Screen
        name="index"
        options={{
          title: "Home",
          tabBarIcon: ({ color }) => (
            <MaterialIcons name="home" size={28} color={color} />
          ),
        }}
      />
      <Tabs.Screen name="settings" options={{ title: "Settings" }} />
    </Tabs>
  );
}
```

### Navigation Actions

```typescript
import { router, useLocalSearchParams, Link } from "expo-router";

// Imperative navigation
router.push("/details");
router.push({ pathname: "/user/[id]", params: { id: "123" } });
router.replace("/home");
router.back();

// Get route params
const { id } = useLocalSearchParams<{ id: string }>();

// Declarative navigation
<Link href="/about">About</Link>;
```

## Common SDK Packages

| Package              | Purpose              | Install                               |
| -------------------- | -------------------- | ------------------------------------- |
| `expo-camera`        | Camera access        | `npx expo install expo-camera`        |
| `expo-image-picker`  | Select images/videos | `npx expo install expo-image-picker`  |
| `expo-notifications` | Push notifications   | `npx expo install expo-notifications` |
| `expo-location`      | GPS location         | `npx expo install expo-location`      |
| `expo-secure-store`  | Encrypted storage    | `npx expo install expo-secure-store`  |
| `expo-file-system`   | File operations      | `npx expo install expo-file-system`   |
| `expo-image`         | Optimized images     | `npx expo install expo-image`         |
| `expo-font`          | Custom fonts         | `npx expo install expo-font`          |
| `expo-splash-screen` | Splash screen        | `npx expo install expo-splash-screen` |
| `expo-haptics`       | Haptic feedback      | `npx expo install expo-haptics`       |

## EAS Build & Deploy

```bash
# Install EAS CLI
npm install -g eas-cli

# Login & configure
eas login
eas build:configure

# Build for platforms
eas build --platform android
eas build --platform ios
eas build --platform all

# Build profiles (eas.json)
eas build --profile development
eas build --profile preview
eas build --profile production

# Submit to stores
eas submit --platform android
eas submit --platform ios
```

## App Configuration

### app.json / app.config.js

```json
{
  "expo": {
    "name": "My App",
    "slug": "my-app",
    "version": "1.0.0",
    "orientation": "portrait",
    "icon": "./assets/icon.png",
    "splash": { "image": "./assets/splash.png", "backgroundColor": "#ffffff" },
    "ios": { "bundleIdentifier": "com.company.myapp", "supportsTablet": true },
    "android": {
      "package": "com.company.myapp",
      "adaptiveIcon": { "foregroundImage": "./assets/adaptive-icon.png" }
    },
    "plugins": ["expo-camera", "expo-notifications"]
  }
}
```

## Resources

| Reference                               | Description                                   |
| --------------------------------------- | --------------------------------------------- |
| `references/sdk-packages.md`            | Camera, notifications, location, storage APIs |
| `references/eas-build.md`               | Build profiles, submit, CI/CD                 |
| `references/routing-guide.md`           | Expo Router navigation patterns               |
| `references/data-fetching.md`           | React Query setup & patterns                  |
| `references/styling-guide.md`           | Uniwind (Tailwind) & Unistyles                |
| `references/component-patterns.md`      | Compound, polymorphic, HOC patterns           |
| `references/common-patterns.md`         | Auth, forms, infinite scroll                  |
| `references/file-organization.md`       | Project structure conventions                 |
| `references/loading-and-error-state.md` | Skeleton, error boundary, empty states        |
| `references/performance.md`             | FlatList, memoization, animations             |
| `references/typescript-standards.md`    | Types, generics, utilities                    |
