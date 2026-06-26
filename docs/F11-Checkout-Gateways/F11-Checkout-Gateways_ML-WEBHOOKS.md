---
layout: default
title: F11-Checkout-Gateways ML-WEBHOOKS
---

# Your integrations

Your Integrations is your integration management environment automatically created with a user ID (the Mercado Pago ID) when you open an account on Mercado Pago. In it, you can create a new application in the [Developer Dashboard](/developers/panel/app) or access the [Application details](/developers/en/guides/additional-content/your-integrations/application-details) page for each listed application, as well as request access to credentials for an application you don't manage.

> WARNING
> 
> Important
>
> For security reasons related to Mercado Pago, the environment **"Your integrations" is not available for users under the age of majority**.

## Application details

The [Application details](/developers/en/guides/additional-content/your-integrations/application-details) page consists of different sections, each with a different purpose.
* **General Information**: displays general information about the application.
* **Testing**: test the integration's functionality, perform tests, and simulate different transactions with [Credentials](/developers/en/guides/additional-content/your-integrations/credentials), [Test accounts](/developers/en/guides/additional-content/your-integrations/test-accounts), and [Test cards](/developers/en/guides/additional-content/your-integrations/test-cards).
* **Notifications**: configure the application to receive notifications for transaction-related events, such as payment alerts, fraud notifications, disputes, etc. There are two types of notifications available for configuration:
  1. [Webhooks](/developers/en/guides/additional-content/your-integrations/webhooks)
  2. [IPN](/developers/en/guides/additional-content/your-integrations/ipn)
* **Production**: activate **Production Credentials** to start receiving payments in your online store and other applications.
* **Evaluation**: validate the [quality of your integration](/developers/en/guides/additional-content/homologator/homologator) to ensure that your development meets the necessary quality and security requirements to provide both the seller and the buyer with the best experience with Mercado Pago.


# Developer dashboard

In the [Developer dashboard](/developers/panel/app), you can find the listing of your applications.

Applications are different integrations contained within one or more stores. You can create an application for each solution you implement in order to keep everything organized and have better management control.

Each application has a set of credentials and the possibility to configure its own notifications. Each card represents a created application and displays the application name and number, along with a button that directs you to the **Application Details** where you can manage it.

## Create a new application

Create your application and obtain your credentials to integrate with Mercado Pago. Follow the steps below to create an application.

1. Click on **Your Integrations** in the top right corner of the screen.
2. Click on **Create application**.

> NOTE
>
> Important
>
> During the creation of your application, you may need to reauthenticate your identity. If you have already completed the verification process, you will be prompted to reauthenticate. If you have not yet completed the verification, you will be redirected to submit the necessary documents. 
>
> This additional authentication step is essential to protect your account and ensure compliance with operations. Follow the provided instructions to successfully create your application.

3. Enter a name to identify your application (limit of 50 characters).
4. Choose a payment solution to integrate, either **Online Payments** or **In-person Payments**.

  - **Online payments**: If you are going to use an e-commerce platform, mark **Yes**. Then, select the **platform** you will integrate with. Finally, choose the **product** you are integrating.

If you are not using an e-commerce platform, mark **No** and select the **product** you are integrating. Optionally, you can select the integration model(s).

  - **In-person Payments**: Select the **product** you are integrating. If you select the QR Code option, optionally you can also choose the integration model(s).

5. Check the checkbox to authorize the use of your personal data in accordance with the [Privacy Statement](https://www.mercadopago.com.br/privacidade) and certify that your account uses Mercado Pago tools in accordance with the [Terms and Conditions](/developers/en/docs/resources/legal/terms-and-conditions).
6. Check the **I'm not a robot** checkbox.
7. Click on **Create application**.

For each created application, a new card containing the name, number, and quality status of the application is automatically generated in the [Developer dashboard](/developers/panel/app).

> It is necessary that the application is registered with an integration of a product from those where the measuring tool is available. For now, the integration quality measuring tool is only available for integrations with [Checkout Pro,](/developers/en/docs/checkout-pro/landing) [Checkout API](/developers/en/docs/checkout-api-payments/overview), [Checkout Bricks](/developers/en/docs/checkout-bricks/landing) and [Mercado Pago Point](/developers/en/docs/mp-point/landing).

## Accessing credentials for an application you don't manage

You can request access to application credentials from other people and integrate solutions for accounts other than your own. To securely request access to credentials for an application you don't manage, follow the steps below:

1. In the [Developer dashboard](/developers/panel/app), click on the **Request access to credentials** button.
2. Click on the "Request credentials" button.
3. Enter the email associated with the account for which the credentials are being requested.
4. Check the "I'm not a robot" checkbox.
5. Click on **Request credentials**.

Once access to the credentials is granted, you can use them to integrate solutions. After the integrations are completed, remove the access permissions for the shared credentials and ensure the security of the data.

> When requesting access to other credentials, you are asking other Mercado Pago accounts to share the public and private keys of their applications with you for integrations. Do not use the credentials of other accounts without proper consent.


# Application details

To access the general data of your application, navigate to the [Developer Dashboard](/developers/panel/app) and click on the card of an application to access the **Application details**.

## Application data

This section displays the basic data of the application, including:
  - **User ID**: Automatically generated user identification number.
  - **Application number**: Automatically generated application identification number.
  - **Integration with**: The product or platform integrated with the application.
  - **Integration model** (if applicable): Integration model options are available depending on the used product or platform.

### Edit data

You can click on the **Edit data** button to view and edit the basic and advanced settings that include the data of your application and the product to be integrated. They are:

#### Basic settings

* **Logo**: JPG or PNG image format up to 1MB.
* **Application name**: To easily identify your applications (maximum of 50 characters).
* **Application short name**: secondary identifier of the application (this field cannot contain spaces or special characters).
* **Application description** (maximum of 150 characters).
* **Industry**: Choose the category that best describes your business.
* **Production website URL** (optional).
* **Payment Solution to be Integrated**: Edit the payment solution to be integrated between **Online Ppyments** and **In-person payments**.
  - **Online payments**: If you are going to use an e-commerce platform, mark **Yes**. Then, select the **platform** you will integrate with. Finally, choose the **product** you are integrating. If you are not using an e-commerce platform, mark **No** and select the **product** you are integrating. Optionally, you can select the integration model(s).
  - **In-person payments**: Select the **product** you are integrating. If you select the QR Code option, optionally you can also choose the integration model(s).

#### Advanced settings

* **Redirect URL**: URL (in https) where you want to receive the authorization code when your integration is set up as a marketplace or performed through the flow **Authorization code** by OAuth. **Make sure that is a static URL**. Check out [OAuth](/developers/en/docs/security/oauth) documentation for more details.
* **Use the authorization code flow with PKCE**: If the integration is done with the flow **Authorization code** by OAuth, you can enable PKCE (Proof Key for Code Exchange) to generate an additional secret code to be used during the authorization process. Check out [Configure PKCE](/developers/en/docs/security/oauth/creation#:~:text=Access%20Token.-,Configure%20PKCE,-The%20PKCE%20) documentation for more details.
* **Application permissions**: Options for accessing your application, including **read**, **offline access** and **write**. By default, your application is created with all permissions enabled, but you can disable a permission by unchecking the corresponding checkbox.

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

## Application quality measurement

The [quality measurement](/developers/en/docs/integration-quality) is the final stage of the integration process, where you can validate whether it meets the necessary quality and security requirements to provide the best experience for both sellers and buyers.

There are two ways to measure the quality of your integration:
 * **Manual:** you can conduct the measurement on your own whenever you prefer. You only need a `payment ID` from a payment made with production credentials and access **“Integration Quality"** in the side menu, where you can find the step-by-step instructions.

 * **Automatic:** From the 1st to the 7th of each month, Mercado Pago conducts a periodic quality measurement for all integrations with **Checkout Pro, Checkout API , Checkout Bricks, and Mercado Pago Point** that have a payment made with production credentials.

> WARNING
>
> Important
>
> The only way to evaluate the quality of an integration with **QR Code** is by performing a manual measurement. Integrations with **Plugins and Platforms** cannot be evaluated.

As a result of this measurement, you will receive a score indicating how secure and aligned your application's configuration is with Mercado Pago's best integration practices, along with necessary recommendations for adjustments if needed.

For more details, refer to the documentation on [integration quality](/developers/en/docs/integration-quality).

## Integration test

In this section, you have a step-by-step guide to test your integration, which will allow you to validate that you are meeting the necessary requirements based on the integrated product. 

In addition, you have direct links to the corresponding documentation, as well as a status bar that will allow you to view your progress easily.


# Credentials

Credentials are unique access keys that we use to identify an integration in your account. They are directly linked to the :toolTipComponent[application]{link="/developers/en/docs/your-integrations/application-details" linkText="Application details" content="Entity registered in Mercado Pago that acts as an identifier to manage your integrations. For more information, access the link below."} you created for that integration and will allow you to develop your project with the best Mercado Pago security measures.

## Types of credentials

Credentials are divided into two types: **production credentials** and **test credentials**. Below, we explain what they are about.

:::::TabsComponent

::::TabComponent{title="Production credentials"}
### Production credentials

**Production credentials** are a set of keys that allow you to receive real payments in stores and other applications.

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

::::TabComponent{title="Test credentials"}
### Test credentials

Test credentials are a set of keys that are used both in the development stage, to ensure secure settings, and in the testing stage, to test the integration.

> NOTE
> 
> Test credentials are only available for [Checkout API](https://www.mercadopago[FAKER][URL][DOMAIN]/developers/en/docs/checkout-api/landing) and [Checkout Bricks](https://www.mercadopago[FAKER][URL][DOMAIN]/developers/en/docs/checkout-bricks/landing) integrations.
---

---

When accessing the test credentials, the **Public Key and Access Token** credential pair will be displayed.

### Public Key and Access Token

The test **Public Key** and **Access Token** credentials are used in the same way as production credentials, but will not allow any real transactions to be made. In some integrations, they will be required during the development stage to simulate transactions and verify that your integration works correctly.

| Type | Description |
|---|---|
| Public Key | The application's public key is generally used in the frontend. It allows, for example, access to information about payment methods and encrypt card data. |
| Access Token | Application's private key that should always be used in the backend to generate payments. It is essential to keep this information safe on your servers. |

> NOTE
> 
> If when creating an application you selected a Mercado Pago product that does not require test credentials, you will not be able to use them. Instead, you must use the production credentials of a [test account](/developers/en/docs/your-integrations/test/accounts) to test your integration properly.

::::

:::::

## Get credentials

Mercado Pago credentials are created from a Mercado Pago application. That is, they are directly linked to the
:toolTipComponent[application]{link="/developers/es/docs/your-integrations/application-details" linkText="Application details" content="Entity registered in Mercado Pago that acts as an identifier to manage your integrations. For more information, see the documentation on [Application details](/developers/en/docs/your-integrations/application-details)."} that you created through Your integrations.

Below, learn how to get the credentials.

1. In the upper right corner of [Mercado Pago Developers](https://www.mercadopago[FAKER][URL][DOMAIN]/developers/panel/app), click **Log in** and fill in the required data with the information corresponding to your Mercado Pago account. Then, click on the **Your integrations** button located in the upper right corner.
2. Access your application or create one if you have not already done so.
3. You will find your credentials under the title **Testing > Test credentials** or **Production > Production credentials**, in the menu located on the left side of the screen.

![Cómo acceder a las credenciales a través de Tus Integraciones](/images/snippets/credentials-test-panel-es.jpg)

![Cómo acceder a las credenciales a través de Tus Integraciones](/images/snippets/credentials-prod-panel-es-v2.jpg)

### Activate production credentials
To obtain production credentials, you must **activate them** by completing some information about your business. Follow the steps below:

1. Go to [Your integrations](https://www.mercadopago[FAKER][URL][DOMAIN]/developers/panel/app) and select an application.
2. Go to the **Production credentials** section in the left side menu. You will find the **Public Key** and the **Access Token**.
3. In the **Industry** field, select from the drop-down menu the industry or category to which the business you are integrating belongs.
4. In the **Website (required)** field, complete with the URL of your business website.
5. Accept the [Privacy Statement](https://www.mercadopago[FAKER[URL][DOMAIN]]/privacidad) and the [Terms and Conditions](/developers/es/docs/resources/legal/terms-and-conditions). Fill in the reCAPTCHA and click on **Activate production credentials**.

When accessing production credentials, the following credential pairs will be displayed: **Public Key and Access Token**, as well as **Client ID and Client Secret**.

> NOTE
>
> Test credentials do not need to be activated. By simply creating an application, you can already use them.

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

![Compartir credenciales en Tus Integraciones](/images/snippets/share-credentials-panel-es.jpg)

## Renew credentials

You can renew your **production credentials** for security reasons or any other relevant reason.

> WARNING
>
> Renewing credentials already configured in an integration will affect its operation. It is necessary that **you replace the old credentials with the ones obtained** after the renewal process to continue operating.

To renew a credential pair, follow the steps below.

1. Access your production credentials through [Your integrations](https://www.mercadopago[FAKER][URL][DOMAIN]/developers/panel/app).
2. Select the credential pair you want to renew. These can be **Public Key** and **Access Token** or **Client ID** and **Client Secret**. Keep in mind that both credentials in the pair you choose will be renewed.
3. Click on the three dots located to the right of the credential you want to renew and select **Renew**. Click on **Renew now** to confirm the change.

![Cómo renovar tus credenciales](/images/snippets/renew-credentials-es.jpg)

Ready, your credentials have been renewed.

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


# Test accounts

Use test accounts to ensure that your integration supports all possible flows and scenarios. They have the same features as a real Mercado Pago account, which allows you to test the functioning of the integrations you are developing.

Test accounts are **automatically created** after the application is created. If you prefer to create them manually, follow the steps below. You can generate **up to 15 test user accounts** simultaneously, and for now, it is not possible to delete them.

> WARNING
>
> Integrations with [Checkout Bricks](/developers/en/docs/checkout-bricks/landing) do not support test accounts for integration testing. For more information, please refer to the documentation [Make test purchase](/developers/en/docs/checkout-bricks/integration-test/test-payment-flow) with Checkout Bricks.

To perform the test, you must have at least two accounts:

* **Seller**: account required to **configure application and credentials**. This is your user account.
* **Buyer**: account required to **test the purchase process**.
* **Integrator**: account used in **marketplace model integrations**.

In addition to these accounts, it is also important to use [test cards](/developers/en/docs/additional-content/your-integrations/test-cards) to test payment integration and simulate the purchase process, as well as **balance in the test user's Mercado Pago account**. See more details below.

![create test user](/images/snippets/test-cross/test-user-es-create-seller-v1.png)

To create accounts and test how the integrations work, follow the steps below.

1. On the [Devsite](/developers/en/docs), navigate to **[Your integrations](/developers/panel/app)** and click on the card corresponding to your application.
2. On the application page, go to the **Test accounts** section and click the **+ Create test account** button.
3. In the "Create new account" screen, select the **operating country** for the account. This information **cannot be edited later**, and furthermore, the Buyer and Seller users need to be from the same country.
4. Then, enter a description to identify the account. For example: "Seller - Store 1".
5. Next, select the type of account you want to create. This can be **Seller**, **Buyer** or **Integrator**.
6. If the test account requires it, enter a **fictional money value** that will serve as a reference for testing your applications. This value will appear as the balance in the Mercado Pago account of the test user and can be used for payment simulation, just like with the [test cards](/developers/en/docs/additional-content/your-integrations/test-cards).
7. Authorize the use of your personal data in accordance with the [Privacy Statement](https://www.mercadopago[FAKER][URL][DOMAIN]/privacidad) and ensure that your account uses Mercado Pago's tools in accordance with the [Terms and Conditions](https://www.mercadopago.com.br/developers/en/docs/resources/legal/terms-and-conditions) by checking the checkbox.
8. Click on **Create test account**.

Done! The test account has been created and will be displayed in the table with the information below.

![access test user](/images/snippets/test-cross/test-user-es-list-full-v1.png)

* **Country**: Origin location of the account selected in your registration.
* **User ID**: User identification number, which is created automatically.
* **User**: Automatically generated username of the test account. This is the username used to log in with the test user.
* **Password**: Automatically generated password to access the test user account. To generate a new password, click on the vertical ellipsis (three dots) at the end of the table row and select the **Generate new password** option.
* **Verification code**: 6-digit number that you must enter in case email verification is requested when logging in with the test account.

> NOTE
>
> To edit the **account identification** or **add more fictional money** to test your applications, click on the **vertical ellipsis** (three dots) at the end of the table row and select the **Edit data** option.

## Validate login with test accounts

If an email authentication is requested when logging in with test accounts, enter the **6-digit verification code** of that test account. You can find it in **[Your integrations](/developers/panel/app) > *Your application* > Tests > Test accounts**.

Please note that when you log in with a test account, you will not have access to certain sections within the Developer Dashboard, such as **Test Credentials** or **Integration Quality**. These are sections that are not only not necessary for this type of accounts, but can also interfere with their proper and desired use.

# Test cards

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


# Webhooks

Webhooks (also known as web callbacks) are a simple method that allows an application or system to provide real-time information whenever an event occurs. It's a passive way of receiving data between two systems via an `HTTP POST` request.

Webhooks notifications can be configured for each application created in [Your integrations](/developers/panel/app). You can also configure a test URL that, along with your test credentials, allows you to test the correct operation of your notifications before going live.

Once configured, the Webhook will be sent whenever one or more registered events occur, eliminating the need for constant checks and thus preventing system overload and data loss in critical situations.

To configure your Webhooks notifications, choose one of the options below:

| Configuration type | Description |
|---|---|
| [Configuration through Your integrations](/developers/en/docs/your-integrations/notifications/webhooks#bookmark_configuration_through_your_integrations) | Allows configuring notifications for each one of your applications, identifying different accounts if necessary, and validating the notification origin using the secret signature (except notifications for QR Code integrations). |
| [Configuration during payment creation](/developers/en/docs/your-integrations/notifications/webhooks#bookmark_configuration_during_payment_creation) | Allows specific configuration of notifications for each payment, preference or order . |

> WARNING
>
> Important
>
> The URLs configured during payment creation will take precedence over those configured through Your integrations.

Once notifications are configured, refer to the necessary [actions after receiving a notification](/developers/en/docs/your-integrations/notifications/webhooks#bookmark_necessary_actions_after_receiving_a_notification) to validate that the notifications were properly received.

## Configuration through Your integrations

Set up notifications for each application directly in [Your integrations](/developers/panel/app) efficiently and securely. In this documentation, we will explain how:
 1. Specify URLs and configure events
 2. Validate the notification source
 3. Simulate receiving the notification

> WARNING
>
> Important
>
> This configuration method is not available for QR Code or Subscriptions integrations. To set up notifications for either of these integrations, use the [Configuration during payment creation](/developers/en/docs/your-integrations/notifications/webhooks#bookmark_configuration_during_payment_creation) method.

### 1. Specify URLs and configure events

To configure Webhooks notifications via Your integrations, it is necessary to specify the URLs where they will be received and the events for which you wish to receive notifications.

To do this, follow these steps:

1. Access [Your integrations](/developers/panel/app) and select the application for which you want to enable notifications. If you haven't created an application yet, access the [Developer Dashboard documentation](/developers/en/docs/your-integrations/dashboard) and follow the instructions to do so.
2. In the left menu, click on **Webhooks > Configure notifications** and configure the URLs that will be used to receive notifications. We recommend using different URLs for testing mode and production mode:
  * **Test mode URL:** provide a URL that allows testing the correct operation of notifications for this application during the testing or development phase. Testing these notifications should be done exclusively with the **test credentials of productive users**.
  * **Production mode URL:** provide a URL to receive notifications with your productive integration. These notifications should be configured with **productive credentials**.

![webhooks](/images/dashboard/webhooks-es-v1.png)

> NOTE
>
> Note
> 
> If you need to identify multiple accounts, you can add the parameter `?cliente=(sellersname)` to the endpoint URL to identify the sellers.

3. Select the **events** from which you want to receive notifications in `JSON` format via an `HTTP POST` to the URL specified earlier. An event can be any type of update on the reported object, including status changes or attributes. Refer to the table below to see the events that can be configured, considering the integrated Mercado Pago solution and its business specifics.

| Events | Name in Your Integrations | Topic | Associated products |
|---|---|---|---|
| Creation and update of payments | Order (Mercado Pago) | `orders` | [Checkout API](/developers/en/docs/checkout-api-orders/overview)<br>[Mercado Pago Point](/developers/en/docs/mp-point/landing)<br>[QR Code](/developers/en/docs/qr-code/overview) |
| Creation and update of payments | Payments | `payment` | [Checkout API](/developers/en/docs/checkout-api-payments/overview) (**legacy**)<br>[Checkout Pro](/developers/en/docs/checkout-pro/overview)<br>[Checkout Bricks](/developers/en/docs/checkout-bricks/overview)<br>[Subscriptions](/developers/en/docs/subscriptions/overview)<br>[Wallet Connect](/developers/en/docs/wallet-connect/landing) |
| Recurring payment of a subscription (creation - update) | Plans and Subscriptions | `subscription_authorized_payment` | [Subscriptions](/developers/en/docs/subscriptions/overview) |
| Subscription linking (creation - update) | Plans and Subscriptions | `subscription_preapproval` | [Subscriptions](/developers/en/docs/subscriptions/overview) |
| Subscription plan linking (creation - update) | Plans and Subscriptions | `subscription_preapproval_plan` | [Subscriptions](/developers/en/docs/subscriptions/overview) |
| Linking and unlinking of accounts connected via OAuth | Application linking | `mp-connect` | All products that have implemented OAuth |
| Wallet Connect transactions | Wallet Connect | `wallet_connect` | [Wallet Connect](/developers/en/docs/wallet-connect/landing) |
| Fraud alerts after order processing | Fraud alerts | `stop_delivery_op_wh` | [Checkout API](/developers/en/docs/checkout-api-orders/overview)<br>[Checkout Pro](/developers/en/docs/checkout-pro/overview) |
| Creation of refunds and claims | Claims | `topic_claims_integration_wh` | [Checkout API](/developers/en/docs/checkout-api-orders/overview)<br>[Checkout Pro](/developers/en/docs/checkout-pro/overview)<br>[Checkout Bricks](/developers/en/docs/checkout-bricks/overview)<br>[Subscriptions](/developers/en/docs/subscriptions/overview)<br>[Wallet Connect](/developers/en/docs/wallet-connect/landing) |
| Retrieval of card information and update within Mercado Pago | Card Updater | `topic_card_id_wh` | [Checkout Pro](/developers/en/docs/checkout-pro/overview)<br>[Checkout API](/developers/en/docs/checkout-api-orders/overview)<br>[Checkout Bricks](/developers/en/docs/checkout-bricks/overview) |
| Creation, closure, or expiration of commercial orders | Commercial orders | `topic_merchant_order_wh` | [Checkout Pro](/developers/en/docs/checkout-pro/overview)<br>[QR Code](/developers/en/docs/qr-code-legacy/overview) (**legacy**) |
| Opening of chargebacks, status changes, and modifications related to the release of funds | Chargebacks | `topic_chargebacks_wh` | [Checkout Pro](/developers/en/docs/checkout-pro/overview)<br>[Checkout API](/developers/en/docs/checkout-api-orders/overview)<br>[Checkout Bricks](/developers/en/docs/checkout-bricks/overview) |

> WARNING
>
> Important
>
> If you have any questions about the topics to de activated or the events that will be notified, check the [Additional information about Notifications documentation](/developers/en/docs/your-integrations/notifications/additional-info). 

4. Finally, click on **Save**. This will generate a unique **secret signature** for your application, allowing you to validate the authenticity of received notifications, ensuring they were sent by Mercado Pago. Note that the generated signature does not have an expiration date, and its periodic renewal is not mandatory but highly recommended. Simply click the **Reset** button next to the signature to renew it.

> WARNING
> 
> Important
> 
> QR Code notifications cannot be verified using the secret signature. Therefore, you should proceed directly to the Simulate receiving notifications step. If you have a QR Code integration and still want to verify the origin of your notifications, please contact [Mercado Pago Support](https://www.mercadopago[FAKER][URL][DOMAIN]/developers/en/support/center).

### 2. Validate notification origin

Notifications sent by Mercado Pago will be similar to the following example for a `payment` topic alert:

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

Mercado Pago will always include the secret signature in the Webhooks notifications received at the registered URL, which will allow you to validate their authenticity to provide greater security and prevent potential fraud.

This signature will be sent in the `x-signature` header, as shown in the example below.

```x-signature

`ts=1704908010,v1=618c85345248dd820d5fd456117c2ab2ef8eda45a0282ff693eac24131a5e839`

```

To confirm the validation, it is necessary to extract the key from the _header_ and compare it with the key provided for your application in [Your integrations](/developers/panel/app). 

Follow one of the approaches below to validate the authenticity of the notification.

::::TabsComponent

:::TabComponent{title="With SDKs"}

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
  request.headers.get("x-signature"),
  request.headers.get("x-request-id"),
  request.args.get("data.id"),
  secret,
  )
  return "", 200
except InvalidWebhookSignatureError:
  return "", 401
```
```go
import "github.com/mercadopago/sdk-go/pkg/webhook"

err := webhook.ValidateSignature(
  r.Header.Get("x-signature"),
  r.Header.Get("x-request-id"),
  r.URL.Query().Get("data.id"),
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
  xSignature: Request.Headers["x-signature"],
  xRequestId: Request.Headers["x-request-id"],
  dataId: Request.Query["data.id"],
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
  request.getHeader("x-signature"),
  request.getHeader("x-request-id"),
  request.getParameter("data.id"),
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

:::TabComponent{title="Without SDKs"}
1. To extract the _timestamp_ (`ts`) and key (`v1`) from the `x-signature` _header_, divide the _header_ content by the `,` character, which will result in a list of elements. The value for the `ts` prefix is the notification _timestamp_ (in milliseconds) and `v1` is the encrypted key.
2. Using the _template_ below, substitute the parameters with the data received in your notification.

```
id:[data.id_url];request-id:[x-request-id_header];ts:[ts_header];
```

- `[data.id_url]` will be replaced by the value of the `data.id` parameter received in the URL _query params_.

> NOTE
>
> If `data.id` is returned with uppercase alphanumeric characters, convert it to lowercase before using it in the manifest. For example, `ORD01JQ4S4KY8HWQ6NA5PXB65B3D3` should be used as `ord01jq4s4ky8hwq6na5pxb65b3d3`.
- `[x-request-id_header]` must be replaced by the value received in the `x-request-id` _header_.
- `[ts_header]` will be the `ts` value extracted from the `x-signature` _header_.

> NOTE
>
> If any of the values (`data.id`, `x-request-id`) are not present in the received notification, you must remove them from the manifest before computing the `HMAC`.

3. In [Your integrations](/developers/panel/app), select the integrated application, click **Webhooks > Configure notification** and reveal the generated secret key.

4. Generate the counter-key for validation. To do this, compute an [HMAC](https://en.wikipedia.org/wiki/HMAC) with the `SHA256 hash` function in hexadecimal base, using the secret key as the key and the _template_ with the values as the message.

[[[
```php
$cyphedSignature = hash_hmac('sha256', $data, $key);
```
```node
const crypto = require('crypto');
const cyphedSignature = crypto
  .createHmac('sha256', secret)
  .update(signatureTemplateParsed)
  .digest('hex'); 
```
```java
String cyphedSignature = new HmacUtils("HmacSHA256", secret).hmacHex(signedTemplate);
```
```python
import hashlib, hmac, binascii

cyphedSignature = binascii.hexlify(hmac.new(secret.encode(), signedTemplate.encode(), hashlib.sha256).digest())
```
]]]

5. Finally, compare the generated key with the key extracted from the _header_, ensuring they match exactly. Additionally, you can use the _timestamp_ extracted from the _header_ to compare it with a _timestamp_ generated at the time of receipt, in order to establish a delay tolerance in receiving the message.

Here are complete code examples:

[[[
```php
<?php 
$client = new PaymentClient();

  $body = [
  'transaction_amount' => 100,
  'token' => 'token',
  'description' => 'description',
  'installments' => 1,
  'payment_method_id' => 'visa',
  'notification_url' => 'http://test.com',
  'payer' => array(
  'email' => 'test_payer@example.com',
  'identification' => array(
  'type' => 'CPF',
  'number' => '19119119100'
  )
  )
  ];

$client->create(body);
?>
```
```node
const client = new MercadoPagoConfig({ accessToken: 'ACCESS_TOKEN' });
const payment = new Payment(client);

const body = {
 transaction_amount: '100',
  token: 'token',
  description: 'description',
  installments: 1,
  payment_method_id: 'visa',
  notification_url: 'http://test.com',
  payer: {
  email: 'test_payer@example.com',
  identification: {
  type: 'CPF',
  number: '19119119100'
  }
  }
};

payment.create({ body: body, requestOptions: { idempotencyKey: '<SOME_UNIQUE_VALUE>' } }).then(console.log).catch(console.log);
```
```java
MercadoPago.SDK.setAccessToken("YOUR_ACCESS_TOKEN");

Payment payment = new Payment();
payment.setTransactionAmount(Float.valueOf(request.getParameter("transactionAmount")))
  .setToken(request.getParameter("token"))
  .setDescription(request.getParameter("description"))
  .setInstallments(Integer.valueOf(request.getParameter("installments")))
  .setPaymentMethodId(request.getParameter("paymentMethodId"))
  .setNotificationUrl("http://requestbin.fullcontact.com/1ogudgk1");

Identification identification = new Identification();
identification.setType(request.getParameter("docType"))
  .setNumber(request.getParameter("docNumber")); 

Payer payer = new Payer();
payer.setEmail(request.getParameter("email"))
  .setIdentification(identification);
  
payment.setPayer(payer);

payment.save();

System.out.println(payment.getStatus());

```
```ruby
require 'mercadopago'
sdk = Mercadopago::SDK.new('YOUR_ACCESS_TOKEN')

payment_data = {
 transaction_amount: params[:transactionAmount].to_f,
 token: params[:token],
 description: params[:description],
 installments: params[:installments].to_i,
 payment_method_id: params[:paymentMethodId],
 notification_url: "http://requestbin.fullcontact.com/1ogudgk1",
 payer: {
  email: params[:email],
  identification: {
  type: params[:docType],
  number: params[:docNumber]
  }
 }
}

payment_response = sdk.payment.create(payment_data)
payment = payment_response[:response]

puts payment

```
```csharp
using System;
using MercadoPago.Client.Common;
using MercadoPago.Client.Payment;
using MercadoPago.Config;
using MercadoPago.Resource.Payment;

MercadoPagoConfig.AccessToken = "YOUR_ACCESS_TOKEN";

var paymentRequest = new PaymentCreateRequest
{
  TransactionAmount = decimal.Parse(Request["transactionAmount"]),
  Token = Request["token"],
  Description = Request["description"],
  Installments = int.Parse(Request["installments"]),
  PaymentMethodId = Request["paymentMethodId"],
  NotificationUrl = "http://requestbin.fullcontact.com/1ogudgk1",

  Payer = new PaymentPayerRequest
  {
  Email = Request["email"],
  Identification = new IdentificationRequest
  {
  Type = Request["docType"],
  Number = Request["docNumber"],
  },
  },
};

var client = new PaymentClient();
Payment payment = await client.CreateAsync(paymentRequest);

Console.WriteLine(payment.Status);

```
```python
import mercadopago
sdk = mercadopago.SDK("ACCESS_TOKEN")

payment_data = {
  "transaction_amount": float(request.POST.get("transaction_amount")),
  "token": request.POST.get("token"),
  "description": request.POST.get("description"),
  "installments": int(request.POST.get("installments")),
  "payment_method_id": request.POST.get("payment_method_id"),
  "notification_url" = "http://requestbin.fullcontact.com/1ogudgk1",
  "payer": {
  "email": request.POST.get("email"),
  "identification": {
  "type": request.POST.get("type"), 
  "number": request.POST.get("number")
  }
  }
}

payment_response = sdk.payment().create(payment_data)
payment = payment_response["response"]

print(payment)
```
```go
accessToken := "{{ACCESS_TOKEN}}"

cfg, err := config.New(accessToken)
if err != nil {
  fmt.Println(err)
  return
}

client := payment.NewClient(cfg)

request := payment.Request{
  TransactionAmount: <transactionAmount>,
  Token: <token>,
  Description: <description>,
  Installments: <installments>,
  PaymentMethodID: <paymentMethodId>,
  NotificationURL: "https:/mysite.com/notifications/new",
  Payer: &payment.PayerRequest{
  Email: <email>,
  Identification: &payment.IdentificationRequest{
  Type: <type>,
  Number: <number>,
  },
  },
}

resource, err := client.Create(context.Background(), request)
if err != nil {
fmt.Println(err)
}

fmt.Println(resource)
```
```curl
curl -X POST \
  -H 'accept: application/json' \
  -H 'content-type: application/json' \
  -H 'Authorization: Bearer YOUR_ACCESS_TOKEN' \
  'https://api.mercadopago.com/v1/payments' \
  -d '{
  "transaction_amount": 100,
  "token": "ff8080814c11e237014c1ff593b57b4d",
  "description": "Blue shirt",
  "installments": 1,
  "payment_method_id": "visa",
  "issuer_id": 310,
  "notification_url": "http://requestbin.fullcontact.com/1ogudgk1",
  "payer": {
  "email": "test_payer@example.com"

  }
  }'

```
]]]

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

After making the necessary configurations, the Webhooks notification will be delivered in `JSON` format. See the example of a notification for the `payments` topic and the descriptions of the information sent in the table below.

> WARNING
>
> Important
>
> Test payments, created with test credentials, will not send notifications. The only way to test notification reception is through the [Configuration through Your integrations](/developers/en/docs/your-integrations/notifications/webhooks#bookmark_configuration_through_your_integrations).

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
| **live_mode** | Indicates if the URL provided is valid | `true` |
| **type** | Type of notification received according to the previously selected topic (payments, mp-connect, subscription, claim, automatic-payments, etc.) | `payment` |
| **date_created** | Date the notified resource was created | `2015-03-25T10:04:58.396-04:00` |
| **user_id**| Seller identifier | `44444` |
| **api_version** | Value indicating the API version sending the notification | `v1` |
| **action** | Notified event, indicating if it's a resource update or a new creation | `payment.created` |
| **data.id** | ID of the payment, `merchant_order`, or claim | `999999999` |

> WARNING
>
> Important
>
> To obtain the notification format for topics other than `payment`, such as `topic_claims_integration_wh` and `topic_card_id_wh`, consult [Additional information about notifications](/developers/en/docs/your-integrations/notifications/additional-info).

## Necessary actions after receiving a notification

When you receive a notification on your platform, Mercado Pago expects a response to validate that you received it correctly. To do this, you need to return an `HTTP STATUS 200 (OK)` or `201 (CREATED)` status.

The **waiting time** for confirmation of receipt of notifications is **22 seconds**. If this confirmation is not sent, the system will understand that the notification was not received and will **retry sending every 15 minutes** until a response is received. After the third attempt, the interval will be extended, but the attempts will continue.

After responding to the notification and confirming its receipt, you can obtain the complete information of the notified resource by making a request to the corresponding API endpoint. To identify which endpoint to use, check the table below:

| Topic | URL | Documentation |
| --- | --- | --- |
| order | `https://api.mercadopago.com/v1/orders/{id}` | [Get order by ID](/developers/en/reference/online-payments/checkout-api/get-order/get) (for [Checkout API](/developers/en/docs/checkout-api-orders/overview)) |
| order | `https://api.mercadopago.com/v1/orders/{order_id}` | [Get order by ID](/developers/en/reference/in-person-payments/point/orders/get-order/get) (for [Mercado Pago Point](/developers/en/docs/mp-point/overview)) |
| order | `https://api.mercadopago.com/v1/orders/{order_id}` | [Get order by ID](/developers/en/reference/in-person-payments/qr-code/orders/get-order/get) (for [QR Code](/developers/en/docs/qr-code/overview)) |
| payment | `https://api.mercadopago.com/v1/payments/[ID]` | Get payment for [Checkout API](/developers/en/reference/online-payments/checkout-api-payments/get-payment/get), [Checkout Pro](/developers/en/reference/online-payments/checkout-pro/get-payment/get) or [Subscriptions](/developers/en/reference/online-payments/subscriptions/get-payment/get) |
| subscription_preapproval | `https://api.mercadopago.com/preapproval/search` | [Search subscriptions](/developers/en/reference/online-payments/subscriptions/search-preapproval/get) |
| subscription_preapproval_plan | `https://api.mercadopago.com/preapproval_plan/search` | [Search subscription plans](/developers/en/reference/online-payments/subscriptions/search-preapproval-plan/get) |
| subscription_authorized_payment | `https://api.mercadopago.com/authorized_payments/[ID]` | [Get invoice data](/developers/en/reference/online-payments/subscriptions/get-authorized-payment/get) |
| topic_claims_integration_wh | `https://api.mercadopago.com/post-purchase/v1/claims/[claim_id]` | [Get claim details](/developers/en/reference/claims/get-claim-details/get) |
| topic_merchant_order_wh | `https://api.mercadopago.com/merchant_orders/[ID]` | [Get merchant order for Checkout Pro](/developers/en/reference/online-payments/checkout-pro/merchant_orders/get-merchant-order/get) or for [QR Code (deprecated)]()|
| topic_chargebacks_wh | `https://api.mercadopago.com/v1/chargebacks/[ID]` | [Get chargeback](/developers/en/reference/online-payments/checkout-pro/get-chargeback/get) |

| Topic | URL | Documentation |
| --- | --- | --- |
| order | `https://api.mercadopago.com/v1/orders/{id}` | [Get order by ID](/developers/en/reference/online-payments/checkout-api/get-order/get) (for [Checkout API](/developers/en/docs/checkout-api-orders/overview)) |
| order | `https://api.mercadopago.com/v1/orders/{order_id}` | [Get order by ID](/developers/en/reference/in-person-payments/point/orders/get-order/get) (for [Mercado Pago Point](/developers/en/docs/mp-point/overview)) |
| payment | `https://api.mercadopago.com/v1/payments/[ID]` | Get payment for [Checkout API](/developers/en/reference/online-payments/checkout-api-payments/get-payment/get), [Checkout Pro](/developers/en/reference/online-payments/checkout-pro/get-payment/get) or [Subscriptions](/developers/en/reference/online-payments/subscriptions/get-payment/get) |
| subscription_preapproval | `https://api.mercadopago.com/preapproval/search` | [Search subscriptions](/developers/en/reference/online-payments/subscriptions/search-preapproval/get) |
| subscription_preapproval_plan | `https://api.mercadopago.com/preapproval_plan/search` | [Search subscription plans](/developers/en/reference/online-payments/subscriptions/search-preapproval-plan/get) |
| subscription_authorized_payment | `https://api.mercadopago.com/authorized_payments/[ID]` | [Get invoice data](/developers/en/reference/online-payments/subscriptions/get-authorized-payment/get) |
| topic_claims_integration_wh | `https://api.mercadopago.com/post-purchase/v1/claims/[claim_id]` | [Get claim details](/developers/en/reference/claims/get-claim-details/get) |
| topic_merchant_order_wh | `https://api.mercadopago.com/merchant_orders/[ID]` | [Get merchant order for Checkout Pro](/developers/en/reference/online-payments/checkout-pro/merchant_orders/get-merchant-order/get) or for [QR Code (deprecated)]()|
| topic_chargebacks_wh | `https://api.mercadopago.com/v1/chargebacks/[ID]` | [Get chargeback](/developers/en/reference/online-payments/checkout-pro/get-chargeback/get) |

With this information, you will be able to make the necessary updates to your platform, such as updating an approved payment.

## Notifications dashboard

The notification dashboard allows the user to view the events triggered on a specific integration, check the status, and obtain detailed information about these events.

This dashboard will be displayed once you configure your Webhooks notifications, and you can access it anytime by clicking on **Webhooks** within the [Your integrations](/developers/panel/app).

Among the available information, you will find the percentage of notifications delivered, as well as a quick view of which URLs and events are configured.

Additionally, you will find a complete list of the latest notifications sent and their details, such as **delivery status** (success or failure), **action** (action associated with the triggered event), **event** (type of triggered event), and **date and time**. If desired, you can filter these displayed results by **delivery status** and by period (**date and time**).

![notifications dashboard](/images/dashboard/notification-dashboard-es-v1.png)

### Evet details

When you click on one of the listed notifications, you can access the event details. This section provides additional information, allowing you to retrieve lost data in case of notification delivery failure, thereby keeping your system up to date.
 * **Status:** Event status along with the corresponding success or error code.
 * **Event:** Type of event triggered as selected in the notification configuration.
 * **Type:** Topic to which the triggered event belongs as selected during configuration.
 * **Trigger date and time:** Date and time when the event was triggered.
 * **Description:** Detailed description of the event as documented.
 * **Trigger ID:** Unique identifier of the sent notification.
 * **Request:** JSON of the request corresponding to the triggered notification.

![notifications details](/images/dashboard/notification-details-dashboard-es-v1.png)

In case of notification delivery failure, you can view the reasons and correct the necessary information to prevent future issues.

# IPN

Instant Payment Notification (IPN) is a mechanism that allows your application to receive notifications from Mercado Pago informing about the status of a specific payment, chargeback, or `merchant_order`, through an `HTTP POST` call to report on your transactions.

> WARNING
>
> Important
>
> IPN notifications will be discontinued. Additionally, despite receiving the `x-Signature` header, they do not allow validation through the secret key to confirm they were sent by Mercado Pago. If you wish to perform this origin validation, we recommend migrating to [Webhooks notifications](/developers/en/docs/your-integrations/notifications/webhooks), which now also send the `merchant_order` and `chargebacks` topics.

IPN notifications can be configured in two ways: 

| Configuration mode | Description |
|---|---|
| [Description configuration through Your integrations](/developers/en/docs/your-integrations/notifications/ipn#bookmark_configuration_through_your_integrations) | Only **one notification URL** can be configured per account (depending on the application, more than one application can use this URL). |
| [Configuration during the creation of a payment, preference or order](/developers/en/docs/your-integrations/notifications/ipn#bookmark_configuration_during_payment_creation) | This can be done using the `notification_url` field. The URL can be different for each object. |

In this documentation, we will explain the necessary configurations for receiving IPN notifications, as well as the required actions to ensure that Mercado Pago validates that the messages were properly received.

## Configuration through Your integrations

Configure notifications directly in Your integrations efficiently and securely.

### Specify URLs and configure events

To configure IPN notifications via Your integrations, it is necessary to specify the URLs where they will be received and specify the events for which you wish to receive notifications.

> WARNING
>
> Important
>
> When configuring IPN notifications via Your integrations, you are setting up the URL and Events for **all applications within your Mercado Pago account**.

To configure URLs and events, follow these steps:

1. Access [Your integrations](/developers/panel/app) and select the application to enable notifications for your account. If you haven't created an application yet, access the [Developer Dashboard documentation](/developers/en/docs/your-integrations/dashboard) and follow the instructions to do so.
2. In the left menu, click on **IPN** and configure the **production URL** that will be used to receive notifications. Keep in mind that you can also experiment and test whether the indicated URL is correctly receiving notifications, allowing you to verify the request, server response, and event description.

![ipn](/images/dashboard/ipn_es_v1.png)

> NOTE
>
> Note
>
> If you need to identify multiple accounts, you can add the parameter `?cliente=(sellersname)` to the endpoint URL to identify the sellers.

3. Select the **events** from which you want to receive notifications in JSON format via an HTTP POST to the URL specified earlier. An event can be any type of update on the reported object, including status changes or attributes. Refer to the table below to see the events that can be configured, considering the integrated Mercado Pago solution and its business specifics.

| Events| Name in Your integrations | Topic | Associated products |
|---|---|---|---|
| Creation and update of payments | Payments | `payment` | [Checkout API](/developers/en/docs/checkout-api-payments/overview) (**legacy**)<br>[Checkout Pro](/developers/en/docs/checkout-pro/overview)<br>[Checkout Bricks](/developers/en/docs/checkout-bricks/overview)<br>[Subscriptions](/developers/en/docs/subscriptions/overview)<br>[Mercado Pago Point](/developers/en/docs/mp-point-legacy/overview) (**legacy**)<br>[Wallet Connect](/developers/en/docs/wallet-connect/landing) |
| Fraud alerts after processing an order | Fraud alerts | `delivery_cancellation` | [Checkout API](/developers/en/docs/checkout-api-payments/overview) (**legacy**)<br>[Checkout Pro](/developers/en/docs/checkout-pro/overview) |
| Creation, closure, or expiration of commercial orders | Commercial orders | `merchant_order` | [Checkout Pro](/developers/en/docs/checkout-pro/overview)<br>[QR Code](/developers/en/docs/qr-code-legacy/overview) (**legacy**) |
| Opening of chargebacks, status changes, and modifications related to the release of funds | Chargebacks | `chargebacks` | [Checkout Pro](/developers/en/docs/checkout-pro/overview)<br>[Checkout API](/developers/en/docs/checkout-api-payments/overview) (**legacy**)<br>[Checkout Bricks](/developers/en/docs/checkout-bricks/overview) |

> WARNING
>
> Important
>
> If you have any questions about the topics to activate or the events that will be notified, consult the documentation [Additional information about notifications](/developers/en/docs/your-integrations/notifications/additional-info). 

4. Finally, click on **Save**. 

## Configuration during payment creation

During the process of creating a payment, preference or order, it's possible to configure the notification URL more specifically for each payment using the `notification_url` field and implementing the necessary notification receiver. 

Next, we explain how to do this with the help of the SDKs.

1. In the `notification_url` field, specify the URL where notifications will be received, as shown in the example below. To receive notifications exclusively via Webhooks and not via IPN, you can add the parameter `source_news=ipn` to the `notification_url`. For example: `https://www.yourserver.com/notifications?source_news=ipn`.

> WARNING
>
> Do not use local domains in the `notification_url` value, such as 'localhost/' or '127.0.0.1' with or without a specified port. We recommend using a server with a named domain (DNS) or an externally accessible development IP so that Mercado Pago can send notifications correctly.

[[[
```php
<?php
  require_once 'vendor/autoload.php';

  MercadoPago\SDK::setAccessToken("YOUR_ACCESS_TOKEN");

  $payment = new MercadoPago\Payment();
  $payment->transaction_amount = (float)$_POST['transactionAmount'];
  $payment->token = $_POST['token'];
  $payment->description = $_POST['description'];
  $payment->installments = (int)$_POST['installments'];
  $payment->payment_method_id = $_POST['paymentMethodId'];
  $payment->issuer_id = (int)$_POST['issuer'];
  $payment->notification_url = `http://requestbin.fullcontact.com/1ogudgk1`;
  ...
  $response = array(
  'status' => $payment->status,
  'status_detail' => $payment->status_detail,
  'id' => $payment->id
  );
  echo json_encode($response);

?>
```
```node
var mercadopago = require('mercadopago');
mercadopago.configurations.setAccessToken("YOUR_ACCESS_TOKEN");

var payment_data = {
 transaction_amount: Number(req.body.transactionAmount),
 token: req.body.token,
 description: req.body.description,
 installments: Number(req.body.installments),
 payment_method_id: req.body.paymentMethodId,
 issuer_id: req.body.issuer,
 notification_url: "http://requestbin.fullcontact.com/1ogudgk1",
 payer: {
  email: req.body.email,
  identification: {
  type: req.body.docType,
  number: req.body.docNumber
  }
 }
};

mercadopago.payment.save(payment_data)
 .then(function(response) {
  res.status(response.status).json({
  status: response.body.status,
  status_detail: response.body.status_detail,
  id: response.body.id
≈ });
 })
 .catch(function(error) {
  res.status(response.status).send(error);
 });
```
```java
MercadoPago.SDK.setAccessToken("YOUR_ACCESS_TOKEN");

Payment payment = new Payment();
payment.setTransactionAmount(Float.valueOf(request.getParameter("transactionAmount")))
  .setToken(request.getParameter("token"))
  .setDescription(request.getParameter("description"))
  .setInstallments(Integer.valueOf(request.getParameter("installments")))
  .setPaymentMethodId(request.getParameter("paymentMethodId"))
  .setNotificationUrl("http://requestbin.fullcontact.com/1ogudgk1");

Identification identification = new Identification();
identification.setType(request.getParameter("docType"))
  .setNumber(request.getParameter("docNumber")); 

Payer payer = new Payer();
payer.setEmail(request.getParameter("email"))
  .setIdentification(identification);
  
payment.setPayer(payer);

payment.save();

System.out.println(payment.getStatus());

```
```ruby
require 'mercadopago'
sdk = Mercadopago::SDK.new('YOUR_ACCESS_TOKEN')

payment_data = {
 transaction_amount: params[:transactionAmount].to_f,
 token: params[:token],
 description: params[:description],
 installments: params[:installments].to_i,
 payment_method_id: params[:paymentMethodId],
 notification_url: "http://requestbin.fullcontact.com/1ogudgk1",
 payer: {
  email: params[:email],
  identification: {
  type: params[:docType],
  number: params[:docNumber]
  }
 }
}

payment_response = sdk.payment.create(payment_data)
payment = payment_response[:response]

puts payment

```
```csharp
using System;
using MercadoPago.Client.Common;
using MercadoPago.Client.Payment;
using MercadoPago.Config;
using MercadoPago.Resource.Payment;

MercadoPagoConfig.AccessToken = "YOUR_ACCESS_TOKEN";

var paymentRequest = new PaymentCreateRequest
{
  TransactionAmount = decimal.Parse(Request["transactionAmount"]),
  Token = Request["token"],
  Description = Request["description"],
  Installments = int.Parse(Request["installments"]),
  PaymentMethodId = Request["paymentMethodId"],
  NotificationUrl = "http://requestbin.fullcontact.com/1ogudgk1",

  Payer = new PaymentPayerRequest
  {
  Email = Request["email"],
  Identification = new IdentificationRequest
  {
  Type = Request["docType"],
  Number = Request["docNumber"],
  },
  },
};

var client = new PaymentClient();
Payment payment = await client.CreateAsync(paymentRequest);

Console.WriteLine(payment.Status);

```
```python
import mercadopago
sdk = mercadopago.SDK("ACCESS_TOKEN")

payment_data = {
  "transaction_amount": float(request.POST.get("transaction_amount")),
  "token": request.POST.get("token"),
  "description": request.POST.get("description"),
  "installments": int(request.POST.get("installments")),
  "payment_method_id": request.POST.get("payment_method_id"),
  "notification_url": "http://requestbin.fullcontact.com/1ogudgk1",
  "payer": {
  "email": request.POST.get("email"),
  "identification": {
  "type": request.POST.get("type"), 
  "number": request.POST.get("number")
  }
  }
}

payment_response = sdk.payment().create(payment_data)
payment = payment_response["response"]

print(payment)
```
```curl
curl -X POST \
  -H 'accept: application/json' \
  -H 'content-type: application/json' \
  -H 'Authorization: Bearer YOUR_ACCESS_TOKEN' \
  'https://api.mercadopago.com/v1/payments' \
  -d '{
  "transaction_amount": 100,
  "token": "ff8080814c11e237014c1ff593b57b4d",
  "description": "Blue shirt",
  "installments": 1,
  "payment_method_id": "visa",
  "issuer_id": 310,
  "notification_url": "http://requestbin.fullcontact.com/1ogudgk1",
  "payer": {
  "email": "test_payer@example.com"

  }
  }'

```
]]]

2. Implement the notification receiver using the following code as an example:

```php
<?php
  MercadoPago\SDK::setAccessToken("ENV_ACCESS_TOKEN");
  $merchant_order = null;
  switch($_GET["topic"]) {
  case "payment":
  $payment = MercadoPago\Payment::find_by_id($_GET["id"]);
  // Get the payment and the corresponding merchant_order reported by the IPN.
  $merchant_order = MercadoPago\MerchantOrder::find_by_id($payment->order->id);
  break;
  case "merchant_order":
  $merchant_order = MercadoPago\MerchantOrder::find_by_id($_GET["id"]);
  break;
  }
  $paid_amount = 0;
  foreach ($merchant_order->payments as $payment) { 
  if ($payment['status'] == 'approved'){
  $paid_amount += $payment['transaction_amount'];
  }
  }
  // If the payment's transaction amount is equal (or bigger) than the merchant_order's amount you can release your items
  if($paid_amount >= $merchant_order->total_amount){
  if (count($merchant_order->shipments)>0) { // The merchant_order has shipments
  if($merchant_order->shipments[0]->status == "ready_to_ship") {
  print_r("Totally paid. Print the label and release your item.");
  }
  } else { // The merchant_order don't has any shipments
  print_r("Totally paid. Release your item.");
  }
  } else {
  print_r("Not paid yet. Do not release your item.");
  }
 ?>
```

3. Once the configurations are done, Mercado Pago will notify that URL with two parameters every time a resource is created or updated. For example, if you set up the URL `https://www.yoursite.com/notifications`, you will receive payment notifications like this: `https://www.yoursite.com/notifications?topic=payment&id=123456789`.

| Field | Description |
| --- | --- |
| `topic` | Identifies what the resource is, which could be `payment`, `chargebacks`, `merchant_order ` o `point_integration_ipn`. |
| `id` | It is a unique identifier of the notified resource. |

## Necessary actions after receiving a notification

When you receive a notification on your platform, Mercado Pago expects a response to validate that you received it correctly. To do this, you need to return an `HTTP STATUS 200 (OK)` or `201 (CREATED)` status.

The **waiting time** for that confirmation is **22 seconds**. If this confirmation is not sent, the system will understand that the notification was not received and will **retry sending every 15 minutes** until a response is received. After the third attempt, the interval will be extended, but the attempts will continue.

After responding to the notification and confirming its receipt, you can obtain the complete information of the notified resource by making a request to the corresponding API endpoint. To identify which endpoint to use, check the table below:

| Topic | URL | Documentation |
| --- | --- | --- |
| payment | `https://api.mercadopago.com/v1/payments/[ID]` | [Get payment](/developers/en/reference/online-payments/checkout-api-payments/get-payment/get) |
| point_integration_ipn| `https://api.mercadopago.com/point/integration-api/payment-intents/{paymentintentid}` | [Search payment intent](/developers/en/reference/integrations_api/_point_integration-api_payment-intents_paymentintentid/get) |
| merchant_orders | `https://api.mercadopago.com/merchant_orders/[ID]` | [Get merchant order for Checkout Pro](/developers/en/reference/online-payments/checkout-pro/merchant_orders/get-merchant-order/get) or for [QR Code (deprecated)]() |
| chargebacks | `https://api.mercadopago.com/v1/chargebacks/[ID]` | [Get chargeback](/developers/en/reference/online-payments/checkout-pro/get-chargeback/get) |

With this information, you will be able to make the necessary updates to your platform, such as updating an approved payment.

# Additional information about notifications

In this documentation, you will find additional information about notifications, including special considerations depending on the solution you have integrated, specific aspects of certain topics, and examples of particular notifications for your reference.

## Card Updater

Card Updater is a feature for product integrations with recurring payments that updates card data, whether expired or incorrect, and updates this information within Mercado Pago.

This process is triggered by a rejected payment, where the verification done by Card Updater can either generate a new `card_id` for a customer (in cases of data entry errors or card changes) or keep the previously generated `card_id` while updating the database with the correct card information.

In either case, a Webhooks notification will be sent as shown below:

```json

{
  "action": "card.updated",
  "api_version": "v1",
  "application_id": 8339021212080291,
  "data": {
  "customer_id": "12345678-aluyasdhfyt",
  "new_card_id": 50000102202,
  "old_card_id": 50000006036
  },
  "date_created": "2024-01-11T15:23:53-03:00",
  "id": "a47fc06844bf4e418a03aeab1479c496",
  "live_mode": true,
  "type": "automatic-payments",
  "user_id": 1197520450,
  "version": 1
}
```

| Field | Description |
|---|---|
| `action` | `card.updated` is the only possible value and indicates when a customer's card was updated. |
| `application_id` | Identifier of the application being notified. |
| `data` | This field contains the update details, such as the `customer_id` (customer identifier), the new `card_id`, and the old `card_id`. If a new `card_id` is not created, the original one is resent. |
| `date_created` | Creation date of the notification. |
| `id` | Exclusive identifier of the event, prevents duplicate messages. |
| `live_mode` | Indicates if the informed URL is valid. |
| `type` | This value will always be `automatic-payments`. |
| `user_id` | Identifier of the user to whom the notification is sent. |

## Subscriptions

To activate notifications for your Subscriptions integration, you should keep in mind:
* If you have integrated **Subscriptions with associated plans**, you must activate the `subscription_preapproval_plan` topic to receive alerts about the creation or update of a Plan.
* If you have integrated **Subscriptions without associated plans**, you must activate the `subscription_preapproval` topic to receive alerts about the creation or update of a **pending payment subscription**, or the `subscription_authorized_payment` topic for updates on **authorized payment subscriptions**.
* In **all cases, you should also activate the payments topic**, which will allow you to receive notifications about payments associated with those subscriptions when they are made.

## Checkout Pro

If you have integrated with Checkout Pro and want to receive notifications, you should keep in mind:
* Activating the `merchant_orders` topic will allow you to receive alerts about the creation and updates of orders.
* Additionally, activating the `payments` topic will be useful for keeping your database up to date, as it will notify you about updates to the payments corresponding to those generated orders.

## Fraud alerts

If a fraud alert is detected, and you have the `stop_delivery_op_wh` topic activated, you will receive a notification like the following:

```json
{
  "action": "Created",
  "api_version": "v1",
  "data": {
  "description": "desc",
  "merchant_order": 249940988000,
  "payment_id": 58980959081,
  "site_id": "MLA"
  },
  "date_created": "2022-07-23T23:03:5704:00",
  "id": "58980959081",
  "live_mode": true,
  "type": "stop_delivery_op_wh",
  "user_id": 224403329,
  "version": 1
}
```

It includes the details of the order that triggered the alert, under the merchant_order parameter, and the payment_id associated with the payment. With this information, you should proceed to **cancel the order without delivering it** by making a requisition to the cancellations API for [Checkout API](/developers/en/reference/online-payments/checkout-api-payments/create-cancellation/put) or [Checkout Pro](/developers/en/reference/online-payments/checkout-pro/create-cancellation/put).

Please note that this type of notification does not adhere to the usual retry logic. If you do not respond with an `HTTP STATUS 200 (OK)` or `201 (CREATED)` upon receipt, the notification will be lost and will not be resent.

## Claims

In cases where notifications for the topic `topic_claims_integration_wh` have been activated, a Webhooks notification will be sent when a claim or chargeback is initiated, as shown below:

```json
{
  "action": "Created",
  "api_version": "v1",
  "data": {
  "description": "desc",
  "merchant_order": 249940988000,
  "payment_id": 58980959081,
  "site_id": "MLA"
  },
  "date_created": "2022-07-23T23:03:5704:00",
  "id": "58980959081",
  "live_mode": true,
  "type": "stop_delivery_op_wh",
  "user_id": 224403329,
  "version": 1
}
```

| Field | Description |
|---|---|
| `action` | Notification event, indicating whether it is the creation of a resource or its update. |
| `api_version` | Value indicating the API version sending the notification. |
| `data.id` | Unique identifier of the claim or chargeback. |
| `data.resource` | Type of notification received. In this case, it indicates notifications related to claims. |
| `date_created` | Notification creation date. |
| `id` | Received notification identifier. |
| `live_mode` | Indicates if the provided URL is valid. |
| `type` | Type of notification received, according to the previously selected topic. In this case, it will always be `claim`. |
| `user_id `| User identifier for whom the notification is sent. |

## Chargebacks

In cases where notifications for the topic `topic_chargebacks_wh` have been activated, a Webhooks notification will be sent when a chargeback is initiated or its status is changed, as shown below:

```json
{
  "actions":["changed_case_status"],
  "api_version":"v1",
  "application_id":9007201037432480,
  "data":{
  "checkout":"PRO",
  "date_updated":"0001-01-01T00:00:00Z",
  "id":217000061307271000,
  "payment_id":81034165129,
  "product_id":"BC32A57TRPP001U8NHHG",
  "site_id":"MLA",
  "transaction_intent_id":""
  },
  "date_created":"2024-07-02T22:03:24-04:00",
  "id":114544942708,
  "live_mode":true,
  "type":"topic_chargebacks_wh",
  "user_id":425424311,
  "version":1720427447
}
```

## Offline payment methods

If you have integrated payments with offline payment methods and configured your notifications with the payments topic, you should know that all changes in payment status will be notified to you.

This also applies to **expired payments**: their status will change from `pending` to `canceled`, and the corresponding alert will be sent to your system.

## QR Code

If you integrated with QR Code and wish to receive notifications, please note the following:
* Webhooks notifications cannot be configured through Your integrations. You must set them up when creating a payment.
* Consequently, it is not possible to validate the origin of notifications using the `x-Signature` header. For alternative methods to verify the origin of these notifications, please contact [Mercado Pago Support](https://www.mercadopago[FAKER][URL][DOMAIN]/developers/en/support/center).
* The activation of the `merchant_orders` topic will allow you to receive alerts about order creation and updates. While the topic sends a `status=opened`, it will be the notification with `status=closed` that will securely certify that the generated order has been paid.

## Payment links

It is not possible to configure notifications for Payment links generated through the Mercado Pago Panel.