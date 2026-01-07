# Common Patterns

Essential patterns for Expo/React Native development.

## Authentication Flow

```typescript
// contexts/AuthContext.tsx
import {
  createContext,
  useContext,
  useState,
  useEffect,
  ReactNode,
} from "react";
import * as SecureStore from "expo-secure-store";
import { router } from "expo-router";

type AuthContextType = {
  user: User | null;
  isLoading: boolean;
  signIn: (email: string, password: string) => Promise<void>;
  signOut: () => Promise<void>;
};

const AuthContext = createContext<AuthContextType | null>(null);

export function AuthProvider({ children }: { children: ReactNode }) {
  const [user, setUser] = useState<User | null>(null);
  const [isLoading, setIsLoading] = useState(true);

  useEffect(() => {
    loadUser();
  }, []);

  const loadUser = async () => {
    const token = await SecureStore.getItemAsync("token");
    if (token) {
      const userData = await fetchUser(token);
      setUser(userData);
    }
    setIsLoading(false);
  };

  const signIn = async (email: string, password: string) => {
    const { token, user } = await loginApi(email, password);
    await SecureStore.setItemAsync("token", token);
    setUser(user);
    router.replace("/(tabs)");
  };

  const signOut = async () => {
    await SecureStore.deleteItemAsync("token");
    setUser(null);
    router.replace("/login");
  };

  return (
    <AuthContext.Provider value={{ user, isLoading, signIn, signOut }}>
      {children}
    </AuthContext.Provider>
  );
}

export const useAuth = () => {
  const context = useContext(AuthContext);
  if (!context) throw new Error("useAuth must be used within AuthProvider");
  return context;
};
```

## Protected Routes

```typescript
// app/(auth)/_layout.tsx
import { Redirect, Stack } from "expo-router";
import { useAuth } from "@/contexts/AuthContext";

export default function AuthLayout() {
  const { user, isLoading } = useAuth();

  if (isLoading) return <LoadingScreen />;
  if (!user) return <Redirect href="/login" />;

  return <Stack />;
}
```

## Form Handling

```typescript
import { useState } from "react";
import { TextInput, Pressable, Text, View } from "react-native";

type FormData = { email: string; password: string };
type FormErrors = Partial<Record<keyof FormData, string>>;

export function LoginForm() {
  const [form, setForm] = useState<FormData>({ email: "", password: "" });
  const [errors, setErrors] = useState<FormErrors>({});
  const [isSubmitting, setIsSubmitting] = useState(false);

  const validate = (): boolean => {
    const newErrors: FormErrors = {};
    if (!form.email) newErrors.email = "Email required";
    if (!form.password) newErrors.password = "Password required";
    setErrors(newErrors);
    return Object.keys(newErrors).length === 0;
  };

  const handleSubmit = async () => {
    if (!validate()) return;
    setIsSubmitting(true);
    try {
      await signIn(form.email, form.password);
    } catch (e) {
      setErrors({ email: "Invalid credentials" });
    } finally {
      setIsSubmitting(false);
    }
  };

  return (
    <View>
      <TextInput
        value={form.email}
        onChangeText={(text) => setForm({ ...form, email: text })}
        placeholder="Email"
        keyboardType="email-address"
        autoCapitalize="none"
      />
      {errors.email && <Text>{errors.email}</Text>}

      <TextInput
        value={form.password}
        onChangeText={(text) => setForm({ ...form, password: text })}
        placeholder="Password"
        secureTextEntry
      />
      {errors.password && <Text>{errors.password}</Text>}

      <Pressable onPress={handleSubmit} disabled={isSubmitting}>
        <Text>{isSubmitting ? "Loading..." : "Sign In"}</Text>
      </Pressable>
    </View>
  );
}
```

## Infinite Scroll List

```typescript
import { FlatList, ActivityIndicator } from "react-native";
import { useInfiniteQuery } from "@tanstack/react-query";

export function InfiniteList() {
  const { data, fetchNextPage, hasNextPage, isFetchingNextPage } =
    useInfiniteQuery({
      queryKey: ["items"],
      queryFn: ({ pageParam = 1 }) => fetchItems(pageParam),
      getNextPageParam: (lastPage) => lastPage.nextPage,
      initialPageParam: 1,
    });

  const items = data?.pages.flatMap((page) => page.items) ?? [];

  return (
    <FlatList
      data={items}
      keyExtractor={(item) => item.id}
      renderItem={({ item }) => <ItemCard item={item} />}
      onEndReached={() => hasNextPage && fetchNextPage()}
      onEndReachedThreshold={0.5}
      ListFooterComponent={isFetchingNextPage ? <ActivityIndicator /> : null}
    />
  );
}
```

## Pull to Refresh

```typescript
import { FlatList, RefreshControl } from "react-native";
import { useQuery } from "@tanstack/react-query";

export function RefreshableList() {
  const { data, refetch, isRefetching } = useQuery({
    queryKey: ["items"],
    queryFn: fetchItems,
  });

  return (
    <FlatList
      data={data}
      refreshControl={
        <RefreshControl refreshing={isRefetching} onRefresh={refetch} />
      }
      renderItem={({ item }) => <ItemCard item={item} />}
    />
  );
}
```

## Keyboard Avoiding

```typescript
import { KeyboardAvoidingView, Platform, ScrollView } from "react-native";

export function FormScreen({ children }: { children: ReactNode }) {
  return (
    <KeyboardAvoidingView
      behavior={Platform.OS === "ios" ? "padding" : "height"}
      style={{ flex: 1 }}
    >
      <ScrollView
        contentContainerStyle={{ flexGrow: 1 }}
        keyboardShouldPersistTaps="handled"
      >
        {children}
      </ScrollView>
    </KeyboardAvoidingView>
  );
}
```

## Deep Link Handling

```typescript
// app.json
{
  "expo": {
    "scheme": "myapp",
    "android": {
      "intentFilters": [{
        "action": "VIEW",
        "data": [{ "scheme": "myapp" }, { "scheme": "https", "host": "myapp.com" }],
        "category": ["BROWSABLE", "DEFAULT"]
      }]
    }
  }
}

// Usage in component
import { useLocalSearchParams } from 'expo-router';
import * as Linking from 'expo-linking';

const { id } = useLocalSearchParams<{ id: string }>();

// Open deep link
Linking.openURL('myapp://product/123');
```

## Environment Variables

```typescript
// app.config.js
export default {
  expo: {
    extra: {
      apiUrl: process.env.API_URL,
      env: process.env.APP_ENV ?? "development",
    },
  },
};

// Usage
import Constants from "expo-constants";
const { apiUrl, env } = Constants.expoConfig?.extra ?? {};
```
