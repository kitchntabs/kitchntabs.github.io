---
layout: default
title: F12-Billing-Subscriptions-Payments REDBILL-API
---

API Quickstart
Learn how to create your first payment link by integrating our API and start processing payments across Latin America in 3 simple steps.


Alternatively, if you wish to integrate payment forms directly into your web applications, our SDK is available for securely collecting payment information and processing transactions.


Before starting, ensure you have a secret key.

If you're logged in, your sandbox secret key will be automatically populated in the code snippets where applicable.

Step 1: Create a plan or product
To generate a payment link, you first need an active plan or product in Rebill, which represents the product or service you intend to sell. The payment link will be associated with this plan or product.

If you prefer to create a one-time payment link without associating it with a predefined plan or product, you can skip this step and proceed to create an Instant Payment Link.

Use the following API endpoint to create a new plan:

Example request for creating a plan
POST
https://api.rebill.com/v3/plans
curl -X POST  https://api.rebill.com/v3/plans \
  -H "accept: application/json" \
  -H "content-type: application/json" \
  {% raw %}-H "x-api-key: {{API_KEY}}" \{% endraw %}
  -d '{
  "name": [
    {
      "language": "en",
      "text": "Monthly Premium Plan"
    }
  ],
  "description": [
    {
      "language": "en",
      "text": "Premium subscription billed monthly"
    }
  ],
  "frequency": {
      "period": "months",
      "count": 1
  },
  "type": "units",
  "status": "active",
  "prices": [
    {
      "amount": 1990,
      "currency": "ARS",
      "isDefault": true
    },
    {
      "amount": 1790,
      "currency": "CLP"
    }
  ]
}'
  

Copy
Copied!
{% raw %}Replace {{API_KEY}} with your actual secret key, or log in so that your sandbox secret key is automatically populated.{% endraw %}

Customize the plan details in the request body as necessary for your specific offering.

After successfully executing this request, Rebill will return a response containing the unique id of the created plan. You will use this ID in the next step.

Example Plan Creation Response
  {
    "plan": {
       "id": "pln_4b970527a2fe4923ba7477c0c86ec933",
       "name": [
          {
            "language": "en",
            "text": "Monthly Premium Plan"
          }
        ],
        "description": [
          {
            "language": "en",
            "text": "Premium subscription billed monthly"
          }
        ],
        "status": "active",
        "frequency": {
          "period": "months",
          "count": 1
        },
        "type": "units",
        // ... other plan details
    }
}

Copy
Copied!
For more information on the plan object, please refer to our API reference.

Step 2: Create a payment link for the plan/product
Once you have a plan or product ID, you can generate a payment link associated with it. Refer to the Payment Links section of the API reference for comprehensive details on all available parameters for creating payment links.

Note that the currencies available for the payment link are limited to those defined in the associated plan or product.

Use the following endpoint to create a payment link for a plan:

Example request: Create a payment link for a plan
POST
https://api.rebill.com/v3/payment-links
curl -X POST  https://api.rebill.com/v3/payment-links \
  -H "accept: application/json" \
  -H "content-type: application/json" \
  {% raw %}-H "x-api-key: {{API_KEY}}" \{% endraw %}
  -d '{
        "title": [
          {
            "language": "en",
            "text": "Test Payment Link"
          }
        ],
        "plan": {
          "id": "{planId}"
        },
        "paymentMethods": [
          {
            "methods": ["card", "bank_transfer"],
            "currency": "ARS"
          },
          {
            "methods": ["card", "bank_transfer"],
            "currency": "CLP"
          }
        ]
      }'
  

Copy
Copied!
{% raw %}Replace {{API_KEY}} with your actual secret key, or log in so that your sandbox secret key is automatically populated.{% endraw %}

Replace {planId} in the request body with the actual ID of the plan you created in Step 1.

Step 3: Share the payment link
Upon successful creation, the API will respond with the URL of the payment link:

Example Payment Link Creation Response
  {
    "url": "https://pay.rebill.com/my-business-alias/pl_5555fd46072648408c127833"
  }

Copy
Copied!
Share this URL with your customers via email, SMS, social media, or embed it on your website. When customers click the link, they will be directed to a secure Checkout Landing Page hosted by Rebill to complete their payment.

Instant payment links
You can also create Instant Payment Links, which are designed for one-time payments of a specific amount without needing to be associated with a pre-existing product or plan. This is useful for unique charges or services.

To create these, use the Create Instant Payment Link API endpoint.

Integrating payment forms directly
For a more embedded experience, remember that our JavaScript SDK allows you to securely integrate payment forms directly into your web applications. Utilize the SDK if you plan to collect payment information on your site, ensuring PCI DSS compliance.

Testing your integration
Once you have set up your integration for creating plans/products and generating payment links, it's crucial to test the end-to-end flow. Rebill provides a comprehensive set of test card numbers and a Postman collection for testing the product.

Using these test methods, you can simulate various transaction scenarios, including successful payments, rejections due to insufficient funds, expired cards, and more, ensuring your integration handles all cases correctly before going live.

For a complete list of test cards and detailed instructions for simulating different payment outcomes, please refer to our dedicated guide:

Sandbox & Testing
Overview
This comprehensive guide helps developers run realistic and complete tests when integrating with Rebill. It includes payment methods, fake data generators, and internal testing tools to ensure your integration works correctly in all scenarios.


This guide provides everything you need to test your Rebill integration thoroughly. Use these tools and resources to simulate real-world scenarios without moving real money or using personal data.

Important: All examples in this guide are for testing purposes only. Never use real personal data or production credentials in your test environment.

Test payment methods
Test card numbers
Use these test card numbers and specific conditions to simulate various transaction scenarios in Rebill's sandbox environment.

Country	Brand	Number	Exp	CVV	Result
Argentina	Visa	4539 1488 0343 6467	01/99	123	approved
Argentina	Mastercard	5511 0002 2141 4072	01/99	123	approved
Argentina	Visa	4485 3647 3952 7352	01/99	123	generic_reject
Argentina	Visa	4242 4247 6602 5862	01/99	123	human_decline
Argentina	Mastercard	5511 0194 3632 1948	01/99	123	hard_decline
Argentina	American Express	3744 0093 2889 231	01/99	1234	generic_reject
Argentina	Visa (debit)	4280 6300 0000 7713	01/99	123	approved
Brazil	Visa	4532 6381 9543 1230	01/2099	123	approved
Brazil	Mastercard	5555 1224 2222 4444	01/2099	123	approved
Brazil	Visa	4486 3462 9547 8236	01/2099	123	generic_reject
Brazil	Visa	4243 4384 1852 5292	01/99	123	human_decline
Brazil	Mastercard	5105 1051 0510 5100	01/99	123	hard_decline
Brazil	American Express	3745 0079 8569 882	01/2099	1234	generic_reject
Mexico	Visa	4539 6722 9047 6389	01/2099	123	approved
Mexico	Mastercard	5555 0020 4444 0000	01/2099	123	approved
Mexico	Visa	4485 5500 9000 0001	01/2099	123	generic_reject
Mexico	Visa	4244 4482 8478 2108	01/99	123	human_decline
Mexico	Mastercard	5512 0022 3704 7986	01/99	123	hard_decline
Mexico	American Express	3746 0043 2171 150	01/2099	1234	generic_reject
Chile	Visa	4539 9978 0343 0007	01/2099	123	approved
Chile	Mastercard	5513 0064 2588 8480	01/2099	123	approved
Chile	Visa	4485 1070 3952 0019	01/2099	123	generic_reject
Chile	Visa	4245 4517 6949 2184	01/99	123	human_decline
Chile	Mastercard	5513 0138 0747 2123	01/99	123	hard_decline
Chile	American Express	3747 0081 6954 658	01/2099	1234	generic_reject
Colombia	Visa	4539 5422 0343 0015	01/2099	123	approved
Colombia	Mastercard	5555 9856 4444 0026	01/2099	123	approved
Colombia	Visa	4485 6749 3952 0027	01/2099	123	generic_reject
Colombia	Visa	4246 4654 1876 2341	01/99	123	human_decline
Colombia	Mastercard	5514 0055 0087 2558	01/99	123	hard_decline
Colombia	American Express	3748 0098 3705 170	01/2099	1234	generic_reject
Test data generators
Use our Test Data Generator Webapp to create realistic identities, addresses, phones and IPs for LATAM markets. Validate KYC, address formats and phone codes consistently.

Identifications
Generate random IDs for multiple countries and formats:

Country	Type	Format	Example
Argentina	DNI	XX.XXX.XXX	12.345.678
Brazil	CPF	XXX.XXX.XXX-XX	123.456.789-01
Chile	RUT	XX.XXX.XXX-X	12.345.678-9
Colombia	CC	XXX.XXX.XXX	123.456.789
Mexico	INE	XXXX XXXX XXXX XXXX	1234 5678 9012 3456
Billing addresses
Random addresses per country with proper formatting:

Argentina

Street: Av. Corrientes 1234
City: Buenos Aires
State: Buenos Aires
ZIP: 1043

Copy
Copied!
Brazil

Street: Rua das Flores, 123
City: São Paulo
State: SP
ZIP: 01234-567

Copy
Copied!
Chile

Street: Av. Providencia 1234
City: Santiago
State: Región Metropolitana
ZIP: 8320000

Copy
Copied!
Colombia

Street: Carrera 7 #123-45
City: Bogotá
State: Cundinamarca
ZIP: 110111

Copy
Copied!
Mexico

Street: Av. Insurgentes Sur 1234
City: Ciudad de México
State: CDMX
ZIP: 03100

Copy
Copied!
Phone numbers
Examples with international format:

Country	Format	Example
Argentina	+54 9 11 XXXX-XXXX	+54 9 11 1234-5678
Brazil	+55 11 9XXXX-XXXX	+55 11 91234-5678
Chile	+56 9 XXXX-XXXX	+56 9 1234-5678
Colombia	+57 300 XXX-XXXX	+57 300 123-4567
Mexico	+52 55 XXXX-XXXX	+52 55 1234-5678
Valid IP addresses
Examples and ranges for testing:

Country	IP Range	Example IP
Argentina	181.0.0.0/8	181.123.45.67
Brazil	177.0.0.0/8	177.123.45.67
Chile	190.0.0.0/8	190.123.45.67
Colombia	186.0.0.0/8	186.123.45.67
Mexico	187.0.0.0/8	187.123.45.67
Supported currencies
Available currencies for payment processing:

Currency	Description
ARS	Argentine Peso
BRL	Brazilian Real
CLP	Chilean Peso
COP	Colombian Peso
MXN	Mexican Peso
Supported languages
The language parameter defines the language used for Product and Plan creation. Use ISO 639-1 two-letter codes.

Code	Language
es	Spanish
en	English
pt	Portuguese
Usage examples
{
  "name": "Producto de prueba",
  "language": "es"
}

Copy
Copied!
Country codes
The country parameter is used across multiple endpoints to specify where payments will be processed. This field requires a two-letter ISO country code in ISO-3166-1 format.

Supported countries
Code	Country	Description
AR	Argentina	Argentine market
BR	Brazil	Brazilian market
CL	Chile	Chilean market
CO	Colombia	Colombian market
MX	Mexico	Mexican market
Usage examples
{
  "country": "AR",
  "amount": 1000,
  "currency": "ARS"
}

Copy
Copied!
ISO 3166-1 Standard

The country codes follow the international ISO 3166-1 alpha-2 standard, which provides unique two-letter codes for countries and territories. This ensures compatibility with global payment systems and regulatory requirements.

For more information, see Wikipedia ISO 3166-1.

Payment methods by country
Available payment methods for each market. Required for checkout configuration.

Country	Type	Method
Argentina	Card	card
Argentina	Transfer	ar-transfer-qr
Colombia	Card	card
Colombia	Transfer	co-transfer-pse
Brazil	Card	card
Brazil	Cash	br-cash-boleto
Brazil	Transfer	br-transfer-pix
Chile	Card	card
Chile	Transfer	cl-transfer-transfer
Mexico	Card	card
Mexico	Transfer	mx-transfer-spei
ID prefixes reference
All Rebill entities use consistent prefixes to identify their type. Use these prefixes to understand what kind of object an ID represents.

Core entities
Prefix	Entity	Description
org_	Organizations	Your business organization
usr_	Users	Platform users and team members
key_	API Keys	Authentication keys for API access
Products & billing
Prefix	Entity	Description
prd_	Products	Items available for purchase
pln_	Plans	Subscription plans
pl_	Payment Links	Shareable payment pages
cpn_	Coupons	Discount codes and promotions
Payments & customers
Prefix	Entity	Description
cus_	Customers	Customer profiles
pay_	Payments	Payment transactions
crd_	Cards	Stored payment cards
addr_	Addresses	Customer addresses
ch_	Chargebacks	Dispute transactions
Subscriptions
Prefix	Entity	Description
sub_	Subscriptions	Active subscription records
Usage examples

prd_3ec2432fb0c446a8af280fda5fdca14a - Product ID
cus_a1b2c3d4e5f6422885535a6a3794f89e - Customer ID
pay_52b0d61e4d79422885535a6a3794f89e - Payment ID
sub_cd55b3a26d894b77b30101c00e3ef983 - Subscription ID
These prefixes help you quickly identify object types in API responses and ensure you're using the correct IDs in your requests.

States
Get state/province list for address validation and KYC.

Endpoint
curl -X GET https://api.rebill.com/v3/data/states/:isoCountry

Copy
Copied!
Response:

{
  "country": "Argentina",
  "isoCountryCode": "AR",
  "states": ["Buenos Aires", "Córdoba", "Santa Fe", ...the list of states]
}

Copy
Copied!
Phone codes
Get country calling codes for phone number validation.

Endpoint
curl -X GET https://api.rebill.com/v3/data/country-codes/:isoCountry

Copy
Copied!
Response:

{
  "countryCode": "54",
  "isoCountryCode": "AR"
}

Copy
Copied!
Testing Error Scenarios
Understanding and testing error scenarios is crucial for building robust applications. This section covers common checkout errors and how to test them.

Test Card Numbers for Error Scenarios
Use these specific test card numbers to simulate different error conditions:

Card Number	Error Type	Description
4000000000000002	INSUFFICIENT_FUNDS	Simulates insufficient funds
4000000000009995	DECLINED	Simulates declined transaction
4000000000009987	EXPIRED_CARD	Simulates expired card
4000000000009979	INVALID_CVC	Simulates invalid security code


My Organization
Get your organization's data with a single API call.

GET
/v3/organizations/me
Get my organization's data
Fetch your organization's complete data structure including environment settings, customizations, and paired organization details.

Headers
x-api-key
string
required
{% raw %}API key for authentication. Format: x-api-key: {{API_KEY}}{% endraw %}

Response
id
string
Unique identifier for the organization

name
string
Display name of the organization

alias
string
URL-friendly identifier for the organization

status
string
Current status of the organization:

in_progress - Initial setup in progress
active - Organization is active and operational
inactive - Temporarily disabled organization
deletion_requested - Deletion has been requested and is pending
environment
string
Environment where the organization operates:

sandbox - Testing environment with no real charges
production - Live environment processing real transactions
logoUrl
string | null
URL to the organization's logo image, if available

Team Members API
Control your team's access and permissions programmatically. This API gives you granular control over who can do what in your Rebill account.

Understanding Team Roles: Each role has specific permissions that control access to different features. Learn more about what each role can do in our Team Members and Role Management guide.

GET
/v3/members/roles
Get available roles
Get a list of all available team roles. Use this endpoint to populate role selection dropdowns in your application.

Response
roles
array

Show child properties
Get available roles
GET
https://api.rebill.com/v3/members/roles
curl -X GET 'https://api.rebill.com/v3/members/roles' \
        -H 'accept: application/json'

Copy
Copied!
Response
[
  { "id": "owner", "name": "OWNER" },
  { "id": "admin", "name": "ADMIN" },
  { "id": "manager", "name": "MANAGER" },
  { "id": "developer", "name": "DEVELOPER" },
  { "id": "finance", "name": "FINANCE" },
  { "id": "support", "name": "SUPPORT" },
  { "id": "sales", "name": "SALES" },
  { "id": "collection", "name": "COLLECTION" },
  { "id": "viewer", "name": "VIEWER" }
]

Copy
Copied!
GET
/v3/members
List team members
Get a paginated list of team members with filtering options. Use this to build team management interfaces.

Headers
x-api-key
string
required
{% raw %}API key for authentication. Format: x-api-key: {{API_KEY}}{% endraw %}

Query Parameters
offset
integer
Records to skip. Default: 0

limit
integer
Records per page. Default: 10

role
string
Filter by role:

OWNER
ADMIN
MANAGER
DEVELOPER
FINANCE
SUPPORT
SALES
COLLECTION
VIEWER

See role permissions guide for details.

status
string
Filter by status:

INVITED - Pending invitations
ACTIVE - Active members
INACTIVE - Deactivated members
name
string
Filter by member name

email
string
Filter by member email

Response
records
array

Show child properties
pagination
object

Show child properties
List team members
GET
https://api.rebill.com/v3/members
curl -X GET 'https://api.rebill.com/v3/members?limit=10&offset=0&role=admin&status=active' \
        -H 'accept: application/json' \
        {% raw %}-H 'x-api-key: {{API_KEY}}'{% endraw %}

Copy
Copied!
Response
{
  "records": [
    {
      "id": "mem_c5cd5362d014f199759e12f52a306a6",
      "organizationId": "org_79b768cd4a864ddca3052eeb1ad17f12",
      "role": "ADMIN",
      "email": "admin@example.com",
      "name": "John Doe",
      "status": "ACTIVE",
      "invitedAt": "2024-01-01T00:00:00Z",
      "lastEnabledAt": "2024-01-02T00:00:00Z",
      "lastDisabledAt": null
    }
  ],
  "pagination": {
    "totalItems": 25,
    "totalPages": 3,
    "currentPage": 1,
    "itemsPerPage": 10,
    "hasNextPage": true,
    "hasPreviousPage": false
  }
}

Copy
Copied!
GET
/v3/members/{memberId}
Get member details
Get detailed information about a specific team member. Use this to display member profiles or validate member data.

Permission Required: Only users with ADMIN, OWNER, or MANAGER roles can view member details.

Headers
x-api-key
string
required
{% raw %}API key for authentication. Format: x-api-key: {{API_KEY}}{% endraw %}

Query Parameters
id
string
required
ID of the member

Response
member
object

Show child properties
Get member details
GET
https://api.rebill.com/v3/members/{memberId}
curl -X GET 'https://api.rebill.com/v3/members/{memberId}' \
        -H 'accept: application/json' \
        {% raw %}-H 'x-api-key: {{API_KEY}}'{% endraw %}

Copy
Copied!
Response
{
  "id": "mem_c5cd5362d014f199759e12f52a306a6",
  "organizationId": "org_79b768cd4a864ddca3052eeb1ad17f12",
  "role": "ADMIN",
  "email": "admin@example.com",
  "name": "John Doe",
  "status": "ACTIVE",
  "invitedAt": "2024-01-01T00:00:00Z",
  "lastEnabledAt": "2024-01-02T00:00:00Z",
  "lastDisabledAt": null
}

Copy
Copied!
POST
/v3/members/invite
Invite team members
Send invitations to new team members with specific roles. Each invitation triggers an email with a secure signup link.

Permission Required: Only users with ADMIN, OWNER, or MANAGER roles can invite new team members.

Headers
x-api-key
string
required
{% raw %}API key for authentication. Format: x-api-key: {{API_KEY}}{% endraw %}

Request Body Parameters
members
array
required

Show child properties
Invite team members
POST
https://api.rebill.com/v3/members/invite
curl -X POST 'https://api.rebill.com/v3/members/invite' \
      -H 'accept: application/json' \
      -H 'Content-Type: application/json' \
      {% raw %}-H 'x-api-key: {{API_KEY}}' \{% endraw %}
      -d '{
        "members": [
          { "email": "user@example.com", "role": "MANAGER" },
          { "email": "user2@example.com", "role": "VIEWER" }
        ]
      }'

Copy
Copied!
Response
200 OK

Copy
Copied!
PATCH
/v3/members/{memberId}/role
Update member role
Change a member's access level. Role changes take effect immediately.

Permission Required: Only users with ADMIN, OWNER, or MANAGER roles can update member roles.

Headers
x-api-key
string
required
{% raw %}API key for authentication. Format: x-api-key: {{API_KEY}}{% endraw %}

Query Parameters
memberId
string
required
ID of the member

Request Body Parameters
role
string
required
New role: OWNER, ADMIN, MANAGER, DEVELOPER, FINANCE, SUPPORT, SALES, COLLECTION, VIEWER. See role permissions guide for detailed descriptions and permissions.

Update member role
PATCH
https://api.rebill.com/v3/members/{memberId}/role
curl -X PATCH 'https://api.rebill.com/v3/members/{memberId}/role' \
        -H 'accept: application/json' \
        -H 'Content-Type: application/json' \
        {% raw %}-H 'x-api-key: {{API_KEY}}' \{% endraw %}
        -d '{
          "role": "ADMIN"
        }'

Copy
Copied!
Response
204 No Content

Copy
Copied!
PATCH
/v3/members/{memberId}/deactivate
Deactivate Member
Temporarily disable a member's access. Their data remains intact for reactivation.

Permission Required: Only users with ADMIN, OWNER, or MANAGER roles can deactivate members.

Headers
x-api-key
string
required
{% raw %}API key for authentication. Format: x-api-key: {{API_KEY}}{% endraw %}

Query Parameters
memberId
string
required
ID of the member to deactivate

Deactivate member
PATCH
https://api.rebill.com/v3/members/{memberId}/deactivate
curl -X PATCH 'https://api.rebill.com/v3/members/{memberId}/deactivate' \
        -H 'accept: application/json' \
        {% raw %}-H 'x-api-key: {{API_KEY}}'{% endraw %}

Copy
Copied!
Response
204 No Content

Copy
Copied!
PATCH
/v3/members/{memberId}/activate
Activate member
Restore access for a deactivated member. All previous permissions are maintained.

Permission Required: Only users with ADMIN, OWNER, or MANAGER roles can activate members.

Headers
x-api-key
string
required
{% raw %}API key for authentication. Format: x-api-key: {{API_KEY}}{% endraw %}

Query Parameters
memberId
string
required
ID of the member to activate

Activate member
PATCH
https://api.rebill.com/v3/members/{memberId}/activate
curl -X PATCH 'https://api.rebill.com/v3/members/{memberId}/activate' \
        -H 'accept: application/json' \
        {% raw %}-H 'x-api-key: {{API_KEY}}'{% endraw %}

Copy
Copied!
Response
204 No Content

Copy
Copied!
DELETE
/v3/members/invite/{memberId}
Revoke invitation
Cancel a pending invitation immediately. The member won't be able to accept it after revocation.

Permission Required: Only users with ADMIN, OWNER, or MANAGER roles can revoke invitations.

Headers
x-api-key
string
required
{% raw %}API key for authentication. Format: x-api-key: {{API_KEY}}{% endraw %}

Query Parameters
memberId
string
required
ID of the invited member

Revoke invitation
DELETE
https://api.rebill.com/v3/members/invite/{memberId}
curl -X DELETE 'https://api.rebill.com/v3/members/invite/{memberId}' \
        -H 'accept: application/json' \
        {% raw %}-H 'x-api-key: {{API_KEY}}'{% endraw %}



Addresses
Manage customer addresses in a single API. Use these endpoints to create, retrieve, and manage addresses for your customers.

GET
/v3/addresses/:id
Get address by ID
Retrieve a specific address's information including street, city, state, country, zip code and extra info.

Headers
x-api-key
string
required
{% raw %}API key for authentication. Format: x-api-key: {{API_KEY}}{% endraw %}

Path Parameters
id
string
required
Address ID

Response
address
object

Show child properties
Production-ready request
GET
https://api.rebill.com/v3/addresses/:id
curl -X GET "https://api.rebill.com/v3/addresses/:id" \
      {% raw %}-H "x-api-key: {{API_KEY}}"{% endraw %}

Copy
Copied!
Response
  address: {
    "id": "addr_12aa31cdfb574e4191e96e67523a3560",
    "country": "AR",
    "state": "Buenos Aires",
    "city": "Buenos Aires",
    "zipCode": "1000",
    "lineOne": "Av. Corrientes 1234",
    "lineTwo": "Piso 5, Depto A",
    "type": "billing",
    "customerId": "cus_12aa31cdfb574e4191e96e67523a3560"
  }

Copy
Copied!
GET
/v3/addresses
List addresses
Retrieve all addresses associated with a customer, including address details and billing information.

Headers
x-api-key
string
required
{% raw %}API key for authentication. Format: x-api-key: {{API_KEY}}{% endraw %}

Response
addresses
array

Show child properties
Production-ready request
GET
https://api.rebill.com/v3/addresses
curl -X GET "https://api.rebill.com/v3/addresses" \
    {% raw %}-H "x-api-key: {{API_KEY}}"{% endraw %}

Copy
Copied!
Response
addresses: [
  {
      "id": "addr_12aa31cdfb574e4191e96e67523a3560",
      "country": "AR",
      "state": "Buenos Aires",
      "city": "Buenos Aires",
      "zipCode": "1000",
      "lineOne": "Av. Corrientes 1234",
      "lineTwo": "Apartment",
      "type": "billing",
      "customerId": "cus_12aa31cdfb574e4191e96e67523a3560"
  },
  {
      "id": "addr_2a94dfaf407c4f84a41578aad0a6122b",
      "country": "AR",
      "state": "Buenos Aires",
      "city": "Buenos Aires",
      "zipCode": "1414",
      "lineOne": "El Salvador 1234",
      "lineTwo": "Office",
      "type": "shipping",
      "customerId": "cus_12aa31cdfb574e4191e96e67523a3560"
   },
   ...
]

Copy
Copied!
POST
/v3/addresses
Create a address
Create a new address for a customer. All address fields are required for creation.

Headers
x-api-key
string
required
{% raw %}API key for authentication. Format: x-api-key: {{API_KEY}}{% endraw %}

content-type
string
required
Content type. Must be application/json

Request Body
country
string
required
ISO country code (e.g., 'AR', 'US', 'BR'). See Supported Countries for more information.

state
string
required
State or province name

city
string
required
City name

zipCode
string
required
Postal or ZIP code

lineOne
string
required
Primary street address

lineTwo
string
Additional address information (apartment, floor, etc.)

type
string
required
The purpose of the address. Must be either ‘billing’ (used for invoices and payment) or ‘shipping’ (used for deliveries).

customerId
string
required
Customer ID to associate with the address

Response
address
object

Show child properties
Production-ready request
POST
https://api.rebill.com/v3/addresses
curl --request POST \
      --url "https://api.rebill.com/v3/addresses" \
      --header 'content-type: application/json' \
      {% raw %}--header 'x-api-key: {{API_KEY}}' \{% endraw %}
      --data '{
      "country": "AR",
      "state": "Buenos Aires",
      "city": "Buenos Aires",
      "zipCode": "1000",
      "lineOne": "Av. Corrientes 1234",
      "lineTwo": "Apartment",
      "type": "billing",
      "customerId": "cus_12aa31cdfb574e4191e96e67523a3560"
  }'

Copy
Copied!
Response
  address: {
    "id": "addr_12aa31cdfb574e4191e96e67523a3560",
    "country": "AR",
    "state": "Buenos Aires",
    "city": "Buenos Aires",
    "zipCode": "1000",
    "lineOne": "Av. Corrientes 1234",
    "lineTwo": "Apartment",
    "type": "billing",
    "customerId": "cus_12aa31cdfb574e4191e96e67523a3560"
  }

Copy
Copied!
PATCH
/v3/addresses/:id
Update address
Update an existing address. Only provide the fields you want to update.

Headers
x-api-key
string
required
{% raw %}API key for authentication. Format: x-api-key: {{API_KEY}}{% endraw %}

content-type
string
required
Content type. Must be application/json

Path Parameters
id
string
required
Address ID to update

Request Body
country
string
ISO country code (e.g., 'AR', 'US', 'BR')

state
string
State or province name

city
string
City name

zipCode
string
Postal or ZIP code

lineOne
string
Primary street address

lineTwo
string
Additional address information (apartment, floor, etc.)

type
string
The purpose of the address. Must be either ‘billing’ (used for invoices and payment) or ‘shipping’ (used for deliveries).

Response
address
object

Hide child properties
id
string
Unique identifier for the address
country
string
ISO country code
state
string
State or province name
city
string
City name
zipCode
string
Postal code
lineOne
string
Primary street address
lineTwo
string
Additional address information
type
string
Address type ('shipping' or 'billing')
customerId
string
Customer ID
Production-ready request
PATCH
https://api.rebill.com/v3/addresses/:id
curl --request PATCH \
--url "https://api.rebill.com/v3/addresses/test_addr_a5695db8d23e441193e13125f9264cda" \
--header 'content-type: application/json' \
{% raw %}--header 'x-api-key: {{API_KEY}}' \{% endraw %}
--data '{
"lineOne": "Av. Cordoba 1235",
"lineTwo": "Office"
}'


Response
  address: {
    "id": "addr_12aa31cdfb574e4191e96e67523a3560",
    "country": "AR",
    "state": "Buenos Aires",
    "city": "Buenos Aires",
    "zipCode": "1000",
    "lineOne": "Av. Cordoba 1235",
    "lineTwo": "Office",
    "type": "billing",
    "customerId": "cus_12aa31cdfb574e4191e96e67523a3560"
  }


Cards
Store and manage payment cards for your customers. Use these endpoints to create, retrieve, and manage cards for subscriptions and one-time payments.

GET
/v3/cards/:id
Get a card by ID
Retrieve a specific card's information including brand, type, expiration, and creation details.

Headers
x-api-key
string
required
{% raw %}API key for authentication. Format: x-api-key: {{API_KEY}}{% endraw %}

Path Parameters
id
string
required
Card ID

Response
card
object

Show child properties
Production-ready request
GET
https://api.rebill.com/v3/cards/:id
curl -X GET "https://api.rebill.com/v3/cards/:id" \
    {% raw %}-H "x-api-key: {{API_KEY}}"{% endraw %}

Copy
Copied!
Response
{
  "card": {
    "id": "crd_d16eb336861744e3aadc6d29874bd9a1",
    "createdAt": "2025-09-17T15:55:56.872Z",
    "brand": "visa",
    "type": "credit",
    "lastFour": "4905",
    "expiration": {
      "month": "08",
      "year": "2030"
    }
  }
}

Copy
Copied!
GET
/v3/cards?customerId=:customerId
Get card by customer ID
Retrieve all cards associated with a customer, including card details and billing information.

Headers
x-api-key
string
required
{% raw %}API key for authentication. Format: x-api-key: {{API_KEY}}{% endraw %}

Path Parameters
customerId
string
required
Customer ID

Response
card
object

Show child properties
Production-ready request
GET
https://api.rebill.com/v3/cards?customerId=:customerId
curl -X GET "https://api.rebill.com/v3/cards?customerId=:customerId" \
    {% raw %}-H "x-api-key: {{API_KEY}}"{% endraw %}

Copy
Copied!
Response
[
  {
    "card": {
      "id": "crd_d16eb336861744e3aadc6d29874bd9a1",
      "createdAt": "2025-09-17T15:55:56.872Z",
      "brand": "visa",
      "type": "credit",
      "lastFour": "4905",
      "expiration": {
        "month": "08",
        "year": "2030"
      }
    }
  },
  {
    "card": {
      "id": "crd_04bb352e5798471a888a1456cfcc7d6c",
      "createdAt": "2025-09-22T18:32:57.574Z",
      "brand": "visa",
      "type": "credit",
      "lastFour": "4905",
      "expiration": {
        "month": "08",
        "year": "2030"
      }
    }
  },
  {
    "card": {
      "id": "crd_6590119571fe416ea7b04bb318e2335c",
      "createdAt": "2025-09-23T03:45:59.453Z",
      "brand": "visa",
      "type": "credit",
      "lastFour": "4905",
      "expiration": {
        "month": "11",
        "year": "2099"
      }
    }
  }
]

Copy
Copied!
POST
/v3/cards/{customerId}
Create a card
You need to be a certified PCI compliant organization to use this endpoint. If you’re not PCI compliant, please refer to our SDK to handle card details securely.

Headers
x-api-key
string
required
{% raw %}API key for authentication. Format: x-api-key: {{API_KEY}}{% endraw %}

Path Parameters
customerId
string
required
Customer ID

Request Body Parameters
card
object
required

Show child properties
billingDetails
object
required

Show child properties
processingCountry
string
required
Card's processing country code in ISO 3166-1 alpha-2 format. See Supported Countries for more information.

Response
customer
object

Show child properties
card
object

Show child properties
billingDetails
object

Show child properties
Production-ready request
POST
https://api.rebill.com/v3/cards/:customerId
curl -X POST "https://api.rebill.com/v3/cards/:customerId" \
    {% raw %}-H "x-api-key: {{API_KEY}}" \{% endraw %}
    -H "Content-Type: application/json" \
    -d '{
      "card": {
          "number": "4539148803436467",
          "name": "Ana López",
          "cvv": 123,
          "expiration": {
              "month": "11",
              "year": "2099"
          }
      },
      "billingDetails": {
          "address": {
              "lineOne": "Av. Corrientes 1234",
              "city": "Buenos Aires",
              "state": "CABA",
              "zipCode": "C1043AAZ",
              "country": "AR",
          },
          "identification": {
              "type": "DNI",
              "value": "12345678"
          }
      },
      "processingCountry": "AR"
    }'

Copy
Copied!
Response
{
"customer": {
  "id": "cus_90fa7a3726de41db848458da33ed682a",
  "email": "ana@example.com"
},
"card": {
  "id": "crd_0e7073b3b5b8405aa8dd41390f745a46",
  "createdAt": "2025-09-26T14:39:56.747Z",
  "name": "Ana Lopez",
  "bin": "453914",
  "brand": "visa",
  "type": "credit",
  "lastFour": "6467",
  "status": "operative",
  "expiration": {
      "month": "11",
      "year": "2099"
  }
},
"billingDetails": {
  "identification": {
      "id": "id_54c0a9c9a07249f8987e237f214fde9b"
  },
  "address": {
      "id": "addr_c73768f9551d4b43b6dae703e19d7891"
  }
}
}

Checkout
Process payments across Latin America through a unified API. This endpoint handles different payment methods:

Card payments: Process credit/debit card transactions
Alternative Payment Methods (APM): Handle bank transfers, cash payments, and local payment methods
POST
/v3/checkout
Card checkout
Process card payments for products, subscriptions, or custom amounts.

This endpoint supports two ways to provide card information:

Full card object: Send complete card details (for PCI compliant merchants)
Card ID: Use a previously stored card ID
What can you sell?
This endpoint supports four types of transactions. Choose only one per request:

Transaction Type	Required Fields	Description
Existing Product	productId	Sell an existing product from your catalog
Existing Plan	planId	Start a recurring subscription with an existing plan
Instant Payment	amount, currency, name	Charge a custom amount for a one-time payment
Instant Subscription	amount, currency, name, frequency, type	Create a subscription on-the-fly with custom pricing
Important: You can only include one transaction type per request. Mixing different types will cause an error.



Headers
x-api-key
string
required
{% raw %}API key for authentication. Format: x-api-key: {{API_KEY}} API key for authentication. Format: x-api-key: {{API_KEY}}{% endraw %}

Request Body Parameters
These are the essential fields you need to process a card payment:

transaction
object

Show child properties
subscription
object

Show child properties
customer
object
required

Show child properties
cardId
string
ID of a previously stored card. Use this if you've already saved the customer's card. Choose one method: card or cardId.

card
object

Show child properties
billingDetails
object
required

Show child properties
installments
number
Number of installments to split the payment (if supported by the card and country).

paymentMetadata
object

Show child properties
subscriptionMetadata
object

Show child properties
saveCard
boolean
Whether to save the card after the payment is processed. Default is false.

customAttributes
object

Show child properties
Response
The API will return a response with the following structure:

traceId
string
Unique identifier for tracking this specific checkout operation.

date
string
Timestamp when the response was generated (ISO 8601 format).

result
object

Show child properties
error
object

Show child properties
Existing product checkout
POST
https://api.rebill.com/v3/checkout
curl --location 'https://api.rebill.com/v3/checkout' \
--header 'Content-Type: application/json' \
{% raw %}--header 'x-api-key: {{API_KEY}}' \{% endraw %}
--data-raw '{
  "transaction": {
      "quantity": 1,
      "currency": "ARS",
      "productId": "test_prd_c5718bae2e5545ecae2e396a796570f5"
  },
  "customer": {
      "firstName": "Ana",
      "lastName": "López",
      "email": "analopez@example.com",
      "phone": {
          "countryCode": "54",
          "number": "1153190141"
      },
      "shippingAddress": {
          "lineOne": "Av. Corrientes 1234",
          "lineTwo": "Apartment",
          "city": "Buenos Aires",
          "state": "CABA",
          "zipCode": "C1043AAZ",
          "country": "AR"
      }
  },
  "card": {
      "name": "Ana López",
      "expiration": {
          "month": "11",
          "year": "2099"
      },
      "cvv": "123",
      "number": "4507990000004905"
  },
  "billingDetails": {
      "address": {
          "lineOne": "Av. Corrientes 1234",
          "lineTwo": "Apartment",
          "city": "Buenos Aires",
          "state": "CABA",
          "zipCode": "C1043AAZ",
          "country": "AR"
      },
      "identification": {
          "type": "DNI",
          "value": "43044413"
      }
  },
  "paymentMetadata": {
      "customField1": "value1",
      "customField2": "value2"
  },
  "customAttributes": {
      "deviceId": "fpt_9ec48794-95e9-47ba-8092-f86c1088b65a"
  }
}'

Copy
Copied!
Existing plan checkout
POST
https://api.rebill.com/v3/checkout
curl --location 'https://api.rebill.com/v3/checkout' \
--header 'Content-Type: application/json' \
{% raw %}--header 'x-api-key: {{API_KEY}}' \{% endraw %}
--data-raw '{
  "subscription": {
      "quantity": 1,
      "currency": "ARS",
      "planId": "test_pln_3724ff11fa5c4853bea5a22b2867191b"
  },
  "customer": {
      "firstName": "Ana",
      "lastName": "López",
      "email": "analopez@example.com",
      "phone": {
          "countryCode": "54",
          "number": "1153190141"
      },
      "shippingAddress": {
          "lineOne": "Av. Corrientes 1234",
          "lineTwo": "Apartment",
          "city": "Buenos Aires",
          "state": "CABA",
          "zipCode": "C1043AAZ",
          "country": "AR"
      }
  },
  "card": {
      "name": "Ana López",
      "expiration": {
          "month": "11",
          "year": "2099"
      },
      "cvv": "123",
      "number": "4507990000004905"
  },
  "billingDetails": {
      "address": {
          "lineOne": "Av. Corrientes 1234",
          "lineTwo": "Apartment",
          "city": "Buenos Aires",
          "state": "CABA",
          "zipCode": "C1043AAZ",
          "country": "AR"
      },
      "identification": {
          "type": "DNI",
          "value": "43044413"
      }
  },
  "paymentMetadata": {
      "customField1": "value1",
      "customField2": "value2"
  },
  "customAttributes": {
      "deviceId": "fpt_9ec48794-95e9-47ba-8092-f86c1088b65a"
  }
}'

Copy
Copied!
Instant payment checkout
POST
https://api.rebill.com/v3/checkout
curl --location 'https://api.rebill.com/v3/checkout' \
--header 'Content-Type: application/json' \
{% raw %}--header 'x-api-key: {{API_KEY}}' \{% endraw %}
--data-raw '{
  "transaction": {
      "quantity": 1,
      "amount": 25000,
      "name": [{ "language": "es", "text": "Pago instantaneo" }],
      "currency": "ARS"
  },
 "customer": {
      "firstName": "Ana",
      "lastName": "López",
      "email": "analopez@example.com",
      "phone": {
          "countryCode": "54",
          "number": "1153190141"
      },
      "shippingAddress": {
          "lineOne": "Av. Corrientes 1234",
          "lineTwo": "Apartment",
          "city": "Buenos Aires",
          "state": "CABA",
          "zipCode": "C1043AAZ",
          "country": "AR"
      }
  },
   "card": {
      "name": "Ana López",
      "expiration": {
          "month": "11",
          "year": "2099"
      },
      "cvv": "123",
      "number": "4507990000004905"
  },
   "billingDetails": {
      "address": {
          "lineOne": "Av. Corrientes 1234",
          "lineTwo": "Apartment",
          "city": "Buenos Aires",
          "state": "CABA",
          "zipCode": "C1043AAZ",
          "country": "AR"
      },
      "identification": {
          "type": "DNI",
          "value": "43044413"
      }
  },
  "paymentMetadata": {
      "customField1": "value1",
      "customField2": "value2"
  },
  "customAttributes": {
      "deviceId": "fpt_9ec48794-95e9-47ba-8092-f86c1088b65a"
  }
}'

Copy
Copied!
Instant subscription checkout
POST
https://api.rebill.com/v3/checkout
curl --location 'https://api.rebill.com/v3/checkout' \
--header 'Content-Type: application/json' \
{% raw %}--header 'x-api-key: {{API_KEY}}' \{% endraw %}
--data-raw '{
  "subscription": {
      "name": [
          {
              "language": "en",
              "text": "Instant subscription"
          }
      ],
      "amount": 250,
      "currency": "ARS",
      "frequency": {
          "period": "month",
          "count": 1
      },
      "repetitions": 3,
      "type": "units",
      "quantity": 1
  },
  "customer": {
      "firstName": "Ana",
      "lastName": "López",
      "email": "analopez@example.com",
      "phone": {
          "countryCode": "54",
          "number": "1153190141"
      },
      "shippingAddress": {
          "lineOne": "Av. Corrientes 1234",
          "lineTwo": "Apartment",
          "city": "Buenos Aires",
          "state": "CABA",
          "zipCode": "C1043AAZ",
          "country": "AR"
      }
  },
  "card": {
      "name": "Ana López",
      "expiration": {
          "month": "11",
          "year": "2099"
      },
      "cvv": "123",
      "number": "4507990000004905"
  },
  "billingDetails": {
      "address": {
          "lineOne": "Av. Corrientes 1234",
          "lineTwo": "Apartment",
          "city": "Buenos Aires",
          "state": "CABA",
          "zipCode": "C1043AAZ",
          "country": "AR"
      },
      "identification": {
          "type": "DNI",
          "value": "43044413"
      }
  },
  "paymentMetadata": {
      "customField1": "value1",
      "customField2": "value2"
  },
  "customAttributes": {
      "deviceId": "fpt_9ec48794-95e9-47ba-8092-f86c1088b65a"
  }
}'

Copy
Copied!
Response
Successful Response
Error Response
{
  "traceId": "checkout_1709058830240_kj8n2x5",
  "date": "2024-02-24T22:33:50.240Z",
  "result": {
    "paymentId": "pay_987f8a061d2c3da6ab044711e51f163d",
    "status": "approved",
    "subscriptionId": "sub_3k1568576a364e10aa96a149c753093j",
    "cardId": "crd_251568576a364e10aa96a149c753krut",
    "customerId": "cust_327f8a061d2c3da6ab044711e510sder"
  }
}

Copy
Copied!
POST
/v3/checkout/request
APM checkout (Alternative Payment Methods)
Trigger a redirect-based payment flow for cash, bank transfer, or QR methods. You define the amount, currency, product name, and payment method. The customer is redirected to complete the payment. Use this for any supported APM.

Headers
x-api-key
string
required
{% raw %}API key for authentication. Format: x-api-key: {{API_KEY}} API key for authentication. Format: x-api-key: {{API_KEY}}{% endraw %}

Required Body Parameters
transaction
object
required

Show child properties
method
string
required
Payment method - Choose which payment provider to use. Each method is specific to a country and payment type.

customer
object
required

Show child properties
billingDetails
object
required

Show child properties
redirect
object
required

Show child properties
paymentMetadata
object

Show child properties
subscriptionMetadata
object

Show child properties
customAttributes
object

Show child properties
Example request for APM checkout
POST
https://api.rebill.com/v3/checkout/request
curl -X POST  https://api.rebill.com/v3/checkout/request \
      -H "accept: application/json" \
      -H "content-type: application/json" \
      {% raw %}-H "x-api-key: {{API_KEY}}" \{% endraw %}
      -d '{
            "transaction": {
              "amount": 1000,
              "currency": "ARS",
              "name": [
                { "language": "en", "text": "Product Name" }
              ],
              "description": [
                { "language": "en", "text": "Product Description" }
              ] 
            },
            "method": "co-transfer-pse",
            "billingDetails": {
              "address": {
                "lineOne": "123 Main St",
              "city": "Buenos Aires",
                "state": "CABA",
                "zipCode": "1000",
                "country": "AR"
              },
              "identification": {
                "type": "DNI",
                "value": "30021085"
              }
            },
            "customer": {
              "firstName": "John",
              "lastName": "Doe",
              "email": "john.doe@example.com",
              "phone": {
                "countryCode": "54",
                "number": "1234567"
              },
              "shippingAddress": {
                "lineOne": "123 Main St",
                "city": "Buenos Aires",
                "state": "CABA",
                "zipCode": "1000",
                "country": "AR"
              }
            },
            "billingDetails": {
              "address": {
                "country": "AR",
                "state": "CABA",
                "city": "Buenos Aires",
                "zipCode": "1000",
                "lineOne": "Av. Corrientes 1232"
              },
              "identification": {
                "type": "DNI",
                "value": "30021085"
              }
            },
            "paymentMetadata": {
              "customField1": "value1",
              "customField2": "value2"
            },
            "redirect": {
              "approved": "https://yourstore.com/success",
              "rejected": "https://yourstore.com/failed"
            }
        }'

Copy
Copied!
Response
Successful Response
Error Response
{
  "traceId": "checkout_1709058830244_r8h3k5m",
  "date": "2024-02-24T22:33:50.244Z",
  "result": {
    "checkoutRequestId": "chk_req_2f5a8d1c4e7b9a3d6f8c1e4a7b2d5c8e",
    "status": "PENDING",
    "data": {
      "redirectUrl": "https://pse.com/98765432",
    }
  }
}

Copy
Copied!
GET
/v3/checkout/request/:checkoutRequestId
APM checkout details
Retrieve the status and details of an Alternative Payment Method (APM) checkout request. Use this endpoint to poll the current state of a payment initiated via /checkout/request. This is useful for updating your UI or backend after redirect-based or cash payments.

Path Parameters
checkoutRequestId
string
required
Unique identifier for the APM checkout request. Returned by the POST /checkout/request endpoint.

Headers
x-api-key
string
required
{% raw %}API key for authentication. Format: x-api-key: {{API_KEY}} API key for authentication. Format: x-api-key: {{API_KEY}}{% endraw %}

Response
The API returns detailed information about the APM checkout request:

checkoutRequestId
string
required
Unique identifier for this checkout request. Use this ID to track the payment status.

status
string
required
Current status of the payment. Possible values:

pending_customer_charge - Customer needs to complete the payment
approved - Payment completed successfully and funds are available
expired - Payment request expired before customer could complete it
rejected - Payment was rejected
type
string
required
Type of payment method used:

cash - Cash payment
bank_transfer - Bank transfer
data
object
required

Show child properties
Example request to get APM checkout status
GET
https://api.rebill.com/v3/checkout/request/:checkoutRequestId
curl -X GET https://api.rebill.com/v3/checkout/request/:checkoutRequestId \
-H "accept: application/json" \
{% raw %}-H "x-api-key: {{API_KEY}}"{% endraw %}

Copy
Copied!
Response
Successful Response
Error Response: Not Found
{
  "checkoutRequestId": "chk_req_2f5a8d1c4e7b9a3d6f8c1e4a7b2d5c8e",
  "status": "approved",
  "type": "bank_transfer",
  "data": {
    "url": "https://pse.com/98765432",
    "message": "Payment completed successfully"
  },
}

Copy
Copied!
To see the full list of payment methods, please refer to the Payment Methods section.

GET
/v3/checkout/deviceId/:countryCode
Get Device ID
Generate a unique device identifier for fraud detection and risk assessment. This endpoint returns a deviceId that you can include in your checkout requests to improve payment approval rates and security.

Path Parameters
countryCode
string
required
Two-letter country code (ISO 3166-1 alpha-2) where the payment will be processed. This helps generate the appropriate device ID format for the specific country.

Headers
x-api-key
string
required
{% raw %}API key for authentication. Format: x-api-key: {{API_KEY}}{% endraw %}

Response
The API returns a unique device identifier:

deviceId
string
Unique device identifier that should be included in the customAttributes field of your checkout requests. This helps with fraud detection and improves payment approval rates.

Usage
Once you obtain the deviceId, include it in your checkout requests within the customAttributes object:

{
  "customAttributes": {
    "deviceId": "fpt_9ec48794-95e9-47ba-8092-f86c1088b65a"
  }
}

Copy
Copied!
Get device ID for Argentina
GET
https://api.rebill.com/v3/checkout/deviceId/:countryCode
curl --location 'https://api.rebill.com/v3/checkout/deviceId/AR' \
{% raw %}--header 'x-api-key: {{API_KEY}}'{% endraw %}

Copy
Copied!
Response
{
  "deviceId": "fpt_9ec48794-95e9-47ba-8092-f86c1088b65a"
}

Coupons
Create, manage and track discount coupons programmatically. Use this API to build custom discount flows, loyalty programs, or promotional campaigns.

GET
/v3/coupons/:id
Get coupon by ID
Fetch a specific coupon's details by ID.

Headers
x-api-key
string
required
{% raw %}API key for authentication. Format: x-api-key: {{API_KEY}}{% endraw %}

Request Body Parameters
id
string
required
Coupon ID to fetch

Response
id
string
Unique coupon identifier with cpn_ prefix
name
string
Coupon name for identification and display
description
string
Public description shown to customers during checkout
notes
string
Internal notes for tracking and management purposes
format
string
Discount type: PERCENTAGE or FIXED_AMOUNT
code
string
Promotional code for manual redemption (null if auto-applied)
productIds
array

Show child properties
planIds
array

Show child properties
paymentLinkIds
array

Show child properties
customerId
string
Specific customer ID restriction
expirationDate
string
ISO 8601 expiration date (null if never expires)
redemptions
number
Current number of times this coupon has been used
status
string
Current status: active, expired, or used
percentage
number
Percentage discount value (1-100, null for fixed amount)
fixedAmountsPerCurrency
array

Show child properties
applicableCycles
number
Number of billing cycles discount applies to (null for infinite)
availableUses
number
Maximum number of times coupon can be used (null for unlimited)
lastArchivedAt
string
Timestamp when coupon was last archived (null if never archived)
lastUnarchivedAt
string
Timestamp when coupon was last unarchived (null if never unarchived)
isArchived
boolean
Whether coupon is currently archived and unavailable for use
createdAt
string
ISO 8601 timestamp when coupon was created
Fetch coupon details
GET
https://api.rebill.com/v3/coupons/:id
curl -X GET https://api.rebill.com/v3/coupons/:id \
{% raw %}-H "x-api-key: {{API_KEY}}"{% endraw %}

Copy
Copied!
Response
    {
      "id": "cpn_64d92e630b054c60ba083a8ac543f63e",
      "name": "10% OFF Descount",
      "description": "10% OFF Descount",
      "notes": null,
      "format": "PERCENTAGE",
      "code": "CODE10",
      "productIds": [],
      "planIds": [],
      "paymentLinkIds": [],
      "customerId": null,
      "expirationDate": "2025-11-25",
      "redemptions": 0,
      "status": "active",
      "percentage": 10,
      "fixedAmountsPerCurrency": null,
      "applicableCycles": 5,
      "availableUses": 10,
      "lastArchivedAt": null,
      "lastUnarchivedAt": null,
      "isArchived": false,
      "createdAt": "2025-09-03T18:56:07.639Z"
    }

Copy
Copied!
POST
/v3/coupons
Create a coupon
Create a new coupon with flexible discount options. Supports both percentage and fixed amount discounts across multiple currencies.

Headers
x-api-key
string
required
{% raw %}API key for authentication. Format: x-api-key: {{API_KEY}}{% endraw %}

Request Body Parameters
name
string
required
Coupon name for identification. Max 50 characters.

description
string
Brief public description shown to customers. Max 50 characters.

notes
string
Internal notes for tracking purposes.

format
string
required
Discount type: PERCENTAGE or FIXED_AMOUNT

code
string
Required only for promotional code redemption. If omitted, coupon applies automatically via direct association.

productIds
array

Show child properties
planIds
array

Show child properties
paymentLinkIds
array

Show child properties
customerId
string
Customer ID this coupon applies to. (E.g. cus_235e2d548a...)

expirationDate
string
ISO 8601 format expiration date (e.g. "2025-12-31T23:59:59Z"). If omitted, coupon never expires.

percentage
number
Required for PERCENTAGE format. Integer value between 1-100 (represents percentage).

fixedAmountsPerCurrency
array

Show child properties
availableUses
number
Maximum redemption count. If omitted, unlimited usage.

applicableCycles
number
Number of billing cycles to apply discount. If omitted, applies to all cycles (infinite).

Note: When multiple restriction types are specified (productIds, planIds, paymentLinkIds, customerId), the coupon applies only when ALL conditions are met (AND logic).

Response Parameters
id
string
Unique coupon identifier with cpn_ prefix
name
string
Coupon name for identification and display
description
string
Public description shown to customers during checkout
notes
string
Internal notes for tracking and management purposes
format
string
Discount type: PERCENTAGE or FIXED_AMOUNT
code
string
Promotional code for manual redemption (null if auto-applied)
productIds
array

Show child properties
planIds
array

Show child properties
paymentLinkIds
array

Show child properties
customerId
string
Specific customer ID restriction
expirationDate
string
ISO 8601 expiration date (null if never expires)
redemptions
number
Current number of times this coupon has been used
status
string
Current status: active, expired, or used
percentage
number
Percentage discount value (1-100, null for fixed amount)
fixedAmountsPerCurrency
array

Show child properties
applicableCycles
number
Number of billing cycles discount applies to (null for infinite)
availableUses
number
Maximum number of times coupon can be used (null for unlimited)
lastArchivedAt
string
Timestamp when coupon was last archived (null if never archived)
lastUnarchivedAt
string
Timestamp when coupon was last unarchived (null if never unarchived)
isArchived
boolean
Whether coupon is currently archived and unavailable for use
createdAt
string
ISO 8601 timestamp when coupon was created
Create a multi-currency fixed amount coupon
POST
https://api.rebill.com/v3/coupons
curl -X POST https://api.rebill.com/v3/coupons \
  -H "accept: application/json" \
  -H "content-type: application/json" \
  {% raw %}-H "x-api-key: {{API_KEY}}" \{% endraw %}
  -d '{
    "name": "Multi-currency 3-5 OFF",
    "description": "Applies $3 USD or €5 EUR discount",
    "notes": "Valid for purchases in USD and EUR",
    "format": "FIXED_AMOUNT",
    "code": "MULTI3OFF",
    "fixedAmountsPerCurrency": [
        {
            "amount": 300,
            "currency": "ARS"
        },
        {
            "amount": 500,
            "currency": "COP"
        }
    ],
    "expirationDate": "2025-11-25T00:00:00Z",
    "availableUses": 10,
    "applicableCycles": 5
  }'

Copy
Copied!
Response
Response
400 Bad Request
401 Unauthorized
422 Unprocessable Entity
{
  "id": "cpn_22fff09f9dc54f9d8d0a0f1fdcc29822",
  "name": "Multi-currency 3-5 OFF",
  "description": "Applies $3 USD or €5 EUR discount",
  "notes": "Valid for purchases in USD and EUR",
  "format": "FIXED_AMOUNT",
  "code": "MULTI3OFF",
  "productIds": [],
  "planIds": [],
  "paymentLinkIds": [],
  "customerId": null,
  "expirationDate": "2025-11-25T00:00:00.000Z",
  "redemptions": 0,
  "status": "active",
  "percentage": null,
  "fixedAmountsPerCurrency": [
      {
          "amount": 300,
          "currency": "ARS"
      },
      {
          "amount": 500,
          "currency": "COP"
      }
  ],
  "applicableCycles": 5,
  "availableUses": 10,
  "lastArchivedAt": null,
  "lastUnarchivedAt": null,
  "isArchived": false,
  "createdAt": "2025-09-03T18:38:27.113Z"
}

Copy
Copied!
Create a coupon with percentage discount
POST
https://api.rebill.com/v3/coupons
curl -X POST https://api.rebill.com/v3/coupons \
  -H "accept: application/json" \
  -H "content-type: application/json" \
  {% raw %}-H "x-api-key: {{API_KEY}}" \{% endraw %}
  -d '{
    "name": "10% OFF Descount",
    "description": "10% OFF Descount",
    "format": "PERCENTAGE",
    "code": "CODE10",
    "percentage": 10,
    "expirationDate": "2025-11-25T00:00:00Z",
    "availableUses": 10,
    "applicableCycles": 5
  }'

Copy
Copied!
Response
Response
400 Bad Request
401 Unauthorized
422 Unprocessable Entity
{
  "id": "cpn_64d92e630b054c60ba083a8ac543f63e",
  "name": "10% OFF Descount",
  "description": "10% OFF Descount",
  "notes": null,
  "format": "PERCENTAGE",
  "code": "CODE10",
  "productIds": [],
  "planIds": [],
  "paymentLinkIds": [],
  "customerId": null,
  "expirationDate": "2025-11-25T00:00:00.000Z",
  "redemptions": 0,
  "status": "active",
  "percentage": 10,
  "fixedAmountsPerCurrency": null,
  "applicableCycles": 5,
  "availableUses": 10,
  "lastArchivedAt": null,
  "lastUnarchivedAt": null,
  "isArchived": false,
  "createdAt": "2025-09-03T18:56:07.639Z"
}

Copy
Copied!
POST
/v3/coupons/search
List coupons
Look up coupons with granular filters. Build custom search logic for your use case.

Headers
x-api-key
string
required
{% raw %}API key for authentication. Format: x-api-key: {{API_KEY}}{% endraw %}

Request Body Parameters
filters
object

Show child properties
pagination
object

Show child properties
Response
records
array

Show child properties
pagination
object

Show child properties
List active coupons
POST
https://api.rebill.com/v3/coupons/search
curl -X POST https://api.rebill.com/v3/coupons/search \
      -H "accept: application/json" \
      {% raw %}-H "x-api-key: {{API_KEY}}" \{% endraw %}
      -H "Content-Type: application/json" \
      -d '{
        "filters": {
          "status": ["active"]
        },
        "pagination": {
          "limit": 10,
          "offset": 0
        }
      }'

Copy
Copied!
Response
{
  "records": [
      {
          "id": "cpn_64d92e630b054c60ba083a8ac543f63e",
          "name": "10% OFF Descount",
          "description": "10% OFF Descount",
          "notes": null,
          "format": "PERCENTAGE",
          "code": "CODE10",
          "productIds": [],
          "planIds": [],
          "paymentLinkIds": [],
          "customerId": null,
          "expirationDate": "2025-11-25",
          "redemptions": 0,
          "status": "active",
          "percentage": 10,
          "fixedAmountsPerCurrency": null,
          "applicableCycles": 5,
          "availableUses": 10,
          "lastArchivedAt": null,
          "lastUnarchivedAt": null,
          "isArchived": false,
          "createdAt": "2025-09-03T18:56:07.639Z"
      },
      {
          "id": "cpn_22fff09f9dc54f9d8d0a0f1fdcc29822",
          "name": "Multi-currency 3-5 OFF",
          "description": "Applies $3 USD or €5 EUR discount",
          "notes": "Valid for purchases in USD and EUR",
          "format": "FIXED_AMOUNT",
          "code": "MULTI3OFF",
          "productIds": [],
          "planIds": [],
          "paymentLinkIds": [],
          "customerId": null,
          "expirationDate": "2025-11-25",
          "redemptions": 0,
          "status": "active",
          "percentage": null,
          "fixedAmountsPerCurrency": [
              {
                  "amount": 300,
                  "currency": "ARS"
              },
              {
                  "amount": 500,
                  "currency": "COP"
              }
          ],
          "applicableCycles": 5,
          "availableUses": 10,
          "lastArchivedAt": null,
          "lastUnarchivedAt": null,
          "isArchived": false,
          "createdAt": "2025-09-03T18:38:27.113Z"
      },
      {
          "id": "cpn_e6e4000a10404a79bba3961934d8113c",
          "name": "Desc10",
          "description": "Descuento del 10%",
          "notes": null,
          "format": "PERCENTAGE",
          "code": "DESC10",
          "productIds": [],
          "planIds": [],
          "paymentLinkIds": [],
          "customerId": null,
          "expirationDate": "2025-09-06",
          "redemptions": 1,
          "status": "active",
          "percentage": 10,
          "fixedAmountsPerCurrency": null,
          "applicableCycles": 1,
          "availableUses": 1,
          "lastArchivedAt": null,
          "lastUnarchivedAt": null,
          "isArchived": false,
          "createdAt": "2025-09-02T22:16:34.695Z"
      }
  ],
  "pagination": {
      "totalItems": 3,
      "totalPages": 1,
      "currentPage": 1,
      "itemsPerPage": 10,
      "hasNextPage": false,
      "hasPreviousPage": false
  }
}

Copy
Copied!
PUT
/v3/coupons/:id
Update a coupon
Update specific coupon fields. Only include fields that need to change.

Headers
x-api-key
string
required
{% raw %}API key for authentication. Format: x-api-key: {{API_KEY}}{% endraw %}

Request Body Parameters
id
string
required
Coupon ID to update

name
string
Coupon name for identification. Max 50 characters.

description
string
Brief public description shown to customers. Max 50 characters.

notes
string
Internal notes for tracking purposes. Max 255 characters.

format
string
Discount type: PERCENTAGE or FIXED_AMOUNT

code
string
Required only for promotional code redemption. If omitted, coupon applies automatically via direct association.

productIds
array

Show child properties
planIds
array

Show child properties
paymentLinkIds
array

Show child properties
customerId
string
Customer ID this coupon applies to. (E.g. cus_235e2d548a...)

expirationDate
string
ISO 8601 format expiration date (e.g. "2025-12-31T23:59:59Z"). If omitted, coupon never expires.

percentage
number
Required for PERCENTAGE format. Integer value between 1-100 (represents percentage).

fixedAmountsPerCurrency
array

Show child properties
availableUses
number
Maximum redemption count. If omitted, unlimited usage.

applicableCycles
number
Number of billing cycles to apply discount. If omitted, applies to all cycles (infinite).

Response
id
string
Unique coupon identifier with cpn_ prefix
name
string
Updated coupon name for identification and display
description
string
Updated public description shown to customers during checkout
notes
string
Updated internal notes for tracking and management purposes
format
string
Updated discount type: PERCENTAGE or FIXED_AMOUNT
code
string
Updated promotional code for manual redemption (null if auto-applied)
productIds
array

Show child properties
planIds
array

Show child properties
paymentLinkIds
array

Show child properties
customerId
string
Updated customer ID restriction
expirationDate
string
Updated ISO 8601 expiration date (null if never expires)
redemptions
number
Current number of times this coupon has been used (unchanged)
status
string
Current status: active, expired, or used
percentage
number
Updated percentage discount value (1-100, null for fixed amount)
fixedAmountsPerCurrency
array

Show child properties
applicableCycles
number
Updated number of billing cycles discount applies to (null for infinite)
availableUses
number
Updated maximum number of times coupon can be used (null for unlimited)
lastArchivedAt
string
Timestamp when coupon was last archived (null if never archived)
lastUnarchivedAt
string
Timestamp when coupon was last unarchived (null if never unarchived)
isArchived
boolean
Whether coupon is currently archived and unavailable for use
createdAt
string
ISO 8601 timestamp when coupon was created (unchanged)
Update coupon usage limits
PUT
https://api.rebill.com/v3/coupons/:id
curl -X PUT https://api.rebill.com/v3/coupons/:id \
-H "accept: application/json" \
-H "content-type: application/json" \
{% raw %}-H "x-api-key: {{API_KEY}}" \{% endraw %}
-d '{
"availableUses": 50,
"expirationDate": "2024-11-26T00:00:00Z"
}'

Copy
Copied!
Response
{
  "id": "cpn_64d92e630b054c60ba083a8ac543f63e",
  "name": "10% OFF Descount",
  "description": "10% OFF Descount",
  "notes": null,
  "format": "PERCENTAGE",
  "code": "CODE10",
  "productIds": [],
  "planIds": [],
  "paymentLinkIds": [],
  "customerId": null,
  "expirationDate": "2024-11-26",
  "redemptions": 0,
  "status": "active",
  "percentage": 10,
  "fixedAmountsPerCurrency": null,
  "applicableCycles": 5,
  "availableUses": 50,
  "lastArchivedAt": null,
  "lastUnarchivedAt": null,
  "isArchived": false,
  "createdAt": "2025-09-03T18:56:07.639Z"
}

Copy
Copied!
PUT
/v3/coupons/:id/archive
Archive a coupon
Archive a coupon to prevent further usage while preserving historical data. Sets isArchived: true and prevents new redemptions.

Headers
x-api-key
string
required
{% raw %}API key for authentication. Format: x-api-key: {{API_KEY}}{% endraw %}

Required Path Parameters
id
string
required
Coupon ID to archive

Response
Returns 200 on success with empty response body.

Archive a coupon
PUT
https://api.rebill.com/v3/coupons/:id/archive
curl -X PUT https://api.rebill.com/v3/coupons/:id/archive \
{% raw %}-H "x-api-key: {{API_KEY}}"{% endraw %}

Copy
Copied!
Response
200 OK

Copy
Copied!
PUT
/v3/coupons/:id/unarchive
Unarchive a coupon
Reactivate an archived coupon. Sets isArchived: false and allows new redemptions again.

Headers
x-api-key
string
required
{% raw %}API key for authentication. Format: x-api-key: {{API_KEY}}{% endraw %}

Required Path Parameters
id
string
required
Coupon ID to unarchive

Reactivate an archived coupon
PUT
https://api.rebill.com/v3/coupons/:id/unarchive
curl -X PUT https://api.rebill.com/v3/coupons/:id/unarchive \
-H "accept: application/json" \
-H "content-type: application/json" \
{% raw %}-H "x-api-key: {{API_KEY}}"{% endraw %}

Copy
Copied!
Response
200 OK

Copy
Copied!
DELETE
/v3/coupons/:id
Delete a coupon
Permanently delete a coupon. This action cannot be undone.

Headers
x-api-key
string
required
{% raw %}API key for authentication. Format: x-api-key: {{API_KEY}}{% endraw %}

Required Path Parameters
id
string
required
Coupon ID to delete

Delete a coupon permanently
DELETE
https://api.rebill.com/v3/coupons/:id
curl -X DELETE https://api.rebill.com/v3/coupons/:id \
-H "accept: application/json" \
-H "content-type: application/json" \
{% raw %}-H "x-api-key: {{API_KEY}}"{% endraw %}

Copy
Copied!
Response
200 OK

Customers
Manage customer details, payment methods and compliance information in a single API. Store customer profiles, handle KYC requirements and manage payment methods with local compliance in mind.

GET
/v3/customers/:id
Get customer by ID
Headers
x-api-key
string
required
{% raw %}API key for authentication. Format: x-api-key: {{API_KEY}}{% endraw %}

Fetch a customer's complete profile including payment methods, addresses and KYC data.

Required Path Parameters
id
string
required
Customer ID (starts with cus_)

Response Fields
id
string
Unique customer identifier

firstName
string
Customer's first name

lastName
string
Customer's last name

email
string
Customer's email address

phoneNumbers
array

Show child properties
addresses
array

Show child properties
identifications
array

Show child properties
cards
array

Show child properties
createdAt
string
Customer creation timestamp in ISO 8601 format

The response includes all associated payment methods, addresses and identification documents. Use this endpoint when you need the complete customer profile.

Get customer profile
GET
https://api.rebill.com/v3/customers/:id
curl -X GET https://api.rebill.com/v3/customers/:id \
        {% raw %}-H "x-api-key: {{API_KEY}}" \{% endraw %}
        -H "accept: application/json"

Copy
Copied!
Response
  {
    "id": "cust_4aae7f62e74a6fbd3ed9328e522746",
    "firstName": "John",
    "lastName": "Doe",
    "email": "john.doe@example.com",
    "phoneNumbers": [
      {
        "countryCode": "1",
        "number": "55550123"
      }
    ],
    "addresses": [
      {
        "id": "addr_9c4e5dbdc52445f89a32e2ab9e7ad5",
        "street": "123 Market St",
        "city": "San Francisco",
        "state": "CA",
        "country": "US",
        "zipCode": "94105",
        "extraInfo": "Suite 100"
      }
    ],
    "identifications": [
      {
        "id": "id_5545d29cf4269914b1d233045fb57",
        "type": "DNI",
        "value": "12345678"
      }
    ],
    "cards": [
      {
        "id": "card_a9a162530e164b1881eed4652ebc6b",
        "lastFourDigits": "4242",
        "brand": "visa",
        "expirationMonth": "12",
        "expirationYear": "2025",
        "isDefault": true
      }
    ],
    "createdAt": "2024-01-01T10:00:00.000Z"
  }

Copy
Copied!
POST
/v3/customers
Create customer
Create a new customer profile with personal information, contact details, and compliance data. This endpoint allows you to store customer information for future payments and compliance requirements.

Headers
x-api-key
string
required
{% raw %}API key for authentication. Format: x-api-key: {{API_KEY}}{% endraw %}

Request Body Parameters
firstName
string
required
Customer's legal first name (as it appears on official documents)

lastName
string
required
Customer's legal last name (as it appears on official documents)

email
string
required
Valid email address where receipts and notifications will be sent

Response
id
string
Unique customer identifier (starts with cus_)

firstName
string
Customer's first name

lastName
string
Customer's last name

email
string
Customer's email address

phoneNumbers
array

Show child properties
addresses
array

Show child properties
identifications
array

Show child properties
createdAt
string
Customer creation timestamp in ISO 8601 format

updatedAt
string
Last update timestamp in ISO 8601 format

Note: All personal information is stored securely and used for compliance and fraud prevention. Make sure to collect only the data you need for your business requirements.

Create customer with complete profile
POST
https://api.rebill.com/v3/customers
curl -X POST https://api.rebill.com/v3/customers \
        {% raw %}-H "x-api-key: {{API_KEY}}" \{% endraw %}
        -H "Content-Type: application/json" \
        -d '{
          "firstName": "Dario",
          "lastName": "Gomez",
          "email": "dariogomez@gmail.com",
          "phoneNumbers": [
            {
              "number": "5551234567",
              "countryCode": "52"
            },
            {
              "number": "3001234567",
              "countryCode": "57"
            }
          ],
          "addresses": [
            {
              "country": "CO",
              "state": "Cundinamarca",
              "city": "Bogotá",
              "zipCode": "110111",
              "lineOne": "Carrera 15 #93-47",
              "lineTwo": "Torre A, Piso 8"
            }
          ],
          "identifications": [
            {
              "type": "DNI",
              "value": "12345678"
            }
          ]
        }'

Copy
Copied!
Response
  {
    "id": "test_cus_90fa7a3726de41db848458da33ed682a",
    "firstName": "DAN",
    "lastName": "Gomez",
    "email": "dariogomez@gmail.com",
    "phoneNumbers": [
      {
        "number": "5551234567",
        "countryCode": "52"
      },
      {
        "number": "3001234567",
        "countryCode": "57"
      }
    ],
    "addresses": [
      {
        "id": "test_addr_colombia_1234567890abcdef",
        "country": "CO",
        "state": "Cundinamarca",
        "city": "Bogotá",
        "zipCode": "110111",
        "lineOne": "Carrera 15 #93-47",
        "lineTwo": "Torre A, Piso 8"
      }
    ],
    "identifications": [
      {
        "id": "test_id_1234567890abcdef",
        "type": "DNI",
        "value": "12345678"
      }
    ],
    "createdAt": "2024-01-15T10:30:00.000Z",
    "updatedAt": "2024-01-15T10:30:00.000Z"
  }

Copy
Copied!
POST
/v3/customers/search
List customers
Filter and paginate through your customer base. Use this endpoint to find customers by email, name, country or creation date.

Headers
x-api-key
string
required
{% raw %}API key for authentication. Format: x-api-key: {{API_KEY}}{% endraw %}

Required Body Parameters
pagination
object
required

Show child properties
filters
object

Show child properties
search
string
Full-text search across customer name and email fields.

Response
records
array

Show child properties
pagination
object

Show child properties
Note: The search parameter uses full-text search, while individual filters use exact matches. Use search for fuzzy matching and filters for precise queries.

List customers with filters
POST
https://api.rebill.com/v3/customers/search
curl -X POST https://api.rebill.com/v3/customers/search \
        {% raw %}-H "x-api-key: {{API_KEY}}" \{% endraw %}
        -H "Content-Type: application/json" \
        -d '{
          "pagination": {
              "limit": 10,
              "offset": 0
          },
          "filters": {
              "firstName": "Ana",
              "billingCountries": [
                  "AR"
              ],
              "createdAt": {
                  "startDate": "2025-09-01",
                  "endDate": "2025-09-04"
              }
          }
      }'

Copy
Copied!
Response
  {
  "records": [
      {
          "id": "cus_e27056aff31f42119b60d6c3b32711a1",
          "firstName": "Ana",
          "lastName": "López",
          "email": "ana@example.com",
          "phoneNumbers": [
              {
                  "number": "4422345894",
                  "countryCode": "54"
              }
          ],
          "addresses": [
              {
                  "id": "addr_df4b253df2a44d7382cba290c466e694",
                  "country": "AR",
                  "state": "Chaco",
                  "city": "Resistencia",
                  "zipCode": "H3506",
                  "lineOne": "2270 Avenida 25 de Mayo",
                  "lineTwo": null
              }
          ],
          "identifications": [
              {
                  "id": "id_455d075c265845a89d0ed93f91945a39",
                  "type": "DNI",
                  "value": "45840443"
              }
          ],
          "cards": [
              {
                  "id": "crd_dc8fff72bbe44c88aff70d885f4dc3df",
                  "createdAt": "2025-09-03T14:11:16.173Z",
                  "name": "Ana López",
                  "bin": "425821",
                  "brand": "visa",
                  "type": "credit",
                  "lastFour": "4094",
                  "status": "operative",
                  "expiration": {
                      "month": "08",
                      "year": "2030"
                  }
              }
          ],
          "createdAt": "2025-09-03T14:11:10.905Z"
      },
      {
          "id": "cus_47cd778f3a7c425986c6c59e75263b7f",
          "firstName": "Ana",
          "lastName": "Fernandez",
          "email": "anafernandez@example.com",
          "phoneNumbers": [
              {
                  "number": "3622345894",
                  "countryCode": "54"
              }
          ],
          "addresses": [
              {
                  "id": "addr_bdeab63c669447e59f281993347c61b9",
                  "country": "AR",
                  "state": "CABA",
                  "city": "Buenos Aires",
                  "zipCode": "C1043AAZ",
                  "lineOne": "Av. Corrientes 1234",
                  "lineTwo": null
              },
              {
                  "id": "addr_703e04d5c16b4ada967ea93ddea7411d",
                  "country": "AR",
                  "state": "Chaco",
                  "city": "Resistencia",
                  "zipCode": "3500",
                  "lineOne": "Av. Córdoba 4321",
                  "lineTwo": null
              }
          ],
          "identifications": [
              {
                  "id": "id_e32a04e1cdbc4b2db3d88301740078d8",
                  "type": "DNI",
                  "value": "43736789"
              }
          ],
          "cards": [
              {
                  "id": "crd_0ac76662295d49dd83e28ed7a3eace4f",
                  "createdAt": "2025-09-02T22:15:15.047Z",
                  "name": "Ana Fernandez",
                  "bin": "450799",
                  "brand": "visa",
                  "type": "credit",
                  "lastFour": "4905",
                  "status": "operative",
                  "expiration": {
                      "month": "08",
                      "year": "2030"
                  }
              }
          ],
          "createdAt": "2025-09-02T22:15:08.064Z"
      }
  ],
  "pagination": {
      "totalItems": 2,
      "totalPages": 1,
      "currentPage": 1,
      "itemsPerPage": 10,
      "hasNextPage": false,
      "hasPreviousPage": false
  }
}

Copy
Copied!
PATCH
/customers/:id
Update a customer
Headers
x-api-key
string
required
{% raw %}API key for authentication. Format: x-api-key: {{API_KEY}} API key for authentication. Format: x-api-key: {{API_KEY}}{% endraw %}

Update customer profile fields. Only included fields are updated.

Required Path Parameters
id
string
required
Customer ID (starts with cus_)

Request Body Parameters
email
string
Valid email address

firstName
string
First name

lastName
string
Last name

phoneNumbers
array

Show child properties
identifications
array

Show child properties
shippingAddresses
array

Show child properties
Response
id
string
Unique customer identifier

firstName
string
Updated customer's first name

lastName
string
Updated customer's last name

email
string
Updated customer's email address

phoneNumbers
array

Show child properties
addresses
array

Show child properties
identifications
array

Show child properties
createdAt
string
Original customer creation timestamp in ISO 8601 format

Note: When updating arrays (phoneNumbers, identifications, addresses), you must send the complete array. Partial updates are not supported.

Update customer profile
PATCH
https://api.rebill.com/v3/customers/:id
curl -X PATCH https://api.rebill.com/v3/customers/:id \
        {% raw %}-H "x-api-key: {{API_KEY}}" \{% endraw %}
        {% raw %}-H "x-api-key: {{API_KEY}}" \{% endraw %}
        -H "Content-Type: application/json" \
        -d '{
          "firstName": "John",
          "lastName": "Doe",
          "email": "john.doe@example.com",
          "phoneNumbers": [
            {
              "countryCode": "1",
              "number": "55550123"
              "number": "55550123"
            }
          ],
          "identifications": [
            {
              "type": "DNI",
              "value": "12345678"
            }
          ],
          "shippingAddresses": [
            {
              "street": "123 Market St",
              "city": "San Francisco",
              "state": "CA",
              "country": "US",
              "zipCode": "94105",
              "extraInfo": "Suite 100"
            }
          ]
        }'

Copy
Copied!
Response
  {
    "id": "cust_4aae7f62e74a6fbd3ed9328e522746",
    "firstName": "John",
    "lastName": "Doe",
    "email": "john.doe@example.com",
    "phoneNumbers": [
      {
        "countryCode": "1",
        "number": "55550123"
        "number": "55550123"
      }
    ],
    "addresses": [
      {
        "id": "addr_9c4e5dbdc52445f89a32e2ab9e7ad5",
        "street": "123 Market St",
        "city": "San Francisco",
        "state": "CA",
        "country": "US",
        "zipCode": "94105",
        "extraInfo": "Suite 100"
      }
    ],
    "identifications": [
      {
        "id": "id_5545d29cf4269914b1d233045fb57",
        "type": "DNI",
        "value": "12345678"
      }
    ],
    "createdAt": "2024-01-01T10:00:00.000Z"
  }

Copy
Copied!
GET
/v3/customers/:id/identifications
Get customer identifications
Headers
x-api-key
string
required
{% raw %}API key for authentication. Format: x-api-key: {{API_KEY}}{% endraw %}

List all KYC documents for a customer.

Required Path Parameters
id
string
required
Customer ID (starts with cus_)

Response
identifications
array

Show child properties
Use this endpoint when you only need KYC data. It's more efficient than fetching the complete customer profile.

Get customer KYC documents
GET
https://api.rebill.com/v3/customers/:id/identifications
curl -X GET https://api.rebill.com/v3/customers/:id/identifications \
        {% raw %}-H "x-api-key: {{API_KEY}}" \{% endraw %}
        -H "accept: application/json"

Copy
Copied!
Response
  [
    {
      "id": "id_5545d29cf4269914b1d233045fb57",
      "type": "DNI",
      "value": "12345678"
    }
  ]

Copy
Copied!

Plans
Plans define your subscription business model. They set pricing, billing cycles, and payment rules. Use this API to build subscription products that work with local payment methods across Latin America. Plans support both fixed pricing models to accommodate various business needs.

For a complete guide on implementing subscription plans, see our Plans Guide.

Plan object reference
All plan endpoints return this standard plan object structure:

Attributes
id
string
Unique plan identifier

name
array

Show child properties
description
array

Show child properties
status
PlanStatusEnum
Plan status: active or draft

frequency
object

Show child properties
repetitions
number
Number of billing cycles before plan ends. Set to null for unlimited repetitions.

createdAt
string
Plan creation timestamp

updatedAt
string
Last update timestamp

prices
array

Show child properties
metadata
object

Show child properties
PublicPlanFixedPrice object
id
string
Unique price identifier

currency
SupportedCurrency
Currency code (e.g., USD, ARS, CLP)

isDefault
boolean
Whether this is the default price for the plan

createdAt
string
Timestamp when the price was created

updatedAt
string
Timestamp when the price was last updated

amount
number
Price amount in minor units (e.g., cents)

setupFee
number
One-time setup fee in minor units (e.g., cents)

THE PLAN OBJECT
{
  "id": "pln_4b970527a2fe4923ba7477c0c86ec933",
  "name": [
    {
      "language": "en",
      "text": "Premium Monthly Plan"
    },
    {
      "language": "es",
      "text": "Plan Premium Mensual"
    }
  ],
  "description": [
    {
      "language": "en", 
      "text": "Premium subscription with full access"
    }
  ],
  "status": "active",
  "frequency": {
    "period": "month",
    "count": 1
  },
  "repetitions": null,
  "createdAt": "2025-01-15T10:30:00.000Z",
  "updatedAt": "2025-01-15T10:30:00.000Z",
  "prices": [
    {
      "id": "prc_4b970527a2fe4923ba7477c0c86ec933",
      "amount": 2990,
      "currency": "ARS",
      "isDefault": true,
      "createdAt": "2025-01-15T10:30:00.000Z",
      "updatedAt": "2025-01-15T10:30:00.000Z",
      "setupFee": 0
    },
    {
      "id": "prc_4b970527a2fe4923ba7477c0c86ec934",
      "amount": 1990,
      "currency": "CLP",
      "isDefault": false,
      "createdAt": "2025-01-15T10:30:00.000Z",
      "updatedAt": "2025-01-15T10:30:00.000Z",
      "setupFee": 0
    }
  ],
  "metadata": {
    "category": "premium",
    "features": "advanced_analytics,priority_support"
  }
}

Copy
Copied!
GET
/v3/plans/:id
Get plan by id
Get detailed information about a specific plan. This endpoint returns all plan details including pricing configurations for each supported currency. Use this to retrieve complete plan details for display, editing, or integration purposes.

Headers
x-api-key
string
required
{% raw %}API key for authentication. Format: x-api-key: {{API_KEY}}{% endraw %}

Path Parameters
id
string
required
Plan ID

Response
plan
object

Show child properties
Get plan details
GET
https://api.rebill.com/v3/plans/:id
curl -X GET https://api.rebill.com/v3/plans/:id 
    -H "accept: application/json"

Copy
Copied!
POST
/v3/plans
Create a plan with fixed prices
Create a subscription plan with fixed pricing. This endpoint lets you define a plan that charges the same amount each billing cycle. Fixed pricing is ideal for simple subscription models where customers pay a consistent amount regardless of usage.

Headers
x-api-key
string
required
{% raw %}API key for authentication. Format: x-api-key: {{API_KEY}}{% endraw %}

Request Body Parameters
name
array of objects
required
Plan name. You can provide the name in multiple languages.

language
string
Language code (e.g., 'en')
text
string
Text content in the specified language
frequency
object
required

Show child properties
prices
array of objects
required
Price configurations for different currencies

amount
number
Price amount in smallest currency unit (e.g., cents)
currency
string
Currency code (e.g., 'ARS', 'CLP')
isDefault
boolean
Set to true for the primary price
setupFee
number
One-time setup fee
description
array of objects
Plan description. You can provide the description in multiple languages.

language
string
Language code (e.g., 'en')
text
string
Text content in the specified language
status
string
Plan status: "active" or "draft"

repetitions
number
Number of billing cycles before plan ends (null for unlimited)

metadata
object

Show child properties
Response
plan
object

Show child properties
Create a monthly subscription plan with local pricing
POST
https://api.rebill.com/v3/plans
curl -X POST https://api.rebill.com/v3/plans \
{% raw %}-H "x-api-key: {{API_KEY}}" \{% endraw %}
-H "content-type: application/json" \
-d '{
  "name": [
    {
      "language": "en",
      "text": "Monthly Premium Plan"
    }
  ],
  "description": [
    {
      "language": "en",
      "text": "Premium subscription billed monthly"
    }
  ],
  "frequency": {
    "period": "month",
    "count": 1
  },
  "status": "active",
  "prices": [
    {
      "amount": 1990,
      "currency": "ARS",
      "isDefault": true
    },
    {
      "amount": 1790,
      "currency": "CLP"
    }
  ]
}'

Copy
Copied!
Response
{
  "id": "pln_4b970527a2fe4923ba7477c0c86ec933",
  "name": [
    {
      "language": "en",
      "text": "Monthly Premium Plan"
    }
  ],
  "description": [
    {
      "language": "en",
      "text": "Premium subscription billed monthly"
    }
  ],
  "status": "active",
  "frequency": {
    "period": "month",
    "count": 1
  },
  "repetitions": null,
  "createdAt": "2025-05-05T19:35:45.866Z",
  "updatedAt": "2025-05-05T19:35:45.866Z",
  "prices": [
    {
      "id": "prc_4b970527a2fe4923ba7477c0c86ec933",
      "amount": 1990,
      "currency": "ARS",
      "isDefault": true,
      "createdAt": "2025-05-05T19:35:45.866Z",
      "updatedAt": "2025-05-05T19:35:45.866Z",
      "setupFee": 0
    },
    {
      "id": "prc_4b970527a2fe4923ba7477c0c86ec934",
      "amount": 1790,
      "currency": "CLP",
      "isDefault": false,
      "createdAt": "2025-05-05T19:35:45.866Z",
      "updatedAt": "2025-05-05T19:35:45.866Z",
      "setupFee": 0
    }
  ],
  "metadata": {}
}

Copy
Copied!
POST
/v3/plans/search
List plans
Find plans using flexible search criteria. Filter by status, metadata, date ranges, frequency, renewal type, or use free text search across all fields.

Headers
x-api-key
string
required
{% raw %}API key for authentication. Format: x-api-key: {{API_KEY}}{% endraw %}

Search Parameters
pagination
object

Show child properties
filters
object

Show child properties
search
string
Free text search across plan names and descriptions. Supports partial matches.

Response
data
array

Show child properties
total
number
Total number of plans matching the search criteria

limit
number
Number of items per page

offset
number
Items skipped for pagination

Notes
Performance
string
Use specific filters instead of free text search when possible
Combine filters to narrow down results faster
Set reasonable pagination limits to avoid timeouts
Cache results if you need to display them frequently
Common Use Cases
string
Find all active plans in a specific currency
Search plans created in the last 30 days
Filter plans by custom metadata (e.g., category, features)
Find plans with specific billing frequency
Search active plans with local currency support
POST
https://api.rebill.com/v3/plans/search
curl -X POST https://api.rebill.com/v3/plans/search \
{% raw %}-H "x-api-key: {{API_KEY}}" \{% endraw %}
-H "content-type: application/json" \
-d '{
  "pagination": {
    "limit": 10,
    "offset": 0,
    "sort": "created_at",
    "order": "DESC"
  },
  "filters": {
    "status": [
      "active"
    ]
  }
}'

Copy
Copied!
Response
{
  "data": [
    {
      "id": "test_pln_821a91ff9b264bfb8a2fceaa092e9a21",
      "name": [
        {
          "text": "AWS advanced course",
          "language": "en"
        },
        {
          "text": "Curso avanzado de AWS",
          "language": "es"
        }
      ],
            "description": [
                {
                    "text": "Monthly subscription to AWS advanced course",
                    "language": "en"
                },
                {
                    "text": "Subscripción mensual a curso avanzado de AWS",
                    "language": "es"
                }
            ],
            "status": "active",
            "frequency": {
                "period": "month",
                "count": 1
            },
            "repetitions": null,
            "createdAt": "2025-09-03T21:48:02.421Z",
            "updatedAt": "2025-09-03T21:48:02.421Z",
            "prices": [
                {
                    "id": "prc_821a91ff9b264bfb8a2fceaa092e9a21",
                    "amount": 1990,
                    "currency": "ARS",
                    "isDefault": true,
                    "createdAt": "2025-09-03T21:48:02.421Z",
                    "updatedAt": "2025-09-03T21:48:02.421Z",
                    "setupFee": 0
                },
                {
                    "id": "prc_821a91ff9b264bfb8a2fceaa092e9a22",
                    "amount": 1790,
                    "currency": "CLP",
                    "isDefault": false,
                    "createdAt": "2025-09-03T21:48:02.421Z",
                    "updatedAt": "2025-09-03T21:48:02.421Z",
                    "setupFee": 0
                }
            ],
            "metadata": {}
        },
        {
            "id": "test_pln_7b60d18b54c84e1dbb875741a367210c",
            "name": [
                {
                    "text": "Amazon prime video",
                    "language": "en"
                },
                {
                    "text": "Amazon prime video",
                    "language": "es"
                },
                {
                    "text": "Amazon prime video",
                    "language": "pt"
                }
            ],
            "description": [
                {
                    "text": "Plan de subscripción a Amazon Prime Video",
                    "language": "en"
                },
                {
                    "text": "Plan de subscripción a Amazon Prime Video",
                    "language": "es"
                },
                {
                    "text": "Plan de subscripción a Amazon Prime Video",
                    "language": "pt"
                }
            ],
            "status": "active",
            "frequency": {
                "period": "month",
                "count": 2
            },
            "repetitions": 1,
            "createdAt": "2025-09-02T22:13:28.098Z",
            "updatedAt": "2025-09-02T22:18:02.681Z",
            "prices": [
                {
                    "id": "prc_7b60d18b54c84e1dbb875741a367210c",
                    "amount": 1000000,
                    "currency": "ARS",
                    "isDefault": true,
                    "createdAt": "2025-09-02T22:13:28.098Z",
                    "updatedAt": "2025-09-02T22:13:28.098Z",
                    "setupFee": 0
                }
            ],
            "metadata": {}
        }
    ],
  "total": 2,
  "limit": 10,
  "offset": 0
}

Copy
Copied!
PUT
/v3/plans/:id
Update a plan
Update an existing plan. This endpoint lets you modify any plan property. Only sent fields are updated. Use this to adjust pricing, billing frequency, or other plan attributes without affecting existing subscriptions.

Headers
x-api-key
string
required
{% raw %}API key for authentication. Format: x-api-key: {{API_KEY}}{% endraw %}

Path Parameters
id
string
required
Plan ID

Request Body Parameters
name
array of objects
Plan name in multiple languages

description
array of objects
Plan description in multiple languages

frequency
object

Show child properties
repetitions
number
Number of cycles before plan ends (null for unlimited)

usageCalculation
string
How to calculate usage (for usage-type plans)

usageUnit
string
Unit of measurement (for usage-type plans)

metadata
object

Show child properties
prices
array of objects
Price configurations. Include id to update existing prices, omit id to add new ones.

id
string
Existing price ID (for updates)
currency
string
Currency code
amount
number
Price amount (for fixed pricing)
isDefault
boolean
Boolean
setupFee
number
Initial charge
tiers
array
Array of pricing tiers (for tiered pricing)
Response
plan
object

Show child properties
Update plan pricing and frequency
PUT
https://api.rebill.com/v3/plans/:id
curl -X PUT https://api.rebill.com/v3/plans/:id \
    {% raw %}-H "x-api-key: {{API_KEY}}" \{% endraw %}
    -H "content-type: application/json" \
    -d '{
      "name": [
        {
          "language": "en",
          "text": "Updated Plan Name"
        }
      ],
      "frequency": {
        "period": "month",
        "count": 1
      },
      "usageCalculation": "SUM",
      "prices": [
        {
          "currency": "ARS",
          "amount": 29990,
          "isDefault": true
        },
        {
          "currency": "CLP",
          "amount": 24990,
          "setupFee": 500
        }
      ]
    }'

Copy
Copied!
Response
  {
    "id": "pln_ded429aa41044cd8803c81da3aa96d85",
    "name": [
      {
        "language": "en",
        "text": "Updated Plan Name"
      }
    ],
    "description": [
      {
        "language": "en",
        "text": "API access with fixed pricing based on monthly usage"
      }
    ],
    "status": "active",
    "frequency": {
      "period": "month",
      "count": 1
    },
    "repetitions": null,
    "createdAt": "2025-05-05T21:00:41.084Z",
    "updatedAt": "2025-05-05T21:08:38.934Z",
    "prices": [
      {
        "id": "prc_ded429aa41044cd8803c81da3aa96d85",
        "amount": 29990,
        "currency": "ARS",
        "isDefault": true,
        "createdAt": "2025-05-05T21:00:41.084Z",
        "updatedAt": "2025-05-05T21:08:38.934Z",
        "setupFee": 0
      }
    ],
    "metadata": {}
  }

Copy
Copied!
PATCH
/v3/plans/:id/archive
Archive a plan
Archive a plan to prevent new subscriptions. Existing subscriptions continue to work. Archived plans remain visible in your dashboard but cannot be used for new subscriptions, making this ideal for sunsetting old plans while preserving existing customer relationships.

Headers
x-api-key
string
required
{% raw %}API key for authentication. Format: x-api-key: {{API_KEY}}{% endraw %}

Path Parameters
id
string
required
Plan ID

Notes
Archived plans cannot be used for new subscriptions
Existing subscriptions continue to work
Use unarchive endpoint to reactivate
Changes plan status to "archived"
Response
plan
object

Show child properties
Archive a plan
PATCH
https://api.rebill.com/v3/plans/:id/archive
curl -X PATCH https://api.rebill.com/v3/plans/:id/archive \
    {% raw %}-H "x-api-key: {{API_KEY}}" \{% endraw %}
    -H "content-type: application/json"

Copy
Copied!
PATCH
/v3/plans/:id/unarchive
Unarchive a plan
Reactivate an archived plan. This makes the plan available for new subscriptions again. Use this when you want to bring back a previously archived plan, perhaps after making improvements or in response to customer demand.

Headers
x-api-key
string
required
{% raw %}API key for authentication. Format: x-api-key: {{API_KEY}}{% endraw %}

Path Parameters
id
string
required
Plan ID

Notes
Changes plan status back to "active"
Plan becomes available for new subscriptions
Response
plan
object

Show child properties
Reactivate an archived plan
PATCH
https://api.rebill.com/v3/plans/:id/unarchive
curl -X PATCH https://api.rebill.com/v3/plans/:id/unarchive \
{% raw %}-H "x-api-key: {{API_KEY}}" \{% endraw %}
-H "content-type: application/json"

Products
Products are the foundation of your billing infrastructure in Rebill. They represent what you sell - from SaaS subscriptions to physical goods. Each product can have multiple prices in different currencies, supporting both fixed and tiered pricing models.

Product object reference
All product endpoints return this standard product object structure:

Attributes
id
string
Unique product identifier

name
array

Show child properties
description
array

Show child properties
status
ProductStatusEnum
Product status: active or draft

prices
array

Show child properties
archivedAt
Date
Timestamp when the product was archived

unarchivedAt
Date
Timestamp when the product was unarchived

metadata
object

Show child properties
createdAt
Date
Timestamp when the product was created

updatedAt
Date
Timestamp when the product was last updated

PublicFixedPrice object
id
string
Unique price identifier

currency
SupportedCurrency
Currency code (e.g., USD, ARS, CLP)

isDefault
boolean
Whether this is the default price for the product

createdAt
Date
Timestamp when the price was created

updatedAt
Date
Timestamp when the price was last updated

amount
number
Price amount in minor units (e.g., cents)

THE PRODUCT OBJECT
  {
    "id": "prd_3ec2432fb0c446a8af280fda5fdca14a",
    "name": [
      {
        "language": "en",
        "text": "Premium Service"
      }
    ],
    "description": [
      {
        "language": "en",
        "text": "Our premium service with all features"
      }
    ],
    "status": "active",
    "prices": [
      {
        "id": "prc_3ec2432fb0c446a8af280fda5fdca14a",
        "amount": 1990,
        "currency": "ARS",
        "isDefault": true,
        "createdAt": "2025-05-01T00:31:28.733Z",
        "updatedAt": "2025-05-01T00:31:28.733Z"
      }
    ],
    "metadata": {
      "category": "SaaS"
    },
    "createdAt": "2025-05-01T00:31:28.733Z",
    "updatedAt": "2025-05-01T00:31:28.733Z"
  }

Copy
Copied!
GET
/v3/products/:id
Get product by id
Retrieve a specific product's details, including its pricing structure and metadata. Use this endpoint to fetch complete product information for display or processing.

Headers
x-api-key
string
required
{% raw %}API key for authentication. Format: x-api-key: {{API_KEY}}{% endraw %}

Path Parameters
id
string
required
The product's unique identifier (starts with 'prd_')

Response
product
object

Show child properties
Notes
Common Use Cases
string
Display product details in your admin dashboard
Fetch pricing for order processing
Verify product status before creating subscriptions
Update product information in your local database
Get product details by ID
GET
https://api.rebill.com/v3/products/:id
curl -X GET https://api.rebill.com/v3/products/:id \
-H "accept: application/json" \
{% raw %}-H "x-api-key: {{API_KEY}}" \{% endraw %}
-H "content-type: application/json"

Copy
Copied!
Response
{
  "id": "prd_cd55b3a26d894b77b30101c00e3ef983",
  "name": [
    {
      "language": "en",
      "text": "Enterprise API Access"
    }
  ],
  "description": [
    {
      "language": "en",
      "text": "API access with tiered pricing based on usage"
    }
  ],
  "status": "active",
  "prices": [
    {
      "id": "prc_cd55b3a26d894b77b30101c00e3ef983",
      "amount": 10000,
      "currency": "ARS",
      "isDefault": true,
      "createdAt": "2025-05-02T18:09:35.838Z",
      "updatedAt": "2025-05-02T18:09:35.838Z"
    }
  ],
  "metadata": {},
  "createdAt": "2025-05-02T18:09:35.838Z",
  "updatedAt": "2025-05-02T18:09:35.838Z"
}

Copy
Copied!
POST
/v3/products
Create a product
Create a product with its pricing structure. Each product requires at least one price in a supported currency.

Headers
x-api-key
string
required
{% raw %}API key for authentication. Format: x-api-key: {{API_KEY}}{% endraw %}

Request Body Parameters
name
array of objects
required
language
string
Language code (e.g., 'en', 'es')
text
string
Product name in that language
description
array of objects
language
string
Language code (e.g., 'en', 'es')
text
string
Product description in that language
status
ProductStatusEnum
Product status: "active" for immediate use, "draft" for testing, "archived" to hide from customers. Defaults to "draft" if not provided.

metadata
object

Show child properties
prices
array of objects
required
Array of product prices. At least one price must be defined, and at least one must be set as default.

id
string
Optional price identifier. If not provided, one will be generated.
amount
number
Price amount in minor units (e.g., cents). Must be greater than or equal to 0.
currency
SupportedCurrency
Currency code (e.g., ARS, COP, CLP)
isDefault
boolean
Whether this is the default price. Defaults to false if not provided.
Response
product
object

Show child properties
Notes
Authentication
string
Requires a valid bearer token with appropriate permissions

Always set prices in minor units (cents) to avoid floating-point issues
At least one price must be defined
At least one price must be set as default (isDefault: true)
Amount must be greater than or equal to 0
Products in "draft" status won't appear in customer-facing APIs
Archived products can't be used for new purchases but preserve historical data
Create a product
POST
https://api.rebill.com/v3/products
curl -X POST https://api.rebill.com/v3/products \
-H "accept: application/json" \
-H "content-type: application/json" \
{% raw %}-H "x-api-key: {{API_KEY}}" \{% endraw %}
-d '{
  "name": [
    {
      "language": "en",
      "text": "Premium Service"
    }
  ],
  "description": [
    {
      "language": "en",
      "text": "Our premium service with all features"
    }
  ],
  "status": "active",
  "prices": [
    {
      "amount": 1990,
      "currency": "ARS",
      "isDefault": true
    }
  ]
}'

Copy
Copied!
Response
{
  "id": "prd_3ec2432fb0c446a8af280fda5fdca14a",
  "name": [
    {
      "language": "en",
      "text": "Premium Service"
    }
  ],
  "description": [
    {
      "language": "en",
      "text": "Our premium service with all features"
    }
  ],
  "status": "active",
  "prices": [
    {
      "id": "prc_3ec2432fb0c446a8af280fda5fdca14a",
      "amount": 1990,
      "currency": "ARS",
      "isDefault": true,
      "createdAt": "2025-05-01T00:31:28.733Z",
      "updatedAt": "2025-05-01T00:31:28.733Z"
    }
  ],
  "metadata": {},
  "createdAt": "2025-05-01T00:31:28.733Z",
  "updatedAt": "2025-05-01T00:31:28.733Z"
}

Copy
Copied!
POST
/v3/products/search
List products
Find products using flexible search criteria. Filter by pricing mode, metadata, date ranges, or use free text search across all fields.

Headers
x-api-key
string
required
{% raw %}API key for authentication. Format: x-api-key: {{API_KEY}}{% endraw %}

Search Parameters
pagination
object

Show child properties
filters
object

Show child properties
search
string
Free text search across product names and descriptions. Supports partial matches.

Response
products
array

Show child properties
Notes
Performance
string
Use specific filters instead of free text search when possible
Combine filters to narrow down results faster
Set reasonable pagination limits to avoid timeouts
Cache results if you need to display them frequently
Common Use Cases
string
Find all active products in a specific currency
Search products created in the last 30 days
Filter products by custom metadata (e.g., category, SKU)
Get all products with tiered pricing
List active SaaS products with fixed pricing in ARS
POST
https://api.rebill.com/v3/products/search
curl -X POST https://api.rebill.com/v3/products/search \
-H "accept: application/json" \
-H "content-type: application/json" \
{% raw %}-H "x-api-key: {{API_KEY}}" \{% endraw %}
-d '{
  "pagination": {
    "limit": 10,
    "offset": 0,
    "sort": "created_at",
    "order": "DESC"
  },
  "filters": {
    "metadata": {
      "category": "SaaS"
    },
    "createdAt": {
      "startDate": "2024-01-01T00:00:00Z",
      "endDate": "2024-12-31T23:59:59Z"
    },
    "status": ["active"],
    "currencies": ["ARS"]
  },
  "search": "premium"
}'

Copy
Copied!
Response
{
  "data": [
    {
      "id": "prd_52b0d61e4d79422885535a6a3794f89e",
      "name": [
        {
          "language": "en",
          "text": "Blue Premium Package"
        }
      ],
      "description": [
        {
          "language": "en",
          "text": "Premium product with additional features"
        }
      ],
      "status": "active",
      "prices": [
        {
          "id": "prc_52b0d61e4d79422885535a6a3794f89e",
          "amount": 15000,
          "currency": "ARS",
          "isDefault": true,
          "createdAt": "2024-02-15T10:25:28.769Z",
          "updatedAt": "2024-03-19T14:32:45.112Z"
        }
      ],
      "metadata": {
        "category": "SaaS",
        "SKU": "BLU-PREM-001"
      },
      "createdAt": "2024-02-15T10:25:28.769Z",
      "updatedAt": "2024-03-19T14:32:45.112Z"
    },
    {
      "id": "prd_a1b2c3d4e5f6422885535a6a3794f89e",
      "name": [
        {
          "language": "en",
          "text": "Enterprise API Access"
        }
      ],
      "description": [
        {
          "language": "en",
          "text": "API access with tiered pricing based on usage"
        }
      ],
      "status": "active",
      "prices": [
        {
          "id": "prc_a1b2c3d4e5f6422885535a6a3794f89e",
          "amount": 5000,
          "currency": "ARS",
          "isDefault": true,
          "createdAt": "2024-03-01T08:15:22.123Z",
          "updatedAt": "2024-03-19T14:32:45.112Z"
        }
      ],
      "metadata": {
        "category": "API",
        "maxRequests": 1000000
      },
      "createdAt": "2024-03-01T08:15:22.123Z",
      "updatedAt": "2024-03-19T14:32:45.112Z"
    }
  ],
  "total": 2,
  "limit": 10,
  "offset": 0
}

Copy
Copied!
PUT
/v3/products/:id
Update a product
Modify an existing product's properties. Update names, descriptions, metadata, or prices. All fields are optional - only included fields will be updated.

Headers
x-api-key
string
required
{% raw %}API key for authentication. Format: x-api-key: {{API_KEY}}{% endraw %}

Path Parameters
id
string
required
The product's unique identifier (starts with 'prd_')

Request Body Parameters
name
array of objects
language
string
Language code (e.g., 'en', 'es')
text
string
Updated product name
description
array of objects
language
string
Language code (e.g., 'en', 'es')
text
string
Updated product description
metadata
object

Show child properties
prices
array of objects
Update product prices. If provided, at least one price must be defined, and at least one must be set as default.

id
string
Optional price identifier. If not provided, one will be generated.
amount
number
Price amount in minor units (e.g., cents). Must be greater than or equal to 0.
currency
SupportedCurrency
Currency code (e.g., ARS, COP, CLP)
isDefault
boolean
Whether this is the default price. Defaults to false if not provided.
Response
product
object

Show child properties
Implementation Notes
Update Rules
string
Only included fields will be updated - omitted fields remain unchanged
All fields are optional - include only the fields you want to update
When updating prices, at least one price must be defined, and at least one must be set as default
Price amount must be greater than or equal to 0
Metadata updates are merged with existing values
Common Use Cases
string
Update product information for new markets
Modify product prices or add new currencies
Add or update custom metadata fields
Update product descriptions in multiple languages
Update product name, description, metadata, and prices
PUT
https://api.rebill.com/v3/products/:id
curl -X PUT https://api.rebill.com/v3/products/:id \
-H "accept: application/json" \
-H "content-type: application/json" \
{% raw %}-H "x-api-key: {{API_KEY}}" \{% endraw %}
-d '{
  "name": [
    {
      "language": "en",
      "text": "Premium Enterprise Service Updated"
    },
    {
      "language": "es",
      "text": "Servicio Premium Empresarial Actualizado"
    }
  ],
  "description": [
    {
      "language": "en",
      "text": "Updated enterprise service description"
    }
  ],
  "metadata": {
    "category": "enterprise",
    "featured": true
  },
  "prices": [
    {
      "amount": 25000,
      "currency": "ARS",
      "isDefault": true
    }
  ]
}'

Copy
Copied!
Response
{
  "id": "prd_f87da711a05c494cb82cdac5d5911f24",
  "name": [
    {
      "language": "en",
      "text": "Premium Enterprise Service Updated"
    },
    {
      "language": "es",
      "text": "Servicio Premium Empresarial Actualizado"
    }
  ],
  "description": [
    {
      "language": "en",
      "text": "Updated enterprise service description"
    }
  ],
  "status": "active",
  "prices": [
    {
      "id": "prc_f87da711a05c494cb82cdac5d5911f24",
      "amount": 25000,
      "currency": "ARS",
      "isDefault": true,
      "createdAt": "2025-05-02T22:05:27.301Z",
      "updatedAt": "2025-05-02T22:05:27.301Z"
    }
  ],
  "metadata": {
    "category": "enterprise",
    "featured": true
  },
  "createdAt": "2025-05-02T22:05:27.301Z",
  "updatedAt": "2025-05-02T22:53:17.968Z"
}

Copy
Copied!
PATCH
/v3/products/:id/archive
Archive a product
Archive a product to hide it from customers while preserving its data. Archived products can't be used for new purchases but maintain their historical records.

Path Parameters
id
string
required
The product's unique identifier (starts with 'prd_')

Implementation Notes
Archive Behavior
string
Product becomes invisible to customers immediately
Existing subscriptions continue to work normally
Historical data and analytics remain accessible
Product can be unarchived later if needed
Associated plans remain active unless archived separately
Common Use Cases
string
Seasonal product management
Discontinue products without losing data
Hide products during maintenance
Prepare for product updates
Archive a product
PATCH
https://api.rebill.com/v3/products/:id/archive
curl -X PATCH https://api.rebill.com/v3/products/:id/archive \
-H "accept: application/json" \
{% raw %}-H "x-api-key: {{API_KEY}}" \{% endraw %}
-H "content-type: application/json"

Copy
Copied!
Response
OK 200

Copy
Copied!
PATCH
/v3/products/:id/unarchive
Unarchive a product
Restore an archived product to make it available for purchases again. The product returns to its previous state with all its original configuration.

Path Parameters
id
string
required
The product's unique identifier (starts with 'prd_')

Implementation Notes
Unarchive Behavior
string
Product becomes visible to customers immediately
Returns to its previous active state
All pricing and configuration is restored
Associated plans need to be unarchived separately
Product history and analytics are preserved
Common Use Cases
string
Restore seasonal products
Bring back discontinued products
Reactivate products after maintenance
Resume product availability
Unarchive a product
PATCH
https://api.rebill.com/v3/products/:id/unarchive
curl -X PATCH https://api.rebill.com/v3/products/:id/unarchive \
-H "accept: application/json" \
{% raw %}-H "x-api-key: {{API_KEY}}" \{% endraw %}
-H "content-type: application/json"

Copy
Copied!
Response
OK 200

Copy
Copied!


Payments
Build payment infrastructure that scales across Latin America. Rebill's Payments API gives you programmatic access to search, retrieve, and export payment details with enterprise-grade reliability.

Payment object reference
All payment endpoints return this standard payment object structure:

Attributes
id
string
Payment's unique identifier

createdAt
Date
Payment creation timestamp

updatedAt
Date
Last update timestamp

organizationId
string
Organization that owns this payment

amount
number
Payment amount in smallest currency unit (e.g., cents)

currency
string
Payment currency code (e.g., USD, ARS, CLP)

customer
object

Show child properties
status
string
Payment status (approved, rejected, pending)

metadata
object

Show child properties
paymentMethodType
string
Type of payment method used. Possible values:

cash
card
bank_transfer
card
object

Show child properties
quantity
number
Item quantity purchased

installments
number
Number of installments

couponId
string
Applied coupon identifier

description
string
Payment description

discount
object

Show child properties
processingMode
string
Processing mode (local or crossborder)

errorDetail
string
Detailed error message if payment failed

errorType
string
Type of error if payment failed

subscriptionId
string
Associated subscription identifier

country
string
ISO country code where the payment was made

timezone
string
Timezone where the payment was made

traceId
string
Unique identifier for tracking this payment operation

type
string
Payment type:

one_time_payment: A payment generated through a product or an instant link.
manual_one_time_payment: A payment generated from the dashboard by the merchant to a customer who already has a tokenized card. For example, generated from a customer detail page.
manual_subscription_payment: A payment generated from the dashboard in the subscription section where a charge is forced.
first_subscription_payment: A payment from which a subscription is generated.
recurring_subscription_payment: A payment generated from a subscription's recurrence.
retry_subscription_payment: A payment generated from a subscription that is retrying a rejected charge in the recurrence of its current cycle.
origin
string
Origin of the payment: sdk, checkout_landing, api, dashboard, automatic

oneClick
boolean
Whether the customer used an OTP (One-Time Password) to authenticate the payment

Customer Object Fields
customer
object

Show child properties
Card Object Fields
card
object

Show child properties
Discount Object Fields
discount
object

Show child properties
THE PAYMENT OBJECT
{
  "id": "pay_d03f9b0c037f44e99107210bc39184fd",
  "createdAt": "2025-05-15T16:56:06.603Z",
  "updatedAt": "2025-05-15T16:56:06.603Z",
  "organizationId": "org_8fa0d70f8ab54c7d8e54bc356422b2bd",
  "amount": 10000,
  "currency": "ARS",
  "customer": {
    "id": "cus_08d93677c7ca45abbea1a0dc21b85aed",
    "email": "john.doe@example.com",
    "firstName": "John",
    "lastName": "Doe",
    "defaultLanguage": "es",
    "phone": "+5491123456789"
  },
  "status": "approved",
  "metadata": null,
  "paymentMethodType": "card",
  "card": {
    "id": "crd_99b867433c3c46759ad14f5ae9046894",
    "brand": "visa",
    "type": "credit",
    "lastFourDigits": "1111",
    "name": "John Doe"
  },
  "quantity": 1,
  "installments": null,
  "couponId": null,
  "description": "Premium Plan",
  "discount": null,
  "processingMode": "local",
  "errorDetail": null,
  "errorType": null,
  "subscriptionId": null,
  "country": "AR",
  "timezone": "America/Argentina/Buenos_Aires",
  "traceId": "trace_1234567890",
  "type": "one_time_payment",
  "origin": "sdk",
  "oneClick": true
}

Copy
Copied!
GET
/v3/payments/:id
Get payment by ID
Retrieve a specific payment's complete data. Use this endpoint to build detailed payment views or handle webhook events.

Headers
x-api-key
string
required
{% raw %}API key for authentication. Format: x-api-key: {{API_KEY}}{% endraw %}

Path Parameters
id
string
required
Payment's unique identifier

Response
payment
object

Show child properties
Example request for retrieving payment information
GET
https://api.rebill.com/v3/payments/:id
curl -X GET https://api.rebill.com/v3/payments/:id 
      -H "accept: application/json" \
      {% raw %}-H "x-api-key: {{API_KEY}}"{% endraw %}

Copy
Copied!
Response
  {
    "id": "pay_d03f9b0c037f44e99107210bc39184fd",
    "createdAt": "2025-05-15T16:56:06.603Z",
    "updatedAt": "2025-05-15T16:56:06.603Z",
    "organizationId": "org_8fa0d70f8ab54c7d8e54bc356422b2bd",
    "amount": 10000,
    "currency": "ARS",
    "customer": {
      "id": "cus_08d93677c7ca45abbea1a0dc21b85aed",
      "email": "john.doe@example.com",
      "firstName": "John",
      "lastName": "Doe",
      "defaultLanguage": "es",
      "phone": "+5491123456789"
    },
    "status": "approved",
    "metadata": null,
    "paymentMethodType": "card",
    "card": {
      "id": "crd_99b867433c3c46759ad14f5ae9046894",
      "brand": "visa",
      "type": "credit",
      "lastFourDigits": "1111",
      "name": "John Doe"
    },
    "quantity": 1,
    "installments": null,
    "couponId": null,
    "description": "Premium Plan",
    "discount": null,
    "processingMode": "local",
    "fees": [
      {
        "id": "fee_c789",
        "feeRuleId": "frule_d01",
        "amount": 5.0,
        "currency": "USD",
        "description": "Service fee",
        "percentageAmount": 5.0,
        "fixedAmount": 0,
        "type": "financing"
      }
    ],
    "taxes": [
      {
        "id": "tax_c789",
        "taxRuleId": "trule_d01",
        "amount": 0.50,
        "currency": "USD",
        "description": "Tax on service fee",
        "percentageAmount": 10,
        "fixedAmount": 0,
        "feeAppliedId": "fee_c789",
        "name": "VAT"
      }
    ],
    "exchangeRate": 1,
    "netAmount": 95,
    "currencyNetAmount": "USD",
    "errorDetail": null,
    "errorType": null,
    "isProviderError": false,
    "subscriptionId": null,
    "country": "US",
    "timezone": "America/New_York",
    "traceId": "trace_1234567890",
    "type": "one_time_payment",
    "origin": "api",
    "oneClick": false
  }

Copy
Copied!
POST
/v3/payments/search
List payments
Search and filter payments with advanced filtering options.

Headers
x-api-key
string
required
{% raw %}API key for authentication. Format: x-api-key: {{API_KEY}}{% endraw %}

Request Body Parameters
filters
object

Show child properties
search
string
General search term

pagination
object

Show child properties
Response
records
array

Show child properties
pagination
object

Show child properties
Example request for searching payments
POST
https://api.rebill.com/v3/payments/search
curl -X POST https://api.rebill.com/v3/payments/search \
      -H "accept: application/json" \
      {% raw %}-H "x-api-key: {{API_KEY}}" \{% endraw %}
      -H "content-type: application/json" \
      -d '{
        "filters": {
          "status": ["approved"]
        },
        "search": "",
        "pagination": {
          "limit": 10,
          "offset": 0,
          "sort": "created_at",
          "order": "DESC"
        }
      }'

Copy
Copied!
Response
  {
    "records": [
      {
        "id": "pay_45c0276d0de84661b313af0877d7d7a0",
        "createdAt": "2025-05-15T16:56:06.608Z",
        "updatedAt": "2025-05-15T16:56:06.608Z",
        "organizationId": "org_8fa0d70f8ab54c7d8e54bc356422b2bd",
        "amount": 5000,
        "currency": "ARS",
        "customer": {
          "id": "cus_08d93677c7ca45abbea1a0dc21b85aed",
          "email": "seed-customer@example.com",
          "firstName": "Seed",
          "lastName": "Customer",
          "defaultLanguage": "es",
          "phone": "+5491123456789"
        },
        "status": "rejected",
        "metadata": null,
        "paymentMethodType": "bank_transfer",
        "quantity": 1,
        "installments": null,
        "couponId": null,
        "description": "Premium Plan",
        "discount": null,
        "processingMode": "crossborder",
        "errorDetail": "Insufficient funds",
        "errorType": "payment_error",
        "subscriptionId": null,
        "country": "AR",
        "timezone": "America/Argentina/Buenos_Aires",
        "traceId": "trace_1234567891",
        "type": "one_time_payment",
        "origin": "api",
        "oneClick": false
      },
      {
        "id": "pay_d03f9b0c037f44e99107210bc39184fd",
        "createdAt": "2025-05-15T16:56:06.603Z",
        "updatedAt": "2025-05-15T16:56:06.603Z",
        "organizationId": "org_8fa0d70f8ab54c7d8e54bc356422b2bd",
        "amount": 10000,
        "currency": "ARS",
        "customer": {
          "id": "cus_08d93677c7ca45abbea1a0dc21b85aed",
          "email": "seed-customer@example.com",
          "firstName": "Seed",
          "lastName": "Customer",
          "defaultLanguage": "es",
          "phone": "+5491123456789"
        },
        "status": "approved",
        "metadata": null,
        "paymentMethodType": "card",
        "card": {
          "id": "crd_99b867433c3c46759ad14f5ae9046894",
          "brand": "visa",
          "type": "credit",
          "lastFourDigits": "1111",
          "name": "John Doe"
        },
        "quantity": 1,
        "installments": null,
        "couponId": null,
        "description": "Premium Plan",
        "discount": null,
        "processingMode": "local",
        "errorDetail": null,
        "errorType": null,
        "subscriptionId": null,
        "country": "AR",
        "timezone": "America/Argentina/Buenos_Aires",
        "traceId": "trace_1234567890",
        "type": "one_time_payment",
        "origin": "api",
        "oneClick": false
      }
    ],
    "pagination": {
      "totalItems": 2,
      "totalPages": 1,
      "currentPage": 1,
      "itemsPerPage": 10,
      "hasNextPage": false,
      "hasPreviousPage": false
    }
  }

Copy
Copied!
POST
/v3/refunds/:paymentId
Refund a payment
Refund a card payment by its payment ID. The refund processes immediately and returns the refund status.

Headers
x-api-key
string
required
{% raw %}API key for authentication. Format: x-api-key: {{API_KEY}}{% endraw %}

Path Parameters
paymentId
string
required
The payment ID from the original transaction. Must be a successful card transaction.

Response
status
string
The refund status (e.g., refunded, pending, rejected).

Refund a payment
POST
https://api.rebill.com/v3/refunds/:paymentId
curl -X POST 'https://api.rebill.com/v3/refunds/:paymentId' \
      -H 'accept: application/json' \
      {% raw %}-H 'x-api-key: {{API_KEY}}'{% endraw %}

Copy
Copied!
Response (201 Created)
Success Response
Pending Response
Rejected Response
{
  "status": "refunded"
}

Subscriptions
Build and manage recurring revenue streams with Rebill's Subscriptions API. Process payments, handle card updates, and control subscription lifecycle events programmatically.

GET
/v3/subscriptions/:id
Get subscription by ID
Retrieve a subscription's complete state including payment history, next charge date, and customer details.

Headers
x-api-key
string
required
{% raw %}API key for authentication. Format: x-api-key: {{API_KEY}}{% endraw %}

Required Path Parameters
id
string
required
Subscription's unique identifier.

Response
id
string
Unique subscription identifier.

name
string
Subscription name.

description
string
Subscription description.

status
string
Main subscription status:

active - Active and charging
paused - Paused; no charges
retrying - Payment retry in progress
default - In default due to failed payments
cancelled - Cancelled; no future charges
finished - Completed subscription (all cycles charged)
processing - Payment or update in progress
statusDetail
string
Detailed subscription status. Possible values: - active - Active and charging

paused - Paused; no charges
cancelled - Cancelled; no future charges
finished - Completed subscription (all cycles charged)
lastChargeDate
string
Last charge date timestamp.

nextChargeDate
string
Next scheduled charge date in ISO 8601 format.

amount
number
Subscription amount in smallest currency unit.

lastChargedAmount
number
Last charged amount in smallest currency unit.

currency
string
ISO 4217 currency code (USD, ARS, EUR, etc.).

setupFee
number
Setup fee amount in smallest currency unit.

frequency
object

Hide child properties
Billing frequency configuration.

period
string
Billing interval unit:

day - Daily interval
month - Monthly interval
year - Yearly interval
count
number
Number of period units (e.g., 1 for monthly, 3 for quarterly).

billingCycles
object

Hide child properties
Billing cycle information.

total
number
Total number of billing cycles. Not present for unlimited subscriptions.

current
number
Current billing cycle number.

remaining
number
Remaining billing cycles. Not present for unlimited subscriptions.

plan
object

Hide child properties
Plan configuration and pricing details.

id
string
Plan identifier with pln_ prefix.

title
string
Human-readable plan name.

amount
number
Price per billing cycle in the smallest currency unit (e.g., cents for USD).

currency
string
ISO 4217 currency code (USD, ARS, EUR, etc.).

frequency
object

Show child properties
repetitions
number
Total number of billing cycles. null for unlimited subscriptions.

paymentMethod
string
Payment method type (e.g., card, bank_transfer, cash).

card
object

Hide child properties
Card payment details (only present for card payments).

id
string
Card identifier.

brand
string
Card brand (visa, mastercard, etc.).

type
string
Card type (credit, debit, prepaid).

lastFourDigits
string
Last 4 digits of card number.

discount
object

Hide child properties
Applied discount information (only present when a discount is active).

couponCode
string
Customer-facing coupon code (e.g., WELCOME10, SAVE20).

type
string
Discount type: fixed or percentage.

percentage
number
Percentage discount applied (if type is percentage).

amount
number
Fixed discount amount (if type is fixed).

billingCyclesToApply
object

Show child properties
customer
object

Hide child properties
Customer information.

id
string
Customer identifier with cus_ prefix.

name
string
Customer's full name.

email
string
Customer's email address.

phone
string
Customer's phone number.

createdAt
string
Subscription creation timestamp.

updatedAt
string
Subscription last update timestamp.

metadata
object

Hide child properties
Custom subscription metadata.

Example request for retrieving detailed subscription information
GET
https://api.rebill.com/v3/subscriptions/:id
curl -X GET https://api.rebill.com/v3/subscriptions/:id \
      -H "accept: application/json" \
      {% raw %}-H "x-api-key: {{API_KEY}}"{% endraw %}

Copy
Copied!
Response
  {
    "id": "sub_ad128372a40b8dbac50a8ca20c7305b",
    "name": "Premium Plan",
    "description": "Premium subscription plan",
    "status": "active",
    "lastChargeDate": "2024-03-05T15:59:59.000Z",
    "nextChargeDate": "2024-04-05T15:59:59.000Z",
    "amount": 15000,
    "lastChargedAmount": 15000,
    "currency": "ARS",
    "setupFee": 0,
    "frequency": {
      "period": "month",
      "count": 1
    },
    "billingCycles": {
      "total": 12,
      "current": 1,
      "remaining": 11
    },
    "plan": {
      "id": "plan_647838573cf58d61bc659f6525f528ba",
      "title": "Premium Plan",
      "amount": 15000,
      "currency": "ARS",
      "frequency": {
        "period": "month",
        "count": 1
      },
      "repetitions": 12
    },
    "paymentMethod": "card",
    "card": {
      "id": "card_647838573cf58d61bc659f6525f528ba",
      "brand": "visa",
      "type": "credit",
      "lastFourDigits": "4242"
    },
    "discount": {
      "couponCode": "DESC10",
      "type": "percentage",
      "percentage": 10,
      "billingCyclesToApply": {
        "total": 12,
        "remaining": 11
      }
    },
    "customer": {
      "id": "cus_647838573cf58d61bc659f6525f528ba",
      "name": "John Doe",
      "email": "john.doe@example.com",
      "phone": "+1234567890"
    },
    "createdAt": "2024-03-05T15:59:59.000Z",
    "updatedAt": "2024-03-05T16:00:00.000Z",
    "metadata": {
      "customField": "value"
    }
  }


Copy
Copied!
POST
/v3/subscriptions/search
List subscriptions
Filter and paginate subscriptions using flexible search criteria. Search by customer details, status, amount ranges, and billing frequency.

Headers
x-api-key
string
required
{% raw %}API key for authentication. Format: x-api-key: {{API_KEY}}{% endraw %}

Required Body Parameters
pagination
object
required

Hide child properties
limit
number
Items per page (max: 100).

offset
number
Items to skip for pagination.

Optional Body Parameters
filters
object

Hide child properties
customer
object

Hide child properties
Filter by customer attributes.

id
string
Customer ID.
email
string
Customer email.
firstName
string
Customer first name.
lastName
string
Customer last name.
createdAt
object

Hide child properties
Filter by creation date range.

startDate
date
Start date.
endDate
date
End date.
updatedAt
object

Hide child properties
Filter by last update date range.

startDate
date
Start date.
endDate
date
End date.
nextCollection
object

Hide child properties
Filter by next charge date range.

startDate
date
Start date.
endDate
date
End date.
couponId
string
Filter by applied coupon.

planId
string
Filter by plan ID.

status
array

Hide child properties
Filter by subscription status:

active - Active and charging
paused - Paused; no charges
retrying - Payment retry in progress
default - In default due to failed payments
cancelled - Cancelled; no future charges
finished - Completed subscription (all cycles charged)
processing - Payment or update in progress
amount
object

Hide child properties
Filter by subscription amount.

value
number
Value to compare.
valueTo
number
End value for range.
operator
string
Comparison operator:

equal - Equal to value
greaterThan - Greater than value
lessThan - Less than value
between - Between value and valueTo inclusive
paymentMethod
array

Hide child properties
Filter by payment method. You can find the payment method details in the Payments API reference.

currencies
array

Hide child properties
Filter by currency (supports both fiat and crypto).

frequency
object

Hide child properties
Filter by billing frequency.

type
string
Frequency type:

minute - Minute-based interval
day - Daily interval
month - Monthly interval
year - Yearly interval
quantity
number
Time units quantity.
renewal
object

Hide child properties
Filter by renewal type.

type
string
Renewal type:

autoRenewal - Auto-renews every cycle
hasPendingCycles - Limited number of pending cycles
custom - Custom renewal rules
repetitions
number
Number of repetitions.
Response
data
array

Hide child properties
Array of subscription objects matching the search criteria. Each subscription object has the same structure as described in the Get subscription by ID response.

total
number
Total number of subscriptions matching the search criteria.

limit
number
Maximum number of results returned per page.

offset
number
Number of results skipped for pagination.

Example request for listing subscriptions
POST
https://api.rebill.com/v3/subscriptions/search
curl -X POST https://api.rebill.com/v3/subscriptions/search \
      -H "accept: application/json" \
      -H "content-type: application/json" \
      {% raw %}-H "x-api-key: {{API_KEY}}" \{% endraw %}
      -d '{
      "pagination": {
        "limit": 10,
        "offset": 0
        },
      "filters": {
        "status": ["active"],
        "currencies": ["ARS","CLP"]
        }
      }'

Copy
Copied!
Response
  {
    "data": [
     {
        "id": "sub_ad128372a40b8dbac50a8ca20c7305b",
        "name": "Premium Plan",
        "description": "Premium subscription plan",
        "status": "active",
        "lastChargeDate": "2024-03-05T15:59:59.000Z",
        "nextChargeDate": "2024-04-05T15:59:59.000Z",
        "amount": 15000,
        "lastChargedAmount": 15000,
        "currency": "ARS",
        "setupFee": 0,
            "frequency": {
          "period": "month",
          "count": 1
        },
        "billingCycles": {
          "total": 12,
          "current": 1,
          "remaining": 11
        },
        "plan": {
          "id": "plan_647838573cf58d61bc659f6525f528ba",
          "title": "Premium Plan",
          "amount": 15000,
          "currency": "ARS",
          "frequency": {
            "period": "month",
            "count": 1
          },
          "repetitions": 12
        },
        "paymentMethod": "card",
        "card": {
          "id": "card_647838573cf58d61bc659f6525f528ba",
          "brand": "visa",
          "type": "credit",
          "lastFourDigits": "4242"
        },
        "discount": {
          "couponCode": "DESC10",
          "type": "percentage",
          "percentage": 10,
          "billingCyclesToApply": {
            "total": 12,
            "remaining": 11
          }
        },
        "customer": {
          "id": "cus_647838573cf58d61bc659f6525f528ba",
          "name": "John Doe",
          "email": "john.doe@example.com",
          "phone": "+1234567890"
        },
        "createdAt": "2024-03-05T15:59:59.000Z",
        "metadata": {
          "customField": "value"
        }
    }
    ... Rest of the response
    ],
    "total": 100,
    "limit": 10,
    "offset": 0
  }

Copy
Copied!
POST
/v3/subscriptions/:id/pay
Process a subscription and schedule its next charge
Process a subscription payment immediately and set the next billing date. Triggers payment processing for the current billing cycle and schedules the subsequent charge. Returns HTTP 200 on successful initiation.

Required Path Parameters
id
string
required
Subscription's unique identifier.

Optional Body Parameters
nextChargeDate
string
Custom next charge date. Defaults to: current next charge date + price frequency. Format: ISO 8601 (YYYY-MM-DDTHH:mm:ss.sssZ)

Example request for processing a subscription payment
POST
https://api.rebill.com/v3/subscriptions/:id/pay
curl -X POST https://api.rebill.com/v3/subscriptions/:id/pay \
      -H "accept: application/json" \
      -H "content-type: application/json" \
      {% raw %}-H "x-api-key: {{API_KEY}}" \{% endraw %}
      -d '{
        "nextChargeDate":"2024-03-04T18:58:24.433Z"
      }'

Copy
Copied!
Response
  200 OK

Copy
Copied!
POST
/v3/subscriptions/:id/request-card-change
Request card change
Send a secure card update link to the customer's email address. Generates a secure, time-limited URL that allows customers to update their payment method. Returns HTTP 200 when the email is successfully queued.

Headers
x-api-key
string
required
{% raw %}API key for authentication. Format: x-api-key: {{API_KEY}}{% endraw %}

Required Path Parameters
id
string
required
Subscription's unique identifier.

Example request for changing the card for a specific subscription
POST
https://api.rebill.com/v3/subscriptions/:id/request-card-change
curl -X POST https://api.rebill.com/v3/subscriptions/:id/request-card-change \
      -H "accept: application/json" \
      -H "content-type: application/json" \
      {% raw %}-H "x-api-key: {{API_KEY}}"{% endraw %}

Copy
Copied!
Response
  200 OK

Copy
Copied!
PATCH
/v3/subscriptions/:id
Update subscription
Modify subscription attributes including status, amount, payment method, and billing schedule. Changes are applied immediately to the subscription.

Headers
x-api-key
string
required
{% raw %}API key for authentication. Format: x-api-key: {{API_KEY}}{% endraw %}

Path Parameters
id
string
required
Subscription's unique identifier.

Request Body Parameters
name
array

Hide child properties
Subscription name in multiple languages (optional).

language
string
Language code (e.g., 'en', 'es')
text
string
Name in that language
description
array

Hide child properties
Subscription description in multiple languages (optional).

language
string
Language code (e.g., 'en', 'es')
text
string
Description in that language
status
string
New subscription status. Options:

active - Active and charging
paused - Paused; no charges
retrying - Payment retry in progress
default - In default due to failed payments
cancelled - Cancelled; no future charges
finished - Completed subscription (all cycles charged)
processing - Payment or update in progress
amount
number
New subscription amount.

cardId
string
New card ID (must belong to the customer).

statusDetail
string
Detailed subscription status. Possible values: - active - Active and charging

paused - Paused; no charges
cancelled - Cancelled; no future charges
finished - Completed subscription (all cycles charged)
nextChargeDate
string
New next charge date (must be in the future). Format: ISO 8601 (YYYY-MM-DDTHH:mm:ss.sssZ)

couponId
string | null
Coupon ID to apply. Can be null to remove an existing coupon.

frequency
object

Show child properties
repetitions
number
Total number of billing cycles.

remainingIterations
number
Remaining billing cycles (minimum: 1).

Response
id
string
Unique subscription identifier.

name
string
Subscription name.

description
string
Subscription description.

status
string
Updated subscription status.

statusDetail
string
Detailed subscription status. Possible values: - active - Active and charging

paused - Paused; no charges
cancelled - Cancelled; no future charges
finished - Completed subscription (all cycles charged)
lastChargeDate
string
Last charge date timestamp.

nextChargeDate
string
Next scheduled charge date in ISO 8601 format.

amount
number
Subscription amount in smallest currency unit.

lastChargedAmount
number
Last charged amount in smallest currency unit.

currency
string
ISO 4217 currency code (USD, ARS, EUR, etc.).

setupFee
number
Setup fee amount in smallest currency unit.

frequency
object

Hide child properties
Billing frequency configuration.

period
string
Billing interval unit:

day - Daily interval
month - Monthly interval
year - Yearly interval
count
number
Number of period units (e.g., 1 for monthly, 3 for quarterly).

billingCycles
object

Hide child properties
Billing cycle information.

total
number
Total number of billing cycles. Not present for unlimited subscriptions.

current
number
Current billing cycle number.

remaining
number
Remaining billing cycles. Not present for unlimited subscriptions.

plan
object

Hide child properties
Plan configuration and pricing details.

id
string
Plan identifier with pln_ prefix.

title
string
Human-readable plan name.

amount
number
Price per billing cycle in the smallest currency unit (e.g., cents for USD).

currency
string
ISO 4217 currency code (USD, ARS, EUR, etc.).

frequency
object

Show child properties
repetitions
number
Total number of billing cycles. null for unlimited subscriptions.

paymentMethod
string
Payment method type (e.g., card, bank_transfer, cash).

card
object

Hide child properties
Card payment details (only present for card payments).

id
string
Card identifier.

brand
string
Card brand (visa, mastercard, etc.).

type
string
Card type (credit, debit, prepaid).

lastFourDigits
string
Last 4 digits of card number.

discount
object

Hide child properties
Applied discount information (only present when a discount is active).

couponCode
string
Customer-facing coupon code (e.g., WELCOME10, SAVE20).

type
string
Discount type: fixed or percentage.

percentage
number
Percentage discount applied (if type is percentage).

amount
number
Fixed discount amount (if type is fixed).

billingCyclesToApply
object

Show child properties
customer
object

Hide child properties
Customer information.

id
string
Customer identifier with cus_ prefix.

name
string
Customer's full name.

email
string
Customer's email address.

phone
string
Customer's phone number.

createdAt
string
Subscription creation timestamp.

updatedAt
string
Subscription last update timestamp.

metadata
object

Hide child properties
Custom subscription metadata.

Example request for updating subscription information
PATCH
https://api.rebill.com/v3/subscriptions/:id
curl -X PATCH https://api.rebill.com/v3/subscriptions/:id \
      -H "accept: application/json" \
      -H "content-type: application/json" \
      {% raw %}-H "x-api-key: {{API_KEY}}" \{% endraw %}
      -d '{
          "status": "paused",
          "amount": 15500,
          "frequency": {
            "type": "month",
            "count": 1
          },
          "repetitions": 12
        }'

Copy
Copied!
Response
  {
    "id": "sub_ad128372a40b8dbac50a8ca20c7305b",
    "name": "Premium Plan",
    "description": "Premium subscription plan",
    "status": "paused",
    "lastChargeDate": "2024-03-05T15:59:59.000Z",
    "nextChargeDate": "2024-04-05T15:59:59.000Z",
    "amount": 15500,
    "lastChargedAmount": 15000,
    "currency": "ARS",
    "setupFee": 0,
    "frequency": {
      "period": "month",
      "count": 1
    },
    "billingCycles": {
      "total": 12,
      "current": 1,
      "remaining": 11
    },
    "plan": {
      "id": "plan_647838573cf58d61bc659f6525f528ba",
      "title": "Premium Plan",
      "amount": 15500,
      "currency": "ARS",
      "frequency": {
        "period": "month",
        "count": 1
      },
      "repetitions": 12
    },
    "paymentMethod": "card",
    "card": {
      "id": "card_647838573cf58d61bc659f6525f528ba",
      "brand": "visa",
      "type": "credit",
      "lastFourDigits": "4242"
    },
    "discount": {
      "couponCode": "DESC10",
      "type": "percentage",
      "percentage": 10,
      "billingCyclesToApply": {
        "total": 12,
        "remaining": 11
      }
    },
    "customer": {
      "id": "cus_647838573cf58d61bc659f6525f528ba",
      "name": "John Doe",
      "email": "john.doe@example.com",
      "phone": "+1234567890"
    },
    "createdAt": "2024-03-05T15:59:59.000Z",
    "updatedAt": "2024-03-05T16:00:00.000Z",
    "metadata": {
      "customField": "value"
    }
  }

Copy
Copied!
PATCH
/v3/subscriptions/:id/plan
Update subscription plan
Change a subscription to a different plan. The plan change takes effect immediately and may trigger prorated billing adjustments.

Headers
x-api-key
string
required
{% raw %}API key for authentication. Format: x-api-key: {{API_KEY}}{% endraw %}

Path Parameters
id
string
required
Subscription's unique identifier.

Request Body Parameters
planId
string
required
New plan's unique identifier.

Response
id
string
Unique subscription identifier.

name
string
Subscription name.

description
string
Subscription description.

status
string
Current subscription status.

statusDetail
string
Detailed subscription status. Possible values: - active - Active and charging

paused - Paused; no charges
cancelled - Cancelled; no future charges
finished - Completed subscription (all cycles charged)
lastChargeDate
string
Last charge date timestamp.

nextChargeDate
string
Next scheduled charge date in ISO 8601 format.

amount
number
Subscription amount in smallest currency unit.

lastChargedAmount
number
Last charged amount in smallest currency unit.

currency
string
ISO 4217 currency code (USD, ARS, EUR, etc.).

setupFee
number
Setup fee amount in smallest currency unit.

frequency
object

Hide child properties
Billing frequency configuration.

period
string
Billing interval unit:

day - Daily interval
month - Monthly interval
year - Yearly interval
count
number
Number of period units (e.g., 1 for monthly, 3 for quarterly).

billingCycles
object

Hide child properties
Billing cycle information.

total
number
Total number of billing cycles. Not present for unlimited subscriptions.

current
number
Current billing cycle number.

remaining
number
Remaining billing cycles. Not present for unlimited subscriptions.

plan
object

Hide child properties
Updated plan configuration and pricing details.

id
string
New plan identifier with pln_ prefix.

title
string
Human-readable plan name.

amount
number
Price per billing cycle in the smallest currency unit (e.g., cents for USD).

currency
string
ISO 4217 currency code (USD, ARS, EUR, etc.).

frequency
object

Show child properties
repetitions
number
Total number of billing cycles. null for unlimited subscriptions.

paymentMethod
string
Payment method type (e.g., card, bank_transfer, cash).

card
object

Hide child properties
Card payment details (only present for card payments).

id
string
Card identifier.

brand
string
Card brand (visa, mastercard, etc.).

type
string
Card type (credit, debit, prepaid).

lastFourDigits
string
Last 4 digits of card number.

discount
object

Hide child properties
Applied discount information (only present when a discount is active).

couponCode
string
Customer-facing coupon code (e.g., WELCOME10, SAVE20).

type
string
Discount type: fixed or percentage.

percentage
number
Percentage discount applied (if type is percentage).

amount
number
Fixed discount amount (if type is fixed).

billingCyclesToApply
object

Show child properties
customer
object

Hide child properties
Customer information.

id
string
Customer identifier with cus_ prefix.

name
string
Customer's full name.

email
string
Customer's email address.

phone
string
Customer's phone number.

createdAt
string
Subscription creation timestamp.

updatedAt
string
Subscription last update timestamp.

metadata
object

Hide child properties
Custom subscription metadata.

Example request for updating subscription plan
PATCH
https://api.rebill.com/v3/subscriptions/:id/plan
curl -X PATCH https://api.rebill.com/v3/subscriptions/:id/plan \
      -H "accept: application/json" \
      -H "content-type: application/json" \
      {% raw %}-H "x-api-key: {{API_KEY}}" \{% endraw %}
      -d '{
        "planId": "plan_new_647838573cf58d61bc659f6525f528ba"
      }'

Copy
Copied!
Response
  {
    "id": "sub_ad128372a40b8dbac50a8ca20c7305b",
    "name": "Premium Plan Plus",
    "description": "Premium subscription plan plus",
    "status": "active",
    "lastChargeDate": "2024-03-05T15:59:59.000Z",
    "nextChargeDate": "2024-04-05T15:59:59.000Z",
    "amount": 20000,
    "lastChargedAmount": 20000,
    "currency": "ARS",
    "setupFee": 0,
    "frequency": {
      "period": "month",
      "count": 1
    },
    "billingCycles": {
      "total": 12,
      "current": 1,
      "remaining": 11
    },
    "plan": {
      "id": "plan_new_647838573cf58d61bc659f6525f528ba",
      "title": "Premium Plan Plus",
      "amount": 20000,
      "currency": "ARS",
      "frequency": {
        "period": "month",
        "count": 1
      },
      "repetitions": 12
    },
    "paymentMethod": "card",
    "card": {
      "id": "card_647838573cf58d61bc659f6525f528ba",
      "brand": "visa",
      "type": "credit",
      "lastFourDigits": "4242"
    },
    "discount": {
      "couponCode": "DESC10",
      "type": "percentage",
      "percentage": 10,
      "billingCyclesToApply": {
        "total": 12,
        "remaining": 11
      }
    },
    "customer": {
      "id": "cus_647838573cf58d61bc659f6525f528ba",
      "name": "John Doe",
      "email": "john.doe@example.com",
      "phone": "+1234567890"
    },
    "createdAt": "2024-03-05T15:59:59.000Z",
    "updatedAt": "2024-03-05T16:00:00.000Z",
    "metadata": {
      "customField": "value"
    }
  }

Webhooks
Manage webhook notifications in your Rebill account. Create, update, delete and monitor webhooks that trigger on specific events in your payment flow.

For detailed information about webhook events and payloads, see the Webhooks Guide.

GET
/webhooks/:id
Get webhook by ID
Retrieve details for a specific webhook. Use this to verify configuration or check status.

Headers
x-api-key
string
required
{% raw %}API key for authentication. Format: x-api-key: {{API_KEY}}{% endraw %}

Required Path Parameters
id
string
required
Webhook ID (starts with 'we_')

Response
id
string
Webhook ID

url
string
Webhook URL

events
array of strings
Array of events subscribed to

organizationId
string
Organization identifier

Example request for retrieving information about a specific webhook
GET
https://api.rebill.com/v3/webhooks/:id
curl -X GET https://api.rebill.com/v3/webhooks/:id \
      -H "accept: application/json" \
      {% raw %}-H "x-api-key: {{API_KEY}}"{% endraw %}

Copy
Copied!
Response
  {
    "id": "we_f2b90261588e45edaf93c488e577ac66",
    "url": "https://hook.us1.make.com/1gh9w22g24qdrvll62n0ed7x6z3h53n4",
    "active": true,
    "events": [
      "payment.created"
    ],
    "organizationId": "org_8fa0d70f8ab54c7d8e54bc356422b2bd",
  }

Copy
Copied!
POST
/webhooks
Create a webhook
Set up a new webhook endpoint to receive real-time notifications. Requires ADMIN, DEVELOPER, or OWNER role.

Headers
x-api-key
string
required
{% raw %}API key for authentication. Format: x-api-key: {{API_KEY}}{% endraw %}

Required Body Parameters
url
string
required
Your endpoint URL that will receive webhook notifications. Must be HTTPS.

events
array of strings
required
Array of events to subscribe to. Example: ["payment.created", "subscription.updated"]

Response
id
string
Webhook ID

url
string
Webhook URL

events
array of strings
Array of events subscribed to

organizationId
string
Organization identifier

Example request for creating a new webhook
POST
https://api.rebill.com/v3/webhooks
curl -X POST https://api.rebill.com/v3/webhooks \
      -H "accept: application/json" \
      -H "content-type: application/json" \
      {% raw %}-H "x-api-key: {{API_KEY}}" \{% endraw %}
      -d '{
      "url": "https://hook.us1.make.com/1gh9w22g24qdrvll62n0ed7x6z3h53n4",
      "events": ["payment.created"]
    }'

Copy
Copied!
Response
  {
    "id": "we_f2b90261588e45edaf93c488e577ac66",
    "url": "https://hook.us1.make.com/1gh9w22g24qdrvll62n0ed7x6z3h53n4",
    "active": true,
    "events": [
      "payment.created"
    ],
    "organizationId": "org_8fa0d70f8ab54c7d8e54bc356422b2bd",
  }

Copy
Copied!
POST
/webhooks/search
List webhooks
List and filter your webhooks with pagination. Use this endpoint to audit your webhook configurations or find specific endpoints.

Headers
x-api-key
string
required
{% raw %}API key for authentication. Format: x-api-key: {{API_KEY}}{% endraw %}

Optional Body Parameters
order
string
Sort direction: asc or desc

sort
string
Field to sort by (e.g., created_at, updated_at)

page
number
Page number for pagination

limit
number
Items per page (default: 10, max: 100)

offset
number
Number of items to skip

gte
string
Filter by date greater than or equal to (ISO 8601)

lte
string
Filter by date less than or equal to (ISO 8601)

expand
array of strings
Additional fields to include in response

Response
records
array

Show child properties
pagination
object

Show child properties
Example request for listing webhooks
POST
https://api.rebill.com/v3/webhooks/search
curl -X POST https://api.rebill.com/v3/webhooks/search \
      -H "accept: application/json" \
      -H "content-type: application/json" \
      {% raw %}-H "x-api-key: {{API_KEY}}" \{% endraw %}
      -d '{
        "order": "DESC",
        "sort": "created_at",
        "limit": 10,
        "offset": 0
      }'

Copy
Copied!
Response
 {
  "records": [
    {
      "id": "we_f2b90261588e45edaf93c488e577ac66",
      "url": "https://hook.us1.make.com/1gh9w22g24qdrvll62n0ed7x6z3h53n4",
      "active": true,
      "events": [
        "payment.created"
      ],
      "organizationId": "org_8fa0d70f8ab54c7d8e54bc356422b2bd"
    }
  ],
  "pagination": {
    "totalItems": 1,
    "totalPages": 1,
    "currentPage": 1,
    "itemsPerPage": 10,
    "hasNextPage": false,
    "hasPreviousPage": false
  }
}

Copy
Copied!
Reset the retry settings configuration to system default values.

Headers
x-api-key
string
required
{% raw %}API key for authentication. Format: x-api-key: {{API_KEY}}{% endraw %}

Response
response
array

Show child properties
Example request for resetting retry settings to defaults
PUT
https://api.rebill.com/v3/webhooks/retry-settings/reset-defaults
curl -X PUT https://api.rebill.com/v3/webhooks/retry-settings/reset-defaults \
      -H "accept: application/json" \
        {% raw %}-H "x-api-key: {{API_KEY}}"{% endraw %}

Copy
Copied!
Response
  [
    {
      "id": "rs_1",
      "order": 1,
      "delayType": "minutes",
      "delayQuantity": 5,
      "organizationId": "org_8fa0d70f8ab54c7d8e54bc356422b2bd"
    },
    {
      "id": "rs_2",
      "order": 2,
      "delayType": "hours",
      "delayQuantity": 1,
      "organizationId": "org_8fa0d70f8ab54c7d8e54bc356422b2bd"
    }
  ]

Copy
Copied!
DELETE
/webhooks/:id
Delete webhook
Remove a webhook endpoint. This action is permanent and cannot be undone.

Headers
x-api-key
string
required
{% raw %}API key for authentication. Format: x-api-key: {{API_KEY}}{% endraw %}

Required Path Parameters
id
string
required
Webhook ID (starts with 'we_')

Response
id
string
Webhook ID

events
array of strings
Array of events subscribed to

deleted
boolean
Webhook deletion status

Example request for deleting an existing webhook
DELETE
https://api.rebill.com/v3/webhooks/:id
curl -X DELETE https://api.rebill.com/v3/webhooks/:id \
      -H "accept: application/json" \
      {% raw %}-H "x-api-key: {{API_KEY}}"{% endraw %}

Copy
Copied!
Response
  {
    "id": "we_f2b90261588e45edaf93c488e577ac66",
    "events": [
      "payment.created"
    ],
    "deleted": true
  }

Copy
Copied!
