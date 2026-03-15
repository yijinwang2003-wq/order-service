# Order Service

REST API service for order management.

---

## Git Workflow

This repository follows the Git Flow branching model:

- main: production-ready code
- develop: integration branch for development
- feature/*: feature branches from develop
- release/*: release preparation branches
- hotfix/*: urgent fixes from main

This structure ensures stable production releases while enabling continuous development.


## CI/CD Pipeline

The Jenkins pipeline includes the following stages:

1. Build & Lint
2. Test
3. Security Scan
4. Container Build
5. Container Push
6. Deploy to environments

Environment triggers:

PR → Build validation only  
Develop → Dev deployment  
Release branches → Staging deployment  
Main → Production deployment with approval