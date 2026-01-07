# TypeScript Standards

TypeScript patterns and conventions for Expo apps.

## Project Setup

```json
// tsconfig.json
{
  "extends": "expo/tsconfig.base",
  "compilerOptions": {
    "strict": true,
    "noUncheckedIndexedAccess": true,
    "baseUrl": ".",
    "paths": {
      "@/*": ["./*"]
    }
  },
  "include": ["**/*.ts", "**/*.tsx", ".expo/types/**/*.ts", "expo-env.d.ts"]
}
```

## Component Types

### Functional Components

```typescript
import { View, Text, ViewProps, TextProps } from 'react-native';
import { ReactNode } from 'react';

interface CardProps extends ViewProps {
  title: string;
  children: ReactNode;
}

export function Card({ title, children, style, ...props }: CardProps) {
  return (
    <View style={[styles.card, style]} {...props}>
      <Text style={styles.title}>{title}</Text>
      {children}
    </View>
  );
}
```

### Props with Discriminated Unions

```typescript
type ButtonProps = {
  size?: 'sm' | 'md' | 'lg';
  disabled?: boolean;
} & (
  | { variant: 'solid'; color: string }
  | { variant: 'outline'; borderColor: string }
  | { variant: 'ghost' }
);

function Button(props: ButtonProps) {
  if (props.variant === 'solid') {
    return <View style={{ backgroundColor: props.color }} />;
  }
  if (props.variant === 'outline') {
    return <View style={{ borderColor: props.borderColor }} />;
  }
  return <View />;
}
```

### Generic Components

```typescript
interface ListProps<T> {
  data: T[];
  renderItem: (item: T, index: number) => ReactNode;
  keyExtractor: (item: T) => string;
}

function List<T>({ data, renderItem, keyExtractor }: ListProps<T>) {
  return (
    <View>
      {data.map((item, index) => (
        <View key={keyExtractor(item)}>{renderItem(item, index)}</View>
      ))}
    </View>
  );
}

// Usage
<List
  data={users}
  renderItem={(user) => <Text>{user.name}</Text>}
  keyExtractor={(user) => user.id}
/>
```

## Hook Types

### Custom Hook Return Types

```typescript
interface UseAuthReturn {
  user: User | null;
  isLoading: boolean;
  signIn: (email: string, password: string) => Promise<void>;
  signOut: () => Promise<void>;
}

function useAuth(): UseAuthReturn {
  const [user, setUser] = useState<User | null>(null);
  const [isLoading, setIsLoading] = useState(true);

  const signIn = async (email: string, password: string) => {
    // Implementation
  };

  const signOut = async () => {
    // Implementation
  };

  return { user, isLoading, signIn, signOut };
}
```

### Generic Hooks

```typescript
function useLocalStorage<T>(key: string, initialValue: T) {
  const [value, setValue] = useState<T>(initialValue);

  const setStoredValue = async (newValue: T | ((prev: T) => T)) => {
    const valueToStore = newValue instanceof Function ? newValue(value) : newValue;
    setValue(valueToStore);
    await AsyncStorage.setItem(key, JSON.stringify(valueToStore));
  };

  return [value, setStoredValue] as const;
}

// Usage
const [theme, setTheme] = useLocalStorage<'light' | 'dark'>('theme', 'light');
```

## API Types

### Request/Response Types

```typescript
// types/api.ts
interface User {
  id: string;
  email: string;
  name: string;
  createdAt: string;
}

interface CreateUserDto {
  email: string;
  password: string;
  name: string;
}

interface UpdateUserDto {
  name?: string;
  email?: string;
}

interface PaginatedResponse<T> {
  data: T[];
  meta: {
    total: number;
    page: number;
    perPage: number;
    totalPages: number;
  };
}

interface ApiError {
  message: string;
  code: string;
  details?: Record<string, string[]>;
}
```

### Type-Safe API Client

```typescript
async function apiClient<T>(endpoint: string, options?: RequestInit): Promise<T> {
  const response = await fetch(`${BASE_URL}${endpoint}`, options);

  if (!response.ok) {
    const error: ApiError = await response.json();
    throw new Error(error.message);
  }

  return response.json() as Promise<T>;
}

// Usage
const users = await apiClient<User[]>('/users');
const user = await apiClient<User>('/users/123');
```

## Navigation Types

### Expo Router Type Safety

```typescript
// types/navigation.ts
export type RootStackParamList = {
  '/(tabs)': undefined;
  '/(tabs)/home': undefined;
  '/(tabs)/profile': undefined;
  '/user/[id]': { id: string };
  '/search': { query?: string };
  '/settings': undefined;
};

// Usage with useLocalSearchParams
import { useLocalSearchParams } from 'expo-router';

function UserScreen() {
  const { id } = useLocalSearchParams<{ id: string }>();
  // id is typed as string
}
```

## Context Types

```typescript
import { createContext, useContext, ReactNode } from 'react';

interface ThemeContextType {
  theme: 'light' | 'dark';
  toggleTheme: () => void;
}

const ThemeContext = createContext<ThemeContextType | null>(null);

export function ThemeProvider({ children }: { children: ReactNode }) {
  const [theme, setTheme] = useState<'light' | 'dark'>('light');

  const toggleTheme = () => setTheme((t) => (t === 'light' ? 'dark' : 'light'));

  return (
    <ThemeContext.Provider value={{ theme, toggleTheme }}>
      {children}
    </ThemeContext.Provider>
  );
}

export function useTheme(): ThemeContextType {
  const context = useContext(ThemeContext);
  if (!context) {
    throw new Error('useTheme must be used within ThemeProvider');
  }
  return context;
}
```

## Utility Types

```typescript
// Make all properties optional recursively
type DeepPartial<T> = {
  [P in keyof T]?: T[P] extends object ? DeepPartial<T[P]> : T[P];
};

// Extract non-null type
type NonNullableFields<T> = {
  [P in keyof T]: NonNullable<T[P]>;
};

// Pick required fields only
type RequiredFields<T> = {
  [K in keyof T as undefined extends T[K] ? never : K]: T[K];
};

// Create action types for reducers
type ActionMap<M extends Record<string, unknown>> = {
  [Key in keyof M]: M[Key] extends undefined
    ? { type: Key }
    : { type: Key; payload: M[Key] };
};

// Usage
type Actions = ActionMap<{
  SET_USER: User;
  CLEAR_USER: undefined;
  UPDATE_SETTINGS: Partial<Settings>;
}>[keyof ActionMap<{
  SET_USER: User;
  CLEAR_USER: undefined;
  UPDATE_SETTINGS: Partial<Settings>;
}>];
```

## Form Types

```typescript
interface FormField<T> {
  value: T;
  error?: string;
  touched: boolean;
}

interface LoginForm {
  email: FormField<string>;
  password: FormField<string>;
}

type FormValues<T> = {
  [K in keyof T]: T[K] extends FormField<infer V> ? V : never;
};

type FormErrors<T> = Partial<{
  [K in keyof T]: string;
}>;

// Usage
const initialForm: LoginForm = {
  email: { value: '', touched: false },
  password: { value: '', touched: false },
};
```

## Enum Alternatives

```typescript
// Prefer const objects over enums
const Status = {
  PENDING: 'pending',
  ACTIVE: 'active',
  COMPLETED: 'completed',
} as const;

type Status = (typeof Status)[keyof typeof Status];
// Type: 'pending' | 'active' | 'completed'

// Usage
function getStatusLabel(status: Status): string {
  switch (status) {
    case Status.PENDING:
      return 'Pending';
    case Status.ACTIVE:
      return 'Active';
    case Status.COMPLETED:
      return 'Completed';
  }
}
```

## Type Guards

```typescript
// Type predicate
function isUser(value: unknown): value is User {
  return (
    typeof value === 'object' &&
    value !== null &&
    'id' in value &&
    'email' in value
  );
}

// Assertion function
function assertUser(value: unknown): asserts value is User {
  if (!isUser(value)) {
    throw new Error('Value is not a User');
  }
}

// Usage
const data: unknown = await fetchUser();
if (isUser(data)) {
  console.log(data.email); // data is typed as User
}
```

## Best Practices

1. **Prefer interfaces** for object types (better error messages)
2. **Use `unknown` over `any`** when type is uncertain
3. **Enable strict mode** in tsconfig
4. **Export types** alongside components
5. **Use const assertions** for literal types
6. **Avoid type assertions** (`as`) when possible
7. **Define return types** for public functions
8. **Use discriminated unions** for state machines
