# Backend-gpu

## Overview

This directory hosts the GPU-enabled version of the backend services for the app, tailored for using local Large Language Models.

## Contents

```shell
backend-gpu/               # Backend-gpu specific files
│
├── Dockerfile             # Docker configuration for GPU-enabled services
├── Pipfile                # Manages Python dependencies for GPU compatibility
├── Pipfile.lock            # Manages Python dependencies for GPU compatibility
├── logs/                  # Directory for runtime logs
└── models/                # LLMs optimized for GPU usage
```

## Setup and Installation

To use the GPU-enabled services, a compatible Docker environment with GPU support must be set up. Follow the installation steps similar to the regular backend, but ensure your system supports GPU acceleration.

Refer to the [`backend.md`](../docs/backend.md) file in the `docs` directory for more detailed instructions on setting up and running the GPU-enabled backend.
