---
phase: design
title: [Feature Name] - Web Design
description: Design for [feature description] on web
---

# [Feature Name] - Web Design

**Version**: 1.0  
**Updated**: 2025-01-XX  
**Tech Stack**: Next.js 16, React 19, Tailwind CSS, shadcn/ui

This document describes the detailed design for [feature description] on web.

**Reference**:

- Overview: `[overview_design.md]` (if applicable)
- Design System: `../design-system.md`
- Requirements: `../../requirements/[feature]/[feature]_requirements.md`
- API Design: `../../../server/design/[feature]/[feature]_design.md`

---

## 1. Layout Structure

**Base**: [Brief description of page/component layout]

**File Structure**:

```
apps/web/src/
├── app/
│   └── [route]/
│       └── page.tsx
└── components/
    └── [feature]/
        ├── [component-name].tsx
        └── ...
```

---

## 2. [Page/Component Name] (`/[route]`)

### 2.1. Component Hierarchy

**Page Component**: `app/[route]/page.tsx`

- **Layout**: [Layout type - Dashboard layout, Public layout, etc.]
- **Container**: [Container description]
- **Components**:
  1. `[Component1]` component
  2. `[Component2]` component
  3. ...

### 2.2. Visual Design

```
┌─────────────────────────────────────────────────────────────┐
│  [Visual ASCII representation of the page/component]        │
└─────────────────────────────────────────────────────────────┘
```

---

## 3. [Component/Feature Section]

### 3.1. [Sub-section]

[Description]

### 3.2. [Sub-section]

[Description]

---

## 4. State Management

### 4.1. [State Type]

**Store**: [Where state is stored - URL params, React Query, Local state, etc.]

**State**:

```typescript
interface [StateName] {
  // State properties
}
```

---

## 5. API Integration

### 5.1. API Calls

**Hook**: `hooks/use-[feature].ts`

```typescript
export function use[Feature]() {
  return useQuery({
    queryKey: ['[feature]'],
    queryFn: () => [apiFunction](),
  });
}
```

### 5.2. Data Transformation

[How API response is transformed for component use]

---

## 6. Responsive Design

### 6.1. Mobile (< 768px)

[Mobile-specific design considerations]

### 6.2. Tablet (768px - 1023px)

[Tablet-specific design considerations]

### 6.3. Desktop (≥ 1024px)

[Desktop-specific design considerations]

---

## 7. Accessibility

### 7.1. Keyboard Navigation

[Keyboard navigation details]

### 7.2. Screen Reader Support

[Screen reader support details]

### 7.3. Focus Management

[Focus management details]

---

## 8. Error Handling

### 8.1. Error Types

[Error types and how they're handled]

### 8.2. Error Display

[How errors are displayed to users]

---

## 9. Loading States

### 9.1. Initial Load

[Initial loading state]

### 9.2. [Other Loading States]

[Other loading states]

---

## 10. Performance Considerations

### 10.1. [Performance Aspect 1]

[Performance optimization details]

### 10.2. [Performance Aspect 2]

[Performance optimization details]

---

## 11. Related Documents

- **Overview**: `[overview_design.md]` (if applicable)
- **API Design**: `../../../server/design/[feature]/[feature]_design.md`
- **Requirements**: `../../requirements/[feature]/[feature]_requirements.md`

---

**Last Updated**: 2025-01-XX
