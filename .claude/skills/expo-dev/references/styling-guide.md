# Styling Guide

Styling options for React Native: Uniwind (Tailwind) and Unistyles.

---

## Option 1: Uniwind (Tailwind CSS)

Fastest Tailwind CSS bindings for React Native.

### Setup

```bash
npx expo install uniwind
```

```javascript
// metro.config.js
const { getDefaultConfig } = require('expo/metro-config');
const { withUnistyles } = require('uniwind/metro');

const config = getDefaultConfig(__dirname);

module.exports = withUnistyles(config);
```

```css
/* global.css */
@import 'tailwindcss';
@source '../app';
@source '../components';
```

```typescript
// app/_layout.tsx
import '../global.css';

export default function RootLayout() {
  return <Stack />;
}
```

### Basic Usage

```typescript
import { View, Text, Pressable } from 'react-native';

export function Card() {
  return (
    <View className="bg-white rounded-lg p-4 shadow-md">
      <Text className="text-lg font-bold text-gray-900">Title</Text>
      <Text className="text-sm text-gray-600 mt-2">Description</Text>
    </View>
  );
}

export function Button({ title, onPress }: { title: string; onPress: () => void }) {
  return (
    <Pressable
      onPress={onPress}
      className="bg-blue-500 active:bg-blue-600 px-4 py-2 rounded-lg"
    >
      <Text className="text-white font-semibold text-center">{title}</Text>
    </Pressable>
  );
}
```

### Dark Mode

```typescript
<View className="bg-white dark:bg-gray-800 p-4">
  <Text className="text-gray-900 dark:text-white">
    Adapts to theme automatically
  </Text>
</View>
```

### Responsive (Breakpoints)

```typescript
<View className="flex-col md:flex-row gap-4">
  <View className="w-full md:w-1/2">Column 1</View>
  <View className="w-full md:w-1/2">Column 2</View>
</View>
```

### Custom Themes

```css
/* global.css */
@layer theme {
  :root {
    @variant light {
      --color-background: #ffffff;
      --color-foreground: #000000;
      --color-primary: #3b82f6;
    }
    @variant dark {
      --color-background: #121212;
      --color-foreground: #ffffff;
      --color-primary: #60a5fa;
    }
  }
}
```

```typescript
<View className="bg-background">
  <Text className="text-foreground">Uses theme colors</Text>
  <Text className="text-primary">Primary color</Text>
</View>
```

---

## Option 2: React Native Unistyles

High-performance styling with themes, breakpoints, and variants.

### Setup

```bash
npx expo install react-native-unistyles
```

```typescript
// styles/unistyles.ts
import { StyleSheet } from 'react-native-unistyles';

const lightTheme = {
  colors: {
    background: '#FFFFFF',
    foreground: '#121212',
    primary: '#3b82f6',
    secondary: '#64748b',
  },
  spacing: (v: number) => v * 4,
} as const;

const darkTheme = {
  colors: {
    background: '#121212',
    foreground: '#FFFFFF',
    primary: '#60a5fa',
    secondary: '#94a3b8',
  },
  spacing: (v: number) => v * 4,
} as const;

const breakpoints = {
  xs: 0,
  sm: 576,
  md: 768,
  lg: 992,
  xl: 1200,
} as const;

type AppThemes = { light: typeof lightTheme; dark: typeof darkTheme };
type AppBreakpoints = typeof breakpoints;

declare module 'react-native-unistyles' {
  export interface UnistylesThemes extends AppThemes {}
  export interface UnistylesBreakpoints extends AppBreakpoints {}
}

StyleSheet.configure({
  themes: { light: lightTheme, dark: darkTheme },
  breakpoints,
  settings: { adaptiveThemes: true },
});
```

```typescript
// app/_layout.tsx
import '../styles/unistyles';

export default function RootLayout() {
  return <Stack />;
}
```

### Basic Usage

```typescript
import { View, Text, Pressable } from 'react-native';
import { StyleSheet } from 'react-native-unistyles';

export function Card() {
  return (
    <View style={styles.card}>
      <Text style={styles.title}>Title</Text>
      <Text style={styles.description}>Description</Text>
    </View>
  );
}

const styles = StyleSheet.create((theme) => ({
  card: {
    backgroundColor: theme.colors.background,
    borderRadius: 12,
    padding: theme.spacing(4),
    shadowColor: '#000',
    shadowOpacity: 0.1,
    shadowRadius: 8,
  },
  title: {
    fontSize: 18,
    fontWeight: 'bold',
    color: theme.colors.foreground,
  },
  description: {
    fontSize: 14,
    color: theme.colors.secondary,
    marginTop: theme.spacing(2),
  },
}));
```

### Variants

```typescript
const styles = StyleSheet.create((theme) => ({
  button: {
    paddingVertical: theme.spacing(3),
    paddingHorizontal: theme.spacing(4),
    borderRadius: 8,
    variants: {
      variant: {
        primary: {
          backgroundColor: theme.colors.primary,
        },
        secondary: {
          backgroundColor: theme.colors.secondary,
        },
        outline: {
          backgroundColor: 'transparent',
          borderWidth: 1,
          borderColor: theme.colors.primary,
        },
      },
      size: {
        sm: { paddingVertical: theme.spacing(2), paddingHorizontal: theme.spacing(3) },
        md: { paddingVertical: theme.spacing(3), paddingHorizontal: theme.spacing(4) },
        lg: { paddingVertical: theme.spacing(4), paddingHorizontal: theme.spacing(6) },
      },
    },
  },
}));

// Usage
<Pressable style={styles.button({ variant: 'primary', size: 'md' })} />
```

### Responsive Breakpoints

```typescript
const styles = StyleSheet.create((theme, rt) => ({
  container: {
    flexDirection: { xs: 'column', md: 'row' },
    padding: { xs: theme.spacing(2), md: theme.spacing(4) },
  },
  text: {
    fontSize: { xs: 14, sm: 16, md: 18 },
  },
}));
```

### Runtime Values

```typescript
const styles = StyleSheet.create((theme, rt) => ({
  container: {
    paddingTop: rt.insets.top,
    paddingBottom: rt.insets.bottom,
  },
  text: {
    fontSize: 16 * rt.fontScale,
  },
  responsive: {
    width: rt.screen.width > 768 ? '50%' : '100%',
  },
}));
```

### Theme Switching

```typescript
import { UnistylesRuntime } from 'react-native-unistyles';

// Get current theme
const currentTheme = UnistylesRuntime.themeName;

// Switch theme
UnistylesRuntime.setTheme('dark');

// Toggle
const toggleTheme = () => {
  UnistylesRuntime.setTheme(
    UnistylesRuntime.themeName === 'light' ? 'dark' : 'light'
  );
};
```

---

## Comparison

| Feature | Uniwind | Unistyles |
|---------|---------|-----------|
| Syntax | `className="..."` | `style={styles.name}` |
| Learning Curve | Easy (Tailwind) | Moderate |
| Performance | Build-time | Runtime (optimized) |
| Type Safety | Limited | Full TypeScript |
| Variants | Via classes | Built-in |
| Breakpoints | Via classes | Built-in |
| Themes | CSS variables | JS objects |
| Dark Mode | `dark:` prefix | `adaptiveThemes` |

**Recommendation:**
- **Uniwind**: Familiar with Tailwind, rapid prototyping
- **Unistyles**: Type safety, complex theming, variants
