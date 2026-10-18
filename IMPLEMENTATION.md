# SNAP Automations — production integration plan

The static MVP proves the **user-facing workflow and rule semantics**; it is not an unattended execution service.

## Minimal production version

- **UI:** Reuse the simple When → Do editor and template cards in SNAP's responsive web app, with role-based project context.
- **Auth & tenant isolation:** Authenticate every request, validate workspace/project scope, and authorize each action and resolved recipient on the server. Never trust client-supplied project IDs or device tokens.
- **Rule persistence:** `automation_rules` (tenant_id, scope, project_id, version, trigger, conditions, actions, enabled, creator, timestamps), schema-validated and versioned. PostgreSQL JSONB works for the initial production release.
- **Event ingestion:** Existing task/project/invoice transactions commit application changes and a transactional outbox event atomically. A worker consumes events and matches them against indexed active rules.
- **Scheduler:** Server worker calculates future fire time using IANA timezone and workspace calendar. Use a DB schedule table / durable queue; not browser timers. Define DST, weekend, holiday and missed-run policies.
- **Delayed rules:** Persist an execution item with `run_after`, idempotency key, original entity ID/version and recheck policy. Re-fetch the current entity when the delay expires.
- **Digests:** Store event references in a tenant-scoped digest bucket; flush by delivery window and recipient, not by individually sending 30 messages.
- **Action workers:** In-app (DB row), FCM Admin SDK, approved transactional email provider, WhatsApp Business Platform, SMS provider. Each has retry policy, provider message ID, rate limits, monitoring and credentials in a secrets manager.
- **Safety:** Stable event and run IDs, idempotency, maximum chain depth, loop suppression, per-rule cooldown, per-user notification preferences, privacy-aware templates and cost budgets.
- **Run history:** Distinguish matched, skipped, scheduled, provider-accepted, delivered if provable, failed and dead-letter states.
- **Natural language:** Use an LLM only to draft a schema-constrained rule; validate every field server-side and present proposed assumptions for explicit review. Avoid arbitrary code execution.

## Priorities

| Phase | Scope |
|---|---|
| Pilot | Task/project status, scheduled health report, delayed escalation, in-app + FCM/email, activity logs, idempotency |
| Production | Recurring digests, integration configuration, retries, monitoring, WhatsApp/SMS with consent and quotas |
| Later | Complex branching, cross-platform workflows, external webhooks, AI-authored report commentary |

## Recommended rollout

1. Conduct 5 usability sessions including a non-technical field supervisor or clinic coordinator. Check whether users spot workspace-wide scope and default recipients.
2. Validate 50+ natural language prompts with known intended automation rules. Flag time and recipient ambiguity.
3. Build backend event outbox + one worker using existing SNAP deployment infrastructure, not microservices.
4. Integrate email/FCM first, then WhatsApp/SMS after provider and consent validation.
5. Pilot one workspace, monitor duplicate rates, missed runs, failed deliveries, cost per active rule, and help requests.

## Security notice

Do not repurpose `localStorage` as a production rule store; use authenticated APIs. Do not expose SMTP, Firebase service-account, WhatsApp access tokens or SMS credentials in GitHub Pages JavaScript. For clinic-like projects, do not include patient-sensitive content in external push/SMS previews.
