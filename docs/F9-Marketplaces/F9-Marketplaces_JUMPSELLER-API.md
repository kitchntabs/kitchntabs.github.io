Jumpseller logo
Search...
Endpoint Structure
Version
Authentication
Plain JSON only. No XML.
Rate Limit
Pagination
More
Stores
Hooks
Apps
Products
Product Options
Product Option Values
Product Variants
Product Images
Product Attachments
Product DigitalProducts
Product Custom Fields
Categories
Orders
Fulfillments
Pages
Customers
Customer Categories
Customer Additional Fields
Promotions
Payment Methods
Shipping Methods
Pickup Locations
Custom Fields
Custom Field Select Options
Checkout Custom Fields
Countries
Regions
Municipalities
Taxes
Partners
Cart
Documents
Transaction Ledgers
Products Locations
get
Stock by Product and Location
put
Update Stock by Product and Location
redocly logoAPI docs by Redocly
Jumpseller API (1.0.0)
Endpoint Structure
All URLs are in the format:

https://api.jumpseller.com/v1/path.json  
The path is prefixed by the API version.

For example, to request all the products at your store, you would append the products' index path to the base URL to create the following URL:

https://api.jumpseller.com/v1/products.json



Version
The current version of the API is v1.
If we change the API in backward-incompatible ways, we'll increase the version number and maintain stable support for the old urls.


Authentication
The API uses a token-based authentication with a combination of a login key and an auth token. Both parameters can be found on the left sidebar of the Account section, accessed from the main menu of your Admin Panel. The auth token of the user can be reset on the same page.

Store Login

The auth token is a 32 characters string.

To make authenticated requests, you can either use Basic Authentication (recommend method) or provide the login and auth token in the URL parameters (deprecated method).

If you are developing a Jumpseller App, the authentication should be done using OAuth-2. Please read the article Build an App for more information.


Query Parameters (deprecated)
Assuming login is XXXXX and authtoken is YYYYY we present the following examples (the real values can be found on the left sidebar of the Account section, accessed from the main menu of your Admin Panel):

Curl Examples
In curl, you can invoke that URL with:

curl -X GET "https://api.jumpseller.com/v1/products.json?login=XXXXX&authtoken=YYYYY"
To create a product, you will include the JSON data and specify the MIME Type:

curl -X POST -d '{ "product" : {"name": "My new Product!", "price": 100} }' "https://api.jumpseller.com/v1/products.json?login=XXXXX&authtoken=YYYYY" -H "Content-Type:application/json"
and to update the product identified with 123:

curl -X PUT -d '{ "product" : {"name": "My updated Product!", "price": 99} }' "https://api.jumpseller.com/v1/products/123.json?login=XXXXX&authtoken=YYYYY" -H "Content-Type:application/json"
or delete it:

curl -X DELETE "https://api.jumpseller.com/v1/products/123.json?login=XXXXX&authtoken=YYYYY" -H "Content-Type:application/json"
PHP Examples
$url = 'https://api.jumpseller.com/v1/products.json?login=XXXXX&authtoken=YYYYY';
$ch = curl_init($url);
curl_setopt($ch, CURLOPT_RETURNTRANSFER, true);
curl_setopt($ch, CURLOPT_HTTPHEADER, array('Content-Type: application/json'));

curl_setopt($ch, CURLOPT_CUSTOMREQUEST, "POST"); //post method
curl_setopt($ch, CURLOPT_POSTFIELDS, '{ "product" : {"name": "My updated Product!", "price": 99} }');

$result = curl_exec($ch);
print_r($result);
curl_close($ch);
Basic Authentication
Assuming login is XXXXX and authtoken is YYYYY we present the following examples (the real values can be found on the left sidebar of the Account section, accessed from the main menu of your Admin Panel):

Curl Examples
In curl, you can invoke that URL with:

curl -u XXXXX:YYYYY -X GET "https://api.jumpseller.com/v1/products.json"
To create a product, you will include the JSON data and specify the MIME Type:

curl -u XXXXX:YYYYY -X POST -d '{ "product" : {"name": "My new Product!", "price": 100} }' "https://api.jumpseller.com/v1/products.json" -H "Content-Type:application/json"
and to update the product identified with 123:

curl -u XXXXX:YYYYY -X PUT -d '{ "product" : {"name": "My updated Product!", "price": 99} }' "https://api.jumpseller.com/v1/products/123.json" -H "Content-Type:application/json"
or delete it:

curl -u XXXXX:YYYYY -X DELETE "https://api.jumpseller.com/v1/products/123.json" -H "Content-Type:application/json"
PHP Examples
$login = 'XXXXX';
$authtoken = 'YYYYY';
$url = 'https://api.jumpseller.com/v1/products.json';
$ch = curl_init($url);
curl_setopt($ch, CURLOPT_RETURNTRANSFER, true);
curl_setopt($ch, CURLOPT_HTTPHEADER, array('Content-Type: application/json'));
curl_setopt($ch, CURLOPT_USERPWD, $login . ":" . $authtoken);

curl_setopt($ch, CURLOPT_CUSTOMREQUEST, "POST"); //post method
curl_setopt($ch, CURLOPT_POSTFIELDS, '{ "product" : {"name": "My updated Product!", "price": 99} }');

$result = curl_exec($ch);
print_r($result);
curl_close($ch);
OAuth2
OAuth 2 is the industry-standard protocol for authorization. Generally, OAuth provides to clients a secure delegated access to server resources on behalf of a resource owner. It specifies a process for resource owners to authorize third-party access to their server resources without sharing their credentials. Designed specifically to work with HTTP, OAuth essentially allows access tokens to be issued to third-party clients by an authorization server, with the approval of the resource owner. The third party then uses the access token to access the protected resources hosted by the resource server.

Read more about this type of authentication and how to implement it in your Jumpseller App by clicking here.




Plain JSON only. No XML.
We only support JSON for data serialization.
Our node format has no root element.
We use snake_case to describe attribute keys (like "created_at").
All empty value are replaced with null strings.
All API URLs end in .json to indicate that they accept and return JSON.
POST and PUT methods require you to explicitly state the MIME type of your request's body content as "application/json".

Rate Limit
You can perform a maximum of:

800 (eight hundred) requests per minute and
20 (twenty) requests per second
If you exceed this limit, you'll get a 429 Too Many Requests (Rate Limit Exceeded) response for subsequent requests.

The rate limits apply by IP address and by store. This means that multiple requests on different stores are not counted towards the same rate limit.

This limits are necessary to ensure resources are correctly used. Your application should be aware of this limits and retry any unsuccessful request, check the following Ruby stub:

tries = 0; limit = 3;
begin
  HTTParty.send(method, uri) # perform an API call.
  tries += 1
rescue # 403 response
  unless tries >= limit
    sleep 1.0 # wait the necessary time before retrying the call again.
    retry
  end
end
Finally, you can review the Response Headers of each request:

Jumpseller-PerMinuteRateLimit-Limit: 800  
Jumpseller-PerMinuteRateLimit-Remaining: 799 # requests available on the per-minute interval  
Jumpseller-PerSecondRateLimit-Limit: 20  
Jumpseller-PerSecondRateLimit-Remaining: 19 # requests available on the per-second interval
to better model your application requests intervals.

After 2000 rate-limit hits, we will set a temporary ban. The Response Header Jumpseller-BannedByRateLimit-Reset informs you the time (UTC) when will your ban be reseted:

Jumpseller-BannedByRateLimit-Reset: 2024-05-23T16:13:47+00:00



Pagination
By default we will return 50 objects (products, orders, etc) per page. There is a maximum of 100, using a query string &limit=100. If the result set gets paginated it is your responsibility to check the next page for more objects -- you do this by using query strings &page=2, &page=3 and so on.

https://api.jumpseller.com/v1/products.json?page=3&limit=100



More
Jumpseller API wrapper provides a public Ruby abstraction over our API;
Apps Page showcases external integrations with Jumpseller done by technical experts;
Imgbb API provides an easy way to upload and temporaly host for images and files.




Stores
Retrieve Store Information.
Authorizations:
BasicAuthentication(loginParameterauthtokenParameter)
Responses
200 OK

get
/store/info.json
Response samples
200
Content type
application/json

Copy
Expand allCollapse all
{
"name": "string",
"code": "string",
"currency": "string",
"country": "string",
"timezone": "string",
"email": "string",
"hooks_token": "string",
"url": "string",
"logo": "string",
"weight_unit": "string",
"subscription_status": "string",
"subscription_plan": "string",
"fb_pixel_id": "string",
"address": {
"address": "string",
"city": "string",
"postal": "string",
"region": "string",
"country": "string",
"region_code": "string",
"country_code": "string"
},
"whatsapp_phone": "string"
}
Retrieve Store Languages.
Authorizations:
BasicAuthentication(loginParameterauthtokenParameter)
Responses
200 OK

get
/store/languages.json
Response samples
200
Content type
application/json

Copy
Expand allCollapse all
[
{
"code": "string",
"name": "string"
}
]
Hooks
Retrieve all Hooks.
Authorizations:
BasicAuthentication(loginParameterauthtokenParameter)
query Parameters
limit	
integer <integer> <= 200
Default: 50
List restriction

page	
integer <integer>
Default: 1
List page

Responses
200 An array of Hooks

get
/hooks.json
Response samples
200
Content type
application/json

Copy
Expand allCollapse all
[
{
"hook": {}
}
]
Create a new Hook.
Authorizations:
BasicAuthentication(loginParameterauthtokenParameter)
Request Body schema: application/json
required
Hook parameters.

hook	
object (HookEditFields)
Responses
200 OK
404 Hook Not Found.

post
/hooks.json
Request samples
Payload
Content type
application/json

Copy
Expand allCollapse all
{
"hook": {
"event": "order_updated",
"url": "string"
}
}
Response samples
200404
Content type
application/json

Copy
Expand allCollapse all
{
"hook": {
"id": 0,
"name": "string",
"event": "string",
"url": "string",
"created_at": "string"
}
}
Retrieve a single Hook.
Authorizations:
BasicAuthentication(loginParameterauthtokenParameter)
path Parameters
id
required
integer <int32>
Id of the Hook

Responses
200 OK
404 Hook Not Found.

get
/hooks/{id}.json
Response samples
200404
Content type
application/json

Copy
Expand allCollapse all
{
"hook": {
"id": 0,
"name": "string",
"event": "string",
"url": "string",
"created_at": "string"
}
}
Update a Hook.
Authorizations:
BasicAuthentication(loginParameterauthtokenParameter)
path Parameters
id
required
integer <int32>
Id of the Hook

Request Body schema: application/json
required
Hook parameters.

hook	
object (HookEditFields)
Responses
200 OK
404 Hook Not Found.

put
/hooks/{id}.json
Request samples
Payload
Content type
application/json

Copy
Expand allCollapse all
{
"hook": {
"event": "order_updated",
"url": "string"
}
}
Response samples
200404
Content type
application/json

Copy
Expand allCollapse all
{
"hook": {
"id": 0,
"name": "string",
"event": "string",
"url": "string",
"created_at": "string"
}
}
Delete an existing Hook.
Authorizations:
BasicAuthentication(loginParameterauthtokenParameter)
path Parameters
id
required
integer <int32>
Id of the Hook

Responses
200 OK
404 Hook Not Found.

delete
/hooks/{id}.json
Response samples
200404
Content type
application/json

Copy
"string"
Apps
Retrieve all the Store's JSApps.
Authorizations:
BasicAuthentication(loginParameterauthtokenParameter)
Responses
200 OK

get
/jsapps.json
Response samples
200
Content type
application/json

Copy
Expand allCollapse all
{
"apps": [
{}
]
}
Create a Store JSApp.
Authorizations:
BasicAuthentication(loginParameterauthtokenParameter)
Request Body schema: application/json
required
JSApp parameters to create

app	
object (JSApp)
Responses
200 OK

post
/jsapps.json
Request samples
Payload
Content type
application/json

Copy
Expand allCollapse all
{
"app": {
"url": "string",
"template": "string",
"element": "string"
}
}
Response samples
200
Content type
application/json

Copy
{
"url": "string",
"template": "string",
"element": "string"
}
Retrieve a JSApp.
Authorizations:
BasicAuthentication(loginParameterauthtokenParameter)
path Parameters
code
required
string
Code of the App

Responses
200 OK

get
/jsapps/{code}.json
Response samples
200
Content type
application/json

Copy
{
"url": "string",
"template": "string",
"element": "string"
}
Delete an existing JSApp.
Authorizations:
BasicAuthentication(loginParameterauthtokenParameter)
path Parameters
code
required
string
Code of the App

Responses
200 OK
404 App Not Found.

delete
/jsapps/{code}.json
Response samples
200404
Content type
application/json

Copy
"string"
Products
Retrieve all Products.
Authorizations:
BasicAuthentication(loginParameterauthtokenParameter)
query Parameters
limit	
integer <integer> <= 200
Default: 50
List restriction

page	
integer <integer>
Default: 1
List page

locale	
string <string>
Locale code of the translation

Responses
200 OK

get
/products.json
Response samples
200
Content type
application/json

Copy
Expand allCollapse all
[
{
"product": {}
}
]
Create a new Product.
Authorizations:
BasicAuthentication(loginParameterauthtokenParameter)
query Parameters
locale	
string <string>
Locale code of the translation

Request Body schema: application/json
required
Product parameters.

product	
object (ProductCreateFields)
Responses
200 OK

post
/products.json
Request samples
Payload
Content type
application/json

Copy
Expand allCollapse all
{
"product": {
"name": "string",
"description": "string",
"page_title": "string",
"meta_description": "string",
"type": "string",
"days_to_expire": 365,
"price": 0.1,
"weight": 1,
"stock": 100,
"stock_unlimited": true,
"stock_threshold": 0,
"stock_notification": true,
"cost_per_item": 0,
"compare_at_price": 0,
"minimum_quantity": 0,
"maximum_quantity": 0,
"sku": "string",
"barcode": "string",
"google_product_category": "string",
"featured": false,
"shipping_required": true,
"status": "available",
"package_format": "box",
"length": 0.1,
"width": 0.1,
"height": 0.1,
"diameter": 0.1,
"categories": [],
"variants": []
}
}
Response samples
200
Content type
application/json

Copy
Expand allCollapse all
{
"product": {
"id": 0,
"name": "string",
"page_title": "string",
"description": "string",
"type": "string",
"days_to_expire": 365,
"price": 0.1,
"discount": 0.1,
"weight": 1,
"stock": 100,
"stock_unlimited": true,
"stock_threshold": 0,
"stock_notification": true,
"cost_per_item": 0,
"compare_at_price": 0,
"sku": "string",
"brand": "string",
"barcode": "string",
"google_product_category": "string",
"featured": false,
"reviews_enabled": true,
"status": "available",
"created_at": "string",
"updated_at": "string",
"package_format": "box",
"length": 0.1,
"width": 0.1,
"height": 0.1,
"diameter": 0.1,
"permalink": "string",
"categories": [],
"images": [],
"variants": []
}
}
Count all Products.
Authorizations:
BasicAuthentication(loginParameterauthtokenParameter)
Responses
200 OK

get
/products/count.json
Response samples
200
Content type
application/json

Copy
{
"count": 0
}
Retrieves Products after the given id.
Authorizations:
BasicAuthentication(loginParameterauthtokenParameter)
path Parameters
id
required
integer <int32>
Id of the Product

query Parameters
locale	
string <string>
Locale code of the translation

Responses
200 OK
404 Product Not Found.

get
/products/after/{id}.json
Response samples
200404
Content type
application/json

Copy
Expand allCollapse all
[
{
"product": {}
}
]
Retrieve Products filtered by status.
Authorizations:
BasicAuthentication(loginParameterauthtokenParameter)
path Parameters
status
required
string
Enum: "available" "not-available" "disabled"
Status of the Product used as filter

query Parameters
locale	
string <string>
Locale code of the translation

Responses
200 OK
404 Status Invalid.

get
/products/status/{status}.json
Response samples
200404
Content type
application/json

Copy
Expand allCollapse all
[
{
"product": {}
}
]
Retrieve Products filtered by category.
Authorizations:
BasicAuthentication(loginParameterauthtokenParameter)
path Parameters
category_id
required
integer <int32>
Category ID of the Product used as filter

query Parameters
locale	
string <string>
Locale code of the translation

Responses
200 OK
404 Product Not Found.

get
/products/category/{category_id}.json
Response samples
200404
Content type
application/json

Copy
Expand allCollapse all
[
{
"product": {}
}
]
Count Products filtered by status.
Authorizations:
BasicAuthentication(loginParameterauthtokenParameter)
path Parameters
status
required
string
Enum: "available" "not-available" "disabled"
Status of the Product used as filter

query Parameters
locale	
string <string>
Locale code of the translation

Responses
200 OK
404 Status Invalid.

get
/products/status/{status}/count.json
Response samples
200404
Content type
application/json

Copy
{
"count": 0
}
Count Products filtered by category.
Authorizations:
BasicAuthentication(loginParameterauthtokenParameter)
path Parameters
category_id
required
integer <int32>
Category ID of the Product used as filter

query Parameters
locale	
string <string>
Locale code of the translation

Responses
200 OK
404 Category Not Found.

get
/products/category/{category_id}/count.json
Response samples
200404
Content type
application/json

Copy
{
"count": 0
}
Retrieve a single Product.
Authorizations:
BasicAuthentication(loginParameterauthtokenParameter)
path Parameters
id
required
integer <int32>
Id of the Product

query Parameters
locale	
string <string>
Locale code of the translation

Responses
200 OK
404 Product Not Found.

get
/products/{id}.json
Response samples
200404
Content type
application/json

Copy
Expand allCollapse all
{
"product": {
"id": 0,
"name": "string",
"page_title": "string",
"description": "string",
"type": "string",
"days_to_expire": 365,
"price": 0.1,
"discount": 0.1,
"weight": 1,
"stock": 100,
"stock_unlimited": true,
"stock_threshold": 0,
"stock_notification": true,
"cost_per_item": 0,
"compare_at_price": 0,
"sku": "string",
"brand": "string",
"barcode": "string",
"google_product_category": "string",
"featured": false,
"reviews_enabled": true,
"status": "available",
"created_at": "string",
"updated_at": "string",
"package_format": "box",
"length": 0.1,
"width": 0.1,
"height": 0.1,
"diameter": 0.1,
"permalink": "string",
"categories": [],
"images": [],
"variants": []
}
}
Modify an existing Product.
Authorizations:
BasicAuthentication(loginParameterauthtokenParameter)
path Parameters
id
required
integer <int32>
Id of the Product

query Parameters
locale	
string <string>
Locale code of the translation

Request Body schema: application/json
required
Product parameters to change

product	
object (ProductEditFields)
Responses
200 OK
404 Product Not Found.

put
/products/{id}.json
Request samples
Payload
Content type
application/json

Copy
Expand allCollapse all
{
"product": {
"name": "string",
"description": "string",
"page_title": "string",
"meta_description": "string",
"type": "string",
"days_to_expire": 365,
"price": 0.1,
"weight": 1,
"stock": 100,
"stock_unlimited": true,
"stock_threshold": 0,
"stock_notification": true,
"cost_per_item": 0,
"compare_at_price": 0,
"minimum_quantity": 0,
"maximum_quantity": 0,
"sku": "string",
"barcode": "string",
"google_product_category": "string",
"featured": false,
"shipping_required": true,
"status": "available",
"package_format": "box",
"length": 0.1,
"width": 0.1,
"height": 0.1,
"diameter": 0.1,
"permalink": "string",
"categories": [],
"variants": []
}
}
Response samples
200404
Content type
application/json

Copy
Expand allCollapse all
{
"product": {
"id": 0,
"name": "string",
"page_title": "string",
"description": "string",
"type": "string",
"days_to_expire": 365,
"price": 0.1,
"discount": 0.1,
"weight": 1,
"stock": 100,
"stock_unlimited": true,
"stock_threshold": 0,
"stock_notification": true,
"cost_per_item": 0,
"compare_at_price": 0,
"sku": "string",
"brand": "string",
"barcode": "string",
"google_product_category": "string",
"featured": false,
"reviews_enabled": true,
"status": "available",
"created_at": "string",
"updated_at": "string",
"package_format": "box",
"length": 0.1,
"width": 0.1,
"height": 0.1,
"diameter": 0.1,
"permalink": "string",
"categories": [],
"images": [],
"variants": []
}
}
Delete an existing Product.
Authorizations:
BasicAuthentication(loginParameterauthtokenParameter)
path Parameters
id
required
integer <int32>
Id of the Product

Responses
200 OK
404 Product Not Found.

delete
/products/{id}.json
Response samples
200404
Content type
application/json

Copy
"string"
Retrieve a Product List from a query.
Endpoint example:

https://api.jumpseller.com/v1/products/search.json?query=test&fields=name,description 
Authorizations:
BasicAuthentication(loginParameterauthtokenParameter)
query Parameters
locale	
string <string>
Locale code of the translation

query
required
string <string>
Text to query for the Product

fields	
string <string>
Enum: "sku" "barcode" "brand" "name" "description" "variants" "option_name" "custom_fields" "custom_fields_selects"
Comma separated values of the fields to query for the Product

status	
string <string>
Enum: "available" "not-available" "disabled" "featured"
Product Status to query for the Product

categories	
string <string>
Comma separated values of the Category IDs to query for the Product

Responses
200 An array of products
404 Invalid query.

get
/products/search.json
Response samples
200404
Content type
application/json

Copy
Expand allCollapse all
[
{
"product": {}
}
]
Product Options
Retrieve all Product Options.
Authorizations:
BasicAuthentication(loginParameterauthtokenParameter)
path Parameters
id
required
integer <int32>
Id of the Product

Responses
200 OK
404 Product Not Found.

get
/products/{id}/options.json
Response samples
200404
Content type
application/json

Copy
Expand allCollapse all
[
{
"option": {}
}
]
Create a new Product Option.
Authorizations:
BasicAuthentication(loginParameterauthtokenParameter)
path Parameters
id
required
integer <int32>
Id of the Product

Request Body schema: application/json
required
Product Option parameters.

option	
object (ProductOptionEditFields)
Responses
200 OK

post
/products/{id}/options.json
Request samples
Payload
Content type
application/json

Copy
Expand allCollapse all
{
"option": {
"name": "string",
"position": 0,
"option_type": "option"
}
}
Response samples
200
Content type
application/json

Copy
Expand allCollapse all
{
"option": {
"id": 0,
"name": "string",
"position": 0,
"option_type": "option",
"values": []
}
}
Count all Product Options.
Authorizations:
BasicAuthentication(loginParameterauthtokenParameter)
path Parameters
id
required
integer <int32>
Id of the Product

Responses
200 OK
404 Product Not Found.

get
/products/{id}/options/count.json
Response samples
200404
Content type
application/json

Copy
{
"count": 0
}
Retrieve a single Product Option.
Authorizations:
BasicAuthentication(loginParameterauthtokenParameter)
path Parameters
id
required
integer <int32>
Id of the Product

option_id
required
integer <int32>
Id of the Product Option

Responses
200 OK
404 Product Not Found.

get
/products/{id}/options/{option_id}.json
Response samples
200404
Content type
application/json

Copy
Expand allCollapse all
{
"option": {
"id": 0,
"name": "string",
"position": 0,
"option_type": "option",
"values": []
}
}
Modify an existing Product Option.
Authorizations:
BasicAuthentication(loginParameterauthtokenParameter)
path Parameters
id
required
integer <int32>
Id of the Product

option_id
required
integer <int32>
Id of the Product Option

Request Body schema: application/json
required
Product option parameters to change

option	
object (ProductOptionEditFields)
Responses
200 OK
404 Product Not Found.

put
/products/{id}/options/{option_id}.json
Request samples
Payload
Content type
application/json

Copy
Expand allCollapse all
{
"option": {
"name": "string",
"position": 0,
"option_type": "option"
}
}
Response samples
200404
Content type
application/json

Copy
Expand allCollapse all
{
"option": {
"id": 0,
"name": "string",
"position": 0,
"option_type": "option",
"values": []
}
}
Delete a Product Option.
Authorizations:
BasicAuthentication(loginParameterauthtokenParameter)
path Parameters
id
required
integer <int32>
Id of the Product

option_id
required
integer <int32>
Id of the Product Option

Responses
200 OK
404 Product Not Found.

delete
/products/{id}/options/{option_id}.json
Response samples
200404
Content type
application/json

Copy
"string"
Product Option Values
Retrieve all Product Option Values.
Authorizations:
BasicAuthentication(loginParameterauthtokenParameter)
path Parameters
id
required
integer <int32>
Id of the Product

option_id
required
integer <int32>
ID of the Product Option

Responses
200 OK
404 Product Not Found.

get
/products/{id}/options/{option_id}/values.json
Response samples
200404
Content type
application/json

Copy
Expand allCollapse all
[
{
"value": {}
}
]
Create a new Product Option Value.
Authorizations:
BasicAuthentication(loginParameterauthtokenParameter)
path Parameters
id
required
integer <int32>
Id of the Product

option_id
required
integer <int32>
Id of the Product Option

Request Body schema: application/json
required
Product Option Value parameters.

value	
object (ProductOptionValueEditFields)
Responses
200 OK

post
/products/{id}/options/{option_id}/values.json
Request samples
Payload
Content type
application/json

Copy
Expand allCollapse all
{
"value": {
"name": "string",
"position": 0,
"custom": "string"
}
}
Response samples
200
Content type
application/json

Copy
Expand allCollapse all
{
"value": {
"id": 0,
"name": "string",
"custom": "string",
"position": 0,
"product_option": {},
"variants": []
}
}
Count all Product Option Values.
Authorizations:
BasicAuthentication(loginParameterauthtokenParameter)
path Parameters
id
required
integer <int32>
Id of the Product

option_id
required
integer <int32>
ID of the Product Option

Responses
200 OK
404 Product Not Found.

get
/products/{id}/options/{option_id}/values/count.json
Response samples
200404
Content type
application/json

Copy
{
"count": 0
}
Retrieve a single Product Option Value.
Authorizations:
BasicAuthentication(loginParameterauthtokenParameter)
path Parameters
id
required
integer <int32>
Id of the Product

option_id
required
integer <int32>
Id of the Product Option

value_id
required
integer <int32>
ID of the Product Option Value

Responses
200 OK
404 Product Not Found.

get
/products/{id}/options/{option_id}/values/{value_id}.json
Response samples
200404
Content type
application/json

Copy
Expand allCollapse all
{
"value": {
"id": 0,
"name": "string",
"custom": "string",
"position": 0,
"product_option": {},
"variants": []
}
}
Modify an existing Product Option Value.
Authorizations:
BasicAuthentication(loginParameterauthtokenParameter)
path Parameters
id
required
integer <int32>
Id of the Product

option_id
required
integer <int32>
Id of the Product Option

value_id
required
integer <int32>
Id of the Product Option Value

Request Body schema: application/json
required
Product option value parameters to change

value	
object (ProductOptionValueEditFields)
Responses
200 OK
404 Product Not Found.

put
/products/{id}/options/{option_id}/values/{value_id}.json
Request samples
Payload
Content type
application/json

Copy
Expand allCollapse all
{
"value": {
"name": "string",
"position": 0,
"custom": "string"
}
}
Response samples
200404
Content type
application/json

Copy
Expand allCollapse all
{
"value": {
"id": 0,
"name": "string",
"custom": "string",
"position": 0,
"product_option": {},
"variants": []
}
}
Delete a Product Option Value.
Authorizations:
BasicAuthentication(loginParameterauthtokenParameter)
path Parameters
id
required
integer <int32>
Id of the Product

option_id
required
integer <int32>
Id of the Product Option

value_id
required
integer <int32>
ID of the Product Option Value

Responses
200 OK
404 Product Not Found.

delete
/products/{id}/options/{option_id}/values/{value_id}.json
Response samples
200404
Content type
application/json

Copy
"string"
Product Variants
Retrieve a single Product Variant.
Authorizations:
BasicAuthentication(loginParameterauthtokenParameter)
path Parameters
id
required
integer <int32>
Id of the Product

variant_id
required
integer <int32>
Id of the Product Variant

Responses
200 OK
404 Product Not Found.

get
/products/{id}/variants/{variant_id}.json
Response samples
200404
Content type
application/json

Copy
Expand allCollapse all
{
"variant": {
"id": 0,
"price": 0.1,
"sku": "string",
"barcode": "string",
"stock": 100,
"stock_unlimited": true,
"stock_threshold": 0,
"stock_notification": true,
"cost_per_item": 0,
"compare_at_price": 0,
"options": [],
"image": {}
}
}
Modify an existing Product Variant.
Authorizations:
BasicAuthentication(loginParameterauthtokenParameter)
path Parameters
id
required
integer <int32>
Id of the Product

variant_id
required
integer <int32>
Id of the Product Variant

Request Body schema: application/json
required
Product Variant parameters to change

variant	
object (VariantEditFields)
Responses
200 OK
404 Product Not Found.

put
/products/{id}/variants/{variant_id}.json
Request samples
Payload
Content type
application/json

Copy
Expand allCollapse all
{
"variant": {
"price": 0.1,
"sku": "string",
"barcode": 123456,
"stock": 100,
"stock_unlimited": true,
"stock_threshold": 0,
"stock_notification": true,
"cost_per_item": 0,
"compare_at_price": 0,
"image_id": 0,
"options": []
}
}
Response samples
200404
Content type
application/json

Copy
Expand allCollapse all
{
"variant": {
"id": 0,
"price": 0.1,
"sku": "string",
"barcode": "string",
"stock": 100,
"stock_unlimited": true,
"stock_threshold": 0,
"stock_notification": true,
"cost_per_item": 0,
"compare_at_price": 0,
"options": [],
"image": {}
}
}
Retrieve all Product Variants.
Authorizations:
BasicAuthentication(loginParameterauthtokenParameter)
path Parameters
id
required
integer <int32>
Id of the Product

Responses
200 OK
404 Product Not Found.

get
/products/{id}/variants.json
Response samples
200404
Content type
application/json

Copy
Expand allCollapse all
[
{
"variant": {}
}
]
Create a new Product Variant.
Authorizations:
BasicAuthentication(loginParameterauthtokenParameter)
path Parameters
id
required
integer <int32>
Id of the Product

Request Body schema: application/json
required
Product Variant parameters.

variant	
object (VariantEditFields)
Responses
200 OK
404 Product Not Found.

post
/products/{id}/variants.json
Request samples
Payload
Content type
application/json

Copy
Expand allCollapse all
{
"variant": {
"price": 0.1,
"sku": "string",
"barcode": 123456,
"stock": 100,
"stock_unlimited": true,
"stock_threshold": 0,
"stock_notification": true,
"cost_per_item": 0,
"compare_at_price": 0,
"image_id": 0,
"options": []
}
}
Response samples
200404
Content type
application/json

Copy
Expand allCollapse all
{
"variant": {
"id": 0,
"price": 0.1,
"sku": "string",
"barcode": "string",
"stock": 100,
"stock_unlimited": true,
"stock_threshold": 0,
"stock_notification": true,
"cost_per_item": 0,
"compare_at_price": 0,
"options": [],
"image": {}
}
}
Count all Product Variants.
Authorizations:
BasicAuthentication(loginParameterauthtokenParameter)
path Parameters
id
required
integer <int32>
Id of the Product

Responses
200 OK
404 Product Not Found.

get
/products/{id}/variants/count.json
Response samples
200404
Content type
application/json

Copy
{
"count": 0
}
Product Images
Retrieve all Product Images.
Authorizations:
BasicAuthentication(loginParameterauthtokenParameter)
path Parameters
id
required
integer <int32>
Id of the Product

Responses
200 OK
404 Product Not Found.

get
/products/{id}/images.json
Response samples
200404
Content type
application/json

Copy
Expand allCollapse all
[
{
"image": {}
}
]
Create a new Product Image.
Authorizations:
BasicAuthentication(loginParameterauthtokenParameter)
path Parameters
id
required
integer <int32>
Id of the Product

Request Body schema: application/json
required
Product Image parameters.

image	
object (ImageEditFields)
Responses
200 OK

post
/products/{id}/images.json
Request samples
Payload
Content type
application/json

Copy
Expand allCollapse all
{
"image": {
"url": "string",
"position": 0
}
}
Response samples
200
Content type
application/json

Copy
Expand allCollapse all
{
"image": {
"id": 0,
"position": 0,
"url": "string"
}
}
Update a Product Image position.
Authorizations:
BasicAuthentication(loginParameterauthtokenParameter)
path Parameters
id
required
integer <int32>
Id of the Product

image_id
required
integer <int32>
Id of the Product Image

query Parameters
position
required
integer <int32>
Desired position of the Product Image

Responses
200 OK
404 Product or Image Not Found.

put
/products/{id}/images.json
Response samples
200404
Content type
application/json

Copy
Expand allCollapse all
{
"image": {
"id": 0,
"position": 0,
"url": "string"
}
}
Count all Product Images.
Authorizations:
BasicAuthentication(loginParameterauthtokenParameter)
path Parameters
id
required
integer <int32>
Id of the Product

Responses
200 OK
404 Product Not Found.

get
/products/{id}/images/count.json
Response samples
200404
Content type
application/json

Copy
{
"count": 0
}
Retrieve a single Product Image.
Authorizations:
BasicAuthentication(loginParameterauthtokenParameter)
path Parameters
id
required
integer <int32>
Id of the Product

image_id
required
integer <int32>
Id of the Product Image

Responses
200 OK
404 Product Not Found.

get
/products/{id}/images/{image_id}.json
Response samples
200404
Content type
application/json

Copy
Expand allCollapse all
{
"image": {
"id": 0,
"position": 0,
"url": "string"
}
}
Delete a Product Image.
Authorizations:
BasicAuthentication(loginParameterauthtokenParameter)
path Parameters
id
required
integer <int32>
Id of the Product

image_id
required
integer <int32>
Id of the Product Image

Responses
200 OK
404 Product Not Found.

delete
/products/{id}/images/{image_id}.json
Response samples
200404
Content type
application/json

Copy
"string"
Product Attachments
Retrieve all Product Attachments.
Authorizations:
BasicAuthentication(loginParameterauthtokenParameter)
path Parameters
id
required
integer <int32>
Id of the Product

Responses
200 OK
404 Product Not Found.

get
/products/{id}/attachments.json
Response samples
200404
Content type
application/json

Copy
Expand allCollapse all
[
{
"attachment": {}
}
]
Create a new Product Attachment.
Authorizations:
BasicAuthentication(loginParameterauthtokenParameter)
path Parameters
id
required
integer <int32>
Id of the Product

Request Body schema: application/json
required
Product Attachment parameters.

attachment	
object (AttachmentEditFields)
Responses
200 OK

post
/products/{id}/attachments.json
Request samples
Payload
Content type
application/json

Copy
Expand allCollapse all
{
"attachment": {
"filename": "string",
"url": "string"
}
}
Response samples
200
Content type
application/json

Copy
Expand allCollapse all
{
"attachment": {
"id": 0,
"url": "string"
}
}
Count all Product Attachments.
Authorizations:
BasicAuthentication(loginParameterauthtokenParameter)
path Parameters
id
required
integer <int32>
Id of the Product

Responses
200 OK
404 Product Not Found.

get
/products/{id}/attachments/count.json
Response samples
200404
Content type
application/json

Copy
{
"count": 0
}
Retrieve a single Product Attachment.
Authorizations:
BasicAuthentication(loginParameterauthtokenParameter)
path Parameters
id
required
integer <int32>
Id of the Product

attachment_id
required
integer <int32>
Id of the Product Attachment

Responses
200 OK
404 Product Not Found.

get
/products/{id}/attachments/{attachment_id}.json
Response samples
200404
Content type
application/json

Copy
Expand allCollapse all
{
"attachment": {
"id": 0,
"url": "string"
}
}
Delete a Product Attachment.
Authorizations:
BasicAuthentication(loginParameterauthtokenParameter)
path Parameters
id
required
integer <int32>
Id of the Product

attachment_id
required
integer <int32>
Id of the Product Attachment

Responses
200 OK
404 Product Not Found.

delete
/products/{id}/attachments/{attachment_id}.json
Response samples
200404
Content type
application/json

Copy
"string"
Product DigitalProducts
Retrieve all Product DigitalProducts.
Authorizations:
BasicAuthentication(loginParameterauthtokenParameter)
path Parameters
id
required
integer <int32>
Id of the Product

Responses
200 OK
404 Product Not Found.

get
/products/{id}/digital_products.json
Response samples
200404
Content type
application/json

Copy
Expand allCollapse all
[
{
"digital_product": {}
}
]
Create a new Product DigitalProduct.
Authorizations:
BasicAuthentication(loginParameterauthtokenParameter)
path Parameters
id
required
integer <int32>
Id of the Product

Request Body schema: application/json
required
Product DigitalProduct parameters.

digital_product	
object (DigitalProductEditFields)
Responses
200 OK

post
/products/{id}/digital_products.json
Request samples
Payload
Content type
application/json

Copy
Expand allCollapse all
{
"digital_product": {
"filename": "string",
"url": "string"
}
}
Response samples
200
Content type
application/json

Copy
Expand allCollapse all
{
"digital_product": {
"id": 0,
"url": "string",
"expiration_seconds": 0
}
}
Count all Product DigitalProducts.
Authorizations:
BasicAuthentication(loginParameterauthtokenParameter)
path Parameters
id
required
integer <int32>
Id of the Product

Responses
200 OK
404 Product Not Found.

get
/products/{id}/digital_products/count.json
Response samples
200404
Content type
application/json

Copy
{
"count": 0
}
Retrieve a single Product DigitalProduct.
Authorizations:
BasicAuthentication(loginParameterauthtokenParameter)
path Parameters
id
required
integer <int32>
Id of the Product

digital_product_id
required
integer <int32>
Id of the Product DigitalProduct

Responses
200 OK
404 Product Not Found.

get
/products/{id}/digital_products/{digital_product_id}.json
Response samples
200404
Content type
application/json

Copy
Expand allCollapse all
{
"digital_product": {
"id": 0,
"url": "string",
"expiration_seconds": 0
}
}
Delete a Product DigitalProduct.
Authorizations:
BasicAuthentication(loginParameterauthtokenParameter)
path Parameters
id
required
integer <int32>
Id of the Product

digital_product_id
required
integer <int32>
Id of the Product DigitalProduct

Responses
200 OK
404 Product Not Found.

delete
/products/{id}/digital_products/{digital_product_id}.json
Response samples
200404
Content type
application/json

Copy
"string"
Product Custom Fields
Retrieve all Product Custom Fields
Authorizations:
BasicAuthentication(loginParameterauthtokenParameter)
path Parameters
id
required
integer <int32>
Id of the Product

Responses
200 OK
404 Product Not Found.

get
/products/{id}/fields.json
Response samples
200404
Content type
application/json

Copy
Expand allCollapse all
[
{
"field": {}
}
]
Add an existing Custom Field to a Product.
Authorizations:
BasicAuthentication(loginParameterauthtokenParameter)
path Parameters
id
required
integer <int32>
Id of the Product

Request Body schema: application/json
required
Product Custom Field parameters.

field	
object (AddProductCustomFieldFields)
Responses
200 OK
404 Product Not Found.

post
/products/{id}/fields.json
Request samples
Payload
Content type
application/json

Copy
Expand allCollapse all
{
"field": {
"id": 0,
"value": "string",
"variants": []
}
}
Response samples
200404
Content type
application/json

Copy
Expand allCollapse all
{
"product": {
"id": 0,
"name": "string",
"page_title": "string",
"description": "string",
"type": "string",
"days_to_expire": 365,
"price": 0.1,
"discount": 0.1,
"weight": 1,
"stock": 100,
"stock_unlimited": true,
"stock_threshold": 0,
"stock_notification": true,
"cost_per_item": 0,
"compare_at_price": 0,
"sku": "string",
"brand": "string",
"barcode": "string",
"google_product_category": "string",
"featured": false,
"reviews_enabled": true,
"status": "available",
"created_at": "string",
"updated_at": "string",
"package_format": "box",
"length": 0.1,
"width": 0.1,
"height": 0.1,
"diameter": 0.1,
"permalink": "string",
"categories": [],
"images": [],
"variants": []
}
}
Count all Product Custom Fields.
Authorizations:
BasicAuthentication(loginParameterauthtokenParameter)
path Parameters
id
required
integer <int32>
Id of the Product

Responses
200 OK
404 Product Not Found.

get
/products/{id}/fields/count.json
Response samples
200404
Content type
application/json

Copy
{
"count": 0
}
Update value of Product Custom Field
Authorizations:
BasicAuthentication(loginParameterauthtokenParameter)
path Parameters
product_id
required
integer <int32>
Id of the Product.

field_id
required
integer <int32>
Id of the Custom Field Value.

Responses
200 OK
404 Product or Custom Field Value Not Found.

put
/products/{product_id}/fields/{field_id}.json
Response samples
200404
Content type
application/json

Copy
Expand allCollapse all
{
"field": {
"id": 0,
"custom_field_id": 0,
"type": "string",
"label": "string",
"value": "string",
"value_id": "string",
"variant_id": 0
}
}
Delete value of Product Custom Field
Authorizations:
BasicAuthentication(loginParameterauthtokenParameter)
path Parameters
product_id
required
integer <int32>
Id of the Product.

field_id
required
integer <int32>
Id of the Custom Field Value.

Responses
200 OK
404 Product or Custom Field Value Not Found.

delete
/products/{product_id}/fields/{field_id}.json
Response samples
200404
Content type
application/json

Copy
{
"message": "string"
}
Categories
Retrieve all Categories.
Authorizations:
BasicAuthentication(loginParameterauthtokenParameter)
Responses
200 OK

get
/categories.json
Response samples
200
Content type
application/json

Copy
Expand allCollapse all
{
"category": {
"id": 0,
"name": "string",
"parent_id": 0,
"permalink": "string"
}
}
Create a new Category.
Category's permalink is automatically generated from the given category's name.

Authorizations:
BasicAuthentication(loginParameterauthtokenParameter)
Request Body schema: application/json
required
Category parameters.

category	
object (CategoryEditFields)
Responses
200 OK

post
/categories.json
Request samples
Payload
Content type
application/json

Copy
Expand allCollapse all
{
"category": {
"name": "string",
"parent_id": 0
}
}
Response samples
200
Content type
application/json

Copy
Expand allCollapse all
{
"category": {
"id": 0,
"name": "string",
"parent_id": 0,
"permalink": "string"
}
}
Count all Categories.
Authorizations:
BasicAuthentication(loginParameterauthtokenParameter)
Responses
200 OK

get
/categories/count.json
Response samples
200
Content type
application/json

Copy
{
"count": 0
}
Retrieve a single Category.
Authorizations:
BasicAuthentication(loginParameterauthtokenParameter)
path Parameters
id
required
integer <int32>
Id of the Category

Responses
200 The selected Category.
404 Category Not Found.

get
/categories/{id}.json
Response samples
200404
Content type
application/json

Copy
Expand allCollapse all
{
"category": {
"id": 0,
"name": "string",
"parent_id": 0,
"permalink": "string"
}
}
Modify an existing Category.
Authorizations:
BasicAuthentication(loginParameterauthtokenParameter)
path Parameters
id
required
integer <int32>
Id of the Category

Request Body schema: application/json
required
Category parameters.

category	
object (CategoryEditFields)
Responses
200 OK
404 Category Not Found.

put
/categories/{id}.json
Request samples
Payload
Content type
application/json

Copy
Expand allCollapse all
{
"category": {
"name": "string",
"parent_id": 0
}
}
Response samples
200404
Content type
application/json

Copy
Expand allCollapse all
{
"category": {
"id": 0,
"name": "string",
"parent_id": 0,
"permalink": "string"
}
}
Delete an existing Category.
Authorizations:
BasicAuthentication(loginParameterauthtokenParameter)
path Parameters
id
required
integer <int32>
Id of the Category

Responses
200 OK
404 Category Not Found.

delete
/categories/{id}.json
Response samples
200404
Content type
application/json

Copy
"string"
Orders
Retrieve all Orders.
Authorizations:
BasicAuthentication(loginParameterauthtokenParameter)
query Parameters
limit	
integer <integer> <= 200
Default: 50
List restriction

page	
integer <integer>
Default: 1
List page

Responses
200 An array of Orders

get
/orders.json
Response samples
200
Content type
application/json

Copy
Expand allCollapse all
[
{
"order": {}
}
]
Create a new Order.
Orders created externally keep the given order product's values (bypassing internal promotion or product amounts).

Authorizations:
BasicAuthentication(loginParameterauthtokenParameter)
query Parameters
locale	
string <string>
Locale code of the translation

Request Body schema: application/json
required
Order parameters.

order	
object (OrderCreateFields)
Responses
200 OK

post
/orders.json
Request samples
Payload
Content type
application/json

Copy
Expand allCollapse all
{
"order": {
"status": "Abandoned",
"shipping_method_id": 0,
"shipping_method_name": "string",
"shipping_price": 0.1,
"shipping_required": true,
"allow_missing_products": true,
"customer": {},
"products": [],
"billing_information": {}
}
}
Response samples
200
Content type
application/json

Copy
Expand allCollapse all
{
"order": {
"id": 0,
"source": {},
"created_at": "string",
"completed_at": "string",
"currency": "string",
"subtotal": 0.1,
"tax": 0.1,
"shipping_tax": 0.1,
"shipping": 0.1,
"shipping_required": true,
"total": 0.1,
"discount": 0.1,
"shipping_discount": 0.1,
"gift_cards_discount": 0.1,
"fulfillment_status": "string",
"shipping_method_id": 0,
"shipping_service_id": 0,
"shipping_method_name": "string",
"payment_method_name": "string",
"payment_method_type": "string",
"payment_information": "string",
"additional_information": "string",
"duplicate_url": "string",
"recovery_url": "string",
"review_url": "string",
"checkout_url": "string",
"coupons": "string",
"promotions": [ ],
"customer": {},
"shipping_branch": {},
"shipping_address": {},
"billing_address": {},
"pickup_address": {},
"products": [],
"additional_fields": [],
"shipping_taxes": [],
"status": "Abandoned",
"status_name": "Abandoned",
"status_enum": "abandoned",
"tracking_url": "string",
"tracking_company": "string",
"tracking_number": "string",
"shipping_option": "delivery",
"same_day_delivery": false,
"shipment_status": "Delivered",
"shipment_status_enum": "delivered",
"recovered_from": 0,
"external_shipping_rate_id": "string",
"external_shipping_rate_description": "string",
"billing_information": {}
}
}
Count all Orders.
Authorizations:
BasicAuthentication(loginParameterauthtokenParameter)
Responses
200 OK

get
/orders/count.json
Response samples
200
Content type
application/json

Copy
{
"count": 0
}
Retrieve orders filtered by status.
Authorizations:
BasicAuthentication(loginParameterauthtokenParameter)
path Parameters
status
required
string
Enum: "abandoned" "canceled" "pending_payment" "paid"
Status of the Order used as filter

Responses
200 OK
404 Status Invalid.

get
/orders/status/{status}.json
Response samples
200404
Content type
application/json

Copy
Expand allCollapse all
[
{
"order": {}
}
]
Retrieve a single Order.
Authorizations:
BasicAuthentication(loginParameterauthtokenParameter)
path Parameters
id
required
integer <int32>
Id of the Order

Responses
200 OK
404 Order Not Found.

get
/orders/{id}.json
Response samples
200404
Content type
application/json

Copy
Expand allCollapse all
{
"order": {
"id": 0,
"source": {},
"created_at": "string",
"completed_at": "string",
"currency": "string",
"subtotal": 0.1,
"tax": 0.1,
"shipping_tax": 0.1,
"shipping": 0.1,
"shipping_required": true,
"total": 0.1,
"discount": 0.1,
"shipping_discount": 0.1,
"gift_cards_discount": 0.1,
"fulfillment_status": "string",
"shipping_method_id": 0,
"shipping_service_id": 0,
"shipping_method_name": "string",
"payment_method_name": "string",
"payment_method_type": "string",
"payment_information": "string",
"additional_information": "string",
"duplicate_url": "string",
"recovery_url": "string",
"review_url": "string",
"checkout_url": "string",
"coupons": "string",
"promotions": [ ],
"customer": {},
"shipping_branch": {},
"shipping_address": {},
"billing_address": {},
"pickup_address": {},
"products": [],
"additional_fields": [],
"shipping_taxes": [],
"status": "Abandoned",
"status_name": "Abandoned",
"status_enum": "abandoned",
"tracking_url": "string",
"tracking_company": "string",
"tracking_number": "string",
"shipping_option": "delivery",
"same_day_delivery": false,
"shipment_status": "Delivered",
"shipment_status_enum": "delivered",
"recovered_from": 0,
"external_shipping_rate_id": "string",
"external_shipping_rate_description": "string",
"billing_information": {}
}
}
Modify an existing Order.
Only status, shipment_status, tracking_number, tracking_company, tracking_url, additional_information and additional_fields are available for update. An email is send if shipment_status changes.

Authorizations:
BasicAuthentication(loginParameterauthtokenParameter)
path Parameters
id
required
integer <int32>
Id of the Order

Request Body schema: application/json
required
Order parameters to change

order	
object (OrderEditFields)
Responses
200 OK
404 Order Not Found.

put
/orders/{id}.json
Request samples
Payload
Content type
application/json

Copy
Expand allCollapse all
{
"order": {
"status": "Abandoned",
"shipment_status": "requested",
"tracking_number": "string",
"tracking_company": "string",
"tracking_url": "string",
"additional_information": "string",
"additional_fields": []
}
}
Response samples
200404
Content type
application/json

Copy
Expand allCollapse all
{
"order": {
"id": 0,
"source": {},
"created_at": "string",
"completed_at": "string",
"currency": "string",
"subtotal": 0.1,
"tax": 0.1,
"shipping_tax": 0.1,
"shipping": 0.1,
"shipping_required": true,
"total": 0.1,
"discount": 0.1,
"shipping_discount": 0.1,
"gift_cards_discount": 0.1,
"fulfillment_status": "string",
"shipping_method_id": 0,
"shipping_service_id": 0,
"shipping_method_name": "string",
"payment_method_name": "string",
"payment_method_type": "string",
"payment_information": "string",
"additional_information": "string",
"duplicate_url": "string",
"recovery_url": "string",
"review_url": "string",
"checkout_url": "string",
"coupons": "string",
"promotions": [ ],
"customer": {},
"shipping_branch": {},
"shipping_address": {},
"billing_address": {},
"pickup_address": {},
"products": [],
"additional_fields": [],
"shipping_taxes": [],
"status": "Abandoned",
"status_name": "Abandoned",
"status_enum": "abandoned",
"tracking_url": "string",
"tracking_company": "string",
"tracking_number": "string",
"shipping_option": "delivery",
"same_day_delivery": false,
"shipment_status": "Delivered",
"shipment_status_enum": "delivered",
"recovered_from": 0,
"external_shipping_rate_id": "string",
"external_shipping_rate_description": "string",
"billing_information": {}
}
}
Retrieve an Orders List from a query.
Endpoint example:

 https://api.jumpseller.com/v1/orders/search.json?fulfillment_filters=unfulfilled,fulfilled&status_filters[]=paid&status_filters[]=abandoned&dateFilter=last7days 
Authorizations:
BasicAuthentication(loginParameterauthtokenParameter)
query Parameters
locale	
string <string>
Locale code of the translation

query	
string <string>
Text to query for the Order

status_filters[]	
string <string>
Enum: "paid" "created" "pending_payment" "canceled" "abandoned"
Order Status to query for the Order

fulfillment_filters	
string <string>
Enum: "unfulfilled" "fulfilled"
Comma separated values of the fulfillment filters to query for the Order

dateFilter	
string <string>
Enum: "today" "yesterday" "last30days" "last7days" "last90days" "customDate"
Date to query for the Order.

initialDate	
string <string>
Starting date to query for the Order in the format YYYY-MM-DD. CustomDate and finalDate need to be used

finalDate	
string <string>
Starting date to query for the Order in the format YYYY-MM-DD. CustomDate and initialDate need to be used

fields	
string <string>
Enum: "id" "tax" "..."
Comma separated values of the fields to query for the Order

Responses
200 An array of orders
404 Invalid query.

get
/orders/search.json
Response samples
200404
Content type
application/json

Copy
Expand allCollapse all
[
{
"order": {}
}
]
Retrieve orders filtered by Order Id.
For example the GET /orders/after/5000 will return Order 5001, 5002, 5003, etc.

Authorizations:
BasicAuthentication(loginParameterauthtokenParameter)
path Parameters
id
required
integer <int32>
Id of the Order

Responses
200 OK
404 Order Not Found.

get
/orders/after/{id}.json
Response samples
200404
Content type
application/json

Copy
Expand allCollapse all
{
"order": {
"id": 0,
"source": {},
"created_at": "string",
"completed_at": "string",
"currency": "string",
"subtotal": 0.1,
"tax": 0.1,
"shipping_tax": 0.1,
"shipping": 0.1,
"shipping_required": true,
"total": 0.1,
"discount": 0.1,
"shipping_discount": 0.1,
"gift_cards_discount": 0.1,
"fulfillment_status": "string",
"shipping_method_id": 0,
"shipping_service_id": 0,
"shipping_method_name": "string",
"payment_method_name": "string",
"payment_method_type": "string",
"payment_information": "string",
"additional_information": "string",
"duplicate_url": "string",
"recovery_url": "string",
"review_url": "string",
"checkout_url": "string",
"coupons": "string",
"promotions": [ ],
"customer": {},
"shipping_branch": {},
"shipping_address": {},
"billing_address": {},
"pickup_address": {},
"products": [],
"additional_fields": [],
"shipping_taxes": [],
"status": "Abandoned",
"status_name": "Abandoned",
"status_enum": "abandoned",
"tracking_url": "string",
"tracking_company": "string",
"tracking_number": "string",
"shipping_option": "delivery",
"same_day_delivery": false,
"shipment_status": "Delivered",
"shipment_status_enum": "delivered",
"recovered_from": 0,
"external_shipping_rate_id": "string",
"external_shipping_rate_description": "string",
"billing_information": {}
}
}
Retrieve all Order History.
Authorizations:
BasicAuthentication(loginParameterauthtokenParameter)
path Parameters
id
required
integer <int32>
Id of the Order

Responses
200 An array with Order History

get
/orders/{id}/history.json
Response samples
200
Content type
application/json

Copy
Expand allCollapse all
[
{
"order_history": {}
}
]
Create a new Order History Entry.
Authorizations:
BasicAuthentication(loginParameterauthtokenParameter)
path Parameters
id
required
integer <int32>
Id of the OrderHistory

Request Body schema: application/json
required
Order History parameters.

order_history	
object (OrderHistoryEditFields)
Responses
200 OK

post
/orders/{id}/history.json
Request samples
Payload
Content type
application/json

Copy
Expand allCollapse all
{
"order_history": {
"message": "string"
}
}
Response samples
200
Content type
application/json

Copy
Expand allCollapse all
{
"order_history": {
"id": 0,
"message": "string",
"created_at": "string"
}
}
Retrieve all Documents from an Order.
Authorizations:
BasicAuthentication(loginParameterauthtokenParameter)
path Parameters
id
required
integer <int32>
Id of the Order

Responses
200 An array with Documents

get
/orders/{id}/documents.json
Response samples
200
Content type
application/json

Copy
Expand allCollapse all
[
{
"document": {}
}
]
Create a new Order Document Entry.
Authorizations:
BasicAuthentication(loginParameterauthtokenParameter)
path Parameters
id
required
integer <int32>
Id of the Order

Request Body schema: application/json
required
Document parameters.

document	
object (DocumentFields)
Responses
200 OK

post
/orders/{id}/documents.json
Request samples
Payload
Content type
application/json

Copy
Expand allCollapse all
{
"document": {
"document_type": "0 - credit note",
"external_id": "string",
"public_id": "string",
"url": "string",
"order_id": 0,
"store_id": 0,
"app_code": "string"
}
}
Response samples
200
Content type
application/json

Copy
Expand allCollapse all
{
"document": {
"document_type": "0 - credit note",
"external_id": "string",
"public_id": "string",
"url": "string",
"order_id": 0,
"store_id": 0,
"app_code": "string"
}
}
Update a Document from an Order.
Authorizations:
BasicAuthentication(loginParameterauthtokenParameter)
path Parameters
id
required
integer <int32>
Id of the Order

public_id
required
integer <int32>
Public Id of the Document

Request Body schema: application/json
required
Document parameters.

document_type	
integer
Enum: "0 - credit note" "1 - invoice"
Type of Document

external_id	
string
Document ID on the external service

public_id	
string
Human recognizable document ID

url	
string
Document url

Responses
200 OK
404 Document Not Found.

put
/orders/{id}/documents/{public_id}.json
Request samples
Payload
Content type
application/json

Copy
{
"document_type": "0 - credit note",
"external_id": "string",
"public_id": "string",
"url": "string"
}
Response samples
200404
Content type
application/json

Copy
Expand allCollapse all
{
"document": {
"document_type": "0 - credit note",
"external_id": "string",
"public_id": "string",
"url": "string",
"order_id": 0,
"store_id": 0,
"app_code": "string"
}
}
Delete a Document from an Order.
Authorizations:
BasicAuthentication(loginParameterauthtokenParameter)
path Parameters
id
required
integer <int32>
Id of the Order

public_id
required
integer <int32>
Public Id of the Document

Responses
200 OK
404 Page Not Found.

delete
/orders/{id}/documents/{public_id}.json
Response samples
200404
Content type
application/json

Copy
"string"
Fulfillments
Count all Fulfillments.
Authorizations:
BasicAuthentication(loginParameterauthtokenParameter)
Responses
200 OK

get
/fulfillments/count.json
Response samples
200
Content type
application/json

Copy
{
"count": 0
}
Retrieve all Fulfillments.
Authorizations:
BasicAuthentication(loginParameterauthtokenParameter)
query Parameters
limit	
integer <integer> <= 200
Default: 50
List restriction

page	
integer <integer>
Default: 1
List page

Responses
200 An array of Fulfillments

get
/fulfillments.json
Response samples
200
Content type
application/json

Copy
Expand allCollapse all
[
{
"fulfillment": {}
}
]
Create a new Fulfillment.
Authorizations:
BasicAuthentication(loginParameterauthtokenParameter)
Request Body schema: application/json
required
Fulfillment parameters.

fulfillment	
object (FulfillmentCreateFields)
Responses
200 OK

post
/fulfillments.json
Request samples
Payload
Content type
application/json

Copy
Expand allCollapse all
{
"fulfillment": {
"shipment_status": "requested",
"order_id": "string",
"type": "manual",
"tracking_number": "string",
"tracking_company": "string",
"tracking_url": "string",
"external_id": "string",
"service_type": "string",
"expected_arrival_from": "string",
"expected_arrival_to": "string",
"send_email": true
}
}
Response samples
200
Content type
application/json

Copy
Expand allCollapse all
{
"fulfillment": {
"id": 0,
"created_at": "string",
"updated_at": "string",
"tracking_number": "string",
"tracking_company": "string",
"type": "string",
"shipment_status": "string",
"label_url": "string",
"expected_arrival_from": "string",
"expected_arrival_to": "string",
"fulfillment_address": {},
"order_id": 0,
"order": {}
}
}
Retrieve a single Fulfillment.
Authorizations:
BasicAuthentication(loginParameterauthtokenParameter)
path Parameters
id
required
integer <int32>
Id of the Fulfillment

Responses
200 OK
404 Fulfillment Not Found.

get
/fulfillments/{id}.json
Response samples
200404
Content type
application/json

Copy
Expand allCollapse all
{
"fulfillment": {
"id": 0,
"created_at": "string",
"updated_at": "string",
"tracking_number": "string",
"tracking_company": "string",
"type": "string",
"shipment_status": "string",
"label_url": "string",
"expected_arrival_from": "string",
"expected_arrival_to": "string",
"fulfillment_address": {},
"order_id": 0,
"order": {}
}
}
Modify an existing Fulfillment.
Authorizations:
BasicAuthentication(loginParameterauthtokenParameter)
path Parameters
id
required
integer <int32>
Id of the Fulfillment

Request Body schema: application/json
required
Fulfillment parameters to change

fulfillment	
object (FulfillmentEditFields)
Responses
200 OK
404 Fulfillment Not Found.

put
/fulfillments/{id}.json
Request samples
Payload
Content type
application/json

Copy
Expand allCollapse all
{
"fulfillment": {
"shipment_status": "requested",
"type": "manual",
"tracking_number": "string",
"tracking_company": "string",
"tracking_url": "string",
"external_id": "string",
"service_type": "string",
"expected_arrival_from": "string",
"expected_arrival_to": "string"
}
}
Response samples
200404
Content type
application/json

Copy
Expand allCollapse all
{
"fulfillment": {
"id": 0,
"created_at": "string",
"updated_at": "string",
"tracking_number": "string",
"tracking_company": "string",
"type": "string",
"shipment_status": "string",
"label_url": "string",
"expected_arrival_from": "string",
"expected_arrival_to": "string",
"fulfillment_address": {},
"order_id": 0,
"order": {}
}
}
Retrieve the Fulfillments associated with the Order.
Authorizations:
BasicAuthentication(loginParameterauthtokenParameter)
path Parameters
id
required
integer <int32>
Id of the Order

Responses
200 OK
404 Fulfillment Not Found.

get
/order/{id}/fulfillments.json
Response samples
200404
Content type
application/json

Copy
Expand allCollapse all
[
{
"fulfillment": {}
}
]
Pages
Retrieve all Pages.
Authorizations:
BasicAuthentication(loginParameterauthtokenParameter)
query Parameters
limit	
integer <integer> <= 200
Default: 50
List restriction

page	
integer <integer>
Default: 1
List page

Responses
200 An array of Pages

get
/pages.json
Response samples
200
Content type
application/json

Copy
Expand allCollapse all
[
{
"page": {}
}
]
Create a new Page.
Authorizations:
BasicAuthentication(loginParameterauthtokenParameter)
Request Body schema: application/json
required
Page parameters.

page	
object (PageModifyFields)
Responses
200 OK

post
/pages.json
Request samples
Payload
Content type
application/json

Copy
Expand allCollapse all
{
"page": {
"title": "string",
"body": "string",
"status": "public",
"page_title": "string",
"meta_description": "string",
"categories": [],
"template": 0,
"permalink": "string",
"image": {}
}
}
Response samples
200
Content type
application/json

Copy
Expand allCollapse all
{
"page": {
"id": 0,
"title": "string",
"body": "string",
"status": "public",
"legal": true,
"page_title": "string",
"meta_description": "string",
"categories": [],
"template": {},
"permalink": "string",
"image": {}
}
}
Count all Pages.
Authorizations:
BasicAuthentication(loginParameterauthtokenParameter)
Responses
200 Total number of pages

get
/pages/count.json
Response samples
200
Content type
application/json

Copy
{
"count": 0
}
Retrieve a single Page by id.
Authorizations:
BasicAuthentication(loginParameterauthtokenParameter)
path Parameters
id
required
integer <int32>
Id of the Page

Responses
200 OK
404 Page Not Found.

get
/pages/{id}.json
Response samples
200404
Content type
application/json

Copy
Expand allCollapse all
{
"page": {
"id": 0,
"title": "string",
"body": "string",
"status": "public",
"legal": true,
"page_title": "string",
"meta_description": "string",
"categories": [],
"template": {},
"permalink": "string",
"image": {}
}
}
Update a Page.
Authorizations:
BasicAuthentication(loginParameterauthtokenParameter)
path Parameters
id
required
integer <int32>
Id of the Page

Request Body schema: application/json
required
Page parameters.

page	
object (PageModifyFields)
Responses
200 OK
404 Page Not Found.

put
/pages/{id}.json
Request samples
Payload
Content type
application/json

Copy
Expand allCollapse all
{
"page": {
"title": "string",
"body": "string",
"status": "public",
"page_title": "string",
"meta_description": "string",
"categories": [],
"template": 0,
"permalink": "string",
"image": {}
}
}
Response samples
200404
Content type
application/json

Copy
Expand allCollapse all
{
"page": {
"id": 0,
"title": "string",
"body": "string",
"status": "public",
"legal": true,
"page_title": "string",
"meta_description": "string",
"categories": [],
"template": {},
"permalink": "string",
"image": {}
}
}
Delete an existing Page.
Authorizations:
BasicAuthentication(loginParameterauthtokenParameter)
path Parameters
id
required
integer <int32>
Id of the Page

Responses
200 OK
404 Page Not Found.

delete
/pages/{id}.json
Response samples
200404
Content type
application/json

Copy
"string"
Customers
Retrieve all Customers.
Authorizations:
BasicAuthentication(loginParameterauthtokenParameter)
query Parameters
limit	
integer <integer> <= 200
Default: 50
List restriction

page	
integer <integer>
Default: 1
List page

Responses
200 An array of Orders

get
/customers.json
Response samples
200
Content type
application/json

Copy
Expand allCollapse all
[
{
"customer": {}
}
]
Create a new Customer.
Authorizations:
BasicAuthentication(loginParameterauthtokenParameter)
Request Body schema: application/json
required
Customer parameters.

customer	
object (CustomerFieldsWithPasswordNoID)
Responses
200 OK
404 Customer Not Found.

post
/customers.json
Request samples
Payload
Content type
application/json

Copy
Expand allCollapse all
{
"customer": {
"email": "string",
"phone": "string",
"password": "string",
"status": "approved",
"shipping_address": {},
"billing_address": {},
"customer_category": []
}
}
Response samples
200404
Content type
application/json

Copy
Expand allCollapse all
{
"customer": {
"id": 0,
"email": "string",
"phone": "string",
"fullname": "string",
"status": "approved",
"accepts_marketing": false,
"accepted_marketing_at": "string",
"cancelled_marketing_at": "string",
"shipping_address": {},
"billing_address": {},
"customer_categories": [],
"customer_additional_fields": []
}
}
Count all Customers.
Authorizations:
BasicAuthentication(loginParameterauthtokenParameter)
Responses
200 OK

get
/customers/count.json
Response samples
200
Content type
application/json

Copy
{
"count": 0
}
Retrieve a single Customer by email.
Authorizations:
BasicAuthentication(loginParameterauthtokenParameter)
path Parameters
email
required
string
Email of the Customer

Responses
200 OK
404 Customer Not Found.

get
/customers/email/{email}.json
Response samples
200404
Content type
application/json

Copy
Expand allCollapse all
{
"customer": {
"id": 0,
"email": "string",
"phone": "string",
"fullname": "string",
"status": "approved",
"accepts_marketing": false,
"accepted_marketing_at": "string",
"cancelled_marketing_at": "string",
"shipping_address": {},
"billing_address": {},
"customer_categories": [],
"customer_additional_fields": []
}
}
Retrieve all orders of single Customer
Authorizations:
BasicAuthentication(loginParameterauthtokenParameter)
path Parameters
id
required
integer
ID of the Customer

query Parameters
limit	
integer <integer> <= 200
Default: 50
List restriction

page	
integer <integer>
Default: 1
List page

Responses
200 An array of Orders
404 Customer Not Found.

get
/customers/{id}/orders.json
Response samples
200404
Content type
application/json

Copy
Expand allCollapse all
[
{
"order": {}
}
]
Retrieve all orders of single Customer
Authorizations:
BasicAuthentication(loginParameterauthtokenParameter)
path Parameters
id
required
integer
ID of the Customer

status
required
string
Enum: "Abandoned" "Canceled" "Pending Payment" "Paid"
Status of the Order used as filter

query Parameters
limit	
integer <integer> <= 200
Default: 50
List restriction

page	
integer <integer>
Default: 1
List page

Responses
200 An array of Orders
404 Customer Not Found.

get
/customers/{id}/orders/status/{status}.json
Response samples
200404
Content type
application/json

Copy
Expand allCollapse all
[
{
"order": {}
}
]
Retrieve a single Customer by id.
Authorizations:
BasicAuthentication(loginParameterauthtokenParameter)
path Parameters
id
required
integer <int32>
Id of the Customer

Responses
200 OK
404 Customer Not Found.

get
/customers/{id}.json
Response samples
200404
Content type
application/json

Copy
Expand allCollapse all
{
"customer": {
"id": 0,
"email": "string",
"phone": "string",
"fullname": "string",
"status": "approved",
"accepts_marketing": false,
"accepted_marketing_at": "string",
"cancelled_marketing_at": "string",
"shipping_address": {},
"billing_address": {},
"customer_categories": [],
"customer_additional_fields": []
}
}
Update a new Customer.
Authorizations:
BasicAuthentication(loginParameterauthtokenParameter)
path Parameters
id
required
integer <int32>
Id of the Customer

Request Body schema: application/json
required
Customer parameters.

customer	
object (CustomerFieldsWithPasswordNoID)
Responses
200 OK
404 Customer Not Found.

put
/customers/{id}.json
Request samples
Payload
Content type
application/json

Copy
Expand allCollapse all
{
"customer": {
"email": "string",
"phone": "string",
"password": "string",
"status": "approved",
"shipping_address": {},
"billing_address": {},
"customer_category": []
}
}
Response samples
200404
Content type
application/json

Copy
Expand allCollapse all
{
"customer": {
"id": 0,
"email": "string",
"phone": "string",
"fullname": "string",
"status": "approved",
"accepts_marketing": false,
"accepted_marketing_at": "string",
"cancelled_marketing_at": "string",
"shipping_address": {},
"billing_address": {},
"customer_categories": [],
"customer_additional_fields": []
}
}
Delete an existing Customer.
Authorizations:
BasicAuthentication(loginParameterauthtokenParameter)
path Parameters
id
required
integer <int32>
Id of the Customer

Responses
200 OK
404 Customer Not Found.

delete
/customers/{id}.json
Response samples
200404
Content type
application/json

Copy
"string"
Retrieve a Customer List from a query.
Endpoint example:

https://api.jumpseller.com/v1/customers/search.json?query=test&order=desc,description 
Authorizations:
BasicAuthentication(loginParameterauthtokenParameter)
query Parameters
query
required
string <string>
Text to query for the Customer. If empty return all customers.

order	
string <string>
Default: "asc"
Sort Customers by creation date, 'asc' for ascending order or 'desc' for descending order.

limit	
integer <integer> <= 200
Default: 50
List restriction

page	
integer <integer>
Default: 1
List page

Responses
200 An array of Customers

get
/customers/search.json
Response samples
200
Content type
application/json

Copy
Expand allCollapse all
[
{
"customer": {}
}
]
Customer Categories
Retrieve all Customer Categories.
Authorizations:
BasicAuthentication(loginParameterauthtokenParameter)
query Parameters
limit	
integer <integer> <= 200
Default: 50
List restriction

page	
integer <integer>
Default: 1
List page

Responses
200 An array of Customer Categories

get
/customer_categories.json
Response samples
200
Content type
application/json

Copy
Expand allCollapse all
[
{
"customer_category": {}
}
]
Create a new CustomerCategory.
Authorizations:
BasicAuthentication(loginParameterauthtokenParameter)
Request Body schema: application/json
required
CustomerCategory parameters.

customer_category	
object (CustomerCategoryEditFields)
Responses
200 OK
404 CustomerCategory Not Found.

post
/customer_categories.json
Request samples
Payload
Content type
application/json

Copy
Expand allCollapse all
{
"customer_category": {
"name": "string"
}
}
Response samples
200404
Content type
application/json

Copy
Expand allCollapse all
{
"customer_category": {
"id": 0,
"name": "string",
"code": "string"
}
}
Retrieve a single CustomerCategory.
Authorizations:
BasicAuthentication(loginParameterauthtokenParameter)
path Parameters
id
required
integer <int32>
Id of the CustomerCategory

Responses
200 OK
404 CustomerCategory Not Found.

get
/customer_categories/{id}.json
Response samples
200404
Content type
application/json

Copy
Expand allCollapse all
{
"customer_category": {
"id": 0,
"name": "string",
"code": "string"
}
}
Update a CustomerCategory.
Authorizations:
BasicAuthentication(loginParameterauthtokenParameter)
path Parameters
id
required
integer <int32>
Id of the CustomerCategory

Request Body schema: application/json
required
CustomerCategory parameters.

customer_category	
object (CustomerCategoryEditFields)
Responses
200 OK
404 CustomerCategory Not Found.

put
/customer_categories/{id}.json
Request samples
Payload
Content type
application/json

Copy
Expand allCollapse all
{
"customer_category": {
"name": "string"
}
}
Response samples
200404
Content type
application/json

Copy
Expand allCollapse all
{
"customer_category": {
"id": 0,
"name": "string",
"code": "string"
}
}
Delete an existing CustomerCategory.
Authorizations:
BasicAuthentication(loginParameterauthtokenParameter)
path Parameters
id
required
integer <int32>
Id of the CustomerCategory

Responses
200 OK
404 CustomerCategory Not Found.

delete
/customer_categories/{id}.json
Response samples
200404
Content type
application/json

Copy
"string"
Retrieves the customers in a CustomerCategory.
Authorizations:
BasicAuthentication(loginParameterauthtokenParameter)
path Parameters
id
required
integer <int32>
Id of the CustomerCategory

Responses
200 OK
404 CustomerCategory Not Found.

get
/customer_categories/{id}/customers.json
Response samples
200404
Content type
application/json

Copy
Expand allCollapse all
[
{
"customer": {}
}
]
Adds Customers to a CustomerCategory.
Authorizations:
BasicAuthentication(loginParameterauthtokenParameter)
path Parameters
id
required
integer <int32>
Id of the CustomerCategory

Request Body schema: application/json
required
Customer parameters.

customers	
Array of objects (CustomerToCustomerCategory)
Responses
200 Array of Customers in the Customer Category
404 CustomerCategory Not Found.

post
/customer_categories/{id}/customers.json
Request samples
Payload
Content type
application/json

Copy
Expand allCollapse all
{
"customers": [
{}
]
}
Response samples
200404
Content type
application/json

Copy
Expand allCollapse all
[
{
"customer": {}
}
]
Delete Customer from an existing CustomerCategory.
Authorizations:
BasicAuthentication(loginParameterauthtokenParameter)
path Parameters
id
required
integer <int32>
Id of the CustomerCategory

customer_id
required
integer <int32>
Id of the Customer

Responses
200 OK
404 CustomerCategory or Customer Not Found.

delete
/customer_categories/{id}/customers/{customer_id}.json
Response samples
200404
Content type
application/json

Copy
"string"
Customer Additional Fields
Retrieves the Customer Additional Field of a Customer.
Authorizations:
BasicAuthentication(loginParameterauthtokenParameter)
path Parameters
id
required
integer <int32>
Id of the Customer

Responses
200 OK
404 Customer Not Found.

get
/customers/{id}/fields
Response samples
200404
Content type
application/json

Copy
Expand allCollapse all
[
{
"customer_additional_field": {}
}
]
Adds Customer Additional Fields to a Customer.
Authorizations:
BasicAuthentication(loginParameterauthtokenParameter)
path Parameters
id
required
integer <int32>
Id of the Customer

Request Body schema: application/json
required
Customer Additional Field parameters.

customer_additional_field	
object (CustomerAdditionalFieldEditFields)
Responses
200 OK
404 Customer Additional Field Not Found.

post
/customers/{id}/fields
Request samples
Payload
Content type
application/json

Copy
Expand allCollapse all
{
"customer_additional_field": {
"value": "string",
"checkout_custom_field_id": 0
}
}
Response samples
200404
Content type
application/json

Copy
Expand allCollapse all
{
"customer_additional_field": {
"id": 0,
"label": "string",
"value": "string",
"area": "string",
"customer_id": 0,
"checkout_custom_field_id": 0
}
}
Retrieve a single Customer Additional Field.
Authorizations:
BasicAuthentication(loginParameterauthtokenParameter)
path Parameters
id
required
integer <int32>
Id of the Customer

field_id
required
integer <int32>
Id of the Customer Additional Field

Responses
200 OK
404 Customer Not Found.

get
/customers/{id}/fields/{field_id}
Response samples
200404
Content type
application/json

Copy
Expand allCollapse all
{
"customer_additional_field": {
"id": 0,
"label": "string",
"value": "string",
"area": "string",
"customer_id": 0,
"checkout_custom_field_id": 0
}
}
Update a Customer Additional Field.
Authorizations:
BasicAuthentication(loginParameterauthtokenParameter)
path Parameters
id
required
integer <int32>
Id of the Customer

field_id
required
integer <int32>
Id of the Customer Additional Field

Request Body schema: application/json
required
Customer Additional Field parameters.

customer_additional_field	
object (CustomerAdditionalFieldEditFields)
Responses
200 OK
400 Customer Additional Field Bad Parameters.
404 Customer Additional Field Not Found.

put
/customers/{id}/fields/{field_id}
Request samples
Payload
Content type
application/json

Copy
Expand allCollapse all
{
"customer_additional_field": {
"value": "string",
"checkout_custom_field_id": 0
}
}
Response samples
200400404
Content type
application/json

Copy
Expand allCollapse all
{
"customer_additional_field": {
"id": 0,
"label": "string",
"value": "string",
"area": "string",
"customer_id": 0,
"checkout_custom_field_id": 0
}
}
Delete a Customer Additional Field.
Authorizations:
BasicAuthentication(loginParameterauthtokenParameter)
path Parameters
id
required
integer <int32>
Id of the Customer

field_id
required
integer <int32>
Id of the Customer Additional Field

Responses
200 OK
404 Customer Not Found.

delete
/customers/{id}/fields/{field_id}
Response samples
200404
Content type
application/json

Copy
"string"
Promotions
Retrieve all Promotions.
Authorizations:
BasicAuthentication(loginParameterauthtokenParameter)
query Parameters
limit	
integer <integer>
Promotions' list restriction (default: 50 | max: 200).

page	
integer <integer>
Promotions' list page (default: 1).

Responses
200 An array of Promotions

get
/promotions.json
Response samples
200
Content type
application/json

Copy
Expand allCollapse all
[
{
"promotion": {}
}
]
Create a new Promotion.
Authorizations:
BasicAuthentication(loginParameterauthtokenParameter)
Request Body schema: application/json
required
Promotion parameters.

promotion	
object (PromotionEditFields)
Responses
200 OK
404 Promotion Not Found.

post
/promotions.json
Request samples
Payload
Content type
application/json

Copy
Expand allCollapse all
{
"promotion": {
"name": "string",
"enabled": true,
"discount_target": "string",
"buys_at_least": "string",
"condition_price": 0.1,
"condition_qty": 0,
"quantity_x": 0,
"type": "string",
"discount_amount_fix": 0.1,
"discount_amount_percent": 0.1,
"lasts": "string",
"begins_at": "string",
"expires_at": "string",
"max_times_used": 0,
"cumulative": false,
"customers": "string",
"categories": [],
"categories_x": [],
"customer_categories": [],
"products": [],
"products_x": [],
"coupons": [],
"countries": [],
"regions": [],
"municipalities": []
}
}
Response samples
200404
Content type
application/json

Copy
Expand allCollapse all
{
"promotion": {
"id": 0,
"name": "string",
"status": "string",
"enabled": true,
"discount_target": "string",
"condition_price": 0.1,
"condition_qty": 0,
"quantity_x": 0,
"discount_amount_fix": 0.1,
"discount_amount_percent": 0.1,
"lasts": "string",
"begins_at": "string",
"expires_at": "string",
"times_used": 0,
"max_times_used": 0,
"cumulative": false,
"categories": [],
"customer_categories": [],
"products": [],
"products_x": [],
"coupons": [],
"countries": [],
"regions": [],
"municipalities": []
}
}
Retrieve a single Promotion.
Authorizations:
BasicAuthentication(loginParameterauthtokenParameter)
path Parameters
id
required
integer <int32>
Id of the Promotion

Responses
200 OK
404 Promotion Not Found.

get
/promotions/{id}.json
Response samples
200404
Content type
application/json

Copy
Expand allCollapse all
{
"promotion": {
"id": 0,
"name": "string",
"status": "string",
"enabled": true,
"discount_target": "string",
"condition_price": 0.1,
"condition_qty": 0,
"quantity_x": 0,
"discount_amount_fix": 0.1,
"discount_amount_percent": 0.1,
"lasts": "string",
"begins_at": "string",
"expires_at": "string",
"times_used": 0,
"max_times_used": 0,
"cumulative": false,
"categories": [],
"customer_categories": [],
"products": [],
"products_x": [],
"coupons": [],
"countries": [],
"regions": [],
"municipalities": []
}
}
Update a Promotion.
Authorizations:
BasicAuthentication(loginParameterauthtokenParameter)
path Parameters
id
required
integer <int32>
Id of the Promotion

Request Body schema: application/json
required
Promotion parameters.

promotion	
object (PromotionEditFields)
Responses
200 OK
404 Promotion Not Found.

put
/promotions/{id}.json
Request samples
Payload
Content type
application/json

Copy
Expand allCollapse all
{
"promotion": {
"name": "string",
"enabled": true,
"discount_target": "string",
"buys_at_least": "string",
"condition_price": 0.1,
"condition_qty": 0,
"quantity_x": 0,
"type": "string",
"discount_amount_fix": 0.1,
"discount_amount_percent": 0.1,
"lasts": "string",
"begins_at": "string",
"expires_at": "string",
"max_times_used": 0,
"cumulative": false,
"customers": "string",
"categories": [],
"categories_x": [],
"customer_categories": [],
"products": [],
"products_x": [],
"coupons": [],
"countries": [],
"regions": [],
"municipalities": []
}
}
Response samples
200404
Content type
application/json

Copy
Expand allCollapse all
{
"promotion": {
"id": 0,
"name": "string",
"status": "string",
"enabled": true,
"discount_target": "string",
"condition_price": 0.1,
"condition_qty": 0,
"quantity_x": 0,
"discount_amount_fix": 0.1,
"discount_amount_percent": 0.1,
"lasts": "string",
"begins_at": "string",
"expires_at": "string",
"times_used": 0,
"max_times_used": 0,
"cumulative": false,
"categories": [],
"customer_categories": [],
"products": [],
"products_x": [],
"coupons": [],
"countries": [],
"regions": [],
"municipalities": []
}
}
Delete an existing Promotion.
Authorizations:
BasicAuthentication(loginParameterauthtokenParameter)
path Parameters
id
required
integer <int32>
Id of the Promotion

Responses
200 OK
404 Promotion Not Found.

delete
/promotions/{id}.json
Response samples
200404
Content type
application/json

Copy
"string"
Payment Methods
Retrieve all Store's Payment Methods.
Authorizations:
BasicAuthentication(loginParameterauthtokenParameter)
Responses
200 An array of Payment Methods

get
/payment_methods.json
Response samples
200
Content type
application/json

Copy
Expand allCollapse all
[
{
"payment_method": {}
}
]
Retrieve a single Payment Method.
Authorizations:
BasicAuthentication(loginParameterauthtokenParameter)
path Parameters
id
required
integer <int32>
Id of the Payment Method

Responses
200 OK
404 PaymentMethod Not Found.

get
/payment_methods/{id}.json
Response samples
200404
Content type
application/json

Copy
Expand allCollapse all
{
"payment_method": {
"id": 0,
"type": "manual",
"name": "string"
}
}
Shipping Methods
Retrieve all Store's Shipping Methods.
Authorizations:
BasicAuthentication(loginParameterauthtokenParameter)
path Parameters
enabled	
boolean
If shipping method is enabled

Responses
200 An array of Shipping Methods

get
/shipping_methods.json
Response samples
200
Content type
application/json

Copy
Expand allCollapse all
[
{
"shipping_method": {}
}
]
Creates a Shipping Method.
Authorizations:
BasicAuthentication(loginParameterauthtokenParameter)
Request Body schema: application/json
required
Shipping Method parameters.

shipping_method	
object
Responses
200 OK
404 ShippingMethod Not Found.

post
/shipping_methods.json
Request samples
Payload
Content type
application/json

Copy
Expand allCollapse all
{
"shipping_method": {
"name": "string",
"callback_url": "string",
"fetch_services_url": "string",
"token": "string",
"state": "string",
"city": "string",
"postal": "string"
}
}
Response samples
200404
Content type
application/json

Copy
Expand allCollapse all
{
"shipping_method": {
"id": 0,
"type": "free",
"name": "string",
"enabled": true,
"free_shipping": true,
"free_shipping_minimum_purchase": true,
"fee": [],
"callback_url": "string",
"fetch_services_url": "string",
"state": "string",
"city": "string",
"postal": "string",
"services": [],
"tables": []
}
}
Retrieve a single Shipping Method.
Authorizations:
BasicAuthentication(loginParameterauthtokenParameter)
path Parameters
id
required
integer <int32>
Id of the Shipping Method

Responses
200 OK
404 ShippingMethod Not Found.

get
/shipping_methods/{id}.json
Response samples
200404
Content type
application/json

Copy
Expand allCollapse all
{
"shipping_method": {
"id": 0,
"type": "free",
"name": "string",
"enabled": true,
"free_shipping": true,
"free_shipping_minimum_purchase": true,
"fee": [],
"callback_url": "string",
"fetch_services_url": "string",
"state": "string",
"city": "string",
"postal": "string",
"services": [],
"tables": []
}
}
Update a Shipping Method.
Authorizations:
BasicAuthentication(loginParameterauthtokenParameter)
path Parameters
id
required
integer <int32>
Id of the Shipping Method

Request Body schema: application/json
required
Shipping Method parameters.

shipping_method	
object
Responses
200 OK
404 Shipping Method Not Found.

put
/shipping_methods/{id}.json
Request samples
Payload
Content type
application/json

Copy
Expand allCollapse all
{
"shipping_method": {
"name": "string",
"callback_url": "string",
"fetch_services_url": "string",
"token": "string",
"state": "string",
"city": "string",
"postal": "string"
}
}
Response samples
200404
Content type
application/json

Copy
Expand allCollapse all
{
"shipping_method": {
"id": 0,
"type": "free",
"name": "string",
"enabled": true,
"free_shipping": true,
"free_shipping_minimum_purchase": true,
"fee": [],
"callback_url": "string",
"fetch_services_url": "string",
"state": "string",
"city": "string",
"postal": "string",
"services": [],
"tables": []
}
}
Delete an existing Shipping Method.
Authorizations:
BasicAuthentication(loginParameterauthtokenParameter)
path Parameters
id
required
integer <int32>
Id of the Shipping Method

Responses
200 OK
404 Shipping Method Not Found.

delete
/shipping_methods/{id}.json
Response samples
200404
Content type
application/json

Copy
"string"
Pickup Locations
Retrieve all Store's Locations
Authorizations:
BasicAuthentication(loginParameterauthtokenParameter)
Responses
200 An array of Pickup Locations

get
/locations.json
Response samples
200
Content type
application/json

Copy
Expand allCollapse all
[
{
"shipping_method": {}
}
]
Create a Pickup Location
Authorizations:
BasicAuthentication(loginParameterauthtokenParameter)
Request Body schema: application/json
required
Location parameters.

name
required
string
Name of the location

main	
boolean
Is the main location

email
required
string
Email for the location

pickup_point	
boolean
Is a pickup_point

postal	
string
Postal code of the location

address
required
string
Address of the location

city
required
string
City of the location

country
required
string
Country of the location

Region	
string
Region of the location

Responses
200 An array of Pickup Locations

post
/locations.json
Request samples
Payload
Content type
application/json

Copy
{
"name": "string",
"main": true,
"email": "string",
"pickup_point": true,
"postal": "string",
"address": "string",
"city": "string",
"country": "string",
"Region": "string"
}
Response samples
200
Content type
application/json

Copy
Expand allCollapse all
{
"shipping_method": {
"id": 0,
"name": "string",
"email": "string",
"active": true,
"pickup_point": true,
"is_stock_origin": true,
"location_address": {}
}
}
Retrieve a Store's Locations by ID
Authorizations:
BasicAuthentication(loginParameterauthtokenParameter)
path Parameters
id
required
integer <int32>
Id of the Product

Responses
200 OK
404 Location not found.

get
/locations/{id}.json
Response samples
200404
Content type
application/json

Copy
Expand allCollapse all
[
{
"shipping_method": {}
}
]
Update a Pickup Location
Authorizations:
BasicAuthentication(loginParameterauthtokenParameter)
path Parameters
id
required
integer <int32>
Id of the Product

Request Body schema: application/json
required
Location parameters.

name
required
string
Name of the location

main	
boolean
Is the main location

email
required
string
Email for the location

pickup_point	
boolean
Is a pickup_point

postal	
string
Postal code of the location

address
required
string
Address of the location

city
required
string
City of the location

country
required
string
Country of the location

Region	
string
Region of the location

Responses
200 An array of Pickup Locations

put
/locations/{id}.json
Request samples
Payload
Content type
application/json

Copy
{
"name": "string",
"main": true,
"email": "string",
"pickup_point": true,
"postal": "string",
"address": "string",
"city": "string",
"country": "string",
"Region": "string"
}
Response samples
200
Content type
application/json

Copy
Expand allCollapse all
{
"shipping_method": {
"id": 0,
"name": "string",
"email": "string",
"active": true,
"pickup_point": true,
"is_stock_origin": true,
"location_address": {}
}
}
Delete a Store's Locations by ID
Authorizations:
BasicAuthentication(loginParameterauthtokenParameter)
path Parameters
id
required
integer <int32>
Id of the Product

Responses
200 OK
404 Location Not Found.

delete
/locations/{id}.json
Response samples
200404
Content type
application/json

Copy
"string"
Custom Fields
Retrieve all Store's Custom Fields.
Authorizations:
BasicAuthentication(loginParameterauthtokenParameter)
Responses
200 An array of Custom Fields

get
/custom_fields.json
Response samples
200
Content type
application/json

Copy
Expand allCollapse all
[
{
"custom_field": {}
}
]
Create a new Custom Field.
Authorizations:
BasicAuthentication(loginParameterauthtokenParameter)
Request Body schema: application/json
required
Custom Field parameters.

custom_field	
object (CustomFieldEditFields)
Responses
200 OK

post
/custom_fields.json
Request samples
Payload
Content type
application/json

Copy
Expand allCollapse all
{
"custom_field": {
"label": "string",
"type": "text",
"values": [],
"product_visibility": true
}
}
Response samples
200
Content type
application/json

Copy
Expand allCollapse all
{
"custom_field": {
"id": 0,
"label": "string",
"type": "text",
"values": [],
"product_visibility": true
}
}
Retrieve a single CustomField.
Authorizations:
BasicAuthentication(loginParameterauthtokenParameter)
path Parameters
id
required
integer <int32>
Id of the CustomField

Responses
200 OK
404 CustomField Not Found.

get
/custom_fields/{id}.json
Response samples
200404
Content type
application/json

Copy
Expand allCollapse all
{
"custom_field": {
"id": 0,
"label": "string",
"type": "text",
"values": [],
"product_visibility": true
}
}
Update a CustomField.
Authorizations:
BasicAuthentication(loginParameterauthtokenParameter)
path Parameters
id
required
integer <int32>
Id of the CustomField

Request Body schema: application/json
required
CustomField parameters.

custom_field	
object (CustomFieldEditFields)
Responses
200 OK
404 CustomField Not Found.

put
/custom_fields/{id}.json
Request samples
Payload
Content type
application/json

Copy
Expand allCollapse all
{
"custom_field": {
"label": "string",
"type": "text",
"values": [],
"product_visibility": true
}
}
Response samples
200404
Content type
application/json

Copy
Expand allCollapse all
{
"custom_field": {
"id": 0,
"label": "string",
"type": "text",
"values": [],
"product_visibility": true
}
}
Delete an existing CustomField.
Authorizations:
BasicAuthentication(loginParameterauthtokenParameter)
path Parameters
id
required
integer <int32>
Id of the CustomField

Responses
200 OK
404 CustomField Not Found.

delete
/custom_fields/{id}.json
Response samples
200404
Content type
application/json

Copy
"string"
Delete an existing CustomFieldSelectOption.
Authorizations:
BasicAuthentication(loginParameterauthtokenParameter)
path Parameters
id
required
integer <int32>
Id of the CustomField

custom_field_select_option_id
required
integer <int32>
Id of the CustomFieldSelectOption

Responses
200 OK
404 CustomFieldSelectOption Not Found.

delete
/custom_fields/{id}/select_options/{custom_field_select_option_id}.json
Response samples
200404
Content type
application/json

Copy
"string"
Custom Field Select Options
Retrieve all Store's Custom Fields.
Authorizations:
BasicAuthentication(loginParameterauthtokenParameter)
path Parameters
id
required
integer <int32>
Id of the CustomField

Responses
200 An array of Custom Fields Select Options

get
/custom_fields/{id}/select_options.json
Response samples
200
Content type
application/json

Copy
Expand allCollapse all
[
{
"custom_field_select_option": {}
}
]
Create a new Custom Field Select Option.
Authorizations:
BasicAuthentication(loginParameterauthtokenParameter)
path Parameters
id
required
integer <int32>
Id of the CustomField

Request Body schema: application/json
required
Custom Field Select Option parameters.

custom_field_select_option	
object (CustomFieldSelectOptionEditFields)
Responses
200 OK

post
/custom_fields/{id}/select_options.json
Request samples
Payload
Content type
application/json

Copy
Expand allCollapse all
{
"custom_field_select_option": {
"value": "string"
}
}
Response samples
200
Content type
application/json

Copy
Expand allCollapse all
{
"custom_field_select_option": {
"id": 0,
"value": "string"
}
}
Retrieve a single SelectOption from a CustomField.
Authorizations:
BasicAuthentication(loginParameterauthtokenParameter)
path Parameters
id
required
integer <int32>
Id of the CustomField

custom_field_select_option_id
required
integer <int32>
Id of the CustomFieldSelectOption

Responses
200 OK
404 CustomFieldSelectOption Not Found.

get
/custom_fields/{id}/select_options/{custom_field_select_option_id}.json
Response samples
200404
Content type
application/json

Copy
Expand allCollapse all
{
"custom_field_select_option": {
"id": 0,
"value": "string"
}
}
Update a SelectOption from a CustomField.
Authorizations:
BasicAuthentication(loginParameterauthtokenParameter)
path Parameters
id
required
integer <int32>
Id of the CustomField

custom_field_select_option_id
required
integer <int32>
Id of the CustomFieldSelectOption

Request Body schema: application/json
required
CustomFieldSelectOption parameters.

custom_field_select_option	
object (CustomFieldSelectOptionEditFields)
Responses
200 OK
404 CustomFieldSelectOption Not Found.

put
/custom_fields/{id}/select_options/{custom_field_select_option_id}.json
Request samples
Payload
Content type
application/json

Copy
Expand allCollapse all
{
"custom_field_select_option": {
"value": "string"
}
}
Response samples
200404
Content type
application/json

Copy
Expand allCollapse all
{
"custom_field_select_option": {
"id": 0,
"value": "string"
}
}
Checkout Custom Fields
Retrieve all Checkout Custom Fields.
Authorizations:
BasicAuthentication(loginParameterauthtokenParameter)
query Parameters
limit	
integer <integer> <= 200
Default: 50
List restriction

page	
integer <integer>
Default: 1
List page

Responses
200 An array of Checkout Custom Fields

get
/checkout_custom_fields.json
Response samples
200
Content type
application/json

Copy
Expand allCollapse all
[
{
"checkout_custom_field": {}
}
]
Create a new CheckoutCustomField.
Type values can be: input, selection, checkbox, date or text. Area values can be: contact, billing_shipping or other.

Authorizations:
BasicAuthentication(loginParameterauthtokenParameter)
Request Body schema: application/json
required
CheckoutCustomField parameters.

checkout_custom_field	
object (CheckoutCustomFieldEditFields)
Responses
200 OK
404 CheckoutCustomField Not Found.

post
/checkout_custom_fields.json
Request samples
Payload
Content type
application/json

Copy
Expand allCollapse all
{
"checkout_custom_field": {
"label": "string",
"type": "text",
"area": "contact",
"required": false,
"position": 0,
"deletable": false,
"custom_field_select_options": []
}
}
Response samples
200404
Content type
application/json

Copy
Expand allCollapse all
{
"checkout_custom_field": {
"id": 0,
"label": "string",
"type": "text",
"area": "contact",
"required": false,
"position": 0,
"deletable": false,
"custom_field_select_options": []
}
}
Retrieve a single CheckoutCustomField.
Authorizations:
BasicAuthentication(loginParameterauthtokenParameter)
path Parameters
id
required
integer <int32>
Id of the CheckoutCustomField

Responses
200 OK
404 CheckoutCustomField Not Found.

get
/checkout_custom_fields/{id}.json
Response samples
200404
Content type
application/json

Copy
Expand allCollapse all
{
"checkout_custom_field": {
"id": 0,
"label": "string",
"type": "text",
"area": "contact",
"required": false,
"position": 0,
"deletable": false,
"custom_field_select_options": []
}
}
Update a CheckoutCustomField.
Authorizations:
BasicAuthentication(loginParameterauthtokenParameter)
path Parameters
id
required
integer <int32>
Id of the CheckoutCustomField

Request Body schema: application/json
required
CheckoutCustomField parameters.

checkout_custom_field	
object (CheckoutCustomFieldEditFields)
Responses
200 OK
404 CheckoutCustomField Not Found.

put
/checkout_custom_fields/{id}.json
Request samples
Payload
Content type
application/json

Copy
Expand allCollapse all
{
"checkout_custom_field": {
"label": "string",
"type": "text",
"area": "contact",
"required": false,
"position": 0,
"deletable": false,
"custom_field_select_options": []
}
}
Response samples
200404
Content type
application/json

Copy
Expand allCollapse all
{
"checkout_custom_field": {
"id": 0,
"label": "string",
"type": "text",
"area": "contact",
"required": false,
"position": 0,
"deletable": false,
"custom_field_select_options": []
}
}
Delete an existing CheckoutCustomField.
Authorizations:
BasicAuthentication(loginParameterauthtokenParameter)
path Parameters
id
required
integer <int32>
Id of the CheckoutCustomField

Responses
200 OK
404 CheckoutCustomField Not Found.

delete
/checkout_custom_fields/{id}.json
Response samples
200404
Content type
application/json

Copy
"string"
Countries
Retrieve all Countries.
Authorizations:
BasicAuthentication(loginParameterauthtokenParameter)
Responses
200 An array of Countries

get
/countries.json
Response samples
200
Content type
application/json

Copy
Expand allCollapse all
[
{
"code": "string",
"name": "string"
}
]
Retrieve a single Country information.
Authorizations:
BasicAuthentication(loginParameterauthtokenParameter)
path Parameters
country_code
required
string <string>
ISO3166 Country Code

Responses
200 A Country information object
404 Country Not Found.

get
/countries/{country_code}.json
Response samples
200404
Content type
application/json

Copy
{
"code": "string",
"name": "string"
}
Retrieve all Regions from a single Country.
Authorizations:
BasicAuthentication(loginParameterauthtokenParameter)
path Parameters
country_code
required
string <string>
ISO3166 Country Code

Responses
200 An array of Regions from a single Country
404 Country Not Found.

get
/countries/{country_code}/regions.json
Response samples
200404
Content type
application/json

Copy
Expand allCollapse all
[
{
"code": "string",
"name": "string",
"iso": "string"
}
]
Retrieve all Municipalities from a single Region.
Authorizations:
BasicAuthentication(loginParameterauthtokenParameter)
path Parameters
country_code
required
string <string>
ISO3166 Country Code

region_code
required
string <string>
Region Code

Responses
200 An array of Municipalities from a single Region
404 Country or Region Not Found.

get
/countries/{country_code}/regions/{region_code}/municipalities.json
Response samples
200404
Content type
application/json

Copy
Expand allCollapse all
[
{
"code": "string",
"name": "string"
}
]
Retrieve a single Region information object.
Authorizations:
BasicAuthentication(loginParameterauthtokenParameter)
path Parameters
country_code
required
string <string>
ISO3166 Country Code

region_code
required
string <string>
Region Code

Responses
200 A Region information object
404 Country or Region not found.

get
/countries/{country_code}/regions/{region_code}.json
Response samples
200404
Content type
application/json

Copy
{
"code": "string",
"name": "string",
"iso": "string"
}
Regions
Retrieve all Regions from a single Country.
Authorizations:
BasicAuthentication(loginParameterauthtokenParameter)
path Parameters
country_code
required
string <string>
ISO3166 Country Code

Responses
200 An array of Regions from a single Country
404 Country Not Found.

get
/countries/{country_code}/regions.json
Response samples
200404
Content type
application/json

Copy
Expand allCollapse all
[
{
"code": "string",
"name": "string",
"iso": "string"
}
]
Retrieve all Municipalities from a single Region.
Authorizations:
BasicAuthentication(loginParameterauthtokenParameter)
path Parameters
country_code
required
string <string>
ISO3166 Country Code

region_code
required
string <string>
Region Code

Responses
200 An array of Municipalities from a single Region
404 Country or Region Not Found.

get
/countries/{country_code}/regions/{region_code}/municipalities.json
Response samples
200404
Content type
application/json

Copy
Expand allCollapse all
[
{
"code": "string",
"name": "string"
}
]
Retrieve a single Region information object.
Authorizations:
BasicAuthentication(loginParameterauthtokenParameter)
path Parameters
country_code
required
string <string>
ISO3166 Country Code

region_code
required
string <string>
Region Code

Responses
200 A Region information object
404 Country or Region not found.

get
/countries/{country_code}/regions/{region_code}.json
Response samples
200404
Content type
application/json

Copy
{
"code": "string",
"name": "string",
"iso": "string"
}
Municipalities
Retrieve all Municipalities from a single Region.
Authorizations:
BasicAuthentication(loginParameterauthtokenParameter)
path Parameters
country_code
required
string <string>
ISO3166 Country Code

region_code
required
string <string>
Region Code

Responses
200 An array of Municipalities from a single Region
404 Country or Region Not Found.

get
/countries/{country_code}/regions/{region_code}/municipalities.json
Response samples
200404
Content type
application/json

Copy
Expand allCollapse all
[
{
"code": "string",
"name": "string"
}
]
Taxes
Retrieve all Taxes.
Authorizations:
BasicAuthentication(loginParameterauthtokenParameter)
Responses
200 An array of Taxes

get
/taxes.json
Response samples
200
Content type
application/json

Copy
Expand allCollapse all
[
{
"tax": {}
}
]
Create a new Tax.
Authorizations:
BasicAuthentication(loginParameterauthtokenParameter)
Request Body schema: application/json
required
Tax parameters.

tax	
object (TaxEditFields)
Responses
200 OK
404 Tax Not Found.

post
/taxes.json
Request samples
Payload
Content type
application/json

Copy
Expand allCollapse all
{
"tax": {
"country": "string",
"name": "string",
"region": "string",
"category_id": 0,
"tax": 0.1,
"fixed": false,
"shipping": false
}
}
Response samples
200404
Content type
application/json

Copy
Expand allCollapse all
{
"tax": {
"id": 0,
"name": "string",
"country": "string",
"region": "string",
"category_id": 0,
"tax_amount": 0.1,
"fixed": false,
"shipping": false
}
}
Retrieve a single Tax information.
Authorizations:
BasicAuthentication(loginParameterauthtokenParameter)
path Parameters
id
required
integer <int32>
Id of the Tax

Responses
200 A Tax information object
404 Tax Not Found.

get
/taxes/{id}.json
Response samples
200404
Content type
application/json

Copy
Expand allCollapse all
{
"tax": {
"id": 0,
"name": "string",
"country": "string",
"region": "string",
"category_id": 0,
"tax_amount": 0.1,
"fixed": false,
"shipping": false
}
}
Partners
Create a Partnered Store
Authorizations:
BasicAuthentication(partner_codeParameterauth_tokenParameter)
Request Body schema: application/json
required
New partnered Store parameters.

email	
string <email>
New Store administrator email.

password	
string <string>
New Store administrator password.

store_name	
string
New Store name.

plan_name	
string
Default: "pro"
Enum: "pro" "plus" "premium"
New Store plan name.

aff	
string
Partner code.

locale	
string
Default: "en"
ISO3166-2 code for the store langauge.

reject_duplicates	
boolean
Default: false
Indicates whether the request should fail if the Store name provided is already in use.

Responses
200 A Partner Store object.
400 Bad Request.

post
/store/create.json
Request samples
Payload
Content type
application/json

Copy
{
"email": "user@example.com",
"password": "string",
"store_name": "string",
"plan_name": "pro",
"aff": "string",
"locale": "en",
"reject_duplicates": false
}
Response samples
200400
Content type
application/json

Copy
Expand allCollapse all
{
"store": {
"code": "string"
}
}
Retrive store creation status.
Authorizations:
BasicAuthentication(partner_codeParameterauth_tokenParameter)
query Parameters
store_code
required
string <string>
Store Code

locale	
string <string>
Default: "en"
ISO 3166-2 code of the language used in the response messages.

Responses
200 A Store status object if creation is still in progress. A new Partner Store object when creation is done.
400 Bad Request.

get
/store/check_status.json
Response samples
200400
Content type
application/json
Example

PartnerStoreStatus
PartnerStoreStatus

Copy
Expand allCollapse all
{
"status": {
"message": "string",
"percentage": "string"
}
}
Retrieve statistics.
Authorizations:
BasicAuthentication(partner_codeParameterauth_tokenParameter)
query Parameters
page	
integer <integer>
Default: 1
List page

from
required
string <string>
Statistics start date. Should be in format 'Y-m-d'.

to
required
string <sting>
Statistics end date. Should be in format 'Y-m-d'.

Responses
200 Array of partner stores statistics.
400 Bad Request.

get
/partners/stores.json
Response samples
200400
Content type
application/json

Copy
Expand allCollapse all
[
{
"code": "string",
"stats": {}
}
]
Retrieve subscriptions and transactions.
Authorizations:
BasicAuthentication(partner_codeParameterauth_tokenParameter)
query Parameters
page	
integer <integer>
Default: 1
List page

Responses
200 Array of partner stores statistics.
400 Bad Request.

get
/partners/subscriptions.json
Response samples
200400
Content type
application/json

Copy
Expand allCollapse all
[
{
"store": {}
}
]
Cart
Obtain information for a cart.
Authorizations:
BasicAuthentication(loginParameterauthtokenParameter)
path Parameters
id
required
integer <int32>
Id of the cart

query Parameters
locale	
string <string>
Locale code of the translation

Responses
200 An array of Orders
404 Cart Not Found.

get
/carts/{id}.json
Response samples
200404
Content type
application/json

Copy
Expand allCollapse all
[
{
"order": {}
}
]
Documents
Retrieve all Documents from a Store.
Authorizations:
BasicAuthentication(loginParameterauthtokenParameter)
query Parameters
limit	
integer <integer> <= 200
Default: 50
List restriction

page	
integer <integer>
Default: 1
List page

Responses
200 An array of documents

get
/documents.json
Response samples
200
Content type
application/json

Copy
Expand allCollapse all
[
{
"document": {}
}
]
Transaction Ledgers
Store Balance
Authorizations:
BasicAuthentication(loginParameterauthtokenParameter)
Responses
200 Store Balance Information

get
/transaction_ledger/balance.json
Response samples
200
Content type
application/json

Copy
Expand allCollapse all
[
{
"balance": 0,
"currency": "string",
"balance_formatted": "string"
}
]
Products Locations
Stock by Product and Location
Authorizations:
BasicAuthentication(loginParameterauthtokenParameter)
query Parameters
location_ids
required
Array of integers <= 50 items
List of location IDs (comma separated)

product_ids
required
Array of integers <= 50 items
List of product IDs (comma separated)

variant_ids	
Array of integers <= 50 items
List of variant IDs (comma separated)

Responses
200 Array of products locations
404 Not found

get
/products_locations
Response samples
200
Content type
application/json

Copy
Expand allCollapse all
[
{
"location_id": 0,
"product_id": 0,
"variant_id": 0,
"stock": 0
}
]
Update Stock by Product and Location
Authorizations:
BasicAuthentication(loginParameterauthtokenParameter)
Request Body schema: application/json
required
location_id
required
integer
product_id
required
integer
variant_id	
integer
stock_unlimited
required
boolean
stock
required
integer
Responses
200 Products locations updated successfully
400 Bad request, check your parameters
500 Error while updating stock error

put
/products_locations
Request samples
Payload
Content type
application/json

Copy
{
"location_id": 0,
"product_id": 0,
"variant_id": 0,
"stock_unlimited": true,
"stock": 0
}
