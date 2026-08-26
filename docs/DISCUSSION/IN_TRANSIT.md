Backend: genuinely small. orders.status is a plain varchar with no enum or check constraint, so no migration is needed. It's one constant plus one array entry in Order.php. Twelve files reference Order::STATUS_*, but they're specific comparisons, not exhaustive lists — nothing validates against Order::STATUSES.

Frontend: a handful of switch cases — kt-utils/src/orderStatusHelper.ts plus four components in kt-tabs (colour, label, progress step). Each falls through to a default, so omitting one degrades to a raw string rather than breaking.

But I'd push back on where it goes, because two things suggest it may already exist:

orders.delivery_status already exists — nullable, alongside driver_id, delivery_started_at, delivery_completed_at, plus a whole Delivery/ module. It is completely unused: all 31 rows are null. That column looks like exactly the intended home for a transit state.

Jumpseller already maps PICKED_UP → 'in_transit' (OrdersServiceMethods.php:306,333). So the concept exists today, expressed as PICKED_UP.

The design risk: orders already carries three status vocabularies (status, broker_status, tab_status) that demonstrably disagree — TabsNotificationService maps tab CLOSED to order CLOSED while TabController sets SHIPPED for the same transition. IN_TRANSIT is orthogonal to lifecycle (an order can be PREPARED and in transit), so putting it in status adds a fourth axis to a model that already can't keep three straight.

My recommendation: put it in delivery_status, which is already there, already scoped to delivery, and currently empty — no migration, no new value in a vocabulary other systems map. If it must be visible in the main funnel, the reports engine can pivot on delivery_status as its own dimension, which is a one-line Dimension::column.

Which way do you want it? I'll wire it either way — including the frontend switches and a delivery_status report dimension so it shows up in the widgets.

For the turn just completed: all six dashboard widgets are working and verified.

Backend suites green (800 core + 122 domain, 0 failures) after I qualified ResourceVisibility — it used bare tenant_id/tenancy_id, which goes ambiguous the moment you join orders⋈tabs or payments⋈point_of_sales. That was blocking three widgets.
Origin resolves as one flat list (20 kiosk / 5 staff on real data) via a CASE joined down to system_marketplaces, so Uber/JumpSeller name themselves.
Snapshot-on-close verified end to end — created a draft, closed it, read widget_data back (6 widgets), confirmed the API serves source: snapshot, then removed the test row.
Cash count visibility needed no change: kitchntabs-web already picks its manifest by active_tenant_id, and cashCountResource is only in the impersonated-tenant one. Reports are now in both.
Corrected the two F1 READMEs — hash_id/HasHashId//api/tabs don't exist (all 16 occurrences were the docs describing themselves), plus the float/decimal sum hazard, the lowercase 'approved', and the two missing order statuses.
sales and payment-methods return zeros because point_of_sales is empty in dev — the SQL runs, the figures are unverified against real payments.