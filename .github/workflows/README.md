# CI/CD Workflows

This directory holds GitHub Actions workflow definitions for continuous API testing and Newman automated execution.

---

## Workflow Execution per Workspace

Workflows in this directory can be configured to:
1. Spin up the SUT (EShop backend service and mock database).
2. Install Newman and necessary reporters (`newman-reporter-htmlextra`).
3. Execute the Postman collections for each student workspace (`23127259/`, `23127060/`, `23127195/`).
4. Upload generated HTML test reports as build artifacts.
5. Provide evidence for both **Passing Pipeline** and **Failing Pipeline** runs as required by the HW06 specification.
