# Interactive Survey Interface

Revolutionising traditional survey methods by integrating conversational AI capabilities into a web-based survey interface. This interface will not only collect responses but also interact dynamically with respondents, providing a more engaging and personalised experience.

## Repository Folder Structure

```shell
ai-chat-survey/
│
├── .github/                   # Github workflows and codeowners configuration files
│
├── backend-gpu/               # Backend-gpu specific files
│
├── backend/                   # Backend specific files
│
├── database/                  # Database specific files
│
├── docs/                      # Documentation files
│
├── frontend/                  # Frontend specific files
│
├── reverse-proxy/             # Reverse proxy specific files
│
├── scripts/                   # Scripts for integration tests, setup, etc.
│
├── compose.yaml               # Docker Compose file for the application
├── compose.ssl.yaml           # Docker Compose file for the application in production
├── compose.eval.yaml          # Docker Compose file for the LLM evaluation
├── compose.gpu.yaml           # Docker Compose file for the GPU version of the application for local LLMs
├── compose.tests.yaml         # Docker Compose file for the integration tests
│
│── sample.env                 # Sample environment variables
│
├── .gitignore                 # Specifies intentionally untracked files to ignore
│
└── README.md                  # This document
```
