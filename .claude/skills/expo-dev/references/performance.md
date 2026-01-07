# Performance Optimization

Performance patterns for React Native / Expo apps.

## List Optimization

### FlatList Best Practices

```typescript
import { FlatList, View, Text } from 'react-native';
import { memo, useCallback } from 'react';

// 1. Memoize list items
const ListItem = memo(function ListItem({ item }: { item: Item }) {
  return (
    <View>
      <Text>{item.title}</Text>
    </View>
  );
});

// 2. Stable key extractor
const keyExtractor = (item: Item) => item.id;

// 3. Memoize renderItem
const renderItem = useCallback(({ item }: { item: Item }) => <ListItem item={item} />, []);

// 4. Fixed item height (when possible)
const getItemLayout = (_: any, index: number) => ({
  length: ITEM_HEIGHT,
  offset: ITEM_HEIGHT * index,
  index,
});

<FlatList
  data={items}
  renderItem={renderItem}
  keyExtractor={keyExtractor}
  getItemLayout={getItemLayout}
  removeClippedSubviews={true}
  maxToRenderPerBatch={10}
  windowSize={5}
  initialNumToRender={10}
  updateCellsBatchingPeriod={50}
/>
```

### FlashList (Faster Alternative)

```bash
npx expo install @shopify/flash-list
```

```typescript
import { FlashList } from '@shopify/flash-list';

<FlashList
  data={items}
  renderItem={renderItem}
  keyExtractor={keyExtractor}
  estimatedItemSize={80}
  drawDistance={250}
/>
```

## Image Optimization

### expo-image (Recommended)

```typescript
import { Image } from 'expo-image';

<Image
  source={{ uri: imageUrl }}
  style={{ width: 200, height: 200 }}
  contentFit="cover"
  transition={200}
  placeholder={blurhash}
  cachePolicy="memory-disk"
  recyclingKey={item.id} // Helps with list recycling
/>
```

### Image Caching Strategy

```typescript
import { Image } from 'expo-image';

// Prefetch images
Image.prefetch([imageUrl1, imageUrl2, imageUrl3]);

// Clear cache if needed
Image.clearDiskCache();
Image.clearMemoryCache();
```

## Memoization

### React.memo

```typescript
import { memo } from 'react';

// Only re-renders when props change
const ExpensiveComponent = memo(function ExpensiveComponent({ data }: Props) {
  return <View>{/* Complex render */}</View>;
});

// With custom comparison
const CustomMemoComponent = memo(
  function CustomMemoComponent({ item }: Props) {
    return <View />;
  },
  (prevProps, nextProps) => prevProps.item.id === nextProps.item.id
);
```

### useMemo & useCallback

```typescript
import { useMemo, useCallback } from 'react';

function ParentComponent({ items, filter }: Props) {
  // Memoize expensive computations
  const filteredItems = useMemo(
    () => items.filter((item) => item.category === filter),
    [items, filter]
  );

  // Memoize callbacks passed to children
  const handlePress = useCallback((id: string) => {
    router.push(`/item/${id}`);
  }, []);

  return (
    <FlatList
      data={filteredItems}
      renderItem={({ item }) => <ListItem item={item} onPress={handlePress} />}
    />
  );
}
```

## Animation Performance

### Use Native Driver

```typescript
import { Animated } from 'react-native';

// ✅ Uses native thread
Animated.timing(opacity, {
  toValue: 1,
  duration: 300,
  useNativeDriver: true, // Important!
}).start();

// ❌ Runs on JS thread (slower)
Animated.timing(height, {
  toValue: 100,
  duration: 300,
  useNativeDriver: false, // Required for layout properties
}).start();
```

### Reanimated (Better Performance)

```bash
npx expo install react-native-reanimated
```

```typescript
import Animated, {
  useAnimatedStyle,
  useSharedValue,
  withSpring,
} from 'react-native-reanimated';

function AnimatedBox() {
  const offset = useSharedValue(0);

  const animatedStyle = useAnimatedStyle(() => ({
    transform: [{ translateX: offset.value }],
  }));

  const moveRight = () => {
    offset.value = withSpring(offset.value + 50);
  };

  return (
    <Animated.View style={[styles.box, animatedStyle]}>
      <Pressable onPress={moveRight} />
    </Animated.View>
  );
}
```

## Heavy Computation

### InteractionManager

```typescript
import { InteractionManager } from 'react-native';

useEffect(() => {
  // Wait until animations complete
  const task = InteractionManager.runAfterInteractions(() => {
    // Expensive work here
    processLargeDataset();
  });

  return () => task.cancel();
}, []);
```

### Web Workers (expo-worker)

```typescript
// worker.ts
const ctx: Worker = self as any;

ctx.onmessage = (event) => {
  const result = heavyComputation(event.data);
  ctx.postMessage(result);
};

// Component
import { useWorker } from 'expo-worker';

function Component() {
  const worker = useWorker(require('./worker.ts'));

  const compute = async () => {
    worker.postMessage(data);
    worker.onmessage = (e) => setResult(e.data);
  };
}
```

## Memory Management

### Cleanup Effects

```typescript
useEffect(() => {
  const subscription = eventEmitter.addListener('event', handler);
  const interval = setInterval(tick, 1000);

  return () => {
    subscription.remove();
    clearInterval(interval);
  };
}, []);
```

### Avoid Memory Leaks

```typescript
function Component() {
  const [data, setData] = useState(null);
  const isMounted = useRef(true);

  useEffect(() => {
    isMounted.current = true;

    fetchData().then((result) => {
      if (isMounted.current) {
        setData(result); // Only update if mounted
      }
    });

    return () => {
      isMounted.current = false;
    };
  }, []);

  return <View />;
}
```

## Bundle Size

### Tree Shaking Imports

```typescript
// ❌ Imports entire library
import { format } from 'date-fns';

// ✅ Import only what you need
import format from 'date-fns/format';

// ❌ Imports all icons
import { Ionicons } from '@expo/vector-icons';

// ✅ Use specific icon
import Ionicons from '@expo/vector-icons/Ionicons';
```

### Analyze Bundle

```bash
npx expo export --dump-sourcemap
npx source-map-explorer dist/_expo/static/js/*.js
```

## Profiling

### React DevTools Profiler

```typescript
// Enable in development
if (__DEV__) {
  require('react-devtools');
}
```

### Performance Monitoring

```typescript
import * as Updates from 'expo-updates';

// Track app startup time
const startTime = Date.now();

export function App() {
  useEffect(() => {
    const loadTime = Date.now() - startTime;
    analytics.track('app_loaded', { loadTime });
  }, []);
}
```

## Quick Wins Checklist

- [ ] Use `FlashList` instead of `FlatList` for long lists
- [ ] Use `expo-image` instead of `Image`
- [ ] Add `keyExtractor` to all lists
- [ ] Memoize list items with `memo()`
- [ ] Use `useCallback` for event handlers passed to children
- [ ] Enable `useNativeDriver: true` for animations
- [ ] Avoid inline styles in render
- [ ] Use `InteractionManager` for heavy work after navigation
- [ ] Clean up subscriptions and timers in effects
- [ ] Import only needed modules (tree shaking)
