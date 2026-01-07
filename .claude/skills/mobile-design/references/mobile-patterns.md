# Mobile Navigation & UI Patterns

## Navigation Patterns

### Tab Bar (Bottom Navigation)
Best for 3-5 top-level destinations.
```
┌─────────────────────────┐
│      Screen Content     │
├─────┬─────┬─────┬─────┬─┤
│ 🏠  │ 🔍  │ ➕  │ ❤️  │ 👤 │
└─────┴─────┴─────┴─────┴─┘
```
- Clear active state
- Consistent across screens
- Most important destinations only

### Navigation Stack
Hierarchical content and detail views.
```
← Back    Title         Action
─────────────────────────────
│      Detail Content       │
```
- Always provide back navigation
- Consistent header styling
- Collapsing headers for more content

### Navigation Drawer
Many destinations, infrequent switching.
```
☰ App Title          🔔 ⚙️
─────────────────────────
│      Main Content      │
```
- Less discoverable than tabs
- Good for settings, secondary features
- More common on Android

### Bottom Sheet
Actions, filters, secondary content.
```
│      Main Content      │
├────────────────────────┤
│ ═══════ (handle)       │
│ Sheet Content          │
└────────────────────────┘
```
- Swipe to expand/dismiss
- Modal or persistent
- Don't overload with options

## Screen Patterns

### List Screen
```
← Title              Filter
─────────────────────────
🔍 Search...
─────────────────────────
┌─────────────────────┐
│ 🖼 Title            > │
│    Subtitle          │
└─────────────────────┘
```
- Pull to refresh
- Swipe/long-press actions
- Lazy loading for long lists

### Detail Screen
```
←                     ⋮
┌───────────────────────┐
│    Hero Image         │
└───────────────────────┘
Title
Subtitle • Metadata

Description text...
─────────────────────────
    [ Primary Action ]
```
- Collapsing hero
- Sticky action bar
- Share/save options

### Form Screen
```
← Create Account    Save
─────────────────────────
Email
┌───────────────────────┐
│ user@example.com      │
└───────────────────────┘

Password
┌───────────────────────┐
│ ••••••••           👁 │
└───────────────────────┘
Hint text

☐ I agree to Terms
─────────────────────────
    [ Submit ]
```
- Inline validation
- Clear error states
- Smart keyboard types
- Sticky submit button

### Empty State
```
        🎨

   No items yet

 Add your first item
  to get started.

    [ Add Item ]
```
- Friendly illustration
- Clear explanation
- Action to resolve

### Error State
```
        ⚠️

Something went wrong

We couldn't load your
data. Please try again.

     [ Retry ]
```
- Friendly, not technical
- Actionable solution
- Retry mechanism

## Component Patterns

### Cards
- Self-contained content units
- Entire card as touch target (when applicable)
- Consistent corner radius and padding

### Lists
- Simple (title), two-line, or three-line
- Leading icons/avatars
- Trailing actions/chevrons
- Swipe for quick actions

### Buttons
- **Primary**: High emphasis, filled
- **Secondary**: Medium emphasis, outlined/tinted
- **Tertiary**: Low emphasis, text only
- Full-width in forms, floating for primary create action

### Inputs
- Label above field
- Placeholder for format hints
- Helper/error text below
- Appropriate keyboard type

### Modals & Dialogs
- iOS: Action sheets from bottom, alerts centered
- Android: Bottom sheets, centered dialogs
- Clear dismiss mechanism

### Toasts & Snackbars
- Non-blocking feedback
- Auto-dismiss
- Position above navigation
- Optional undo action

## Responsive Design

### Adaptation Strategies
- **Fluid**: Components stretch/compress
- **Adaptive**: Different layouts at breakpoints
- **Hide/show**: More content on larger screens

### Tablet Patterns
```
┌────────────┬────────────────────┐
│   List     │    Detail          │
│  Item 1    │   Selected Item    │
│  Item 2 ◄──│   Details here     │
│  Item 3    │                    │
└────────────┴────────────────────┘
```
- Master-detail when space allows
- Utilize extra space meaningfully
- Don't just scale up phone layouts
