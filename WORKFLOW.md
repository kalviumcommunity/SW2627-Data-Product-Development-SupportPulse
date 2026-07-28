# Team GitHub Workflow

## Branch Strategy

- main contains stable code.
- Every new feature is developed in a feature branch.
- Feature branches follow:
  feature/<feature-name>

Example:
feature/customer-validation

Branches are deleted after merge.

---

## Commit Convention

We use Conventional Commits.

Examples:

feat: add validation script

fix: correct missing value calculation

docs: update project documentation

refactor: improve preprocessing logic

chore: update dependencies

---

## Pull Request Process

Every feature requires:

- Feature branch
- Pull Request
- One reviewer approval before merge

Review checks:

- Correctness
- Readability
- Data integrity
- Documentation

---

## Issue Tracking

Every task begins with a GitHub Issue.

Each issue includes:

- Title
- Description
- Label
- Assignee

Issues are closed automatically using

Closes #IssueNumber