# MoMo_Rest_API_Formative_Assignment
This is our Mobile Money (MoMo) REST API project. We built it to manage transaction records from SMS data using pure Python - no frameworks, just the standard library.

---

## Meet the Team

We're a group of ALU students who worked together to build this API:

**Darlene Ayinkamiye** - *Team Lead*
- Built the main API server and routing logic
- Implemented PUT and DELETE endpoints
- Created the DSA comparison tool
- Coordinated the team and integrated everything

**Chely Kelvin Sheja** - *Data & Testing*
- Parsed the XML data and converted it to JSON
- Designed our data structures
- Built the GET endpoints
- Wrote tests and documentation

**Solomon Leek** - *Security*
- Created the authentication system
- Handled authorization and security
- Documented security concerns
- Verified all test cases

Check out our full [Team Participation Sheet](team_participation.md) for more details.

---

## What We Built

- Parse SMS transaction data from XML to JSON
- Full CRUD API (Create, Read, Update, Delete)
- Basic Authentication to protect endpoints
- Performance comparison: Linear Search vs Dictionary Lookup

---

## Quick Start

### 1. Clone and Run

```bash
git clone https://github.com/solomon-211/MoMo_Rest_API_Formative_Assignment
cd MoMo_Rest_API_Formative_Assignment/momo-api-alu-final/
python api/server.py
```

That's it! No pip install needed. Server runs on http://localhost:8000

### 2. Try It Out

```bash
# Get all transactions (login required)
curl -u admin:password http://localhost:8000/transactions

# Get one transaction
curl -u admin:password http://localhost:8000/transactions/1

# Create a new transaction
curl -u admin:password -X POST http://localhost:8000/transactions \
  -H "Content-Type: application/json" \
  -d '{"type":"Send Money","amount":5000,"sender":"250780000001","receiver":"250780000002"}'

# Update a transaction
curl -u admin:password -X PUT http://localhost:8000/transactions/1 \
  -H "Content-Type: application/json" \
  -d '{"amount": 7500, "status": "refunded"}'

# Delete a transaction
curl -u admin:password -X DELETE http://localhost:8000/transactions/1
```

### Login Credentials

| Username | Password |
|----------|----------|
| admin | password |
| user1 | test123 |
| developer | devpass |

---

## API Endpoints

| Method | Endpoint | What it does |
|--------|----------|--------------|
| GET | /transactions | List all transactions |
| GET | /transactions/{id} | Get one transaction |
| POST | /transactions | Create new transaction |
| PUT | /transactions/{id} | Update a transaction |
| DELETE | /transactions/{id} | Delete a transaction |

See [docs/api_docs.md](docs/api_docs.md) for full documentation with examples.

---

## DSA Comparison

We compared two ways to search for transactions:

```bash
python dsa/search_comparison.py
```

**Results:** Dictionary lookup is about **30x faster** than linear search!

| Method | Speed | Why |
|--------|-------|-----|
| Linear Search | O(n) | Checks each item one by one |
| Dictionary Lookup | O(1) | Direct access using hash table |

---

## Project Structure

```
momo-api-alu-final/
+-- api/
|   +-- server.py          # Main API server
|   +-- auth.py            # Authentication
+-- data/
|   +-- modified_sms_v2.xml
+-- docs/
|   +-- api_docs.md        # Full API docs
+-- dsa/
|   +-- parser.py          # XML parser
|   +-- search_comparison.py
+-- screenshots/           # Test screenshots
+-- tests/                 # Test scripts
+-- README.md
+-- report.pdf
+-- team_participation.md
```

---

## Security Note

We used Basic Auth for this project since it's simple to implement. But we know it's not great for production because:

- Credentials are just base64 encoded (not encrypted)
- No token expiration
- Vulnerable without HTTPS

For real apps, use **JWT** or **OAuth 2.0** instead.

---

## Screenshots

All our test screenshots are in the [screenshots/](screenshots/) folder showing successful requests and error handling.

---

## Links

- [API Documentation](docs/api_docs.md)
- [Team Participation Sheet](team_participation.md)
- [Project Report](report.pdf)
