# Test Strategy

## Test Pyramid

- API tests validate service contracts quickly and provide setup/cleanup.
- UI smoke tests validate critical user workflows across browsers.
- Integration tests validate API-to-UI consistency and tenant isolation.
- Mobile tests validate the high-value responsive experience on real devices.

## Stability Practices

- Use stable locators, preferably `data-testid` or accessible roles.
- Avoid fixed sleeps.
- Use Playwright `expect` for UI state.
- Use bounded retries only for accepted eventual consistency.
- Generate unique data for parallel execution.
- Clean up created data through API.
- Keep secrets out of code and logs.

## Risk-Based Coverage

Priority 1:
- Authentication
- Project creation
- Tenant isolation
- Role permission checks

Priority 2:
- Project search and filtering
- Dashboard loading
- Mobile project visibility

Priority 3:
- Visual layout checks
- Extended device matrix
- Third-party integration mocks

## Test Types

- Smoke
- Regression
- API
- UI
- Integration
- Mobile
- Security
- Tenant Isolation
