---
name: task-master
description: System-wide development brain managing complete lifecycle with context-first approach. Use when starting features (checks PRD/architecture), tracking tasks, documenting changes, or preventing AI slop (hallucinated features, over-engineering). Enforces user stories, trade-off analysis, constraint validation. Creates architecture overviews, PRDs, structured feature docs with changelog tracking.
---

# Task-Master Skill

**The Brain of the Development System**: Enforces context-first, anti-AI-slop development. All features must be documented, planned, grounded in project reality with user stories and trade-offs.

## Purpose

Acts as central nervous system for development:

- **Context Management**: Maintain architecture, PRD, constraints, user stories
- **Feature Planning**: Initialize structured docs grounded in project context
- **Reality Enforcement**: Prevent hallucinated features and over-engineering
- **Progress Tracking**: Mark tasks, maintain changelogs
- **Quality Gates**: Ensure all work has user story, follows patterns, respects constraints

## When to Use

**Always use task-master when**:

- Starting ANY new feature (mandatory context check)
- Proposing architectural changes (verify against ARCHITECTURE.md)
- Unsure if feature in scope (check PRD.md)
- Tracking implementation progress
- Documenting requirement/design changes
- Creating project overview documentation

**Use immediately to prevent**:

- Suggesting features not in PRD
- Ignoring existing architecture patterns
- Over-engineering simple problems
- Hallucinating non-existent APIs/libraries

## Usage

### Step 0: Initialize Project Context (First Time)

Create essential context files if they don't exist:

```bash
# Architecture overview
python .cursor/skills/task-master/scripts/init_context.py architecture docs

# Product requirements
python .cursor/skills/task-master/scripts/init_context.py prd docs

# User stories
python .cursor/skills/task-master/scripts/init_context.py user-stories docs

# Technical constraints
python .cursor/skills/task-master/scripts/init_context.py constraints docs

# List available types
python .cursor/skills/task-master/scripts/init_context.py list
```

**Fill these templates immediately** - they prevent AI slop and hallucinations.

### Step 1: Context Check (Before Every Feature)

**MANDATORY**: Read relevant context before proposing features:

```bash
# Verify context exists
ls docs/ARCHITECTURE.md docs/PRD.md docs/USER_STORIES.md docs/CONSTRAINTS.md
```

Read:

- `docs/ARCHITECTURE.md` - System structure, tech stack, patterns
- `docs/PRD.md` - Feature scope, explicit non-goals
- `docs/USER_STORIES.md` - Real user needs
- `docs/CONSTRAINTS.md` - Technical limitations

### Step 2: Initialize New Feature

Create complete documentation structure:

```bash
python .cursor/skills/task-master/scripts/init_feature.py <feature-name> [output-dir]
```

**Naming convention**: Reference user story - `us-042-scan-history` not `history-feature`

Generates:

- `1_requirements.md` - Must reference user story, include trade-offs, explicit non-goals
- `2_design.md` - Must follow ARCHITECTURE.md patterns, justify decisions
- `3_implementation.md` - Task breakdown with checkboxes, reference existing code
- `4_testing.md` - Tests map to acceptance criteria
- `CHANGELOG.md` - Feature-level change tracking

Default output: `docs/v1/<feature-name>/`

### Step 3: Track Implementation Tasks

List incomplete tasks:

```bash
python .cursor/skills/task-master/scripts/mark_task.py list <file-path>
```

Mark task(s) complete:

```bash
python .cursor/skills/task-master/scripts/mark_task.py mark <file-path> [task-pattern]
```

Mark all tasks in file:

```bash
python .cursor/skills/task-master/scripts/mark_task.py mark <file-path> --all
```

Tasks use markdown checkbox format: `- [ ]` becomes `- [x]`

### Step 4: Document Changes

Add changelog to individual document:

```bash
python .cursor/skills/task-master/scripts/add_changelog.py doc <file-path> <type> <description>
```

Add to feature-level CHANGELOG.md:

```bash
python .cursor/skills/task-master/scripts/add_changelog.py feature <feature-dir> <type> <description>
```

Changelog types: `Added`, `Changed`, `Fixed`, `Removed`, `Updated`

## Anti-AI-Slop Protocol

**AI Slop**: Generic, hallucinated, over-engineered suggestions disconnected from project.

**Mandatory checks before proposing features**:

- [ ] Read `docs/ARCHITECTURE.md` - understand existing system
- [ ] Read `docs/PRD.md` - feature in scope?
- [ ] Read `docs/USER_STORIES.md` - which user need addressed?
- [ ] Read `docs/CONSTRAINTS.md` - respects limits?
- [ ] Review similar code - follow patterns?
- [ ] Identify trade-offs - what gained/lost?
- [ ] Simplest solution - no over-engineering?

**Red flags** (reject immediately):

- Features not in PRD without strong justification
- Ignoring existing architecture patterns
- Microservices for simple CRUD
- Generic "dashboards" without user story
- Hallucinated APIs/libraries
- Boilerplate without project context

## Workflow

1. **Context Setup** (first time): Run `init_context.py` to create ARCHITECTURE.md, PRD.md, etc.
2. **Context Check** (every feature): Read relevant docs before proposing
3. **Initialize**: Run `init_feature.py` with user-story-based name
4. **Requirements**: Link to user story, include non-goals, analyze trade-offs
5. **Design**: Follow existing patterns, justify decisions, document alternatives
6. **Implementation**: Concrete tasks with checkboxes, reference existing code
7. **Testing**: Map tests to acceptance criteria
8. **Track Changes**: Log all requirement/design updates

## Phase Document Requirements

**1_requirements.md must include**:

- User story reference: "Implements US-042 from USER_STORIES.md"
- Explicit non-goals: "NOT building: feature X (out of scope per PRD)"
- Trade-off analysis: "Choose X over Y: gains Z, loses W"
- Constraint validation: "Per CONSTRAINTS.md, supports Android 8.0+"

**2_design.md must include**:

- Architecture alignment: "Uses MVVM per ARCHITECTURE.md"
- Decision rationale: "Choose eager loading: US-042 prioritizes speed"
- Alternatives considered: "Rejected pagination: avg user has <100 items"
- Mermaid diagrams showing component interactions

**3_implementation.md must include**:

- Concrete tasks (not generic): `- [ ] Create ScanHistoryScreen with RecyclerView`
- Existing code references: "Extend ScanRepository (app/src/.../data/)"
- Pattern adherence: "Follow repository pattern per architecture"

**4_testing.md must include**:

- Acceptance criteria mapping: Each test → user story criterion
- Coverage per project standards from CONSTRAINTS.md

## Context Files

**docs/ARCHITECTURE.md**: System structure, tech stack, core components, patterns, constraints

**docs/PRD.md**: Product vision, in-scope features, explicit out-of-scope, success metrics

**docs/USER_STORIES.md**: As [user], I want [action] so that [benefit] + acceptance criteria

**docs/CONSTRAINTS.md**: Platform, performance, security, compliance requirements

All templates in `docs/templates/`: requirements.md, design.md, implementation.md, testing.md

## Best Practices

**Quality Gates**:

- No feature without user story
- No architecture change without rationale
- No generic solutions - must be project-specific
- No hallucinations - verify APIs/libraries exist

**Documentation**:

- Keep documents <200 lines; split if needed
- Mark tasks immediately after completion
- Reference context files explicitly
- Include trade-offs in every decision

**Good vs Bad Examples**:

❌ Bad: "Add user dashboard with analytics"

- No user story reference
- Generic feature
- Unclear if in PRD scope

✅ Good: "Implement US-042 scan history list. Per ARCHITECTURE.md, extend ScanRepository with Room query. Trade-off: basic UI now vs filters later (user data will inform need per PRD metrics)"

- Cites user story
- References architecture
- Shows trade-off thinking

## References

- `references/workflow.md` - Detailed workflow with examples
- `references/templates.md` - Template structure guide
- `references/architecture-overview.md` - Architecture doc template
- `references/project-context.md` - Context files guide

Read workflow.md for comprehensive examples and anti-slop strategies.
