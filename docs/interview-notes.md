# Interview Discussion Notes

## Flaky Test Questions

Q: Why is `page.url == expected_url` flaky?
A: It checks the current URL at one instant. Redirects, authentication callbacks, and dashboard loading can still be in progress. `expect(page).to_have_url(...)` waits until the condition is true or times out.

Q: Why avoid `locator.all()` for dynamic content?
A: It returns the current snapshot. If cards are still loading, the test may validate an incomplete list. Wait for a stable container or expected card before reading content.

Q: How do you handle 2FA in automation?
A: Prefer dedicated automation users with approved test bypass. If 2FA must remain enabled, retrieve OTP from a secure test-only channel, never from committed code.

## Framework Questions

Q: Why Page Object Model?
A: It centralizes selectors and page behavior, keeps tests readable, and reduces duplication when UI changes.

Q: Where should test data live?
A: Static templates can live in version control. Real credentials and environment-specific values must live in secret stores. Created data should be generated uniquely and cleaned up.

Q: How do you scale to many tenants?
A: Put tenant metadata in config, pass tenant IDs explicitly, use tenant-scoped credentials and API headers, and run tenant-isolation tests in parallel-safe data sets.

## API + UI Questions

Q: Why create data by API instead of UI?
A: API setup is faster, less flaky, and isolates the test objective. The UI step then validates rendering and user access, not every setup click.

Q: How do you validate tenant security?
A: Create data in Tenant A, verify visibility in Tenant A, then authenticate as Tenant B and confirm the data is unavailable through UI and ideally API.

Q: How do you reduce BrowserStack cost?
A: Run most tests locally in browser matrix, reserve real-device BrowserStack for smoke, release, and high-risk responsive paths, and keep setup API-driven.
