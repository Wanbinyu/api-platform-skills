---
description: Run breaking-change-review on the current API/OpenAPI/PR diff
---

Follow the skill `breaking-change-review` strictly.

1. Locate before/after (OpenAPI files, DTOs, or git diff of public handlers).
2. List every discrete delta in a table.
3. Classify each delta.
4. Require migration notes or waivers for breaks.
5. End with an explicit merge verdict: request-changes | approve | approve-with-version-bump | waiver-documented.

Use the skill output template. Check every exit criteria box.
