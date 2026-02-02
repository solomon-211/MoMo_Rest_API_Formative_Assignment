# MoMo Transaction REST API Documentation

**Author:** Kamunuga Mparaye  
**Last Updated:** January 22, 2026

---

## Table of Contents
1. [Overview](#overview)
2. [Authentication](#authentication)
3. [Endpoints](#endpoints)
4. [Error Codes](#error-codes)
5. [Examples](#examples)

---

## Overview

The MoMo Transaction REST API provides secure access to mobile money transaction records. All endpoints require authentication and return JSON responses.

**Base URL:** `http://localhost:8000`

**Content Type:** `application/json`

---

## Authentication

All API endpoints require **Basic Authentication**.

### How to Authenticate

Include the `Authorization` header in your requests:

```
Authorization: Basic <base64-encoded-credentials>
```

Where `<base64-encoded-credentials>` is the Base64 encoding of `username:password`.

### Default Credentials

| Username | Password |
|----------|----------|
| admin    | password |
| user1    | test123  |
| developer| devpass  |

### Example Authentication Header

For username `admin` and password `password`:
```
Authorization: Basic YWRtaW46cGFzc3dvcmQ=
```

### Using curl
```bash
curl -u admin:password http://localhost:8000/transactions
```

### Using Postman
1. Go to the **Authorization** tab
2. Select **Basic Auth** from the Type dropdown
3. Enter username and password

---

## Endpoints

### 1. List All Transactions

**GET** `/transactions`

Retrieve a list of all transactions in the system.

#### Request

```http
GET /transactions HTTP/1.1
Host: localhost:8000
Authorization: Basic YWRtaW46cGFzc3dvcmQ=
```

#### Response (200 OK)

```json
{
  "success": true,
  "count": 22,
  "data": [
    {
      "id": 1,
      "type": "Send Money",
      "amount": 5000.0,
      "sender": "250780000001",
      "receiver": "250780000002",
      "timestamp": "2026-01-15T10:30:00",
      "status": "completed"
    },
    {
      "id": 2,
      "type": "Receive Money",
      "amount": 3000.0,
      "sender": "250780000003",
      "receiver": "250780000001",
      "timestamp": "2026-01-15T11:45:00",
      "status": "completed"
    }
  ]
}
```

---

### 2. Get Single Transaction

**GET** `/transactions/{id}`

Retrieve details of a specific transaction by ID.

#### Request

```http
GET /transactions/5 HTTP/1.1
Host: localhost:8000
Authorization: Basic YWRtaW46cGFzc3dvcmQ=
```

#### Response (200 OK)

```json
{
  "success": true,
  "data": {
    "id": 5,
    "type": "Send Money",
    "amount": 7500.0,
    "sender": "250780000002",
    "receiver": "250780000005",
    "timestamp": "2026-01-16T12:30:00",
    "status": "completed"
  }
}
```

#### Response (404 Not Found)

```json
{
  "error": true,
  "message": "Transaction with ID 999 not found",
  "status": 404
}
```

---

### 3. Create New Transaction

**POST** `/transactions`

Create a new transaction record.

#### Request

```http
POST /transactions HTTP/1.1
Host: localhost:8000
Authorization: Basic YWRtaW46cGFzc3dvcmQ=
Content-Type: application/json

{
  "type": "Send Money",
  "amount": 15000,
  "sender": "250780000001",
  "receiver": "250780000009",
  "timestamp": "2026-01-22T14:00:00",
  "status": "completed"
}
```

#### Required Fields

| Field    | Type   | Description                          |
|----------|--------|--------------------------------------|
| type     | string | Transaction type (e.g., "Send Money")|
| amount   | number | Transaction amount                   |
| sender   | string | Sender identifier                    |
| receiver | string | Receiver identifier                  |

#### Optional Fields

| Field     | Type   | Description                          |
|-----------|--------|--------------------------------------|
| timestamp | string | ISO 8601 timestamp                   |
| status    | string | Transaction status (default: "pending")|

#### Response (201 Created)

```json
{
  "success": true,
  "message": "Transaction created successfully",
  "data": {
    "id": 23,
    "type": "Send Money",
    "amount": 15000.0,
    "sender": "250780000001",
    "receiver": "250780000009",
    "timestamp": "2026-01-22T14:00:00",
    "status": "completed"
  }
}
```

#### Response (400 Bad Request)

```json
{
  "error": true,
  "message": "Missing required fields: amount, receiver",
  "status": 400
}
```

---

### 4. Update Transaction

**PUT** `/transactions/{id}`

Update an existing transaction. Only provided fields will be updated.

#### Request

```http
PUT /transactions/5 HTTP/1.1
Host: localhost:8000
Authorization: Basic YWRtaW46cGFzc3dvcmQ=
Content-Type: application/json

{
  "amount": 8000,
  "status": "refunded"
}
```

#### Response (200 OK)

```json
{
  "success": true,
  "message": "Transaction 5 updated successfully",
  "data": {
    "id": 5,
    "type": "Send Money",
    "amount": 8000.0,
    "sender": "250780000002",
    "receiver": "250780000005",
    "timestamp": "2026-01-16T12:30:00",
    "status": "refunded"
  }
}
```

#### Response (404 Not Found)

```json
{
  "error": true,
  "message": "Transaction with ID 999 not found",
  "status": 404
}
```

---

### 5. Delete Transaction

**DELETE** `/transactions/{id}`

Delete a transaction from the system.

#### Request

```http
DELETE /transactions/10 HTTP/1.1
Host: localhost:8000
Authorization: Basic YWRtaW46cGFzc3dvcmQ=
```

#### Response (200 OK)

```json
{
  "success": true,
  "message": "Transaction 10 deleted successfully",
  "data": {
    "id": 10,
    "type": "Receive Money",
    "amount": 8000.0,
    "sender": "250780000006",
    "receiver": "250780000001",
    "timestamp": "2026-01-19T11:00:00",
    "status": "completed"
  }
}
```

#### Response (404 Not Found)

```json
{
  "error": true,
  "message": "Transaction with ID 999 not found",
  "status": 404
}
```

---

## Error Codes

| Status Code | Description                                    |
|-------------|------------------------------------------------|
| 200         | Success                                        |
| 201         | Created - Resource successfully created        |
| 204         | No Content - Used for OPTIONS requests         |
| 400         | Bad Request - Invalid input or missing fields  |
| 401         | Unauthorized - Authentication failed           |
| 404         | Not Found - Resource does not exist            |
| 500         | Internal Server Error                          |

---

## Examples

### Example 1: List All Transactions (curl)

```bash
curl -u admin:password http://localhost:8000/transactions
```

### Example 2: Get Specific Transaction (curl)

```bash
curl -u admin:password http://localhost:8000/transactions/5
```

### Example 3: Create Transaction (curl)

```bash
curl -u admin:password \
  -X POST http://localhost:8000/transactions \
  -H "Content-Type: application/json" \
  -d '{
    "type": "Withdraw Cash",
    "amount": 50000,
    "sender": "250780000001",
    "receiver": "AGENT001",
    "timestamp": "2026-01-22T15:30:00",
    "status": "pending"
  }'
```

### Example 4: Update Transaction (curl)

```bash
curl -u admin:password \
  -X PUT http://localhost:8000/transactions/5 \
  -H "Content-Type: application/json" \
  -d '{
    "status": "completed",
    "amount": 7600
  }'
```

### Example 5: Delete Transaction (curl)

```bash
curl -u admin:password \
  -X DELETE http://localhost:8000/transactions/5
```

### Example 6: Unauthorized Request (curl)

```bash
curl -u admin:wrongpassword http://localhost:8000/transactions
```

**Response:**
```json
{
  "error": "Unauthorized",
  "message": "Invalid or missing authentication credentials",
  "status": 401
}
```

---

## Testing with Postman

### Setup

1. Open Postman
2. Create a new collection named "MoMo API Tests"
3. Set collection-level authorization:
   - Type: **Basic Auth**
   - Username: `admin`
   - Password: `password`

### Test Cases

#### Test 1: GET All Transactions
- Method: `GET`
- URL: `http://localhost:8000/transactions`
- Expected: 200 OK with list of transactions

#### Test 2: GET Single Transaction
- Method: `GET`
- URL: `http://localhost:8000/transactions/1`
- Expected: 200 OK with transaction details

#### Test 3: POST New Transaction
- Method: `POST`
- URL: `http://localhost:8000/transactions`
- Body (JSON):
```json
{
  "type": "Pay Bill",
  "amount": 12000,
  "sender": "250780000001",
  "receiver": "UTILITY001"
}
```
- Expected: 201 Created with new transaction

#### Test 4: PUT Update Transaction
- Method: `PUT`
- URL: `http://localhost:8000/transactions/1`
- Body (JSON):
```json
{
  "status": "refunded"
}
```
- Expected: 200 OK with updated transaction

#### Test 5: DELETE Transaction
- Method: `DELETE`
- URL: `http://localhost:8000/transactions/1`
- Expected: 200 OK with deleted transaction details

#### Test 6: Unauthorized Request
- Method: `GET`
- URL: `http://localhost:8000/transactions`
- Authorization: Use wrong password
- Expected: 401 Unauthorized

---

## Transaction Types

Common transaction types in the system:

- **Send Money** - Transfer funds to another user
- **Receive Money** - Receive funds from another user
- **Withdraw Cash** - Withdraw cash from agent
- **Deposit Cash** - Deposit cash via agent
- **Pay Bill** - Pay utility bills or services
- **Airtime Purchase** - Buy mobile airtime

---

## Rate Limiting

Currently, there is no rate limiting implemented. For production deployment, consider:

- **Request rate limiting** (e.g., 100 requests per minute per user)
- **IP-based throttling** to prevent abuse
- **429 Too Many Requests** response for exceeded limits

---

## CORS Support

The API includes CORS headers to allow cross-origin requests:

```
Access-Control-Allow-Origin: *
Access-Control-Allow-Methods: GET, POST, PUT, DELETE, OPTIONS
Access-Control-Allow-Headers: Content-Type, Authorization
```

For production, restrict `Access-Control-Allow-Origin` to specific domains.

---

## Notes

1. **Data Persistence:** Currently, data is stored in-memory. Restarting the server will reset to initial XML data.

2. **ID Assignment:** New transactions receive auto-incremented IDs starting from the highest existing ID + 1.

3. **Timestamp:** If not provided in POST requests, timestamp defaults to empty string. Consider server-side timestamp generation for production.

4. **Validation:** Basic validation is performed. Enhance with:
   - Amount must be positive
   - Phone number format validation
   - Transaction type enum validation

5. **Security:** See `api/auth.py` for detailed security analysis and recommendations.

---

## Support

For issues or questions, contact your team lead or refer to the project README.
