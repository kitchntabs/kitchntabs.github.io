---
product_landing_hero:
 - title: Integrate Mercado Pago Point into your business model
 - message: Transform the payment experience by integrating Point terminals into your point of sale (POS) system. This integration allows you to process in-person payments with cards (including meal cards), and perform an automatic reconciliation of your sales with Mercado Pago in a unified manner.
 - image: https://http2.mlstatic.com/storage/dx-devsite/docs-assets/custom-upload/2025/5/19/1750357851664-terminalsmlbes.png
 - benefit_icon: categories
 - benefit_title: In-person payments
 - benefit_icon: link
 - benefit_title: Multiple payment methods
 - benefit_icon: sort
 - benefit_title: Automatic reconciliation
 - benefit_icon: categories
 - benefit_title: Service experience with or without operator
 - info: Are you looking for development-free options? Get a [card reader ready to operate](https://www.mercadopago.com.br/ferramentas-para-vender/maquininhas-point?code=POINT_ORG_LEGACY).
---

---
product_landing_how_works:
 - title: How it works
 - message: By integrating payments with the Point terminals, you will link them directly to your point of sale system. This way, you can process payments in a unified manner, reducing the possibility of unintentional errors and ensuring synchronization between your system and Mercado Pago.
 - sub_title: Payment collection process
 - image: https://http2.mlstatic.com/storage/dx-devsite/docs-assets/custom-upload/2025/5/23/1750690996278-howitworksen.png
 - image_text: Check the processing rates
 - image_text_link: https://www.mercadopago.com.br/developers/pt/support/37740
 - list_title: Create the payment order from your system using our unified API.
 - list_title: The Point terminal will automatically load the order.
 - list_title: The buyer makes the payment with the selected payment method.
 - list_title: The integrated system receives notification of the payment status.
 - button_description: How to integrate
 - button_link: /developers/en/docs/mp-point/create-application
---

---
product_landing_what_it_offers:
 - title: What it offers
 - message: Unlike models without integration, where each payment must be processed and reconciled manually, integrating Mercado Pago Point into your point of sale transforms your experience.
 - benefit_title: Agility in management
 - benefit_bullet: Manage payments directly from your system.
 - benefit_bullet: Automatically reconcile operations with Mercado Pago.
 - benefit_title: Payment experience
 - benefit_bullet: Offer multiple payment methods and adapt to each buyer.
 - benefit_bullet: Choose whether to offer installments [with](https://www.mercadopago.com.br/ajuda/24694) or [without](/developers/pt/support/oferecer-parcelas-sem-acrescimo-para-compradores_454).
 - benefit_title: Unified API
 - benefit_bullet: Integrate different payment solutions without having to work with several separate APIs.
 - benefit_bullet: Simplify your integration process with Mercado Pago.
 - benefit_title: Efficiency and security
 - benefit_bullet: Optimize your business's performance by automating tasks and reducing errors in collections and reconciliation.
 - benefit_bullet: Protect data involved in transactions using HTTPS protocols and OAuth authentications.
---

---
product_landing_what_differentiates:
 - title: Available terminals
 - message: Below are the terminals that allow you to integrate your business with Mercado Pago Point. If you do not have one, access the [official store](https://www.mercadopago.cl/herramientas-para-vender/lectores-point).
 - columns_amount: 1
 - column_image: https://http2.mlstatic.com/storage/dx-devsite/docs-assets/custom-upload/2025/5/19/1750364222941-terminalsmart2es.png
 - column_product: Point Smart 2
 - column_button_text: Go to store
 - column_button_link: https://www.mercadopago.cl/herramientas-para-vender/lectores-point
 - line_text: Card payments
 - line_type: text
 - line_values: Debit, credit and prepaid, with chip technology, NFC and magnetic stripe.|
 - line_text: Payments with meal cards and in cash
 - line_type: check
 - line_values: true|
 - line_text: QR code payments
 - line_type: check
 - line_values: true|
 - line_text: Tips
 - line_type: check
 - line_values: true|
---

---
product_landing_how_integrate:
 - title: How to integrate
 - sub_title: Learn the steps you need to follow to integrate Mercado Pago Point.
 - requirement_title: Prerequisites
 - requirement_table_title: Mercado Pago Point Smart terminal
 - requirement_table_list: To offer in-person payments through Point, it is necessary to acquire the machine. If you haven't done so yet, go to the [store](https://www.mercadopago[FAKER][URL][DOMAIN]/herramientas-para-vender/lectores-point).
 - requirement_table_title: Mercado Pago app on your phone
 - requirement_table_list: Along with the machine, it is necessary to have the Mercado Pago app on your phone to log into the terminal. You can download it for [Android](https://play.google.com/store/apps/details?id=com.mercadopago.wallet&hl=es_419) or [iOS](https://apps.apple.com/ar/app/mercado-pago/id925436649) devices.
 - requirement_table_title: Mercado Pago account
 - requirement_table_list: You need to create a user in Mercado Pago or Mercado Libre to have a [seller account](https://www.mercadopago[FAKER][URL][DOMAIN]/hub/registration/landing), either for an [own integration](/developers/en/docs/mp-point/create-application#:~:text=access%20your%20credentials.-,Get,-credentials%20for%20a) or for [third parties](/developers/en/docs/mp-point/create-application#:~:text=a%20personal%20integration-,Get,-credentials%20for%20a).
---
|||column1|||
---
product_landing_how_integrate:
 - list_title: Integration process
 - list_item: [Create your application](/developers/en/docs/mp-point/create-application) from [Your integrations](/developers/panel/app).
 - list_item: [Configure your Point terminal](/developers/en/docs/mp-point/configure-terminal).
 - list_item: [Integrate payment processing](/developers/en/docs/mp-point/payment-processing).
 - list_item: [Configure terminal printing](/developers/en/docs/mp-point/configure-printings).
 - list_item: [Set up your payment notifications](/developers/en/docs/mp-point/notifications).
 - list_item: [Test your integration](/developers/en/docs/mp-point/integration-test).
 - list_item: [Go to production](/developers/en/docs/mp-point/go-to-production).
 - button_description: I want to start integrating
 - button_link: /developers/en/docs/mp-point/create-application
---
|||column2|||
<div class="mermaid-overview">
  <pre class="mermaid">
  flowchart TD
  A[Create your application from Your integrations] --> B[Configure your Point terminal]
  B --> C[Integrate payment processing]
  C --> D[Configure terminal printing]
  D --> E[Set up your payment notifications]
  E --> F[Test your integration]
  F --> G[Go to production]
  </pre>
</div>
|||

# Create application

**Applications** are registered entities within Mercado Pago that act as a unique identifier for managing the authentication and authorization of your integrations. They represent the link between your development and Mercado Pago and constitute the first stage in carrying out the integration.

To create an application, you have three options available: with an **AI agent from your code editor**, with the **Mercado Pago Developers Assistant**, or **manually from the** [integration Panel](/developers/panel/app).

![Three options to create an application](/images/snippets/create-application/new-create-app-onboarding-es.png)

:::::TabsComponent
::::TabComponent{title="Create with AI"}

You can use our AI resources to create your application from your IDE or agent in 2 steps. The agent will take care of creating the application in the integration panel and guiding you through the entire configuration.

![Installing the Mercado Pago plugin](/images/snippets/create-application/new-create-app-ia-v2-es.png)

To do this, you have two options: installing the [Mercado Pago Plugin](/developers/en/docs/mp-plugin/overview), available for Claude Code and Codex, or configuring the [Mercado Pago MCP Server](/developers/en/docs/mcp-server/overview), available for editors such as VS Code and Cursor. Follow the instructions for the option you choose.

:::AccordionComponent{title="Plugin"}

### Claude Code

Run the following command to install the Mercado Pago plugin for Claude Code.

```bash
claude plugin install mercadopago@claude-plugins-official
```

Once installed, run the `/mp-connect` command to authorize the agent's access to your Mercado Pago account.

### Codex

Run the following commands to install the Mercado Pago plugin for Codex.

```bash
codex plugin marketplace add mercadopago/mercadopago-codex-marketplace
codex plugin add mercadopago@mercadopago-codex-marketplace
```

Once installed, run the `/mp-connect` command to authorize the agent's access to your Mercado Pago account.

:::

:::AccordionComponent{title="MCP"}

### VS Code

Add the following configuration to your `mcp.json` file.

```json
{
  "mcp": {
  "servers": {
  "mercadopago-mcp-server": {
  "type": "http",
  "url": "https://mcp.mercadopago.com/mcp"
  }
  }
  }
}
```

### Cursor

Add the following configuration to your `mcp.json` file.

```json
{
  "mcpServers": {
  "mercadopago-mcp-server": {
  "url": "https://mcp.mercadopago.com/mcp"
  }
  }
}
```

:::

Finally, ask the agent to create your application in Mercado Pago. If you'd like, you can copy and paste the following prompt.

```
I want to integrate with Mercado Pago. Recommend the ideal payment solution for my project, create the application, and guide me through the integration.
```

> NOTE
>
> You can complete the integration with AI support. If you need help, check the [Integrate with AI guide](/developers/en/docs/ai-resources).

::::
::::TabComponent{title="Create with the Assistant"}

You can use the **Mercado Pago Developers Assistant to create your application** conversationally and easily, without navigating through forms. To do this, follow the steps below.

1. Go to [Mercado Pago Developers](https://www.mercadopago[FAKER][URL][DOMAIN]/developers) and log in with your account.
2. In the bottom right corner of the screen, you'll see the **Assistant** widget. Click to open it.
3. From there, you can simply ask the Assistant to create your application conversationally, meaning you tell it you want to create an application and interact with the questions and answers.
3. Next, the Assistant will ask you to provide a series of details to complete the setup:
  - **Application name**: provide a name that lets you identify your integration. It accepts a maximum of 100 characters.
  - **Product to integrate**: from the list of all Mercado Pago payment solutions shown by the Assistant, select the one that best fits your business.
4. Finally, when the Assistant confirms your application has been created, it will show you the **App ID**, the **Product ID**, and the **integration type**, if applicable.

> NOTE
>
> Once your application is created, the Assistant can help you obtain test credentials, production credentials, or configure Webhooks, as well as suggest how to carry out your integration based on your stack.

::::
::::TabComponent{title="Create manually"}

If you prefer, you can **create your application manually** from the [integration Panel](/developers/panel/app) by following the steps below.

![Mercado Pago Developers panel](/images/snippets/create-application/new-create-app-panel1-v2-es.png)

1. Go to [Mercado Pago Developers](https://www.mercadopago[FAKER][URL][DOMAIN]/developers) with your Mercado Pago account.

2. On the home screen, select the **Create in the integration panel** option.

  > NOTE
  >
  > If you already have applications created, go to **Your integrations** and click **Create application**.

3. In **Choose a solution to integrate**, select **Mercado Pago Point**.
4. In **Other information**, enter an **Application name** that lets you identify it.
5. Accept the [Privacy Statement](https://www.mercadopago[FAKER][URL][DOMAIN]/privacidad) and the [Terms and Conditions](/developers/en/docs/resources/legal/terms-and-conditions) and click **Create application**.

![Application creation form (Mercado Pago Point)](/images/snippets/create-application/new-create-app-panel2-other-es.png)

::::
:::::

In [Your integration](/developers/panel/app), you will be able to view the list of all your created applications and access the [Integration data](/developers/en/docs/mp-point/resources/application-details) for each of them.

> NOTE
>
> If you wish, you can edit or delete an application. In the latter case, keep in mind that your store will lose the ability to use our resources or receive payments through the Mercado Pago integration associated with that application. For more information, please refer to the [Integration data](/developers/en/docs/mp-point/resources/application-details).

## Access test credentials

After creating your application, the :toolTipComponent[test credentials]{link="/developers/en/docs/mp-point/resources/credentials" linkText="Credentials" content="Unique access keys that we use to identify an integration in your account, linked to your application. For more information, access the link below."} will be automatically generated. You should use them to perform all the necessary configurations and validations in a secure test environment. If, instead, you are using an existing application, it will be necessary to [activate the test credentials](/developers/en/docs/mp-point/resources/credentials).

When accessing these credentials, the following keys will be displayed: :toolTipComponent[Public Key]{content="Public key that is used in the frontend to access information and encrypt data. You can access it through Your integrations > Integration data > Tests > Test credentials."} and the test :toolTipComponent[Access Token]{content="Private key of the application created in Mercado Pago, which is used in the backend. You can access it through Your integrations > Integration data > Tests > Test credentials."}. The test Access Token starts with the prefix `APP_USR`, just like your production Access Token.

![test credentials](/images/qr-orders/credentials-test-panel-en-v1.png) 

If you are using an existing application, it will be necessary to activate the test credentials. For more information, access the [Credentials](/developers/en/docs/mp-point/resources/credentials) documentation. 

To develop your Mercado Pago Point integration, use your :toolTipComponent[test Access Token]{content="Private key of the application created in Mercado Pago, which is used in the backend. You can access it through Your integrations > Integration data > Tests > Test credentials. During integration, use the test Access Token and, upon completion, replace it with the production Access Token if it is your own integration, or with the Access Token obtained through OAuth in the case of third-party integrations. The test Access Token starts with the prefix `APP_USR`."}.

> WARNING
>
> If you are integrating the Mercado Pago Point on behalf of a third party, it is recommended to use the **test Access Token** throughout the entire development and testing of the integration. Before [going to production](/developers/en/docs/mp-point/go-to-production), you will need to obtain a production Access Token through the OAuth protocol (using the [Authorization code flow](/developers/en/docs/security/oauth/creation#bookmark_authorization_code)) and replace it.

Once you have obtained the necessary credentials, you can proceed with terminal configuration.

# Configure terminal

To continue with the integration of Mercado Pago Point to your system, after [having created your application](/developers/en/docs/mp-point/create-application) and obtained the appropriate credentials, it is necessary to configure your Point terminal to operate in integrated mode.

This configuration ensures that payments made on the terminals can be managed from your system, optimizing efficiency in reconciliation and task management.

To configure your Point terminal in integrated mode, you must first **create and configure a store and a point of sale**, and then **associate that terminal to the created store and point of sale**. This allows each reader to be linked not only to a Mercado Pago account, but also to a physical point of sale identified in our system.

Finally, with your terminal already linked, you must **activate its operating mode as Point of Sale (PDV)**. Follow the instructions below to correctly perform each step.

:::::AccordionComponent{title="Create and configure store and point of sale" pill="1"} 

Creating stores and points of sale in Mercado Pago is necessary to operate in physical stores with Point terminals and thus maintain reconciliation between your point of sale and Mercado Pago.

A **store** represents a physical store within Mercado Pago, which can have one or more associated points of sale. However, **each point of sale only allows one associated terminal in PDV mode**. This means that if you want to integrate more than one terminal, you must create the same number of points of sale and perform their association individually.

The creation and subsequent configuration of stores and points of sale can be done through two ways: through the Mercado Pago panel, or via API. The latter option is useful for systems that need to operate with multiple points of sale, as it allows associating multiple stores from the integrating system.

Choose the way that best suits your needs and follow the detailed steps as appropriate.

::::TabsComponent

:::TabComponent{title="API"}
It is possible to create stores and points of sale from your system through our APIs for in-person payments. To do this, follow the steps below.

### Create store

To create a store via API, send a request with the :toolTipComponent[test Access Token]{link="/developers/en/docs/mp-point/create-application#bookmark_access_test_credentials" linkText="Access test credentials" content="Private key of the application created in Mercado Pago, used in the backend during integration development. You can access it in Your integrations > Integration data > Tests > Test credentials. When going to production, replace it with the production Access Token if it is your own integration, or with the Access Token obtained via OAuth in the case of third-party integrations. The test Access Token starts with the prefix `APP_USR`."} to the endpoint :TagComponent{tag="POST" text="/users/{user_id}/stores" href="/developers/en/reference/in-person-payments/point/stores/create-store/post" color="green"}. You must add the :toolTipComponent[test account `user_id`]{content="During development, use the User ID from the test account. Go to Your integrations > Integration data > Test credentials > Test credentials data and copy the displayed User ID. When going to production, replace it with the User ID from the real Mercado Pago account that will receive the payments."} in the path of your request and complete the required parameters with the business details as indicated below.

> WARNING
>
> It is essential to correctly fill in all store location information (`city_name`, `state_name`, `latitude` and `longitude`). Incorrect data can cause errors in tax calculations, directly impacting billing and fiscal compliance of your company.

```curl
curl -X POST \
  'https://api.mercadopago.com/users/{{USER_ID}}/stores'\
  -H 'Content-Type: application/json' \
  -H 'Authorization: Bearer {{YOUR_ACCESS_TOKEN}}' \
  -d '{
  "name": "Instore Store",
  "business_hours": {
  "monday": [
  {
  "open": "08:00",
  "close": "12:00"
  }
  ],
  "tuesday": [
  {
  "open": "09:00",
  "close": "18:00"
  }
  ]
  },
  "external_id": "SUC001",
  "location": {
  "street_number": "0123",
  "street_name": "Example Street Name.",
  "city_name": "City name.",
  "state_name": "State name.",
  "latitude": 27.175193925922862,
  "longitude": 78.04213533235064,
  "reference": "Near to Mercado Pago"
  }
}'
```

| Parameter | Requirement | Description and examples |
|-------------|------------|-----------------------|
| `user_id` | Required| Identifier of the Mercado Pago account that receives the money for sales made at the store.<br><br>During development, use the `user_id` from the test account, available in **Your integrations > Integration data > Test credentials > Test credentials data**.<br><br>When going to production, replace it with the `user_id` from the real account that will receive payments: If you are performing your :toolTipComponent[own]{content="Mercado Pago Point integrations to your system for your own use and configured using your application's credentials."} integration, you will find this value in the [Integration data](/developers/en/docs/mp-point/resources/application-details). If, on the other hand, you are performing an integration :toolTipComponent[for third parties]{content="Mercado Pago Point integrations to your system on behalf of a seller and configured using credentials obtained through the OAuth security protocol."}, you will obtain the value in the response to :toolTipComponent[linking through OAuth]{link="/developers/en/docs/mp-point/resources/security/landing-hub" linkText="OAuth" content="Private key generated through the OAuth security protocol, which allows managing integrations on behalf of third parties. For more information, go to the documentation."}. |
| `name` | Required| Name of the created store. |
| `external_id` | Optional | External identifier of the store for the integrator's system. It can contain any alphanumeric value up to 60 characters, and must be unique for each store. For example, `SUCMercadoPago`. |
| `location` | Required| This object must contain all data relating to the store location. You must pay particular attention to completing them correctly with the simple decimal standard, especially the `latitude` and `longitude` parameters, with the real data of the physical location. For example, `"latitude": 27.175193925922862`, and `"longitude": 78.04213533235064` correspond to the exact location of the Taj Mahal, in India. |

If the request was sent correctly, the response will look like the example below.

```json
{
  "id": 1234567,
  "name": "Instore Store",
  "date_created": "2019-08-08T19:29:45.019Z",
  "business_hours": {
  "monday": [
  {
  "open": "08:00",
  "close": "12:00"
  }
  ],
  "tuesday": [
  {
  "open": "09:00",
  "close": "18:00"
  }
  ]
  },
  "location": {
  "address_line": "Example Street Name, 0123, City name, State name.",
  "latitude": 27.175193925922862,
  "longitude": 78.04213533235064,
  "reference": "Near to Mercado Pago"
  },
  "external_id": "SUC001"
}
```

In addition to the data sent in the request, it will return the identifier assigned to that store by Mercado Pago under the id parameter.

### Create point of sale

To be able to make sales with Mercado Pago, each created store must contain at least one associated point of sale. It is possible to create a point of sale and associate it with the previously created store by sending a request with the :toolTipComponent[test Access Token]{link="/developers/en/docs/mp-point/create-application#bookmark_access_test_credentials" linkText="Access test credentials" content="Private key of the application created in Mercado Pago, used in the backend during integration development. You can access it in Your integrations > Integration data > Tests > Test credentials. When going to production, replace it with the production Access Token if it is your own integration, or with the Access Token obtained via OAuth in the case of third-party integrations. The test Access Token starts with the prefix `APP_USR`."} to the endpoint :TagComponent{tag="POST" text="/v2/pos" href="/developers/en/reference/in-person-payments/point/pos/create-pos/post" color="green"} as shown below.

```curl
curl -X POST \
  'https://api.mercadopago.com/v2/pos'\
  -H 'Content-Type: application/json' \
  -H 'Authorization: Bearer {{YOUR_ACCESS_TOKEN}}' \
  -H 'X-Idempotency-Key: {{SOME_UNIQUE_VALUE}}' \
  -d '{
  "name": "POS-001",
  "store_id": "1234567",
  "external_id": "SUC001POS001"
}'
```

| Parameter | Requirement | Description and examples |
|-------------------|------------|-----------------------|
| `name` | Optional | Name of the created point of sale. |
| `store_id` | Conditional | Identifier of the store to which the point of sale belongs, assigned to that store by Mercado Pago. It is returned in the response to the store creation under the `id` parameter. Required if `external_store_id` is not provided. If both are sent, they must refer to the same store. |
| `external_store_id` | Conditional | External identifier of the store, which was assigned by the integrator's system at the time of its creation under the `external_id` parameter. Required if `store_id` is not provided. If both are sent, they must refer to the same store. |
| `external_id` | Optional | External identifier of the point of sale, defined for the integrator system. It must be a unique value for each point of sale and has a limit of 40 characters. |

If the request was sent correctly, the response will look like the example below.

```json
{
  "id": 1234567,
  "name": "POS-001",
  "status": "active",
  "date_created": "2024-01-15T10:30:00Z",
  "date_last_updated": "2024-01-15T10:30:00Z",
  "user_id": 123456,
  "store_id": "1234567",
  "external_store_id": "SUC001",
  "external_id": "SUC001POS001",
  "qr_response": {
  "uuid": "0977011a027c4b4387e52069da4264deae2946af4dcc44ee98a8f1dbb376c8a1",
  "image": "https://www.mercadopago.com/instore/merchant/qr/1234567/abc123.png",
  "template_document": "https://www.mercadopago.com/instore/merchant/qr/1234567/template_abc123.pdf",
  "template_image": "https://www.mercadopago.com/instore/merchant/qr/1234567/template_abc123.png",
  "qr_code": "00020101021226940014BR.GOV.BCB.PIX2572pix-qr-h.mercadopago.com/instore/h/p/v2/abc123"
  }
}
```

You can see in the table below the description of some of the returned parameters that may be useful for continuing with your integration later.

| Parameter | Description |
|-------------------|-------------|
| `id` | Identifier assigned to the point of sale by Mercado Pago. |
| `status` | Status of the point of sale creation. |
| `user_id` | Identifier of the Mercado Pago account that receives the money for sales made at the point of sale. |
| `name` | Name assigned to the point of sale at the time of its creation. |
| `store_id` | Identifier of the store to which the point of sale belongs, assigned to that store by Mercado Pago. It is returned in the response to the store creation under the `id` parameter. |
| `external_store_id` | External identifier of the store, which was assigned by the integrator's system at the time of its creation under the `external_id` parameter. |
| `external_id` | External identifier of the point of sale, defined for the integrator system at the time of its creation. |
| `qr` | Object that will contain a QR code associated with the created point of sale. It can only be used if you have integrated the [QR Code](/developers/en/docs/qr-code/overview) payment solution. |

> NOTE
>
> Remember that it is only possible to configure one terminal in PDV mode per point of sale. If you want to integrate multiple terminals, you must create a point of sale for each one of them.

If both requests were successful, you will have created and configured the store and point of sale necessary to continue with the configuration of your terminal in PDV mode.

:::
:::TabComponent{title="Mercado Pago Panel"}
Creating stores and points of sale through the Mercado Pago Panel is the option for those who only need to manage one point of sale and prefer to simplify the process. To do this, log into your [Mercado Pago account](https://www.mercadopago[FAKER][URL][DOMAIN]/home), and follow the instructions below.

1. In the left side menu, go to **Your business > Stores and points of sale**.
2. In the "Store list" section, click the **+ Add store** button.
3. Complete the **Name** and **Address** of your new store, optionally add **Extra data**, if you need more detail, and click **Continue**.
4. Complete the required information with the **store operating hours**, selecting the days and opening hours. When finished, click **Continue**.

> SUCCESS_MESSAGE
>
> The options available on this screen adapt to multiple scenarios. It will allow you to select a single schedule for all days of the week, or a different schedule for each one, along with the possibility of entering special schedules for holidays. Choose the option that best suits your store.

5. Next, you will be on the screen to **create points of sale** associated with the store, where you must assign a **Name**. If you wish, you can create more than one point of sale.

> NOTE
>
> Remember that it is only possible to configure one terminal in PDV mode per point of sale. If you want to integrate multiple terminals, you must create a point of sale for each one of them.

6. Click the **Continue** button, and you're done! You have created and configured your store and your point of sale.

:::
::::
:::::
:::AccordionComponent{title="Associate terminal" pill="2"}

The association of the Point terminal to the Mercado Pago account and the created store and point of sale must be performed from the Mercado Pago application on the **mobile device of the receiving account or the one indicated as a collaborator**. This application is available for Android or iOS devices.

Start by turning on the Point terminal. You will see the message "**Log in to this device with your Mercado Pago account**" on the screen. There you must choose between the options below.

- **I am the business owner**: select this option if you are the owner of the physical store.
- **I am a collaborator**: choose this option if your account was designated as a collaborator account by the store owner.

Once you have selected the appropriate option, a QR code will appear on the terminal screen, which you must scan with the Mercado Pago mobile application.

To do this, access the application and log in with the test seller account, whose username and password are available in **Your integrations > Integration data > Test credentials > Test credentials information**. Then, press the **QR icon** at the bottom and scan the code presented by the terminal.

> NOTE
>
> In the [Go to production](/developers/en/docs/mp-point/go-to-production) stage, you must repeat this association process using the receiving account or the one designated as a collaborator account, as appropriate.

After a few seconds, the Point terminal may request some additional configurations for the store. Follow the instructions displayed on the screen to complete all stages.

The terminal will ask you to select the store and point of sale to which you want to associate the terminal, and confirm the address of the store previously created with your Mercado Pago account. When finished, press the **Confirm** button.

> NOTE
>
> If, for some reason, you have more than one store created, make sure you are correctly selecting the one you want to integrate with your Point terminal.

Finally, the terminal will ask you to enter a password that will ensure its safe use.

Once this process is finished, the screen will display the message "Ready! You can now charge with your Point", and you will have finished associating your terminal to the desired Mercado Pago account, and to the created store and point of sale.

:::
:::AccordionComponent{title="Activate PDV mode on the terminal" pill="3"} 

As the last step in terminal configuration, and for them to be integrated with our API, it is necessary to activate the Point of Sale (PDV) operating mode.

To activate PDV mode via API for the first time, you need to query the available active terminals in your account. To do so, send a request to the endpoint :TagComponent{tag="GET" text="/terminals/v1/list" href="/developers/en/reference/in-person-payments/point/terminals/get-terminals/get" color="accent"}, using the :toolTipComponent[test Access Token]{link="/developers/en/docs/mp-point/create-application#bookmark_access_test_credentials" linkText="Access test credentials" content="Private key of the application created in Mercado Pago, used in the backend during integration development. You can access it in Your integrations > Integration data > Tests > Test credentials. When going to production, replace it with the production Access Token if it is your own integration, or with the Access Token obtained via OAuth in the case of third-party integrations. The test Access Token starts with the prefix `APP_USR`."}. We recommend optionally using the `store_id` and `pos_id` parameters to filter the results; these identifiers are returned when creating the store and point of sale, respectively.

```curl
curl -X GET \
  'https://api.mercadopago.com/terminals/v1/list?limit=50&offset=0&store_id={{STORE_ID}}&pos_id={{POS_ID}}'\
  -H 'Content-Type: application/json' \
  -H 'Authorization: Bearer {{YOUR_ACCESS_TOKEN}}'
```

This call will return a list of terminals linked to the Mercado Pago account, along with their respective associated point of sale and store, and their operating mode.

```json
{
  "data": {
  "terminals": [
  {
  "id": "NEWLAND_N950__N950NCB801293324",
  "pos_id": "23545678",
  "store_id": "12354567",
  "external_pos_id": "SUC0101POS",
  "operating_mode": "PDV | STANDALONE | UNDEFINED"
  }
  ]
  },
  "paging": {
  "total": 1,
  "offset": 0,
  "limit": 50
  }
}
```

| Parameter | Description |
|-------------------------|-------------|
| `terminals.id` | Unique identifier of the terminal. The format in which this field is returned is **"terminal type + "__" + terminal serial"**. For example, "NEWLAND_N950__N950NCB801293324". You can identify the Point you want through the last characters of this field, which should match the serial that appears on the back label of the physical terminal. |
| `terminals.pos_id` | Identifier of the point of sale to which the Point terminal is associated. |
| `terminals.store_id` | Identifier of the store to which the Point terminal is associated. |
| `terminals.operating_mode`| Operating mode in which the terminal is functioning at the time of the query. It can be: <br><br> - **PDV**: Point of Sale (PDV) operating mode. This is the mode in which the terminal operates when integrated via API and can only receive card payments. <br> - **STANDALONE**: default terminal configuration. This is the mode in which it operates when **not** integrated via API. <br> - **UNDEFINED**: the configuration that the terminal has is not recognized. |

Since the only operating mode that allows integrating terminals via API is PDV, once you have located the desired Point terminal, you must activate it. To do this, send a request with the :toolTipComponent[test Access Token]{link="/developers/en/docs/mp-point/create-application#bookmark_access_test_credentials" linkText="Access test credentials" content="Private key of the application created in Mercado Pago, used in the backend during integration development. You can access it in Your integrations > Integration data > Tests > Test credentials. When going to production, replace it with the production Access Token if it is your own integration, or with the Access Token obtained via OAuth in the case of third-party integrations. The test Access Token starts with the prefix `APP_USR`."} to the endpoint :TagComponent{tag="PATCH" text="/terminals/v1/setup" href="/developers/en/reference/in-person-payments/point/terminals/update-operation-mode/patch" color="gray"}, as shown below.

> NOTE
>
> If in the response to the query you find that the terminal you want to process integrated payments with already has PDV mode activated, you do not need to make this request and can continue with [Payment processing](/developers/en/docs/mp-point/payment-processing). Additionally, if you have already performed the API activation of PDV mode on a terminal, and for some reason you need to configure it again, you can do it directly from the reader, going to **More options > Settings > Pairing mode**.

```curl
curl -X PATCH \
  'https://api.mercadopago.com/terminals/v1/setup'\
  -H 'Content-Type: application/json' \
  -H 'Authorization: Bearer {{YOUR_ACCESS_TOKEN}}' \
  -d '{
  "terminals": [
  {
  "id": "NEWLAND_N950__N950NCB801293324",
  "operating_mode": "PDV"
  }
  ]
}'
```

| Field | Type | Description |
|------------------------|--------|-------------|
| `terminals.id` | String | Unique identifier of the terminal whose operating mode you want to modify, obtained in the request to query available terminals. You must send it following the format **"terminal type + "__" + terminal serial"**, as in the following example: "NEWLAND_N950__N950NCB801293324". |
| `terminals.operating_mode` | String | Operating mode in which you want to configure the terminal. To integrate your terminal via API, the value must be `PDV`, which corresponds to the Point of Sale operating mode. |

If the request was successful, the response should return the parameter `operating_mode=PDV`.

```json
{
  "terminals": [
  {
  "id": "NEWLAND_N950__N950NCB801293324",
  "operating_mode": "PDV"
  }
  ]
}
```

> NOTE
>
> Remember that it is only possible to configure one terminal in PDV mode per point of sale. If you want to integrate multiple terminals, you must create a point of sale for each one of them.

To finish configuring your terminal, you must restart it and then verify that it has been applied by going to **More options > Settings > Pairing mode**. If you find that the pairing mode is **Point of Sale (PDV)**, the change in operating mode was effective and you can continue integrating payment processing.
:::

# Integrate payment processing

Payment processing with Mercado Pago Point integrated into your point of sale is based on creating orders that have an associated payment transaction. When an order is created, it will be automatically loaded to the specified terminal, and the buyer will be able to make the payment in person.

Integrated payment processing with Mercado Pago Point will allow you to create orders, process them, cancel them, or make refunds and query their information or status updates.

> NOTE
>
> If you want the installments set to be [with](https://www.mercadopago.cl/ayuda/24694) or [without](/developers/es/support/3299) interests in credit card transactions, before creating an order, you must **set them up in your Mercado Pago account**.

:::::AccordionComponent{title="Create an order"}

To start processing payments with Point from points of sale, you first need to identify which terminal you want to assign the order to. Remember that this terminal must be :TagComponent{tag="PATCH" text="set to PDV mode" href="/developers/en/reference/in-person-payments/point/terminals/update-operation-mode/patch" color="gray"}.

For this, send a request to the endpoint :TagComponent{tag="GET" text="Get list of terminals" href="/developers/en/reference/in-person-payments/point/terminals/get-terminals/get" color="accent"}, using your :toolTipComponent[test Access Token]{link="/developers/en/docs/mp-point/create-application#bookmark_access_test_credentials" linkText="Access test credentials" content="Private key of the application created in Mercado Pago, used in the backend during integration development. You can access it in Your integrations > Integration data > Tests > Test credentials. When going to production, replace it with the production Access Token if it is your own integration, or with the Access Token obtained via OAuth in the case of third-party integrations. The test Access Token starts with the prefix `APP_USR`."}.

If necessary, you can filter the search using the optional query params `store_id` and `pos_id`, which correspond to the store and box identifiers returned in the response to the creation of each one.

```curl
curl -X GET \
  'https://api.mercadopago.com/terminals/v1/list?limit=50&offset=0&store_id=12354567&pos_id=23545678' \
  -H 'Content-Type: application/json' \
  -H 'Authorization: Bearer {{YOUR_ACCESS_TOKEN}}'
```

The response to this request will show the terminals associated with your account, allowing you to select the one you want to use to create your order.

The terminal can be identified by the last characters of the `id` field, which correspond to the serial number printed on the back label of the physical terminal.

```json
{
  "data": {
  "terminals": [
  {
  "id": "NEWLAND_N950__N950NCB801293324",
  "pos_id": "23545678",
  "store_id": "12354567",
  "external_pos_id": "SUC0101POS",
  "operating_mode": "PDV"
  }
  ]
  },
  "paging": {
  "total": 1,
  "offset": 0,
  "limit": 50
  }
}
```

Then, you'll need to create the order. For this, send a request to the endpoint :TagComponent{tag="POST" text="/v1/orders" href="/developers/en/reference/in-person-payments/point/orders/create-order/post" color="green"}, making sure to include your :toolTipComponent[test Access Token]{link="/developers/en/docs/mp-point/create-application#bookmark_access_test_credentials" linkText="Access test credentials" content="Private key of the application created in Mercado Pago, used in the backend during integration development. You can access it in Your integrations > Integration data > Tests > Test credentials. When going to production, replace it with the production Access Token if it is your own integration, or with the Access Token obtained via OAuth in the case of third-party integrations. The test Access Token starts with the prefix `APP_USR`."}, and the ID of the terminal to which you want to assign the order, obtained in the previous step.

```curl
curl -X POST \
  'https://api.mercadopago.com/v1/orders' \
  -H 'Content-Type: application/json' \
  -H 'X-Idempotency-Key: {{SOME_UNIQUE_VALUE}}' \
  -H 'Authorization: Bearer {{YOUR_ACCESS_TOKEN}}' \
  -d '{
  "type": "point",
  "external_reference": "ext_ref_1234",
  "expiration_time": "PT16M",
  "transactions": {
  "payments": [
  {
  "amount": "24"
  }
  ]
  },
  "config": {
  "point": {
  "terminal_id": "NEWLAND_N950__N950NCB801293324",
  "print_on_terminal": "no_ticket"
  }
  },
  "description": "Point Smart 2",
  "integration_data": {
  "platform_id": "dev_1234567890",
  "integrator_id": "dev_1234567890",
  "sponsor": {
  "id": "446566691"
  }
  },
  "taxes": [
  {
  "payer_condition": "payment_taxable_iva"
  }
  ]
  }'
```

Check the table below for descriptions of parameters that have some important particularity that should be highlighted.

| Attribute | Type | Description | Required |
|---|---|---|---|
| `Authorization` | Header | Refers to the :toolTipComponent[test Access Token]{link="/developers/en/docs/mp-point/create-application#bookmark_access_test_credentials" linkText="Access test credentials" content="Private key of the application created in Mercado Pago, used in the backend during integration development. You can access it in Your integrations > Integration data > Tests > Test credentials. When going to production, replace it with the production Access Token if it is your own integration, or with the Access Token obtained via OAuth in the case of third-party integrations. The test Access Token starts with the prefix `APP_USR`."}. | Required |
| `X-Idempotency-Key` | Header | Idempotency key. It is used to ensure that each request is processed only once, avoiding duplications. Use a unique value in the header of your request, such as a UUID V4 or random strings. | Required |
| `type` | Body.String | Type of order, associated with the Mercado Pago solution for which it is being created. For payments with Mercado Pago Point, the only possible value is `point`. | Required |
| `external_reference` | Body.String | It is an external reference of the order, assigned at the time of its creation. It must be a unique value for each order and cannot contain PII data. The maximum allowed limit is 64 characters and the allowed ones are: **uppercase and lowercase letters**, **numbers** and **hyphen (-) and underscore (_) symbols**. | Required |
| `expiration_time` | Body. String | Indicates the **validity period** of the payment order from its creation. During this time, the order will be available for processing by the customer; if it is not processed within the specified period, it will automatically expire and cannot be used, requiring the generation of a new payment order to continue. The minimum allowed value is 30 seconds (PT30S) and the maximum is 3 hours (PT3H). Usage examples: for a 30-second expiration: "PT30S", for 10 minutes: "PT10M", and for 1 hour and 15 minutes: "PT1H15M". | Optional |
| `transactions.payments.amount` | Body.String | Total amount of the payment order. Must be an integer, with no decimal places. | Required |
| `config.point.terminal_id` | Body.String | Identifier of the Point terminal that will receive the order. You must send it exactly as it was returned by the :TagComponent{tag="GET" text="Get terminals" href="/developers/en/reference/in-person-payments/point/terminals/get-terminals/get" color="accent"} request, as in the following example: `NEWLAND_N950__N950NCB801293324`. | Required |

> NOTE
>
> To find out more details about all the parameters to be sent in this request, please check our :TagComponent{tag="API" text="API Reference" href="/developers/en/reference/in-person-payments/point/orders/create-order/post"}.

If the request was successful, the response will return an order with status `created`.

```json
{
  "id": "ORD00001111222233334444555566",
  "type": "point",
  "user_id": "5238400195",
  "external_reference": "ext_ref_1234",
  "description": "Point Smart 2",
  "expiration_time": "PT16M",
  "processing_mode": "automatic",
  "country_code": "CHL",
  "integration_data": {
  "application_id": "1234567890",
  "platform_id": "dev_1234567890",
  "integrator_id": "dev_1234567890",
  "sponsor": {
  "id": "446566691"
  }
  },
  "status": "created",
  "status_detail": "created",
  "created_date": "2024-09-10T14:26:42.109320977Z",
  "last_updated_date": "2024-09-10T14:26:42.109320977Z",
  "config": {
  "point": {
  "terminal_id": "NEWLAND_N950__N950NCB801293324",
  "print_on_terminal": "no_ticket"
  },
  "payment_method": {
  "default_type": "credit_card"
  }
  },
  "transactions": {
  "payments": [
  {
  "id": "PAY01J67CQQH5904WDBVZEM4JMEP3",
  "amount": "24",
  "status": "created"
  }
  ]
  },
  "taxes": [
  {
  "payer_condition": "payment_taxable_iva"
  }
  ]
}
```

> NOTE
>
> Since the order is the basis for payment processing, it's important that you save both its ID (`order_id`) and the payment ID (`transactions.payments.id`) obtained when creating it, as they will allow you to perform other operations and properly query your notifications. Additionally, you can consult our documentation in the **Resources section** to better understand the [possible status of an order and a transaction](/developers/en/docs/mp-point/resources/status-order-transaction).

This created order will be automatically received by the terminal to which it was assigned. If the order is not automatically loaded on the terminal, you must press the **Update** button or, if the terminal has one, the **green button** to receive the order. In this way, the buyer can make the payment on the terminal and then it will be processed. **Keep in mind that if you do not fill in the `expiration_time` parameter, the payment must be made within 15 minutes of the order's creation; after that time, the order will expire.**

:::::

:::::AccordionComponent{title="Cancel an order"}
An order can be canceled via API or, when it has `at_terminal` status, directly from the terminal.

> NOTE
>
> To track the cancellation of an order in `at_terminal`, whether requested via API or performed from the terminal, configure your [Webhook notifications](/developers/en/docs/mp-point/notifications) beforehand. The notification confirms that the cancellation took effect and allows you to maintain your reconciliation.

- If the order's `status` is `created`, it must be canceled via API and is processed synchronously.

- If its `status` is `at_terminal`, it has already been retrieved by the terminal. In this case, cancellation can be requested asynchronously via API or performed directly from the terminal.

Choose the option that best suits your needs to learn how to cancel your order.

::::TabsComponent

:::TabComponent{title="Via API"}
To cancel an order with `created` or `at_terminal` status via API, send a request to the :TagComponent{tag="POST" text="/v1/orders/{order_id}/cancel" href="/developers/en/reference/in-person-payments/point/orders/cancel-order/post" color="green"} endpoint, including your :toolTipComponent[test Access Token]{link="/developers/en/docs/mp-point/create-application#bookmark_access_test_credentials" linkText="Access test credentials" content="Private key of the application created in Mercado Pago, used in the backend during integration development. You can access it in Your integrations > Integration data > Tests > Test credentials. When going to production, replace it with the production Access Token if it is your own integration, or with the Access Token obtained via OAuth in the case of third-party integrations. The test Access Token starts with the prefix `APP_USR`."} and the order ID obtained in the response to its creation.

> WARNING
>
> If the `x-allow-cancelable-status` header is omitted or has a value other than `at_terminal`, the API cancellation request for an order with `status=at_terminal` returns the `409 cannot_cancel_order` error.
> <br><br>
> In addition, the feature is available on Point Smart 2 terminals that have their software updated to the latest available version. Otherwise, the request is handled as if the header had not been sent and returns the same error.

```curl
curl -X POST \
  'https://api.mercadopago.com/v1/orders/{{ORDER_ID}}/cancel' \
  -H 'Content-Type: application/json' \
  -H 'X-Idempotency-Key: {{SOME_UNIQUE_VALUE}}' \
  -H 'x-allow-cancelable-status: at_terminal' \
  -H 'Authorization: Bearer {{YOUR_ACCESS_TOKEN}}'
```

The result depends on the order status at the time of the request:

- For `created`, cancellation is synchronous and the API returns `HTTP 200`, with the order in `status=canceled` and the payment in `status_detail=canceled_by_api`. The `x-allow-cancelable-status` header is optional and, when sent, is ignored.
- For `at_terminal`, the API accepts the request asynchronously and returns `HTTP 202`. The order remains in `status=at_terminal`, while the payment changes to `status_detail=cancellation_requested`, until a Webhook notification confirms the cancellation. If the payment is already being processed, the terminal may prioritize it and not complete the cancellation; therefore, the `HTTP 202` response must not be interpreted as final confirmation.

### Response for an order in `created`

```json
{
  "id": "ORD00009999222233334444555566",
  "user_id": "5238400195",
  "type": "point",
  "external_reference": "ext_ref_1234",
  "description": "Point Smart 2",
  "expiration_time": "PT16M",
  "country_code": "CHL",
  "processing_mode": "automatic",
  "integration_data": {
  "application_id": "1234567890",
  "platform_id": "dev_1234567890",
  "integrator_id": "dev_1234567890",
  "sponsor": {
  "id": "446566691"
  }
  },
  "status": "canceled",
  "status_detail": "canceled",
  "created_date": "2024-09-10T14:26:42.109320977Z",
  "last_updated_date": "2024-09-10T14:26:42.109320977Z",
  "config": {
  "point": {
  "terminal_id": "NEWLAND_N950__N950NCB801293324",
  "print_on_terminal": "no_ticket"
  },
  "payment_method": {
  "default_type": "credit_card"
  }
  },
  "transactions": {
  "payments": [
  {
  "id": "PAY01J67CQQH5904WDBVZEM4JMEP4",
  "amount": "24.00",
  "status": "canceled",
  "status_detail": "canceled_by_api"
  }
  ]
  },
  "taxes": [
  {
  "payer_condition": "payment_taxable_iva"
  }
  ]
}
```

### Response for an order in `at_terminal`

```json
{
  "id": "ORD00009999222233334444555566",
  "status": "at_terminal",
  "status_detail": "at_terminal",
  "transactions": {
  "payments": [
  {
  "id": "PAY01J67CQQH5904WDBVZEM4JMEP4",
  "status": "at_terminal",
  "status_detail": "cancellation_requested"
  }
  ]
  }
}
```

The `HTTP 202` response only confirms that the request was accepted. Consider the order canceled only after receiving confirmation through [Webhook notifications](/developers/en/docs/mp-point/notifications).

:::
:::TabComponent{title="From the terminal"}

Since the order is automatically retrieved by the terminal, to cancel it you'll need to exit the screen without completing the charge. To do this, press the **bottom right button** on the terminal.

Then, when asked if you want to exit without finishing, choose the **Yes** option.

Once you finish the cancellation via terminal, and once your [Webhook notifications](/developers/en/docs/mp-point/notifications) are configured, you will receive the notification in your system, which will allow you to maintain your reconciliation.

:::
::::

:::::

:::::AccordionComponent{title="Refund an order"}

If needed, it is possible to refund an order created through our API. This endpoint allows you to make a **total or partial** refund of a payment transaction associated with the order. To request a total refund, you do not need to send a `body` in the request. For a partial refund, you must inform in the `body` the amount to be refunded and the transaction identifier.

> WARNING
>
> Card payment refunds via API can be made **up to 90 days after payment**. For Edenred payments, refunds via API can be made **until 23:59:59 on the same day**, and for Pluxee, within **up to 5 business days** after payment creation.

Choose the option that best suits your needs and follow the corresponding instructions.

::::TabsComponent

:::TabComponent{title="Total refund"}

To make a **total** refund of an order, send a request to the endpoint :TagComponent{tag="POST" text="/v1/orders/{order_id}/refund" href="/developers/en/reference/in-person-payments/point/orders/refund-order/post" color="green"} **without sending a body** in the request. Make sure to include your :toolTipComponent[test Access Token]{link="/developers/en/docs/mp-point/create-application#bookmark_access_test_credentials" linkText="Access test credentials" content="Private key of the application created in Mercado Pago, used in the backend during integration development. You can access it in Your integrations > Integration data > Tests > Test credentials. When going to production, replace it with the production Access Token if it is your own integration, or with the Access Token obtained via OAuth in the case of third-party integrations. The test Access Token starts with the prefix `APP_USR`."}. You must also include the ID of the order (`order_id`) you want to refund, obtained in the response to its creation.

```curl
curl -X POST \
  'https://api.mercadopago.com/v1/orders/{{ORDER_ID}}/refund' \
  -H 'Content-Type: application/json' \
  -H 'X-Idempotency-Key: {{SOME_UNIQUE_VALUE}}' \
  -H 'Authorization: Bearer {{YOUR_ACCESS_TOKEN}}'
```

If the request is successful, the response will return `status=refunded` and a new node `transactions.refunds`, which will contain the details of the refund, along with the original payment ID (`transactions.payments.id`) and the refund transaction ID (`transaction_id`).

```json
{
  "id": "ORD00001111222233334444555566",
  "status": "refunded",
  "status_detail": "refunded",
  "transactions": {
  "refunds": [
  {
  "id": "REF01J67CQQH5904WDBVZEM1234D",
  "transaction_id": "PAY01J67CQQH5904WDBVZEM4JMEP3",
  "reference_id": "12345678",
  "amount": "24.00",
  "status": "processed"
  }
  ]
  }
}
```

:::
:::TabComponent{title="Partial refund"}

To make a **partial** refund of an order, send a request to the endpoint :TagComponent{tag="POST" text="/v1/orders/{order_id}/refund" href="/developers/en/reference/in-person-payments/point/orders/refund-order/post" color="green"}, including in the request **body** the array `transactions` with the payment transaction identifier (`id`) and the amount to be refunded (`amount`). Make sure to include your :toolTipComponent[test Access Token]{link="/developers/en/docs/mp-point/create-application#bookmark_access_test_credentials" linkText="Access test credentials" content="Private key of the application created in Mercado Pago, used in the backend during integration development. You can access it in Your integrations > Integration data > Tests > Test credentials. When going to production, replace it with the production Access Token if it is your own integration, or with the Access Token obtained via OAuth in the case of third-party integrations. The test Access Token starts with the prefix `APP_USR`."}. You should send the fields as indicated in the table below.

> WARNING
>
> Partial refunds are available for payments made with card and QR codes.

```curl
curl -X POST \
  'https://api.mercadopago.com/v1/orders/{{ORDER_ID}}/refund' \
  -H 'Content-Type: application/json' \
  -H 'X-Idempotency-Key: {{SOME_UNIQUE_VALUE}}' \
  -H 'Authorization: Bearer {{YOUR_ACCESS_TOKEN}}' \
  -d '{
  "transactions": [
  {
  "id": "PAY01J67CQQH5904WDBVZEM4JMEP3",
  "amount": "12.45"
  }
  ]
  }'
```

| Attribute | Type | Description | Requirement |
|-|-|-|-|
| `order_id` | String | ID of the order containing the associated payment transaction to be refunded. This value is returned in the response to the [Create an order](/developers/en/docs/mp-point/payment-processing#:~:text=Create%20an%20order-,To,-start%20processing%20payments) request. | Required. |
| `transactions` | Array | Contains information about the transaction associated with the order to be refunded. | Required for partial refunds. |
| `transactions.id` | String | Identifier of the payment transaction created in the request, obtained in the response to the creation of the order (`transactions.payments.id`). | Required for partial refunds. |
| `transactions.amount` | String | Amount to be refunded. You can perform multiple partial refunds, as long as the sum does not exceed the total transaction amount. The value must be an integer number. That is, decimals are not allowed. | Required for partial refunds. |

If the request was successful, the response will show `status=processed` (if there is still balance in the order) and `status_detail=partially_refunded`, along with the `transactions.refunds` node containing the partial refund details.

```json
{
  "id": "ORD01J49MMW3SSBK5PSV3DFR32959",
  "status": "processed",
  "status_detail": "partially_refunded",
  "transactions": {
  "refunds": [
  {
  "id": "REF01J75Z9M6KQ8R3C4V2N7P1TXAB",
  "transaction_id": "PAY01J67CQQH5904WDBVZEM4JMEP3",
  "reference_id": "12345678",
  "amount": "12.45",
  "status": "processed"
  }
  ]
  }
}
```

:::

::::

:::::

:::::AccordionComponent{title="Query order data"}
If needed, you can query the data of an order and its associated transactions, whether payments or refunds, including their statuses or values.

Although the recurring use of this API query **is not recommended**, it can be useful if you need additional information about the order.

To query order data, send a request to the endpoint :TagComponent{tag="GET" text="/v1/orders/{order_id}" href="/developers/en/reference/in-person-payments/point/orders/get-order/get" color="accent"}, making sure to include your :toolTipComponent[test Access Token]{link="/developers/en/docs/mp-point/create-application#bookmark_access_test_credentials" linkText="Access test credentials" content="Private key of the application created in Mercado Pago, used in the backend during integration development. You can access it in Your integrations > Integration data > Tests > Test credentials. When going to production, replace it with the production Access Token if it is your own integration, or with the Access Token obtained via OAuth in the case of third-party integrations. The test Access Token starts with the prefix `APP_USR`."}, and the ID of the order (`order_id`) whose information you want to query, obtained in the response to its creation.

> WARNING
>
> Keep in mind that this request will only allow you to query **orders created less than 3 months ago**. If you need information about older orders, we recommend that you contact our customer service for additional assistance.

```curl
curl -X GET \
  'https://api.mercadopago.com/v1/orders/{{ORDER_ID}}' \
  -H 'Content-Type: application/json' \
  -H 'Authorization: Bearer {{YOUR_ACCESS_TOKEN}}'
```

If the request was successful, the response will return all the order information, including its status and the status of the payment and/or refund in real time:

```json
{
  "id": "ORD00001111222233334444555566",
  "user_id": "5238400195",
  "type": "point",
  "external_reference": "ext_ref_1234",
  "processing_mode": "automatic",
  "description": "Point Smart 2",
  "expiration_time": "PT16M",
  "country_code": "CHL",
  "integration_data": {
  "application_id": "1234567890",
  "platform_id": "dev_1234567890",
  "integrator_id": "dev_1234567890",
  "sponsor": {
  "id": "446566691"
  }
  },
  "status": "refunded",
  "status_detail": "refunded",
  "created_date": "2024-09-10T14:26:42.109320977Z",
  "last_updated_date": "2024-09-10T14:26:42.109320977Z",
  "config": {
  "point": {
  "terminal_id": "NEWLAND_N950__N950NCB801293324",
  "print_on_terminal": "no_ticket"
  },
  "payment_method": {
  "default_type": "credit_card"
  }
  },
  "transactions": {
  "payments": [
  {
  "id": "PAY01J67CQQH5904WDBVZEM4JMEP3",
  "amount": "24.00",
  "refunded_amount": "24.00",
  "paid_amount": "24.00",
  "status": "refunded",
  "status_detail": "refunded",
  "reference_id": "12345678",
  "payment_method": {
  "type": "credit_card",
  "installments": 1,
  "id": "master"
  }
  }
  ],
  "refunds": [
  {
  "id": "REF01J67CQQH5904WDBVZEM1234D",
  "transaction_id": "PAY01J67CQQH5904WDBVZEM4JMEP3",
  "reference_id": "12345678",
  "amount": "24.00",
  "status": "processed"
  }
  ]
  },
  "taxes": [
  {
  "payer_condition": "payment_taxable_iva"
  }
  ]
}
```

:::::

# Configure notifications

**Webhooks** notifications, also known as **web callbacks**, are an effective method that allows Mercado Pago servers to send information in **real time** when a specific event related to your integration occurs. Instead of your system constantly querying for updates, Webhooks allow the passive and automatic transmission of data between Mercado Pago and your integration through an **HTTPS POST** request, optimizing communication and reducing server load.

:::AccordionComponent{title="Configure Webhooks"}

Below, we present a step-by-step guide to receiving payment notifications in integrations with Point. Once configured, Webhook notifications will be sent whenever any update occurs on the reported topic, including the creation and update of orders and transaction processing.

> RED_MESSAGE
>
> If you are developing using test credentials, go to **Your integrations > Integration data > Test credentials > Test credentials data**, log in to [Mercado Pago Developers](/developers/en/docs) with the username and password from that test account, and configure Webhooks in production mode for that account. This way, you will be able to test the notifications correctly.

1. Go to [Your integrations](/developers/panel/app) and select the application integrated with Point for which you want to activate notifications.

![cofigure notifications](/images/api-orders/not1-app-es-v1.png)

2. In the left menu, select **Webhooks > Configure notifications**.

![cofigure notifications](/images/api-orders/not2-configure-es-v1.png)

3. Select the **Production mode** tab and provide an `HTTPS URL` to receive notifications with your productive integration.

![cofigure notifications](/images/api-orders/not3-url-es-v1.png)

4. Select the **Order (Mercado Pago)** event to receive notifications, which will be sent in `JSON` format via an `HTTPS POST` to the URL specified above.

![cofigure notifications](/images/api-orders/not4-order-es-v1.png)

5. Finally, click on **Save configuration**. This will generate an exclusive secret key for the application, which will allow you to validate the authenticity of the received notifications, ensuring that they were sent by Mercado Pago. Keep in mind that this generated key does not have an expiration date and its periodic renewal is not mandatory, although it is recommended. To do this, simply click the **Reset** button.

Once completed, your Webhooks notifications for Mercado Pago Point will be configured and you will be able to receive the following alerts about the order:

- **Processed** (`order.processed`)
- **Canceled** (`order.canceled`)
- **Refunded** (`order.refunded`)
- **Requires confirmation on the terminal** (`order.action_required`)
- **Failed** (`order.failed`)
- **Expired** (`order.expired`)

:::

:::::AccordionComponent{title="Simulate receiving the notification"}

To ensure that notifications are configured correctly, it is necessary to simulate their reception. To do this, follow the steps below.

1. After configuring your Webhooks, click **Simulate notification**.
2. On the simulation screen, select the URL to be tested.
3. Next, choose the **event type** and enter the **ID** that will be sent in the notification body (`Data ID`).

![cofigure notifications](/images/api-orders/not5-order-es-v2.png)

4. Finally, click on **Send test** to verify the request, the response provided by the server, and the event description. You will receive a response as shown in the examples below, representing the body of the notification received on your server.

::::TabsComponent

:::TabComponent{title="Processed"}

```json
{
  "action": "order.processed",
  "api_version": "v1",
  "application_id": "123456",
  "data": {
  "external_reference": "ext_ref_1235",
  "id": "ORD01JYH1Z1YJN4HZ8J3Q0RB3YP6D",
  "status": "processed",
  "status_detail": "accredited",
  "total_paid_amount": "120",
  "transactions": {
  "payments": [
  {
  "amount": "120",
  "id": "PAY01K22Y503EJ8JHGF64KGY1PZ2B",
  "paid_amount": "120",
  "payment_method": {
  "id": "debvisa",
  "installments": 1,
  "type": "debit_card"
  },
  "reference": {
  "id": "123456789980"
  },
  "status": "processed",
  "status_detail": "accredited",
  "tip_amount": "10"
  }
  ]
  },
  "type": "point",
  "version": 3
  },
  "date_created": "2025-08-07T18:54:40.851374414Z",
  "live_mode": true,
  "type": "order",
  "user_id": "123456"
} 
```

:::
:::TabComponent{title="Canceled"}
```json
{
  "action": "order.canceled",
  "api_version": "v1",
  "application_id": "123456",
  "data": {
  "external_reference": "ext_ref_1234",
  "id": "ORD01JYH1Z1YJN4HZ8J3Q0RB3YP6D",
  "status": "canceled",
  "status_detail": "canceled",
  "transactions": {
  "payments": [
  {
  "amount": "120",
  "id": "PAY01K22Y503EJ8JHGF64KGY1PZ2B",
  "status": "canceled",
  "status_detail": "canceled_on_terminal"
  }
  ]
  },
  "type": "point",
  "version": 3
  },
  "date_created": "2025-08-07T19:30:44.741479284Z",
  "live_mode": true,
  "type": "order",
  "user_id": "123456"
}
```
:::
:::TabComponent{title="Requires confirmation on terminal"}
```json
{
  "action": "order.action_required",
  "api_version": "v1",
  "application_id": "123456",
  "data": {
  "external_reference": "ext_ref_1234",
  "id": "ORD01JYH1Z1YJN4HZ8J3Q0RB3YP6D",
  "status": "action_required",
  "status_detail": "check_on_terminal",
  "type": "point",
  "version": 3
  },
  "date_created": "2025-06-24T13:28:36.44747706Z",
  "live_mode": false,
  "type": "order",
  "user_id": "123456"
}
```
:::
:::TabComponent{title="Failed"}
```json
{
  "action": "order.failed",
  "api_version": "v1",
  "application_id": "123456",
  "data": {
  "external_reference": "ext_ref_1234",
  "id": "ORD01K23219YK26BC6GK0HASE8VT6",
  "status": "failed",
  "status_detail": "failed",
  "transactions": {
  "payments": [
  {
  "amount": "120",
  "id": "PAY01K22Y503EJ8JHGF64KGY1PZ2B",
  "payment_method": {
  "id": "debvisa",
  "installments": 1,
  "type": "debit_card"
  },
  "reference": {
  "id": "123456789980"
  },
  "status": "failed",
  "status_detail": "bad_filled_card_data"
  }
  ]
  },
  "type": "point",
  "version": 3
  },
  "date_created": "2025-08-07T20:03:04.897928692Z",
  "live_mode": true,
  "type": "order",
  "user_id": "123456"
}
```
:::
:::TabComponent{title="Expired"}
```json
{
  "action": "order.expired",
  "api_version": "v1",
  "application_id": "123456",
  "data": {
  "external_reference": "ext_ref_1234",
  "id": "ORD01JYH1Z1YJN4HZ8J3Q0RB3YP6D",
  "status": "expired",
  "status_detail": "expired",
  "transactions": {
  "payments": [
  {
  "amount": "120",
  "id": "PAY01K22Y503EJ8JHGF64KGY1PZ2B",
  "status": "expired",
  "status_detail": "expired"
  }
  ]
  },
  "type": "point",
  "version": 3
  },
  "date_created": "2025-08-07T19:50:29.172256789Z",
  "live_mode": true,
  "type": "order",
  "user_id": "123456"
}
```
:::
::::

:::::

:::::AccordionComponent{title="Validate the origin of the notification"}

Validating the origin of a notification is essential to ensure the security and authenticity of the received information. This process helps prevent fraud and ensures that only legitimate notifications are processed.

Mercado Pago will send a notification similar to the example below for a `order` topic alert. This example includes the complete notification, which contains the query params, the body, and the header of the notification.

- **Query params**: These are query parameters that accompany the URL. In the example, we have `data.id=ORD01JQ4S4KY8HWQ6NA5PXB65B3D3` and `type=order`.
- **Body**: The body of the notification contains detailed information about the event, such as `action`, `api_version`, `application_id`, `date_created`, `id`, `live_mode`, `type`, `user_id`, and `data`.
- **Header**: The header contains important metadata, including the secret signature of the notification `x-signature`.

```notification
POST /test?data.id=ORD01JQ4S4KY8HWQ6NA5PXB65B3D3&type=order HTTP/1.1
Host: test.requestcatcher.com
Accept: */*
Accept-Encoding: *
Connection: keep-alive
Content-Length: 177
Content-Type: application/json
Newrelic: eyJ2IjpbMCwxXSwiZCI6eyJ0eSI6IkFwcCIsImFjIjoiOTg5NTg2IiwiYXAiOiI5NjA2MzYwOTQiLCJ0eCI6ImY4MzljZjg4ODg2MGRmZTIiLCJ0ciI6ImMwOGMwZGMyMjNjZDY2YjJkZWQwMjUxZmYxNWNiNGQ1IiwicHIiOjEuMjUwMzIsInNhIjp0cnVlLCJ0aSI6MTc0Mjg0MjU4MDE2NCwiaWQiOiIxOGI2NDcxNjNkNzI3NjU4IiwidGsiOiIxNzA5NzA3In19=
Traceparent: 00-c08c0dc223cd66b2ded0251ff15cb4d5-18b647163d727658-01
Tracestate: 1709707@nr=0-0-989586-960636094-18b647163d727658-f839cf888860dfe2-1-1.250320-1742842580164
User-Agent: restclient-node/4.15.3
X-Request-Id: 2066ca19-c6f1-498a-be75-1923005edd06
X-Rest-Pool-Name: /services/webhooks.js
X-Retry: 0
X-Signature: ts=1742505638683,v1=ced36ab6d33566bb1e16c125819b8d840d6b8ef136b0b9127c76064466f5229b
X-Socket-Timeout: 22000
{"action":"order.action_required","api_version":"v1","application_id":"76506430185983","date_created":"2021-11-01T02:02:02Z","id":"123456","live_mode":false,"type":"order","user_id":2025701502,"data":{"id":"ORD01JQ4S4KY8HWQ6NA5PXB65B3D3"}}
```

From the received Webhook notification, you can validate the authenticity of its origin. Mercado Pago will always include the secret key in the Webhooks notifications to be received, which will allow validating their authenticity. This key will be sent in the `x-signature` header, similar to the example below.

```
ts=1742505638683,v1=ced36ab6d33566bb1e16c125819b8d840d6b8ef136b0b9127c76064466f5229b
```

To confirm the validation, it is necessary to extract the key from the header and compare it with the key provided for your application in [Your integrations](/developers/panel/app).

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
1. To extract the timestamp (`ts`) and key (`v1`) from the `x-signature` header, divide the header content by the `,` character, which will result in a list of elements. The value for the `ts` prefix is the notification timestamp (in milliseconds) and `v1` is the encrypted key.
2. Using the template below, substitute the parameters with the data received in your notification.

```
id:[data.id_url];request-id:[x-request-id_header];ts:[ts_header];
```

- `[data.id_url]` will be replaced by the value of the `data.id` parameter received in the URL query params.

> NOTE
>
> If `data.id` is returned with uppercase alphanumeric characters, convert it to lowercase before using it in the manifest. For example, `ORD01JQ4S4KY8HWQ6NA5PXB65B3D3` should be used as `ord01jq4s4ky8hwq6na5pxb65b3d3`.
- `[x-request-id_header]` must be replaced by the value received in the `x-request-id` header.
- `[ts_header]` will be the `ts` value extracted from the `x-signature` header.

> NOTE
>
> If any of the values (`data.id`, `x-request-id`) are not present in the received notification, you must remove them from the manifest before computing the `HMAC`.

3. In [Your integrations](/developers/panel/app), select the integrated application, click **Webhooks > Configure notification** and reveal the generated secret key.

![cofigure notifications](/images/api-orders/not6-signature-es-v1.png)

4. Generate the counter-key for validation. To do this, compute an [HMAC](https://en.wikipedia.org/wiki/HMAC) with the `SHA256 hash` function in hexadecimal base, using the secret key as the key and the template with the values as the message.

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

5. Finally, compare the generated key with the key extracted from the header, ensuring they match exactly. Additionally, you can use the timestamp extracted from the header to compare it with a timestamp generated at the time of receipt, in order to establish a delay tolerance in receiving the message.

Here are complete code examples:

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
if ($dataID !== '') $parts[] = "id:{$dataID}";
if ($xRequestId !== '') $parts[] = "request-id:{$xRequestId}";
$parts[] = "ts:{$ts}";
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

x_signature = request.headers.get("x-signature", "")
x_request_id = request.headers.get("x-request-id", "")
data_id = (request.args.get("data.id", "") or "").lower()

ts = hash_value = None
for part in x_signature.split(","):
  if "=" not in part:
  continue
  key, _, value = part.partition("=")
  key = key.strip()
  value = value.strip()
  if key == "ts": ts = value
  if key == "v1": hash_value = value

parts = []
if data_id: parts.append(f"id:{data_id}")
if x_request_id: parts.append(f"request-id:{x_request_id}")
parts.append(f"ts:{ts}")
manifest = ";".join(parts) + ";"

computed = hmac.new(secret.encode(), manifest.encode(), hashlib.sha256).hexdigest()
if not hmac.compare_digest(computed, hash_value):
  return "", 401
return "", 200
```
```go
import (
  "crypto/hmac"
  "crypto/sha256"
  "encoding/hex"
  "net/http"
  "strings"
)

xSignature := r.Header.Get("x-signature")
xRequestID := r.Header.Get("x-request-id")
dataID := strings.ToLower(r.URL.Query().Get("data.id"))

var ts, hash string
for _, part := range strings.Split(xSignature, ",") {
  kv := strings.SplitN(part, "=", 2)
  if len(kv) != 2 { continue }
  key := strings.TrimSpace(kv[0])
  val := strings.TrimSpace(kv[1])
  if key == "ts" { ts = val }
  if key == "v1" { hash = val }
}

var parts []string
if dataID != "" { parts = append(parts, "id:"+dataID) }
if xRequestID != "" { parts = append(parts, "request-id:"+xRequestID) }
parts = append(parts, "ts:"+ts)
manifest := strings.Join(parts, ";") + ";"

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

var xSignature = Request.Headers["x-signature"].ToString();
var xRequestId = Request.Headers["x-request-id"].ToString();
var dataId = (Request.Query["data.id"].ToString() ?? "").ToLowerInvariant();

string ts = null, hash = null;
foreach (var part in xSignature.Split(','))
{
  var eq = part.IndexOf('=');
  if (eq < 0) continue;
  var key = part[..eq].Trim();
  var val = part[(eq + 1)..].Trim();
  if (key == "ts") ts = val;
  if (key == "v1") hash = val;
}

var parts = new List<string>();
if (!string.IsNullOrEmpty(dataId)) parts.Add($"id:{dataId}");
if (!string.IsNullOrEmpty(xRequestId)) parts.Add($"request-id:{xRequestId}");
parts.Add($"ts:{ts}");
var manifest = string.Join(";", parts) + ";";

using var hmacSha = new HMACSHA256(Encoding.UTF8.GetBytes(secret));
var computed = BitConverter
  .ToString(hmacSha.ComputeHash(Encoding.UTF8.GetBytes(manifest)))
  .Replace("-", "").ToLowerInvariant();

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

String xSignature = request.getHeader("x-signature") != null ? request.getHeader("x-signature") : "";
String xRequestId = request.getHeader("x-request-id") != null ? request.getHeader("x-request-id") : "";
String dataId = request.getParameter("data.id") != null
  ? request.getParameter("data.id").toLowerCase() : "";

String ts = null, hash = null;
for (String part : xSignature.split(",")) {
  String[] kv = part.split("=", 2);
  if (kv.length != 2) continue;
  String key = kv[0].trim();
  String val = kv[1].trim();
  if ("ts".equals(key)) ts = val;
  if ("v1".equals(key)) hash = val;
}

List<String> parts = new ArrayList<>();
if (!dataId.isEmpty()) parts.add("id:" + dataId);
if (!xRequestId.isEmpty()) parts.add("request-id:" + xRequestId);
parts.add("ts:" + ts);
String manifest = String.join(";", parts) + ";";

Mac mac = Mac.getInstance("HmacSHA256");
mac.init(new SecretKeySpec(secret.getBytes(StandardCharsets.UTF_8), "HmacSHA256"));
byte[] bytes = mac.doFinal(manifest.getBytes(StandardCharsets.UTF_8));
StringBuilder sb = new StringBuilder();
for (byte b : bytes) sb.append(String.format("%02x", b & 0xff));
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
parts << "id:#{data_id}" unless data_id.empty?
parts << "request-id:#{x_request_id}" unless x_request_id.empty?
parts << "ts:#{ts}"
manifest = "#{parts.join(';')};"

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

:::AccordionComponent{title="Actions required after receiving the notification"}

When you receive a notification on your platform, Mercado Pago expects a response to validate that the reception was correct. To do this, you must return an `HTTP STATUS 200 (OK)` or `201 (CREATED)`.

The waiting time for this confirmation will be 22 seconds. If this response is not sent, the system will understand that the notification was not received and will make a new attempt to send it every 15 minutes until it receives the response. After the third attempt, the deadline will be extended, but the deliveries will continue to happen.

After responding to the Webhook notification and confirming its receipt, only if the information received is not sufficient and you need additional information, you can obtain all the data about the notified resource by sending a **GET** to the endpoint :TagComponent{tag="GET" text="/v1/orders/{id}" href="/developers/en/reference/in-person-payments/point/orders/get-order/get" color="accent"}.

With this information, you will be able to make the necessary updates to your platform, such as updating an approved payment.

:::

# Configure optional notifications

In addition to the primary orders topic, Mercado Pago offers optional topics that notify your application about integration management events: account linking via OAuth, buyer-initiated claims, and chargebacks. These notifications complement the main flow and keep your system synchronized with events beyond payment processing.

None of these topics replaces the orders topic or is mandatory. Activate only the ones relevant to your integration.

## Available topics

| Topic | Panel name | Description |
|---|---|---|
| `mp-connect` | Application linking | Notifies when an account is linked or unlinked via [OAuth](/developers/en/docs/security/oauth). Applies to all integrations that use OAuth. |
| `topic_claims_integration_wh` | Claims | Notifies when a buyer files a claim or when a status change occurs. |
| `topic_chargebacks_wh` | Chargebacks | Notifies when a buyer initiates a chargeback or a status change occurs. |

## Configure Webhooks

Follow the steps below to activate the optional topics in your integration.

> RED_MESSAGE
>
> If you are developing using test credentials, go to **Your integrations > Application details > Test credentials > Test credentials data**, sign in to [Mercado Pago Developers](/developers/en/docs) with the username and password of that test account, and configure the Webhooks in production mode for that account. This way, you will be able to test the notifications correctly.

1. Go to [Your integrations](https://www.mercadopago.com/developers/panel/app) and select the application for which you want to activate notifications.

![configure notifications](/images/api-orders/not1-app-es-v1.png)

2. In the left menu, select **Webhooks > Configure notifications**.

![configure notifications](/images/api-orders/not2-configure-es-v1.png)

3. Select the **Production mode** tab and provide an `HTTPS URL` to receive notifications.

4. In the optional topics section, select the events you want to activate: **Application linking**, **Claims**, and/or **Chargebacks**.

5. Finally, click **Save configuration**. This will generate a :toolTipComponent[secret key]{content="Key used to validate the authenticity of each received notification." link="/developers/en/docs/mp-point/notifications"} for your application. Note that this key has no expiration date and periodic renewal is not mandatory, though recommended. To do so, click the **Reset** button.

## Simulate receiving the notification

To ensure notifications are configured correctly, simulate receiving them by following the steps below.

1. After configuring your Webhooks, click **Simulate notification**.
2. On the simulation screen, select the URL to test.
3. Choose the event type you want to test and enter the **resource ID** to be sent in the notification body (`Data ID`).
![cofigure notifications](/images/api-orders/not5-order-es-v2.png)

4. Finally, click **Send test** to verify the request, the server response, and the event description.

## Validate the notification origin

Validating the origin of a notification is essential to ensure the security and authenticity of the received information. This process helps prevent fraud and ensures that only legitimate notifications are processed.

Mercado Pago will send your server a notification similar to the example below. Below are examples of notifications for each topic.

::::TabsComponent

:::TabComponent{title="Application linking"}

```
POST /?data.id=123456789&type=mp-connect HTTP/1.1
Host: test-optional-nots.requestcatcher.com
Accept: */*
Accept-Encoding: *
Connection: keep-alive
Content-Length: 187
Content-Type: application/json
User-Agent: restclient-node/5.1.10
X-Request-Id: 4ed4fa2b-0b31-42ec-a62f-ad793c486c59
X-Rest-Pool-Name: /services/webhooks.js
X-Retry: 0
X-Signature: ts=1781009491,v1=654866c48793d9f716f255f8a8e6cb162f643d93b29391daa6ac7ce78cf0ce81
X-Socket-Timeout: 22000
{"action":"application.authorized","api_version":"v1","data":{"id":"123456789"},"date_created":"2026-06-12T13:14:01.351Z","id":100000000000,"live_mode":true,"type":"mp-connect","user_id":123456789}
```

| Field | Type | Description |
|---|---|---|
| `action` | string | Notified event. Possible values: `application.authorized` (linking) and `application.deauthorized` (unlinking). |
| `api_version` | string | API version. Always `v1`. |
| `data.id` | string | Identifier of the resource associated with the event. |
| `date_created` | string | Notification creation date (ISO 8601). |
| `id` | long | Unique notification identifier. Use it for idempotency control. |
| `live_mode` | boolean | `true` in production, `false` in test mode. |
| `type` | string | Always `mp-connect`. |
| `user_id` | long | Identifier of the seller for whom the notification is sent. |

:::

:::TabComponent{title="Claims"}

```
POST /?data.id=1234567890&type=claim HTTP/1.1
Host: test-optional-nots.requestcatcher.com
Accept: */*
Accept-Encoding: *
Connection: keep-alive
Content-Length: 207
Content-Type: application/json
User-Agent: restclient-node/5.1.10
X-Request-Id: 1d07590a-fd51-4e67-8b13-7d45600670e5
X-Rest-Pool-Name: /services/webhooks.js
X-Retry: 0
X-Signature: ts=1781009658,v1=e446ded9a9e0dd94acba3fd0fa9e35e497abcf2ef11a6d0f5291f7c7eab00fb7
X-Socket-Timeout: 22000
{"action":"updated","api_version":"v1","data":{"id":1234567890,"resource":"/v1/claims/1234567890"},"date_created":"2026-06-12T06:14:40-04:00","id":"00000000-0000-0000-0000-000000000001","live_mode":true,"type":"claim","user_id":123456789}
```

| Field | Type | Description |
|---|---|---|
| `action` | string | Notified event. Indicates the action that occurred on the claim. |
| `api_version` | string | API version. Always `v1`. |
| `data.id` | long | Unique identifier of the claim. |
| `data.resource` | string | Path of the claim resource in the API. |
| `date_created` | string | Notification creation date (ISO 8601). |
| `id` | string | Unique notification identifier (UUID). Use it for idempotency control. |
| `live_mode` | boolean | `true` in production, `false` in test mode. |
| `type` | string | Always `claim`. |
| `user_id` | long | Identifier of the seller for whom the notification is sent. |

:::

:::TabComponent{title="Chargebacks"}

```
POST /?data.id=114544942708&type=topic_chargebacks_wh HTTP/1.1
Host: test-optional-nots.requestcatcher.com
Accept: */*
Accept-Encoding: *
Connection: keep-alive
Content-Type: application/json
User-Agent: restclient-node/5.1.10
X-Request-Id: 948ac0a7-bf77-4877-8fe8-8ab69a356fa4
X-Rest-Pool-Name: /services/webhooks.js
X-Retry: 0
X-Signature: ts=1781009697,v1=108c6756aa1b96a5303b41769bb89261ebeb2922333b483886502f5b7ae3d79d
X-Socket-Timeout: 22000
{"actions":["changed_case_status"],"api_version":"v1","application_id":1234567890987654,"data":{"checkout":"PRO","date_updated":"0001-01-01T00:00:00Z","id":217000061307271000,"payment_id":81034165129,"product_id":"BC32A57TRPP001U8NHHG","site_id":"MLA","transaction_intent_id":""},"date_created":"2024-07-02T22:03:24-04:00","id":114544942708,"live_mode":true,"type":"topic_chargebacks_wh","user_id":123456789,"version":1720427447}
```

| Field | Type | Description |
|---|---|---|
| `actions` | array | List of actions that occurred. For example, `changed_case_status`. |
| `api_version` | string | API version. Always `v1`. |
| `data.id` | long | Chargeback identifier. |
| `data.payment_id` | long | Associated payment identifier. |
| `data.site_id` | string | Site identifier (country). |
| `date_created` | string | Notification creation date (ISO 8601). |
| `id` | long | Notification identifier. |
| `live_mode` | boolean | `true` in production, `false` in test mode. |
| `type` | string | Always `topic_chargebacks_wh`. |
| `user_id` | long | Seller identifier. |
| `version` | long | Event version timestamp. |

:::

::::

From the received notification, you can validate the authenticity of its origin through the secret key. This key will be sent in the `x-signature` header, with the following format:

```
ts=1742505638683,v1=ced36ab6d33566bb1e16c125819b8d840d6b8ef136b0b9127c76064466f5229b
```

To confirm the validation, extract the key from the header and compare it with the key provided for your application in [Your integrations](/developers/panel/app).

Follow one of the approaches below to validate the authenticity of the notification.

::::TabsComponent

:::TabComponent{title="With SDKs"}

The official SDK implements HMAC-based Webhook Signature Verification to authenticate the origin of each received notification.

To get your secret key (`secret`), go to [Your integrations](/developers/panel/app), select the application, click **Webhooks > Configure notification** and reveal the generated key.

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

If you don't use the official SDK, you can manually validate the authenticity of notifications by following these steps:

1. To extract the timestamp (`ts`) and key (`v1`) from the `x-signature` header, divide the header content by the `,` character, which will result in a list of elements. The value for the `ts` prefix is the notification timestamp (in milliseconds) and `v1` is the encrypted key.
2. Using the template below, substitute the parameters with the data received in your notification.

```
id:[data.id_url];request-id:[x-request-id_header];ts:[ts_header];
```

- `[data.id_url]` will be replaced by the value of the `data.id` parameter received in the URL query params.
- `[x-request-id_header]` must be replaced by the value received in the `x-request-id` header.
- `[ts_header]` will be the `ts` value extracted from the `x-signature` header.

> NOTE
>
> If any of the values (`data.id`, `x-request-id`) are not present in the received notification, you must remove them from the manifest before computing the `HMAC`.

3. In [Your integrations](/developers/panel/app), select the integrated application, click **Webhooks > Configure notification** and reveal the generated secret key.

4. Generate the counter-key for validation. To do this, compute an [HMAC](https://en.wikipedia.org/wiki/HMAC) with the `SHA256 hash` function in hexadecimal base, using the secret key as the key and the template with the values as the message.

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

5. Finally, compare the generated key with the key extracted from the header, ensuring they match exactly. Additionally, you can use the timestamp extracted from the header to compare it with a timestamp generated at the time of receipt, in order to establish a delay tolerance in receiving the message.

Here are complete code examples:

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
if ($dataID !== '') $parts[] = "id:{$dataID}";
if ($xRequestId !== '') $parts[] = "request-id:{$xRequestId}";
$parts[] = "ts:{$ts}";
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

x_signature = request.headers.get("x-signature", "")
x_request_id = request.headers.get("x-request-id", "")
data_id = (request.args.get("data.id", "") or "").lower()

ts = hash_value = None
for part in x_signature.split(","):
  if "=" not in part:
  continue
  key, _, value = part.partition("=")
  key = key.strip()
  value = value.strip()
  if key == "ts": ts = value
  if key == "v1": hash_value = value

parts = []
if data_id: parts.append(f"id:{data_id}")
if x_request_id: parts.append(f"request-id:{x_request_id}")
parts.append(f"ts:{ts}")
manifest = ";".join(parts) + ";"

computed = hmac.new(secret.encode(), manifest.encode(), hashlib.sha256).hexdigest()
if not hmac.compare_digest(computed, hash_value):
  return "", 401
return "", 200
```
```go
import (
  "crypto/hmac"
  "crypto/sha256"
  "encoding/hex"
  "net/http"
  "strings"
)

xSignature := r.Header.Get("x-signature")
xRequestID := r.Header.Get("x-request-id")
dataID := strings.ToLower(r.URL.Query().Get("data.id"))

var ts, hash string
for _, part := range strings.Split(xSignature, ",") {
  kv := strings.SplitN(part, "=", 2)
  if len(kv) != 2 { continue }
  key := strings.TrimSpace(kv[0])
  val := strings.TrimSpace(kv[1])
  if key == "ts" { ts = val }
  if key == "v1" { hash = val }
}

var parts []string
if dataID != "" { parts = append(parts, "id:"+dataID) }
if xRequestID != "" { parts = append(parts, "request-id:"+xRequestID) }
parts = append(parts, "ts:"+ts)
manifest := strings.Join(parts, ";") + ";"

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

var xSignature = Request.Headers["x-signature"].ToString();
var xRequestId = Request.Headers["x-request-id"].ToString();
var dataId = (Request.Query["data.id"].ToString() ?? "").ToLowerInvariant();

string ts = null, hash = null;
foreach (var part in xSignature.Split(','))
{
  var eq = part.IndexOf('=');
  if (eq < 0) continue;
  var key = part[..eq].Trim();
  var val = part[(eq + 1)..].Trim();
  if (key == "ts") ts = val;
  if (key == "v1") hash = val;
}

var parts = new List<string>();
if (!string.IsNullOrEmpty(dataId)) parts.Add($"id:{dataId}");
if (!string.IsNullOrEmpty(xRequestId)) parts.Add($"request-id:{xRequestId}");
parts.Add($"ts:{ts}");
var manifest = string.Join(";", parts) + ";";

using var hmacSha = new HMACSHA256(Encoding.UTF8.GetBytes(secret));
var computed = BitConverter
  .ToString(hmacSha.ComputeHash(Encoding.UTF8.GetBytes(manifest)))
  .Replace("-", "").ToLowerInvariant();

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

String xSignature = request.getHeader("x-signature") != null ? request.getHeader("x-signature") : "";
String xRequestId = request.getHeader("x-request-id") != null ? request.getHeader("x-request-id") : "";
String dataId = request.getParameter("data.id") != null
  ? request.getParameter("data.id").toLowerCase() : "";

String ts = null, hash = null;
for (String part : xSignature.split(",")) {
  String[] kv = part.split("=", 2);
  if (kv.length != 2) continue;
  String key = kv[0].trim();
  String val = kv[1].trim();
  if ("ts".equals(key)) ts = val;
  if ("v1".equals(key)) hash = val;
}

List<String> parts = new ArrayList<>();
if (!dataId.isEmpty()) parts.add("id:" + dataId);
if (!xRequestId.isEmpty()) parts.add("request-id:" + xRequestId);
parts.add("ts:" + ts);
String manifest = String.join(";", parts) + ";";

Mac mac = Mac.getInstance("HmacSHA256");
mac.init(new SecretKeySpec(secret.getBytes(StandardCharsets.UTF_8), "HmacSHA256"));
byte[] bytes = mac.doFinal(manifest.getBytes(StandardCharsets.UTF_8));
StringBuilder sb = new StringBuilder();
for (byte b : bytes) sb.append(String.format("%02x", b & 0xff));
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
parts << "id:#{data_id}" unless data_id.empty?
parts << "request-id:#{x_request_id}" unless x_request_id.empty?
parts << "ts:#{ts}"
manifest = "#{parts.join(';')};"

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

## Actions needed after receiving the notification

When you receive a notification on your platform, Mercado Pago expects a response to validate that the receipt was correct. To do so, return an `HTTP STATUS 200` or `201` within 22 seconds of receipt.

We recommend that you first respond with a `200` or `201`, and then process the notification on the server, to avoid duplicate notifications.

If this response is not sent, the system will make new delivery attempts every 15 minutes. After the first failures, the interval progressively increases, but deliveries continue until the notification is confirmed.

# Configure printings

The printers of the **Point Smart 1 and 2 terminals** allow printing the purchase ticket and, additionally, **integrate custom printings through the Terminals API**. This function can be useful for those who require printing complementary receipts, such as coupons or even images.

This way, you can manage additional printings directly from your Point of Sale system, and obtain them from the terminal to which they are assigned.

## Create printings

The printings generated from your system are actions that your point of sale sends to the terminal. Therefore, to create a printing, you must send a request to the endpoint :TagComponent{tag="POST" text="/terminals/v1/actions" href="/developers/en/reference/in-person-payments/point/impressions/create-terminal/post" color="green"} with your :toolTipComponent[test Access Token]{link="/developers/en/docs/mp-point/create-application#bookmark_access_test_credentials" linkText="Access test credentials" content="Private key of the application created in Mercado Pago, used in the backend during integration development. You can access it in Your integrations > Integration data > Tests > Test credentials. When going to production, replace it with the production Access Token if it is your own integration, or with the Access Token obtained via OAuth in the case of third-party integrations. The test Access Token starts with the prefix `APP_USR`."}, taking care to correctly send the **mandatory parameters** indicated below.

```curl
curl -X POST \
  'https://api.mercadopago.com/terminals/v1/actions'\
  -H 'Content-Type: application/json' \
  -H 'X-Idempotency-Key: {{SOME_UNIQUE_VALUE}}' \
  -H 'Authorization: Bearer {{YOUR_ACCESS_TOKEN}}' \
  -d '{
  "type": "print",
  "external_reference": "ext_ref_1234",
  "config": {
  "point": {
  "terminal_id": "NEWLAND_N950__N950NCB123456789",
  "subtype": "image"
  }
  },
  "content": "iVBORw0KGgoAAAANSUhEUgAAAEAAAABACAYAAACqaXHeAAAABHNCSVQICAgIfAhkiAAAAAlwSFlzAAAB2AAAAdgB+lymcgAAABl0RVh0U29mdHdhcmUAd3d3Lmlua3NjYXBlLm9yZ5vuPBoAAAPqSURBVHic7ZrZaxRBEIe/mJh4xRgDGk8ivqtvIvGESLwQ7wsU/yD/Ah+NURQjIioY8FbwRZ9UEFREvEFjEm83GR96Byab2Zlf9/RuFp0PlsxR1dVTXVXdPRPIycnJycnJ+V+pc9DpANYAU8vc/wXcBZ479qkcLcBmYGaZ+6PAI+C+Z7tj2Ar8AIKU3x9gl0e7HcBbwW4AHPNodxwPxE4EwEtgkie7xy3sjgLtnuyO46tFRwJgnQebU4CBStm1GaFGYLqFPMBBS/k4dgKzLHVkeRsHtFl2AmAf0OSgF+WIg05FHDDboSOtQLeDXshcoMtBryIOaHXoCGRLg8NAg4NeiypY6QgA2A40O+oedtSrKQdMA3Y46K0AljnarJkaEOKSBi7FL6SmagDARkxBU2kgW+2ouQhoAPZYyHeTbTVXcw4AOGQh61r8QmwXThJXsVuOxq3Rlwh2ZgLfM9r6pD5UtWoAmK23ktf7Kb/VVmnBbaufyDOyjUoAPBHs3PFgJ6D8ewNnPnvq2PIEGx2YVPFhZ7HyUGoKTMJidZVCUjE8ir/Q9VoI2/AzKgHwinjH1+EnzcLfWuXB1AjIOgVGWQSsjrneCSz1aEeKANUBWWeAUuJmgyxL3zhq2gF7gcmR86biNYUBUU6qWb5TYEiUawM2RM43oY3YK+C6aMNrBKivw/qAn6Ls7sjxAVGnFxgUZb1GgDqlvMEsmRV2APWY9wXbRJ1e9CiT0rYSKXBWlJ2D+cK0FZghyD8EHgPDYvvSoKnv21QHDAIXMV+PlPX8LmC+2HZP8a8aAV5rgOqAL5iPJ1dE+b3AFkGuAJwuHk9IDVAdEE5RZ0T5drRI6Qc+FI9rPgIALmMiwRc9kWM1AibUAd+BS6JOGkOYuhI9V5iFsLHyvRL8EjlW0yCNPoxDQ9QIqEebXVJpRt+BNUb0mjAOybqri64YARZa6C5KezglAtTR/wb8jpz/YmzouvAGuF1yTU0BEOqA4gDb/I+SNQ1OACMl14Yxb40UJtwB/ZhXaa6cirkW4HE1WGkH/AEuiPqlPMD801Mc3qbCSjsA9L1BKT0J97wthnw6oNyoXAM+im2EFEiuH1WNAJc1QJQC9mnQD7xPuO9tP1CNFAD72SAp/EFPAS8OUCMgaVRuAu/EdkqXvra2otREEQQzb58X2znH2KVvHFV1gPpFKMkBoKfBSUFGTYHUwVMcoIbu05T794AXKTLPgFsebIUkFVKZlaRvatKKVkgnZn0f18ZrYJXYTiPpX5EHi31PRP0QOQ9Yz/h/dwswo1G6YUmiAViA2a6GjGAcU7Bsp4v4r8DDwA08RUBOTk5OTk7Ov8lfFiKY13GwsdoAAAAASUVORK5CYII="
}'
```

| Attribute | Type | Description |
|----------|------|-------------|
| `Authorization` | Header | Refers to either your :toolTipComponent[test Access Token]{link="/developers/en/docs/mp-point/create-application#bookmark_access_test_credentials" linkText="Access test credentials" content="Private key of the application created in Mercado Pago, used in the backend during integration development. You can access it in Your integrations > Integration data > Tests > Test credentials. When going to production, replace it with the production Access Token if it is your own integration, or with the Access Token obtained via OAuth in the case of third-party integrations. The test Access Token starts with the prefix `APP_USR`."}. |
| `X-Idempotency-Key` | Header | Idempotency key. This key ensures that each request is processed only once, avoiding duplicates. Use an exclusive value in your request header, such as a UUID V4 or random strings. |
| `type` | Body. String | Action type. You must send the value `print`, which is associated with creating printing actions for the Point of Sale. |
| `external_reference` | Body. String | It is an external reference of the action, assigned at the time of its creation. The maximum allowed limit is 64 characters and the allowed ones are: **uppercase and lowercase letters**, **numbers** and **hyphen (-) and underscore (_) symbols**. |
| `config.point.terminal_id` | Body. String | Identifier of the Point terminal that will obtain the order. You must send it as it was returned in the call :TagComponent{tag="GET" text="Get terminals" href="/developers/en/reference/in-person-payments/point/terminals/get-terminals/get" color="accent"}, as in the following example: "NEWLAND_N950__N950NCB801293324". |
| `config.point.subtype` | Body. String | Identifier of the print subtype that will be created for the Point terminal. If the action is print, you must choose one of the following values: <br> -`invoice`: for printing DTEs or invoices. <br> -`custom`: for custom printing. <br> -`image`: for image printing. |
| `content` | Body. String | Contains the information to print on the Point terminal. Go to [Requirements for printing content](/developers/en/docs/mp-point/configure-printings#bookmark_requirements_for_printing_content) to know what validations to consider depending on the type of printing. |

### Requirements for printing content

To implement the different types of printing desired, in addition to indicating which one it is in the `config.point.subtype` field, you must take into account the requirements, formats and validations that each of them requires when sending their content through the `content` parameter.

::::TabsComponent

:::TabComponent{title="DTE printing"}
When selecting the `config.point.subtype` as `invoice`, the DTE to be sent in the `content` parameter must be compatible with the formats defined by the [SII](https://www.sii.cl/servicios_online/3532-formato_xml-3811.html), and must be sent in XML format.

Additionally, the following document types are accepted:

| Document type | Description |
|---------------|-------------|
| **Affected Invoice (33) and Exempt (34)** | Refers to the tax document that has legal validity before the Internal Revenue Service (SII). |
| **Affected Receipt (39) and Exempt (41)** | Refers to the document that the customer receives when making a purchase, which has accounting and tax validity. |

:::
:::TabComponent{title="Custom printings"}
Custom printings use tags that allow adjusting the format and appearance of printed documents, ensuring greater control over the style and structure of the text.

When defining the `subtype` attribute as `custom`, you must include in the `content` field a string with the desired content, formatted using **at least one of the supported tags**. The content for this attribute is a **minimum of 100 characters and a maximum of 4096**, including the tags themselves.

Below, check the different available tags and their functions.

| Tags | Function | Example |
|------|----------|---------|
| `{b}` | Bold | `{b}Bold text{/b}` |
| `{w}` | Large letter | `{w}Large letter text{/w}` |
| `{s}` | Small letter | `{s}Small letter text{/s}` |
| `{br}` | Line break | `{br}` |
| `{left}` | Align left | `{left}Left aligned text{/left}` |
| `{center}` | Center text | `{center}Centered text{/center}` |
| `{qr}` | Print a QR that represents the sent text | `{qr}Text{/qr}` |
| `{pdf417}` | Print a barcode | `{pdf417}Text{/pdf417}` |

Additionally, we provide you with a usage example.

```json
{
  "type": "print",
  "config": {
  "point": {
  "terminal_id": "{{id}}",
  "subtype": "custom"
  }
  },
  "external_reference": "8a42e06e45d5",
  "content": "{br}--------------------------------{br}{center}{w} DELIVERY RECEIPT{/w}{br}{br}{s} Order number :12345{/s}{br}{s} Store: Test store{/s}{br}--------------------------------{br}{s}***DISPATCH ITEM(S)***{/s}{br}{s}SKU / ARTICLE QUANTITY {/s}{br}{s}----------------------------------------------{/s}{br}{s}4065432630504 / SOCCER BALL WUCL LGE EHV240424 1{br}{s}DELIVER: 06/06/2024{/s}{br}{s}ADDRESS: METROPOLITAN {/s}{br}{s}RECEIVES: John{/s}{br}{s}delivery to customer in am schedule{/s}{br}--------------------------------{br}"
}
```

:::
:::TabComponent{title="Image printings"}
When defining the `subtype` attribute as `image`, you must include in the `content` field an image in **PNG** or **JPEG** format, with **Base64** encoding and a **maximum size of 1MB**.

If your images exceed the dimensions of the Point terminal paper roll, an automatic adjustment will be made.

:::
::::

If the request is sent correctly, the response will return the `id` of the created action along with the `status: created`, and the printing will be automatically obtained by the terminal, in which case it will then have a `status: on_terminal`. If the latter does not happen, you can check [our troubleshooting documentation](/developers/en/docs/mp-point/resources/troubleshooting).

The Terminals API will also allow you to :TagComponent{tag="GET" text="get an action" href="/developers/en/reference/in-person-payments/point/impressions/get-action/get" color="accent"}, including its `status` in real time, by sending the reference `id` obtained in the response to its creation.

Finally, it is also possible to :TagComponent{tag="POST" text="cancel an action" href="/developers/en/reference/in-person-payments/point/impressions/cancel-action/post" color="green"} using the reference `id` obtained in the response to its creation, as long as its status is `created`.

# Configure printings

The printers of the **Point Smart 1 and 2 terminals** allow printing the purchase ticket and, additionally, **integrate custom printings through the Terminals API**. This function can be useful for those who require printing complementary receipts, such as coupons or even images.

This way, you can manage additional printings directly from your Point of Sale system, and obtain them from the terminal to which they are assigned.

## Create printings

The printings generated from your system are actions that your point of sale sends to the terminal. Therefore, to create a printing, you must send a request to the endpoint :TagComponent{tag="POST" text="/terminals/v1/actions" href="/developers/en/reference/in-person-payments/point/impressions/create-terminal/post" color="green"} with your :toolTipComponent[test Access Token]{link="/developers/en/docs/mp-point/create-application#bookmark_access_test_credentials" linkText="Access test credentials" content="Private key of the application created in Mercado Pago, used in the backend during integration development. You can access it in Your integrations > Integration data > Tests > Test credentials. When going to production, replace it with the production Access Token if it is your own integration, or with the Access Token obtained via OAuth in the case of third-party integrations. The test Access Token starts with the prefix `APP_USR`."}, taking care to correctly send the **mandatory parameters** indicated below.

```curl
curl -X POST \
  'https://api.mercadopago.com/terminals/v1/actions'\
  -H 'Content-Type: application/json' \
  -H 'X-Idempotency-Key: {{SOME_UNIQUE_VALUE}}' \
  -H 'Authorization: Bearer {{YOUR_ACCESS_TOKEN}}' \
  -d '{
  "type": "print",
  "external_reference": "ext_ref_1234",
  "config": {
  "point": {
  "terminal_id": "NEWLAND_N950__N950NCB123456789",
  "subtype": "image"
  }
  },
  "content": "iVBORw0KGgoAAAANSUhEUgAAAEAAAABACAYAAACqaXHeAAAABHNCSVQICAgIfAhkiAAAAAlwSFlzAAAB2AAAAdgB+lymcgAAABl0RVh0U29mdHdhcmUAd3d3Lmlua3NjYXBlLm9yZ5vuPBoAAAPqSURBVHic7ZrZaxRBEIe/mJh4xRgDGk8ivqtvIvGESLwQ7wsU/yD/Ah+NURQjIioY8FbwRZ9UEFREvEFjEm83GR96Byab2Zlf9/RuFp0PlsxR1dVTXVXdPRPIycnJycnJ+V+pc9DpANYAU8vc/wXcBZ479qkcLcBmYGaZ+6PAI+C+Z7tj2Ar8AIKU3x9gl0e7HcBbwW4AHPNodxwPxE4EwEtgkie7xy3sjgLtnuyO46tFRwJgnQebU4CBStm1GaFGYLqFPMBBS/k4dgKzLHVkeRsHtFl2AmAf0OSgF+WIg05FHDDboSOtQLeDXshcoMtBryIOaHXoCGRLg8NAg4NeiypY6QgA2A40O+oedtSrKQdMA3Y46K0AljnarJkaEOKSBi7FL6SmagDARkxBU2kgW+2ouQhoAPZYyHeTbTVXcw4AOGQh61r8QmwXThJXsVuOxq3Rlwh2ZgLfM9r6pD5UtWoAmK23ktf7Kb/VVmnBbaufyDOyjUoAPBHs3PFgJ6D8ewNnPnvq2PIEGx2YVPFhZ7HyUGoKTMJidZVCUjE8ir/Q9VoI2/AzKgHwinjH1+EnzcLfWuXB1AjIOgVGWQSsjrneCSz1aEeKANUBWWeAUuJmgyxL3zhq2gF7gcmR86biNYUBUU6qWb5TYEiUawM2RM43oY3YK+C6aMNrBKivw/qAn6Ls7sjxAVGnFxgUZb1GgDqlvMEsmRV2APWY9wXbRJ1e9CiT0rYSKXBWlJ2D+cK0FZghyD8EHgPDYvvSoKnv21QHDAIXMV+PlPX8LmC+2HZP8a8aAV5rgOqAL5iPJ1dE+b3AFkGuAJwuHk9IDVAdEE5RZ0T5drRI6Qc+FI9rPgIALmMiwRc9kWM1AibUAd+BS6JOGkOYuhI9V5iFsLHyvRL8EjlW0yCNPoxDQ9QIqEebXVJpRt+BNUb0mjAOybqri64YARZa6C5KezglAtTR/wb8jpz/YmzouvAGuF1yTU0BEOqA4gDb/I+SNQ1OACMl14Yxb40UJtwB/ZhXaa6cirkW4HE1WGkH/AEuiPqlPMD801Mc3qbCSjsA9L1BKT0J97wthnw6oNyoXAM+im2EFEiuH1WNAJc1QJQC9mnQD7xPuO9tP1CNFAD72SAp/EFPAS8OUCMgaVRuAu/EdkqXvra2otREEQQzb58X2znH2KVvHFV1gPpFKMkBoKfBSUFGTYHUwVMcoIbu05T794AXKTLPgFsebIUkFVKZlaRvatKKVkgnZn0f18ZrYJXYTiPpX5EHi31PRP0QOQ9Yz/h/dwswo1G6YUmiAViA2a6GjGAcU7Bsp4v4r8DDwA08RUBOTk5OTk7Ov8lfFiKY13GwsdoAAAAASUVORK5CYII="
}'
```

| Attribute | Type | Description |
|----------|------|-------------|
| `Authorization` | Header | Refers to either your :toolTipComponent[test Access Token]{link="/developers/en/docs/mp-point/create-application#bookmark_access_test_credentials" linkText="Access test credentials" content="Private key of the application created in Mercado Pago, used in the backend during integration development. You can access it in Your integrations > Integration data > Tests > Test credentials. When going to production, replace it with the production Access Token if it is your own integration, or with the Access Token obtained via OAuth in the case of third-party integrations. The test Access Token starts with the prefix `APP_USR`."}. |
| `X-Idempotency-Key` | Header | Idempotency key. This key ensures that each request is processed only once, avoiding duplicates. Use an exclusive value in your request header, such as a UUID V4 or random strings. |
| `type` | Body. String | Action type. You must send the value `print`, which is associated with creating printing actions for the Point of Sale. |
| `external_reference` | Body. String | It is an external reference of the action, assigned at the time of its creation. The maximum allowed limit is 64 characters and the allowed ones are: **uppercase and lowercase letters**, **numbers** and **hyphen (-) and underscore (_) symbols**. |
| `config.point.terminal_id` | Body. String | Identifier of the Point terminal that will obtain the order. You must send it as it was returned in the call :TagComponent{tag="GET" text="Get terminals" href="/developers/en/reference/in-person-payments/point/terminals/get-terminals/get" color="accent"}, as in the following example: "NEWLAND_N950__N950NCB801293324". |
| `config.point.subtype` | Body. String | Identifier of the print subtype that will be created for the Point terminal. If the action is print, you must choose one of the following values: <br> -`invoice`: for printing DTEs or invoices. <br> -`custom`: for custom printing. <br> -`image`: for image printing. |
| `content` | Body. String | Contains the information to print on the Point terminal. Go to [Requirements for printing content](/developers/en/docs/mp-point/configure-printings#bookmark_requirements_for_printing_content) to know what validations to consider depending on the type of printing. |

### Requirements for printing content

To implement the different types of printing desired, in addition to indicating which one it is in the `config.point.subtype` field, you must take into account the requirements, formats and validations that each of them requires when sending their content through the `content` parameter.

::::TabsComponent

:::TabComponent{title="DTE printing"}
When selecting the `config.point.subtype` as `invoice`, the DTE to be sent in the `content` parameter must be compatible with the formats defined by the [SII](https://www.sii.cl/servicios_online/3532-formato_xml-3811.html), and must be sent in XML format.

Additionally, the following document types are accepted:

| Document type | Description |
|---------------|-------------|
| **Affected Invoice (33) and Exempt (34)** | Refers to the tax document that has legal validity before the Internal Revenue Service (SII). |
| **Affected Receipt (39) and Exempt (41)** | Refers to the document that the customer receives when making a purchase, which has accounting and tax validity. |

:::
:::TabComponent{title="Custom printings"}
Custom printings use tags that allow adjusting the format and appearance of printed documents, ensuring greater control over the style and structure of the text.

When defining the `subtype` attribute as `custom`, you must include in the `content` field a string with the desired content, formatted using **at least one of the supported tags**. The content for this attribute is a **minimum of 100 characters and a maximum of 4096**, including the tags themselves.

Below, check the different available tags and their functions.

| Tags | Function | Example |
|------|----------|---------|
| `{b}` | Bold | `{b}Bold text{/b}` |
| `{w}` | Large letter | `{w}Large letter text{/w}` |
| `{s}` | Small letter | `{s}Small letter text{/s}` |
| `{br}` | Line break | `{br}` |
| `{left}` | Align left | `{left}Left aligned text{/left}` |
| `{center}` | Center text | `{center}Centered text{/center}` |
| `{qr}` | Print a QR that represents the sent text | `{qr}Text{/qr}` |
| `{pdf417}` | Print a barcode | `{pdf417}Text{/pdf417}` |

Additionally, we provide you with a usage example.

```json
{
  "type": "print",
  "config": {
  "point": {
  "terminal_id": "{{id}}",
  "subtype": "custom"
  }
  },
  "external_reference": "8a42e06e45d5",
  "content": "{br}--------------------------------{br}{center}{w} DELIVERY RECEIPT{/w}{br}{br}{s} Order number :12345{/s}{br}{s} Store: Test store{/s}{br}--------------------------------{br}{s}***DISPATCH ITEM(S)***{/s}{br}{s}SKU / ARTICLE QUANTITY {/s}{br}{s}----------------------------------------------{/s}{br}{s}4065432630504 / SOCCER BALL WUCL LGE EHV240424 1{br}{s}DELIVER: 06/06/2024{/s}{br}{s}ADDRESS: METROPOLITAN {/s}{br}{s}RECEIVES: John{/s}{br}{s}delivery to customer in am schedule{/s}{br}--------------------------------{br}"
}
```

:::
:::TabComponent{title="Image printings"}
When defining the `subtype` attribute as `image`, you must include in the `content` field an image in **PNG** or **JPEG** format, with **Base64** encoding and a **maximum size of 1MB**.

If your images exceed the dimensions of the Point terminal paper roll, an automatic adjustment will be made.

:::
::::

If the request is sent correctly, the response will return the `id` of the created action along with the `status: created`, and the printing will be automatically obtained by the terminal, in which case it will then have a `status: on_terminal`. If the latter does not happen, you can check [our troubleshooting documentation](/developers/en/docs/mp-point/resources/troubleshooting).

The Terminals API will also allow you to :TagComponent{tag="GET" text="get an action" href="/developers/en/reference/in-person-payments/point/impressions/get-action/get" color="accent"}, including its `status` in real time, by sending the reference `id` obtained in the response to its creation.

Finally, it is also possible to :TagComponent{tag="POST" text="cancel an action" href="/developers/en/reference/in-person-payments/point/impressions/cancel-action/post" color="green"} using the reference `id` obtained in the response to its creation, as long as its status is `created`.

# Test the integration

The integration test of Mercado Pago Point to your system is based on simulating different transaction statuses using our API. This way, you can ensure the correct functioning of your integration before going to production, through different test scenarios. It is not possible to process real payments on the physical terminal using test accounts; to perform real transactions on the Point device, you must use a production account with real payment methods.

In these tests, you must use :toolTipComponent[test credentials]{link="/developers/en/docs/mp-point/create-application#bookmark_access_test_credentials" linkText="Access test credentials" content="Keys from the application created in Mercado Pago. You can access them through Your integrations > Integration data > Tests > Test credentials."}. Although the simulation allows you to validate the integration without interaction with the terminal in each test transaction, **it is recommended that the terminal is previously linked to your test credentials**. For more information on how to perform this association, access [Configure terminal](/developers/en/docs/mp-point/configure-terminal).

> WARNING
>
> Before starting the tests, make sure that [Webhook notifications](/developers/en/docs/mp-point/notifications) are configured. This configuration is necessary to validate the correct functioning of notifications in each test scenario.

## Use a standard virtual device

If you don't have a physical device, you can use a standard virtual device (identified by the serial `SBX0000001`) to run the tests. This device is compatible with any valid terminal (`poi_type`) for the country, so you can create an order using, for example, `NEWLAND_N950__SBX0000001`.

> WARNING
>
> The standard virtual device is not valid for integration quality measurement.

## Simulate test scenarios

Below, select and execute the desired scenarios to validate your integration. To simulate the different test scenarios below, you must use the :toolTipComponent[test Access Token]{link="/developers/en/docs/mp-point/create-application#bookmark_access_test_credentials" linkText="Access test credentials" content="Private key of the application created in Mercado Pago, used in the backend. You can access it through Your integrations > Integration data > Tests > Test credentials. The test Access Token starts with the prefix `APP_USR`."}.

The status change may take up to 10 seconds to be processed (or up to 40 seconds to simulate the `action_required` status) and, during this process, the order will automatically change to the `at_terminal` status before reaching the requested final status, **except** in the case of the `refunded` status, which transitions directly. For more information about possible statuses, see the [Order and transaction status](/developers/en/docs/mp-point/resources/status-order-transaction) documentation.

:::AccordionComponent{title="Create an order and process the payment"}

To test the correct creation of an order and the processing of the associated payment, follow the steps below.

1. Make a request to the :TagComponent{tag="POST" text="Create order" href="/developers/en/reference/in-person-payments/point/orders/create-order/post" color="green"} endpoint using the :toolTipComponent[test Access Token]{link="/developers/en/docs/mp-point/create-application#bookmark_access_test_credentials" linkText="Access test credentials" content="Private key of the application created in Mercado Pago, used in the backend. You can access it through Your integrations > Integration data > Tests > Test credentials. The test Access Token starts with the prefix `APP_USR`."}.
2. Store the order identifier, returned in the response to its creation under the `id` parameter.
3. Send a request to the :TagComponent{tag="POST" text="Simulate order status" href="/developers/en/reference/in-person-payments/point/orders/simulate-order/post" color="green"} endpoint, replacing the `{order_id}` in the request path with the order ID (`order_id`) created in step 1. In the request body, include the `status` field with the value `processed`, as shown below.

[[[
```curl
curl -X POST \
  'https://api.mercadopago.com/v1/orders/{order_id}/events' \
  -H 'Content-Type: application/json' \
  -H 'Authorization: Bearer TEST-232********97488-12********26f67454********f4c8b49c********9526408' \
  -d '{
  "status": "processed",
  "payment_method_type": "credit_card",
  "installments": 1,
  "payment_method_id": "visa",
  "status_detail": "accredited"
  }'
```
]]]

See the table below for descriptions of the parameters that can be sent in this request.

| Attribute | Type | Description | Possible values | Required |
|----------|------|-----------|-------------------|-----------------|
| `status` | Body. String | Final status you want to simulate for the order. | `processed` | Required |
| `payment_method_type` | Body. String | Type of payment method that will be used in the simulation. | `debit_card`, `credit_card`, `qr`, `voucher_card` | Optional |
| `installments` | Body. Integer | Number of payment installments. | `1` | Conditional. Send this field only when `payment_method_type` is `credit_card`. |
| `payment_method_id` | Body.String | Payment method brand. | `amex`, `master`, `visa`, `debmaster`, `debvisa` | Conditional. Send this field when `payment_method_type` is `debit_card` or `credit_card`. |
| `status_detail` | Body.String | Specific status detail you want to simulate. | `accredited` | Optional |

If the request is successful, the response will return a status `204 No Content`, with no response body.

You will receive a Webhook notification from Mercado Pago with the `action` field set to `order.processed`. In the `transactions.payments` node, you can check the payment `status`, as shown in the example below.

Additionally, you can query the :TagComponent{tag="GET" text="Get order by ID" href="/developers/en/reference/in-person-payments/point/orders/get-order/get" color="accent"} endpoint to check the order status.

```json
{
  "action": "order.processed",
  "api_version": "v1",
  "application_id": "2644473656269379",
  "data": {
  "external_reference": "ext-ref",
  "id": "ORD01JY0PGGPZ4DBV73E2PXRBCQ84",
  "status": "processed",
  "status_detail": "accredited",
  "total_paid_amount": "5.00",
  "transactions": {
  "payments": [
  {
  "amount": "5.00",
  "id": "PAY01JY0PGGPZ4DBV73E2Q0DQZQCJ",
  "paid_amount": "5.00",
  "payment_method": {
  "id": "visa",
  "installments": 1,
  "type": "credit_card"
  },
  "reference": {
  "id": "115019989861"
  },
  "status": "processed",
  "status_detail": "accredited"
  }
  ]
  },
  "type": "point",
  "version": 3
  },
  "date_created": "2025-06-18T05:00:19.274162018Z",
  "live_mode": false,
  "type": "order",
  "user_id": "123456"
}
```

:::
:::AccordionComponent{title="Simulate a payment failure"}

To validate that your integration correctly handles failed payments, you can simulate the `failed` status of an order.

1. Make a new request to the :TagComponent{tag="POST" text="Create order" href="/developers/en/reference/in-person-payments/point/orders/create-order/post" color="green"} endpoint using the :toolTipComponent[test Access Token]{link="/developers/en/docs/mp-point/create-application#bookmark_access_test_credentials" linkText="Access test credentials" content="Private key of the application created in Mercado Pago, used in the backend. You can access it through Your integrations > Integration data > Tests > Test credentials. The test Access Token starts with the prefix `APP_USR`."}.
2. Store the order identifier, returned in the response to its creation under the `id` parameter.
3. Send a request to the :TagComponent{tag="POST" text="Simulate order status" href="/developers/en/reference/in-person-payments/point/orders/simulate-order/post" color="green"} endpoint, replacing the `{order_id}` in the request path with the order ID (`order_id`) created in step 1. In the request body, include the `status` field with the value `failed`.

[[[
```curl
curl -X POST \
  'https://api.mercadopago.com/v1/orders/{order_id}/events' \
  -H 'Content-Type: application/json' \
  -H 'Authorization: Bearer TEST-232********97488-12********26f67454********f4c8b49c********9526408' \
  -d '{
  "status": "failed",
  "payment_method_type": "credit_card",
  "installments": 1,
  "payment_method_id": "visa",
  "status_detail": "insufficient_amount"
  }'
```
]]]

See the table below for descriptions of the parameters that can be sent in this request.

| Attribute | Type | Description | Possible values | Required |
|----------|------|-----------|-------------------|-----------------|
| `status` | Body. String | Final status you want to simulate for the order. | `failed` | Required |
| `payment_method_type` | Body. String | Type of payment method that will be used in the simulation. | `debit_card`, `credit_card`, `qr`, `voucher_card` | Optional |
| `installments` | Body. Integer | Number of payment installments. | `1` | Conditional. Send this field only when `payment_method_type` is `credit_card`. |
| `payment_method_id` | Body. String | Payment method brand. | `amex`, `master`, `visa`, `debmaster`, `debvisa` | Conditional. Send this field when `payment_method_type` is `debit_card` or `credit_card`. |
| `status_detail` | Body. String | Specific status detail you want to simulate. | `bad_filled_card_data`, `required_call_for_authorize`, `card_disabled`, `high_risk`, `insufficient_amount`, `invalid_installments`, `max_attempts_exceeded`, `rejected_other_reason`, `processing_error` | Optional |

If the request is successful, the response will return a status `204 No Content`, with no response body.

You will receive a Webhook notification from Mercado Pago with the `action` field set to `order.failed`. In the `transactions.payments` node, you can check the payment `status`, as shown in the example below.

Additionally, you can query the :TagComponent{tag="GET" text="Get order by ID" href="/developers/en/reference/in-person-payments/point/orders/get-order/get" color="accent"} endpoint to check the order status.

```json
{
  "action": "order.failed",
  "api_version": "v1",
  "application_id": "123456",
  "data": {
  "external_reference": "ext_ref_1234",
  "id": "ORD01K23219YK26BC6GK0HASE8VT6",
  "status": "failed",
  "status_detail": "failed",
  "transactions": {
  "payments": [
  {
  "amount": "120",
  "id": "PAY01K22Y503EJ8JHGF64KGY1PZ2B",
  "payment_method": {
  "id": "debvisa",
  "installments": 1,
  "type": "debit_card"
  },
  "reference": {
  "id": "123456789980"
  },
  "status": "failed",
  "status_detail": "bad_filled_card_data"
  }
  ]
  },
  "type": "point",
  "version": 3
  },
  "date_created": "2025-08-07T20:03:04.897928692Z",
  "live_mode": false,
  "type": "order",
  "user_id": "123456"
}
```

:::
:::AccordionComponent{title="Refund a payment"}

To confirm that the refund flow is working correctly, you need to simulate the `refunded` status on a previously processed order. The simulation of this status can only be performed on orders that already have the `processed` status. Therefore, execute the "Create an order and process the payment" scenario first.

Send a request to the :TagComponent{tag="POST" text="Simulate order status" href="/developers/en/reference/in-person-payments/point/orders/simulate-order/post" color="green"} endpoint, replacing the `{order_id}` in the request path with the ID of the previously processed order. In the request body, include the `status` field with the value `refunded`.

[[[
```curl
curl -X POST \
  'https://api.mercadopago.com/v1/orders/{order_id}/events' \
  -H 'Content-Type: application/json' \
  -H 'Authorization: Bearer TEST-232********97488-12********26f67454********f4c8b49c********9526408' \
  -d '{
  "status": "refunded"
  }'
```
]]]

See the table below for descriptions of the parameters that can be sent in this request.

| Attribute | Type | Description | Possible values | Required |
|----------|------|-----------|-------------------|-----------------|
| `status` | Body.String | Final status you want to simulate for the order. **Important:** To simulate this status, the order must have been previously processed. | `refunded` | Required |

If the request is successful, the response will return a status `204 No Content`, with no response body.

You will receive a Webhook notification from Mercado Pago with the `action` field set to `order.refunded`, indicating that the order was refunded, as shown in the example below.

Additionally, you can query the :TagComponent{tag="GET" text="Get order by ID" href="/developers/en/reference/in-person-payments/point/orders/get-order/get" color="accent"} endpoint to check the order status.

```json
{
  "action": "order.refunded",
  "api_version": "v1",
  "application_id": "2644473656269379",
  "data": {
  "external_reference": "ext-ref",
  "id": "ORD01JY0PGGPZ4DBV73E2PXRBCQ84",
  "status": "refunded",
  "status_detail": "refunded",
  "total_paid_amount": "5.00",
  "type": "point",
  "version": 4
  },
  "date_created": "2025-06-18T05:05:08.255803326Z",
  "live_mode": false,
  "type": "order",
  "user_id": "123456"
}
```

:::
:::AccordionComponent{title="Create and cancel a payment order"}

To validate that the payment cancellation flow works correctly, you can simulate the `canceled` status of an order.

1. Make a request to the :TagComponent{tag="POST" text="Create order" href="/developers/en/reference/in-person-payments/point/orders/create-order/post" color="green"} endpoint using the :toolTipComponent[test Access Token]{link="/developers/en/docs/mp-point/create-application#bookmark_access_test_credentials" linkText="Access test credentials" content="Private key of the application created in Mercado Pago, used in the backend. You can access it through Your integrations > Integration data > Tests > Test credentials. The test Access Token starts with the prefix `APP_USR`."}.
2. Store the order identifier, returned in the response to its creation under the `id` parameter.
3. Send a request to the :TagComponent{tag="POST" text="Simulate order status" href="/developers/en/reference/in-person-payments/point/orders/simulate-order/post" color="green"} endpoint, replacing the `{order_id}` in the request path with the ID of the order created in step 1. In the request body, include the `status` field with the value `canceled`.

[[[
```curl
curl -X POST \
  'https://api.mercadopago.com/v1/orders/{order_id}/events' \
  -H 'Content-Type: application/json' \
  -H 'Authorization: Bearer TEST-232********97488-12********26f67454********f4c8b49c********9526408' \
  -d '{
  "status": "canceled"
  }'
```
]]]

See the table below for descriptions of the parameters that can be sent in this request.

| Attribute | Type | Description | Possible values | Required |
|----------|------|-----------|-------------------|-----------------|
| `status` | Body. String | Final status you want to simulate for the order. | `canceled` | Required |

If the request is successful, the response will return a status `204 No Content`, with no response body.

You will receive a Webhook notification from Mercado Pago with the `action` field set to `order.canceled`. In the `transactions.payments` node, you can check the payment `status`, as shown in the example below.

Additionally, you can query the :TagComponent{tag="GET" text="Get order by ID" href="/developers/en/reference/in-person-payments/point/orders/get-order/get" color="accent"} endpoint to check the order status.

```json
{
  "action": "order.canceled",
  "api_version": "v1",
  "application_id": "123456",
  "data": {
  "external_reference": "ext_ref_1234",
  "id": "ORD01JYH1Z1YJN4HZ8J3Q0RB3YP6D",
  "status": "canceled",
  "status_detail": "canceled",
  "transactions": {
  "payments": [
  {
  "amount": "120",
  "id": "PAY01K22Y503EJ8JHGF64KGY1PZ2B",
  "status": "canceled",
  "status_detail": "canceled_on_terminal"
  }
  ]
  },
  "type": "point",
  "version": 3
  },
  "date_created": "2025-08-07T19:30:44.741479284Z",
  "live_mode": false,
  "type": "order",
  "user_id": "123456"
}
```

:::
:::AccordionComponent{title="Simulate order expiration"}

To validate that your integration correctly handles expired orders, you can simulate the `expired` status of an order.

1. Make a request to the :TagComponent{tag="POST" text="Create order" href="/developers/en/reference/in-person-payments/point/orders/create-order/post" color="green"} endpoint using the :toolTipComponent[test Access Token]{link="/developers/en/docs/mp-point/create-application#bookmark_access_test_credentials" linkText="Access test credentials" content="Private key of the application created in Mercado Pago, used in the backend. You can access it through Your integrations > Integration data > Tests > Test credentials. The test Access Token starts with the prefix `APP_USR`."}.
2. Store the order identifier, returned in the response to its creation under the `id` parameter.
3. Send a request to the :TagComponent{tag="POST" text="Simulate order status" href="/developers/en/reference/in-person-payments/point/orders/simulate-order/post" color="green"} endpoint, replacing the `{order_id}` in the request path with the order ID (`order_id`) created previously. In the request body, include the `status` field with the value `expired`.

[[[
```curl
curl -X POST \
  'https://api.mercadopago.com/v1/orders/{order_id}/events' \
  -H 'Content-Type: application/json' \
  -H 'Authorization: Bearer TEST-232********97488-12********26f67454********f4c8b49c********9526408' \
  -d '{
  "status": "expired"
  }'
```
]]]

See the table below for descriptions of the parameters that can be sent in this request.

| Attribute | Type | Description | Possible values | Required |
|----------|------|-----------|-------------------|-----------------|
| `status` | Body. String | Final status you want to simulate for the order. | `expired` | Required |

If the request is successful, the response will return a status `204 No Content`, with no response body.

You will receive a Webhook notification from Mercado Pago with the `action` field set to `order.expired`. In the `transactions.payments` node, you can check the payment `status`, as shown in the example below.

Additionally, you can query the :TagComponent{tag="GET" text="Get order by ID" href="/developers/en/reference/in-person-payments/point/orders/get-order/get" color="accent"} endpoint to check the order status.

```json
{
  "action": "order.expired",
  "api_version": "v1",
  "application_id": "123456",
  "data": {
  "external_reference": "ext_ref_1234",
  "id": "ORD01JYH1Z1YJN4HZ8J3Q0RB3YP6D",
  "status": "expired",
  "status_detail": "expired",
  "transactions": {
  "payments": [
  {
  "amount": "120",
  "id": "PAY01K22Y503EJ8JHGF64KGY1PZ2B",
  "status": "expired",
  "status_detail": "expired"
  }
  ]
  },
  "type": "point",
  "version": 3
  },
  "date_created": "2025-08-07T19:50:29.172256789Z",
  "live_mode": false,
  "type": "order",
  "user_id": "123456"
}
```

:::
:::AccordionComponent{title="Simulate action required"}

In some cases, a transaction may require an additional action from the customer at the terminal. To validate that your integration correctly handles this scenario, you can simulate the `action_required` status of an order. The simulation of this status may take up to 40 seconds to be processed.

1. Make a request to the :TagComponent{tag="POST" text="Create order" href="/developers/en/reference/in-person-payments/point/orders/create-order/post" color="green"} endpoint using the :toolTipComponent[test Access Token]{link="/developers/en/docs/mp-point/create-application#bookmark_access_test_credentials" linkText="Access test credentials" content="Private key of the application created in Mercado Pago, used in the backend. You can access it through Your integrations > Integration data > Tests > Test credentials. The test Access Token starts with the prefix `APP_USR`."}.
2. Store the order identifier, returned in the response to its creation under the `id` parameter.
3. Send a request to the :TagComponent{tag="POST" text="Simulate order status" href="/developers/en/reference/in-person-payments/point/orders/simulate-order/post" color="green"} endpoint, replacing the `{order_id}` in the request path with the order ID (`order_id`) created in step 1. In the request body, include the `status` field with the value `action_required`.

[[[
```curl
curl -X POST \
  'https://api.mercadopago.com/v1/orders/{order_id}/events' \
  -H 'Content-Type: application/json' \
  -H 'Authorization: Bearer TEST-232********97488-12********26f67454********f4c8b49c********9526408' \
  -d '{
  "status": "action_required"
  }'
```
]]]

See the table below for descriptions of the parameters that can be sent in this request.

| Attribute | Type | Description | Possible values | Required |
|----------|------|-----------|-------------------|-----------------|
| `status` | Body. String | Final status you want to simulate for the order. | `action_required` | Required |

If the request is successful, the response will return a status `204 No Content`, with no response body.

You will receive a Webhook notification from Mercado Pago with the `action` field set to `order.action_required`, indicating that an action is required at the terminal, as shown in the example below.

Additionally, you can query the :TagComponent{tag="GET" text="Get order by ID" href="/developers/en/reference/in-person-payments/point/orders/get-order/get" color="accent"} endpoint to check the order status.

```json
{
  "action": "order.action_required",
  "api_version": "v1",
  "application_id": "123456",
  "data": {
  "external_reference": "ext_ref_1234",
  "id": "ORD01JYH1Z1YJN4HZ8J3Q0RB3YP6D",
  "status": "action_required",
  "status_detail": "check_on_terminal",
  "type": "point",
  "version": 3
  },
  "date_created": "2025-06-24T13:28:36.44747706Z",
  "live_mode": false,
  "type": "order",
  "user_id": "123456"
}
```

:::

After testing all scenarios and verifying the correct functioning of your integration with Mercado Pago Point, you can [Go to production](/developers/en/docs/mp-point/go-to-production).

# Go to production

Before going to production with your Mercado Pago Point integration to your point of sale, make sure to comply with the following points.

:::::CheckboxComponent{label="Credentials" defaultChecked=false}
After testing and validating the integration, you will need to replace the :toolTipComponent[test Access Token]{link="/developers/en/docs/mp-point/create-application#bookmark_access_test_credentials" linkText="Access test credentials" content="Private key of the application created in Mercado Pago, used in the backend during integration development. You can access it in Your integrations > Integration data > Tests > Test credentials. The test Access Token starts with the prefix `APP_USR`."} used during the development and testing process with the **production Access Token** from the real account. This way, your integration will be ready to receive real payments in the production environment.

Depending on whether you are developing a self-integration or one for a third party, these **production credentials** will be different and must be obtained in different ways. Select the option that best suits your needs and follow the indicated steps to access the credentials.

::::TabsComponent

:::TabComponent{title="Get credentials for a self-integration"}

The process of obtaining credentials for a self-integration with Mercado Pago Point is based on activating the :toolTipComponent[production credentials]{content="Set of unique access keys linked to your application that allow you to receive real payments. You can access them through Your integrations > Integration data > Production > Production credentials. Use your production Public Key on the frontend and your production Access Token on the backend."} of your real account. Follow the steps below to learn how to activate them.

1. Go to [Your integrations](https://www.mercadopago[FAKER][URL][DOMAIN]/developers/panel/app) and select your application.
2. Go to the **Production credentials** section in the left side menu.
3. In the **Industry** field, select from the drop-down menu the industry or category to which the business you are integrating belongs.
4. In the **Website (optional)** field, fill in the URL of the business website.
5. Accept the [Privacy Statement](https://www.mercadopago.cl/privacidad) and the [Terms and conditions](/developers/en/docs/resources/legal/terms-and-conditions). Fill in the reCAPTCHA and click **Activate production credentials**.

When accessing production credentials, the following credential pairs will be displayed:

![How to access credentials through Your Integrations](/images/snippets/credentials-prod-panel-es-v2.jpg)

To make your Mercado Pago Point integration available in production, use your :toolTipComponent[production Access Token]{content="Private key of the application created in Mercado Pago and used in the backend in development environments and to receive real payments. You can access it through Your integrations > Integration data > Production > Production credentials."} from your real Mercado Pago account.
:::

:::TabComponent{title="Get credentials for a third-party integration"}

When integrating Mercado Pago Point for a seller, you need to securely obtain their credentials through the [OAuth protocol](/developers/en/docs/mp-point/resources/security/landing-hub), which will allow your application to access information from another Mercado Pago account.

Specifically, you must use the [Authorization code](/developers/en/docs/security/oauth/creation#bookmark_authorization_code) flow, which allows you to obtain an Access Token to use our APIs on the seller's behalf. The process requires explicit authorization, so you must redirect the seller to a URL where you will request their approval for the linkage. Follow the steps below to do so.

1. Go to [Your integrations](https://www.mercadopago[FAKER][URL][DOMAIN]/developers/panel/app) and select the previously created application with which you are integrating Mercado Pago Point.
2. In the [Integration data](/developers/en/docs/mp-point/resources/application-details), select the option to **Edit** its data.
3. Go to the **Advanced settings** section and declare a **redirect URL** where you will receive your authorization code to obtain the Access Token via OAuth. Make sure it is a static URL and uses the *`https`* protocol.

> SUCCESS_MESSAGE
>
> Optionally, from your advanced settings you can add the PKCE protocol for an extra layer of security in obtaining the code. Access the [documentation](/developers/en/docs/security/oauth/creation#bookmark_configure_pkce) for more details.

4. Complete the reCAPTCHA and click **Save changes**.
5. Now, send the authentication URL to the seller, following the scheme indicated below.

```
https://auth.mercadopago.com/authorization?client_id=APP_ID&response_type=code&platform_id=mp&state=RANDOM_ID&redirect_uri=https://www.redirect-url.com
```

| Field | Description |
|---------------|-------------|
| `client_id` | Replace `APP_ID` with your application number. You can find it in "Your integrations > [Integration data](/developers/en/docs/mp-point/resources/application-details)". |
| `state` | Replace `RANDOM_ID` with a unique identifier per attempt that does not contain sensitive information. This will help validate that the response belongs to your request. |
| `redirect_uri`| Enter the same URL you declared in the "Redirect URLs" field of your application. |

6. When the seller accesses that URL and authorizes access, they will be redirected to Mercado Pago, where they must log in and confirm the authorization.
7. Verify if the code was returned correctly in the redirect URL:

```
https://www.redirect-url.com?code=CODE&state=RANDOM_ID
```

8. Finally, send your **Client ID and Client Secret**, the authorization code returned in the `code` property and, if you have [configured PKCE](/developers/en/docs/security/oauth/creation#bookmark_configure_pkce), the `code_verifier` value to the :TagComponent{tag="POST" text="/oauth/token" href="/developers/en/reference/authentication/oauth/_oauth_token/post" color="green"} endpoint.

```curl
curl -X POST \
 'https://api.mercadopago.com/oauth/token' \
 -H 'Content-Type: application/json' \
 -d '{
  "client_secret": "client_secret",
  "client_id": "client_id",
  "grant_type": "authorization_code",
  "code": "TG-XXXXXXXX-241983636",
  "code_verifier": "47DEQpj8HBSa-_TImW-5JCeuQeRkm5NMpJWZG3hSuFU",
  "redirect_uri": "https://www.redirect-url.com?code=CODE&state=RANDOM_ID",
  "test_token": "false"
 }'
```

In the response to this request, the Access Token representing the link between accounts will be returned, with which you can make calls to our APIs on behalf of the seller.

```json
{
 "access_token": "APP_USR-4934588586838432-XXXXXXXX-241983636",
 "token_type": "bearer",
 "expires_in": 15552000,
 "scope": "read write offline_access",
 "user_id": 241983636,
 "refresh_token": "TG-XXXXXXXX-241983636",
 "public_key": "APP_USR-d0a26210-XXXXXXXX-479f0400869e",
 "live_mode": true
}
```

> WARNING
>
> This Access Token is valid for 180 days. You must renew it using the [Renew Access Token](/developers/en/docs/security/oauth/renewal) flow before expiration or you will not be able to operate with our APIs. Also save the `code` (TG-XXXXXX-XXXX) from this response and the new `refresh_token` on each renewal: if you lose them, you will need to repeat the OAuth process.

Additionally, this response will provide the `user_id` value, useful during terminal configuration.
:::
::::

<br>
<br>

Also remember to replace the test credentials with production credentials in the API calls for [payment processing](/developers/en/docs/mp-point/payment-processing).
:::::

:::CheckboxComponent{label="Create and configure new stores and POS" defaultChecked=false}
During development, the store and POS created were associated with the test account. To go to production, you must [create them again](/developers/en/docs/mp-point/configure-terminal), this time using the Access Token that corresponds to your type of integration, as indicated in the Credentials section of this same documentation.

:::
:::CheckboxComponent{label="Reassociate terminal" defaultChecked=false}
During development, the terminal was associated with the test account. When going to production, it is necessary to reassociate it with the real account that will receive payments (or with the collaborator account, as appropriate). To do this, log out of the session previously started on the terminal, and scan the QR code with the Mercado Pago mobile application logged into the corresponding production account.
:::
:::CheckboxComponent{label="Terminals in PDV mode" defaultChecked=false}
Remember that each terminal you will operate in an integrated manner must be configured in [PDV mode](/developers/en/docs/mp-point/configure-terminal#:~:text=en%20la%20terminal-,Como,-%C3%BAltimo%20paso%20de). Confirm this for each of the terminals you will use in production.
:::
:::CheckboxComponent{label="Notifications" defaultChecked=false}
Confirm in [Your integrations](/developers/panel/app) that you have [configured your production mode Webhooks notifications](/developers/en/docs/mp-point/notifications) and have indicated a production URL to receive updates about the orders.

In the case of :toolTipComponent[third-party]{content="Mercado Pago Point integrations to your system on behalf of a seller and configured using credentials obtained through the OAuth security protocol."} integrations, Webhook notifications must be configured in the **application** of the main account.
:::

:::CheckboxComponent{label="Reports" defaultChecked=false}
[Mercado Pago reports](/developers/en/docs/reports/introduction) provide information to track account transactions, such as available balance, movements, and liquidity. This facilitates reconciliation of sales and other operations with internal management systems.

While they are optional, we recommend using reports to improve business financial management once you go to production.
:::

# Status of an order and a transaction

When processing orders with Mercado Pago Point, it’s important to understand how the processing flow works and which status an order and a transaction can take at any given time.

Below, you can view the flow of an order for card payments and then an informative table about each of the possible `status`, including their respective `status_detail`.

<pre class="mermaid">
stateDiagram-v2
  [*] --> created

  created --> expired: It was not processed within 15 minutes after its creation
  created --> canceled: Canceled via API
  created --> at_terminal

  at_terminal --> canceled: Canceled via terminal / Canceled after API request confirmation
  at_terminal --> processed: Processed successfully
  at_terminal --> failed: Payment declined / Payment component failure / EMV reversal
  at_terminal --> action_required: After 40s of processing start
  at_terminal --> expired: Expired while at terminal

  processed --> refunded: Full refund via API, activity, or terminal

  created: created
  expired: expired
  canceled: canceled
  at_terminal: at_terminal
  processed: processed
  failed: failed
  action_required: action_required
  refunded: refunded
</pre>

## Order status

Check the list of `status` and `status_detail` that an order can take.

| `status` | `status_detail` | Description |
|---|---|---|
| `created` | `created` | The order was successfully created but has not yet been captured by the terminal. |
| `processed` | `processed` | The order was successfully processed and the payment was credited. |
| `processed` | `partially_refunded` | The order was partially refunded. This means that the requested transaction amount was returned to the payer. |
| `action_required` | `action_required` | The transaction associated with the order needs to be confirmed. Check the terminal to verify the final status and make sure to update your system accordingly, as this status will not change. |
| `at_terminal` | `at_terminal` | The order was captured by the terminal and is ready to be processed. |
| `failed` | `failed` | The order has failed. This means the transaction was not successful and will not be completed. |
| `refunded` | `refunded` | The order was refunded. This means the transaction amount was fully returned to the payer. |
| `expired` | `expired` | The order expired after more than 15 minutes without being paid. If you wish to complete the payment, a new order must be created. |

## Transaction status

Check the list of `status` and `status_detail` that a transaction can take.

| `status` | `status_detail` | Description |
|---|---|---|
| `created` | `created` | The transaction was successfully created, but it has not yet been processed. This is the initial state of a transaction after it is created. |
| `processed` | `accredited` | The transaction was successfully processed and the amount has been effectively credited. |
| `action_required` | `waiting_payment` | The transaction requires an additional action and is waiting for payment. This means the transaction has been initiated, but the payment has not yet been completed. |
| `action_required` | `check_on_terminal` | The transaction requires confirmation on the terminal to check whether the payment was approved or rejected. |
| `at_terminal` | `at_terminal` | The transaction was received by the terminal and is ready to be processed. |
| `at_terminal` | `cancellation_requested` | The order cancellation request was accepted, but cancellation will only be completed after a [cancellation webhook notification](/developers/en/docs/mp-point/notifications) is received. |
| `expired` | `expired` | The transaction has expired. This means it was not completed within the allowed time and was therefore terminated. |
| `refunded` | `refunded` | The order has been refunded. This means the amount of the transaction has been fully returned to the payer. |
| `canceled` | `canceled` | The transaction was canceled and will not be completed. |
| `canceled` | `canceled_by_api` | The transaction was canceled via the API and will not be completed. |
| `canceled` | `canceled_on_terminal` | The transaction was canceled from the terminal and will not be completed. |
| `failed` | `failed` | A failure occurred while processing the order. This may have been caused by incorrect data submission, fraud risk, or rejection by the card issuer. |
| `failed` | `bad_filled_card_data` | The transaction failed due to incorrectly filled card data. This may include information such as card number, CVV, expiration date, among others. |
| `failed` | `high_risk` | The transaction failed due to high risk detection. This can happen when the fraud detection system identifies a potential risk in the transaction. |
| `failed` | `rejected_by_issuer` | The transaction failed due to rejection by the card issuer. |
| `failed` | `required_call_for_authorize` | The transaction failed because a call for authorization is required. This may occur when the card issuer requires additional verification before approving the transaction. |
| `failed` | `max_attempts_exceeded` | The transaction failed because the maximum number of attempts was exceeded. This can happen when the number of payment attempts goes beyond the system's allowed limit. |
| `failed` | `card_disabled` | The transaction failed because the card is disabled. This may occur when the card has been blocked or deactivated by the issuer. |
| `failed` | `insufficient_amount` | The transaction failed due to insufficient funds. This may happen when the available balance is not enough to cover the transaction amount. |
| `failed` | `amount_limit_exceeded` | The transaction failed because the amount exceeded the allowed limit. This can happen when the transaction amount surpasses the threshold set by the issuer or the system. |
| `failed` | `processing_error` | The transaction failed due to a processing error. This may happen when a technical issue or system error prevents completion. If the problem persists, contact support and provide the `x-request-id` along with details of the operation. |
| `failed` | `invalid_installments` | The transaction failed due to invalid installments. This can happen when the selected number of installments is not accepted by the card issuer or the system. |
| `failed` | `in_review` | The transaction failed and its status is unknown or contains sensitive information. |

# MD for: https://www.mercadopago.cl/developers/en/docs/mp-point/resources/migrate-payment-intent-to-orders.md

\# How to migrate from the Payment Intent API to the Orders API The Orders API unifies in-person payment processing for Mercado Pago Point, providing standardized endpoints, a more complete status model, and new native capabilities that did not exist in the Payment Intent API. In addition, all new Mercado Pago features will be developed on the Orders API. Migrating your Mercado Pago Point integration from the Payment Intent API to the Orders API involves \*\*updating endpoints and request fields\*\*, \*\*adapting the status model\*\*, and leveraging \*\*new native resources\*\*. The new API introduces self-contained statuses, configurable order expiration (\`expiration\_time\`), and a dedicated refund endpoint. The migration does not change the business flow: the terminal continues receiving orders created by the backend and processing payments autonomously. Read on to learn how to complete this migration. ## Map the endpoint changes Before starting the migration steps, see the table below for an overview of all endpoint changes. In the Payment Intent API, each operation had its own URL structure with the device identifier in the path. The Orders API consolidates these operations into standardized endpoints and removes the \`{deviceid}\` from the path in all operations. | Operation | Payment Intent API | Orders API | |---|---|---| | List terminals | :TagComponent{tag="GET" text="GET /point/integration-api/devices" href="/developers/en/reference/integrations\_api/\_point\_integration-api\_devices/get" color="accent"} | :TagComponent{tag="GET" text="GET /terminals/v1/list" href="/developers/en/reference/in-person-payments/point/terminals/get-terminals/get" color="accent"} | | Update terminal operating mode | :TagComponent{tag="PATCH" text="PATCH /point/integration-api/devices/{device\_id}" href="/developers/en/reference/integrations\_api/\_point\_integration-api\_devices\_device-id/patch" color="gray"} | :TagComponent{tag="PATCH" text="PATCH /terminals/v1/setup" href="/developers/en/reference/in-person-payments/point/terminals/update-operation-mode/patch" color="gray"} | | Create payment intent vs. Create order | :TagComponent{tag="POST" text="POST /point/integration-api/devices/{deviceid}/payment-intents" href="/developers/en/reference/integrations\_api/\_point\_integration-api\_devices\_deviceid\_payment-intents/post" color="green"} | :TagComponent{tag="POST" text="POST /v1/orders" href="/developers/en/reference/in-person-payments/point/orders/create-order/post" color="green"} | | Get payment intent vs. Get order | :TagComponent{tag="GET" text="GET /point/integration-api/payment-intents/{paymentintentid}" href="/developers/en/reference/integrations\_api/\_point\_integration-api\_payment-intents\_paymentintentid/get" color="accent"} | :TagComponent{tag="GET" text="GET /v1/orders/{orderid}" href="/developers/en/reference/in-person-payments/point/orders/get-order/get" color="accent"} | | Cancel payment intent vs. Cancel order | :TagComponent{tag="DELETE" text="DELETE /point/integration-api/devices/{deviceid}/payment-intents/{paymentintentid}" href="/developers/en/reference/integrations\_api/\_point\_integration-api\_devices\_deviceid\_payment-intents\_paymentintentid/delete" color="red"} | :TagComponent{tag="POST" text="POST /v1/orders/{orderid}/cancel" href="/developers/en/reference/in-person-payments/point/orders/cancel-order/post" color="green"} | | Refund order | No dedicated endpoint existed | :TagComponent{tag="POST" text="POST /v1/orders/{orderid}/refund" href="/developers/en/reference/in-person-payments/point/orders/refund-order/post" color="green"} | ## Adapt the headers The Orders API introduces two mandatory header changes that affect all endpoints: the sandbox mechanism was removed and a new idempotency control was introduced. Apply the following changes before testing any other resource. :::AccordionComponent{title="Remove the x-test-scope header" pill="1"} The \`x-test-scope: sandbox\` header was used in the Payment Intent API to identify test requests. In the Orders API, the sandbox mechanism was restructured and this header no longer exists. Remove it from all integration requests. To operate in a test environment with the Orders API, use test users. See the \[integration test documentation\](https://www.mercadopago.cl/developers/en/docs/mp-point/integration-test) for more information. ::: :::AccordionComponent{title="Add the X-Idempotency-Key header" pill="2"} The \`X-Idempotency-Key\` header is required for order creation, cancellation, and refund operations. It ensures that a repeated request with the same key returns the original result without processing the operation again. Send a unique UUID v4 or random string per request. GET operations do not require this header. > WARNING > > If the same \`X-Idempotency-Key\` is reused with a different body, the API will return the \`idempotency\_key\_already\_used\` error. Generate a new key for each distinct operation. ::: ## Update terminal listing and configuration The terminal endpoints changed URL: listing moves from \`GET /point/integration-api/devices\` to \`GET /terminals/v1/list\` and mode update moves from \`PATCH /point/integration-api/devices/{device\_id}\` to \`PATCH /terminals/v1/setup\`. In the mode update, the terminal identifier also moves from the path to the body, inside the \`terminals\[\]\` array. Currently, the array accepts a single element, so you can only update one terminal per request. :::AccordionComponent{title="Migrate the terminal listing" pill="1"} In the Payment Intent API, devices were returned in the \`devices\` array. In the Orders API, they move to \`data.terminals\`. The query params \`store\_id\`, \`pos\_id\`, \`limit\`, and \`offset\` remain the same. The table below describes the response changes. | Payment Intent API | Orders API | Description | Change | |---|---|---|---| | \`devices\[\]\` | \`data.terminals\[\]\` | List of terminals associated with the account. In the Payment Intent API, it was returned as a direct array in \`devices\`. In the Orders API, it is moved inside the \`data\` object and renamed to \`terminals\`. | Renamed and moved inside the \`data\` object. | | \`devices\[\].id\` | \`data.terminals\[\].id\` | Unique terminal identifier. The last characters match the serial number on the back label of the terminal. | Same concept. The ID format may vary depending on the terminal model. | | \`devices\[\].pos\_id\` | \`data.terminals\[\].pos\_id\` | Identifier of the point of sale associated with the terminal. | No changes. | | \`devices\[\].store\_id\` (integer) | \`data.terminals\[\].store\_id\` (string) | Identifier of the store associated with the terminal. In the Payment Intent API, it was returned as integer. In the Orders API, it is returned as string. | Changes from integer to string. | | \`devices\[\].external\_pos\_id\` | \`data.terminals\[\].external\_pos\_id\` | External point of sale identifier, defined by the integrator. | No changes. | | \`devices\[\].operating\_mode\` | \`data.terminals\[\].operating\_mode\` | Terminal operating mode. In the Payment Intent API, the possible values are \`PDV\` and \`STANDALONE\`. In the Orders API, the \`UNDEFINED\` value is added for unrecognized configurations. | Adds the \`UNDEFINED\` value for unrecognized configurations. | | \`paging.total\` / \`paging.offset\` / \`paging.limit\` | \`paging.total\` / \`paging.offset\` / \`paging.limit\` | Listing pagination data: total records, start point, and limit. | No changes. | In the terminal listing, errors are grouped by type of change. See the tables below for more details. ### Errors not documented in the Orders API The following errors exist in the Payment Intent API but are not documented in the Orders API. | HTTP | Payment Intent API | Note | |---|---|---| | \`400\` | \`bad\_request\` | Required parameter missing or with incorrect format. | | \`400\` | \`bad\_request\` | Invalid request format. | | \`403\` | \`forbidden\` | Present in the Payment Intent API. | ### Errors that remain unchanged The following errors have the same behavior in both APIs. | HTTP | Error | Note | |---|---|---| | \`401\` | \`unauthorized\` | Invalid or expired token. | | \`500\` | \`internal\_error\` | Internal error. Check the response and retry. | ::: :::::AccordionComponent{title="Migrate the operating mode update" pill="2"} In the Payment Intent API, the terminal identifier was sent in the path. In the Orders API, the identifier moves to the body inside the \`terminals\[\]\` array. Currently, the array accepts a single element, so you can only update one terminal per request. Below is a comparative example of an operating mode update. ::::TabsComponent :::TabComponent{title="Payment Intent API"} Operating mode update via the Payment Intent API. The terminal identifier is sent as a path param. \`\`\`curl curl -X PATCH \\ 'https://api.mercadopago.com/point/integration-api/devices/{{DEVICE\_ID}}' \\ -H 'Authorization: Bearer {{ACCESS\_TOKEN}}' \\ -d '{ "operating\_mode": "PDV" }' \`\`\` ::: :::TabComponent{title="Orders API"} Update via the Orders API. The terminal identifier goes in the body, inside the \`terminals\[\]\` array. \`\`\`curl curl -X PATCH \\ 'https://api.mercadopago.com/terminals/v1/setup' \\ -H 'Authorization: Bearer {{ACCESS\_TOKEN}}' \\ -d '{ "terminals": \[ { "id": "{{TERMINAL\_ID}}", "operating\_mode": "PDV" } \] }' \`\`\` ::: :::: In the Payment Intent API, the response returns only the \`operating\_mode\` field. In the Orders API, the response returns the \`terminals\[\]\` array with \`id\` and \`operating\_mode\`, identifying each updated terminal. See the table below for the complete mapping. | Payment Intent API | Orders API | Description | Change | |---|---|---|---| | \`operating\_mode\` | \`terminals\[\].operating\_mode\` | Operating mode defined for the terminal. In the Payment Intent API, it was returned as a single field. In the Orders API, it is returned inside the \`terminals\[\]\` array. The possible values are \`PDV\` and \`STANDALONE\`. | Moves inside the \`terminals\[\]\` array. | The Orders API also introduces the following field with no equivalent in the Payment Intent API. | Field | Description | |---|---| | \`terminals\[\].id\` | Unique identifier of the updated terminal. It is returned only in the Orders API. | In the operating mode update, errors are grouped by type of change. See the tables below for more details. ### Errors that disappear The following error exists in the Payment Intent API but was removed in the Orders API. | HTTP | Payment Intent API | Note | |---|---|---| | \`424\` | \`failed\_dependency\` | Code removed in the Orders API. | ### Renamed errors The following error was renamed in the Orders API. | HTTP | Payment Intent API | Orders API | Note | |---|---|---|---| | \`403\` | \`forbidden\` | \`store\_pos\_not\_found\` | Terminal has no associated store or point of sale. | ### Errors that change behavior The following error exists in both APIs but with a different meaning in the Orders API. | HTTP | Payment Intent API | Orders API | Note | |---|---|---|---| | \`400\` | \`bad\_request\` | \`property\_value\` | Invalid \`device\_id\` or \`operating\_mode\` value. | ### Errors that remain unchanged The following errors have the same behavior in both APIs. | HTTP | Error | Note | |---|---|---| | \`401\` | \`unauthorized\` | Invalid or expired token. | | \`500\` | \`internal\_error\` | Internal error. Retry the request. | ### Errors introduced by the Orders API The following errors have no equivalent in the Payment Intent API. | HTTP | Orders API error | Note | |---|---|---| | \`400\` | \`unsupported\_site\` | Invalid site. | | \`400\` | \`required\_properties\` | Required property missing. | | \`400\` | \`unsupported\_properties\` | Unsupported field sent. | | \`400\` | \`invalid\_payload\` | Invalid payload. Check the submitted fields. | | \`403\` | \`terminal\_not\_allowed\_action\` | Action not allowed for this terminal model. | | \`404\` | \`not\_found\` | Resource not found or invalid ID. | | \`412\` | (no string code) | Operation not allowed: a terminal is already associated with the point of sale in PDV mode. Only one terminal per point of sale is allowed in PDV mode. | ::::: ## Migrate payment intent creation to order creation The creation endpoint changes from \`POST /point/integration-api/devices/{deviceid}/payment-intents\` to \`POST /v1/orders\`. Beyond the URL change, the request structure was significantly reorganized: the terminal identifier moves from the path to the body, new required fields were introduced, and the Orders API has a distinct structure. Follow the steps below to adapt the request, response, and error handling. \`\`\`curl curl -X POST \\ 'https://api.mercadopago.com/v1/orders' \\ -H 'Content-Type: application/json' \\ -H 'X-Idempotency-Key: {{IDEMPOTENCY\_KEY}}' \\ -H 'Authorization: Bearer {{ACCESS\_TOKEN}}' \\ -d '{ "type": "point", "external\_reference": "ext\_ref\_1234", "transactions": { "payments": \[ { "amount": "24.00" } \] }, "config": { "point": { "terminal\_id": "{{TERMINAL\_ID}}", "print\_on\_terminal": "no\_ticket" } }, "description": "Point Smart 2" }' \`\`\` :::::AccordionComponent{title="Map the request body fields" pill="1"} The Orders API has a different structure from the Payment Intent API: the terminal identifier must be sent in the body, payment and printing configuration fields are placed in new nodes, and identification headers become part of the body. The new required fields are \`type\` (with value \`"point"\`) and \`external\_reference\`. See the table below for the complete field mapping. Below is a comparative example between creating a payment intent and creating an order, followed by the complete field mapping table. ::::TabsComponent :::TabComponent{title="Payment Intent API"} Request to create a payment intent. The terminal identifier is sent as a path param and \`amount\` is an integer value. \`\`\`curl curl -X POST \\ 'https://api.mercadopago.com/point/integration-api/devices/{{DEVICE\_ID}}/payment-intents' \\ -H 'Authorization: Bearer {{ACCESS\_TOKEN}}' \\ -H 'x-test-scope: sandbox' \\ -d '{ "amount": 1500, "additional\_info": { "external\_reference": "order-ref-001", "print\_on\_terminal": true }, "description": "Test product" }' \`\`\` ::: :::TabComponent{title="Orders API"} Request to create an order. The terminal identifier goes in the body and \`type: "point"\` is required. \`\`\`curl curl -X POST \\ 'https://api.mercadopago.com/v1/orders' \\ -H 'Authorization: Bearer {{ACCESS\_TOKEN}}' \\ -H 'X-Idempotency-Key: {{IDEMPOTENCY\_KEY}}' \\ -d '{ "type": "point", "external\_reference": "order-ref-001", "description": "Test product", "config": { "point": { "terminal\_id": "{{TERMINAL\_ID}}", "print\_on\_terminal": "seller\_ticket" } }, "transactions": { "payments": \[ { "amount": "15" } \] } }' \`\`\` ::: :::: | Payment Intent API | Orders API | Description | Change | |---|---|---|---| | \`{deviceid}\` (path param) | \`config.point.terminal\_id\` | Identifies the terminal that will receive the order. In the Payment Intent API, it is sent as a path parameter. In the Orders API, it is sent in the body in the format \`{terminal\_type}\_\_{terminal\_serial}\`. | Moves from path param to body field. | | \`amount\` (integer) | \`transactions.payments\[\].amount\` (string) | Amount to charge. In the Payment Intent API, it is represented as an integer with implicit two decimals (e.g.: \`1500\` for $15.00). In the Orders API, it is represented as a string inside the \`transactions.payments\` array. Decimal values are not accepted (e.g.: \`"15"\`). Only 1 transaction per order is allowed when \`type\` is \`point\`. | Changes from integer to string and enters the \`transactions.payments\` array. | | \`additional\_info.external\_reference\` | \`external\_reference\` | Alphanumeric identifier for the transaction in the integrator's system, returned in webhook notifications. In the Orders API, it is required, with a maximum of 64 characters, only letters, numbers, \`-\` and \`\_\`. Must be unique per order and cannot contain PII data. | Moves to root level and becomes \*\*required\*\*. | | \`additional\_info.print\_on\_terminal\` (boolean) | \`config.point.print\_on\_terminal\` (string) | Controls ticket printing on the terminal. In the Payment Intent API, it accepts the boolean values \`true\` and \`false\`. In the Orders API, it accepts the values \`seller\_ticket\` (prints) and \`no\_ticket\` (does not print). Default value: \`seller\_ticket\`. | Changes from boolean to enum string. | | \`payment.type\` | \`config.payment\_method.default\_type\` | Defines the payment method accepted by the terminal. In the Payment Intent API, the possible values are \`credit\_card\`, \`debit\_card\`, and \`voucher\_card\`. In the Orders API, the possible values are \`credit\_card\`, \`debit\_card\`, and \`qr\`. If not sent, the terminal accepts all payment methods. | Changes node and now also accepts \`qr\`. | | \`description\` | \`description\` | Describes the product, service, or payment reason. In the Orders API, it accepts up to 150 characters. | No changes. | | \`X-platform-id\` (header) | \`integration\_data.platform\_id\` | Identifies the integration platform, assigned by Mercado Pago. In the Payment Intent API, it was sent as a header. In the Orders API, it is sent in the body inside \`integration\_data\`. | Moves from header to body. | | \`X-integrator-id\` (header) | \`integration\_data.integrator\_id\` | Identifies the integrator, assigned by Mercado Pago. In the Payment Intent API, it was sent as a header. In the Orders API, it is sent in the body inside \`integration\_data\`. | Moves from header to body. | The Orders API also introduces the following fields with no equivalent in the Payment Intent API. | Field | Description | |---|---| | \`integration\_data.sponsor.id\` | USER\_ID of the Mercado Pago account of the integrating system. | | \`type\` | Order type. For Point, the only accepted value is \`"point"\`. \*\*Required.\*\* | | \`expiration\_time\` | Defines the order validity period from creation, in ISO 8601 format. The minimum value is \`PT30S\` (30 seconds), the maximum value is \`PT3H\` (3 hours) and the default value is \`PT15M\` (15 minutes). Examples: \`PT30S\` for 30 seconds, \`PT10M\` for 10 minutes, \`PT1H15M\` for 1 hour and 15 minutes. If the order expires without being processed, it is automatically canceled. \*\*Optional.\*\* | The order ID format changes from UUID (e.g.: \`7f25f9aa-eea6-...\`) to alphanumeric (e.g.: \`ORD00001111222233334444555566\`). Update any storage or query logic that depends on the ID format before proceeding. > SUCCESS\_MESSAGE > > Check all available parameters in the :TagComponent{tag="API" text="API Reference" href="/developers/en/reference/in-person-payments/point/orders/create-order/post"}. ::::: :::AccordionComponent{title="Adapt the creation response fields" pill="2"} The table below shows the creation response fields that existed in both APIs and were updated during the migration. | Payment Intent API | Orders API | Description | Change | |---|---|---|---| | \`id\` (UUID) | \`id\` (alphanumeric) | Order identifier, generated by Mercado Pago. In the Payment Intent API, it is returned in UUID format. In the Orders API, it is returned in alphanumeric format with \`ORD\` prefix. | ID format changes to \`ORD...\`. | | \`device\_id\` | \`config.point.terminal\_id\` | Identifier of the terminal that received the order. | Moves to \`config.point\`. | | \`amount\` (integer) | \`transactions.payments\[\].amount\` (string) | Payment amount. In the Payment Intent API, it is returned as an integer. In the Orders API, it is returned as a decimal string inside the payments array. | Moves to the payments array. | | \`additional\_info.external\_reference\` | \`external\_reference\` | External reference of the order in the integrator's system. | Moves to root level. | | \`additional\_info.print\_on\_terminal\` (boolean) | \`config.point.print\_on\_terminal\` (string) | Indicates whether the terminal printed the ticket. In the Payment Intent API, it is returned as a boolean. In the Orders API, it is returned as an enum string: \`seller\_ticket\` or \`no\_ticket\`. | Changes from boolean to enum string. | | \`additional\_info.ticket\_number\` | \`config.point.ticket\_number\` | Alphanumeric value to identify the invoice or ticket number, printed on the terminal when printing is enabled. | Moves to \`config.point\`. | The Orders API also introduces the following fields with no equivalent in the Payment Intent API. | Field | Description | |---|---| | \`status\` | Current order status. On creation: \`created\`. | | \`status\_detail\` | Order status detail. On creation: \`created\`. | | \`type\` | Order type. For Point: always \`point\`. | | \`expiration\_time\` | Order validity period in ISO 8601 format. If the order expires without being processed, it is automatically canceled. | | \`created\_date\` / \`last\_updated\_date\` | Records the order creation and last update dates in \`yyyy-MM-ddTHH:mm:ss.sssZ\` format. | | \`transactions.payments\[\].id\` | Payment transaction identifier, generated by Mercado Pago. Required for partial refunds. | | \`transactions.payments\[\].status\` | Payment transaction status. On creation: \`created\`. | | \`user\_id\` | Identifier of the Mercado Pago user who created the order. | | \`country\_code\` | Application site/country identifier. | | \`integration\_data.application\_id\` | Mercado Pago application identifier. | | \`integration\_data.platform\_id\` | Platform identifier, assigned by Mercado Pago. | | \`integration\_data.integrator\_id\` | Integrator identifier, assigned by Mercado Pago. | | \`integration\_data.sponsor.id\` | USER\_ID of the integrating system. | ::: :::AccordionComponent{title="Update error handling in creation" pill="3"} In creation, errors are grouped by type of change. See the tables below for more details. ### Errors that change behavior In the Payment Intent API, the following errors returned the generic \`bad\_request\` code. In the Orders API, they are replaced by specific codes. | HTTP | Payment Intent API | Orders API | Note | |---|---|---|---| | \`400\` | \`bad\_request\` | \`required\_properties\` | Required property missing. | | \`400\` | \`bad\_request\` | \`property\_value\` | Invalid value in a property. | | \`400\` | \`bad\_request\` | \`property\_type\` | Incorrect type. For example: integer instead of string. | | \`400\` | \`bad\_request\` | \`json\_syntax\_error\` | Invalid JSON. | | \`400\` | \`bad\_request\` | \`unsupported\_properties\` | Unsupported property sent. | ### Renamed errors The following errors were renamed in the Orders API. | HTTP | Payment Intent API | Orders API | Note | |---|---|---|---| | \`403\` | \`forbidden\` | \`forbidden\_checking\_terminal\_owner\` | Terminal not linked to the account. | | \`409\` | \`conflict\_error\` | \`already\_queued\_order\_for\_terminal\` | An order is already queued for this terminal. | ### Errors that disappear The following error exists in the Payment Intent API but was removed in the Orders API. | HTTP | Payment Intent API | Note | |---|---|---| | \`424\` | \`failed\_dependency\` | Code removed in the Orders API. | ### Errors that remain unchanged The following error has the same behavior in both APIs. | HTTP | Error | Note | |---|---|---| | \`401\` | \`unauthorized\` | Invalid or expired token. | | \`500\` | \`internal\_error\` | Internal error. Check the response and retry the request. | ### Errors introduced by the Orders API The following errors have no equivalent in the Payment Intent API. | HTTP | Orders API error | Note | |---|---|---| | \`400\` | \`empty\_required\_header\` | \`X-Idempotency-Key\` missing. | | \`400\` | \`minimum\_properties\` | Minimum number of required properties not sent. | | \`400\` | \`minimum\_items\` / \`maximum\_items\` | Invalid number of items in the \`transactions.payments\` array. | | \`409\` | \`idempotency\_key\_already\_used\` | Idempotency key reused with a different body. | | \`500\` | \`idempotency\_validation\_failed\` | Idempotency validation failure. Retry the request. | ::: ## Update the query mechanism from Payment Intent to Orders The query endpoint changes from :TagComponent{tag="GET" text="GET /point/integration-api/payment-intents/{paymentintentid}" href="/developers/en/reference/integrations\_api/\_point\_integration-api\_payment-intents\_paymentintentid/get" color="accent"} to :TagComponent{tag="GET" text="GET /v1/orders/{orderid}" href="/developers/en/reference/in-person-payments/point/orders/get-order/get" color="accent"}. The order identifier in the path also changes from UUID to alphanumeric format. The response includes new fields with information about the payment result, refunds, and card data. \`\`\`curl curl -X GET \\ 'https://api.mercadopago.com/v1/orders/{{ORDER\_ID}}' \\ -H 'Content-Type: application/json' \\ -H 'Authorization: Bearer {{ACCESS\_TOKEN}}' \`\`\` :::AccordionComponent{title="Adapt the query response fields" pill="1"} In addition to the fields documented in the creation response, the \*\*GET\*\* response includes additional fields relevant to the migration. See the table below for details. | Payment Intent API | Orders API | Description | Change | |---|---|---|---| | \`state\` | \`status\` | Order status. In the Payment Intent API, \`state\` field with uppercase values. In the Orders API, \`status\` field with lowercase values and an expanded set of statuses. | Renamed. See the complete mapping in \[Update status handling\](#bookmark\_update\_status\_handling). | | \`payment.id\` (integer) | \`transactions.payments\[\].reference\_id\` (string) | Identifier of the processed payment, available when the flow completes successfully. In the Payment Intent API, it was returned as an integer in \`payment.id\`. In the Orders API, it is returned as a string in \`transactions.payments\[\].reference\_id\`. | Processed payment identifier. Changes from integer to string. | The Orders API also introduces the following fields with no equivalent in the Payment Intent API. | Field | Description | |---|---| | \`status\_detail\` | Order status detail. Possible values: \`accredited\`, \`canceled\_by\_api\`, \`bad\_filled\_card\_data\`, \`insufficient\_amount\`, among others. See the :TagComponent{tag="GET" text="API Reference" href="/developers/en/reference/in-person-payments/point/orders/get-order/get" color="accent"} for the complete list. | | \`transactions.payments\[\].paid\_amount\` | Amount effectively paid in the transaction. | | \`transactions.payments\[\].refunded\_amount\` | Amount refunded in the transaction. | | \`transactions.payments\[\].status\` | Payment transaction status. | | \`transactions.payments\[\].status\_detail\` | Transaction status detail. Same possible values as \`status\_detail\` of the order. | | \`transactions.payments\[\].payment\_method.type\` | Payment method used in the transaction (e.g.: \`credit\_card\`, \`debit\_card\`). | | \`transactions.payments\[\].payment\_method.installments\` | Number of installments selected in the transaction. | | \`transactions.payments\[\].payment\_method.id\` | Payment method or card brand identifier. See :TagComponent{tag="GET" text="GET /v1/payment\_methods" href="/developers/en/reference/online-payments/checkout-api/payment-methods/get" color="accent"}. | | \`transactions.payments\[\].card.first\_digits\` / \`last\_digits\` | First and last digits of the card used in the transaction, available when payment was made by card. | | \`transactions.refunds\[\]\` | Array with the refund data for the order (\`id\`, \`transaction\_id\`, \`reference\_id\`, \`amount\`, \`status\`). | ::: :::AccordionComponent{title="Update error handling in query" pill="2"} In the query, errors are grouped by type of change. See the tables below for more details. ### Errors that disappear The following errors exist in the Payment Intent API but have no equivalent in the Orders API. | HTTP | Payment Intent API | Note | |---|---|---| | \`401\` | \`unauthorized\` (Unauthorized use of live credentials) | The \`x-test-scope\` header was removed in the Orders API. | | \`403\` | \`forbidden\` | Terminal ownership validation occurs only during creation. | | \`429\` | \`too\_many\_requests\` | Present in the Payment Intent API. Not documented in the Orders API. | ### Renamed errors The following error was renamed in the Orders API. | HTTP | Payment Intent API | Orders API | Note | |---|---|---|---| | \`404\` | \`not\_found\` | \`order\_not\_found\` | Order not found. Verify that the submitted ID is correct. | ### Errors that change behavior The following error exists in both APIs but with a different meaning in the Orders API. | HTTP | Payment Intent API | Orders API | Note | |---|---|---|---| | \`400\` | \`bad\_request\` | \`bad\_request\` | Invalid \`order\_id\` format. The ID changes from UUID to alphanumeric. | ### Errors that remain unchanged The following errors have the same behavior in both APIs. | HTTP | Error | Note | |---|---|---| | \`401\` | \`unauthorized\` | Invalid or expired token. | | \`500\` | \`internal\_error\` | Internal error. Retry the request. | ::: ## Update status handling One of the most significant changes between the Payment Intent API and the Orders API is the \`state\` field, which is renamed to \`status\` in the new API and receives new values. In the Payment Intent API, the \`FINISHED\` status required additional calls to determine the actual payment result. In the Orders API, the \`processed\` and \`failed\` statuses are self-contained and eliminate that need. Update all status checks in your integration according to the table below. :::AccordionComponent{title="Map status values" pill="1"} | Payment Intent API (\`state\`) | Orders API (\`status\`) | Note | |---|---|---| | \`OPEN\` | \`created\` | Renamed | | \`ON\_TERMINAL\` | \`at\_terminal\` | Renamed | | \`PROCESSING\` | Absorbed | No intermediate status in the Orders API | | \`PROCESSED\` | Absorbed | No intermediate status in the Orders API | | \`FINISHED\` (approved payment) | \`processed\` | The approved payment result is contained in the order itself, without requiring additional queries. | | \`FINISHED\` (rejected payment) | \`failed\` | The rejected payment result is contained in the order itself, without requiring additional queries. | | \`CONFIRMATION\_REQUIRED\` | \`action\_required\` | Renamed | | \`ERROR\` | \`failed\` | Renamed | | \`ABANDONED\` | \`expired\` | Renamed (timeout-based) | | \`CANCELED\` | \`canceled\` | Same meaning. Now lowercase | In the Payment Intent API, confirming the result of a payment with \`state: FINISHED\` required inspecting \`payment.state\` in the webhook, calling \`GET /v1/payments/{id}\`, or searching by \`external\_reference\`. In the Orders API, the \`processed\` and \`failed\` statuses are self-contained: the payment result is available directly in the order, without additional queries. The Orders API also introduces the following status with no equivalent in the Payment Intent API. | Status (Orders API) | Note | |---|---| | \`refunded\` | \*\*New status.\*\* It must be handled explicitly in all flows. | ::: ## Update the webhook notification topic In the Payment Intent API, notifications were sent through the \`point\_integration\_wh\` topic. In the Orders API, they move to the \*\*Order (Mercado Pago)\*\* (\`orders\`) topic. Before going to production, update your application settings in \[Your integrations\](https://www.mercadopago.cl/developers/panel/app). To do so, select the \*\*"Order (Mercado Pago)"\*\* topic and deactivate the \`point\_integration\_wh\` topic. For more information, see the \[Configure notifications\](https://www.mercadopago.cl/developers/en/docs/mp-point/notifications) documentation. ## Update order cancellation The new endpoint to cancel an order is \`POST /v1/orders/{orderid}/cancel\`, replacing the \`DELETE\` from the Payment Intent API. The \`{deviceid}\` is removed from the path and the cancellation is now identified solely by the \`{orderid}\`. In the Payment Intent API, it was only possible to cancel payment intents that had not yet reached the terminal. In the Orders API, it is possible to cancel an order even after it has reached the terminal, using a new specific header. \`\`\`curl curl -X POST \\ 'https://api.mercadopago.com/v1/orders/{{ORDER\_ID}}/cancel' \\ -H 'Content-Type: application/json' \\ -H 'X-Idempotency-Key: {{IDEMPOTENCY\_KEY}}' \\ -H 'Authorization: Bearer {{ACCESS\_TOKEN}}' \`\`\` :::AccordionComponent{title="Adapt cancellation headers" pill="1"} The response now returns the complete order object with \`status: "canceled"\`, instead of just the \`id\`. The headers required for this operation are: | Header | Required | Description | |---|---|---| | \`X-Idempotency-Key\` | Required | Unique key per request | | \`x-allow-cancelable-status\` | Conditional | Required to cancel orders in \`at\_terminal\`. Value: \`"at\_terminal"\` | To cancel orders with \`at\_terminal\` status, send the \`x-allow-cancelable-status: at\_terminal\` header. Without this header, only orders with \`status: created\` will be canceled. ::: :::AccordionComponent{title="Update error handling in cancellation" pill="2"} In cancellation, errors are grouped by type of change. See the tables below for more details. ### Errors that disappear The following errors exist in the Payment Intent API but have no equivalent in the Orders API. | HTTP | Payment Intent API | Note | |---|---|---| | \`400\` | \`bad\_request\` (deviceID format) | \`deviceid\` was removed from the path in the Orders API. | | \`429\` | \`too\_many\_requests\` | Present in the Payment Intent API. Not documented in the Orders API. | ### Renamed errors The following error was renamed in the Orders API. | HTTP | Payment Intent API | Orders API | Note | |---|---|---|---| | \`409\` | \`conflict\_error\` | \`cannot\_cancel\_order\` | Order status does not allow cancellation. For \`at\_terminal\`, send \`x-allow-cancelable-status: at\_terminal\`. | ### Errors that change behavior The following errors exist in both APIs but with different behavior in the Orders API. | HTTP | Payment Intent API | Orders API | Note | |---|---|---|---| | \`400\` | \`bad\_request\` | \`bad\_request\` | Invalid \`order\_id\` format. The ID changes from UUID to alphanumeric. | | \`404\` | \`101\` | \`order\_not\_found\` | Order not found. In the Payment Intent API, the \`error\` field uses the numeric code \`"101"\`. | | \`409\` | \`101\` | \`order\_already\_canceled\` | In the Payment Intent API, non-existent orders and already-canceled orders returned the same \`"101"\` error. In the Orders API, they are differentiated into two distinct errors: \`404\` for order not found and \`409\` for order already canceled. | | \`500\` | \`internal\_error\` | \`idempotency\_validation\_failed\` | Idempotency validation failure. Retry the request. | ### Errors that remain unchanged The following error has the same behavior in both APIs. | HTTP | Error | Note | |---|---|---| | \`401\` | \`unauthorized\` | Invalid or expired token. | ### Errors introduced by the Orders API The following errors have no equivalent in the Payment Intent API. | HTTP | Orders API error | Note | |---|---|---| | \`400\` | \`empty\_required\_header\` | \`X-Idempotency-Key\` missing. | | \`409\` | \`idempotency\_key\_already\_used\` | Idempotency key reused. | ::: ## Implement refunds with the dedicated endpoint The Orders API introduces the dedicated endpoint \`POST /v1/orders/{orderid}/refund\` for refunds, which did not exist in the Payment Intent API. Previously, it was necessary to receive the payment webhook, obtain the \`payment\_id\`, and execute the refund through the Payments API separately. Now, the refund is performed directly on the order. :::::AccordionComponent{title="Replace the Payment Intent API refund flow" pill="1"} Choose between a full or partial refund based on the amount to return. ::::TabsComponent :::TabComponent{title="Full refund"} To refund the full order amount, send the request to the :TagComponent{tag="POST" text="POST /v1/orders/{orderid}/refund" href="/developers/en/reference/in-person-payments/point/orders/refund-order/post" color="green"} endpoint without a body. \`\`\`curl curl -X POST \\ 'https://api.mercadopago.com/v1/orders/{{ORDER\_ID}}/refund' \\ -H 'Authorization: Bearer {{ACCESS\_TOKEN}}' \\ -H 'X-Idempotency-Key: {{IDEMPOTENCY\_KEY}}' \`\`\` ::: :::TabComponent{title="Partial refund"} To refund a partial amount, send the request to the :TagComponent{tag="POST" text="POST /v1/orders/{orderid}/refund" href="/developers/en/reference/in-person-payments/point/orders/refund-order/post" color="green"} endpoint with the \`transactions\[\]\` array indicating the transaction identifier and the amount to refund. The \`transactions\[\].id\` field corresponds to the \`transactions.payments\[\].id\` returned in the order creation or query response. \`\`\`curl curl -X POST \\ 'https://api.mercadopago.com/v1/orders/{{ORDER\_ID}}/refund' \\ -H 'Authorization: Bearer {{ACCESS\_TOKEN}}' \\ -H 'X-Idempotency-Key: {{IDEMPOTENCY\_KEY}}' \\ -d '{ "transactions": \[ { "id": "{{TRANSACTION\_ID}}", "amount": "10" } \] }' \`\`\` ::: :::: Refunds are accepted up to 90 days from the payment date. > SUCCESS\_MESSAGE > > See all possible error codes for this operation in \[Refund errors\](https://www.mercadopago.cl/developers/en/docs/mp-point/resources/refund-errors). ::::: :::AccordionComponent{title="Adapt the refund response fields" pill="2"} The refund response varies depending on the type of operation performed. | Field | Type | Description | |---|---|---| | \`id\` | string | Identifier of the refunded order | | \`status\` | string | \`refunded\` for full refund. \`processed\` for partial refund (balance still available) | | \`status\_detail\` | string | \`refunded\` for full refund. \`partially\_refunded\` for partial refund | | \`transactions.refunds\[\].id\` | string | Refund identifier, generated by Mercado Pago | | \`transactions.refunds\[\].transaction\_id\` | string | Identifier of the payment transaction being refunded | | \`transactions.refunds\[\].reference\_id\` | string | Identifier linking the payment and its refund | | \`transactions.refunds\[\].amount\` | string | Refund amount | | \`transactions.refunds\[\].status\` | string | \`processing\` when a full refund was requested and is being processed. \`processed\` when a partial refund was successfully completed | ::: ## Validate the migration After applying the changes, verify that the integration works correctly across all flows before going to production. :::CheckboxComponent{label="x-test-scope header removed" defaultChecked="false"} The \`x-test-scope\` header was removed from all integration requests. ::: :::CheckboxComponent{label="X-Idempotency-Key header configured" defaultChecked="false"} The \`X-Idempotency-Key\` header must be present in all creation, cancellation, and refund operations. ::: :::CheckboxComponent{label="Terminals configured" defaultChecked="false"} Terminals listed with the :TagComponent{tag="GET" text="GET /terminals/v1/list" href="/developers/en/reference/in-person-payments/point/terminals/get-terminals/get" color="accent"} endpoint and operating mode updated with :TagComponent{tag="PATCH" text="PATCH /terminals/v1/setup" href="/developers/en/reference/in-person-payments/point/terminals/update-operation-mode/patch" color="gray"}. ::: :::CheckboxComponent{label="Order creation validated" defaultChecked="false"} Orders successfully created with the new payload at the :TagComponent{tag="POST" text="POST /v1/orders" href="/developers/en/reference/in-person-payments/point/orders/create-order/post" color="green"} endpoint and received by the terminal. ::: :::CheckboxComponent{label="Order query validated" defaultChecked="false"} Orders successfully retrieved via the :TagComponent{tag="GET" text="GET /v1/orders/{orderid}" href="/developers/en/reference/in-person-payments/point/orders/get-order/get" color="accent"} endpoint. ::: :::CheckboxComponent{label="Webhook topic updated" defaultChecked="false"} \*\*"Order (Mercado Pago)"\*\* (\`orders\`) topic configured in \[Your integrations\](https://www.mercadopago.cl/developers/panel/app) replacing \`point\_integration\_wh\`, and order statuses monitored with the new values: \`created\`, \`at\_terminal\`, \`processed\`, \`failed\`, \`canceled\`, and \`refunded\`. ::: :::CheckboxComponent{label="Order cancellation validated" defaultChecked="false"} Orders successfully canceled via the :TagComponent{tag="POST" text="POST /v1/orders/{orderid}/cancel" href="/developers/en/reference/in-person-payments/point/orders/cancel-order/post" color="green"} endpoint. ::: :::CheckboxComponent{label="Refunds validated" defaultChecked="false"} Refunds processed via the dedicated :TagComponent{tag="POST" text="POST /v1/orders/{orderid}/refund" href="/developers/en/reference/in-person-payments/point/orders/refund-order/post" color="green"} endpoint. ::: See the documentation to learn how to \[test the integration\](https://www.mercadopago.cl/developers/en/docs/mp-point/integration-test).

# Reports

The reports from Mercado Pago provide financial information to track the movements of your account, such as available balance, transactions, and liquidity. This facilitates the reconciliation of sales and other operations with your internal management systems.

Check the table below for more details on the available report types.

| Report type | Description |
|---|---|
| Released Money Report | Provides the composition of the available balance in your account, with details about the values involved in a specific period. Read the [Released money documentation](/developers/en/docs/reports/released-money/introduction) for more information. |
| Account Money Report | Informs about transactions/movements that have affected your account balance. For more information, read the [Account money documentation](/developers/en/docs/reports/account-money/introduction). |
| Activity Reports | Let you configure, generate, and download financial information about your account operations, such as collections, post-collections, and withdrawals. For more information, see the [Activity Reports documentation](/developers/en/docs/reports/activities-reports/introduction). |
| Mercado Pago’s split payments sales report | The Mercado Pago’s split payments sales report offers a comprehensive overview of transactions from linked sellers, available for download in _csv_ and _json_ formats. To learn more, read the [documentation](/developers/en/docs/reports/sales-report/introduction). |


# MD for: https://www.mercadopago.cl/developers/en/docs/mp-point/resources/reports/released-money/introduction.md

\# Releases report The Releases Report is a downloadable file detailing the balance available in your Mercado Pago account. It not only displays the total available amount but also provides information on transactions conducted within a specified period, including situations like fund blocks and unblocks. Additionally, it informs you whether your money is available or not, allowing you to request this information for a convenient date range. Keep in mind that currently, this report is only generated through your computer. ## Analysis of reports from August 2022 The reports you generate from August 2022 have the following characteristics: 1\. Movements are shown in chronological order, making them easier to identify and providing more control over your sales. 2\. In case of any complaints or disputes related to an issue with the service or product offered, the corresponding amount is held until the mediation is resolved. This information is included in your report, and you can find it by searching for the "reserve-" prefix. 3\. Movements related to withdrawals and/or transfers from your available balance appear as "Payout," and all mediations that arise when a complaint is initiated or resolved appear as "Dispute." To check the description of other movements and terms, refer to \[the glossary\](https://www.mercadopago.cl/developers/en/docs/checkout-pro/additional-content/reports/released-money/report-use). 4\. You will find a new column called "Sale detail," providing detailed information about the items sold, facilitating reconciliation and control of your sales. Each entry in this column shows the first element of the sale, followed by the grouping of other items. ## Download report To learn how to generate and download the Releases report, go to \[Sales and billing\](https://www.mercadopago.cl/balance/reports) > \*\*Sales and Account Statement Reports > \[Releases\](https://www.mercadopago.cl/balance/reports/release)\*\* > \*\*Generate report\*\*. ### Create report via API Manually create the Releases Report as often as you wish or schedule it according to your frequency needs through the \[API\](https://www.mercadopago.cl/developers/en/docs/checkout-pro/additional-content/reports/released-money/api). Report generation takes a few minutes, depending on how much information you want to include. It won't always be ready instantly, and until it is, you will see the status "In preparation" on the screen. > Refer to \["How to analyze the Releases report?"\](https://www.mercadopago.cl/ajuda/28771) for a better understanding of your report. ### Report values Depending on the \[selected fees and deadlines\](https://www.mercadopago.cl/settings/release-options), the value obtained from the sale will be released after the payment is credited. Therefore, the total amount indicated in the report may not always coincide with your total balance or the total amount in billing reports. Release deadlines are related to banking processes and mediation flows when transactions are made on Mercado Livre. Additionally, disputes and complaints received in sales can impact money release. > For the exact date of availability of funds from a transaction, it is important to review \[the details of credited payments\](https://www.mercadopago.cl/activities/balance). ## Using the report The Releases Report is an essential tool for both reconciliation and analysis of your financial history. It details account transactions, provides understanding and reconciliation of available balances on specific dates, and provides data for each transaction, including date, concept, and amount. Furthermore, this report presents the complete history of released money, covering events such as bank transfers, disputes, refunds, and chargebacks, and highlights settled installments compared to those pending payment. You can use the \[Report glossary\](https://www.mercadopago.cl/developers/en/guides/additional-content/reports/account-money/report-fields) to review a technical term. > WARNING > > Limitations for test accounts > > Due to an environment limitation that prevents populating data, reports generated for test accounts will be displayed without information. However, generation flows, queries, and report lists will work normally.

# MD for: https://www.mercadopago.cl/developers/en/docs/mp-point/resources/reports/released-money/how-to-use.md

\# Report uses Once the report is ready and downloaded, you will have a file ready to consult spreadsheets and import them into the program you use. To review the report, we recommend downloading it in CSV format to open it in a program that can visualize it. The file should be configured in UTF-8 format to avoid reading issues. ## Report content | Report field | Description | | --- | --- | | Initial Available Balance |  
 Initial balance. Indicates the amount available on the initial date of the period you selected for reconciliation.   
  
| | Release |  
Details of releases of money, including the initial balance and transactions impacting the total balance.   
  
 | | Block |   
Money blocks due to disputes.  
  
 | | Unblock |  
 Unblocks after dispute resolution.  
  
| | Subtotal |   
Sum of transactions within each section.  
  
| | Total|   
 Final result composed of the sum of all subtotals.   
  
In other words:  
 subtotal \`Release\` + subtotal \`Block\` + subtotal \`Unblock\` = total result.   
  
It is the difference between the total credited net amount and the total debited net amount. | Additionally, the report reflects accounting concepts of debit (money you need to pay) and credit (money you are due to receive), organizing the report into two columns, one for each concept: > Your \*\*credit\*\* will be in the \`NET\_CREDIT\_AMOUNT\` column. >  
\> Your \*\*debt\*\* will be in the \`NET\_DEBIT\_AMOUNT\` column. The available balances of transactions are displayed in the \`NET\_CREDIT\` (credit) and \`NET\_DEBIT\` (debit) columns according to positive or negative values. In these fields, the gross amount and discounts related to financing, taxes, and shipping costs are also detailed, resulting in the final net amount. If a transfer is not completed, the report remains valid. The amount will be refunded to your account, and the transaction will be displayed on a new line in the \`NET\_CREDIT\` column. > NOTE > > Have the \[Releases Report Glossary\](https://www.mercadopago.cl/developers/en/docs/additional-content/reports/released-money/report-fields) on hand to consult when needed to check any technical term. ## Report example Observe what comprises the Releases Report in the following example to identify the sections and analyze your own reports: !\[Reporte de liberaciones\](/images/manage-account/reports/example-release-es-v1.jpg) The default version will show an extended view of the columns. The final report will have the most detailed information possible. ## Report organization See the following example for the organization of the report: !\[Reporte de Dinero retirado Ejemplos Mercado Pago\](/images/manage-account/reports/example-nledger-es-v1.jpg)

# MD for: https://www.mercadopago.cl/developers/en/docs/mp-point/resources/reports/released-money/generate.md

\# Generate report You can generate a report of Releases through your Mercado Pago account or via API integration. Refer to the table below for more information. ## Generation channels You can generate a report of Releases through your Mercado Pago account: | Channels | Description | |---------------------------|----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------| | Mercado Pago Panel | Manually create the report through the Mercado Pago panel. Access the \[Sales and Billing\](https://www.mercadopago.cl/movements) section, click \*\*Go to Payment and Account Statement Reports\*\*, and select the report. For more information, read the documentation \[Generate report through the panel\](https://www.mercadopago.cl/developers/en/docs/additional-content/reports/released-money/panel). | | API Integration | Create the report manually or scheduled according to the desired frequency using our API integration. For more information, refer to the documentation \[Generate report via API\](https://www.mercadopago.cl/developers/en/docs/additional-content/reports/released-money/api). | ## Technical features of the report Consider the following technical information whenever you create, schedule, or configure a report. ### Report structure Understand the characteristics of the elements that compose your report. | Actions and components | Characteristics | | --- | --- | | Table details | Table details comprise information for at least 1 day. | | Column order | Fixed | | Maximum period | Reports with data for up to 60 days. | | Currency | Local (based on the country where the Mercado Pago account is registered). | | Column time zone: | GMT-4   
  
 Take as reference the place from where the report is downloaded. | | Web date selection | Based on the user account's time zone.   
For example, a user account registered in Brazil corresponds to the São Paulo time zone. | ### Report export All options available when downloading your report. | Actions and components | Characteristics | | --- | --- | | File name format | Scheduled or manual report:  
 "configurable-prefix-creation-date.csv"   
 Example: mystore-28-05-2024.csv. | | Download formats | .\_csv\_, .\_xlsx\_   
  
\*\*Note\*\*: download the report in .\_csv\_ to import the data and use it in other applications. Download it in .\_xlsx\_ to read the information in spreadsheet tables. | | File | Generated reports are saved in your Mercado Pago account. | ## Notifications ### Webhook Webhook, also known as "web callback," is an efficient method to receive real-time information whenever an event occurs in an application or system. This approach allows the passive transfer of data between two systems through HTTP POST requests. Regarding reports used in reconciliation, a notification is sent to the user who has configured this service as soon as the corresponding files are generated. | Attribute | Description | |-----------------|-----------------------------------| | transaction\_id | Transaction ID | | request\_date | Request date | | generation\_date | Creation date | | files | Available files | | type | File format | | url | Download link | | name | File name | | status | Report status | | creation\_type | Manual or scheduled creation | | report\_type | Report type | | is\_test | Determines if it is a test | | signature | Webhook notification digital signature | ### Encryption password The encryption password is essential to secure the notification process to the system. In the message body (\_payload\_), an attribute called \*\*\_"signature"\_\*\* is sent to validate the legitimate origin of the Mercado Pago Webhook notification, avoiding possible imitations. The creation of the \*\*signature\*\* occurs by combining the \`transaction\_id\` with the \`encrypted password\` in the \*\*\_"Webhook Notification"\_\*\* section, along with the \`generation\_date\` of the report. These values are then encrypted using the \*\*\_BCrypt\_\*\* algorithm as follows: \`signature = BCrypt(transaction\_id + '-' + password\_for\_encryption + '-' + generation\_date)\` To validate that it is Mercado Pago who issued the notification, the \*\*\_verification function\_\*\* offered by the \*\*\_BCrypt\_\*\* algorithm for the desired language must be used. \*\*Java example:\*\* \`BCrypt.checkpw(transaction\_id + '-' + password\_for\_encryption + '-' + generation\_date, payload\_signature)\` > NOTE > > Have the \[Glossary of Releases report\](https://www.mercadopago.cl/developers/en/guides/additional-content/reports/released-money/report-fields) on hand to review it when needed or want to review a technical term.

# MD for: https://www.mercadopago.cl/developers/en/docs/mp-point/resources/reports/released-money/report-use.md

\# Glossary If you have any doubts about the technical terms used, check the glossary below. | Name on the report column | What it means | Data type   
 (maximum longitude) | |---|---|---| | Release date (\`DATE\`) | Transaction release date. It is the moment when this transaction impacts the available balance in the user's account. | DateTime   
 (yyyy-MM-dd'T'HH:mm:ssZ) | | Transaction ID in Mercado Pago (\`SOURCE\_ID\`) | Transaction identifier in Mercado Pago's systems. Example: ID of a Payment. | String   
 (100) | | Reference code (\`EXTERNAL\_REFERENCE\`) | This information helps to identify a transaction by its origin. The code can be:   
 \- Order ID, through the order or shipment (if it is a cart purchase).   
 \- Their own ID, provided by the seller, if it is an external integration. These data allow the correlation of transactions (records) between Mercado Pago and external systems   
  
 This field may be empty for some cases, such as invoice payments, money transfers, among others.   
 | String   
 (255) | | Registry type (\`RECORD\_TYPE\`) | \`initial\_available\_balance\` → Available balance of the previous period.   
  
  
 \`release\` → Money that was released from a collection.   
  
 \`total\` → Total net amount.   
  
 \`available\_balance\` → Balance before and after a withdrawal or transfer, which explains the account balance.  
 | String   
 (30) | | Description (\`DESCRIPTION\`) | Possible values that the field can assume:   
  
For \`release\`: Payment (payment), Simplified Regime 2% Exceeded Subject Tax (tax\_payment\_ibex), Shipping fee (shipping), Money refund. Shipping fee (shipping\_cancel), Tax Withholding (tax\_withdholding), Tax Withholding Cancelled (tax\_withdholding\_cancel), (mediation),(mediation\_cancel), Chargeback (chargeback), (fee\_release\_in\_advance), Positive income (asset\_management\_gain), Negative returns (asset\_management\_loss)  
  
 For Balance prior to withdrawal and/or transfer \`available\_balance\`: The field shows the prefix "pre" and "pos" to indicate the balance before or after a withdrawal or transfer, as applicable, followed by the transaction type – in this case, a money transfer (Payout), followed by the transaction identification number or Source ID.   
  
Prefix + transaction name + transaction number.   
  
 Example: Pre cash withdrawal and transaction ID number (pre\_payout\_ID\_source)   
  
 pre\_payout\_1948976543   
 pos\_payout\_1948976543   
  
Definitions to be considered:   
  
 Chargeback \`chargeback\`: it is displayed when a chargeback associated with the referred payment is initiated or resolved.   
  
 Dispute \`dispute\`: appears when a mediation or complaint about the referred payment is initiated or resolved. It can happen before or after the payment has been released as available money and even withdrawn/transferred from the account.   
  
Shipping\_return fee \`shipping\_return\`: it is displayed when a payment for expedited return is blocked or unblocked.   
  
\`shipping\_refund\`: amount of the shipping or shipping-related tax fee. The money from this refund will be released immediately.   
  
Payment \`payment\`: payment released in any of the channels in which the customer operates.   
  
  
Refund \`refund\`: refund associated with the referred payment.   
  
 IIBB Tax Collection \`tax\_payment\_iibb\_cre\_\[jurisdiction\]\`: collection of gross income tax - Mercado Credito, where \[jurisdiction\] is replaced by the name of the province where the tax is generated.   
  
  
 General Regime Added Value Tax Collection \`tax\_iva\`: collection of the added value tax (IVA). General Regime Added Value Tax Collection - Mercado Credito \`tax\_iva\_cre\`.   
  
 Tax withholding cancellation \`tax\_withdholding\_cancel\`: the cancellation of the tax withholding.  
  
  
 Withholding tax \`tax\_withdholding\`: The collection of withholdings that could not be executed transactional to the associated payment. In Argentina they are only Gross Income withholdings (perceptions are debited as another transaction). In Uruguay they are VAT withholdings. In Colombia they are VAT, ICA and Source withholdings, as applicable   
  
 \`tax\_withdholding\_cancel\`: the cancellation of the tax\_withdholding retention.   
  
 Tax on credits and debits on payments \`tax\_withholding\_payer\`: tax on credits and debits on payments.  
  
 Tax on credits and debits on receipts \`tax\_withholding\_collector\`: tax on credits and debits on collections.  
  
 Tax on credits and debits on withdrawals \`tax\_withholding\_payout\`: tax on credits and debits on withdrawals.  
  
Tax on credits and debits on shipments \`tax\_withholding\_shipping\`: tax on credits and debits on shipments.  
  
 Shipping \`shipping\`: shipping fee for cart purchases that is not included in every payment of the cart.   
  
 Shipping\_cancel \`shipping\_cancel\`: cancellation of the shipping charge for cart purchases that is not included in every payment of the cart.   
  
 Chargeback \`chargeback\`: chargeback either for or against an operation.   
  
 Fee payments / Money advance \`fee-release\_in\_advance\`: Fee for advance.   
  
 Positive income \`asset\_management\_gain\`: positive income generated by the change in the value of shares purchased in the investment pool.  
  
Negative returns \`asset\_management\_loss\`: negative return generated by the variation in the value of shares acquired in the common fund.  
  
 Restriction for fraudulent behavior \`restriction\`:happens when a restriction is applied for fraudulent behavior.   
  
 Debit of the installment of a loan \`credit\_payment\`: Appears when the installment of a granted loan is charged.   
  
 Payout \`payout\`: withdrawal of available money in Mercado Pago.  
  
 Reserve for blocking money invested \`reserve\_for\_embargo\_invested\`: blocking the money invested. This value is displayed when there is cash reserve in mutual funds.  
  
 Reserve for BPP shipping return \`reserve\_for\_bpp\_shipping\_return\`: reserve for returns.  
  
 Reserve for debt payment \`reserve\_for\_debt\_payment\`: withheld for debt payment.  
  
 Reserve for refund \`reserve\_for\_refund\`: withheld for approved returns.  
  
 Reserve due to contest on linked account \`reserve\_for\_cbk\_cross\_recovery\`: withheld due to the chargeback in a linked account.  
  
 Reserve for payment \`reserve\_for\_payment\`: expenses pending confirmation.   
  
\`digitalchange\_transaction\`: Transaction due to digital change. Inflows or outflows in the account. If you are a seller, it is the digital change you gave a buyer that paid in cash. If you are a buyer, it is the change you received for a purchase you paid in cash. | String   
 (50) | | Net debit amount (\`NET\_DEBIT\_AMOUNT\`) | Debited to the amount available. | Numeric   
 (17,2) | | Net credit amount (\`NET\_CREDIT\_AMOUNT\`) | Accreditedto to the amount available. | Numeric   
 (17,2) | | Amount received for split payment purchases (\`SELLER\_AMOUNT\`) | Amount received for split purchases. | Numeric   
 (17,2) | | Gross operation amount (\`GROSS\_AMOUNT\`) | Total gross amount (before deductions) that the seller receives for the transaction. | Numeric, decimal   
 (17,2) | | Extra data (\`METADATA\`) | Extra data such as the ID of partial returns or data provided by the seller in case of having an external integration. | String   
 (JSON) | | \`MP\_FEE\_AMOUNT\` | Commission Payment of Mercado Pago and/or Mercado Libre. Includes VAT. | Numeric   
 (17,2) | | Fee for offering installments (\`FINANCING\_FEE\_AMOUNT\`) | Cost for offering interest-free installments. | Numeric   
 (17,2) | | Shipping cost (\`SHIPPING\_FEE\_AMOUNT\`) | Shipping cost. | Numeric   
 (17,2) | | Taxes for IIBB withholding (\`TAXES\_AMOUNT\`) | Taxes charged for gross income withholdings. | Numeric   
 (17,2) | | Discount coupon (\`COUPON\_AMOUNT\`) | This operation shows the total amount of the discount coupon offered to your buyers. | Numeric   
 (17,2) | | Installments (\`INSTALLMENTS\`) | Number of installments in which the operation was carried out. | Numeric   
 (2) | | Payment method (\`PAYMENT\_METHOD\`) | \[Payment methods available\](https://www.mercadopago.cl/developers/en/docs/sales-processing/payment-methods) according to the country with which you operate in Mercado Pago. | String   
 (200) | | Payment method type (\`PAYMENT\_METHOD\_TYPE\`) | Type of \[available payment method\](https://www.mercadopago.cl/developers/en/docs/sales-processing/payment-methods) according to the country in which you operate with Mercado Pago. | String   
 (200) | | Tax detail (\`TAX\_DETAIL\`) | Description of the tax withheld by operation in \`TAXES\_AMOUNT\`.   
 | String   
 (50) | | Tax deducted from gross value (\`TAX\_AMOUNT\_TELCO\`) | It is the value of the tax on telecommunications companies that is deducted from the gross value. | Numeric   
 (17,2) | | Approval Date (\`TRANSACTION\_APPROVAL\_DATE\`) | Date of approval of the operation. | DateTime   
 (yyyy-MM-dd'T'HH:mm:ssZ) | | Operation creation date (\`TRANSACTION\_DATE\`) | Operation creation date. | DateTime   
 (yyyy-MM-dd'T'HH:mm:ssZ) | | Operation creation date - short format (\`TRANSACTION\_DATE\_SHORT\`) | Operation creation date. | YYYY-MM-DD | | Cashier ID (\`POS\_ID\`) | Cash ID if the payment is made through a physical commerce. | String   
 (50) | | Name of the cashier (\`POS\_NAME\`) | Cash name for the payment made through a physical commerce. | String   
 (200) | | Cashier ID defined by user (\`EXTERNAL\_POS\_ID\`) | User-defined cashier ID for payment made through a physical commerce. | String   
 (100) | | Store ID (\`STORE\_ID\`) | Branch ID if payment is made through a physical commerce. | String   
 (50) | | Store name (\`STORE\_NAME\`) | Branch name for payment made through a physical commerce. | String   
 (200) | | Store ID defined by user (\`EXTERNAL\_STORE\_ID\`) | Store ID defined bu the user for payments at a physical store. | String   
 (100) | | Order ID (\`ORDER\_ID\`) | Purchase order. | Numeric   
 (19) | | Shipping ID (\`SHIPPING\_ID\`) | Shipping ID. | Numeric   
 (19) | | Shipping method (\`SHIPMENT\_MODE\`) | Shipping method. | String   
 (10) | | Package ID (\`PACK\_ID\`) | ID of the package in the cart. | Numeric   
 (19) | | Detailed taxes (\`TAXES\_DISAGGREGATED\`) | Detailed taxes in JSON format. | String   
 (JSON) | | Charge to offer discount (\`EFFECTIVE\_COUPON\_AMOUNT\`) | This transaction shows the amount you cover within the discount coupon offered to your buyers. To make it easier to differentiate it from \`COUPON\_AMOUNT\`, we added the "–" sign when the transaction belongs to a sale and "+" when the transaction belongs to a return. | Numeric   
 (17,2) | | POS machine serial number (\`POI\_ID\`) | POS machine ID if payment is made at a physical store. | String   
 (100) | | Buyer card (\`CARD\_INITIAL\_NUMBER\`) | The first digits of the credit or debit card with which the purchase was made. | Numeric   
 (8) | | Transaction tags (\`OPERATION\_TAGS\`) | These are labels to categorize and/or segment different aspects of the transaction, such as the channels used to make a payment. They are identified as:  
 WHATSAPP\_PAY: This label indicates that the payment was made via WhatsApp.   
QR: This label indicates that the payment was made with a QR code.   
MARKETPLACE: This label indicates that the payment was made directly in Mercado Libre. | String   
 (JSON) | | Product identifier (\`ITEM\_ID\`) | Identifier of the sold product. | String   
 (200) | | Balance (\`BALANCE\_AMOUNT\`) | This column displays the balance remaining in an account after a transaction that affects the total value is performed. | Numeric   
 (17,2) | | Transaction destination account (\`PAYOUT\_BANK\_ACCOUNT\_NUMBER\`) | Here you will find the account number to where Mercado Pago money was transferred. | String   
 (200) | | Product SKU Code (\`PRODUCT\_SKU\`) | SKU code with which you will be able to identify your sold products. | String   
 (200) | | Sale detail (\`SALE\_DETAIL\`) | This column offers detailed information on the items sold in each delivery, making it easier to reconcile and control your sales. | String   
 (500) | | Currency (\`CURRENCY\`) | Currency in which the transaction was carried out. | Alphanumeric string | | Card brand (\`FRANCHISE\`) | Name of the used card brand. | Alphanumeric string | | Last 4 digits (\`LAST\_FOUR\_DIGITS\`) | Last 4 digits of the card used. | Numeric, integer | | Request ID (\`ORDER\_MP\`) | Order identifier in Mercado Pago. | Alphanumeric string | | Transaction attempt ID (\`TRANSACTION\_INTENT\_ID\`) | Transaction intent identifier. | Alphanumeric string | | Purchase ID (\`PURCHASE\_ID\`) | Unique identifier assigned to a specific purchase or transaction. | Alphanumeric string | | Released (\`IS\_RELEASED\`) | Boolean indicator (\`true\` / \`false\`) that indicates whether a product has been released for shipping. \`true\` means the product is ready to be shipped, \`false\` means the opposite. | Boolean | | Shipping association ID (\`SHIPPING\_ORDER\_ID\`) | Unique internal identifier to track each shipping order within the company. Allows managing the details of each request. It is not the carrier's tracking number. | Alphanumeric string | | Issuer name (\`ISSUER\_NAME\`) | Name of the financial institution that issued the card or payment method used in the transaction. | Alphanumeric string | | Application ID (\`APPLICATION\_ID\`) | Internal MP application identifier; identifies which specific application generated each transaction. | Alphanumeric string | | Authorization code (\`AUTHORIZATION\_CODE\`) | Unique code issued to identify the payment approval confirmation. | Alphanumeric string | | Card entry mode (\`CARD\_ENTRY\_MODE\`) | Corresponds to the card entry mode; identifies how data was captured at the terminal. | Alphanumeric string | | Segment detail (\`SEGMENT\_DETAIL\`) | Subunit detail; granular classification of transactions according to their nature and specific characteristics. | Alphanumeric string | | Short release date (\`DATE\_SHORT\`) | Payment release date in YYYY-MM-DD format. | Date (YYYY-MM-DD) | | Short transaction approval date (\`TRANSACTION\_APPROVAL\_DATE\_SHORT\`) | Payment approval date in YYYY-MM-DD format. | Date (YYYY-MM-DD) | | Authenticated payer (\`AUTHENTICATED\_PAYER\`) | Indicator of whether the transaction was paid by an authenticated MP user or not. | Boolean |

 # MD for: https://www.mercadopago.cl/developers/en/docs/mp-point/resources/reports/account-money/introduction.md

\# Account money report The Account money report is a \*\*downloadable report that allows you to view the operations that affected the money in your account\*\*, that is, the movements that affected the balance of your money in Mercado Pago. It contains, for example, the detail of your payments, money receipts, chargebacks and reimbursements in a period of time with its gross and net breakdown. It is made up of available and unavailable money. That is to say, the money you have released to withdraw and the money to be released according to your chosen \[rates and terms\](https://www.mercadopago.com.cl/settings/release-options) . ## Download report Follow this path to learn how to generate and download the Account money report: \[Sales and billing\](https://www.mercadopago.cl/balance/reports) > \*\*Sales and account statement reports > \[Account money\](https://www.mercadopago.cl/balance/reports/settlement\_v2)\*\* > \*\*Generate report\*\*. ## Report values Money movements are automatically impacted in the report when the operation is approved. Pending or rejected operations will not be. ## Using the report The report is an essential tool for both reconciliation and analysis of your financial history. This report is \*\*used to reconcile approved money movements\*\* and includes the transactions that comprise it. At the same time, you can use it to see the status of your account. In addition, you can use the report to view the history of your account balance between two dates and see the detail of the events that affect it, such as disputes, chargebacks, reimbursements, shipments, among others. You can use the \[Glossary of the Account balance report\](https://www.mercadopago.cl/developers/en/guides/additional-content/reports/account-money/glossary) to review a technical term. > WARNING > > Limitations for test accounts > > Due to an environment limitation that prevents populating data, reports generated for test accounts will be displayed without information. However, generation flows, queries, and report lists will work normally.

# MD for: https://www.mercadopago.cl/developers/en/docs/mp-point/resources/reports/account-money/how-to-use.md

\# Report uses Once the report is ready and downloaded, you will have a file to review the spreadsheets or import into the reconciliation program you use. To review the report we recommend downloading it in .csv format to open it in the program that you view it. Configure your program to support the UTF-8 format, so you avoid reading problems. ## Report content The report is made up of different types of transactions that you can see in the \`TRANSACTION\_TYPE\` column. Each of them will have the gross amount of the operation. | Transactions | Transaction type | | --- | --- | | \*SETTLEMENT\* |  
 Approved   
  
| | \*REFUND\* |   
 Total or partial returns   
  
 | | \*CHARGEBACK\* |   
 Chargeback   
  
 | | \*DISPUTE\* |  
 In a complaint   
  
| | \*WITHDRAWAL\* |   
 Money withdrawn   
  
| | \*CASHBACK\* |   
 Cashback   
  
 | | \*SETTLEMENT\_SHIPPING\* |   
 Approved shipments   
  
 | | \*REFUND\_SHIPPING\* |   
 Total or partial returns of shipping costs   
  
 | | \*CHARGEBACK\_SHIPPING\* |   
 Shipping chargeback   
  
 | | \*DISPUTE\_SHIPPING\* |   
 The shipment is in claim   
  
 | And in the \`SETTLEMENT\_NET\_AMOUNT\` column you will find the real impact on your account money balance. > NOTE > > Have the \[Glossary of the Account money report\](https://www.mercadopago.cl/developers/en/guides/additional-content/reports/account-money/glossary) on hand to review it when needed or want to review a technical term. ## Report example Note how the Account money report is composed in this example to identify the operations and read your own reports: !\[Reporte de dinero en cuenta Ejemplos Mercado Pago\](/images/manage-account/reports/example-settlement-en-v1.png) The default version will show an extended view of the columns. The final report will have as much detail as possible.

 # MD for: https://www.mercadopago.cl/developers/en/docs/mp-point/resources/reports/account-money/generate.md

\# Generate report You can generate your Account money report through your Mercado Pago account or via API integration. Refer to the table below for more information. > NOTE > > We have created new columns that allow you to identify which digital wallets or banks your clients use when they pay with a Mercado Pago QR Code. Update your settings preferences \[from the panel\](https://www.mercadopago.cl/balance/reports/settlement\_v2/settings) or \[via API\](https://www.mercadopago.cl/developers/en/docs/additional-content/reports/account-money/api) so that you can include these columns in your reports. ## Generation channels There are two ways to generate an Available Balance report: | Channels | Description | | --- | --- | | Mercado Pago panel | Manually create the report through the Mercado Pago panel. Access \[your reports\](https://www.mercadopago.cl/balance/reports?page=1#!/settlement-report) , click \*\*Go to Payment and account statement reports\*\*, and select the report. For more information, read the documentation \[Generate report through the panel.\](https://www.mercadopago.cl/developers/en/docs/additional-content/reports/account-money/panel) | | API integration | Create the report manually or scheduled according to the desired frequency using our API integration. For more information, refer to the documentation \[Generate report via API.\](https://www.mercadopago.cl/developers/en/docs/additional-content/reports/account-money/api)   
  
 | ## Technical characteristics of the report Consider the following technical information when you want to generate, schedule and set up your reports. ### Report schedule Set up how and how often you want to generate your reports. | Element | Characteristics | | --- | --- | | Schedule |   
\- Daily  
 \- Weekly  
\- Monthly  
  
 | | Generation |   
\- Manual  
\- Automatic  
  
 | ### Report structure Know the characteristics of the elements that make up your report. | Element or Action | Characteristics | | --- | --- | | Tables Detail |   
The detail of the tables includes information generated in at least 1 day.  
  
 | | Column Order |  
 Permanent.   
  
 | | Maximum Period |   
 Reports with data of up to 60 days.   
  
 | | Currency |   
 Local (based on the country where the Mercado Pago account is registered).   
  
 | | Time zone of the columns |   
 GMT-4   
  
Take as reference the place where you download the report from.  
  
 | | Date selection via API |  
 Timezone format: UTC / GMT-0\.   
  
 | | Date selection via web |   
 It must be based on the timezone of the user's account.   
 For example, the timezone of São Paulo corresponds to the user account registered in Brazil.   
  
 | ### Report export All the options you have available when downloading your report. | Element or Action | Characteristics | | --- | --- | | Filename format |   
When the report is scheduled or manual:  
 "<prefix-configurable>-<yyyy-MM-dd-hhmmss>.<format>"   
 Example: mystore-2019-05-28-104010.csv  
  
 | | Download formats |   
.csv, .xlsx   
  
Tip: Download the report in .csv to import the data and use it in other applications. Download it in .xlsx to read the information in the spreadsheet tables.   
  
 | | File |   
The generated reports are saved in your Mercado Pago account.  
  
 | | Set up available via API |   
\- Columns to generate per report.  
 \- File prefix for easy identification.  
 \- SFTP upload.  
 \- Column separator (period or semicolon).  
 \- Email notification.  
  
 | ## Notifications ### Webhook Webhook (also known as "web callback") is a simple method that allows an application or system to send real-time data whenever a particular event takes place, that is, it is a way to passively receive information between two systems via an HTTP POST. In the case of the reports used for reconciliation, a notification is sent to the user who has set up this service when their files are generated. | Attribute | Description | |-----------------|------------------------------| | transaction\_id | Transaction ID | | request\_date | Request date | | generation\_date | Generation date | | files | Available files | | type | File format | | url | Download link | | name | File name | | status | Report status | | creation\_type | Manual or scheduled creation | | report\_type | Report type | | is\_test | Determines if it is a test | | signature | Notification signature | ### Password for encryption The encryption password is essential to secure the notification process to the system. In the message body (\_payload\_), an attribute called \*\*\_"signature"\_\*\* is sent to validate the legitimate origin of the Mercado Pago Webhook notification, avoiding possible imitations. The creation of the \*\*signature\*\* occurs by combining the \`transaction\_id\` with the \`encrypted password\` in the \*\*\_"Webhook Notification"\_\*\* section, along with the \`generation\_date\` of the report. These values are then encrypted using the \*\*\_BCrypt\_\*\* algorithm as follows: \`signature = BCrypt(transaction\_id + '-' + password\_for\_encryption + '-' + generation\_date)\` To validate that it is Mercado Pago who issued the notification, the \*\*\_verification function\_\*\* offered by the \*\*\_BCrypt\_\*\* algorithm for the desired language must be used. \*\*Java example:\*\* \`BCrypt.checkpw(transaction\_id + '-' + password\_for\_encryption + '-' + generation\_date, payload\_signature)\` > Have the \[Glossary of the report\](https://www.mercadopago.cl/developers/en/docs/additional-content/reports/account-money/glossary) on hand to review it when needed or want to review a technical term.


 # MD for: https://www.mercadopago.cl/developers/en/docs/mp-point/resources/reports/account-money/report-fields.md

\# Glossary If you have any doubts about the technical terms used, check the glossary below. | Name on the report column | What it means | Data type   
 (maximum longitude) | |---|---|---| | Reference code (\`EXTERNAL\_REFERENCE\`) | ID that helps identify the origin of the transaction. For example, it can be the sale through the order ID or the shipment (if it is a cart purchase) or the ID itself provided by the seller in case of an external integration.   
  
 Please note that this field might be empty in some cases such as the invoice payment, money transfer etc.   
 | String   
 (255) | | Mercado Pago transaction ID (\`SOURCE\_ID\`) | Transaction ID in Mercado Pago (e.g an order payment).| String   
 (100) | | Seller account code (\`USER\_ID\`) | Seller account code. (Cust ID). | String   
 (19) | | Payment method (\`PAYMENT\_METHOD\`) | Check the \[available payment methods\](https://www.mercadopago.cl/developers/en/docs/sales-processing/payment-methods) according to the country you operate with Mercado Pago. | String   
 (50) | | Payment method type (\`PAYMENT\_METHOD\_TYPE\`) | Payment method type. It can be:   
  
 \*credit\_card\*: credit card.  
\*debit\_card\*: debit card.  
\*bank\_transfer\*: transfer.  
\*atm\*: ATM.   
\*ticket\*: cash.  
\*account\_money\*: account money.  
\*prepaid\_card\*: prepaid card.  
| String   
 (200) | | Country of origin of the Mercado Pago account (\`SITE\`) | MLC: Chile | String   
 (200) | | Transaction type (\`TRANSACTION\_TYPE\`) | Transaction type. It can be:  
  
 Approved payment (\*SETTLEMENT\*): payment approved.  
 Money refund (\*REFUND\*): partial or total refund.   
Chargeback (\*CHARGEBACK\*): the buyer has a chargeback (did not recognize the payment) in their credit card.  
Complaint (\*DISPUTE\*): the buyer initiated a complaint for this payment.   
Bank account transfer (\*WITHDRAWAL\*): transfer to a bank account.  
Cancelled bank account transfer (\*WITHDRAWAL\_CANCEL\*): cancel of a transfer to a bank account.  
Cash withdrawal (\*PAYOUT\*): cash withdrawal from the money available in Mercado Pago. | String   
 (200) | | Purchase amount (\`TRANSACTION\_AMOUNT\`) | Transaction net amount. | Numeric   
 (17,2) | | Currency (\`TRANSACTION\_CURRENCY\`) | Can assume some of these values as appropriate:   
  
 MXN (Peso Mexicano)   
 CLP (Peso Chileno)   
 ARS (Peso Argentino)   
 BRL (Real Brasileiro)   
 COP (Peso Colombiano)   
 PEN (Sol Peruano)   
 UYU (Peso Uruguayo)   
 VES (Bolivar Venezolano)   
 USD (Dollar) | String   
 (10) | | Amount received for split purchases (\`SELLER\_AMOUNT\`) | Amount received for split purchases. | Numeric   
 (17,2) | | Date of origin (\`TRANSACTION\_DATE\`) | Transaction creation date. | Numeric   
 (17) | | Fees + VAT (\`FEE\_AMOUNT\`) | Sum of the processing, shipping, installments and coupon fees if it was at seller's expense. Includes VAT. | Numeric   
 (17,2) | | Net amount of the transaction that impacted your balance (\`SETTLEMENT\_NET\_AMOUNT\`) | Net amount of the transaction that impacted the balance. All fees involved were deducted from the purchase amount \`TRANSACTION\_AMOUNT\`. | Numeric   
 (17,2) | | Settlement currency (\`SETTLEMENT\_CURRENCY\`) | Can assume some of these values as appropriate:   
  
 MXN (Peso Mexicano)   
 CLP (Peso Chileno)   
 ARS (Peso Argentino)   
 BRL (Real Brasileiro)   
 COP (Peso Colombiano)   
 PEN (Sol Peruano)   
 UYU (Peso Uruguayo)   
 VES (Bolivar Venezolano)   
 USD (Dollar) | String   
 (10) | | Approval date (\`SETTLEMENT\_DATE\`) | Transaction approval date. | DateTime   
 (yyyy-MM-dd'T'HH:mm:ssZ) | | Transaction net amount (\`REAL\_AMOUNT\`) | Net amount of the transaction, if it is a approved payment (settlement), the amounts regarding chargebacks, complaints or returns are discounted. | Numeric   
 (17,2) | | Discount coupon (\`COUPON\_AMOUNT\`) | Amount of the discount coupon. \*\*It is only deducted from gross amount or purchase amount\*\* (\`TRANSACTION\_AMOUNT\`) \*\*if provided by the seller.\*\* | Numeric   
 (17,2) | | Additional details (\`METADATA\`) | Additional details such as the ID of the partial refunds or details provided by the seller in case they have an external integration.| String   
 (JSON) | | Mercado Libre feed + VAT (\`MKP\_FEE\_AMOUNT\`) | Mercado Libre Fee. Includes VAT. | Numeric   
 (17,2) | | Fee for offering interest-free installments (\`FINANCING\_FEE\_AMOUNT\`) | Fee for offering interest-free installments. | Numeric   
 (17,2) | | Shipping cost (\`SHIPPING\_FEE\_AMOUNT\`) | Shipping cost. | Numeric   
 (17,2) | | Taxes collected for IIBB withholdings (\`TAXES\_AMOUNT\`) | Taxes collected | Numeric   
 (17,2) | | Installments (\`INSTALLMENTS\`) | Number of installments in which the transaction was carried out. | Numeric   
 (2) | | Tax details (\`TAX\_DETAIL\`) | Description of the tax withheld for transaction in the taxes collected by IIBB withholdings \`TAXES\_AMOUNT\`. | String   
 (50) | | Cashier ID (\`POS\_ID\`) | Cashier ID if the payment is made at a physical store. | String   
 (50) | | Cashier name (\`POS\_NAME\`) | Name of the cashier for the payment made at a physical store. | String   
 (200) | | Cashier ID defined by the user (\`EXTERNAL\_POS\_ID\`) | Cashier ID defined by the user for the payment made at a physical store. | String   
 (100) | | Store ID (\`STORE\_ID\`) | Store ID if the payment is made at a physical store. | String   
 (50) | | Store name (\`STORE\_NAME\`) | Store name if the payment is made at a physical store. | String   
 (200) | | Store ID defined by the user (\`EXTERNAL\_STORE\_ID\`) | Store ID defined by the user for the payment made at a physical store. | String   
 (100) | | Order ID (\`ORDER\_ID\`) | Purchase Order. | Numeric   
 (19) | | Shipping ID (\`SHIPPING\_ID\`) | Shipping Identification. | Numeric   
 (19) | | Shipping method (\`SHIPMENT\_MODE\`) | Shipping Method. | String   
 (10) | | Package ID (\`PACK\_ID\`) | Package ID in the cart. | Numeric   
 (19) | | Detailed taxes (\`TAXES\_DISAGGREGATED\`) | Detailed taxes in the JSON format. | String   
 (JSON) | | POS machine series number (S/N) (\`POI\_ID\`) | POS machine ID if the payment is made at a physical store. | String   
 (50) | | Digital Wallet (\`POI\_WALLET\_NAME\`) | Name of the digital wallet from which a digital payment is originated. It allows to identify the origin of a transaction when the payment is made with a Mercado Pago QR Code. | String   
 (200) | | Bank of origin (\`POI\_BANK\_NAME\`) | Name of the bank institution from which a digital payment is originated. It allows to identify the origin of a transaction when the payment is made with a Mercado Pago QR Code. | String   
 (200) | | Description (\`DESCRIPTION\`) | It helps identify the register of the transactions or operations in a period of time.  
 When its a payment in installments, it will be "INSTALLMENT". | String   
 (50) | | Money release date (\`MONEY\_RELEASE\_DATE\`) | Date in which each installment payment will be realeased. | DateTime   
 (yyyy-MM-dd'T'HH:mm:ssZ) | | Released (\`IS\_RELEASED\`) | Indicates if the money from the operation has already been released. It can take the values TRUE (money released) or FALSE (money not released). | Boolean   
 (TRUE/FALSE) | | Buyer card (\`CARD\_INITIAL\_NUMBER\`) | Corresponds to the first digits of the credit or debit card used in a purchase. | Numeric   
 (8) | | Transaction labels (\`OPERATION\_TAGS\`) | These are labels used to categorize and/or segment different aspects of the transaction, such as the channels used to make a payment. They are identified as:  
Payment via WhatsApp (WHATSAPP\_PAY): this label indicates that the payment was made through WhatsApp. | String   
 (JSON) | | Sales channel (\`BUSINESS\_UNIT\`) | Corresponds to the channel through which an order was generated. The channels are Mercado Pago, Mercado Libre, Mercado Shops and Delivery. | String   
 (255) | | Payment platform (\`SUB\_UNIT\`) | It allows to identify the method used to collect a payment with Mercado Pago. | String   
 (255) | | Product SKU Code (\`PRODUCT\_SKU\`) | SKU code with which you will be able to identify your sold products. | String   
 (200) | | Sale detail (\`SALE\_DETAIL\`) | This column offers detailed information on the items sold in each delivery, making it easier to reconcile and control your sales. | String   
 (500) | | Tip amount (\`TIP\_AMOUNT\`) | Tip amount received in the transaction. | Numeric   
 (17,2) | | Card brand (\`FRANCHISE\`) | Name of the used card brand. | Alphanumeric string | | Last 4 digits (\`LAST\_FOUR\_DIGITS\`) | Last 4 digits of the card used. | Numeric, integer | | Request ID (\`ORDER\_MP\`) | Order identifier in Mercado Pago. | Alphanumeric string | | Transaction attempt ID (\`TRANSACTION\_INTENT\_ID\`) | Transaction intent identifier. | Alphanumeric string | | Billing period (\`INVOICING\_PERIOD\`) | Billing period to which the transaction corresponds. Helps organize and reconcile transactions by billing cycle. | Numeric, integer | | Issuer name (\`ISSUER\_NAME\`) | Name of the financial institution that issued the card or payment method used in the transaction. | Alphanumeric string | | Payment bank account number (\`PAY\_BANK\_TRANSFER\_ID\`) | Unique identifier assigned to each bank transfer used as a payment method. Allows tracking and managing the details of that specific transaction. | Alphanumeric string | | Purchase ID (\`PURCHASE\_ID\`) | Unique identifier assigned to a specific purchase or transaction. | Alphanumeric string | | Shipping association ID (\`SHIPPING\_ORDER\_ID\`) | Unique internal identifier to track each shipping order within the company. Allows managing the details of each request. It is not the carrier's tracking number. | Alphanumeric string | | Application ID (\`APPLICATION\_ID\`) | Internal MP application identifier; identifies which specific application generated each transaction. | Alphanumeric string | | Authorization code (\`AUTHORIZATION\_CODE\`) | Unique code issued to identify the payment approval confirmation. | Alphanumeric string | | Card entry mode (\`CARD\_ENTRY\_MODE\`) | Corresponds to the card entry mode; identifies how data was captured at the terminal. | Alphanumeric string | | Segment detail (\`SEGMENT\_DETAIL\`) | Subunit detail; granular classification of transactions according to their nature and specific characteristics. | Alphanumeric string | | Short settlement date (\`SETTLEMENT\_DATE\_SHORT\`) | Short payment approval date in YYYY-MM-DD format. | Date (YYYY-MM-DD) | | Short transaction date (\`TRANSACTION\_DATE\_SHORT\`) | Payment creation date in YYYY-MM-DD format. | Date (YYYY-MM-DD) | | Short money release date (\`MONEY\_RELEASE\_DATE\_SHORT\`) | Payment release date in YYYY-MM-DD format. | Date (YYYY-MM-DD) | | Authenticated payer (\`AUTHENTICATED\_PAYER\`) | Indicator of whether the transaction was paid by an authenticated MP user or not. | Boolean |

 # Credentials

Credentials are unique access keys that we use to identify an integration in your account. They are directly linked to the **application** you created for that integration and will allow you to develop your project with the best Mercado Pago security measures.

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
2. Accept the ----[mla, mlc, mlu, mlm, mco, mpe]----[Privacy Statement](https://www.mercadopago[FAKER][URL][DOMAIN]/privacidad)----------------[mlb]----[Privacy Statement](https://www.mercadopago.com.br/privacidade)------------ and the [Terms and Conditions](/developers/es/docs/resources/legal/terms-and-conditions). Fill in the reCAPTCHA and click on **Activate credentials**.

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
3. Accept the ----[mla, mlc, mlu, mlm, mco, mpe]----[Privacy Statement](https://www.mercadopago[FAKER][URL][DOMAIN]/privacidad)----------------[mlb]----[Privacy Statement](https://www.mercadopago.com.br/privacidade)------------ and the [Terms and Conditions](/developers/en/docs/resources/legal/terms-and-conditions). Fill in the reCAPTCHA and click on **Activate credentials**.

When accessing production credentials, the following credential pairs will be displayed: **Public Key and Access Token**, as well as **Client ID and Client Secret**.

----[mla, mlm]----
![Cómo acceder a las credenciales a través de Tus Integraciones](/images/snippets/credentials-prod-panel-es-v2.jpg)

------------
----[mlb]----
![Como acessar as credenciais através das Suas Integrações](/images/snippets/credentials-prod-panel-pt-v1.jpg)

------------

### Public Key and Access Token
The **Public Key** and **Access Token** credentials are used, not necessarily together, in integrations made with Mercado Pago payment solutions. They are directly linked to the **application** you created, so each credential pair is unique for each integration.

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
3. Go to the **Testing** or **Production** section, depending on the type of credential you want to share. Remember that to access production credentials, you must activate them. If you don't know how to activate them, activate them from the **Production** section.
4. Once you select the credentials, go to the *Share credentials with a developer* section and click on the **Share Credentials** button.
5. Enter the email address of the person you want to grant access to. **Remember**: it is mandatory that the email address is associated with a Mercado Pago account.

----[mlb]----
![Compartilhar credenciais em Suas Integrações](/images/snippets/share-credentials-panel-pt-v1.jpg)

------------
----[mla, mlc, mlu, mlm, mco, mpe]----
![Compartir credenciales en Tus Integraciones](/images/snippets/share-credentials-panel-es-v1.jpg)

------------

## Renew credentials

You can renew your **production credentials** for security reasons or any other relevant reason.

> WARNING
>
> Renewing credentials already configured in an integration will affect its operation. It is necessary that **you replace the old credentials with the ones obtained** after the renewal process to continue operating.

To renew a credential pair, follow the steps below.

1. Access your production credentials through [Your integrations](https://www.mercadopago[FAKER][URL][DOMAIN]/developers/panel/app).
2. Select the credential pair you want to renew. These can be **Public Key** and **Access Token** or **Client ID** and **Client Secret**. Keep in mind that both credentials in the pair you choose will be renewed.
3. Click on the three dots located to the right of the credential you want to renew and select **Renew**. Click on **Renew now** to confirm the change.

----[mlb]----
![Como renovar suas credenciais](/images/snippets/renew-credentials-pt-v1.jpg)
------------
----[mla, mlc, mlu, mlm, mco, mpe]----
![Cómo renovar tus credenciales](/images/snippets/renew-credentials-es-v1.jpg)
------------

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

![Integration data](/images/point-orders/integration-data-point-es-v1.png)

:::AccordionComponent{title="Credentials"}

This section displays the :toolTipComponent[credentials]{link="/developers/en/docs/mp-point/resources/credentials" linkText="Credentials" content="Unique access keys we use to identify an integration in your account, linked to your application. For more information, access the link below."} of your application, which are:

- **Test credentials**: a set of keys used both during the development stage, to ensure secure configurations, and during the testing stage, to test the integration. When you create an application, test credentials are generated automatically.
- **Production credentials**: a set of keys that allow you to receive real payments in stores and other applications. To obtain production credentials, you must **activate them** by clicking on **Activate credentials** and filling in some information about your business.

For more information, see the [Credentials](/developers/en/docs/mp-point/resources/credentials) documentation.

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
* **Payment solution to be integrated**: edit the payment solution to be integrated between **Online payments** and **In-person payments**.
  - **Online payments**: if you are going to use an e-commerce platform, mark **Yes** and select the **platform** you will integrate with. Finally, choose the **product** you are integrating. If you are not using an e-commerce platform, mark **No** and select the **product** you are integrating. Optionally, you can select the integration model(s).
  - **In-person payments**: select the **product** you are integrating.

#### Advanced settings

* **Redirect URL**: URL (in https) where you want to receive the authorization code when your integration is set up as a marketplace or performed through the flow **Authorization code** by OAuth. **Make sure that is a static URL**. Check out [OAuth](/developers/en/docs/security/oauth) documentation for more details.
* **Use the authorization code flow with PKCE**: if the integration is done with the flow **Authorization code** by OAuth, you can enable PKCE (Proof Key for Code Exchange) to generate an additional secret code to be used during the authorization process. Check out [Configure PKCE](/developers/en/docs/security/oauth/creation#bookmark_configurar_pkce) documentation for more details.
* **Application permissions**: options for accessing your application, including **read**, **offline access** and **write**. By default, your application is created with all permissions enabled, but you can disable a permission by unchecking the corresponding checkbox.

### Delete application

To remove an application, follow these steps:

1. Access the "Edit Application" page.
2. Scroll to the bottom of the page and click on the **Delete Application** button.
This way, the application will be successfully deleted.

> RED_MESSAGE
>
> When deleting an application, please note that your store will lose the ability to receive payments through the integration associated with that application. Additionally, all settings, including associated credentials, will be lost. **Once an application is deleted, it cannot be recovered**.

:::
:::AccordionComponent{title="Integration quality"}

The [quality measurement](/developers/en/docs/integration-quality) is the final stage of the integration process, where you can validate whether it meets the necessary quality and security requirements to provide the best experience for both sellers and buyers.

There are 2 ways to measure the quality of your integration:

 * **Manual:** you can conduct the measurement on your own whenever you prefer. You only need a `payment ID` from a payment made with production credentials and access **"Integration Quality"** in the side menu, where you can find the step-by-step instructions.
 * **Automatic:** From the 1st to the 7th of each month, Mercado Pago conducts a periodic quality measurement for all integrations with **Mercado Pago Point** that have at least one payment made with production credentials.

As a result of this measurement, you will receive a score indicating how secure and aligned your application's configuration is with Mercado Pago's best integration practices, along with necessary recommendations for adjustments if needed.

For more details, refer to the documentation on [integration quality](/developers/en/docs/integration-quality).

:::
:::AccordionComponent{title="Notifications"}

If you have already [set up your Webhook notifications](/developers/en/docs/mp-point/notifications), this section will display the percentage of notifications successfully delivered for the integration in question.

:::

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


# Troubleshooting

Below, you can find a list of problems that may occur during your integration and operation with Mercado Pago Point, and how to solve them.

> SUCCESS_MESSAGE
>
> If you are experiencing a problem with Mercado Pago, before resorting to the information in this documentation, make sure that all our services are working correctly by accessing our [real-time status report](https://status.mercadopago.com/).

:::AccordionComponent{title="The terminal does not change the operation mode to PDV"}
If you made the operation mode change of your terminal to PDV mode via API and you don't see it reflected, you will need to restart it.

Remember that each update made to the operation mode of the terminals requires restarting them to complete the process.

:::
:::::AccordionComponent{title="POS mode integration that stopped working"}
If your integration stopped working momentarily, this may be due to some unexpected interruption in our payment APIs.

While we work to restore the service, and only temporarily, you can continue with payment processing with Mercado Pago Point by changing the operation mode of your terminal to `STANDALONE`, which is the mode not integrated with our APIs.

For this, you have three options: do it via API, via terminal, or via Mercado Pago Panel. Choose the one that best suits your needs.

::::TabsComponent

:::TabComponent{title="API"}
Send a request to the endpoint :TagComponent{tag="PATCH" text="Change operation mode" href="/developers/en/reference/in-person-payments/point/terminals/update-operation-mode/patch" color="gray"} using the Access Token that corresponds according to your integration type (:toolTipComponent[personal]{link="/developers/en/docs/mp-point/create-application#bookmark_access_credentials" linkText="Access credentials" content="Mercado Pago Point integrations to your system for your own use and configured using your application's production credentials. For more information, access the link below."} or :toolTipComponent[for a third-party]{link="/developers/en/docs/mp-point/create-application#bookmark_access_credentials" linkText="Access credentials" content="Mercado Pago Point integrations to your system on behalf of a seller and configured using credentials obtained through the OAuth security protocol. For more information, access the link below."}) and making sure to send the value `STANDALONE` in the `terminals.operating_mode` field.

Confirm in the response that the change in operation mode was successful and restart your terminal to complete the process.

:::
:::TabComponent{title="Terminal"}
Press the **More options** button at the bottom of your terminal, choose the **Settings** option and then **Linking mode**.

There, deactivate the **Linked to point of sale** option, and restart your terminal to complete the process.

:::
:::TabComponent{title="Mercado Pago Panel"}
Log into your [Mercado Pago account](https://www.mercadopago[FAKER][URL][DOMAIN]/home), and access **Your business** in the left side menu.

Access the **Your Point terminals** option, locate the terminal whose operation mode you want to modify and click on the three dots. There, select **Unlink reader**.

To finish the process, restart your terminal.

:::
::::

> NOTE
> 
> Remember that this change should be temporary. You will need to [return your terminal to PDV mode](/developers/en/docs/mp-point/configure-terminal#:~:text=mode%20on%20the-,terminal,-As%20the%20last) when the service is restored to maintain automatic reconciliation between your system and Mercado Pago and continue receiving your notifications.

:::::
:::AccordionComponent{title="The order does not load automatically on the terminal"}
If you created an order from your system and it is not automatically obtained by the terminal, it may be due to connection problems in your network.

To solve this and be able to continue with the payment, you should press the **Update** button on your terminal, which will force the order to be obtained.

This solution can also be useful for canceling the order. While it has `status=created`, you can :TagComponent{tag="POST" text="cancel it via API" href="/developers/en/reference/in-person-payments/point/orders/cancel-order/post" color="green"}. If the order already has `status=at_terminal`, you can request its cancellation through the same endpoint by sending the conditional `x-allow-cancelable-status: at_terminal` header, or update the terminal and perform the [cancellation](/developers/en/docs/mp-point/payment-processing#:~:text=Cancel%20an-,order,-An%20order%20can) through the reader. For API requests in `at_terminal`, wait for the [cancellation webhook notification](/developers/en/docs/mp-point/notifications) to confirm completion.

:::
:::::AccordionComponent{title="The API does not allow refunding an order"}
If you are momentarily unable to perform a refund via API, and [verified that you are meeting all the requirements to perform this operation](/developers/en/docs/mp-point/payment-processing#:~:text=Refund%20an-,order,-If%20you%20wish), it may be due to some unexpected interruption in our payment APIs.

While we work to restore the service, you can perform refunds manually from your Mercado Pago Panel or from the same terminal. Choose the option that best suits your needs.

::::TabsComponent

:::TabComponent{title="Terminal"}
Press the **More options** button at the bottom of your terminal and choose the **Activity with this Point** option. There you can see the operations performed.

You should select the operation you want to refund to access its **Details**. In this screen, scroll to the **Related actions** option, and select the **Return money** option.

Finally, review the information to make sure you are refunding the desired transaction and confirm the action by pressing the **Return** button.

The "Operation details" screen should now show you the refunded transaction with the status "Payment returned" and, going back to "More options", you can see this new activity with that terminal.

:::
:::TabComponent{title="Mercado Pago Panel"}
Log into your [Mercado Pago account](https://www.mercadopago[FAKER][URL][DOMAIN]/home). On the main screen, you will see **Your recent activity**, with the operations performed.

You should select the operation you want to refund to access its **Details**. In this screen, scroll to the **Related actions** option, and select the **Return money** option.

Finally, review the information to make sure you are refunding the desired transaction and confirm the action by pressing the **Return money** button.

You will see the confirmation of the operation and, if you press the **Back to activity** button, you will see the detail of the refund transaction.

:::
::::

> NOTE
> 
> To validate that the refund has been effective, whatever way you have performed it, verify that you have received a notification with the action `order.refunded`.

:::::
:::AccordionComponent{title="The terminal does not print"}
If you integrated the printing functionality and you are not able to get prints from your terminal, you must first make sure you have this option enabled. For this, contact our Support team and request its update.

If your terminal already has the necessary update to perform printing, this functionality may be failing due to technical problems, such as insufficient paper roll or the coil has overheated. You should check the terminal warnings to be able to understand and solve the problem in each case.

:::
:::AccordionComponent{title="Order status updates are not working correctly"}
Verify that you have correctly configured [notifications via Webhooks](/developers/en/docs/mp-point/notifications) for the **Order (Mercado Pago)** topic. If you have configured any other topic, such as Payments or Point Integrations, you may be receiving alerts inconsistent with your integration.

:::


# Test accounts

Use test accounts to ensure that your integration supports all possible flows and scenarios. They have the same features as a real Mercado Pago account, which allows you to test the functioning of the integrations you are developing.

Test accounts are **automatically created** after the application is created. If you prefer to create them manually, follow the steps below. You can generate **up to 15 test user accounts** simultaneously, and for now, it is not possible to delete them.

> WARNING
>
> Integrations with [Checkout Bricks](/developers/en/docs/checkout-bricks/overview) do not support test accounts for integration testing. For more information, please refer to the documentation [Make test purchase](/developers/en/docs/checkout-bricks/integration-test/test-payment-flow) with Checkout Bricks.

To perform the test, you must have at least two accounts:

* **Seller**: account required to **configure application and credentials**. This is your user account.
* **Buyer**: account required to **test the purchase process**.
* **Integrator**: account used in **marketplace model integrations**.

In addition to these accounts, it is also important to use **test cards** to test payment integration and simulate the purchase process, as well as **balance in the test user's Mercado Pago account**. See more details below.

![create test user](/images/snippets/test-cross/test-user-es-create-seller-v1.png)

To create accounts and test how the integrations work, follow the steps below.

1. On the [Devsite](/developers/en/docs), navigate to **[Your integrations](/developers/panel/app)** and click on the card corresponding to your application.
2. On the application page, go to the **Test accounts** section and click the **+ Create test account** button.
3. In the "Create new account" screen, select the **operating country** for the account. This information **cannot be edited later**, and furthermore, the Buyer and Seller users need to be from the same country.
4. Then, enter a description to identify the account. For example: "Seller - Store 1".
5. Next, select the type of account you want to create. This can be **Seller**, **Buyer** or **Integrator**.
6. If the test account requires it, enter a **fictional money value** that will serve as a reference for testing your applications. This value will appear as the balance in the Mercado Pago account of the test user and can be used for payment simulation, just like with the **test cards**.
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



---
product_landing_hero:
 - title: Integrate QR Code payments into your solution
 - message: Offer your customers the option to pay via QR codes through a unified API. This integration allows you to manage the complete payment cycle and automatic reconciliation of sales directly from Mercado Pago.
 - image: https://http2.mlstatic.com/storage/dx-devsite/docs-assets/custom-upload/2025/8/15/1757985864136-QR.png
 - benefit_icon: recurring-payments
 - benefit_title: Static and dynamic codes
 - benefit_icon: link
 - benefit_title: Instant payments
 - benefit_icon: sort
 - benefit_title: Real-time notifications
 - benefit_icon: categories
 - benefit_title: Automatic reconciliation
 - info: 
---

---
product_landing_how_works:
 - title: How it works
 - message: By integrating QR Code payments, your customers can pay instantly by scanning a QR code linked to your Mercado Pago account. When scanning the code, the amount to pay appears automatically on the customer's device, streamlining the process. The system can generate dynamic QR codes for each transaction, static codes for fixed points of sale, or even combine both options as needed.
 - sub_title: Payment process
 - image: https://http2.mlstatic.com/storage/dx-devsite/docs-assets/custom-upload/2025/8/25/1758823991390-ImagemEN2x.png
 - image_text: Check processing rates
 - image_text_link: /developers/en/support/37740
 - list_title: Create the payment order from your system using our unified API.
 - list_title: In your system, you need to generate and display a QR code on the point of sale screen, which can be dynamic (different for each transaction) or static (the same for all transactions).
 - list_title: The buyer pays using the selected payment method.
 - list_title: The integrated system receives notification about the payment status.
 - button_description: How to integrate
 - button_link: /developers/en/docs/qr-code/create-application
---

---
product_landing_what_it_offers:
 - title: What it offers
 - message: Integrating Mercado Pago's API into your project completely transforms the payment experience, unlike models without integration, where each payment must be processed and reconciled manually.
 - benefit_title: Different QR Code models
 - benefit_bullet: Static model: fixed QR code associated with a POS for multiple transactions.
 - benefit_bullet: Dynamic model: unique QR code generated specifically for each transaction.
 - benefit_bullet: Hybrid model: intelligent combination of static and dynamic model functionalities. The amount to pay is reflected in the static QR and, at the same time, a dynamic QR exclusive for each transaction is generated.
 - benefit_title: Automatic management
 - benefit_bullet: Manage payments directly from your system.
 - benefit_bullet: Receive automatic notifications via webhooks in real-time.
 - benefit_bullet: Automatic reconciliation of operations with Mercado Pago.
 - benefit_title: Unified API
 - benefit_bullet: Connect your project through a single API to manage orders, payments, and notifications.
 - benefit_bullet: Avoid multiple integrations and centralize your technical development with Mercado Pago.
 - benefit_title: Efficiency and security
 - benefit_bullet: Protect data involved in transactions with HTTPS protocols and OAuth authentications.
 - benefit_bullet: The API automatically manages the transaction lifecycle, eliminating the need for manual intervention, reducing errors, and increasing operational efficiency.
---

---
product_landing_what_differentiates:
 - title: QR Code models
 - message: Compare the available QR code integration models and choose the one that best suits your business. Check the [rates](/developers/en/support/37740#from=/mp_wcs_v2/first_steps&to=our_rates).
 - columns_amount: 3
 - column_product: QR Static Model
 - column_button_text: Learn more
 - column_button_link: /developers/en/docs/qr-code/payment-processing#bookmark_static_mode
 - column_product: QR Dynamic Model
 - column_button_text: Learn more
 - column_button_link: /developers/en/docs/qr-code/payment-processing#bookmark_dynamic_mode
 - column_product: QR Hybrid Model
 - column_button_text: Learn more
 - column_button_link: /developers/en/docs/qr-code/payment-processing#bookmark_hybrid_mode
 - line_text: Integration difficulty
 - line_type: dots
 - line_values: 1|2|2
 - line_text: QR at the POS (reusable)
 - line_type: check
 - line_values: true|false|true
 - line_text: Single-use QR
 - line_type: check
 - line_values: false|true|true
 - line_text: Multiple QR in the same POS
 - line_type: check
 - line_values: false|true|true
 - line_text: Payment completion screen
 - line_type: check
 - line_values: true|true|true
 - line_text: Refunds
 - line_type: check
 - line_values: true|true|true
---

---
product_landing_how_integrate:
 - title: How to integrate
 - sub_title: Learn the necessary steps to integrate QR Code.
 - requirement_title: Prerequisites
 - requirement_table_title: Mercado Pago app
 - requirement_table_list: You need to have the Mercado Pago app installed on your phone to log in. You can download it for [Android](https://play.google.com/store/apps/details?id=com.mercadopago.wallet&hl=en_419) or [iOS](https://apps.apple.com/cl/app/mercado-pago/id925436649) devices.
 - requirement_table_title: Mercado Pago account
 - requirement_table_list: You need to create a user in Mercado Pago (or Mercado Libre) to have a [seller account](https://www.mercadopago[FAKER][URL][DOMAIN]/hub/registration/landing), whether in an [own integration](/developers/en/docs/qr-code/create-application) or for [third parties](/developers/en/docs/qr-code/create-application).
---
|||column1|||
---
product_landing_how_integrate:
 - list_title: Integration process
 - list_item: [Create an application](/developers/en/docs/qr-code/create-application) in [Your integrations](/developers/panel/app).
 - list_item: [Configure your store and POS](/developers/en/docs/qr-code/create-store-and-pos)
 - list_item: [Integrate payment processing](/developers/en/docs/qr-code/payment-processing)
 - list_item: [Configure payment notifications](/developers/en/docs/qr-code/notifications)
 - list_item: [Test the integration](/developers/en/docs/qr-code/test-integration)
 - list_item: [Measure your integration quality](/developers/en/docs/qr-code/integration-quality)
 - list_item: [Go to production](/developers/en/docs/qr-code/go-to-production)
 - button_description: I want to start integrating
 - button_link: /developers/en/docs/qr-code/create-application
---
|||column2|||
<div class="mermaid-overview">
  <pre class="mermaid">
  flowchart TD
  A[Create an application in Your integrations] --> B[Configure your store and POS]
  B --> C[Integrate payment processing]
  C --> D[Configure payment notifications]
  D --> E[Test the integration]
  E --> M[Measure your integration quality]
  M --> F[Go to production]
  </pre>
</div>
|||

