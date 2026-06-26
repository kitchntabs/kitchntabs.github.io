PinoyWok Delivery System Requirements
System Overview

The PinoyWok Delivery System is an application that manages the end-to-end food delivery process for PinoyWok, a food service business. The system integrates with Jumpseller (an e-commerce platform) to receive orders, tracks delivery status, notifies customers, and provides interfaces for delivery drivers and administrators.

Core Components:
-Order Processing System: Receives orders from Jumpseller through a webhook, processes them, and stores them in the current Order system implemented in the dash-backend.
-Delivery Tracking System: Tracks the status of orders through their lifecycle.
-Notification System: Sends email notifications to customers about order status changes, and sends internal messages to system users.
-Driver Interface: Provides tools for delivery drivers to manage their deliveries.
-Admin Dashboard: Allows administrators to view and manage orders.

Customer Stories

Order Placement:
-As a customer, I want to place an order through the PinoyWok website (Jumpseller platform), implicit. not related to this system.
-As a customer, I want to receive a confirmation when my order updates its delivery status (prepared, assigned to driver, out for delivery, delivered)

Order Tracking

As a customer, I want to track the status of my order in real-time
As a customer, I want to receive notifications when my order status changes (preparation, assigned to driver, out for delivery, delivered)
As a customer, I want to see the estimated preparation and delivery times for my order
As a customer, I want to access a tracking page with a map showing my delivery location
Order Information

As a customer, I want to see detailed information about my order (items, quantities, prices)
As a customer, I want to see my delivery address and contact information
Driver Stories
Order Assignment

As a driver, I want to be assigned orders for delivery
As a driver, I want to see order details including customer information and delivery location
Order Status Updates

As a driver, I want to update the order status when I pick up an order (withdrawed)
As a driver, I want to update the order status when I deliver an order (delivered)
As a driver, I want to access a secure page to manage my assigned deliveries using a unique code
Navigation

As a driver, I want to see the delivery location on a map
As a driver, I want integration with navigation apps (like Waze) to get directions
Administrator Stories
Order Management

As an admin, I want to see all orders in the system
As an admin, I want to filter orders by date range and status
As an admin, I want to assign orders to specific drivers
As an admin, I want to track the status of all orders in real-time
System Monitoring

As an admin, I want to receive notifications about new orders
As an admin, I want to see statistics about order processing times and delivery performance
Technical Requirements
Integration Requirements

The system must integrate with Jumpseller's webhook API to receive order notifications
The system must use Google Maps API for geocoding and location services
The system must integrate with AWS SES for sending email notifications
Security Requirements

The system must authenticate webhook requests from Jumpseller using HMAC-SHA256
The system must provide secure access to order details using unique codes
The system must store sensitive information in AWS Secrets Manager
Performance Requirements

The system must handle real-time updates via WebSockets
The system must calculate accurate preparation times based on order complexity
The system must provide estimated delivery times based on preparation time
Infrastructure Requirements

The system must be built using AWS serverless architecture (Lambda, API Gateway, DynamoDB)
The system must use custom domain names for various endpoints (delivery, tracking, webhooks)
The system must implement proper error handling and logging
Order Lifecycle
Order Received: Order is received from Jumpseller webhook
Order Paid: Initial status when order is confirmed and paid
Order Assigned: Order is assigned to a delivery driver
Order Withdrawed: Driver has picked up the order from the restaurant
Order Delivered: Driver has delivered the order to the customer
Each status change triggers notifications to the customer and updates across the system via WebSockets.

System Architecture
The application is built using a serverless architecture on AWS with the following components:

AWS Lambda for processing logic
API Gateway for RESTful and WebSocket APIs
DynamoDB for data storage
AWS SES for email notifications
AWS Secrets Manager for secure storage of API keys
CloudWatch for logging and monitoring
The system uses custom domains for different interfaces:

delivery.pinoywok.cl - Driver interface
tracking.pinoywok.cl - Customer tracking interface
orders.pinoywok.cl - Admin interface
webhooks.pinoywok.cl - Webhook endpoints for Jumpseller