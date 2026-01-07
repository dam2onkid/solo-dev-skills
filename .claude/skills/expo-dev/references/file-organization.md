# File Organization

Recommended project structure for Expo apps.

## Standard Structure

```
my-app/
├── app/                    # Expo Router (file-based routing)
│   ├── _layout.tsx         # Root layout
│   ├── index.tsx           # Home screen (/)
│   ├── +not-found.tsx      # 404 page
│   ├── (tabs)/             # Tab group
│   │   ├── _layout.tsx     # Tab navigator
│   │   ├── index.tsx       # Home tab
│   │   ├── explore.tsx     # Explore tab
│   │   └── profile.tsx     # Profile tab
│   ├── (auth)/             # Auth group (no URL segment)
│   │   ├── _layout.tsx
│   │   ├── login.tsx
│   │   └── register.tsx
│   └── [id]/               # Dynamic routes
│       └── index.tsx
├── components/             # Reusable components
│   ├── ui/                 # Base UI components
│   │   ├── Button.tsx
│   │   ├── Input.tsx
│   │   ├── Card.tsx
│   │   └── index.ts        # Barrel export
│   ├── forms/              # Form components
│   │   ├── LoginForm.tsx
│   │   └── RegisterForm.tsx
│   └── layout/             # Layout components
│       ├── Header.tsx
│       ├── Footer.tsx
│       └── Container.tsx
├── hooks/                  # Custom hooks
│   ├── useAuth.ts
│   ├── useTodos.ts
│   └── useDebounce.ts
├── lib/                    # Utilities & configs
│   ├── api.ts              # API client
│   ├── storage.ts          # Storage helpers
│   ├── constants.ts        # App constants
│   └── utils.ts            # Helper functions
├── contexts/               # React contexts
│   ├── AuthContext.tsx
│   └── ThemeContext.tsx
├── types/                  # TypeScript types
│   ├── api.ts              # API response types
│   ├── navigation.ts       # Navigation types
│   └── index.ts
├── assets/                 # Static assets
│   ├── images/
│   ├── fonts/
│   └── icons/
├── styles/                 # Global styles (if using Unistyles)
│   ├── unistyles.ts        # Unistyles config
│   └── themes.ts           # Theme definitions
├── app.json                # Expo config
├── app.config.js           # Dynamic config (optional)
├── eas.json                # EAS Build config
├── tsconfig.json
└── package.json
```

## Import Aliases

```json
// tsconfig.json
{
  "compilerOptions": {
    "baseUrl": ".",
    "paths": {
      "@/*": ["./*"],
      "@/components/*": ["components/*"],
      "@/hooks/*": ["hooks/*"],
      "@/lib/*": ["lib/*"],
      "@/types/*": ["types/*"]
    }
  }
}
```

## Barrel Exports

```typescript
// components/ui/index.ts
export { Button } from './Button';
export { Input } from './Input';
export { Card } from './Card';
export { Avatar } from './Avatar';

// Usage
import { Button, Input, Card } from '@/components/ui';
```

## Feature-Based Structure (Alternative)

For larger apps, organize by feature:

```
app/
├── _layout.tsx
├── index.tsx
└── (tabs)/
    └── ...

features/
├── auth/
│   ├── components/
│   │   ├── LoginForm.tsx
│   │   └── RegisterForm.tsx
│   ├── hooks/
│   │   └── useAuth.ts
│   ├── api/
│   │   └── authApi.ts
│   ├── types.ts
│   └── index.ts
├── todos/
│   ├── components/
│   │   ├── TodoList.tsx
│   │   ├── TodoItem.tsx
│   │   └── CreateTodo.tsx
│   ├── hooks/
│   │   └── useTodos.ts
│   ├── api/
│   │   └── todosApi.ts
│   ├── types.ts
│   └── index.ts
└── profile/
    └── ...
```

## File Naming Conventions

| Type | Convention | Example |
|------|------------|---------|
| Components | PascalCase | `Button.tsx`, `UserCard.tsx` |
| Hooks | camelCase with `use` prefix | `useAuth.ts`, `useTodos.ts` |
| Utilities | camelCase | `api.ts`, `storage.ts` |
| Types | camelCase or PascalCase | `types.ts`, `ApiTypes.ts` |
| Constants | camelCase or SCREAMING_SNAKE | `constants.ts` |
| Contexts | PascalCase with Context suffix | `AuthContext.tsx` |

## Route Groups Explained

```
app/
├── (tabs)/           # URL: /home, /settings (grouped for tab nav)
│   ├── _layout.tsx   # Tabs navigator
│   ├── home.tsx      # /home
│   └── settings.tsx  # /settings
├── (auth)/           # URL: /login, /register (grouped for stack nav)
│   ├── _layout.tsx   # Stack navigator
│   ├── login.tsx     # /login
│   └── register.tsx  # /register
└── (modals)/         # URL: /share (modal presentation)
    └── share.tsx     # /share (presented as modal)
```

Parentheses `()` create route groups without affecting the URL path.

## Recommended .gitignore

```gitignore
node_modules/
.expo/
dist/
.env*.local
*.jks
*.p8
*.p12
*.key
*.mobileprovision
*.orig.*
web-build/
android/
ios/

# EAS
.eas/

# macOS
.DS_Store
```

## Config Files Location

```
root/
├── app.json              # Static Expo config
├── app.config.js         # Dynamic Expo config (env vars)
├── eas.json              # EAS Build profiles
├── metro.config.js       # Metro bundler config
├── babel.config.js       # Babel config
├── tsconfig.json         # TypeScript config
└── .env                  # Environment variables (gitignored)
```
