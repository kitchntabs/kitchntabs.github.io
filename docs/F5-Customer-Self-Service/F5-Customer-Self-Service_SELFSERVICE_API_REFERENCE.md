
# Self-Service Kiosk - API Reference

> Complete API documentation for the Self-Service Kiosk feature.

---

## Base URL

```
Production: https://api.kitchntabs.app/api
Development: http://localhost:8000/api
```

---

## Authentication

Self-Service endpoints are **public** and do not require authentication tokens. Instead, they use session-based access control via the `selfservice_session` parameter.

---

## Session Endpoints

### Create Client Session

Creates a new self-service session for a tenant.

```http
POST /public/selfservice/client_session/{tenantSlug}
```

**Path Parameters:**

| Parameter | Type | Description |
|-----------|------|-------------|
| `tenantSlug` | string | URL-friendly tenant identifier |

**Request Body:**

```json
{
  "table_number": "12",
  "meta": {
    "location": "Patio"
  }
}
```

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `table_number` | string | No | Table or location identifier |
| `meta` | object | No | Additional metadata |

**Response (200):**

```json
{
  "data": {
    "hash": "DFJNL",
    "tenant_id": "550e8400-e29b-41d4-a716-446655440000",
    "status": "pending",
    "table_number": "12"
  },
  "message": "Self-service session created successfully"
}
```

**Errors:**

| Code | Description |
|------|-------------|
| 404 | Tenant not found or inactive |
| 422 | Validation failed |

---

### Get Session Auth

Validates and activates a session, returning tenant data.

```http
GET /public/selfservice/{hash}/getSessionAuth
```

**Path Parameters:**

| Parameter | Type | Description |
|-----------|------|-------------|
| `hash` | string | 5-character session hash |

**Response (200):**

```json
{
  "tenant": {
    "id": "550e8400-e29b-41d4-a716-446655440000",
    "name": "My Restaurant",
    "slug": "my-restaurant"
  },
  "auth": {
    "tenantSettings": {
      "primary_currency": { "id": 1, "code": "CLP" },
      "primary_language": { "id": 1, "code": "es" }
    },
    "tenantImages": {
      "banner_url": "https://...",
      "horizontal_logo_url": "https://...",
      "squared_logo_url": "https://..."
    }
  },
  "tenantSettings": {},
  "tenantImages": {},
  "systemValues": {
    "point_of_sales": [],
    "selfservice": {
      "tenant_id": "550e8400-e29b-41d4-a716-446655440000",
      "tenant_name": "My Restaurant",
      "session_hash": "DFJNL",
      "table_number": "12",
      "customer_name": null
    },
    "sessionId": "DFJNL",
    "tenant": {
      "id": "550e8400-e29b-41d4-a716-446655440000",
      "name": "My Restaurant",
      "slug": "my-restaurant"
    }
  },
  "redirectTo": "/public/selfservice/tab/create"
}
```

**Errors:**

| Code | Description | Body |
|------|-------------|------|
| 400 | Invalid session status | `{ "message": "Session is not valid", "current_status": "cancelled" }` |
| 403 | Client identity mismatch | `{ "message": "Access denied", "error_code": "CLIENT_IDENTITY_MISMATCH" }` |
| 404 | Session not found | `{ "message": "Session not found" }` |
| 410 | Session expired | `{ "message": "Session has expired", "expired_at": "..." }` |

---

### Get Session

Retrieves session details.

```http
GET /public/selfservice/session/{hash}
```

**Response (200):**

```json
{
  "session": {
    "hash": "DFJNL",
    "tenant_id": "550e8400-e29b-41d4-a716-446655440000",
    "tenant_name": "My Restaurant",
    "status": "active",
    "customer_name": null,
    "table_number": "12",
    "meta": {
      "activated_at": "2026-01-07T19:00:00Z",
      "client_ip": "192.168.1.1"
    }
  }
}
```

---

### Update Session

Updates session metadata.

```http
PUT /public/selfservice/session/{hash}
```

**Request Body:**

```json
{
  "customer_name": "John Doe",
  "table_number": "15",
  "meta": {
    "special_request": "Birthday party"
  }
}
```

**Response (200):**

```json
{
  "session": {
    "hash": "DFJNL",
    "status": "active",
    "customer_name": "John Doe",
    "table_number": "15"
  },
  "message": "Session updated successfully"
}
```

---

### Complete Session

Marks a session as completed.

```http
POST /public/selfservice/session/{hash}/complete
```

**Response (200):**

```json
{
  "session": {
    "hash": "DFJNL",
    "status": "completed"
  },
  "message": "Session completed successfully"
}
```

**Errors:**

| Code | Description |
|------|-------------|
| 409 | Session already completed |

---

### Cancel Session

Cancels an active session.

```http
POST /public/selfservice/session/{hash}/cancel
```

**Response (200):**

```json
{
  "session": {
    "hash": "DFJNL",
    "status": "cancelled"
  },
  "message": "Session cancelled successfully"
}
```

**Errors:**

| Code | Description |
|------|-------------|
| 409 | Cannot cancel completed session |

---

## Tab (Order) Endpoints

### List Tabs

Lists all tabs for a session.

```http
GET /public/selfservice/tab?selfservice_session={hash}
```

**Query Parameters:**

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `selfservice_session` | string | Yes | Session hash |
| `status` | string | No | Filter by status |

**Response (200):**

```json
{
  "data": [
    {
      "id": 123,
      "status": "created",
      "tenant_id": "uuid",
      "order": {
        "id": 456,
        "items": [
          {
            "id": 789,
            "product_id": "uuid",
            "quantity": 2,
            "product": {
              "name": "Hamburguesa",
              "price": 8990
            }
          }
        ]
      },
      "created_at": "2026-01-07T19:15:00Z"
    }
  ],
  "total": 1
}
```

---

### Get Tab

Retrieves a single tab.

```http
GET /public/selfservice/tab/{id}?selfservice_session={hash}
```

**Response (200):**

```json
{
  "id": 123,
  "status": "confirmed",
  "tenant": {
    "id": "uuid",
    "name": "My Restaurant"
  },
  "order": {
    "id": 456,
    "items": [...]
  }
}
```

---

### Create Tab

Creates a new tab (order).

```http
POST /public/selfservice/tab
Content-Type: application/json
```

**Request Body:**

```json
{
  "selfservice_session": "DFJNL",
  "delivery_method": "table",
  "order": {
    "items": [
      {
        "product_id": "550e8400-e29b-41d4-a716-446655440000",
        "quantity": 2,
        "notes": "No onions",
        "modifiers": [
          {
            "modifier_option_id": "uuid",
            "quantity": 1
          }
        ]
      }
    ],
    "notes": "Please hurry!"
  }
}
```

**Response (201):**

```json
{
  "id": 123,
  "status": "created",
  "order": {
    "id": 456,
    "total": 17980
  },
  "message": "Order submitted successfully"
}
```

---

### Update Tab

Updates an existing tab.

```http
PUT /public/selfservice/tab/{id}
Content-Type: application/json
```

**Request Body:**

```json
{
  "selfservice_session": "DFJNL",
  "order": {
    "items": [
      {
        "product_id": "uuid",
        "quantity": 3
      }
    ]
  }
}
```

---

### Download Sale Note

Downloads PDF receipt for a tab.

```http
GET /public/selfservice/tab/{id}/download-sale-note?selfservice_session={hash}
```

**Response:** PDF file download

**Errors:**

| Code | Description |
|------|-------------|
| 400 | Session required |
| 403 | Tab doesn't belong to session |
| 404 | Tab not found |

---

## Status Codes Summary

| Code | Meaning |
|------|---------|
| 200 | Success |
| 201 | Created |
| 400 | Bad Request |
| 403 | Forbidden (access denied) |
| 404 | Not Found |
| 409 | Conflict (already exists/processed) |
| 410 | Gone (expired) |
| 422 | Validation Error |
| 500 | Server Error |

---

## Session Lifecycle

```
pending → active → completed
           ↓
        cancelled
```

| Status | Can Order | Can Update | Duration |
|--------|-----------|------------|----------|
| pending | No | Yes | Until first access |
| active | Yes | Yes | 10 hours |
| completed | No | No | Permanent |
| cancelled | No | No | Permanent |
