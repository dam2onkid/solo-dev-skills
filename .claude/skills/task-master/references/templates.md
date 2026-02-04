# Development Phase Templates

Reference guide for all phase templates used in feature development.

## Template Locations

All templates are in `templates/`:

- `requirements.md` - Problem statement, goals, user stories, success criteria
- `design.md` - Architecture, data models, API design, component breakdown
- `implementation.md` - Task breakdown, milestones, dependencies, code structure
- `testing.md` - Test coverage, unit/integration/E2E tests, performance testing
- `web-design.md` - Web UI/UX design (if applicable)
- `web-design-overview.md` - Web design system overview (if applicable)

## Key Template Sections

### Requirements Template

- **Problem Statement**: Core problem, affected users, current workarounds
- **Goals & Objectives**: Primary/secondary goals, non-goals
- **User Stories**: As [user], I want [action] so that [benefit]
- **Success Criteria**: Measurable outcomes, acceptance criteria
- **Constraints & Assumptions**: Technical/business/time limitations
- **Questions & Open Items**: Unresolved items requiring clarification

### Design Template

- **Architecture Overview**: Mermaid diagrams, component relationships, tech stack
- **Data Models**: Entities, relationships, schemas, data flow
- **API Design**: External/internal interfaces, request/response formats, auth
- **Component Breakdown**: Frontend/backend/database/integrations
- **Design Decisions**: Rationale, alternatives considered, patterns applied
- **Non-Functional Requirements**: Performance, scalability, security, reliability

### Implementation Template

- **Milestones**: Major checkpoints with checkboxes
- **Task Breakdown**: Phased tasks with `- [ ]` checkboxes
- **Dependencies**: Task order, external dependencies, blockers
- **Timeline & Estimates**: Effort per task/phase, target dates
- **Risks & Mitigation**: Technical/resource risks, strategies
- **Development Setup**: Prerequisites, environment, configuration
- **Code Structure**: Directory structure, module organization, naming
- **Patterns & Best Practices**: Design patterns, code style, utilities
- **Security Notes**: Auth/authorization, validation, encryption, secrets

### Testing Template

- **Test Coverage Goals**: Coverage targets, scope alignment
- **Unit Tests**: Component/module test cases with checkboxes
- **Integration Tests**: Component interaction scenarios
- **End-to-End Tests**: User flow validation
- **Test Data**: Fixtures, mocks, seed data
- **Performance Testing**: Load/stress testing scenarios
- **Bug Tracking**: Issue tracking process, severity levels

## Usage Guidelines

**Initialize features with templates**:

```bash
python .cursor/skills/task-master/scripts/init_feature.py <feature-name>
```

**Customize templates** for specific project needs by editing `docs/templates/*`

**Reference templates** when Claude needs guidance on documentation structure
