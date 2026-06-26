Introduction to Uber Eats Marketplace APIs

The Uber Eats Marketplace APIs enable partners to programmatically manage stores, menus and orders on the Uber Eats platform.

Overview
The Integration Activation API can be used to associate your application to a merchant’s location within Uber. Using the merchant’s authorization, you can retrieve their store-list, and allow them to select the locations to configure and activate.

Use the Store API to onboard; manage; or enumerate merchant store information and temporal store status (pausing; unpausing; and holiday hour overrides). These APIs can also be used to manage app access and integration details on a store level.

The Menu API provides the ability to manage menus as well as regular store hours.

Ingest and manage incoming orders from Uber Eats with the Order API. The API includes webhooks for incoming order notifications and cancellations from Uber Eats. Retrieve, accept, deny, and cancel orders with the Order API endpoints.

Use the Reporting API to request and access standardized reporting. The API includes a notification webhook once a report is completed.

Integration Configuration API Suite
API Endpoints
GET Stores
Retrieve the locations for a given user authorized to your application.
POST Activate Integration
Associate application to a merchant’s location.
GET Integration Data
Retrieve specific integration information for a location.
PATCH Update Integration Data
Update integration configuration for a location.
DELETE Remove Integration
Remove your application association from a store.

Webhook Notifications
store.provisioned Webhook
Inform application a location has been provisioned to your application.
store.deprovisioned Webhook
Inform application a location has been de-provisioned from your application.
Menu API Suite
API Endpoints
GET Menu
Retrieve existing store menu.
PUT Menu
Create, update, delete menu and menu items.
POST Update Item
Update item availability and pricing.
Store API Suite
API Endpoints
GET Store Details
Retrieve store information.
GET List All Stores
Retrieve all stores provisioned to developer.
GET/POST Restaurant Status
Retrieve store availability status and set stores on/offline.
GET POS Status
Check if stores are order-integrated.
POST POS Data
Activate store integration.
DELETE POS Data
Remove store integration.
PATCH Update POS Status
Disable or enable order integration.
GET/POST Holiday Hours
Retrieve and set date-specific store hours.
Order API Suite
Order Fulfillment API Endpoints
GET Orders
Retrieve orders.
GET Order Details
Retrieve order details.
POST Order Acceptance
Accept order.
POST Order Denial
Deny order.
POST Cancel Order
Cancel accepted orders.
POST Resolve Fulfillment Issues
Resolve fulfillment issues due to cart issues
Mark Order Ready
Inform Uber an order is ready to assist in modeling dispatch of delivery partners.
POST Adjust Order Price
Adjust the order price based on customer contacting restaurant.
POST Update Ready Time
Update the expected time for an order to be ready for pickup.

Order Delivery API Endpoints
POST Delivery Partner Feedback
Submit delivery partner feedback.
Update Delivery Partner Count
Request multiple delivery partners.
POST Location
Ingest real-time courier location data for BYOC (Bring-Your-Own-Courier) partners.

Webhook Notifications
orders.notification Webhook
Notification event when an order is placed at a location where your application is enabled.
orders.scheduled.notification Webhook
Notification event when a scheduled order is placed at a location where your application is enabled.
orders.failed Webhook
Notification event for failed orders.
order.fulfillment_issues.resolved Webhook
Notification event when fulfillment issues are resolved by the customer on Uber’s end.
delivery.state_changed Webhook
Notification event when the delivery state of an order changes.
Reporting API Suite
API Endpoints
POST Report
Request reporting.

Webhook Notifications
eats.report.success Webhook
Notification event for completed report job.


Authentication
POST
https://auth.uber.com/oauth/v2/token

Reference
Key	Value
url	https://auth.uber.com/oauth/v2/token
scope	Space delimited list of scope(s) that you would like to generate a token for.
grant_type	Based on scope(s). Either client_credentials for an application generated token (to access Store, Menu, Order and Reporting endpoints) or authorization_code for a user access token (to access POS Provision endpoints).
Scopes
The following scopes are available for use with the Uber Eats Marketplace APIs. To gain access to scopes in production, your app must first be approved and whitelisted by the Uber Eats team.

Each Eats endpoint requires one of the scopes listed below and the token generated for the scope(s) must be used correspondingly. Note the grant type associated to each scope. Multiple scopes can be authorized using the same access token, provided that the grant type is the same.

Scope	Grant Type	Description
eats.store	client-credentials	Indicates a token has permission to update and retrieve store and menu information.
eats.store.status.write	client-credentials	Indicates a token has permission to set store availability (pause/unpause stores without changing menu hours).
eats.order	client-credentials	Indicates a token has permission to accept/deny/cancel orders and read v1 orders.
eats.store.orders.read	client-credentials	Indicates a token has permission to read v2 orders.
eats.report	client-credentials	Indicates a token has permission to generate reports (e.g. transaction reports) for stores.
eats.pos_provisioning	authorization-code	Indicates a token has permission to setup/remove pos integration and retrieve stores.
Generating a Client Credentials Token
To generate a client credentials token, retrieve your client_id and client_secret for your app from the Developer Dashboard and see the example below. Note this endpoint expects requests to be encoded as application/x-www-form-urlencoded or multipart/form-data.

Note: Client credentials grant type requests will be rate limited to 100 requests per hour. After generating 100 tokens with the client credentials grant type, creating a new token will invalidate the oldest token.

Example Request
curl -F "client_secret=$CLIENT_SECRET" \
    -F "client_id=$CLIENT_ID" \
    -F "grant_type=client_credentials" \
    -F "scope=eats.store" \
    https://auth.uber.com/oauth/v2/token
Example Response
{
  "last_authenticated": 0,
  "access_token": "KA.ewogICJ2ZXJzaW9uIjogMiwKICAiaWQiOiAiZmFuY3kgc2VlaW5nIHlvdSBoZXJlLCBodHRwOi8vdC51YmVyLmNvbS9kZXYtcGxhdGZvcm0tam9icyIsCiAgImV4cGlyZXNfYXQiOiAxNDk3NzQxNjIyLAogICJwaXBlbGluZV9rZXlfaWQiOiAiZm9vYmFyIiwKICAicGlwZWxpbmVfaWQiOiAxCn0K.9jPtNyS9vHJ9HVmxA4Y6vwIcwv7v1tx1BMYwztpIeID",
  "expires_in": 2592000,
  "token_type": "Bearer",
  "scope": "eats.store",
  "refresh_token": ""
}
Usage
The access_token field will contain the token used to authenticate against the Uber Eats APIs. Once you’ve obtained this token, you can provide it in the “Authorization” header of requests you make to endpoints that require client credentials scopes.

The expires_in field indicates the lifetime of the access token, provided in seconds. Tokens are valid for 30 days (2,592,000 seconds) and should be cached and re-used across requests until (or shortly before) expiration, not re-generated per request.

curl \
  -H 'authorization: Bearer <TOKEN>' \
  https://api.uber.com/v1/eats/stores


  Webhook

  The Uber Eats Marketplace APIs includes a variety of webhooks for incoming orders, store notifications, and order cancellations. In order for your service to receive webhooks from Uber, set your webhook URL in the developer dashboard Setup section, under **Webhooks > Primary Webhook URL. All of the webhooks notifications from Uber’s platform will be sent to your unique primary webhook URL configured within the developer dashboard.

Uber Eats Marketplace Webhook Notifications
The Order API sends notifications to your app’s configured webhook. Each notification has a corresponding event_type:

event_type	Description
orders.notification	Sent whenever an order is created.
orders.failure	Sent when an order is cancelled.
(Only applies to stores configured on API version 1.0.0.)
orders.release	(If fast order release is enabled) Sent when an order is configured for Fast Order Release and courier has reach geo-fence.
orders.scheduled.notification	Sent whenever a scheduled order is created.
(Only applies to stores configured on API version 1.0.0 and where scheduled orders are enabled.)
orders.cancel	Sent when an order is cancelled.
(Only applies to stores NOT configured on API version 1.0.0.)
store.provisioned	Sent whenever a store has granted access to your application/client ID.
store.deprovisioned	Sent whenever a store has been removed access from your application/client ID.
order.fulfillment_issues.resolved	Sent whenever a customer has confirmed change on Resolve Order Fulfillment endpoint.
store.status.changed	Notification when a store’s online status has changed. Requests the scope eats.store.status.notification be whitelisted for your client ID.
Order JSON body parameters
The table below describes each parameter in the order webhook notification. Review the Additional sections below for alternative webhooks:

Once a webhook is received, you can pull the full order information using the resource_href, which corresponds to the Get Order Endpoint endpoints. The resource_id corresponds to the order_id used in the Order API. Your resource_href can be adjusted to your API version using the PATCH /pos_data.

Example Order Notification
Order webhooks are listed within API reference Order API Suite.

Webhook Security
All webhooks sent from Uber contain a signature in the header of the request so that your app can verify that the sender is Uber.

Webhooks requests contain an X-Uber-Signature header. The value of this field is a lowercased hexadecimal HMAC signature of the webhook HTTP request body, using the client secret as a key and SHA256 as the hash function.

Python Example

digester = hmac.new(client_secret, webhook_body, hashlib.sha256)
return digester.hexdigest()
Expected response
Your service should POST a 200 response status code with an empty response body to acknowledge receipt of the webhook event. If no acknowledgement is received, Uber will continue to retry the webhook according to the retry logic described below.

After acknowledging receipt of the webhook, you must explicitly POST /accept_pos_order or /deny_pos_order within 11.5 minutes. Otherwise the order will time out and auto-cancel. Order acceptances should be posted as quickly as possible to minimize Eater cancellations. Note: If your store is set up to receive robocalls for unaccepted orders, a robocall will be triggered if no Accept/Deny is posted after 90 seconds.

Retry logic
If Uber receives either of 500, 502, 503, 504 status codes, timeout or any network error, the webhook event will be retried. The first retry will be sent 10 seconds after the initial event. The following events will be resent based on an exponential backoff algorithm, starting at 30 seconds after the 10s retry, then again after 60 seconds, then after 120 seconds, and so on until a response is received or until 7 total events were sent without a response.

Set up your webhook URL
To test the webhook, set a valid webhook URL and place an order in your test store. Your service (a single webhook URL) can receive webhooks for multiple stores, as long as the developer account’s UUID is mapped to each individual store (org). When your service receives events, you’ll need to use the user_id (which corresponds to store_id) from the webhook to map it to the right store for notifications and order injections.

In the developer dashboard Select Setup, under *Webhooks, enter your primary webhook URL, and click SAVE. At this time, Uber Eats Marketplace does not support multiple webhook URLs to be configured.
For testing purposes, you may want to setup your own webserver or use a third-party hosting provider to receive webhooks.


Integration Configuration Flows

Overview
Uber Eats provides merchants with multiple mechanisms for activating and configuring their live production stores against a given app integration.

During onboarding, Uber may pre-integrate a store with integrator mapping details.
Once live, the merchant should contact Uber technical support teams through our Tech Support Form
Through an integration partner’s own website, by merchant’s authorizing you app with OAuth login flow, allowing you to call the GET /stores and POST /pos_data endpoints. See details below.
In each case, apps will be be notified of any initial and subsequent changes to their store integration status via the store.provisioned webhook. To provide a cohesive merchant experience, you should listen and respond to these webhooks. This is especially important if your app is responsible for core order workflow management (accepting; rejecting; or cancelling orders) as you may be requested to do follow-up actions (e.g. upload a menu).

If the integration details are wrong, or your integration is unable to operate the store, you should modify or deactivate the integration via PATCH /pos_data. Should your app ever be deactivated from a store, you will receive a store.deprovisioned webhook.

Once an app is activated against a given store, its client_credentials access token(s) will be able to call most APIs; and it will start to receive webhook notifications related to the store.

Using GET /pos_data; PATCH /pos_data; and POST /pos_data endpoints, integration partners can read and write their ID and configuration data against each store to facilitate mappings and debugging. For convenience, a subset of this integrator store data is also available when fetching or enumerating store details via the GET /stores endpoints.

Triggering Activation From 3rd Party Workflow
Authorization
Developers can redirect users to Uber’s OAuth login flow, temporarily authorizing your app to access their stores.
Retrieve Stores
Upon authorization, developer can retrieve all stores associated to the authorizing merchant via GET /stores. This call returns Uber’s unique identifier and store location data. Developer must map Uber’s unique ID to correct stores using the location data. External store ID can be arbitrary and should not be used as a sole matchpoint.
Activation
Developers can activate their app against a store the POST /pos_data endpoint using the merchant user’s access token. This grants your app with perpetual access to the store.
Deactivating
Developers can temporarily de-activate their app by setting integration_enabled to false with the PATCH /pos_data; or more permanently revoke integration by calling the DELETE /pos_data endpoints.

Store integration

Overview
The Store API provides developers with the ability to manage stores and retrieve store information. Use the store endpoints to enable/disable POS integration and set date-specific store override hours.

Components
Retrieve Store Data
Developers can retrieve store information such as store address and name on an individual location basis via GET /store/{store_id}.
Retrieve Stores
To see all stores provisioned to your developer account, use the GET /stores endpoint.
Set & Retrieve Restaurant Status
Developers can set stores as online or offline (‘paused’) via the POST /status endpoint. When set to online, stores will be searchable and available to customers on the Uber Eats platform during store hours. When set to offline, stores will show as “currently unavailable”.
Set & Retrieve Date-Specific Hours
Set and retrieve holiday hours via the POST /holiday_hours and GET /holiday_hours endpoints.
Syncing Store Availability
Support of the POST /status endpoint is strongly recommended. To ensure a great Eater experience, stores should be set offline using this endpoint when they are unable to fulfill orders during store hours (e.g. while experiencing connectivity issues or undergoing maintenance).

Setting Holiday Hours
Regular store hours are determined by menu hours set through the Menu API. However, date-specific exceptions to the normal operating hours of a restaurant should be set through the Holiday Hours endpoint. Holiday hours override store hours on the specified date(s) and can be set far in advance.

Testing with Uber Eats Orders
In an incognito Chrome browser, navigate to Uber Eats Orders. Log in as a store using your test store credentials.

Call the POST /status endpoint to pause the store (set it offline). Refresh the Uber Eats Orders page. You should see the display message change to “New orders paused”. Now click on the top button with the three lines (“Menu” on hover) in the left-hand navigation bar. Click “Resume new orders” on the bottom of the sidebar and click “Confirm” in the following prompt. Now use GET /status to retrieve the store’s status. The status should now read as “ONLINE”.

You can also use Uber Eats Orders to test holiday hours. Set holiday hours via the POST /holiday_hours endpoint. Refresh your Uber Eats Orders window. Click again on “Menu” in the left-hand navigation bar. In the Menu sidebar, click “Hours” and then “Holiday Hours”. You should see your newly-set holiday hours reflected.



Menu Integration


Overview
Brunch
9:00 AM - 1:00 PM
Breakfast
Mon 8:00 AM – 10:30 AM
Lunch
Mon 10:30 AM – 3:00 PM
 Egg Dishes         Soft Drinks         Alcoholic Drinks    
Egg Dishes
Scrambled Eggs
Made with the freshest organic eggs.
$7.99
Eggs Benedict
Made with the juciest canadian bacon.
$7.99
Soft Drinks
Orange Juice
Made with the freshest organic oranges.
$2.99
Drip Coffee
The best American coffee. Served hot.
$1.99
menu
category
category
item
item
item
item
Create, update and retrieve menus using the Menu API endpoints. Every store location on the Uber Eats marketplace has its own individually-configurable menu and store hours. It’s constructed from four main entity types:

Item
Represents everything that a user might tangibly select from a marketplace (e.g. an appetizer; a can of soda; a dessert; a pizza topping; a condiment).
Modifier Group
Groups items together to be selected as a customization under a parent item (e.g. “Pizza Toppings” modifier group might have “Mushroom” and “Peppers” items as options within it). Different modifier groups can optionally leverage the same items.
Category
Groups one or more top-level item(s) together into a logical menu section (e.g. “Appetizers”; “Main Courses”; “Soft Drinks”).
Menu
Groups one or more categor(ies) together into a single view with corresponding menu hours (e.g. “Brunch Menu”, “Late Night Menu”). A store can have individual menus for different fulfillment types (delivery, pick-up), or the same menu can be utilized by all.
Store hours are calculated as the union of service_availability across all menus. For example, a store that has both a breakfast menu from 9am to 1pm and lunch menu from 12pm to 3pm, will have store hours of 9am to 3pm.

Components
Retrieve Menu
Retrieve a store’s menu via the GET /menus endpoint.
Upload Menu
Push new menus to a store using PUT /menus. A call to this endpoint overwrites any existing menus.
Update Item
Developers can make updates to individual items on a store menu via the POST /menus/items endpoint. Use this to endpoint to mark items as out-of-stock/back-in-stock or to update item pricing. Note that this endpoint can only be used when the original menu was uploaded via the API, even if an item ID was configured elsewhere and provided here.
Constructing Menus
Use your Uber Eats test store to create and update your menu details via the Menu API in your test environment. You can use the Uber Eats Postman Collection (provided in the Resources section) to help you with testing. If you need additional test stores created and whitelisted for your account, please submit a technical support request and our team members will assist you.

Menu Setup
To help with your menu setup, sample menu payloads are provided within the Menu API reference section. We can also copy the menus of your Merchants’ live stores that are on Uber Eats currently to your test stores. Please submit a tech support request with the name and address of the store that you would like to copy the menu from.

Testing the API
To make a request to any of the Eats Menu API endpoints, you will need to authenticate using an app access-token generated with at least the eats.store Client Credentials scope. You can find code samples and responses for each of the endpoints in our API reference pages.

Once you have created your menus for your stores, you can use your test account to log in to Uber Eats where only you as the developer will be able to see your test store and its associated menu items. Updates to menus are reflected immediately, though you will need to refresh your browser or app if uploading a new menu while viewing. Images are the only components of menus that may take up to a few hours to be processed.

Avoiding Manual Updates
To prevent data sync issues, partners who manage their store menus via the API should not also make updates via Menu Maker. When going live in a production environment, work with your internal contacts and Uber Eats partner manager to ensure menu integrated stores are excluded from manual menu update processes. In case you encounter issues caused by a manual menu update, overwrite the menu by uploading a new menu via the API. If the issue persists, submit a technical support request for help.

FAQ
What specifications do menu item images need to adhere to for successful processing?

File size < 25MB
JPG, WEBP or PNG format
320px ≤ Width ≤ 6000px
320px ≤ Height ≤ 6000px
Can I add alcoholic items to my menu?

Check with your Uber Eats partner manger to see if your stores are in alcohol-enabled markets. If you are wanting to offer alcoholic menu items in enabled markets, you must populate dish_info.classifications’s can_serve_alone and alcoholic_items fields for all menu items.

Can I define specific availability hours for categories, items, or modifiers?

Availability hours can be set at the item level by using the visibility_info fields defined in our menu reference. However, these rules only apply when an item is used as a parent item and not when an item is used as a modifier option. Modifiers inherit the visibility data of the parent item. While availability hours cannot be defined at the category level, you can define the same visibility_info for all items within a category.

Tips for improving the support experience for customers?

We ask that all merchants start populating the core_price and bundled_items fields when configuring their menus. These fields allow you to provide a signal to Uber Eats on how to best support a customers when problems arise with their orders. The core_price field represents the intrinsic value of a modifier option (note that this field is ignored when set at the parent item level). This value can be equal or greater than the price of the the modifier option. The bundled_items helps you specify items that are always included as part of a combo, but not shown to or customizable by customers (i.e. fries as part of a burger combo). When set, the bundled_items are shown to customers when they are requesting support/refund (the initial purchase experience remains unchanged). You can reuse existing items when specify the bundled_items (e.g. reuse the fries items you already sell on the menu).



Order Integration

Overview
Use the Order API to ingest and manage incoming orders from Uber Eats. The API includes a webhook for incoming order notifications from Uber Eats. Once you have successfully set up your webhook URL and menu, retrieve, accept, and deny orders with the Order API endpoints.

Understanding the Order Flow
Adherence to the Eats order integration flow, diagrammed below, is required for order integration. Please study the diagram and read through this page carefully. Note: all orders that are scheduled must be accepted twice, once during the orders.scheduled.notification and again at orders.notification.




Order Notifications
The Order API sends notifications to your app’s configured webhook when an order is placed or canceled. Each notification has a corresponding event_type. See the Order Notification and Order Cancelled reference pages for full details.

event_type	Description
orders.notification	Sent whenever an order is created.
orders.cancel	Sent when an order is cancelled (e.g. by the user or by Uber).
orders.fulfillment_issues.resolved	Sent whenever a customer has confirmed change on Resolve Order Fulfillment endpoint. (Only applies to stores on API version 1.0.0 or above)
orders.scheduled.notification	Sent whenever an order is created. (Only application to stores on API version 1.0.0 or above)
Your service (a single webhook URL) can receive webhooks for multiple stores, as long as the developer is provisioned to each individual store.

Expected Response
For all webhooks:

Your service should return a 200 response status code with an empty response body to acknowledge receipt of webhook events. If no acknowledgement is received, Uber will continue to retry the webhook according to the retry logic described below.

Pull the order information using the resource_href, which corresponds to the Get Order endpoint. Use the user_id (which corresponds to store_id) from the webhook to map it to the right store for notifications and order injections.

For orders.notification only:

After acknowledging receipt of an orders.notification webhook, you must explicitly POST Accept Order, POST Adjust Fulfillment Issues, or POST Deny Order within 11.5 minutes. Otherwise the order will time out and auto-cancel. Order acceptances should be posted as quickly as possible to minimize Eater cancellations. If your store is set up to receive robocalls for unaccepted orders, a robocall will be triggered if no Accept/Deny is posted after 90 seconds.
Order Webhook Retry Logic
Your service should return an HTTP 200 response code with an empty response body to acknowledge receipt of the webhook event. If Uber does not receive a 200 acknowledgement response, the webhook event will be resent based on an exponential backoff algorithm (i.e. starting at 1 second after the initial attempt, then 2 seconds, then 4 seconds etc.) until 7 total events were sent without a response.

Webhook Security
Webhook messages are signed so that your app can verify that the sender is Uber. Webhooks requests contain an X-Uber-Signature header. The value of this field is a lowercased hexadecimal HMAC signature of the webhook HTTP request body, using the client secret as a key and SHA256 as the hash function.

Python Example

digester = hmac.new(client_secret, webhook_body, hashlib.sha256)
return digester.hexdigest()
Accepting Orders
Once an order is successfully accepted through the Order Acceptance endpoint POST Accept Order, no further action is required through the API unless a cancellation occurs. Customers will see that the store is now preparing their order.

Apart from initiating order cancellations, there is no endpoint for stores to provide order updates after acceptance (e.g. to mark an order as ready for pickup or to delay an order). For delivery orders, a courier will be dispatched based on the Uber predicted order prep time. This number will vary depending on various historical and real-time factors. For pickup orders, customers will be notified that their order is ready for pickup after the predicted order prep time has elapsed.

Adjusting Order Fulfillment
If you can’t fulfill an entire order due to various reasons, you can use the Resolve Order Fulfillment endpoint. This lets your application inform the customer, via the Uber Eats app, that certain items or instructions can’t be met.

When this endpoint is triggered:

The customer receives a notification on their Uber Eats app.
They can choose to either:
Cancel the order, which triggers the orders.failure webhook.
Modify their cart based on the given feedback.
If the customer agrees to the adjustments, your integration will receive the order.fulfillment_issues.resolved webhook. You should then fetch the updated order details from the “Get Order Details” endpoint.
Please note: This feature is exclusive to the Uber Eats app on iOS and Android. It’s not available or testable on web browsers.

Denying Orders
Orders should be programmatically denied POST Deny Order if they are not able to be injected into the POS system. All denied orders for a location follow one of the two order injection error workflows below. This is configured when a store is provisioned. To switch between workflows, submit a POS Provision configuration request.

(Default) For stores not using Uber Eats Orders, orders are immediately canceled when denied. No courier will be dispatched and the customer will be notified that the store was unable to fulfill the order.

For stores actively using Uber Eats Orders to manage orders, POS-denied orders can be manually accepted on Uber Eats Orders by in-store staff. The dashboard will flash red and display instructions to manually enter order details into the POS. If no manual order acceptance is received within 11.5 minutes of the order placement time, the order will be canceled.

Testing Orders
After setting up your webhook URL, follow the steps below to test orders on Uber Eats using your test accounts.

Eater (Customer) Setup: Sign in to the Uber Eats consumer website with your test developer account. Set the delivery address as the test store address. Your test store should show up, and you should be able to browse the menu. If your test store is not showing up as available on Uber Eats, make sure your menu’s service_availability is set to encompass the time of testing or you may need to change your store hours.

Store Setup: In an incognito Chrome browser, log in to Uber Eats Orders using your test store credentials. Though integrated stores are not required to use Uber Eats Orders, it is helpful to view orders for testing purposes. Ensure that the store is set to Open.

Place an Order: Request an order like a normal user. You do not need to enter any payment information and no couriers will be dispatched. The order should flow through on the store side to Uber Eats Orders. A webhook should be sent to your webhook URL. Note that orders will not be removed from the dashboard but they will expire after an hour and be marked as “Unable to Deliver”. Since this is a test store, this is normal expected behavior. If you’d like, you can re-order (as the eater) from the test store multiple times to test multiple webhooks.

Check if the webhook was received: Your service should have received a notification request from Uber, with the request body similar to the example webhook on the orders.notification reference page. Acknowledge that your service received the webhook by sending a 200 status code response. If you did not receive a webhook notification, make sure you used a valid webhook URL and have enabled your service to receive requests.

Test ACCEPT_pos_order and DENY_pos_order responses: Use the POST /eats/orders/{order_id}/accept_pos_order endpoint to accept the order from Uber. Then place another order and use the POST /eats/orders/{order_id}/deny_pos_order endpoint to deny the second order. Ensure the appropriate responses are being generated for each order.


