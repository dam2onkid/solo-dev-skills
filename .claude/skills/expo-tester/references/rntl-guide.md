# React Native Testing Library Guide

## Query Priority

Use queries in this order (most to least preferred):

1. `getByRole` - accessibility role + name (best)
2. `getByLabelText` - form inputs with labels
3. `getByPlaceholderText` - inputs with placeholder
4. `getByText` - visible text content
5. `getByDisplayValue` - current input value
6. `getByTestId` - last resort (data-testid)

## Query Variants

| Prefix    | No Match | 1 Match | 1+ Match | Async |
| --------- | -------- | ------- | -------- | ----- |
| getBy     | throw    | return  | throw    | No    |
| getAllBy  | throw    | array   | array    | No    |
| queryBy   | null     | return  | throw    | No    |
| queryAllBy| []       | array   | array    | No    |
| findBy    | throw    | return  | throw    | Yes   |
| findAllBy | throw    | array   | array    | Yes   |

## User Events (Recommended)

```typescript
import { render, screen, userEvent } from '@testing-library/react-native';

describe('Form', () => {
  it('submits form data', async () => {
    const onSubmit = jest.fn();
    const user = userEvent.setup();
    
    render(<LoginForm onSubmit={onSubmit} />);
    
    await user.type(screen.getByLabelText('Email'), 'test@example.com');
    await user.type(screen.getByLabelText('Password'), 'password123');
    await user.press(screen.getByRole('button', { name: 'Login' }));
    
    expect(onSubmit).toHaveBeenCalledWith({
      email: 'test@example.com',
      password: 'password123'
    });
  });
});
```

## fireEvent (Lower-level)

```typescript
import { render, screen, fireEvent } from '@testing-library/react-native';

fireEvent.press(screen.getByText('Submit'));
fireEvent.changeText(screen.getByPlaceholderText('Email'), 'test@example.com');
fireEvent.scroll(screen.getByTestId('list'), { nativeEvent: { contentOffset: { y: 500 } } });
```

## Async Testing

```typescript
import { render, screen, waitFor } from '@testing-library/react-native';

it('loads data asynchronously', async () => {
  render(<DataList />);
  
  // Wait for loading to finish
  await waitFor(() => {
    expect(screen.queryByText('Loading...')).toBeNull();
  });
  
  // Or use findBy (combines getBy + waitFor)
  expect(await screen.findByText('Item 1')).toBeOnTheScreen();
});

it('handles API error', async () => {
  mockApi.mockRejectedValueOnce(new Error('Network error'));
  render(<DataList />);
  
  expect(await screen.findByText('Error loading data')).toBeOnTheScreen();
});
```

## Testing with Providers

```typescript
import { render } from '@testing-library/react-native';
import { ThemeProvider } from '@/context/ThemeContext';

const AllProviders = ({ children }) => (
  <ThemeProvider>
    <AuthProvider>
      {children}
    </AuthProvider>
  </ThemeProvider>
);

const customRender = (ui, options) =>
  render(ui, { wrapper: AllProviders, ...options });

export * from '@testing-library/react-native';
export { customRender as render };
```

## Testing Hooks

```typescript
import { renderHook, act, waitFor } from '@testing-library/react-native';
import { useCounter } from '@/hooks/useCounter';

it('increments counter', () => {
  const { result } = renderHook(() => useCounter());
  
  act(() => {
    result.current.increment();
  });
  
  expect(result.current.count).toBe(1);
});
```

## Common Matchers

```typescript
expect(element).toBeOnTheScreen();
expect(element).toBeVisible();
expect(element).toBeEnabled();
expect(element).toBeDisabled();
expect(element).toHaveTextContent('Hello');
expect(element).toHaveProp('accessibilityLabel', 'Submit button');
expect(element).toHaveStyle({ backgroundColor: 'red' });
```

## Debugging

```typescript
import { render, screen } from '@testing-library/react-native';

render(<MyComponent />);
screen.debug();                    // Print component tree
screen.debug(screen.getByRole('button')); // Print specific element
```
