# Mobile Interactions

## Touch Design

### Touch Targets
- Make targets comfortably tappable
- Important/frequent actions get larger targets
- Adequate spacing prevents mis-taps

### Thumb Zones
```
┌─────────────────────┐
│    Hard to reach    │  ← Stretch zone
├─────────────────────┤
│   Natural reach     │  ← Comfortable zone
├─────────────────────┤
│  Easy / Primary     │  ← Sweet spot
└─────────────────────┘
```
- Critical actions in bottom third
- Navigation in comfortable reach
- Destructive actions can be harder to reach

## Gesture Patterns

### Universal Gestures
| Gesture | Common Usage |
|---------|--------------|
| Tap | Select, activate |
| Long press | Context menu, drag mode |
| Swipe horizontal | Navigate, reveal actions |
| Swipe vertical | Scroll, refresh, dismiss |
| Pinch | Zoom |
| Double tap | Zoom, like |

### Platform-Specific
**iOS**:
- Edge swipe → Back
- Pull down → Refresh, dismiss
- Long press → Context menu

**Android**:
- Back gesture (edge swipe)
- Predictive back animation
- Pull down → Notifications

### Discoverability
- Gestures are invisible—provide hints
- Onboard non-obvious gestures
- Always provide tap alternatives

## Haptic Feedback

### When to Use
- Selection changes (toggles, pickers)
- Action confirmation
- Error feedback
- Gesture thresholds reached

### Best Practices
- Use sparingly—too much feels cheap
- Match intensity to importance
- Provide option to disable
- Test on real devices

## Animation

### Timing Principles
- Micro-interactions: Fast and snappy
- Screen transitions: Smooth but not slow
- Dismissals: Slightly faster than entries

### Motion Curves
- **Ease-out**: Fast start, slow end → Entries
- **Ease-in**: Slow start, fast end → Exits
- **Spring**: Natural, physical feel

### Motion Guidelines
- Responsive: Begin immediately
- Natural: Follow physics
- Intentional: Guide attention
- Consistent: Same actions = same animation

## Loading States

### Patterns
- **Skeleton screens**: Show structure while loading
- **Progress indicators**: Determinate or indeterminate
- **Pull to refresh**: Standard refresh gesture
- **Optimistic updates**: Update UI immediately, sync later

### Principles
- Always show progress for long operations
- Prefer skeleton over spinner for content
- Handle failures gracefully

## Keyboard

### Avoidance
- Content must remain visible with keyboard open
- Focused field should never be hidden
- Consider context above the field

### Input Types
- Match keyboard to input type
- Email, phone, URL get specialized keyboards
- Use appropriate autocomplete hints

### Dismissal
- Tap outside to dismiss
- Scroll to dismiss
- Explicit done/return actions
