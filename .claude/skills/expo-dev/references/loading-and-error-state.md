# Loading & Error States

Patterns for handling loading, error, and empty states.

## Loading States

### Simple Loading

```typescript
import { ActivityIndicator, View } from 'react-native';

export function LoadingSpinner({ size = 'large' }: { size?: 'small' | 'large' }) {
  return (
    <View style={{ flex: 1, justifyContent: 'center', alignItems: 'center' }}>
      <ActivityIndicator size={size} />
    </View>
  );
}
```

### Skeleton Loading

```typescript
import { useEffect, useRef } from 'react';
import { View, Animated, ViewStyle } from 'react-native';

interface SkeletonProps {
  width: number | string;
  height: number;
  borderRadius?: number;
  style?: ViewStyle;
}

export function Skeleton({ width, height, borderRadius = 4, style }: SkeletonProps) {
  const opacity = useRef(new Animated.Value(0.3)).current;

  useEffect(() => {
    const animation = Animated.loop(
      Animated.sequence([
        Animated.timing(opacity, { toValue: 1, duration: 500, useNativeDriver: true }),
        Animated.timing(opacity, { toValue: 0.3, duration: 500, useNativeDriver: true }),
      ])
    );
    animation.start();
    return () => animation.stop();
  }, []);

  return (
    <Animated.View
      style={[{ width, height, borderRadius, backgroundColor: '#E1E9EE', opacity }, style]}
    />
  );
}

// Usage
function CardSkeleton() {
  return (
    <View style={{ padding: 16 }}>
      <Skeleton width="100%" height={200} borderRadius={12} />
      <Skeleton width="70%" height={20} style={{ marginTop: 12 }} />
      <Skeleton width="50%" height={16} style={{ marginTop: 8 }} />
    </View>
  );
}
```

### Loading Overlay

```typescript
import { Modal, View, ActivityIndicator, Text } from 'react-native';

interface LoadingOverlayProps {
  visible: boolean;
  message?: string;
}

export function LoadingOverlay({ visible, message }: LoadingOverlayProps) {
  return (
    <Modal visible={visible} transparent animationType="fade">
      <View
        style={{
          flex: 1,
          backgroundColor: 'rgba(0,0,0,0.5)',
          justifyContent: 'center',
          alignItems: 'center',
        }}
      >
        <View
          style={{
            backgroundColor: 'white',
            padding: 24,
            borderRadius: 12,
            alignItems: 'center',
          }}
        >
          <ActivityIndicator size="large" />
          {message && <Text style={{ marginTop: 12 }}>{message}</Text>}
        </View>
      </View>
    </Modal>
  );
}
```

## Error States

### Error Boundary

```typescript
import { Component, ReactNode } from 'react';
import { View, Text, Button } from 'react-native';

interface Props {
  children: ReactNode;
  fallback?: ReactNode;
}

interface State {
  hasError: boolean;
  error?: Error;
}

export class ErrorBoundary extends Component<Props, State> {
  state: State = { hasError: false };

  static getDerivedStateFromError(error: Error): State {
    return { hasError: true, error };
  }

  handleReset = () => {
    this.setState({ hasError: false, error: undefined });
  };

  render() {
    if (this.state.hasError) {
      return this.props.fallback || <ErrorFallback onReset={this.handleReset} />;
    }
    return this.props.children;
  }
}

function ErrorFallback({ onReset }: { onReset: () => void }) {
  return (
    <View style={{ flex: 1, justifyContent: 'center', alignItems: 'center', padding: 20 }}>
      <Text style={{ fontSize: 18, fontWeight: 'bold' }}>Something went wrong</Text>
      <Text style={{ marginTop: 8, color: '#666', textAlign: 'center' }}>
        An unexpected error occurred. Please try again.
      </Text>
      <Button title="Try Again" onPress={onReset} />
    </View>
  );
}
```

### Error Component

```typescript
import { View, Text, Pressable } from 'react-native';

interface ErrorViewProps {
  title?: string;
  message?: string;
  onRetry?: () => void;
}

export function ErrorView({
  title = 'Error',
  message = 'Something went wrong',
  onRetry,
}: ErrorViewProps) {
  return (
    <View style={{ flex: 1, justifyContent: 'center', alignItems: 'center', padding: 20 }}>
      <Text style={{ fontSize: 48 }}>⚠️</Text>
      <Text style={{ fontSize: 20, fontWeight: 'bold', marginTop: 16 }}>{title}</Text>
      <Text style={{ fontSize: 14, color: '#666', marginTop: 8, textAlign: 'center' }}>
        {message}
      </Text>
      {onRetry && (
        <Pressable
          onPress={onRetry}
          style={{
            marginTop: 24,
            backgroundColor: '#007AFF',
            paddingHorizontal: 24,
            paddingVertical: 12,
            borderRadius: 8,
          }}
        >
          <Text style={{ color: 'white', fontWeight: '600' }}>Try Again</Text>
        </Pressable>
      )}
    </View>
  );
}
```

### Network Error

```typescript
import NetInfo from '@react-native-community/netinfo';
import { useEffect, useState } from 'react';

export function useNetworkStatus() {
  const [isConnected, setIsConnected] = useState(true);

  useEffect(() => {
    const unsubscribe = NetInfo.addEventListener((state) => {
      setIsConnected(state.isConnected ?? true);
    });
    return unsubscribe;
  }, []);

  return isConnected;
}

export function OfflineBanner() {
  const isConnected = useNetworkStatus();

  if (isConnected) return null;

  return (
    <View style={{ backgroundColor: '#FF3B30', padding: 8 }}>
      <Text style={{ color: 'white', textAlign: 'center' }}>No internet connection</Text>
    </View>
  );
}
```

## Empty States

```typescript
import { View, Text, Pressable } from 'react-native';

interface EmptyStateProps {
  icon?: string;
  title: string;
  description?: string;
  actionLabel?: string;
  onAction?: () => void;
}

export function EmptyState({ icon = '📭', title, description, actionLabel, onAction }: EmptyStateProps) {
  return (
    <View style={{ flex: 1, justifyContent: 'center', alignItems: 'center', padding: 32 }}>
      <Text style={{ fontSize: 64 }}>{icon}</Text>
      <Text style={{ fontSize: 20, fontWeight: 'bold', marginTop: 16, textAlign: 'center' }}>
        {title}
      </Text>
      {description && (
        <Text style={{ fontSize: 14, color: '#666', marginTop: 8, textAlign: 'center' }}>
          {description}
        </Text>
      )}
      {actionLabel && onAction && (
        <Pressable
          onPress={onAction}
          style={{
            marginTop: 24,
            backgroundColor: '#007AFF',
            paddingHorizontal: 24,
            paddingVertical: 12,
            borderRadius: 8,
          }}
        >
          <Text style={{ color: 'white', fontWeight: '600' }}>{actionLabel}</Text>
        </Pressable>
      )}
    </View>
  );
}

// Usage
<EmptyState
  icon="📝"
  title="No todos yet"
  description="Create your first todo to get started"
  actionLabel="Create Todo"
  onAction={() => setShowCreateModal(true)}
/>
```

## Combined Pattern

```typescript
import { useQuery } from '@tanstack/react-query';

interface AsyncStateProps<T> {
  queryKey: string[];
  queryFn: () => Promise<T>;
  renderData: (data: T) => ReactNode;
  renderLoading?: () => ReactNode;
  renderError?: (error: Error, retry: () => void) => ReactNode;
  renderEmpty?: () => ReactNode;
  isEmpty?: (data: T) => boolean;
}

export function AsyncState<T>({
  queryKey,
  queryFn,
  renderData,
  renderLoading = () => <LoadingSpinner />,
  renderError = (error, retry) => <ErrorView message={error.message} onRetry={retry} />,
  renderEmpty = () => <EmptyState title="No data" />,
  isEmpty = (data) => Array.isArray(data) && data.length === 0,
}: AsyncStateProps<T>) {
  const { data, isLoading, isError, error, refetch } = useQuery({ queryKey, queryFn });

  if (isLoading) return renderLoading();
  if (isError) return renderError(error as Error, refetch);
  if (!data || isEmpty(data)) return renderEmpty();

  return <>{renderData(data)}</>;
}

// Usage
<AsyncState
  queryKey={['todos']}
  queryFn={fetchTodos}
  renderData={(todos) => <TodoList todos={todos} />}
  renderEmpty={() => <EmptyState icon="📝" title="No todos yet" />}
/>
```

## React Query States

```typescript
function TodoList() {
  const { data, isLoading, isFetching, isError, error, refetch, isRefetching } = useQuery({
    queryKey: ['todos'],
    queryFn: fetchTodos,
  });

  // First load
  if (isLoading) return <LoadingSpinner />;

  // Error state
  if (isError) return <ErrorView message={error.message} onRetry={refetch} />;

  // Empty state
  if (!data?.length) return <EmptyState title="No todos" />;

  return (
    <View style={{ flex: 1 }}>
      {/* Background refresh indicator */}
      {isFetching && !isRefetching && (
        <ActivityIndicator style={{ position: 'absolute', top: 10, right: 10 }} />
      )}

      <FlatList
        data={data}
        renderItem={({ item }) => <TodoItem todo={item} />}
        refreshControl={<RefreshControl refreshing={isRefetching} onRefresh={refetch} />}
      />
    </View>
  );
}
```
