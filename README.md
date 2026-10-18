# SNAP Automations MVP — GitHub Pages ready

A complete, interactive **client-side MVP** of SNAP Automation Lite, following the approved design: **Describe → Review (When → Do) → Try → Turn On**.

## Deploy to your own `snap-automation` GitHub repository

This package is already structured for GitHub Pages and does not need Node.js, npm, a database or build tooling **to run the front-end demo**.

1. Open your GitHub repository `rishikarot/snap-automation`.
2. Upload **`index.html`, `styles.css`, `engine.mjs`, `app.js`** into the root of the repository. Optionally include `README.md` and `tests/`.
3. Commit to the `main` branch.
4. In **Settings → Pages**, select **Deploy from a branch**, `main`, `/(root)`, and save.
5. After the Pages deployment has finished, visit: `https://rishikarot.github.io/snap-automation/`.

Do not upload only the modular `index.html`: the JS and CSS modules must be alongside it. GitHub Pages serves `.mjs` files correctly. **One-file alternative:** rename `snap-automations-standalone.html` to `index.html` and upload that file alone. It bundles the same engine and styles; the appearance uses system fonts when loaded without internet.

For local testing, you can run `python3 -m http.server 8765` in this folder and visit `http://localhost:8765`. Double-clicking `index.html` without HTTP may block ES module imports in some browsers.

## What really works in this MVP

- Fully responsive interface for desktop, tablet, and phone
- Workspace and Project scope, equally visible
- Natural-language proposal creation for documented scenarios (deterministic JavaScript, **not a live AI connection**)
- Safe default suggestions and explicit clarification of ambiguous AM/PM requests
- Inline When → Do editor for events, schedules, delivery modes, conditions, channels and up to five chained actions
- Create, edit, activate, pause, duplicate, delete, export and import automation rules
- Sample project/task board where changing task/project status generates **real local events** processed by the rule engine
- Real local actions: create follow-up task, change task status, add comment, create in-app notification
- Scheduled rule evaluation while the page is open; manual “Run scheduled reports now” control
- Delayed action queue and **recheck before delivery**
- Digest aggregation and flush, including manual digest delivery
- Chain depth limit and event lineage protection
- Dry-run test popup with editable examples, matching/skipping reasons and exact payload preview
- Local activity history, in-app notifications and JSON export/import
- State preserved with browser `localStorage` (per-browser/per-device, not shared)

## Important limits

This is a **functioning static MVP, not a production automation service**. Because GitHub Pages is static hosting:

- **Email, FCM, WhatsApp and SMS are never sent**: outbound messages are logged as explicit safe previews. No secrets are embedded in the site.
- Schedules and delayed actions run **only while the browser tab is open** and the client-side app is active. The demo clock is not real wall clock time.
- The sample projects, recipients and tasks are local fixtures. Changes are not synchronized with SNAP's backend or with other devices.
- The natural-language interpreter is a **limited rule-based demo**. For production, use a typed proposal schema, server-side validation and a reviewed AI interpreter.
- Local rules are not authenticated and `localStorage` is not appropriate for sensitive patient data or real client records.
- This POC does **not** actually use FCM tokens or any external messaging service.

For actual always-on delivery, implement an authenticated backend worker, persistent queues, idempotency, retry/dead-letter processing, provider credentials and authorization. See `IMPLEMENTATION.md`.

## Test it

- Click **Task becomes blocked** recipe. Verify `When → Do`, open **Try with sample data**, and activate.
- Open **Playground** and change `Finish API integration` to `Blocked`; check **Activity** and **in-app notifications**.
- Try **Escalate blocked tasks** in the Garage360 project. Change a task to Blocked, advance the clock two hours, and see the delayed alert. Then test changing it to Completed before advancing; the recheck will skip it.
- Pick **Daily project health** and click **Run scheduled reports now** to generate a report preview.
- Pick **Evening updates digest**, change multiple statuses, then click **Send collected digests**.
- Pick **QA sign-off follow-up**, change a task to `QA Approved`, and verify a follow-up task is created with a chained notification.
- In **Automations**, try export, import, pause, resume, duplicate and delete.

Run engine unit tests (optional, requires Node.js 20+):

```bash
node --test tests/engine.test.mjs
```

## Data & privacy

No account credentials are needed. The demo stores rule configurations, sample tasks and activity in the current browser only. Avoid entering private customer/patient data in this public prototype. The fonts load from Google Fonts when internet is available; system fallback fonts render offline.
