---
phase: design
title: [Feature Name] - Web Design Overview
description: Overview and shared components for [feature] on web
---

# [Feature Name] - Web Design Overview

**Version**: 1.0  
**Updated**: 2025-01-XX  
**Tech Stack**: Next.js 16, React 19, Tailwind CSS, shadcn/ui

This document provides an overview of the design for [feature] features on web, using [shadcn/ui](https://ui.shadcn.com) components and [blocks](https://ui.shadcn.com/blocks).

**Reference**:

- Requirements: `docs/v1/web/requirements/[feature]/[feature]_requirements.md`
- Common Requirements: `docs/v1/requirements/[feature]/[feature]_management.md` (if applicable)
- API Design: `docs/v1/server/design/[feature]/[feature]_design.md`
- shadcn Blocks: [https://ui.shadcn.com/blocks](https://ui.shadcn.com/blocks)

---

## Document Structure

The design documents are organized into separate modules:

| Module       | File                         | Description                    |
| ------------ | ---------------------------- | ------------------------------ |
| **Overview** | `[feature]_design.md` (this) | Overview and shared components |
| **[Page 1]** | `[page1]_design.md`          | [Page 1 description]           |
| **[Page 2]** | `[page2]_design.md`          | [Page 2 description]           |

---

## 1. Design System Reference

**⚠️ IMPORTANT**: All information about design system, components, theme, typography, spacing is defined in the shared file:

**📄 See**: [`design-system.md`](../design-system.md)

This file includes:

- Component library (shadcn/ui components)
- Theme & Colors
- Typography
- Spacing & Layout
- Responsive Design
- Accessibility guidelines
- Animation & Transitions
- Error & Loading states

**Do not duplicate** this information in other design documents. Always reference `design-system.md`.

---

## 2. Shared Components

### 2.1. [Component Name]

**Component**: `components/[feature]/[component-name].tsx`

**Usage**: [How component is used]

**Props**:

```typescript
interface [ComponentName]Props {
  // Props definition
}
```

**Features**:

- [Feature 1]
- [Feature 2]

---

## 3. Component Dependencies

Details about component dependencies, installation commands, and required packages see: [`design-system.md`](../design-system.md#13-dependencies)

---

## 4. API Integration

### 4.1. API Client

**File**: `lib/api/[feature].ts`

**Functions**:

```typescript
// [Function description]
export async function [functionName](
  params: [ParamsType],
): Promise<[ResponseType]>;
```

### 4.2. React Query Hooks

**File**: `hooks/use-[feature].ts`

**Hooks**:

```typescript
// [Hook description]
export function use[Feature](
  params: [ParamsType],
): UseQueryResult<[ResponseType]>;
```

---

## 5. Routes Structure

```
/[route]
├── /[route]/[subroute]          # [Description]
└── /[route]/[subroute]/[id]     # [Description]
```

---

## 6. State Management

### 6.1. [State Type]

**Store**: [Where state is stored]

**State**:

```typescript
interface [StateName] {
  // State properties
}
```

---

## 7. Error Handling

### 7.1. Error Display

**Component**: `components/[feature]/error-display.tsx`

**Usage**: Display API errors gracefully

**Error Types**:

- [Error type 1] → [Handling]
- [Error type 2] → [Handling]

### 7.2. Loading States

**Components**: Skeleton loaders from shadcn/ui

**Usage**:

- [Loading state 1]: `Skeleton` [component]
- [Loading state 2]: `Skeleton` [component]

---

## 8. Accessibility

### 8.1. Keyboard Navigation

- [Navigation detail 1]
- [Navigation detail 2]

### 8.2. Screen Reader Support

- [Screen reader detail 1]
- [Screen reader detail 2]

### 8.3. Focus Management

- [Focus management detail 1]
- [Focus management detail 2]

---

## 9. Performance Considerations

### 9.1. [Performance Aspect 1]

- [Optimization detail 1]
- [Optimization detail 2]

### 9.2. [Performance Aspect 2]

- [Optimization detail 1]
- [Optimization detail 2]

---

## 10. Browser Compatibility

### 10.1. Supported Browsers

- Chrome (latest 2 versions)
- Firefox (latest 2 versions)
- Safari (latest 2 versions)
- Edge (latest 2 versions)

### 10.2. Feature Detection

- [Feature 1] for [purpose]
- [Feature 2] for [purpose]

---

## 11. Related Documents

- **Requirements**: `docs/v1/web/requirements/[feature]/[feature]_requirements.md`
- **API Design**: `docs/v1/server/design/[feature]/[feature]_design.md`
- **Design System**: `docs/v1/web/design/design-system.md`

---

**Last Updated**: 2025-01-XX
