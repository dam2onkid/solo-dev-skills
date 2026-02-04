# Task-Master Workflow

Complete development lifecycle management from requirements to testing with changelog tracking.

## Development Phases

Four-phase structured approach:

1. **Requirements** (`1_requirements.md`)

   - Problem statement, goals, user stories
   - Success criteria, constraints
   - Open questions

2. **Design** (`2_design.md`)

   - Architecture overview with diagrams
   - Data models, API design
   - Component breakdown, decisions

3. **Implementation** (`3_implementation.md`)

   - Task breakdown with checkboxes
   - Milestones, dependencies, timeline
   - Code structure, patterns, security

4. **Testing** (`4_testing.md`)
   - Test coverage goals
   - Unit, integration, E2E tests
   - Performance, manual testing

## Workflow Steps

### 1. Initialize Feature

```bash
python .cursor/skills/task-master/scripts/init_feature.py <feature-name> [output-dir]
```

Creates structured docs with templates + CHANGELOG.md

### 2. Progress Through Phases

Fill each document in order:

- Complete requirements → design → implementation → testing
- Use checkboxes `- [ ]` for trackable tasks
- Update changelog when modifying documents

### 3. Track Implementation

List pending tasks:

```bash
python .cursor/skills/task-master/scripts/mark_task.py list docs/v1/feature/3_implementation.md
```

Mark tasks complete:

```bash
python .cursor/skills/task-master/scripts/mark_task.py mark docs/v1/feature/3_implementation.md "Task 1.1"
```

### 4. Document Changes

Add to document changelog:

```bash
python .cursor/skills/task-master/scripts/add_changelog.py doc docs/v1/feature/1_requirements.md Changed "Updated success criteria"
```

Add to feature CHANGELOG.md:

```bash
python .cursor/skills/task-master/scripts/add_changelog.py feature docs/v1/feature Added "OAuth2 provider"
```

## Changelog Entry Types

- **Added**: New features, requirements, components
- **Changed**: Modifications to existing items
- **Fixed**: Bug fixes, corrections
- **Removed**: Deleted functionality
- **Updated**: Refinements, improvements

## Best Practices

- Initialize features before starting work
- Keep each document under 200 lines; split if needed
- Mark tasks immediately after completion
- Log changes when updating requirements/design
- Reference changelog when reviewing progress
- Use CHANGELOG.md for high-level feature changes
- Use document changelogs for section-specific updates
