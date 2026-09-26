# Accessibility and interaction verification

The black 8BALL workspace now explicitly focuses the destination heading on navigation. Dialogs receive their accessible name from the visible title and initially focus that title. Replacing a dialog preserves the original invoker so closing the second dialog does not drop the operator onto the document body. Tab and Shift+Tab remain inside the dialog, Escape closes it, and the application behind it remains inert. Errors are announced as alerts; ordinary confirmations remain polite status updates.

Visible focus styles remain clear against black/graphite surfaces. Forced-colour and reduced-motion preferences have explicit styles. None of these controls changes case evidence, a reviewed plan or an action's authority.

`tests/browser_accessibility.py` checks every navigation view for labelled controls, named buttons, unique IDs, a single main landmark and no positive tabindex. It exercises keyboard activation and focus movement, nested-dialog restoration, focus trapping, required empty fields, read-only behaviour, 320/390/768-pixel reflow and reduced motion. It preserves the earlier browser suites rather than replacing them with an accessibility score.

The first 36 checks passed in the explicit local ASGI bridge. Consolidated run reports state the exact transport. Native navigation is policy-blocked in the local environment. No human screen-reader evaluation, disabled-user study, macOS/Windows native startup review, full browser-family compatibility or WCAG conformance is claimed.

Official design references consulted: the WAI-ARIA Authoring Practices modal dialog pattern (`https://www.w3.org/WAI/ARIA/apg/patterns/dialog-modal/`) and Playwright accessibility-testing documentation (`https://playwright.dev/docs/accessibility-testing`). These are references for the interaction work, not certification of this application.
