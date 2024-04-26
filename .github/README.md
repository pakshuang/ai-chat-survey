# GitHub Configuration

## Overview

This folder contains configuration files and workflows that are used for GitHub repository management. These ensure that the codebase maintains a high standard of quality and that all integration and deployment workflows are handled automatically.

## Contents

```shell
.github/                   # Github workflows and codeowners configuration files
│
├── CODEOWNERS             # Specifies the owners for code reviews
└── workflows/             # Contains GitHub Actions workflows
```

## Workflows

### Continuous Integration and Deployment

The workflows manage the automated testing and deployment of the application. This ensures that each commit or pull request goes through a rigorous set of tests before it can be merged into the main branch, and is automatically deployed to the production environment once it is merged.

The workflows currently include a linter and an integration test.
