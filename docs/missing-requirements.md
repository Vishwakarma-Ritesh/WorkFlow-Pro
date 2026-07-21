# Missing Requirements / Interview Questions

This document captures the questions I would ask the product, architecture, or QA team when the assessment scope is intentionally limited.

## Questions

1. How are tenants provisioned and isolated?
2. Can the API create and delete users/test data, or must we use existing accounts?
3. How is OTP generated and can automation bypass or consume it securely?
4. Should BrowserStack Local be used for staging/internal environments?
5. How are test users reset between runs?
6. Can tests execute in parallel, and what data isolation guarantees are required?
7. Should cleanup happen through API, DB hooks, or environment reset?
8. How many browsers and device types should be supported in CI?
9. How many mobile devices and OS versions should be part of the mobile matrix?
10. What are the reporting expectations for CI and stakeholder review?
11. Are there any third-party integrations that need to be mocked or validated?
12. What are the recovery expectations for flaky dashboard or eventual consistency cases?
