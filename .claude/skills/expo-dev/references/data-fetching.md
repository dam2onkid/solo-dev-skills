# Data Fetching with React Query

TanStack Query (React Query) patterns for Expo apps.

## Setup

```bash
npx expo install @tanstack/react-query
```

```typescript
// app/_layout.tsx
import { QueryClient, QueryClientProvider } from "@tanstack/react-query";

const queryClient = new QueryClient({
  defaultOptions: {
    queries: {
      staleTime: 1000 * 60 * 5, // 5 minutes
      gcTime: 1000 * 60 * 30, // 30 minutes (previously cacheTime)
      retry: 2,
      refetchOnWindowFocus: false, // Disable for mobile
    },
  },
});

export default function RootLayout() {
  return (
    <QueryClientProvider client={queryClient}>
      <Stack />
    </QueryClientProvider>
  );
}
```

## Basic Query

```typescript
import { useQuery } from "@tanstack/react-query";

const fetchTodos = async (): Promise<Todo[]> => {
  const response = await fetch("https://api.example.com/todos");
  if (!response.ok) throw new Error("Failed to fetch");
  return response.json();
};

export function TodoList() {
  const { data, isLoading, isError, error, refetch } = useQuery({
    queryKey: ["todos"],
    queryFn: fetchTodos,
  });

  if (isLoading) return <ActivityIndicator />;
  if (isError) return <Text>Error: {error.message}</Text>;

  return (
    <FlatList
      data={data}
      renderItem={({ item }) => <TodoItem todo={item} />}
      refreshControl={<RefreshControl refreshing={false} onRefresh={refetch} />}
    />
  );
}
```

## Query with Parameters

```typescript
const fetchTodo = async (id: string): Promise<Todo> => {
  const response = await fetch(`https://api.example.com/todos/${id}`);
  if (!response.ok) throw new Error("Todo not found");
  return response.json();
};

export function TodoDetail({ id }: { id: string }) {
  const { data, isLoading } = useQuery({
    queryKey: ["todo", id],
    queryFn: () => fetchTodo(id),
    enabled: !!id, // Only fetch if id exists
  });

  if (isLoading) return <ActivityIndicator />;
  return <Text>{data?.title}</Text>;
}
```

## Mutations

```typescript
import { useMutation, useQueryClient } from "@tanstack/react-query";

const createTodo = async (title: string): Promise<Todo> => {
  const response = await fetch("https://api.example.com/todos", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ title }),
  });
  if (!response.ok) throw new Error("Failed to create");
  return response.json();
};

export function CreateTodo() {
  const queryClient = useQueryClient();
  const [title, setTitle] = useState("");

  const mutation = useMutation({
    mutationFn: createTodo,
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ["todos"] });
      setTitle("");
    },
    onError: (error) => {
      Alert.alert("Error", error.message);
    },
  });

  return (
    <View>
      <TextInput value={title} onChangeText={setTitle} />
      <Button
        title={mutation.isPending ? "Creating..." : "Create"}
        onPress={() => mutation.mutate(title)}
        disabled={mutation.isPending || !title}
      />
    </View>
  );
}
```

## Optimistic Updates

```typescript
const updateTodo = async ({
  id,
  completed,
}: {
  id: string;
  completed: boolean;
}) => {
  const response = await fetch(`https://api.example.com/todos/${id}`, {
    method: "PATCH",
    body: JSON.stringify({ completed }),
  });
  return response.json();
};

export function useTodoToggle() {
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: updateTodo,
    onMutate: async ({ id, completed }) => {
      await queryClient.cancelQueries({ queryKey: ["todos"] });
      const previousTodos = queryClient.getQueryData<Todo[]>(["todos"]);

      queryClient.setQueryData<Todo[]>(["todos"], (old) =>
        old?.map((todo) => (todo.id === id ? { ...todo, completed } : todo))
      );

      return { previousTodos };
    },
    onError: (_err, _variables, context) => {
      queryClient.setQueryData(["todos"], context?.previousTodos);
    },
    onSettled: () => {
      queryClient.invalidateQueries({ queryKey: ["todos"] });
    },
  });
}
```

## Infinite Query (Pagination)

```typescript
import { useInfiniteQuery } from "@tanstack/react-query";

type PageResponse = {
  items: Item[];
  nextCursor?: string;
};

const fetchItems = async ({
  pageParam,
}: {
  pageParam?: string;
}): Promise<PageResponse> => {
  const url = pageParam
    ? `https://api.example.com/items?cursor=${pageParam}`
    : "https://api.example.com/items";
  const response = await fetch(url);
  return response.json();
};

export function InfiniteList() {
  const { data, fetchNextPage, hasNextPage, isFetchingNextPage, isLoading } =
    useInfiniteQuery({
      queryKey: ["items"],
      queryFn: fetchItems,
      initialPageParam: undefined,
      getNextPageParam: (lastPage) => lastPage.nextCursor,
    });

  const items = data?.pages.flatMap((page) => page.items) ?? [];

  if (isLoading) return <ActivityIndicator />;

  return (
    <FlatList
      data={items}
      keyExtractor={(item) => item.id}
      renderItem={({ item }) => <ItemCard item={item} />}
      onEndReached={() => hasNextPage && !isFetchingNextPage && fetchNextPage()}
      onEndReachedThreshold={0.5}
      ListFooterComponent={isFetchingNextPage ? <ActivityIndicator /> : null}
    />
  );
}
```

## Prefetching

```typescript
const queryClient = useQueryClient();

// Prefetch on hover/focus
const prefetchTodo = (id: string) => {
  queryClient.prefetchQuery({
    queryKey: ["todo", id],
    queryFn: () => fetchTodo(id),
    staleTime: 1000 * 60 * 5,
  });
};

// In list item
<Pressable
  onPressIn={() => prefetchTodo(item.id)}
  onPress={() => router.push(`/todo/${item.id}`)}
>
  <Text>{item.title}</Text>
</Pressable>;
```

## Custom Query Hook

```typescript
// hooks/useTodos.ts
export function useTodos(filters?: TodoFilters) {
  return useQuery({
    queryKey: ["todos", filters],
    queryFn: () => fetchTodos(filters),
    select: (data) => data.sort((a, b) => b.createdAt - a.createdAt),
  });
}

export function useTodo(id: string) {
  return useQuery({
    queryKey: ["todo", id],
    queryFn: () => fetchTodo(id),
    enabled: !!id,
  });
}

export function useCreateTodo() {
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: createTodo,
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ["todos"] });
    },
  });
}

export function useUpdateTodo() {
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: updateTodo,
    onSuccess: (data) => {
      queryClient.invalidateQueries({ queryKey: ["todos"] });
      queryClient.setQueryData(["todo", data.id], data);
    },
  });
}

export function useDeleteTodo() {
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: deleteTodo,
    onSuccess: (_, id) => {
      queryClient.invalidateQueries({ queryKey: ["todos"] });
      queryClient.removeQueries({ queryKey: ["todo", id] });
    },
  });
}
```

## API Client Pattern

```typescript
// lib/api.ts
import * as SecureStore from "expo-secure-store";

const BASE_URL = "https://api.example.com";

async function getAuthHeaders() {
  const token = await SecureStore.getItemAsync("token");
  return token ? { Authorization: `Bearer ${token}` } : {};
}

export async function apiClient<T>(
  endpoint: string,
  options?: RequestInit
): Promise<T> {
  const headers = {
    "Content-Type": "application/json",
    ...(await getAuthHeaders()),
    ...options?.headers,
  };

  const response = await fetch(`${BASE_URL}${endpoint}`, {
    ...options,
    headers,
  });

  if (!response.ok) {
    const error = await response.json().catch(() => ({}));
    throw new Error(error.message || `Request failed: ${response.status}`);
  }

  return response.json();
}

// Usage
export const todosApi = {
  getAll: () => apiClient<Todo[]>("/todos"),
  getById: (id: string) => apiClient<Todo>(`/todos/${id}`),
  create: (data: CreateTodoDto) =>
    apiClient<Todo>("/todos", { method: "POST", body: JSON.stringify(data) }),
  update: (id: string, data: UpdateTodoDto) =>
    apiClient<Todo>(`/todos/${id}`, {
      method: "PATCH",
      body: JSON.stringify(data),
    }),
  delete: (id: string) => apiClient<void>(`/todos/${id}`, { method: "DELETE" }),
};
```
