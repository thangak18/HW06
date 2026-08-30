# CI/CD Workflows

This directory holds GitHub Actions workflow definitions for continuous API testing and Newman automated execution.

---

## Workflow Structure Overview

Workflows in this directory can be configured to:
1. Spin up the SUT (EShop backend service and mock database).
2. Install Newman and necessary reporters (`newman-reporter-htmlextra`).
3. Execute the Postman collections for each member workspace.
4. Upload generated HTML test reports as build artifacts.
5. Provide evidence for both **Passing Pipeline** and **Failing Pipeline** submissions as required by the HW06 specification.
