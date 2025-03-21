
# Bank Transaction API

## Tools used:
1. FastAPI  
2. Pydantic  
3. PostgreSQL  
4. psycopg2  
5. Uvicorn  
6. Requests (for testing)  
7. Concurrent Futures (for stress testing)  

---

## Implemented API:
**POST** `/transaction/debit`  

---

## Installation:
```bash
pip install -r requirements.txt
```

Start the FastAPI server:
```bash
uvicorn main:app --reload
```

Check API documentation:  
- [http://localhost:8000/docs](http://localhost:8000/docs)  
- [http://localhost:8000/redoc](http://localhost:8000/redoc)  

---

## Database Setup:
- Uses **PostgreSQL** for transaction storage.  
- Ensure a PostgreSQL database is running with the following credentials:  
  - **Database**: `postgres`  
  - **User**: `postgres`  
  - **Password**: `*postgres*`  
  - **Host**: `localhost`  
  - **Port**: `5432`  

### Creating Dummy Data:
Run the following to create and insert sample accounts:
```python
from create_insert_in_db import create_insert_dummy

create_insert_dummy()
```

---

## Workflow:

### 1. Take input:
Sample input for a debit transaction:
```json
{
    "account_id": "40",
    "amount": 500.00
}
```

### 2. Process Debit Transaction:
- **Locks the account row** using `SELECT ... FOR UPDATE` to prevent concurrent modifications.  
- Checks if the account exists.  
- Ensures sufficient balance before processing the debit.  
- Updates the balance and increments the version number.  
- Returns the updated balance.  
- Rolls back in case of errors to prevent inconsistent transactions.  

### 3. Handling Concurrency:
- Uses **optimistic locking** by checking the `version` column.  
- If two concurrent requests try to update the same account, one will fail with **HTTP 409 Conflict**.  
- If another request modifies the balance before the update, the transaction is rejected.  

### 4. Sample API Response:
Successful debit:
```json
{
    "message": "Debit Transaction Successful",
    "old_balance": 1000.00,
    "new_balance": 500.00
}
```

Error cases:
- **Account Not Found** → `404 Not Found`  
- **Insufficient Balance** → `400 Bad Request`  
- **Concurrent Modification** → `409 Conflict`  
- **Server Error** → `500 Internal Server Error`  

---

## Performance Testing:
The `api_test.py` script sends **200,000 concurrent debit requests** to test the API's ability to handle high load.

### Running the test:
```bash
python api_test.py
```

### Test Results:
Each request logs:
- HTTP Status Code  
- API Response  
- Time Taken (in seconds)  

Example output:
```
Request 1:
Status Code: 200
Response: {"message": "Debit Transaction Successful", "old_balance": 1000.00, "new_balance": 500.00}
Time Taken: 0.0023s
```

---

## File Structure:
### `main.py`:
- Implements FastAPI endpoint `/transaction/debit`.  
- Uses PostgreSQL for database transactions.  
- Handles concurrency using row-level locks and versioning.  
- Implements error handling.  

### `api_test.py`:
- Sends multiple concurrent requests to test API performance.  
- Measures response time and logs results.  

### `create_insert_in_db.py`:
- Contains functions to create and insert dummy data into PostgreSQL.  

---


