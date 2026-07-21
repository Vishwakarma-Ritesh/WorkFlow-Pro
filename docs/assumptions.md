# Assumptions

- WorkFlow Pro has separate non-production tenants for Company1 and Company2.
- Tenant URLs and API URLs are provided through environment variables.
- Admin users can create and delete projects through the API.
- Test users are stable and managed outside the repository.
- 2FA is either disabled for automation users, bypassed through a secure test-only mechanism, or supplied through `WORKFLOWPRO_TEST_OTP`.
- API project creation is eventually consistent with the UI, so the framework includes bounded polling.
- Project cards expose stable selectors such as `data-testid` attributes in mature environments.
- BrowserStack credentials are stored as environment variables or CI secrets.
- Tests must never run against production unless explicitly approved with production-safe test data.
- Tenant isolation can be validated by checking that Company2 cannot see Company1-created project names.
