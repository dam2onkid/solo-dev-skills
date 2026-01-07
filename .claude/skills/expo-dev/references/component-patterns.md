# Component Patterns

Reusable component patterns for React Native.

## Base Component Structure

```typescript
import { View, Text, Pressable, ViewProps } from "react-native";
import { forwardRef } from "react";

type ButtonVariant = "primary" | "secondary" | "ghost";
type ButtonSize = "sm" | "md" | "lg";

interface ButtonProps extends ViewProps {
  title: string;
  variant?: ButtonVariant;
  size?: ButtonSize;
  disabled?: boolean;
  loading?: boolean;
  onPress?: () => void;
}

export const Button = forwardRef<View, ButtonProps>(
  (
    {
      title,
      variant = "primary",
      size = "md",
      disabled,
      loading,
      onPress,
      ...props
    },
    ref
  ) => {
    return (
      <Pressable
        ref={ref}
        onPress={onPress}
        disabled={disabled || loading}
        {...props}
      >
        {loading ? <ActivityIndicator /> : <Text>{title}</Text>}
      </Pressable>
    );
  }
);
```

## Compound Components

```typescript
import { createContext, useContext, ReactNode } from "react";
import { View, Text, Pressable } from "react-native";

type CardContextType = { variant: "default" | "elevated" };
const CardContext = createContext<CardContextType>({ variant: "default" });

function CardRoot({
  children,
  variant = "default",
}: {
  children: ReactNode;
  variant?: "default" | "elevated";
}) {
  return (
    <CardContext.Provider value={{ variant }}>
      <View>{children}</View>
    </CardContext.Provider>
  );
}

function CardHeader({ children }: { children: ReactNode }) {
  return <View>{children}</View>;
}

function CardTitle({ children }: { children: string }) {
  return <Text>{children}</Text>;
}

function CardContent({ children }: { children: ReactNode }) {
  return <View>{children}</View>;
}

function CardFooter({ children }: { children: ReactNode }) {
  return <View>{children}</View>;
}

export const Card = Object.assign(CardRoot, {
  Header: CardHeader,
  Title: CardTitle,
  Content: CardContent,
  Footer: CardFooter,
});

// Usage
<Card variant="elevated">
  <Card.Header>
    <Card.Title>Title</Card.Title>
  </Card.Header>
  <Card.Content>
    <Text>Content</Text>
  </Card.Content>
</Card>;
```

## Polymorphic Component

```typescript
import { ElementType, ComponentPropsWithoutRef, ReactNode } from 'react';

type PolymorphicProps<T extends ElementType> = {
  as?: T;
  children?: ReactNode;
} & ComponentPropsWithoutRef<T>;

export function Box<T extends ElementType = typeof View>({
  as,
  children,
  ...props
}: PolymorphicProps<T>) {
  const Component = as || View;
  return <Component {...props}>{children}</Component>;
}

// Usage
<Box as={Pressable} onPress={() => {}}>Content</Box>
<Box as={ScrollView}>Scrollable</Box>
```

## Render Props

```typescript
import { useState, ReactNode } from "react";

interface ToggleProps {
  children: (props: { isOn: boolean; toggle: () => void }) => ReactNode;
  initialValue?: boolean;
}

export function Toggle({ children, initialValue = false }: ToggleProps) {
  const [isOn, setIsOn] = useState(initialValue);
  const toggle = () => setIsOn((prev) => !prev);
  return <>{children({ isOn, toggle })}</>;
}

// Usage
<Toggle>
  {({ isOn, toggle }) => (
    <Pressable onPress={toggle}>
      <Text>{isOn ? "ON" : "OFF"}</Text>
    </Pressable>
  )}
</Toggle>;
```

## Controlled/Uncontrolled

```typescript
import { useState, useCallback } from "react";
import { TextInput, TextInputProps } from "react-native";

interface InputProps extends Omit<TextInputProps, "value" | "onChangeText"> {
  value?: string;
  defaultValue?: string;
  onChangeText?: (text: string) => void;
}

export function Input({
  value: controlledValue,
  defaultValue,
  onChangeText,
  ...props
}: InputProps) {
  const [uncontrolledValue, setUncontrolledValue] = useState(
    defaultValue ?? ""
  );
  const isControlled = controlledValue !== undefined;
  const value = isControlled ? controlledValue : uncontrolledValue;

  const handleChange = useCallback(
    (text: string) => {
      if (!isControlled) setUncontrolledValue(text);
      onChangeText?.(text);
    },
    [isControlled, onChangeText]
  );

  return <TextInput value={value} onChangeText={handleChange} {...props} />;
}
```

## Higher Order Component (HOC)

```typescript
import { ComponentType } from "react";
import { ActivityIndicator, View } from "react-native";

interface WithLoadingProps {
  isLoading: boolean;
}

export function withLoading<P extends object>(
  WrappedComponent: ComponentType<P>
) {
  return function WithLoadingComponent({
    isLoading,
    ...props
  }: P & WithLoadingProps) {
    if (isLoading) {
      return (
        <View
          style={{ flex: 1, justifyContent: "center", alignItems: "center" }}
        >
          <ActivityIndicator size="large" />
        </View>
      );
    }
    return <WrappedComponent {...(props as P)} />;
  };
}

// Usage
const UserProfileWithLoading = withLoading(UserProfile);
<UserProfileWithLoading isLoading={isLoading} user={user} />;
```

## Custom Hook Composition

```typescript
function useCounter(initial = 0) {
  const [count, setCount] = useState(initial);
  const increment = () => setCount((c) => c + 1);
  const decrement = () => setCount((c) => c - 1);
  const reset = () => setCount(initial);
  return { count, increment, decrement, reset };
}

function useToggle(initial = false) {
  const [value, setValue] = useState(initial);
  const toggle = () => setValue((v) => !v);
  const setTrue = () => setValue(true);
  const setFalse = () => setValue(false);
  return { value, toggle, setTrue, setFalse };
}

function usePrevious<T>(value: T): T | undefined {
  const ref = useRef<T>();
  useEffect(() => {
    ref.current = value;
  }, [value]);
  return ref.current;
}
```

## List Item Component

```typescript
import { memo } from "react";
import { View, Text, Pressable, Image } from "react-native";

interface ListItemProps {
  title: string;
  subtitle?: string;
  imageUri?: string;
  onPress?: () => void;
  rightElement?: ReactNode;
}

export const ListItem = memo(function ListItem({
  title,
  subtitle,
  imageUri,
  onPress,
  rightElement,
}: ListItemProps) {
  return (
    <Pressable onPress={onPress}>
      <View style={{ flexDirection: "row", alignItems: "center", padding: 16 }}>
        {imageUri && (
          <Image source={{ uri: imageUri }} style={{ width: 48, height: 48 }} />
        )}
        <View style={{ flex: 1, marginLeft: imageUri ? 12 : 0 }}>
          <Text style={{ fontSize: 16, fontWeight: "600" }}>{title}</Text>
          {subtitle && (
            <Text style={{ fontSize: 14, color: "#666" }}>{subtitle}</Text>
          )}
        </View>
        {rightElement}
      </View>
    </Pressable>
  );
});
```

## Modal Component

```typescript
import { Modal as RNModal, View, Pressable, Text } from "react-native";

interface ModalProps {
  visible: boolean;
  onClose: () => void;
  title?: string;
  children: ReactNode;
}

export function Modal({ visible, onClose, title, children }: ModalProps) {
  return (
    <RNModal
      visible={visible}
      transparent
      animationType="fade"
      onRequestClose={onClose}
    >
      <Pressable
        style={{ flex: 1, backgroundColor: "rgba(0,0,0,0.5)" }}
        onPress={onClose}
      >
        <View style={{ flex: 1, justifyContent: "center", padding: 20 }}>
          <Pressable onPress={(e) => e.stopPropagation()}>
            <View
              style={{
                backgroundColor: "white",
                borderRadius: 12,
                padding: 20,
              }}
            >
              {title && (
                <Text style={{ fontSize: 18, fontWeight: "bold" }}>
                  {title}
                </Text>
              )}
              {children}
            </View>
          </Pressable>
        </View>
      </Pressable>
    </RNModal>
  );
}
```
