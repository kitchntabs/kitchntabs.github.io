JUMPSELLER WEBHOOKS:

WEBHOOK TOKEN: 9d60ae2b2f34d97f4911091cb870bf64

TYPES:
{
  "notifications": {
    "order_updated": "Pedido Actualizado",
    "order_pending_payment": "Pedido pendiente de pago",
    "order_paid": "Pedido Pagado",
    "order_shipped": "Pedido Enviado",
    "order_canceled": "Pedido anulado",
    "order_abandoned": "Pedido Abandonado",
    "product_created": "Producto Creado",
    "product_updated": "Producto Actualizado",
    "product_deleted": "Producto Borrado",
    "customer_created": "Cliente Creado",
    "customer_updated": "Cliente Actualizado",
    "customer_deleted": "Cliente Eliminado",
    "contact": "Contacto",
    "order_pickup_available": "Recogida de pedidos disponible",
    "order_in_preparation": "Pedido en preparación"
  }
}

This JSON payload is identically to the one used by Order’s API
For example, if the event was an order created the message would look like:

{
  "order": {
    "id": 1026,
    "created_at": "2023-02-10 13:56:35 UTC",
    "status": "Pending Payment",
    "currency": "USD",
    "subtotal": 399.0,
    "tax": 0,
    "shipping_tax": 0,
    "shipping": 50.0,
    "shipping_required": true,
    "total": 369.2,
    "discount": 79.8,
    "shipping_discount": 0,
    "fulfillment_status": null,
    "shipping_method_id": 317048,
    "shipping_service_id": null,
    "shipping_method_name": "Flat Rate",
    "payment_method_name": "Cash Collection",
    "payment_method_type": "manual",
    "payment_information": "Pay at your door step",
    "additional_information": "Leave at reception if not home.",
    "duplicate_url": "https://store.jumpseller.com/cart/duplicate/<token>",
    "recovery_url": null,
    "checkout_url": "https://store.jumpseller.com/checkout?token=<token>",
    "coupons": null,
    "promotions": [],
    "customer": {
      "id": "123",
      "email": "test@gmail.com",
      "phone": "123",
      "ip": "0.0.0.0"
    },
    "shipping_address": {
      "name": "John",
      "surname": "Mattos",
      "address": "Colliers Wood",
      "city": "London",
      "postal": "5000",
      "region": "England",
      "country": "United Kingdom",
      "country_code": "GB",
      "region_code": "ENG",
      "street_number": null,
      "latitude": 51.4163,
      "longitude": -0.17612
    },
    "billing_address": {
      "name": "John",
      "surname": "Mattos",
      "taxid": null,
      "address": "Nok Ltd",
      "city": "London",
      "postal": "5771",
      "region": "England",
      "country": "United Kingdom",
      "country_code": "GB",
      "region_code": "ENG",
      "street_number": null
    },
    "products": [{
      "id": 10732902,
      "variant_id": 81899012,
      "sku": "black",
      "name": "Black",
      "qty": 1,
      "price": 399.0,
      "tax": 0,
      "discount": 79.8,
      "weight": 1.0,
      "image": "https://example.com/image.png",
      "files": [],
      "taxes": []
    }],
    "additional_fields": [{
      "label": "Test",
      "value": "No",
      "id": 28664,
      "area": "billing"
    }],
    "shipping_taxes": [],
    "source": {
      "source_name": null,
      "medium": null,
      "campaign": null,
      "referral_url": null,
      "referral_code": null,
      "user_agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 11_2_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.114 Safari/537.36",
      "first_page_visited": "https://store.jumpseller.com/",
      "first_page_visited_at": "2021-02-10 12:56:35 UTC",
      "referral_source": "Direct"
    },
    "tracking_url": null,
    "tracking_company": null,
    "tracking_number": null,
    "shipping_option": "delivery",
    "shipment_status": "Not Processed",
    "external_shipping_rate_id": null,
    "external_shipping_rate_description": null
  }
}  
We expect an HTTP response with status code 2xx, like 200 or 201, otherwise we will retry delivery other 4 times over more than 4 days ( N^4 where N is the retry attempt number, p.e. the third retry is scheduled in 3 * 3 * 3 * 3 = 81 mins and then the fourth in 256mins );
We implemented a fifteen (15) second timeout, this means, we will wait 15 seconds to receive a 2xxOK response otherwise we abort the request and start retrying it;
After 8 failed attempts to deliver a message we pause the problematic Webhook and automatically notify the Store Admin and the App Author by email.



Verifying Authenticity
Webhooks can be verified by calculating a digital signature and comparate it with the value sent in the POST headers:

Jumpseller-Hmac-Sha256 the validation code your digital signature needs to match.
This header is generated using the stores hooks token, along with the JSON data sent in the request - so that you confirm all the data on the request was not modified.

To verify that the request came from Jumpseller, compute the HMAC digest according to the following algorithm and check if it’s the same value on the Jumpseller-Hmac-Sha256 header.

The following simplistic Ruby code (Sinatra) verifies a Jumpseller webhook request:

require 'rubygems'
require 'base64'
require 'openssl'
require 'sinatra'

HOOKS_TOKEN = 'XXXXX' # get your token at Admin Panel > Config > Notifications / Webhooks.

helpers do
  def verify_webhook(data, hmac_header)
    digest  = OpenSSL::Digest.new('sha256')
    hmac = Base64.encode64(OpenSSL::HMAC.digest(digest, HOOKS_TOKEN, data)).strip
    hmac == hmac_header
  end
end

post '/' do
  request.body.rewind
  data = request.body.read
  verified = verify_webhook(data, env["HTTP_JUMPSELLER_HMAC_SHA256"])
  puts "verified? #{verified}" # true or false.
end
in PHP:


$token = "TOKEN_FROM_JUMPSELLER_NOTIFICATIONS";

define('API_SECRET_KEY', $token);

function verify_webhook($data, $hmac_header){
  $calculated_hmac = base64_encode(hash_hmac('sha256', $data, API_SECRET_KEY, true));
  return hash_equals($hmac_header, $calculated_hmac);
}

$hmac_header = $_SERVER['HTTP_JUMPSELLER_HMAC_SHA256'];
$data = '' // TODO: get data from request body in your controller
$verified = verify_webhook($data, $hmac_header);

We also sent other Jumpseller specific headers, which are helpful if your applications is handling multiple hooks and/or stores:

Jumpseller-Store-Code identifies the store code. Example: storecode if the store url is storecode.jumpseller.com
Jumpseller-Event identifies the event which fired this webhook.
PHP Examples
Example: Receiving an Order Paid notification

  $post = file_get_contents('php://input'); //post data is in another format (e.g. JSON, etc.)

  file_put_contents("jumpseller_postorder.txt", $post, FILE_APPEND); //store data locally (JSON to a file in this case)
Parsing the Order Paid notification

  $post_data = file_get_contents("jumpseller_postorder.txt"); //read JSON file

  $json_data = json_decode($post_data, true); //Takes a JSON encoded string and converts it into a PHP variable.

  echo $json_data['order']['id'];

  echo $json_data['order']['customer']['email'];
