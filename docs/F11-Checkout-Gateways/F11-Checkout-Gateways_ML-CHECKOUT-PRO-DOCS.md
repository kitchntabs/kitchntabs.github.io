
# MD for: https://www.mercadopago.cl/developers/en/docs/checkout-pro/create-application.md


---
product_landing_hero:
 - title: Integrate Checkout Pro and set up a predesigned experience
 - message: With this solution, your customers buy on your website and pay in the Mercado Pago environment with their saved payment methods.
 - product_svg_image: checkout-pro-en
 - benefit_icon: categories
 - benefit_title: Agile integration
 - benefit_icon: link
 - benefit_title: For web, Android, and iOS
 - benefit_icon: edit
 - benefit_title: Pre-built experience
 - benefit_icon: sort
 - benefit_title: With redirection to Mercado Pago
 - info: Looking for development-free options? Explore [more solutions](/developers/pt/docs#online-payments).
---

---
product_landing_what_it_offers:
 - title: What it offers
 - message: Combine different features to ensure transaction security and conversion.
 - benefit_title: Customization
 - benefit_bullet: Financing in installments
 - benefit_bullet: Return URL after payment approval
 - benefit_bullet: Appearance and style of the payment button
 - benefit_bullet: Customizable payment methods with the option to split the total amount into 2 parts
 - benefit_title: Conversion
 - benefit_bullet: Quick payment with the payment methods saved in Mercado Pago
 - benefit_bullet: Option to pay without a Mercado Pago account, as a guest user
 - benefit_bullet: Online and offline payment methods, such as cards and account money
 - benefit_bullet: Recovery of rejected payments
 - benefit_title: Payment approval
 - benefit_bullet: 3DS 2.0 technology for transaction authentication
 - benefit_bullet: Fraud prevention tools and customer identity verification
 - benefit_bullet: Transaction validation using industry-specific data
 - benefit_title: Fraud protection
 - benefit_bullet: OWASP and PCI DSS protocols
 - benefit_bullet: Buyer identity verification
 - benefit_bullet: Facial recognition with FaceAuth to access the Mercado Pago account
---

---
product_landing_how_works:
 - title: How it works
 - message: The customer chooses the product or service on your site, pays in Mercado Pago’s secure environment, and returns to your website or the configured destination.
 - sub_title: Payment process
 - image: https://http2.mlstatic.com/storage/dx-devsite/docs-assets/custom-upload/2025/3/25/1745588445182-choproesmx990px1.gif
 - image_text: Simulate the payment processing
 - image_text_link: /developers/en/live-demo/checkout-pro
 - list_title: The buyer checks out their shopping cart on your website and chooses to pay with Mercado Pago.
 - list_title: They’re redirected to the payment form, where they decide whether to proceed with their Mercado Pago account or as a guest user.
 - list_title: They can choose their preferred payment method, whether it’s one saved in their account or a new one they entered.
 - list_title: Once the purchase is completed, they are redirected to your website or the configured destination.
 - button_description: How to integrate
 - button_link: /developers/en/docs/checkout-pro/create-application
---

---
product_landing_what_differentiates:
 - title: What sets it apart
 - message: Compare our checkouts and choose the option that best fits your business. Check the [rates](/developers/es/support/37740).
 - highlight_text: You are here
 - column_product_svg_image: checkout-pro-en
 - column_product: Checkout Pro
 - column_button_text: How to integrate
 - column_button_link: /developers/en/docs/checkout-pro/create-application
 - column_product_svg_image: checkout-api-en
 - column_product: Checkout API
 - column_button_text: Go to the overview
 - column_button_link: /developers/en/docs/checkout-api-payments/overview
 - column_product_svg_image: checkout-bricks-en
 - column_product: Checkout Bricks
 - column_button_text: Go to the overview
 - column_button_link: /developers/en/docs/checkout-bricks/landing
 - line_text: Integration effort
 - line_type: dots
 - line_values: 2|5|3
 - line_text: Customization level
 - line_type: dots
 - line_values: 2|5|3
 - line_text: Design ready to set up
 - line_type: check
 - line_values: true|false|true
 - line_text: Collection experience
 - line_type: text
 - line_values: In Mercado Pago|In your site|In your site
 - line_text: Recurring payments
 - line_type: check
 - line_values: false|true|true
 - line_text: Payment methods
 - line_type: text
 - line_values: Credit or debit card, Mercado Pago Account and Installments without Card|Credit or debit card and Mercado Pago Account|Credit or debit card and Mercado Pago Account
 - line_text: Availability by country
 - line_type: sites
 - line_values: all|all|all
---

---
product_landing_how_integrate:
 - title: How to integrate
 - sub_title: Learn about the steps you need to follow to integrate this solution.
 - requirement_title: Prerequisites
 - requirement_table_title: Seller account
 - requirement_table_list: To integrate Checkout Pro, you need to access Mercado Pago and [create a seller account](https://www.mercadopago[FAKER][URL][DOMAIN]/hub/registration/landing).
 - requirement_table_title: SSL Certificate (Secure Sockets Layer)
 - requirement_table_list: Allows secure browsing and the protection of your data during information transfers.
---
|||column1|||

---
product_landing_how_integrate:
 - list_title: Integration process
 - list_item: [Create an application](/developers/es/docs/checkout-pro/create-application) from [Your integrations](/developers/panel/app).
 - list_item: [Configure the development environment](/developers/es/docs/checkout-pro/configure-development-enviroment).
 - list_item: [Create and configure your payment preference](/developers/en/docs/checkout-pro/create-payment-preference).
 - list_item: [Configure the Back URLs](/developers/en/docs/checkout-pro/configure-back-urls).
 - list_item: [Add the SDK to the frontend and initialize the checkout](/developers/en/docs/checkout-pro/web-integration/add-frontend-sdk).
 - list_item: [Configure the payment notifications](/developers/en/docs/checkout-pro/payment-notifications).
 - list_item: [Test your integration](/developers/en/docs/checkout-pro/integration-test).
 - list_item: [Go to production](/developers/en/docs/checkout-pro/go-to-production).
 - button_description: I want to start integrating
 - button_link: /developers/en/docs/checkout-pro/create-application
---
|||column2|||
<div class="mermaid-overview">
  <pre class="mermaid">
  flowchart TD
  A["Access Your integrations"] --> B["Create application"]
  B --> C["Build the environment"]
  C --> D["Create payment preferences"]
  D -- Amount, payment methods, details, others --> F["Configure notifications"]
  F -- Webhooks and IPN --> E["Test the integration"]
  E -- Successful tests --> H["Go to production"]
  E -- Errors detected --> I["Fix configuration"]
  I --> H
  H --> J["Measure quality"]
  </pre>
</div>
|||

# Create application

**Applications** are registered entities within Mercado Pago that act as a unique identifier for managing the authentication and authorization of your integrations. In other words, they serve as the link between your development and Mercado Pago, and they constitute the first stage in carrying out the integration.

With them, you can access the necessary :toolTipComponent[credentials]{link="/developers/en/guides/additional-content/your-integrations/credentials" linkText="Credentials" content="Unique access keys used to identify an integration in your account, linked to your application. For more information, access the link below."} to interact with our APIs or specific services, as well as manage and organize your integration, which is why you must create an application for each Mercado Pago solution you integrate.

To create an **application**, follow the steps below.

1. In the upper right corner of Mercado Pago Developers, click on **Login** and enter the required information with the data for your Mercado Pago account.
2. Once you are logged in, in the upper right corner of Mercado Pago Developers, click on **Create application** if your account does not yet have any created applications, or go to "Your integrations" and select **View all**. There, click on **Create application**.
3. Once inside **Your integrations**, click on the **Create application** button.

> NOTE
>
> To protect your account and ensure compliance with operations, during the creation of an application, you will need to do an identity verification if you haven’t done so already, or a re-authentication if you have previously completed the verification process.

![create-application-1](/images/snippets/create-application-1-es-v1.png)

4. Enter a **name** to identify your application. The limit is up to 50 alphanumeric characters.
5. Select **Online payments** as the type of payment you want to integrate, as this is the solution type corresponding to online stores. Click **Continue**.
6. Select that you are integrating for a self-developed store. Optionally, you can enter your store's URL. Click **Continue**.
7. Select the **Checkouts** option and then choose **Checkout Pro** as the solution you are going to integrate.
8. Confirm the selected options. If you need to modify any selection, click the **Edit** button. Accept the [Privacy Statement](https://www.mercadopago[FAKER][URL][DOMAIN]/privacidad) and the [Terms and Conditions](/developers/en/docs/resources/legal/terms-and-conditions) and click on **Confirm**.

![Resumen de aplicación](/images/snippets/create-application/ES-new-app-CHO-PRO-v1.png)

In [Your integration](/developers/panel/app), you will be able to view the list of all your created applications and access the [Integration data](/developers/en/docs/checkout-pro/resources/application-details) for each of them.

> NOTE
>
> If you wish, you can edit or delete an application. In the latter case, keep in mind that your store will lose the ability to receive payments through the Mercado Pago integration associated with that application. For more information, please refer to the [Integration data](/developers/en/docs/checkout-pro/resources/application-details).

## Access test credentials

After creating your application, the :toolTipComponent[test credentials]{link="/developers/en/docs/checkout-pro/resources/credentials" linkText="Credentials" content="Unique access keys that we use to identify an integration in your account, linked to your application. For more information, see the link below."} will also be automatically created. Use the **test credentials** to perform all necessary configurations and validations in a secure test environment.

When accessing test credentials, the following credential pairs will be displayed: :toolTipComponent[Public Key]{content="Public key used in the frontend to access information and encrypt data. You can access it through *Your integrations > Integration data > Tests > Test credentials*."} and the :toolTipComponent[Access Token]{content="Private key of the application created in Mercado Pago, that must be used in the backend. You can access it through *Your integrations > Integration data > Tests > Test credentials*."}. The test Access Token starts with the prefix `APP_USR`, just like your production Access Token.

![test credentials](/images/snippets/credentials/app-data-test-credentials-es-v1.png)

> NOTE
>
> If you are using an existing application, you will need to activate the test credentials. For more information, see the [Credentials](/developers/en/docs/checkout-pro/additional-content/credentials) documentation.


# Configure development environment

To start integrating Mercado Pago's payment solutions, it is necessary to prepare your development environment with a series of configurations that will allow you to access Mercado Pago's functionalities from the backend.

Next, you will need to install and configure the official Mercado Pago SDK:

> SERVER_SIDE
>
> h2
>
> Install the Mercado Pago SDK

The **backend SDK** is designed to handle server-side operations, allowing you to create and manage :toolTipComponent[payment preferences]{content="A payment preference is an object or set of information that represents the product or service you want to charge for. Within the Mercado Pago ecosystem, this object is known as `preference`."}, process transactions, and perform other critical operations securely.

> NOTE
>
> If you prefer, you can download the Mercado Pago SDKs from our [official libraries](/developers/en/docs/sdks-library/server-side).

Install the Mercado Pago SDK in the language that best fits your integration using a dependency manager, as shown below.

[[[
```php
===
To install the SDK, you must run the following code in your terminal's command line using [Composer](https://getcomposer.org/download):
===
php composer.phar require "mercadopago/dx-php"
```
```node
===
To install the SDK, you must run the following code in your terminal's command line using [npm](https://www.npmjs.com/get-npm):
===
npm install mercadopago
```
```java
===
To install the SDK in your [Maven](http://maven.apache.org/install.html) project, you must add the following dependency to your <code>pom.xml</code> file and run <code>maven install</code> in your terminal's command line:
===
<dependency>
  <groupId>com.mercadopago</groupId>
  <artifactId>sdk-java</artifactId>
  <version>2.1.7</version>
</dependency>
```
```ruby
===
To install the SDK, you must run the following code in your terminal's command line using [Gem](https://rubygems.org/gems/mercadopago-sdk):
===
gem install mercadopago-sdk
```
```csharp
===

To install the SDK, you must run the following code in your terminal's command line using [NuGet](https://docs.microsoft.com/es-es/nuget/reference/nuget-exe-cli-reference):

===
nuget install mercadopago-sdk
```
```python
===
To install the SDK, you must run the following code in your terminal's command line using [Pip](https://pypi.org/project/mercadopago/):
===
pip3 install mercadopago
```
```go
go get -u github.com/mercadopago/sdk-go
```
]]]

> SERVER_SIDE
>
> h2
>
> Initialize Mercado Pago library

Next, create a main file (_main_) in the _backend_ of your project with the programming language you are using. There, place the following code replacing the value `TEST_ACCESS_TOKEN` with the :toolTipComponent[test Access Token]{content="Testing private key of the application created in Mercado Pago, that is used in the backend. You can access it through *Your integrations* in the *Integration data* section, by going to the *Credentials* section located on the right side of the screen and clicking on *Testing*. Alternatively, you can access it through *Your integrations > Integration data > Testing > Testing credentials*. The test Access Token starts with the prefix `APP_USR`."}.

[[[
```php
<?php
// Mercado Pago SDK
use MercadoPago\MercadoPagoConfig;
// Add credentials
MercadoPagoConfig::setAccessToken("TEST_ACCESS_TOKEN");
?>
```
```node
// Mercado Pago SDK
import { MercadoPagoConfig, Preference } from 'mercadopago';
// Add credentials
const client = new MercadoPagoConfig({ accessToken: 'YOUR_ACCESS_TOKEN' });
```
```java
// Mercado Pago SDK
import com.mercadopago.MercadoPagoConfig;
// Add credentials
MercadoPagoConfig.setAccessToken("TEST_ACCESS_TOKEN");
```
```ruby
# Mercado Pago SDK
require 'mercadopago'
# Add credentials
sdk = Mercadopago::SDK.new('TEST_ACCESS_TOKEN')
```
```csharp
// Mercado Pago SDK
 using MercadoPago.Config;
 // Add credentials
MercadoPagoConfig.AccessToken = "TEST_ACCESS_TOKEN";
```
```python
# Mercado Pago SDK
import mercadopago
# Add credentials
sdk = mercadopago.SDK("TEST_ACCESS_TOKEN")
```
```go
import (
	"github.com/mercadopago/sdk-go/pkg/config"
)

cfg, err := config.New("{{ACCESS_TOKEN}}")
if err != nil {
	fmt.Println(err)
}
```
]]]

After completing these configurations, your development environment is ready to proceed with setting up a payment preference.


> SERVER_SIDE
>
> h1
>
> Create and configure a payment preference

A **payment preference** is an object or set of information that represents the product or service you want to charge for. Within the Mercado Pago ecosystem, this object is known as `preference`. When creating a payment preference, you can define essential details such as price, quantity, and payment methods, as well as other related configurations for the payment flow.

During this step, you will also add the **payment methods** you want to offer with Checkout Pro, which by default includes all payment methods available in Mercado Pago.

> WARNING
>
> To offer payments via Fintoc, you must accept the solution’s terms and conditions. To do this, go to [Your business > Settings > Payment preferences](https://www.mercadopago.cl/business/cashing-preferences), read the terms and conditions, and if you agree, enable the **Receive payments by bank transfer** option.

To create a payment preference, use the method associated with `preference` in the backend SDK. You need to **create a payment preference for each order or payment flow** you want to initiate.

Below, you will find examples of how to implement this in your backend using the SDK, which is available in different programming languages. Complete the attributes with the appropriate information to reflect the details of each transaction and ensure an accurate payment flow.

> NOTE
>
> You can adapt the Checkout Pro integration to your business model by configuring the attributes of the payment preference. These will allow you to define installments, exclude a payment method, change the expiration date of a specific payment, among other options. To customize your payment preference, access the documentation in the **Additional settings** section.

[[[
```php
<?php
$client = new PreferenceClient();
$preference = $client->create([
  "items"=> array(
  array(
  "title" => "My product",
  "quantity" => 1,
  "unit_price" => 2000
  )
  )
]);

echo $preference
?>
```
```node
const preference = new Preference(client);

preference.create({
  body: {
  items: [
  {
  title: 'My product',
  quantity: 1,
  unit_price: 2000
  }
  ],
  }
})
.then(console.log)
.catch(console.log);
```
```java
PreferenceItemRequest itemRequest =
  PreferenceItemRequest.builder()
  .id("1234")
  .title("Games")
  .description("PS5")
  .pictureUrl("http://picture.com/PS5")
  .categoryId("games")
  .quantity(2)
  .currencyId("BRL")
  .unitPrice(new BigDecimal("4000"))
  .build();
  List<PreferenceItemRequest> items = new ArrayList<>();
  items.add(itemRequest);
PreferenceRequest preferenceRequest = PreferenceRequest.builder()
.items(items).build();
PreferenceClient client = new PreferenceClient();
Preference preference = client.create(preferenceRequest);
```
```ruby
# Create a preference object
preference_data = {
  items: [
  {
  title: 'My product',
  unit_price: 75.56,
  quantity: 1
  }
  ]
}
preference_response = sdk.preference.create(preference_data)
preference = preference_response[:response]

# This value will replace the string "<%= @preference_id %>" in your HTML
@preference_id = preference['id']
```
```csharp
// Create the preference request object
var request = new PreferenceRequest
{
  Items = new List<PreferenceItemRequest>
  {
  new PreferenceItemRequest
  {
  Title = "My product",
  Quantity = 1,
  CurrencyId = "ARS",
  UnitPrice = 75.56m,
  },
  },
};

// Create the preference using the client
var client = new PreferenceClient();
Preference preference = await client.CreateAsync(request);
```
```python
# Create an item in the preference
preference_data = {
  "items": [
  {
  "title": "My product",
  "quantity": 1,
  "unit_price": 75.76,
  }
  ]
}

preference_response = sdk.preference().create(preference_data)
preference = preference_response["response"]
```
```go
import (
  "github.com/mercadopago/sdk-go/pkg/preference"
)

client := preference.NewClient(cfg)

request := preference.Request{
	Items: []preference.ItemRequest{
		{
			Title: "My product",
			Quantity: 1,
			UnitPrice: 75.76,
		},
	},
}

resource, err := client.Create(context.Background(), request)
if err != nil {
	fmt.Println(err)
	return
}

fmt.Println(resource)
```
]]]

## Obtain the preference identifier

The preference identifier is a unique transaction identifier for a specific payment request. To obtain it, you need to run your application.

In the response, you will get the **preference identifier** in the `ID` property. **Save this value as you will need it in the next step for your integration** on a website or a mobile application.

Below, we show an example of how the `ID` attribute with the preference identifier looks in a response.

```
"id": "787997534-6dad21a1-6145-4f0d-ac21-66bf7a5e7a58"
```

### Choose the type of integration

Once you have obtained your preference ID, you should proceed to the frontend configurations. To do this, you need to choose the type of integration that best suits your needs, whether it is for integrating a **website** or a **mobile application**.

Select the type of integration you want to perform and follow the detailed steps to complete the Checkout Pro integration.

---
future_product_avaible: 
 - card_avaible: true
 - card_icon: Laptop
 - card_title: Continue integration for websites
 - card_description: Offers payments with redirection to Mercado Pago on your website or online store.
 - card_button: /developers/en/docs/checkout-pro/configure-back-urls
 - card_buttonDescription: Web integration
 - card_pillText: AVAILABLE
 - card_linkAvailable: false
 - card_linkProof:
 - card_linkProofDescription:
 - card_avaible: true
 - card_icon: Smartphone
 - card_title: Continue integration for mobile applications
 - card_description: Offers payments with redirection to Mercado Pago in your mobile application.
 - card_button: /developers/en/docs/checkout-pro/mobile-integration
 - card_buttonDescription: Mobile integration
 - card_pillText: AVAILABLE
 - card_linkAvailable: false
 - card_linkProof:
 - card_linkProofDescription:
---


# Configure return URLs

The return URL is the address to which the user is redirected after completing the payment, whether successful, failed, or pending. This URL should be a webpage that you control, such as a server with a named domain (DNS).

This process is configured through the `back_urls` attribute in the backend, in the payment preference associated with your integration. With this attribute, you can define that the buyer will be redirected to the website you configured, either automatically or through the "Return to site" button, depending on the payment status.

You can configure up to three different return URLs, corresponding to pending payment, success, or error scenarios.

> NOTE
>
> In mobile integrations, we recommend that the return URLs be deep links. To learn more, refer to the [Integration for mobile applications](/developers/en/docs/checkout-pro/mobile-integration) documentation.

## Define return URL

In your backend code, you need to set up the URL to which you want Mercado Pago to redirect the user once they have completed the payment process.

> NEUTRAL_MESSAGE
>
> If you prefer, it is also possible to configure the return URLs by sending a POST request to the [Create Preference](/developers/en/reference/online-payments/checkout-pro/preferences/create-preference/post) API with the `back_urls` attribute specifying the URLs to which the buyer should be directed upon payment completion.

Below, we share examples of how to include the `back_urls` attribute according to the programming language you are using, along with the details of each possible parameter.

[[[
```php
<?php
$preference = new MercadoPago\Preference();
//...
$preference->back_urls = array(
  "success" => "https://www.your-site/success",
  "failure" => "https://www.your-site/failure",
  "pending" => "https://www.your-site/pending"
);
$preference->auto_return = "approved";
// ...
?>
```
```node
const preference = new Preference(client);
  preference.create({
  body: {
  // ...
  back_urls: {
  success: "https://www.your-site/success",
  failure: "https://www.your-site/failure",
  pending: "https://www.your-site/pending"
  },
  auto_return: "approved",
  }
  })
  // ...
```
```java
PreferenceBackUrlsRequest backUrls =
// ...
  PreferenceBackUrlsRequest.builder()
  .success("https://www.your-site/success")
  .pending("https://www.your-site/pending")
  .failure("https://www.your-site/failure")
  .build();

PreferenceRequest request = PreferenceRequest.builder().backUrls(backUrls).build();
// ...
```
```ruby
# ...
preference_data = {
  # ...
  back_urls: {
  success: 'https://www.your-site/success',
  failure: 'https://www.your-site/failure',
  pending: 'https://www.your-site/pendings'
  },
  auto_return: 'approved'
  # ...
}
# ...
```
```csharp
var request = new PreferenceRequest
{
  // ...
  BackUrls = new PreferenceBackUrlsRequest
  {
  Success = "https://www.your-site/success",
  Failure = "https://www.your-site/failure",
  Pending = "https://www.your-site/pendings",
  },
  AutoReturn = "approved",
};
```
```python
preference_data = {
  "back_urls": {
  "success": "https://www.your-site/success",
  "failure": "https://www.your-site/failure",
  "pending": "https://www.your-site/pendings"
  },
  "auto_return": "approved"
}
```
]]]

| Attribute | Description |
|--------------|-----|
| `auto_return`| Buyers are automatically redirected to the site when the payment is approved. The default value is `approved`. **The redirection time will be up to 40 seconds and cannot be customized**. By default, a "Return to site" button will also be displayed.|
| `back_urls` | Return URL to the site. The possible scenarios are: <br>`success`: Return URL when the payment is approved.<br>`pending`: Return URL when the payment is pending.<br>`failure`: Return URL when the payment is rejected.

> WARNING
>
> Do not use local domains in the `back_urls` value, such as 'localhost/' or '127.0.0.1' with or without a specified port. We recommend using a server with a named domain (DNS) or development IPs to be able to return to the site after payment. Otherwise, the "Something went wrong" message will appear when the purchase process is completed.

## Return URLs Response

The `back_urls` will return some useful parameters through a GET request. Below, we share an example of what a response will look like and the details of the parameters you may find in it.

```curl
GET /test?collection_id=106400160592&collection_status=rejected&payment_id=106400160592&status=rejected&external_reference=qweqweqwe&payment_type=credit_card&merchant_order_id=29900492508&preference_id=724484980-ecb2c41d-ee0e-4cf4-9950-8ef2f07d3d82&site_id=MLC&processing_mode=aggregator&merchant_account_id=null HTTP/1.1
Host: yourwebsite.com
Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7
Accept-Encoding: gzip, deflate, br, zstd
Accept-Language: es-419,es;q=0.9
Connection: keep-alive
Referer: https://www.mercadopago.com/checkout/v1/payment/redirect/505f641c-cf04-4407-a7ad-8ca471419ee5/congrats/rejected/?preference-id=724484980-ecb2c41d-ee0e-4cf4-9950-8ef2f07d3d82&router-request-id=0edb64e3-d853-447a-bb95-4f810cbed7f7&p=f2e3a023dd16ac953e65c4ace82bb3ab
Sec-Ch-Ua: "Chromium";v="134", "Not:A-Brand";v="24", "Google Chrome";v="134"
Sec-Ch-Ua-Mobile: ?0
Sec-Ch-Ua-Platform: "macOS"
Sec-Fetch-Dest: document
Sec-Fetch-Mode: navigate
Sec-Fetch-Site: cross-site
Sec-Fetch-User: ?1
Upgrade-Insecure-Requests: 1
```

| Parameter | Description |
|-----------------------|-------------------------------------------------------------------------------------------------|
| `payment_id` | ID (identifier) of the Mercado Pago payment. |
| `status` | Payment status. For example: `approved` for an approved payment or `pending` for a pending payment. |
| `external_reference` | Reference that you can synchronize with your payment system. |
| `merchant_order_id` | ID (identifier) of the payment order generated in Mercado Pago. |

### Response for offline payment methods

Offline payment methods are those where the buyer chooses a method that requires them to use a physical payment point to complete the purchase process. In this payment flow, Mercado Pago will generate a voucher that the user needs to make the payment at the corresponding establishment, and will redirect the user to the URL you specified in the `back_urls` attribute as `pending`.

At this point, the payment is in a pending state because the user still needs to go to a physical establishment and pay.

To provide more information to the buyer, we recommend that for `pending` payment statuses, you redirect the buyer to your website and share clear information on how to complete the payment.

Once the user goes to the corresponding establishment and makes the cash payment with the generated voucher, Mercado Pago is notified and the payment status will change. We recommend that you [configure payment notifications](/developers/en/docs/checkout-pro/payment-notifications) so that your server can process this notification and update the order status in your database.


> CLIENT_SIDE
>
> h1
>
> Add the SDK to the frontend and initialize the checkout

Once you have configured your backend, you need to configure the frontend to complete the payment experience on the client-side. For this, you can use the MercadoPago.js SDK, which allows you to capture payments directly on the frontend securely.

In this section, you will learn how to include and initialize it correctly, to finally render the Mercado Pago payment button.

> If you prefer, you can download the MercadoPago.js SDK from our [official libraries](/developers/en/docs/sdks-library/client-side/mp-js-v2).

:::::TabsComponent

::::TabComponent{title="Include the SDK with HTML/js"}
## Include the SDK with HTML/js

To include the MercadoPago.js SDK in your HTML page from a **CDN (Content Delivery Network)**, you first need to add the `<script>` tag just before the `</body>` tag in your main HTML file, as shown in the following example.

```html
<!DOCTYPE html>
<html>
<head>
  <title>My integration with Checkout Pro</title>
</head>
<body>

  <!-- Your page content -->

  <script src="https://sdk.mercadopago.com/js/v2"></script>

  <script>
  // Your JavaScript code will go here
  </script>

</body>
</html>
```

## Initialize the checkout from the payment preference

After including the SDK in your frontend, it's time to initialize it and then start the checkout.

To continue, use your :toolTipComponent[test Public Key]{content="Testing public key, used in the frontend to access information and encrypt data, whether in the development stage or the testing stage. You can access it through **Your integrations > Integration data > Testing > Testing credentials**."} credential.

> NOTE
>
> If you are developing for someone else, you will be able to access the credentials of applications you do not manage. See [Share credentials](/developers/en/docs/checkout-pro/resources/credentials) for more information.

You will also need to use the payment preference ID that you obtained as a response in [Create and configure a payment preference](/developers/en/docs/checkout-pro/create-payment-preference).

Next, to initialize the SDK using a CDN, you should execute this code within the `<script>` tag, replacing the value `YOUR_PUBLIC_KEY` with your key and `YOUR_PREFERENCE_ID` with the **payment preference ID**.

```Javascript
<script src="https://sdk.mercadopago.com/js/v2"></script>
<script>
  // Configure sua chave pública do Mercado Pago
  const publicKey = "YOUR_PUBLIC_KEY";
  // Configure o ID de preferência que você deve receber do seu backend
  const preferenceId = "YOUR_PREFERENCE_ID";

  // Inicializa o SDK do Mercado Pago
  const mp = new MercadoPago(publicKey);

  // Cria o botão de pagamento
  const bricksBuilder = mp.bricks();
  const renderWalletBrick = async (bricksBuilder) => {
  await bricksBuilder.create("wallet", "walletBrick_container", {
  initialization: {
  preferenceId: "<PREFERENCE_ID>",
  }
});
  };

  renderWalletBrick(bricksBuilder);
</script>
```

> CLIENT_SIDE
>
> h2
>
> Create an HTML container for the payment button

Finally, you will need to create a container in your HTML to define the location where the MercadoPago payment button will be displayed. The creation of the container is done by inserting an element in the HTML code of the page where the component will be rendered.

```html
<!-- Container para o botão de pagamento -->
<div id="walletBrick_container"></div>
```

## Render the payment button

The Mercado Pago SDK will automatically render a button within this element, which will be responsible for redirecting the buyer to a purchase form in the Mercado Pago environment, as shown in the following image.

![Button](/images/cow/wallet-render-en-v1.png)
::::

::::TabComponent{title="Install the SDK using React"}
## Install the SDK using React

To include the MercadoPago.js SDK in the frontend of your React project, you first need to set up your React environment. To do this, make sure you have **Node.js** and **npm** installed on your system. If you don't have them, download them from the [official Node.js site](http://Node.js).

In your terminal or command line, run the following command to create a new React application:

```
npx create-react-app my-mercadopago-app
```

This will create a new directory named `my-mercadopago-app` with a basic React application structure.

### Install MercadoPago.js SDK

Install the MercadoPago.js SDK library in the `my-mercadopago-app` directory. You can do this by running the following command:

```
npm install @mercadopago/sdk-react
```

## Create a component for the payment button

Open the `src/App.js` file of your React application. Once there, modify the content of the file to integrate the Mercado Pago `wallet` component, which is responsible for displaying the Mercado Pago payment button.

To continue, use your :toolTipComponent[test Public Key]{content="Testing public key, used in the frontend to access information and encrypt data, whether in the development stage or the testing stage. You can access it through **Your integrations > Integration data > Testing > Testing credentials**."} credential.

> NOTE
>
> If you are developing for someone else, you will be able to access the credentials of applications you do not manage. See [Share credentials](/developers/en/docs/checkout-pro/resources/credentials) for more information.

You will also need to use the payment preference ID that you obtained as a response in [Create and configure a payment preference](/developers/en/docs/checkout-pro/create-payment-preference).

Next, replace the value `YOUR_PUBLIC_KEY` with your key and `YOUR_PREFERENCE_ID` with the **payment preference ID** in the `src/App.js` file. See the following example.

```JavaScript
import React from 'react';
import { initMercadoPago, Wallet } from '@mercadopago/sdk-react';

// Initializes Mercado Pago with your Public Key
initMercadoPago('YOUR_PUBLIC_KEY');

const App = () => {
  return (
  <div style={{ display: 'flex', flexDirection: 'column', alignItems: 'center', marginTop: '50px' }}>
  <h1>Payment Button</h1>
  <p>Click the button to make the payment.</p>
  {/* Renders the payment button */}
  <div style={{ width: '300px' }}>
  <Wallet initialization={{ preferenceId: 'YOUR_PREFERENCE_ID' }} />
  </div>
  </div>
  );
};

export default App;
```

## Render the payment button

When running your React application, the Mercado Pago SDK will render the payment button that will be responsible for redirecting the buyer to a purchase form in the Mercado Pago environment, as shown in the following image.

![Button](/images/cow/wallet-render-en-v1.png)
::::

:::::

<br>

Once you have completed the configuration of your frontend, you will need to set up [Notifications](/developers/en/docs/checkout-pro/payment-notifications) so that your integration receives real-time information about the events that occur in your integration.

# Configure payment notifications

**Webhooks**, also known as **web callbacks**, are an effective method that allows Mercado Pago servers to send **real-time** information when a specific event related to your integration occurs.

Instead of your system constantly polling for updates, Webhooks allow for **passive and automatic** data transmission between Mercado Pago and your integration through an **HTTP POST** request, optimizing communication and reducing server load.

Check the general flow of a notification in the diagram below.

![Diagram](/images/cow/notifications-diagrama-es-v1.jpg)

Below, we present a step-by-step guide to configure payment creation and update notifications. Once configured, Webhook notifications will be sent every time a payment is created or its status is modified (Pending, Rejected, or Approved). 

> NOTE 
> 
> This documentation exclusively covers the configuration of payment notifications, including creations and updates, through the **Payments** event. To obtain information about other notification events available for configuration, please refer to the general [Notifications documentation](/developers/en/docs/checkout-pro/additional-content/notifications).

In the process of integrating with Mercado Pago, you can configure notifications in two ways:

| Configuration Type | Description | Advantages | When to Use |
|---|---|---|---|
| Configuration through Your integrations | This method allows you to configure notifications directly in your Developer Panel. You can set up notifications for each of your applications, identify different accounts if necessary, and validate the origin of the notification using a secret signature. | - Simple identification of different accounts, ensuring proper management in diverse environments. <br> - High security by validating the origin of notifications via a secret signature, which guarantees the integrity of the received information. <br> - More versatile and effective for maintaining centralized control and efficiently managing communication with applications. | Recommended for most integrations. |
| Configuration during the creation of preferences | Notifications are configured for each transaction individually during the preference creation process. | - Specific adjustments for each transaction. <br> - Flexibility in cases where dynamic mandatory parameters are needed. <br> - Ideal for integrations like payment platforms for multiple sellers. | Convenient in cases where it is necessary to send a dynamic query parameter mandatorily, and also suitable for integrations that function as a payment platform for multiple sellers. |

> RED_MESSAGE
>
> Important
>
> The URLs configured during the creation of a payment will take precedence over those configured through Your integrations.

:::::AccordionComponent{title="Configuration through Your integrations"}
## Configuration through Your integrations
You can configure notifications for each of your applications directly from [Your integrations](/developers/panel/app) efficiently and securely. In this section, we will explain how to:

1. Indicate the notification URLs and configure events
2. Validate the origin of a notification
3. Simulate receiving a notification

### 1. Indicate notification URLs and configure the event

To configure Webhook notifications, it is necessary to indicate the URLs to which they will be sent.

To do this, follow the step-by-step instructions below:

1. Go to [Your integrations](/developers/panel/app) and select the application integrated with Checkout Pro for which you want to activate notifications.

![Application](/images/cow/not1-select-app-es-v1.png)

2. In the left menu, select **Webhooks > Configure Notifications** and configure the URL that will be used to receive them.

![Webhooks](/images/cow/not2-webhooks-es-v1.png) 

3. Select the **Production mode** tab and provide an `HTTPS URL` to receive notifications with your production integration.

![URL](/images/cow/not3-url-es-v1.png) 

4. Select the **Payments** event to receive notifications, which will be sent in `JSON` format via an `HTTPS POST` to the URL specified earlier.

![Payment](/images/cow/not4-payment-es-v1.png)

5. Finally, click on **Save configuration**. This will generate a **secret key** exclusive to the application, which will allow you to validate the authenticity of the received notifications, ensuring they were sent by Mercado Pago. Note that this generated key does not have an expiration date and its periodic renewal is not mandatory, although it is recommended. To do this, simply click the **Reset** button.

### 2. Simulate notification reception

To ensure that notifications are configured correctly, it is necessary to simulate their reception. Follow the steps below to perform the simulation:

1. After configuring the URLs and Events, click **Save configuration**.
2. Next, click **Simulate** to test whether the specified URL is receiving notifications correctly.
3. On the simulation screen, select the URL to be tested, which can be **either the test URL or the production URL**.
4. Then, choose the **event type** and enter the **ID** that will be sent in the notification body (`Data ID`).
5. Finally, click **Send test** to verify the request, the response provided by the server, and the event description. You will receive a response similar to the example below, which represents the `body` of the notification received on your server.

```
{
  "action": "payment.updated",
  "api_version": "v1",
  "data": {
  "id": "123456"
  },
  "date_created": "2021-11-01T02:02:02Z",
  "id": "123456",
  "live_mode": false,
  "type": "payment",
  "user_id": 724484980
}
```

### 3. Validate the origin of a notification

Validating the origin of a notification is fundamental to ensuring the security and authenticity of the received information. This process helps prevent fraud and guarantees that only legitimate notifications are processed.

Mercado Pago will send a notification to your server similar to the example below for an alert with the topic `payment`. In this example, the complete notification is included, containing the `query params`, the `body`, and the `header` of the notification.

- **_Query params_**: These are query parameters that accompany the URL. In the example, we have `data.id=123456` and `type=payment`.
- **_Body_**: The body of the notification contains detailed information about the event, such as `action`, `api_version`, `data`, `date_created`, `id`, `live_mode`, `type`, and `user_id`.
- **_Header_**: The header contains important metadata, including the secret signature of the notification `x-signature`.

```
POST /test?data.id=123456&type=payment HTTP/1.1
Host: prueba.requestcatcher.com
Accept: */*
Accept-Encoding: *
Connection: keep-alive
Content-Length: 177
Content-Type: application/json
Newrelic: eyJ2IjpbMCwxXSwiZCI6eyJ0eSI6IkFwcCIsImFjIjoiOTg5NTg2IiwiYXAiOiI5NjA2MzYwOTQiLCJ0eCI6IjU3ZjI4YzNjOWE2ODNlZDYiLCJ0ciI6IjY0NjA0OTM3OWI1ZjA3MzMyZDdhZmQxMjEyM2I5YWE4IiwicHIiOjAuNzk3ODc0LCJzYSI6ZmFsc2UsInRpIjoxNzQyNTA1NjM4Njg0LCJ0ayI6IjE3MDk3MDcifX0=
Traceparent: 00-646049379b5f07332d7afd12123b9aa8-e7f77a41f687aecd-00
Tracestate: 1709707@nr=0-0-989586-960636094-e7f77a41f687aecd-57f28c3c9a683ed6-0-0.797874-1742505638684
User-Agent: restclient-node/4.15.3
X-Request-Id: bb56a2f1-6aae-46ac-982e-9dcd3581d08e
X-Rest-Pool-Name: /services/webhooks.js
X-Retry: 0
X-Signature: ts=1742505638683,v1=ced36ab6d33566bb1e16c125819b8d840d6b8ef136b0b9127c76064466f5229b
X-Socket-Timeout: 22000
{"action":"payment.updated","api_version":"v1","data":{"id":"123456"},"date_created":"2021-11-01T02:02:02Z","id":"123456","live_mode":false,"type":"payment","user_id":724484980}
```

From the received Webhook notification, you will be able to validate the authenticity of its origin. Mercado Pago will always include the secret key in the Webhook notifications that will be received, allowing you to validate their authenticity. This key will be sent in the `x-signature` header, which will be similar to the example below.

```
`ts=1742505638683,v1=ced36ab6d33566bb1e16c125819b8d840d6b8ef136b0b9127c76064466f5229b`
```

To confirm the validation, it is necessary to extract the key from the _header_ and compare it with the key provided for your application in [Your integrations](/developers/panel/app). 

Follow one of the approaches below to validate the authenticity of the notification.

::::TabsComponent

:::TabComponent{title="With SDK"}

The official SDK implements HMAC-based Webhook Signature Verification to authenticate the origin of each received notification.

To get your secret key (`secret`), select the application in [Your integrations](/developers/panel/app), click **Webhooks > Configure notification**, and reveal the generated key.

[[[
```php
<?php
use MercadoPago\Webhook\WebhookSignatureValidator;
use MercadoPago\Exceptions\InvalidWebhookSignatureException;

try {
  WebhookSignatureValidator::validate(
  $_SERVER['HTTP_X_SIGNATURE'],
  $_SERVER['HTTP_X_REQUEST_ID'],
  $_GET['data_id'],
  $secret
  );
  http_response_code(200);
} catch (InvalidWebhookSignatureException $e) {
  http_response_code(401);
}
```
```javascript
import { WebhookSignatureValidator, InvalidWebhookSignatureError } from 'mercadopago';

try {
  WebhookSignatureValidator.validate({
  xSignature: req.headers['x-signature'],
  xRequestId: req.headers['x-request-id'],
  dataId: req.query['data.id'],
  secret,
  });
  res.sendStatus(200);
} catch (err) {
  if (err instanceof InvalidWebhookSignatureError) res.status(401).end();
  else throw err;
}
```
```python
from mercadopago.webhook import WebhookSignatureValidator, InvalidWebhookSignatureError

try:
  WebhookSignatureValidator.validate(
  request.headers.get(“x-signature”),
  request.headers.get(“x-request-id”),
  request.args.get(“data.id”),
  secret,
  )
  return “”, 200
except InvalidWebhookSignatureError:
  return “”, 401
```
```go
import “github.com/mercadopago/sdk-go/pkg/webhook”

err := webhook.ValidateSignature(
  r.Header.Get(“x-signature”),
  r.Header.Get(“x-request-id”),
  r.URL.Query().Get(“data.id”),
  secret,
)
if err != nil {
  w.WriteHeader(http.StatusUnauthorized)
  return
}
w.WriteHeader(http.StatusOK)
```
```csharp
using MercadoPago.Error;
using MercadoPago.Webhook;

try {
  WebhookSignatureValidator.Validate(
  xSignature: Request.Headers[“x-signature”],
  xRequestId: Request.Headers[“x-request-id”],
  dataId: Request.Query[“data.id”],
  secret: secret);
  return Ok();
} catch (InvalidWebhookSignatureException) {
  return Unauthorized();
}
```
```java
import com.mercadopago.webhook.WebhookSignatureValidator;
import com.mercadopago.exceptions.MPInvalidWebhookSignatureException;

try {
  WebhookSignatureValidator.validate(
  request.getHeader(“x-signature”),
  request.getHeader(“x-request-id”),
  request.getParameter(“data.id”),
  secret);
  response.setStatus(200);
} catch (MPInvalidWebhookSignatureException e) {
  response.setStatus(401);
}
```
```ruby
require 'mercadopago/webhook/validator'

begin
  Mercadopago::Webhook::Validator.validate(
  request.headers['x-signature'],
  request.headers['x-request-id'],
  request.params['data.id'],
  secret
  )
  head :ok
rescue Mercadopago::Webhook::InvalidWebhookSignatureError
  head :unauthorized
end
```
]]]

:::

:::TabComponent{title="Without SDK"}

> NOTE
>
> If any of the values (`data.id`, `x-request-id`) are not present in the received notification, you must remove them from the manifest before computing the `HMAC`.

To validate the signature manually, follow these steps:

1. Extract `ts` and `v1` from the `x-signature` _header_ by splitting on `,`
2. Build the _manifest_: `id:{data.id};request-id:{x-request-id};ts:{ts};`, omitting pairs whose values are not present in the request
3. Compute `HMAC-SHA256(secret key, manifest)` in hexadecimal
4. Compare the result with `v1` in constant time
5. If they match: respond with HTTP 200. If not: respond with HTTP 401.

To get your secret key (`secret`), select the application in [Your integrations](/developers/panel/app), click **Webhooks > Configure notification**, and reveal the generated key.

![cofigure notifications](/images/cow/not6-signature-es-v1.png)

[[[
```php
<?php
$xSignature = $_SERVER['HTTP_X_SIGNATURE'] ?? '';
$xRequestId = $_SERVER['HTTP_X_REQUEST_ID'] ?? '';
$dataID = strtolower($_GET['data_id'] ?? ''); // PHP converts dots in query param names to underscores

$ts = null;
$hash = null;
foreach (explode(',', $xSignature) as $part) {
  $kv = explode('=', $part, 2);
  if (count($kv) !== 2) continue;
  $key = trim($kv[0]);
  $value = trim($kv[1]);
  if ($key === 'ts') $ts = $value;
  if ($key === 'v1') $hash = $value;
}

$parts = [];
if ($dataID !== '') $parts[] = “id:{$dataID}”;
if ($xRequestId !== '') $parts[] = “request-id:{$xRequestId}”;
$parts[] = “ts:{$ts}”;
$manifest = implode(';', $parts) . ';';

$computed = hash_hmac('sha256', $manifest, $secret);
if (!hash_equals($computed, $hash)) {
  http_response_code(401);
  exit;
}
http_response_code(200);
```
```javascript
const xSignature = req.headers['x-signature'] ?? '';
const xRequestId = req.headers['x-request-id'] ?? '';
const dataId = (req.query['data.id'] ?? '').toLowerCase();

let ts, hash;
for (const part of xSignature.split(',')) {
  const eq = part.indexOf('=');
  if (eq === -1) continue;
  const key = part.slice(0, eq).trim();
  const val = part.slice(eq + 1).trim();
  if (key === 'ts') ts = val;
  if (key === 'v1') hash = val;
}

const parts = [];
if (dataId) parts.push(`id:${dataId}`);
if (xRequestId) parts.push(`request-id:${xRequestId}`);
parts.push(`ts:${ts}`);
const manifest = parts.join(';') + ';';

const computed = crypto.createHmac('sha256', secret).update(manifest).digest('hex');
if (!crypto.timingSafeEqual(Buffer.from(computed), Buffer.from(hash))) {
  res.status(401).end();
  return;
}
res.sendStatus(200);
```
```python
import hashlib
import hmac

x_signature = request.headers.get(“x-signature”, “”)
x_request_id = request.headers.get(“x-request-id”, “”)
data_id = (request.args.get(“data.id”, “”) or “”).lower()

ts = hash_value = None
for part in x_signature.split(“,”):
  if “=” not in part:
  continue
  key, _, value = part.partition(“=”)
  key = key.strip()
  value = value.strip()
  if key == “ts”: ts = value
  if key == “v1”: hash_value = value

parts = []
if data_id: parts.append(f”id:{data_id}”)
if x_request_id: parts.append(f”request-id:{x_request_id}”)
parts.append(f”ts:{ts}”)
manifest = “;”.join(parts) + “;”

computed = hmac.new(secret.encode(), manifest.encode(), hashlib.sha256).hexdigest()
if not hmac.compare_digest(computed, hash_value):
  return “”, 401
return “”, 200
```
```go
import (
  “crypto/hmac”
  “crypto/sha256”
  “encoding/hex”
  “net/http”
  “strings”
)

xSignature := r.Header.Get(“x-signature”)
xRequestID := r.Header.Get(“x-request-id”)
dataID := strings.ToLower(r.URL.Query().Get(“data.id”))

var ts, hash string
for _, part := range strings.Split(xSignature, “,”) {
  kv := strings.SplitN(part, “=”, 2)
  if len(kv) != 2 { continue }
  key := strings.TrimSpace(kv[0])
  val := strings.TrimSpace(kv[1])
  if key == “ts” { ts = val }
  if key == “v1” { hash = val }
}

var parts []string
if dataID != “” { parts = append(parts, “id:”+dataID) }
if xRequestID != “” { parts = append(parts, “request-id:”+xRequestID) }
parts = append(parts, “ts:”+ts)
manifest := strings.Join(parts, “;”) + “;”

mac := hmac.New(sha256.New, []byte(secret))
mac.Write([]byte(manifest))
computed := hex.EncodeToString(mac.Sum(nil))

if !hmac.Equal([]byte(computed), []byte(hash)) {
  w.WriteHeader(http.StatusUnauthorized)
  return
}
w.WriteHeader(http.StatusOK)
```
```csharp
using System.Security.Cryptography;
using System.Text;

var xSignature = Request.Headers[“x-signature”].ToString();
var xRequestId = Request.Headers[“x-request-id”].ToString();
var dataId = (Request.Query[“data.id”].ToString() ?? “”).ToLowerInvariant();

string ts = null, hash = null;
foreach (var part in xSignature.Split(','))
{
  var eq = part.IndexOf('=');
  if (eq < 0) continue;
  var key = part[..eq].Trim();
  var val = part[(eq + 1)..].Trim();
  if (key == “ts”) ts = val;
  if (key == “v1”) hash = val;
}

var parts = new List<string>();
if (!string.IsNullOrEmpty(dataId)) parts.Add($”id:{dataId}”);
if (!string.IsNullOrEmpty(xRequestId)) parts.Add($”request-id:{xRequestId}”);
parts.Add($”ts:{ts}”);
var manifest = string.Join(“;”, parts) + “;”;

using var hmacSha = new HMACSHA256(Encoding.UTF8.GetBytes(secret));
var computed = BitConverter
  .ToString(hmacSha.ComputeHash(Encoding.UTF8.GetBytes(manifest)))
  .Replace(“-”, “”).ToLowerInvariant();

if (!CryptographicOperations.FixedTimeEquals(
  Encoding.UTF8.GetBytes(computed), Encoding.UTF8.GetBytes(hash)))
{
  return Unauthorized();
}
return Ok();
```
```java
import javax.crypto.Mac;
import javax.crypto.spec.SecretKeySpec;
import java.nio.charset.StandardCharsets;
import java.security.MessageDigest;
import java.util.ArrayList;
import java.util.List;

String xSignature = request.getHeader(“x-signature”) != null ? request.getHeader(“x-signature”) : “”;
String xRequestId = request.getHeader(“x-request-id”) != null ? request.getHeader(“x-request-id”) : “”;
String dataId = request.getParameter(“data.id”) != null
  ? request.getParameter(“data.id”).toLowerCase() : “”;

String ts = null, hash = null;
for (String part : xSignature.split(“,”)) {
  String[] kv = part.split(“=”, 2);
  if (kv.length != 2) continue;
  String key = kv[0].trim();
  String val = kv[1].trim();
  if (“ts”.equals(key)) ts = val;
  if (“v1”.equals(key)) hash = val;
}

List<String> parts = new ArrayList<>();
if (!dataId.isEmpty()) parts.add(“id:” + dataId);
if (!xRequestId.isEmpty()) parts.add(“request-id:” + xRequestId);
parts.add(“ts:” + ts);
String manifest = String.join(“;”, parts) + “;”;

Mac mac = Mac.getInstance(“HmacSHA256”);
mac.init(new SecretKeySpec(secret.getBytes(StandardCharsets.UTF_8), “HmacSHA256”));
byte[] bytes = mac.doFinal(manifest.getBytes(StandardCharsets.UTF_8));
StringBuilder sb = new StringBuilder();
for (byte b : bytes) sb.append(String.format(“%02x”, b & 0xff));
String computed = sb.toString();

if (!MessageDigest.isEqual(
  computed.getBytes(StandardCharsets.UTF_8),
  hash.getBytes(StandardCharsets.UTF_8)))
{
  response.setStatus(401);
  return;
}
response.setStatus(200);
```
```ruby
require 'openssl'

x_signature = request.headers['x-signature'] || ''
x_request_id = request.headers['x-request-id'] || ''
data_id = (params['data.id'] || '').downcase

ts = hash_value = nil
x_signature.split(',').each do |part|
  key, value = part.split('=', 2)
  next unless key && value
  ts = value.strip if key.strip == 'ts'
  hash_value = value.strip if key.strip == 'v1'
end

parts = []
parts << “id:#{data_id}” unless data_id.empty?
parts << “request-id:#{x_request_id}” unless x_request_id.empty?
parts << “ts:#{ts}”
manifest = “#{parts.join(';')};”

computed = OpenSSL::HMAC.hexdigest('SHA256', secret, manifest)
unless OpenSSL.fixed_length_secure_compare(computed, hash_value)
  head :unauthorized
  return
end
head :ok
```
]]]

:::

::::
:::::

:::::AccordionComponent{title="Configuration when creating preferences"}
## Configuration when creating preferences
During the process of creating [preferences](/developers/en/reference/online-payments/checkout-pro/preferences/create-preference/post), it is possible to configure the notification URL more specifically for each payment using the `notification_url` field.

> RED_MESSAGE
>
> Important
>
> The `notification_url` must be an HTTPS URL. This ensures that notifications are transmitted securely and that exchanged data is encrypted, protecting the integrity and confidentiality of the information. Additionally, HTTPS authenticates that the communication is being made with the legitimate server, avoiding possible malicious interceptions.

Below, we explain how to configure notifications when creating a payment using our SDKs.

1. In the `notification_url` field, specify the URL from which notifications will be received, as shown below.

[[[
```php
<?php
$client = new PreferenceClient();
$preference = $client->create([
  "notification_url" => "https://www.your_url_to_notification.com/",
  "items"=> array(
  array(
  "title" => "Mi producto",
  "quantity" => 1,
  "unit_price" => 2000
  )
  )
]);

echo $preference
?>

```
```node
const preference = new Preference(client);

preference.create({
  body: {
  notification_url: 'https://www.your_url_to_notification.com/',
  items: [
  {
  title: 'Mi producto',
  quantity: 1,
  unit_price: 2000
  }
  ],
  }
})
.then(console.log)
.catch(console.log);

```
```java
PreferenceItemRequest itemRequest =
  PreferenceItemRequest.builder()
  .id("1234")
  .title("Games")
  .description("PS5")
  .pictureUrl("http://picture.com/PS5")
  .categoryId("games")
  .quantity(2)
  .currencyId("BRL")
  .unitPrice(new BigDecimal("4000"))
  .build();
  List<PreferenceItemRequest> items = new ArrayList<>();
  items.add(itemRequest);
PreferenceRequest preferenceRequest = PreferenceRequest.builder()
.items(items).build();
PreferenceClient client = new PreferenceClient();
Preference preference = client.create(request);

```
```ruby
# Crea un objeto de preferencia
preference_data = {
  notification_url: 'https://www.your_url_to_notification.com/',
  items: [
  {
  title: 'Mi producto',
  unit_price: 75.56,
  quantity: 1
  }
  ]
}
preference_response = sdk.preference.create(preference_data)
preference = preference_response[:response]

# Este valor reemplazará el string "<%= @preference_id %>" en tu HTML
@preference_id = preference['id']

```
```csharp
// Crea el objeto de request de la preference
var request = new PreferenceRequest
{
  Items = new List<PreferenceItemRequest>
  {
  new PreferenceItemRequest
  {
  Title = "Mi producto",
  Quantity = 1,
  CurrencyId = "ARS",
  UnitPrice = 75.56m,
  },
  },
};

// Crea la preferencia usando el client
var client = new PreferenceClient();
Preference preference = await client.CreateAsync(request);

```
```python
# Crea un ítem en la preferencia
preference_data = {
  "notification_url" : "https://www.your_url_to_notification.com/",
  "items": [
  {
  "title": "Mi producto",
  "quantity": 1,
  "unit_price": 75.76,
  }
  ]
}

preference_response = sdk.preference().create(preference_data)
preference = preference_response["response"]
```
```go
client := preference.NewClient(cfg)

request := preference.Request{
	Items: []preference.ItemRequest{
		{
			Title: "My product",
			Quantity: 1,
			UnitPrice: 75.76,
		},
	},
}

resource, err := client.Create(context.Background(), request)
if err != nil {
	fmt.Println(err)
	return
}

fmt.Println(resource)

```
]]]

> WARNING
>
> Do not use local domains in the `notification_url` value, such as 'localhost/' or '127.0.0.1' with or without a specified port. We recommend using a server with a named domain (DNS) or an externally accessible development IP so that Mercado Pago can send notifications correctly.

2. Implement the notification receiver using the following code as an example:

```php
<?php
 MercadoPago\SDK::setAccessToken("ENV_ACCESS_TOKEN");
 switch($_POST["type"]) {
  case "payment":
  $payment = MercadoPago\Payment::find_by_id($_POST["data"]["id"]);
  break;
  case "plan":
  $plan = MercadoPago\Plan::find_by_id($_POST["data"]["id"]);
  break;
  case "subscription":
  $plan = MercadoPago\Subscription::find_by_id($_POST["data"]["id"]);
  break;
  case "invoice":
  $plan = MercadoPago\Invoice::find_by_id($_POST["data"]["id"]);
  break;
  case "point_integration_wh":
  // $_POST contiene la informaciòn relacionada a la notificaciòn.
  break;
 }
?>
```

After performing the necessary configuration, the Webhook notification will be sent in `JSON` format. Below you can see an example of a notification for the `payment` topic, and the descriptions of the information sent in the table below.

> RED_MESSAGE
>
> Important
>
> Test payments, created with test credentials, will not send notifications. The only way to test notification reception is through [Configuration via Your integrations](/developers/en/docs/checkout-pro/payment-notifications#bookmark_configuration_through_your_integrations).

```json
{
 "id": 12345,
 "live_mode": true,
 "type": "payment",
 "date_created": "2015-03-25T10:04:58.396-04:00",
 "user_id": 44444,
 "api_version": "v1",
 "action": "payment.created",
 "data": {
  "id": "999999999"
 }
}
```

| Attribute | Description | Example in JSON |
| --- | --- | --- |
| **id** | Notification ID | `12345` |
| **live_mode** | Indicates if the entered URL is valid. | `true` |
| **type** | Type of notification received according to the previously selected topic (payments, mp-connect, subscription, claim, automatic-payments, etc) | `payment` |
| **date_created** | Creation date of the notified resource | `2015-03-25T10:04:58.396-04:00` |
| **user_id** | Seller identifier | `44444` |
| **api_version** | Value indicating the API version that sends the notification | `v1` |
| **action** | Notified event, indicating whether it is an update of a resource or the creation of a new one | `payment.created` |
| **data.id** | ID of the payment, commercial order, or claim. | `999999999` |
:::::

Once notifications are configured, check the Necessary actions after receiving a notification to inform that they were properly received.

## Necessary actions after receiving the notification

When you receive a notification on your platform, Mercado Pago expects a response to validate that the reception was correct. For this, you must return an `HTTP STATUS 200 (OK)` or `201 (CREATED)`.

The timeout for this confirmation will be 22 seconds. If this response is not sent, the system will understand that the notification was not received and will make a new attempt to send it every 15 minutes until it receives the response. After the third attempt, the interval will be extended, but the sending will continue.

<pre class="mermaid">
sequenceDiagram
  participant MercadoPago as Mercado Pago
  participant Integrator as Integrator

  MercadoPago->>Integrator: retry: 1. Delay: 0 minutes
  MercadoPago->>Integrator: retry: 2. Delay: 15 minutes
  MercadoPago->>Integrator: retry: 3. Delay: 30 minutes
  MercadoPago->>Integrator: retry: 4. Delay: 6 hours
  MercadoPago->>Integrator: retry: 5. Delay: 48 hours
  MercadoPago->>Integrator: retry: 6. Delay: 96 hours
  MercadoPago->>Integrator: retry: 7. Delay: 96 hours
  MercadoPago->>Integrator: retry: 8. Delay: 96 hours
</pre>

After responding to the notification, confirming its receipt, you can obtain all information about the notified `payments` topic event by making a GET request to the endpoint [v1/payments/{id}](/developers/en/reference/online-payments/checkout-pro/get-payment/get).

With this information, you will be able to make the necessary updates to your platform, such as updating an approved payment.

Additionally, to check the status of the event after the notification, you can use the various methods of our SDKs to perform the query with the ID that was sent in the notification.

[[[
```java
MercadoPago.SDK.setAccessToken("ENV_ACCESS_TOKEN");
switch (type) {
  case "payment":
  Payment payment = Payment.findById(data.id);
  break;
  case "plan":
  Plan plan = Plan.findById(data.id);
  break;
  case "subscription":
  Subscription subscription = Subscription.findById(data.id);
  break;
  case "invoice":
  Invoice invoice = Invoice.findById(data.id);
  break;
  case "point_integration_wh":
  // POST contiene la informaciòn relacionada a la notificaciòn.
  break;
}
```
```node
mercadopago.configurations.setAccessToken('ENV_ACCESS_TOKEN');
switch (type) {
  case 'payment':
  const payment = await mercadopago.payment.findById(data.id);
  break;
  case 'plan':
  const plan = await mercadopago.plans.get(data.id);
  break;
  case 'subscription':
  const subscription = await mercadopago.subscriptions.get(data.id);
  break;
  case 'invoice':
  const invoice = await mercadopago.invoices.get(data.id);
  break;
  case 'point_integration_wh':
  // Contiene la informaciòn relacionada a la notificaciòn.
  break;
}
```
```ruby
sdk = Mercadopago::SDK.new('PROD_ACCESS_TOKEN')

case payload['type']
when 'payment'
  payment = sdk.payment.search(filters: { id: payload['data']['id'] })
when 'plan'
  plan = sdk.preapproval_plan.search(filters: { id: data['data']['id'] })
end
```
```csharp
MercadoPagoConfig.AccessToken = "ENV_ACCESS_TOKEN";
switch (type)
{
  case "payment":
  Payment payment = await Payment.FindByIdAsync(payload["data"]["id"].ToString());
  break;
  case "plan":
  Plan plan = await Plan.FindByIdAsync(payload["data"]["id"].ToString());
  break;
  case "subscription":
  Subscription subscription = await Subscription.FindByIdAsync(payload["data"]["id"].ToString());
  break;
  case "invoice":
  Invoice invoice = await Invoice.FindByIdAsync(payload["data"]["id"].ToString());
  break;
  case "point_integration_wh":
  // Contiene la informaciòn relacionada a la notificaciòn.
  break;
}
```
```python
sdk = mercadopago.SDK("ENV_ACCESS_TOKEN")
notification_type = data["type"]
if notification_type == "payment":
  payment = sdk.payment().get(payload["data"]["id"])
elif notification_type == "plan":
  plan = sdk.preapproval().get(payload["data"]["id"]) 
elif notification_type == "subscription":
  subscription = sdk.preapproval().get(payload["data"]["id"])
elif notification_type == "invoice":
  invoice = sdk.invoice().get(payload["data"]["id"])
elif notification_type == "point_integration_wh":
  # Contiene la informaciòn relacionada a la notificaciòn.
else:
  return
```
```golang
cfg, err := config.New("ENV_ACCESS_TOKEN")
if err != nil {
  fmt.Println(err)
}

switch req.Body.Type {
case "payment":
  client := payment.NewClient(cfg)
  resource, err = client.Get(context.Background(), req.Body.data.id)
  if err != nil {
  fmt.Println(err)
  return
  }
case "plan":
  client := preapprovalplan.NewClient(cfg)
  resource, err := client.Get(context.Background(), req.Body.data.id)
  if err != nil {
  fmt.Println(err)
  return
  }
}
```
]]]


# Integration test

Testing is an essential step to ensure that the integration is working correctly and that payments are processed without errors. This prevents failures when the checkout is available to buyers. 

For this, use the test buyer account automatically created with your application. With it, you can simulate payments and validate their functionality.

Below, we present the step-by-step process:

## Get a test buyer account

To test the integration, make a test purchase using the test buyer account that was automatically created with your application. To find it, follow the steps below.

1. In [Mercado Pago Developers](/developers/en/docs), navigate to [Your integrations](/developers/panel/app) at the top right of the screen and click on the card corresponding to the application you are developing.
2. After accessing "Integration data," go to the **Test Accounts** section in the left sidebar.
3. In the selector menu, click on **Buyer**. Once there, you will see the **operating country** of the account, the **User ID**, the **username** and **password** of the test account.

![testuser](/images/snippets/test-cross/test-accounts-buyer-es-v1.png)

> NOTE
>
> If you need to run tests for another country, create a [test account](/developers/en/docs/checkout-pro/test-accounts) of type **Seller** and another of type **Buyer**, making sure to select the country you want to integrate.

# Perform test purchases

After setting up your test environment, you can perform test purchases to validate your integration with Checkout Pro and ensure that the configured payment methods work correctly. Below, we will show you how to carry out different checks in your integration.

> RED_MESSAGE
>
> Perform test purchases in an **incognito browser tab** to avoid errors from duplicate credentials during the process.

## Test a purchase with card

To test a purchase with a credit or debit card, follow these steps:

1. Access [Mercado Pago Developers](/developers/en/docs) and log in as a **test buyer user** that you created previously. Use the username and password assigned to it. You can find these details in the documentation [Integration test > Get a test buyer account](/developers/en/docs/checkout-pro/integration-test).

> NOTE
>
> If you are asked for a code by email when logging in, enter the **6 digits code** associated with your test account, which you can find in **[Your integrations](/developers/panel/app) > *Your application* > Test accounts**.

2. Initialize the Checkout from the payment preference you created. You can find instructions on how to initialize it in the documentation [Add the SDK to the Frontend and Initialize Checkout](/developers/en/docs/checkout-pro/web-integration/add-frontend-sdk).
3. **In an incognito browser window**, access the store where you integrated Checkout Pro, select a product or service, and at the payment instance, click on the Mercado Pago purchase button.
4. Finally, perform a test purchase using the **test card** details shown below. Note that you can **simulate different purchase outcomes** using different cardholder names on the test cards.

### Test cards

Mercado Pago provides **test cards** that will allow you to test payments without using a real card.

Their data, such as number, security code, and expiration date, can be combined with the **data relating to the cardholder**, which will allow you to test different payment scenarios. That is, **you can use the information of any test card and test different payment results based on the cardholder's data**.

Below, you can see the data of the **test debit and credit cards**. Select the one you want to use to test your integration.

| Card type | Flag | Number | Security code | Expiration date |
| :--- | :---: | :---: | :---: | :---: |
| Credit card | Mastercard | 5416 7526 0258 2580 | 123 | 11/30 |
| Credit card | Visa | 4168 8188 4444 7115 | 123 | 11/30 |
| Credit card | American Express | 3757 781744 61804 | 1234 | 11/30 |
| Debit card | Mastercard | 5241 0198 2664 6950 | 123 | 11/30 |
| Debit card | Visa | 4023 6535 2391 4373 | 123 | 11/30 |

Next, choose which payment scenario to test and fill in the **cardholder's information** (First name and last name, Document type and number) as indicated in the table below.

| Payment Status | Cardholder’s first and last name | Identity document |
| --- | --- | --- |
| Approved payment | `APRO` | (otro) 123456789 |
| Declined for general error | `OTHE` | (otro) 123456789 |
| Pending payment | `CONT` | - |
| Declined with validation to authorize | `CALL` | - |
| Declined for insufficient amount | `FUND` | - |
| Declined for invalid security code | `SECU` | - |
| Declined due to due date issue | `EXPI` | - |
| Declined due to form error | `FORM` | - |
| Rejected for missing card_number | `CARD` | - |
| Rejected for invalid installments | `INST` | - |
| Rejected for duplicate payment | `DUPL` | - |
| Rejected for disabled card | `LOCK` | - |
| Rejected for non-permitted card type | `CTNA` | - |
| Rejected due to exceeded PIN attempts | `ATTE` | - |
| Rejected for being on the blacklist | `BLAC` | - |
| Not supported | `UNSU` | - |
| Used to apply amount rules | `TEST` | - |

Once you have completed all the fields correctly, click the button to process the payment, and wait for the result. If the test is successful, you will see the test purchase success screen.

If you have configured [notifications](/developers/en/docs/checkout-pro/payment-notifications), verify that you are receiving the notifications corresponding to the test transaction.

# Go to production

Once the configuration and testing process is complete, your integration will be ready to receive real payments in production.

Below, you will find the necessary recommendations to make this transition effectively and safely, ensuring that your integration is prepared to receive real transactions.

:::AccordionComponent{title="Activate production credentials" pill="1"}
After performing the appropriate [integration tests](/developers/en/docs/checkout-api-payments/integration-test), **remember to replace the :toolTipComponent[credentials]{link="/developers/en/docs/checkout-api-payments/resources/credentials" linkText="Credentials" content="Unique access keys that identify an integration in your account, linked to your application. For more information, access the link below."} you used in the development stage with production credentials** so you can start operating in your store's production environment and begin receiving real payments. To do this, follow the steps below to learn how to **activate them**.

1. Go to [Your integrations](https://www.mercadopago[FAKER][URL][DOMAIN]/developers/panel/app) and select an application.
2. In the **Integration data** section, go to the **Credentials** section located on the right side of the screen and click **Production**. Click **Activate credentials**. Alternatively, you can go to the **Production credentials** section in the left side menu.
3. In the **Industry** field, select from the dropdown menu the industry or sector to which the business you are integrating belongs.
4. In the **Website (required)** field, complete with the URL of your business website.
5. Accept the [Privacy Statement](https://www.mercadopago[FAKER][URL][DOMAIN]/privacidad) and the [Terms and conditions](/developers/en/docs/resources/legal/terms-and-conditions). Complete the reCAPTCHA and click **Activate production credentials**.
:::

:::AccordionComponent{title="Use production credentials" pill="2"}
To go live, you need to **place the production credentials of your Mercado Pago application** in your integration.

To do this, go to [Your integrations](/developers/panel/app), go to the **Credentials** section located on the right side of the screen and click **Production**. Alternatively, you can access **Production > Production credentials**.

There you will find your productive **Public Key** and **Access Token**, which you should use instead of the test account credentials.

![How to access credentials through Your Integrations](/images/snippets/credentials/app-data-production-credentials-es-v1.png)

For more information, check our [Credentials](/developers/en/docs/checkout-pro/additional-content/credentials) documentation.
:::

:::AccordionComponent{title="Implement SSL certificate" pill="3"}
To ensure a secure integration that protects the data of every transaction, it is essential to implement an SSL (Secure Sockets Layer) certificate. This certificate, together with the use of the HTTPS protocol when providing payment methods, guarantees an encrypted connection between the client and the server.

Adopting these measures not only strengthens the security of user data, but also ensures compliance with the specific regulations and laws of each country regarding data protection and information security. In addition, it significantly contributes to providing a safer and more reliable shopping experience.

Although **the SSL certificate is not required during the testing period**, its implementation is mandatory for production.

For more information, see the [Mercado Pago Terms and Conditions](/developers/en/docs/resources/legal/terms-and-conditions).
:::

:::AccordionComponent{title="Measure the quality of your integration" pill="Optional"}
Once you have finished setting up your integration, we recommend that you perform a **quality measurement**, which is a certification process for your integration. This will ensure that your development meets the necessary quality requirements to provide a better experience and a higher payment approval rate.

To learn more, visit the [How to measure the quality of your integration](/developers/en/docs/checkout-pro/how-tos/integration-quality) documentation.
:::



# Configure refunds and cancellations

**Refunds** and **cancellations** are actions available after a payment has been made. While both involve returning money, it is crucial to understand their differences to correctly execute each process.

- **Cancellation**: It is performed when a payment has not been finalized or is in process. In this case, the amount is refunded to the buyer's card within the time frame established by the issuing bank.

- **Refund**: Occurs after the payment has been captured. The amount is refunded directly to the statement (for credit card payments) or to the payer's account (for other methods).

Below are the essential details about each process.

> RED_MESSAGE
>
> This documentation is **intended for integrators**. If you are a buyer and need to cancel or request a refund for a payment, log in to your Mercado Pago account, select the purchase you want to request it for, click on "I need help" and choose the refund or cancellation option.

## Refunds

Refunds refer to the reversal of a charge, returning the amount to the buyer. This process is managed directly through the API [Create refund](/developers/en/reference/online-payments/checkout-pro/create-refund/post).

Refunds can be made in two ways:

- **Total**: The full amount of the sale is refunded to the buyer. In this case, the request `body` must be sent empty.
- **Partial**: Only a portion of the paid amount is refunded to the buyer. The amount to be refunded must be specified in the request `body`, along with the transaction ID.

Before making a refund, it is important to consider the following factors:

- **Refund period**: Refunds can be issued within 180 days after the payment approval.
- **Payment method**: Credit card payments are refunded to the statement; other methods refund the amount to the payer's account.
- **Account balance**: It is necessary to have sufficient balance available in your account to perform the refund; otherwise, the transaction will be rejected.
- **Manual order processing**: Only individual transactions can be refunded manually. To refund a complete purchase, all associated transactions must be fully reversed.

To perform total or partial refunds of a payment and check the refunds made in your store, consult the APIs [Create refund](/developers/en/reference/online-payments/checkout-pro/create-refund/post), [Get refund list](/developers/en/reference/online-payments/checkout-pro/get-refunds/get), and [Get specific refund](/developers/en/reference/online-payments/checkout-pro/get-refund/get).

## Cancellations

**Cancellations** are operations performed when a purchase is made, but the payment is not approved for some reason. In this case, as the transaction was not completed and no amount was processed, the purchase is voided, and no charge is made.

Before canceling a purchase, it is important to pay attention to the following factors:

- **Payment status**: Cancellations can only be performed if the payment status is `pending` or `in_process`. These details are displayed in the `status` and `status_detail` fields of the response from the API [Create cancellation](/developers/en/reference/online-payments/checkout-pro/create-cancellation/put).
- **Expiration period**: Payments automatically expire after 30 days without confirmation. The final status will be `canceled` or `expired`, as indicated in the `status` and `status_detail` fields of the API [Create cancellation](/developers/en/reference/online-payments/checkout-pro/create-cancellation/put).

For more information, consult the API [Create cancellation](/developers/en/reference/online-payments/checkout-pro/create-cancellation/put) API.


# Configure other payment methods

By default, all payment methods are available in Checkout Pro. This setting can be customized through the payment preference, allowing you to remove unwanted options.

> WARNING
>
> The payment method **Cash in account** cannot be excluded.

The following table lists the available attributes in the payment preferences and the application of each one to configure them according to the business needs.

| Preference Attribute | Description | Possible values |
| --- | --- | --- |
| `payment_methods` | Class that describes the attributes and methods of the Checkout Pro payment methods. | - |
| `excluded_payment_types` | Allows you to exclude unwanted payment method types, such as offline payments, credit or debit cards, among others. You can obtain a detailed list of all available payment types for integration by sending a **GET** request with your :toolTipComponent[Access Token]{content="Private key of the application created in Mercado Pago, which is used in the _backend_. You can access it through *Your integrations > Integration data > Test > Test credentials* or *Production > Production credentials*."} to the endpoint :TagComponent{tag="API" text="/v1/payment_methods" href="/developers/en/reference/online-payments/checkout-pro/payment-methods/get"}. | `ticket` |
| `excluded_payment_methods` | Allows you to exclude specific credit and debit card brands, such as Visa, Mastercard, American Express, among others. You can obtain a detailed list of all available payment methods for integration by sending a **GET** request with your :toolTipComponent[Access Token]{content="Private key of the application created in Mercado Pago, which is used in the _backend_. You can access it through *Your integrations > Integration data > Test > Test credentials* or *Production > Production credentials*."} to the endpoint :TagComponent{tag="API" text="/v1/payment_methods" href="/developers/en/reference/online-payments/checkout-pro/payment-methods/get"}. | `master` |
| `installments` | Defines the maximum number of installments that can be offered to the buyer. | `10` |

With this information, use one of the available SDKs to configure the payment methods you want to exclude.

[[[
```curl
"payment_methods": {
  "excluded_payment_methods": [
  {
  "id": "master"
  }
  ],
  "excluded_payment_types": [
  {
  "id": "ticket"
  }
  ]
}
```
```php
<?php
$preference = new MercadoPago\Preference();
// ...
$preference->payment_methods = array(
"excluded_payment_methods" => array(
array("id" => "master")
),
"excluded_payment_types" => array(
array("id" => "ticket")
),
"installments" => 12
);
// ...
?>
```
```node
const preference = new Preference(client);
	preference.create({
		body: {
			// ...
			payment_methods: {
				excluded_payment_methods: [
					{
						id: "master"
					}
				],
				excluded_payment_types: [
					{
						id: "ticket"
					}
				],
				installments: 12
			}
		}
	})
// ...
```
```java
PreferenceClient client = new PreferenceClient();
//...
List<PreferencePaymentMethodRequest> excludedPaymentMethods = new ArrayList<>();
excludedPaymentMethods.add(PreferencePaymentMethodRequest.builder().id("master").build());
excludedPaymentMethods.add(PreferencePaymentMethodRequest.builder().id("amex").build());

List<PreferencePaymentTypeRequest> excludedPaymentTypes = new ArrayList<>();
excludedPaymentTypes.add(PreferencePaymentTypeRequest.builder().id("ticket").build());

PreferencePaymentMethodsRequest paymentMethods =
PreferencePaymentMethodsRequest.builder()
.excludedPaymentMethods(excludedPaymentMethods)
.excludedPaymentTypes(excludedPaymentTypes)
.installments(12)
.build();

PreferenceRequest request = PreferenceRequest.builder().paymentMethods(paymentMethods).build();

client.create(request);
//...
```
```ruby
#...
preference_data = {
# ...
payment_methods: {
excluded_payment_methods: [
{ id: 'master' }
],
excluded_payment_types: [
{ id: 'ticket' }
],
installments: 12
}
# ...
}
#...
```
```csharp
var paymentMethods = new PreferencePaymentMethodsRequest
{
ExcludedPaymentMethods = new List<PreferencePaymentMethodRequest>
{
new PreferencePaymentMethodRequest
{
Id = "master",
},
},
ExcludedPaymentTypes = new List<PreferencePaymentTypeRequest>
{
new PreferencePaymentTypeRequest
{
Id = "ticket",
},
},
Installments = 12,
};

var request = new PreferenceRequest
{
// ...
PaymentMethods = paymentMethods,
};
```
```python
#...
preference_data = {
"excluded_payment_methods": [
{ "id": "master" }
],
"excluded_payment_types": [
{ "id": "ticket" }
],
"installations": 12
}
#...
```
]]]


# Restrict purchases to registered users only

Allows only users with a Mercado Pago account to make purchases in your Checkout Pro. When enabling this restriction, only authenticated customers will be able to access the checkout, log in and use the available payment methods to complete the purchase.

> WARNING
>
> By adding this option, it will not be possible to receive payments from users not registered in Mercado Pago, as well as you will not be able to receive payments via cash or bank transfer.

Follow the steps below to configure the Mercado Pago account as the only payment method available in the checkout.

::::TabsComponent

:::TabComponent{title="Configure via frontend SDK"}

To restrict payments to users with a Mercado Pago account only, include the `purpose` parameter with the value `wallet_purchase` in the payment preference configuration. Below, see implementation examples using the Mercado Pago SDK for integration.

[[[
```php
===
Mercado Pago Account mode works by adding the _purpose_ attribute to the preference.
===
<?php
  $client = new PreferenceClient();
  $preference = $client->create([
  "items"=> array(
  array(
  "title" => "My product",
  "description" => "Test product",
  "picture_url" => "http://i.mlcdn.com.br/portaldalu/fotosconteudo/48029_01.jpg",
  "category_id" => "electronics",
  "quantity" => 1,
  "currency_id" => "BRL",
  "unit_price" => 100
  )
  ),
  "purpose"=> "wallet_purchase"
  ]);
  echo implode($preference);
?>
```
```node
===
Mercado Pago Account mode works by adding the _purpose_ attribute to the preference.
===
const client = new MercadoPagoConfig({ accessToken: '<ACCESS_TOKEN>' });

const preference = new Preference(client);

preference.create({ 
  body: {
  items: [
  {
  id: '<ID>',
  title: '<title>',
  quantity: 1,
  unit_price: 100
  }
  ],
  purpose: "wallet_purchase",
  }
}).then(console.log).catch(console.log);
```
```java
===
Mercado Pago Account mode works by adding the _purpose_ attribute to the preference.
===
// Create a preference object
PreferenceClient client = new PreferenceClient();

// Create an item in the preference
PreferenceItemRequest item =
  PreferenceItemRequest.builder()
  .title("My product")
  .quantity(1)
  .unitPrice(new BigDecimal("75"))
  .build();

List<PreferenceItemRequest> items = new ArrayList<>();
items.add(item);

PreferenceRequest request =
  PreferenceRequest.builder().items(items).purpose("wallet_purchase").build();

client.create(request);
```
```ruby
===
Mercado Pago Account mode works by adding the _purpose_ attribute to the preference.
===
sdk = Mercadopago::SDK.new('ENV_ACCESS_TOKEN')
# Create a preference object
preference_data = {
  items: [
  {
  title: 'My product',
  unit_price: 100,
  quantity: 1
  }
  ],
  purpose: 'wallet_purchase'
}
preference_response = sdk.preference.create(preference_data)
preference = preference_response[:response]

# This value will replace the string "<%= @preference_id %>" in your HTML
@preference_id = preference['id']
```
```csharp
===
Mercado Pago Account mode works by adding the _purpose_ attribute to the preference.
===
// Create the preference request object
var request = new PreferenceRequest
{
  Items = new List<PreferenceItemRequest>
  {
  new PreferenceItemRequest
  {
  Title = "My product",
  Quantity = 1,
  CurrencyId = "[FAKER][CURRENCY][ACRONYM]",
  UnitPrice = 75m,
  },
  },
  Purpose = "wallet_purchase",
};
// Create the preference
var client = new PreferenceClient();
Preference preference = await client.CreateAsync(request);
```
```python
===
Mercado Pago Account mode works by adding the _purpose_ attribute to the preference.
===
preference_data = {
  "items": [
  {
  "title": "My product",
  "unit_price": 100,
  "quantity": 1
  }
  ],
  "purpose": "wallet_purchase"
}

preference_response = sdk.preference().create(preference_data)
preference = preference_response["response"]
```
```go
===
Mercado Pago Account mode works by adding the _purpose_ attribute to the preference.
===
import (
	"context"
	"fmt"
	"time"

	"github.com/mercadopago/sdk-go/pkg/config"
	"github.com/mercadopago/sdk-go/pkg/preference"
)

cfg, err := config.New("{{ACCESS_TOKEN}}")
if err != nil {
  fmt.Println(err)
}

client := preference.NewClient(cfg)

request := preference.Request{
	Items: []preference.ItemRequest{
		{
			Title: "My product",
			UnitPrice: 100,
			Quantity: 1,
		},
	},
	Purpose: "wallet_purchase",
}

resource, err := client.Create(context.Background(), request)
if err != nil {
	fmt.Println(err)
	return
}

fmt.Println(resource)
```
]]]

> WARNING
>
> Important
>
> The `unit_price` value must be an integer.

:::

:::TabComponent{title="Configure via API"}

To restrict payments only to users with a Mercado Pago account, send a **POST** request to the endpoint :TagComponent{tag="API" text="/checkout/preferences" href="https://www.mercadopago[FAKER][URL][DOMAIN]/developers/pt/reference/online-payments/checkout-pro/preferences/create-preference/post"} including the `purpose` parameter with the value `wallet_purchase`.

```cURL
curl -X POST \
  'https://api.mercadopago.com/checkout/preferences'\
  -H 'Content-Type: application/json' \
  -H 'Authorization: Bearer TEST-484********49456-07********cb4fb5d7********240915e1********548830' \
  -d '{
  "items": [
  {
  "id": "Sound system",
  "title": "Dummy Title",
  "description": "Dummy description",
  "picture_url": "https://www.myapp.com/myimage.jpg",
  "category_id": "car_electronics",
  "quantity": 1,
  "currency_id": "BRL",
  "unit_price": 10
  }
  ],
  "purpose": "wallet_purchase",
  "payer": {
  "name": "John",
  "surname": "Doe",
  "email": "john@doe.com",
  "phone": {
  "area_code": "11",
  "number": 988888888
  },
  "identification": {
  "type": "CPF",
  "number": "19119119100"
  },
  "address": {
  "zip_code": "06233200",
  "street_name": "Example Street",
  "street_number": 123
  },
  "date_created": "2024-04-01T00:00:00Z"
  },
  "payment_methods": {
  "excluded_payment_methods": [
  {
  "id": "master"
  }
  ],
  "excluded_payment_types": [
  {
  "id": "ticket"
  }
  ],
  "default_payment_method_id": "amex",
  "installments": 10,
  "default_installments": 5
  },
  "shipments": {
  "local_pickup": false,
  "dimensions": "32 x 25 x 16",
  "default_shipping_method": null,
  "free_methods": [
  {
  "id": null
  }
  ],
  "cost": 20,
  "free_shipping": false,
  "receiver_address": {
  "zip_code": "72549555",
  "street_name": "Street address test",
  "city_name": "São Paulo",
  "state_name": "São Paulo",
  "street_number": 100,
  "country_name": "Brazil"
  }
  },
  "back_urls": {
  "success": "https://test.com/success",
  "pending": "https://test.com/pending",
  "failure": "https://test.com/failure"
  },
  "notification_url": "https://notificationurl.com",
  "additional_info": "Discount 12.00",
  "auto_return": "approved",
  "external_reference": "1643827245",
  "expires": false,
  "expiration_date_from": "2022-11-17T09:37:52.000-04:00",
  "expiration_date_to": "2022-11-17T10:37:52.000-05:00",
  "marketplace": "NONE",
  "marketplace_fee": 0,
  "differential_pricing": {
  "id": 1
  },
  "tracks": [
  {
  "type": "google_ad",
  "values": {
  "conversion_id": 123,
  "conversion_label": "abc",
  "pixel_id": "abc"
  }
  }
  ],
  "metadata": null
}'
```
:::
::::


# Create preference for multiple items

To create a preference with more than one item, you need to add these items to a list and provide the required attributes for each of them.

> NOTE
>
> In addition to the SDKs, it is also possible to create a preference for multiple items directly through the Preferences API. To do this, send a POST request to the endpoint :TagComponent{tag="API" text="/checkout/preferences" href="/developers/en/reference/online-payments/checkout-pro/preferences/create-preference/post"}, including all desired items in the `items` array.

Use one of the available SDKs to perform this operation:

[[[
```php
<?php
# Create a preference object
$preference = new MercadoPago\Preference();
# Create items in preference
$item1 = new MercadoPago\Item();
$item1->title = "Test Item 1";
$item1->quantity = 2;
$item1->unit_price = 11.96;

$item2= new MercadoPago\Item
$item2->title = "Test Item 2";
$item2->quantity = 1;
$item2->unit_price = 11.96;

$preference->items = array($item1,$item2);
# Save and post the preference
$preference->save();
?>
```
```node
const preference = new Preference(client);
	preference.create({
		body: {
			// ...
			items: [
  {
  title: 'My product 1',
  quantity: 1,
  unit_price: 100
  },
  {
  title: 'My product 2',
  quantity: 1,
  unit_price: 150
  }
  ],
		}
	})
// ...
```
```java
// Create a preference object
PreferenceClient client = new PreferenceClient();
// Create items in preference
PreferenceClient client = new PreferenceClient();

List<PreferenceItemRequest> items = new ArrayList<>();

PreferenceItemRequest item1 =
PreferenceItemRequest.builder()
.id("1234")
.title("Product 1")
.quantity(2)
.currencyId("BRL")
.unitPrice(new BigDecimal("100"))
.build();
PreferenceItemRequest item2 =
PreferenceItemRequest.builder()
.id("12")
.title("Product 2")
.quantity(1)
.currencyId("BRL")
.unitPrice(new BigDecimal("100"))
.build();

items.add(item1);
items.add(item2);

PreferenceRequest request = PreferenceRequest.builder().items(items).build();
// Save and post the preference
client.create(request);
```
```ruby
  sdk = Mercadopago::SDK.new('ENV_ACCESS_TOKEN')
  # Create preference data with items
  preference_data = {
  items: [
  {
  title: 'My product 1',
  quantity: 1,
  unit_price: 75.56
  },
  {
  title: 'My Product 2',
  quantity: 2,
  unit_price: 96.56
  }
  ]
  }

  preference_response = sdk.preference.create(preference_data)
  preference = preference_response[:response]
```
```python
# Create items in preference
preference_data = {
"items": [
{
"title": "My product",
"quantity": 1,
"unit_price": 75.56
},
{
"title": "My product2",
"quantity": 2,
"unit_price": 96.56
}
]
}

# Create the preference
preference_response = sdk.preference().create(preference_data)
preference = preference_response["response"]
```
```csharp
// Create the request with multiple items
var request = new PreferenceRequest
{
Items = new List<PreferenceItemRequest>
{
new PreferenceItemRequest
{
Title = "My Product 1",
quantity = 1,
CurrencyId = "[FAKER][CURRENCY][ACRONYM]",
UnitPrice = 75.56m,
},
new PreferenceItemRequest
{
Title = "My Product 2",
quantity = 2,
CurrencyId = "[FAKER][CURRENCY][ACRONYM]",
UnitPrice = 96.56m,
},
// ...
},
};

// Create a client object
var client = new PreferenceClient();

// Create the preference
Preference preference = await client.CreateAsync(request);
```
]]]

The total value of the preference will be the sum of the price value of each item listed.

# Display shipping cost

Display the shipping cost in the checkout as a separate item from the total purchase amount, allowing the customer to see how much they are paying for the products and how much for shipping before completing the transaction.

To do this, send a **POST** request to the endpoint :TagComponent{tag="API" text="/checkout/preferences" href="https://www.mercadopago[FAKER][URL][DOMAIN]/developers/pt/reference/online-payments/checkout-pro/preferences/create-preference/post"} including the `cost` and `mode` attributes within the `shipments` parameter, as shown in the example below.

```json
{
  "shipments":{
  "cost": 1000,
  "mode": "not_specified",
  }
}
```

| Parameter | Type | Description |
|---|---|---|
| `cost` | Number | Shipping cost value. |
| `mode` | String | Shipping mode. Use `not_specified` to display the cost separately without specifying the shipping method. |


# Change expiration date

The expiration date represents the maximum deadline to make a payment. With Checkout Pro, you can customize the default expiration date for **offline payments**by using the `date_of_expiration` field in the preference creation request.

> WARNING
>
> The crediting timeframe is up to 2 business hours depending on the payment method. Therefore, we recommend setting the expiration date at least 3 days apart to ensure payment is made. In addition, if payment is made after the expiration date, the amount will be refunded to the payer's Mercado Pago account.

To change the expiration date of an existing preference, send a **PUT** request to the endpoint :TagComponent{tag="API" text="/checkout/preferences/{id}" href="/developers/en/reference/online-payments/checkout-pro/preferences/update-preference/put"}, including the `date_of_expiration` parameter with the new expiration date and time for the item.

[[[
```json
===
The date uses the ISO 8601 format: yyyy-MM-dd'T'HH:mm:ssz.
===
"date_of_expiration": "2020-05-30T23:59:59.000-04:00"
```
]]]


# Opening scheme with external redirect

The opening scheme defines how the checkout will be displayed to the user. Checkout Pro offers two modalities:

- **Redirect (default)**: redirects the user within the same browser window
- **External redirect**: opens the checkout in a new window or tab

This configuration can be done via SDK or API. Select the option you prefer and follow the steps below.

> WARNING
>
> Configure the `back_urls` correctly when creating the preference. Without them, users will not be automatically redirected to your website after payment, remaining on the Mercado Pago page. See [Configure return URLs](/developers/en/docs/checkout-pro/configure-back-urls) for more details.

::::TabsComponent

:::TabComponent{title="Configure via frontend SDK"}
## Configure external redirect

To open the checkout in a new window or tab, use the `redirectMode` property with the `blank` value when [initializing the checkout from the payment preference](/developers/en/docs/checkout-pro/web-integration/add-frontend-sdk#bookmark_initialize_the_checkout_from_the_payment_preference).

| Value | Behavior |
| --- |--- |
| `self` | Redirects in the same window (default behavior). |
| `blank` | Opens the checkout in a new window or tab. |

You can use the following example to implement a payment in **redirect** mode:

[[[
```Javascript
mp.bricks().create("wallet", "wallet_container", {
  initialization: {
  preferenceId: "<PREFERENCE_ID>",
  redirectMode: "blank"
  },
});
```
```react-jsx
<Wallet initialization={{ preferenceId: '<PREFERENCE_ID>', redirectMode: 'blank' }} />
```
]]]
:::

:::TabComponent{title="Configure via API"}
## Configure external redirect

To configure the external redirect, you need to use the `init_point` attribute that you receive in the response after [creating and configuring a payment preference](/developers/en/docs/checkout-pro/create-payment-preference) using the endpoint :TagComponent{tag="API" text="/checkout/preferences" href="https://www.mercadopago[FAKER][URL][DOMAIN]/developers/en/reference/online-payments/checkout-pro/preferences/create-preference/post"}. Include this value in your project's frontend to perform the redirection.

```html
<a href="YOUR_INIT_POINT"> <!-- Replace with the init_point from the API response -->
  <button>
  Pay with Mercado Pago
  </button>
</a>
```

To redirect the buyer to a new window or tab, use the following example:

```html
<a href="YOUR_INIT_POINT" target="_blank"> <!-- Add target="_blank" to open in new window -->
  <button>
  Pay with Mercado Pago
  </button>
</a>
```
:::
::::


# Configure invoice description

The invoice description allows you to define the name of the establishment that will be displayed on the buyer’s invoice, making it easier to identify the business and reducing the chance of disputes.

To configure this information, send a **POST** request to the endpoint :TagComponent{tag="API" text="/checkout/preferences" href="/developers/en/reference/online-payments/checkout-pro/preferences/create-preference/post"}, including the `statement_descriptor` parameter. This parameter allows a text of up to 13 characters that will be shown on the buyer’s card statement. See the example below:

```json
"statement_descriptor": "MYBUSINESS"
```

# Configure the payment button appearance

The Mercado Pago payment button is composed of the banner's textual content and the value proposition. You can customize the appearance of the Mercado Pago payment button to adapt it to your website.
Below, learn about the different customizations you can apply.

## Change the button appearance

You can modify the button's background color, the value proposition color, and the color of the images inside the payment button. If the sent property is empty, the screen will show the default design. 

In the following code example, you will find the `customization` object, where you should complete the optional configurations of type `string`. Find the parameter details in the table we show below.

[[[
```javascript
const settings = {
  ...,
  customization: {
  theme:'dark',
  valueProp: 'practicality',
  customStyle: {
  valuePropColor: 'black',
  buttonHeight: '48px',
  borderRadius: '10px',
  verticalPadding: '10px',
  horizontalPadding: '10px',
  }
  }
}

```
```react-jsx
const customization = {
  theme:'dark',
  valueProp: 'practicality',
  customStyle: {
  valuePropColor: 'black',
  buttonHeight: '48px',
  borderRadius: '10px',
  verticalPadding: '10px',
  horizontalPadding: '10px',
  }
};
```
]]]

| Element | Type | Description | Available options |
| :---- | :---- | :---- | :---- |
| `theme` | String | Defines the visual customization theme, determining the light or dark style. | `default` or `black`. Default is `default` |
| `valueProp` | String | Specifies a value or characteristic represented in the style context, which can be interpretive. | 'practicality' |
| `customStyle` | Object | Contains specific customizable style configurations, such as colors, dimensions, and spacing. | |
| `valuePropColor` | String | Indicates the color associated with the valueProp value, used for the presentation style. | If the theme is default, valuePropColor can be blue or white. If the theme is dark, valuePropColor can be black. For the default theme, default is blue, while for the dark theme, default is black. |
| `buttonHeight` | String | Defines the height of the button or other element, determining its vertical size. | Minimum: 48px. Maximum: N/A Default is 48px. |
| `borderRadius` | String | Defines the border radius, determining how curved the corners of the styled elements are. | Minimum: N/A Maximum: N/A Default is 6px |
| `verticalPadding` | String | Specifies the vertical space (padding) (top and bottom) within an element. | Minimum: 8px. Maximum: N/A. Default is 8px. |
| `horizontalPadding` | String | Specifies the horizontal space (padding) (left and right) within an element. | Minimum: 0px. Maximum: N/A. Default is 0x |

## Change the button's value proposition

You can modify the value proposition that is displayed below the button and customize it with the message that best fits your store's needs. To do this, replace the string of the `valueProp` parameter.

![wallet-actioncomplement](cow/wallet-actioncomplement-en-v1.png)

In the following example, we share the `customization` object where the `valueProp` string is included, with which you can customize the value proposition. If no value is specified, the text `security_safety` will be displayed by default.
Below, in the table, review all possible texts for the value proposition content.

[[[
```javascript
const settings = {
  ...,
  customization: {
  theme: 'default',
  customStyle: {
  valueProp: 'practicality',
  }
  }
}
```

```react-jsx
const customization = {
  theme: 'default',
  customStyle: {
  valueProp: 'practicality',
  }
};
```
]]]

| Option | Value proposition | Observation |
| --- | --- | --- |
| `practicality` | **Use saved cards or money in account** | - |
| `security_details` | **All your data protected** | - |
| `security_safety` | **Pay securely** | Default value proposition |
| `payment_methods_logos` | _Available payment method logos_ | The logos of available payment methods configured in the payment preference will be displayed. In case the preference has only one valid payment method, it will stop showing images and show the text: "**With available money**". |

### Hide the value proposition

You can **hide** the value proposition text by configuring the _boolean_ `hideValieProp` as `true`. The default value is `false`, so by default a value proposition will always be displayed.

[[[
```javascript
const settings = {
  ...,
  customization: {
	 theme: 'default',
  customStyle: {
  hideValueProp: true,
  }
  }
}
```
```react-jsx
const settings = {
  ...,
  customization: {
	 theme: 'default',
  customStyle: {
  hideValueProp: true,
  }
  }
}
```
]]]

## Auxiliary callbacks

You can use auxiliary callbacks, which are functions that are automatically executed at specific moments during the payment flow, to offer more transparency. Below, see an example of how to integrate them into your integration.

Below, see an example of how to integrate them into your integration and learn the details in the table.

[[[
```Javascript
mp.bricks().create("wallet", "wallet_container", {
  initialization: {
  preferenceId: "<PREFERENCE_ID>",
  redirectMode: "self",
  },
  callbacks: {
  onReady: () => {},
  onSubmit: () => {},
  onError: (error) => console.error(error),
  },
});
```
```react-jsx
<Wallet
  initialization={{ preferenceId: '<PREFERENCE_ID>', redirectMode: 'self' }}
  onReady={() => {}}
  onError={() => {}}
  onSubmit={() => {}}
/>
```
]]]

| Callback | Description | When to use |
| --- |--- | --- | 
| `onReady` | Callback called when the button is completely loaded. | Serves to hide loading times from your site, for example. |
| `onSubmit` | Callback called when clicking the button. | It is used to indicate to the user that the flow must be completed in another tab, for example. It can be used in redirect mode. |


# Credentials

Credentials are unique access keys that we use to identify an integration in your account. They are directly linked to the :toolTipComponent[application]{link="/developers/en/docs/your-integrations/application-details" linkText="Application details" content="Entity registered in Mercado Pago that acts as an identifier to manage your integrations. For more information, access the link below."} you created for that integration and will allow you to develop your project with the best Mercado Pago security measures.

## Types of credentials

Credentials are divided into two types: **test credentials** and **production credentials**. Below, we explain what they are about.

:::::TabsComponent

::::TabComponent{title="Test credentials"}
### Test credentials

Test credentials are a set of keys that are used both in the development stage, to ensure secure settings, and in the testing stage, to test the integration.

During the integration process, use **test credentials** to perform all necessary configurations and validations, ensuring that no real payments are made in production. These credentials simulate the information of a production account, but in a secure testing environment. Keep using test credentials throughout the entire development phase. Only change them to production credentials when the system is completely validated and ready to be published.

> NOTE
>
> If you are developing for someone else, they will need to request access to the credentials of applications you do not manage. See the **Share credentials** section for more information.

When you create an application, the test credentials will be generated automatically. If this does not happen, simply click on **Activate credentials** in the data of the respective application or as indicated below.

1. In [Your integrations](/developers/panel/app), select your application. Then, go to the **Tests** section and click on **Test Credentials** in the menu on the left side of the screen.
2. Accept the [Privacy Statement](https://www.mercadopago[FAKER][URL][DOMAIN]/privacidad) and the [Terms and Conditions](/developers/es/docs/resources/legal/terms-and-conditions). Fill in the reCAPTCHA and click on **Activate credentials**.

![activate test credentials](/images/snippets/credentials/activate-credetials-tests-EN.png)

When accessing the test credentials, the **Public Key and Access Token** credential pair will be displayed.

### Public Key and Access Token

The test **Public Key** and **Access Token** credentials are used in the same way as production credentials, but will not allow any real transactions to be made. In some integrations, they will be required during the development stage to simulate transactions and verify that your integration works correctly.

> WARNING
>
> The prefix of the test Access Token may vary depending on the solution you are integrating. Check the specific documentation for each one to ensure the correct credential is used.

| Type | Description |
|---|---|
| Public Key | The application's public key is generally used in the frontend. It allows, for example, access to information about payment methods and encrypt card data. |
| Access Token | Application's private key that should always be used in the backend to generate payments. It is essential to keep this information safe on your servers. |

::::
::::TabComponent{title="Production credentials"}
### Production credentials

**Production credentials** are a set of keys that allow you to receive real payments in stores and other applications. To obtain production credentials, you must **activate them** by completing some information about your business. Follow the steps below:

1. Go to [Your integrations](https://www.mercadopago[FAKER][URL][DOMAIN]/developers/panel/app) and select an application.
2. Go to the **Production** section in the left side menu and click on **Production credentials** in the menu on the left side of the screen.
3. Accept the [Privacy Statement](https://www.mercadopago[FAKER][URL][DOMAIN]/privacidad) and the [Terms and Conditions](/developers/en/docs/resources/legal/terms-and-conditions). Fill in the reCAPTCHA and click on **Activate credentials**.

When accessing production credentials, the following credential pairs will be displayed: **Public Key and Access Token**, as well as **Client ID and Client Secret**.

### Public Key and Access Token
The **Public Key** and **Access Token** credentials are used, not necessarily together, in integrations made with Mercado Pago payment solutions. They are directly linked to the :toolTipComponent[application]{link="/developers/en/docs/your-integrations/application-details" linkText="Application details" content="Entity registered in Mercado Pago that acts as an identifier to manage your integrations. For more information, access the link below."} you created, so each credential pair is unique for each integration.

| Type | Description |
|---|---|
| Public Key | The application's public key is generally used in the frontend. It allows, for example, access to information about payment methods and encrypt card data. |
| Access Token | Application's private key that should always be used in the backend to generate payments. It is essential to keep this information safe on your servers. |

For more information on which credentials will be needed for your integration, see the [documentation](https://www.mercadopago[FAKER][URL][DOMAIN]/developers/es/docs) of the solution being integrated.

### Client ID and Client Secret

The **Client ID** and **Client Secret** credentials are used primarily in integrations that use [OAuth](/developers/en/docs/security/oauth) as a protocol for obtaining private information from Mercado Pago accounts. In particular, they are used during the **Client Credentials** flow (_grant type_), which allows you to access a resource on your own behalf and obtain an Access Token without user interaction.

They may also be required in some older integrations with e-commerce platforms.

| Type | Description |
|---|---|
| Client ID | Unique identifier that represents your integration. |
| Client Secret | Private key used in some plugins to generate payments. It is extremely important to keep this information secure on your servers and not allow access to any user of the system or intruder. | 

::::

:::::

## Share credentials

If you are developing for someone else or receiving help in the integration or configuration of your stores, you can securely share the credentials with another Mercado Pago account.

You can share credentials **up to a maximum of 10 times**. If you reach this limit, you must delete old permissions, without impacting already configured integrations.

In addition, if for security reasons you no longer want to share your credentials, you can cancel access.

Below, we show you how to share credentials.

1. In the upper right corner of [Mercado Pago Developers](https://www.mercadopago[FAKER][URL][DOMAIN]/developers/panel/app), click **Log in** and enter the required data with the information corresponding to your Mercado Pago account. Then, click on the **Your integrations** button located in the upper right corner.
2. Access the application of the integration for which you need to share the credentials.
3. Go to the **Testing** or **Production** section, depending on the type of credential you want to share. Remember that to access production credentials, you must activate them. If you don't know how to activate them, go to [Activate production credentials](/developers/en/docs/credentials#bookmark_activate_production_credentials).
4. Once you select the credentials, go to the *Share credentials with a developer* section and click on the **Share Credentials** button.
5. Enter the email address of the person you want to grant access to. **Remember**: it is mandatory that the email address is associated with a Mercado Pago account.

![Compartir credenciales en Tus Integraciones](/images/snippets/share-credentials-panel-es-v1.jpg)

## Renew credentials

You can renew your **production credentials** for security reasons or any other relevant reason.

> WARNING
>
> Renewing credentials already configured in an integration will affect its operation. It is necessary that **you replace the old credentials with the ones obtained** after the renewal process to continue operating.

To renew a credential pair, follow the steps below.

1. Access your production credentials through [Your integrations](https://www.mercadopago[FAKER][URL][DOMAIN]/developers/panel/app).
2. Select the credential pair you want to renew. These can be **Public Key** and **Access Token** or **Client ID** and **Client Secret**. Keep in mind that both credentials in the pair you choose will be renewed.
3. Click on the three dots located to the right of the credential you want to renew and select **Renew**. Click on **Renew now** to confirm the change.

![Cómo renovar tus credenciales](/images/snippets/renew-credentials-es-v1.jpg)

Done, your credentials have been renewed.

## Security Recommendations

When integrating Mercado Pago solutions, you will handle sensitive data that you must protect from potential losses or vulnerabilities, such as your Mercado Pago access credentials, the keys you use in your integrations, or your customers' information.

We will show you how you can optimize the security of your integrations in a simple and quick way.

### Send the Access Token by header

Every time you make API calls, send the **Access Token** via _header_ instead of _query param_. This will allow you to protect it so that it is not exposed to anyone outside your integration.

For example, if you perform a **GET** request to the `/users/me` resource, it would be like this:

```curl
curl -H 'Authorization: Bearer {{YOUR_ACCESS_TOKEN}}' \
https://api.mercadolibre.com/users/me
```

### Use OAuth to manage third-party credentials

OAuth is an authorization protocol that allows applications to securely access user accounts in HTTP services without requiring the user to directly share their credentials. It works as an intermediary that facilitates controlled access to user data by third-party applications.

For more information, access the [documentation](/developers/en/docs/security/oauth).


# Integration data

To access the general data of your integration, navigate to the [Developer Dashboard](/developers/panel/app) and click on the card of an application to access its data and find all useful resources and information. See below which information will be displayed on the screen.

![Datos de integración](/images/cow/integration-data-pro-es-v1.png)

:::AccordionComponent{title="Credenciales"}

This section displays the :toolTipComponent[credentials]{link="/developers/en/docs/checkout-pro/additional-content/credentials" linkText="Credenciais" content="Unique access keys we use to identify an integration in your account, linked to your application. For more information, access the link below."} of your application, which are:

- **Test credentials**: a set of keys used both during the development stage, to ensure secure configurations, and during the testing stage, to test the integration. When you create an application, test credentials are generated automatically.
- **Production credentials**: a set of keys that allow you to receive real payments in stores and other applications. To obtain production credentials, you must **activate them** y clicking on **Activate credentials** and filling in some information about your business.

For more information, see the [Credentials](/developers/en/docs/checkout-pro/additional-content/credentials) documentation.

:::
:::AccordionComponent{title="Integration data"}

This section displays the basic data of the application, including:

  - **User ID**: automatically generated user identification number.
  - **Application number**: automatically generated application identification number.
  - **Integrated product**: the product or platform integrated with the application.
  - **Integration model** (if applicable): integration model options are available depending on the used product or platform.

### Edit data

In the menu on the left side of the screen, you can **click the edit button above your application's name** to edit the **basic and advanced settings** that include your application's data and the product to be integrated. They are:

#### Basic settings

* **Logo**: JPG or PNG image format up to 1MB.
* **Application name**: to easily identify your applications (maximum of 50 characters).
* **Application short name**: secondary identifier of the application (this field cannot contain spaces or special characters).
* **Application description** (maximum of 150 characters).
* **Industry**: choose the category that best describes your business.
* **Production website URL** (optional).
* **Payment solution to be integrated**: edit the payment solution to be integrated between **Online Ppyments** and **In-person payments**.
  - **Online payments**: if you are going to use an e-commerce platform, mark **Yes** and select the **platform** you will integrate with. Finally, choose the **product** you are integrating. If you are not using an e-commerce platform, mark **No** and select the **product** you are integrating. Optionally, you can select the integration model(s).
  - **API to be used in the integration**: indicate which API will be used for the integration, which can be either the Orders API or the Payments API.
  - **In-person payments**: select the **product** you are integrating. If you select the QR Code option, optionally you can also choose the integration model(s).

#### Advanced settings

* **Redirect URL**: URL (in https) where you want to receive the authorization code when your integration is set up as a marketplace or performed through the flow **Authorization code** by OAuth. **Make sure that is a static URL**. Check out [OAuth](/developers/en/docs/security/oauth) documentation for more details.
* **Use the authorization code flow with PKCE**: if the integration is done with the flow **Authorization code** by OAuth, you can enable PKCE (Proof Key for Code Exchange) to generate an additional secret code to be used during the authorization process. Check out [Configure PKCE](/developers/en/docs/security/oauth/creation#:~:text=Access%20Token.-,Configure%20PKCE,-The%20PKCE%20) documentation for more details.
* **Application permissions**: options for accessing your application, including **read**, **offline access** and **write**. By default, your application is created with all permissions enabled, but you can disable a permission by unchecking the corresponding checkbox.

### Delete application

To remove an application, follow these steps:

1. Access the "Edit Application" page.
2. Scroll to the bottom of the page and click on the **Delete Application** button.
This way, the application will be successfully deleted.

> WARNING
>
> Attention
>
> When deleting an application, please note that your store will lose the ability to receive payments through the integration associated with that application. Additionally, all settings, including associated credentials, will be lost. **Once an application is deleted, it cannot be recovered**.

:::
:::AccordionComponent{title="Integration quality"}

The [quality measurement](/developers/en/docs/integration-quality) is the final stage of the integration process, where you can validate whether it meets the necessary quality and security requirements to provide the best experience for both sellers and buyers.

There are two ways to measure the quality of your integration:
 * **Manual:** you can conduct the measurement on your own whenever you prefer. You only need a `payment ID` from a payment made with production credentials and access **“Integration Quality"** in the side menu, where you can find the step-by-step instructions.

 * **Automatic:** From the 1st to the 7th of each month, Mercado Pago conducts a periodic quality measurement for all integrations with **Checkout Pro** that have a payment made with production credentials.

As a result of this measurement, you will receive a score indicating how secure and aligned your application's configuration is with Mercado Pago's best integration practices, along with necessary recommendations for adjustments if needed.

For more details, refer to the documentation on [integration quality](/developers/en/docs/integration-quality).

:::
:::AccordionComponent{title="Notifications"}

If you have already [set up your Webhook notifications](/developers/en/docs/checkout-pro/payment-notifications), this section will display the percentage of notifications successfully delivered for the integration in question.

:::

# Test accounts

Use test accounts to ensure that your integration supports all possible flows and scenarios. They have the same features as a real Mercado Pago account, which allows you to test the functioning of the integrations you are developing.

For integrations with [Checkout Pro](/developers/en/docs/checkout-pro/overview), the **seller** test account **is automatically created** after the application is created and its credentials become your **test credentials**. This is why your test Access Token starts with the prefix `APP_USR`.

If you need to create or add more test accounts manually, follow the steps below. You can generate **up to 15 test user accounts** simultaneously, and for now, it is not possible to delete them.

To perform the test, you must have at least two accounts:

* **Seller**: account required to **configure application and credentials**. This is your user account.
* **Buyer**: account required to **test the purchase process**.
* **Integrator**: account used in **marketplace model integrations**.

In addition to these accounts, it is also important to use [test cards](/developers/en/docs/checkout-pro/test-cards) to test payment integration and simulate the purchase process, as well as **balance in the test user's Mercado Pago account**. See more details below.

![create test user](/images/snippets/test-cross/test-user-es-create-seller-v1.png)

To create accounts and test how the integrations work, follow the steps below.

1. On the [Devsite](/developers/en/docs), navigate to **[Your integrations](/developers/panel/app)** and click on the card corresponding to your application.
2. On the application page, go to the **Test accounts** section and click the **+ Create test account** button.
3. In the "Create new account" screen, select the **operating country** for the account. This information **cannot be edited later**, and furthermore, the Buyer and Seller users need to be from the same country.
4. Then, enter a description to identify the account. For example: "Seller - Store 1".
5. Next, select the type of account you want to create. This can be **Seller**, **Buyer** or **Integrator**.
6. If the test account requires it, enter a **fictional money value** that will serve as a reference for testing your applications. This value will appear as the balance in the Mercado Pago account of the test user and can be used for payment simulation, just like with the [test cards](/developers/en/docs/checkout-pro/test-cards).
7. Authorize the use of your personal data in accordance with the [Privacy Statement](https://www.mercadopago[FAKER][URL][DOMAIN]/privacidad) and ensure that your account uses Mercado Pago's tools in accordance with the [Terms and Conditions](https://www.mercadopago.com.br/developers/en/docs/resources/legal/terms-and-conditions) by checking the checkbox.
8. Click on **Create test account**.

Done! The test account has been created and will be displayed in the table with the information below.

![access test user](/images/snippets/test-cross/test-user-es-list-full-v1.png)

* **Country**: Origin location of the account selected in your registration.
* **User ID**: User identification number, which is created automatically.
* **User**: Automatically generated username of the test account. This is the username used to log in with the test user.
* **Password**: Automatically generated password to access the test user account. To generate a new password, click on the vertical ellipsis (three dots) at the end of the table row and select the **Generate new password** option.
* **Code**: 6-digit number that you must enter in case email verification is requested when logging in with the test account.

> NOTE
>
> To edit the **account identification** or **add more fictional money** to test your applications, click on the **vertical ellipsis** (three dots) at the end of the table row and select the **Edit data** option.

## Validate login with test accounts

If an email authentication is requested when logging in with test accounts, enter the **6 digits code** of that test account. You can find it in **[Your integrations](/developers/panel/app) > *Your application* > Test accounts**.

Please note that when you log in with a test account, you will not have access to certain sections within the Developer Dashboard, such as Test Credentials or Integration Quality. These are sections that are not only not necessary for this type of accounts, but can also interfere with their proper and desired use.


# Chargeback management

A chargeback occurs when a customer contests a charge made to their credit or debit card, requesting a refund from the bank. If the chargeback request is deemed valid after due evaluation, the charge is canceled, the funds are withdrawn from the seller, and returned to the customer.

At Mercado Pago, chargeback management is carried out in two main steps, ensuring both the analysis and resolution of disputes between the store and the customer. These steps are:

1. **Chargeback notifications**:
Configure chargeback notifications to receive alerts whenever a customer initiates a dispute. For more details, refer to the documentation [Configure chargeback notifications](/developers/en/docs/checkout-pro/chargebacks/notifications).

2. **Chargeback processing**:
After notification, if requested, it will be necessary to gather information and submit documentation through the Mercado Pago API. For more information, refer to the [Chargeback management documentation](/developers/en/docs/checkout-pro/chargebacks/manage).

> RED_MESSAGE
>
> During the chargeback resolution period, the disputed amount remains on hold in the seller's account until the process is completed.

Below, we present some of the most common reasons for chargebacks and how to prevent them:

| Reason | Description | How to prevent |
|-|-|-|
| Legitimate Fraud | Legitimate fraud constitutes a large part of chargebacks. In these cases, the customer may open a dispute with the card provider to cancel transactions on their accounts due to fraudulent activities. | Ensure to provide complete information when creating a payment so that the fraud prevention system can block high-risk transactions. For more information, refer to the [Industry data documentation](/developers/en/docs/checkout-pro/additional-settings/industry-data). We also recommend configuring and activating Webhooks notifications for the fraud alert topic to receive warnings of irregular behaviors. For more information, visit the [Webhooks documentation](/developers/en/docs/checkout-pro/additional-content/notifications). If you receive a fraud alert, we recommend [canceling the purchase](/developers/en/docs/checkout-pro/additional-settings/refunds-and-cancellations) and refunding the money to the buyer to avoid the chargeback. |
| Customer does not recognize the charge | The customer does not recognize the transaction because they do not remember making a specific purchase or because the store name is unclear on the statement. | Send detailed purchase confirmation emails that include the payment receipt and use a clear and recognizable name to be displayed on the customer's statement. To learn how to configure the establishment name to be displayed on the buyer's invoice, refer to the documentation [Configure invoice description](/developers/en/docs/checkout-pro/additional-settings/preferences/invoice-description). |
| Delivery issues | The customer may choose to request a chargeback in case of undelivered or late-delivered items before seeking more information from the store. | Provide tracking information and proactive communication about the order status. |
| Billing errors | Errors such as duplicate charges or subscriptions not canceled correctly. | Maintain an accurate billing system and offer accessible and efficient customer support. |


# Configure chargeback notifications

Webhook notifications (also known as web callbacks) are a simple method that allows an application or system to provide real-time information whenever an event occurs. It is a passive way of receiving data between two systems through an `HTTP POST` request.

Once configured, these notifications will be sent whenever a chargeback is created or its status is modified. From the received information, it will be possible to manage the chargeback.

Below, we present a step-by-step guide to perform the configuration.

1. Access [Your integrations](/developers/panel/app) and select the application for which you want to activate chargeback notifications.

![Application](/images/cow/not1-select-app-es-v1.png)

2. In the left menu, select **Webhooks > Configure Notifications**.

![Webhooks](/images/cow/not2-webhooks-es-v1.png) 

3. Configure the productive HTTPS URL that will be used to receive notifications.

![URL](/images/cow/not3-url-es-v1.png) 

4. In recommended events, select the **Chargebacks** event to receive notifications, which will be sent in `JSON` format via an `HTTPS POST` to the specified URL.

![Chargebacks](/images/cow/not4-url-es-v1.png) 

5. Finally, click **Save Settings**. This will generate a unique secret key for the application, which will allow you to validate the authenticity of the received notifications, ensuring that they have been sent by Mercado Pago. For more details, refer to the [Webhook Notifications Documentation](/developers/en/docs/checkout-pro/additional-content/notifications/webhooks).

**Notification example**:

The notifications sent by Mercado Pago for the `chargebacks` topic will be similar to the following example:

```
{
  "actions":[
  "changed_case_status",
  ],
  "api_version":"v1",
  "application_id":9007201037432480,
  "data":{
  "checkout":"PRO",
  "date_updated":"0001-01-01T00:00:00Z",
  "id":233000061680860000,
  "payment_id":81968653106,
  "product_id":"C00A2J8RF4DI8BCIMFU0",
  "site_id":"MLA",
  "transaction_intent_id":""
  },
  "date_created":"2024-07-03T19:34:28-04:00",
  "id":114411153595,
  "live_mode":true,
  "type":"topic_chargebacks_wh",
  "user_id":634060442,
  "version":1720035618
}
```

These notifications provide complete information about the process initiated by the customer, being essential to [manage the chargeback](/developers/en/docs/checkout-pro/chargebacks/manage).


# Manage chargebacks

Upon receiving a chargeback initiation notification, use the provided data to assist in managing the process. This data will be essential for preparing and submitting the necessary documentation for the dispute.

In this stage, analyze the detailed information included in the notification to understand the specific aspects of the chargeback. Below, we present a diagram that illustrates how the document submission and receipt flow works:

![Chargebacks](/images/cow/chargebacks-flow-v1.png) 

## Consult chargeback

Start the process by consulting the chargeback information using the `id` or `payment_id` provided in the notification body. From the obtained details, it will be possible to evaluate if there is a need to submit documentation to continue the chargeback.

:::::TabsComponent

::::TabComponent{title="Consult chargeback by id"}

To consult more information about the chargeback, send a GET request to the endpoint [/v1/chargebacks/{id}](/developers/en/reference/online-payments/checkout-pro/chargebacks/get), replacing the `id` field with the `id` of the chargeback brought in the notification body:

```
curl --location --globoff 'https://api.mercadopago.com/v1/chargebacks/{id}' \
--header 'Content-Type: application/json' \
--header 'Authorization: Bearer {{access_token}}'
```

Below is an example of a response to the request:

```
{
  "id": "234000062890459000",
  "payments": [
  86439942806
  ],
  "currency": "ARS",
  "amount": 1000.50,
  "reason": "general",
  "coverage_applied": null,
  "coverage_elegible": true,
  "documentation_required": false,
  "documentation_status": "not_supplied",
  "documentation": [],
  "date_documentation_deadline": null,
  "date_created": null,
  "date_last_updated": "2024-10-17T12:48:24.000-04:00",
  "live_mode": true
}
```
::::

::::TabComponent{title="Consult chargeback by payment_id"}
To consult more information about the chargeback, execute a GET request to the endpoint [/v1/chargebacks/{id}](/developers/en/reference/online-payments/checkout-pro/chargebacks/get), replacing the `payment_id` field with the `payment_id` of the chargeback brought in the notification body:

```
curl --location 'https://api.mercadopago.com/v1/chargebacks/search?payment_id={payment_id}' \
--header 'Content-Type: application/json' \
--header 'Authorization: Bearer {{access_token}}'
```

Below is an example of a response to the request:

```
{
  "paging": {
  "offset": 0,
  "limit": 25,
  "total": 1
  },
  "results": [
  {
  "id": "234000062890459000",
  "payments": [
  86439942806
  ],
  "currency": "ARS",
  "amount": 1000.5,
  "reason": "general",
  "coverage_applied": null,
  "coverage_elegible": true,
  "documentation_required": false,
  "documentation_status": "not_supplied",
  "documentation": [],
  "date_documentation_deadline": null,
  "date_created": null,
  "date_last_updated": "2024-10-17T12:48:24.000-04:00",
  "live_mode": true
  }
  ]
}
```
::::

:::::

## Submit documentation for chargeback

In the response to the query made to obtain more information about the chargeback, it will be indicated if you need to submit the necessary documentation to dispute it. You will only need to do so if the `documentation_required` field is true and the `date_documentation_deadline` field indicates a future date.

At this stage, you can submit the documentation proving that the sale is valid through the following POST request:

> RED_MESSAGE
>
> The files must be sent in .jpg, .png, or .pdf format and have a maximum size of up to 10MB.

```
curl -X POST \
-F 'files[]=@/path/to/file/file1.png' \
-F 'files[]=@/path/to/file/file2.pdf' \
-H 'Authorization: Bearer {{access_token}}'
https://api.mercadopago.com/v1/chargebacks/{id}/documentation
```

If the files are successfully submitted, the API will return an `HTTP 200` code and the `documentation_status` of the chargeback will be changed to `review_pending`.

After receiving the documentation, Mercado Pago acts as a mediator in the chargeback resolution process. The analysis is initiated with the card brand, which then sends the received documentation to the card-issuing bank. Once the bank's analysis is completed, the chargeback resolution is determined and the involved parties are notified.

Wait for the Webhook notification regarding the resolution and check the chargeback again using the endpoint [Get Chargeback](/developers/en/reference/online-payments/checkout-pro/chargebacks/get). After the resolution, the `coverage_applied` field will indicate the result and will assume one of the possible values:

| Value | Description |
|-------|---------------------------------------------------------------------------|
| `true` | Indicates that the decision was in favor of the seller and the money will be refunded. |
| `false` | Indicates that the decision was against the seller and the money will be deducted. |

> RED_MESSAGE
>
> The chargeback resolution can take up to 6 months, depending on the card brand.

## Payment status

When a chargeback is initiated, the status of the associated payment is directly impacted. Initially, the `status` is changed to `charged_back` and the `status_detail` to `in_process`. After the conclusion of the chargeback analysis, whether by the decision of the issuing bank, the determination of eligibility for coverage by Mercado Pago, or the absence of provided documentation, the `status_detail` of the payment will be updated to `settled` or `reimbursed`.

| Status | Status detail | Description |
|------------------|---------------|--------------------------------------------------------------------------------------------------|
| `charged_back` | `in_process` | Chargeback received. The payment dispute is in progress, awaiting a final decision. |
| `charged_back` | `settled` | Decision against the seller. Money withdrawn from the seller's account. |
| `charged_back` | `reimbursed` | Decision in favor of the seller. Money refunded to the seller's account. |


# Security

At Mercado Pago, we have implemented a series of security measures designed to protect customer and user payments, ensure confidentiality and integrity in all processes, and provide greater security in the integrations that our payment solutions offer.

Next, we present the protocols used by Mercado Pago.

## OAuth

OAuth (Open Authorization) is an authorization protocol that allows applications to gain limited access to user accounts on an HTTP service, such as social networks, without the user having to share their credentials. Instead, OAuth defines a method for users to grant third-party applications access to their data without needing to reveal their login information.

For more information, access the [documentation](/developers/en/docs/security/oauth).

## OWASP

OWASP (Open Web Application Security Project) is an open and secure community that provides tools and standards for the development and maintenance of web applications. It aims to promote the research and development of security in applications. Through its initiatives, OWASP contributes to raising the security standard in the software industry and creating a safer online community.

For more information, access the [documentation](/developers/es/docs/security/owasp).

## PCI DSS

PCI DSS (Payment Card Industry Data Security Standard) is an international security standard that all entities storing, processing, or transmitting card data must comply with. It is one of the most demanding security standards in the payment industry, which Mercado Pago adheres to, allowing it to operate with credit and debit cards.

For more information, access the [documentation](/developers/en/docs/security/pci).


# Credentials

Credentials are unique access keys that we use to identify an integration in your account. They are directly linked to the :toolTipComponent[application]{link="/developers/en/docs/your-integrations/application-details" linkText="Application details" content="Entity registered in Mercado Pago that acts as an identifier to manage your integrations. For more information, access the link below."} you created for that integration and will allow you to develop your project with the best Mercado Pago security measures.

## Types of credentials

Credentials are divided into two types: **test credentials** and **production credentials**. Below, we explain what they are about.

:::::TabsComponent

::::TabComponent{title="Test credentials"}
### Test credentials

Test credentials are a set of keys that are used both in the development stage, to ensure secure settings, and in the testing stage, to test the integration.

During the integration process, use **test credentials** to perform all necessary configurations and validations, ensuring that no real payments are made in production. These credentials simulate the information of a production account, but in a secure testing environment. Keep using test credentials throughout the entire development phase. Only change them to production credentials when the system is completely validated and ready to be published.

> NOTE
>
> If you are developing for someone else, they will need to request access to the credentials of applications you do not manage. See the **Share credentials** section for more information.

When you create an application, the test credentials will be generated automatically. If this does not happen, simply click on **Activate credentials** in the data of the respective application or as indicated below.

1. In [Your integrations](/developers/panel/app), select your application. Then, go to the **Tests** section and click on **Test Credentials** in the menu on the left side of the screen.
2. Accept the [Privacy Statement](https://www.mercadopago[FAKER][URL][DOMAIN]/privacidad) and the [Terms and Conditions](/developers/es/docs/resources/legal/terms-and-conditions). Fill in the reCAPTCHA and click on **Activate credentials**.

![activate test credentials](/images/snippets/credentials/activate-credetials-tests-EN.png)

When accessing the test credentials, the **Public Key and Access Token** credential pair will be displayed.

### Public Key and Access Token

The test **Public Key** and **Access Token** credentials are used in the same way as production credentials, but will not allow any real transactions to be made. In some integrations, they will be required during the development stage to simulate transactions and verify that your integration works correctly.

> WARNING
>
> The prefix of the test Access Token may vary depending on the solution you are integrating. Check the specific documentation for each one to ensure the correct credential is used.

| Type | Description |
|---|---|
| Public Key | The application's public key is generally used in the frontend. It allows, for example, access to information about payment methods and encrypt card data. |
| Access Token | Application's private key that should always be used in the backend to generate payments. It is essential to keep this information safe on your servers. |

::::
::::TabComponent{title="Production credentials"}
### Production credentials

**Production credentials** are a set of keys that allow you to receive real payments in stores and other applications. To obtain production credentials, you must **activate them** by completing some information about your business. Follow the steps below:

1. Go to [Your integrations](https://www.mercadopago[FAKER][URL][DOMAIN]/developers/panel/app) and select an application.
2. Go to the **Production** section in the left side menu and click on **Production credentials** in the menu on the left side of the screen.
3. Accept the [Privacy Statement](https://www.mercadopago[FAKER][URL][DOMAIN]/privacidad) and the [Terms and Conditions](/developers/en/docs/resources/legal/terms-and-conditions). Fill in the reCAPTCHA and click on **Activate credentials**.

When accessing production credentials, the following credential pairs will be displayed: **Public Key and Access Token**, as well as **Client ID and Client Secret**.

### Public Key and Access Token
The **Public Key** and **Access Token** credentials are used, not necessarily together, in integrations made with Mercado Pago payment solutions. They are directly linked to the :toolTipComponent[application]{link="/developers/en/docs/your-integrations/application-details" linkText="Application details" content="Entity registered in Mercado Pago that acts as an identifier to manage your integrations. For more information, access the link below."} you created, so each credential pair is unique for each integration.

| Type | Description |
|---|---|
| Public Key | The application's public key is generally used in the frontend. It allows, for example, access to information about payment methods and encrypt card data. |
| Access Token | Application's private key that should always be used in the backend to generate payments. It is essential to keep this information safe on your servers. |

For more information on which credentials will be needed for your integration, see the [documentation](https://www.mercadopago[FAKER][URL][DOMAIN]/developers/es/docs) of the solution being integrated.

### Client ID and Client Secret

The **Client ID** and **Client Secret** credentials are used primarily in integrations that use [OAuth](/developers/en/docs/security/oauth) as a protocol for obtaining private information from Mercado Pago accounts. In particular, they are used during the **Client Credentials** flow (_grant type_), which allows you to access a resource on your own behalf and obtain an Access Token without user interaction.

They may also be required in some older integrations with e-commerce platforms.

| Type | Description |
|---|---|
| Client ID | Unique identifier that represents your integration. |
| Client Secret | Private key used in some plugins to generate payments. It is extremely important to keep this information secure on your servers and not allow access to any user of the system or intruder. | 

::::

:::::

## Share credentials

If you are developing for someone else or receiving help in the integration or configuration of your stores, you can securely share the credentials with another Mercado Pago account.

You can share credentials **up to a maximum of 10 times**. If you reach this limit, you must delete old permissions, without impacting already configured integrations.

In addition, if for security reasons you no longer want to share your credentials, you can cancel access.

Below, we show you how to share credentials.

1. In the upper right corner of [Mercado Pago Developers](https://www.mercadopago[FAKER][URL][DOMAIN]/developers/panel/app), click **Log in** and enter the required data with the information corresponding to your Mercado Pago account. Then, click on the **Your integrations** button located in the upper right corner.
2. Access the application of the integration for which you need to share the credentials.
3. Go to the **Testing** or **Production** section, depending on the type of credential you want to share. Remember that to access production credentials, you must activate them. If you don't know how to activate them, go to [Activate production credentials](/developers/en/docs/credentials#bookmark_activate_production_credentials).
4. Once you select the credentials, go to the *Share credentials with a developer* section and click on the **Share Credentials** button.
5. Enter the email address of the person you want to grant access to. **Remember**: it is mandatory that the email address is associated with a Mercado Pago account.

![Compartir credenciales en Tus Integraciones](/images/snippets/share-credentials-panel-es-v1.jpg)

## Renew credentials

You can renew your **production credentials** for security reasons or any other relevant reason.

> WARNING
>
> Renewing credentials already configured in an integration will affect its operation. It is necessary that **you replace the old credentials with the ones obtained** after the renewal process to continue operating.

To renew a credential pair, follow the steps below.

1. Access your production credentials through [Your integrations](https://www.mercadopago[FAKER][URL][DOMAIN]/developers/panel/app).
2. Select the credential pair you want to renew. These can be **Public Key** and **Access Token** or **Client ID** and **Client Secret**. Keep in mind that both credentials in the pair you choose will be renewed.
3. Click on the three dots located to the right of the credential you want to renew and select **Renew**. Click on **Renew now** to confirm the change.

![Cómo renovar tus credenciales](/images/snippets/renew-credentials-es-v1.jpg)

Done, your credentials have been renewed.

## Security Recommendations

When integrating Mercado Pago solutions, you will handle sensitive data that you must protect from potential losses or vulnerabilities, such as your Mercado Pago access credentials, the keys you use in your integrations, or your customers' information.

We will show you how you can optimize the security of your integrations in a simple and quick way.

### Send the Access Token by header

Every time you make API calls, send the **Access Token** via _header_ instead of _query param_. This will allow you to protect it so that it is not exposed to anyone outside your integration.

For example, if you perform a **GET** request to the `/users/me` resource, it would be like this:

```curl
curl -H 'Authorization: Bearer {{YOUR_ACCESS_TOKEN}}' \
https://api.mercadolibre.com/users/me
```

### Use OAuth to manage third-party credentials

OAuth is an authorization protocol that allows applications to securely access user accounts in HTTP services without requiring the user to directly share their credentials. It works as an intermediary that facilitates controlled access to user data by third-party applications.

For more information, access the [documentation](/developers/en/docs/security/oauth).