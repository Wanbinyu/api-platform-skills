---
description: Write a consumer-facing API changelog from OpenAPI or review deltas
---

Follow the skill `api-changelog` strictly.

1. Gather before/after specs or breaking-change-review deltas.
2. Optionally run `python scripts/openapi_breaking_diff.py old.yaml new.yaml`.
3. Bucket breaks / semantic / additive / deprecations.
4. Write the full changelog template with migration steps.
5. End with Publish? yes/no and a 5-line blurb for Slack/email.
