# MoMo API - Test Scripts

This folder contains automated test scripts for the MoMo Transaction REST API.

## Available Tests

| File | Platform | Description |
|------|----------|-------------|
| `test_api.sh` | Linux/Mac | Bash script using curl |
| `test_api.ps1` | Windows | PowerShell script |

## How to Run

### Prerequisites
- API server must be running on `http://localhost:8000`
- Valid credentials: `admin` / `password`

### Start the Server First
```bash
python API/server.py
```

### Run Tests (Windows PowerShell)
```powershell
cd tests
powershell -ExecutionPolicy Bypass -File test_api.ps1
```

### Run Tests (Linux/Mac)
```bash
cd tests
chmod +x test_api.sh
./test_api.sh
```

## Test Coverage

| # | Test Case | Method | Endpoint | Expected |
|---|-----------|--------|----------|----------|
| 1 | List all transactions | GET | /transactions | 200 OK |
| 2 | Get single transaction | GET | /transactions/5 | 200 OK |
| 3 | Create transaction | POST | /transactions | 201 Created |
| 4 | Update transaction | PUT | /transactions/3 | 200 OK |
| 5 | Delete transaction | DELETE | /transactions/20 | 200 OK |
| 6 | Invalid credentials | GET | /transactions | 401 Unauthorized |
| 7 | Non-existent ID | GET | /transactions/999 | 404 Not Found |
| 8 | Missing required fields | POST | /transactions | 400 Bad Request |

## Quick Manual Tests (curl)

```bash
# GET all
curl -u admin:password http://localhost:8000/transactions

# GET one
curl -u admin:password http://localhost:8000/transactions/1

# POST new
curl -u admin:password -X POST http://localhost:8000/transactions \
  -H "Content-Type: application/json" \
  -d '{"type":"Send Money","amount":5000,"sender":"250780000001","receiver":"250780000002"}'

# PUT update
curl -u admin:password -X PUT http://localhost:8000/transactions/1 \
  -H "Content-Type: application/json" \
  -d '{"amount":7500,"status":"refunded"}'

# DELETE
curl -u admin:password -X DELETE http://localhost:8000/transactions/1

# Test wrong password (should return 401)
curl -u admin:wrong http://localhost:8000/transactions
```

## Author
- **Darlene Ayinkamiye** - Test scripts and verification
