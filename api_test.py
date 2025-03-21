import requests
import concurrent.futures
import time

API_URL = "http://127.0.0.1:8000/transaction/debit"


ACCOUNT_ID = "40"

NUM_REQUESTS = 200000


TRANSACTION_AMOUNT = 0.0

def send_debit_request():

    payload = {
        "account_id": ACCOUNT_ID,
        "amount": TRANSACTION_AMOUNT
    }

    start_time = time.time()
    response = requests.post(API_URL, json=payload)
    end_time = time.time()

    return {
        "status_code": response.status_code,
        "response": response.json(),
        "time_taken": round(end_time - start_time, 4)
    }

def run_concurrent_requests():
    with concurrent.futures.ThreadPoolExecutor(max_workers=1) as executor:
        futures = [executor.submit(send_debit_request) for _ in range(NUM_REQUESTS)]
        results = [future.result() for future in concurrent.futures.as_completed(futures)]

    # Print test results
    for i, result in enumerate(results):
        print(f"Request {i+1}:")
        print(f"Status Code: {result['status_code']}")
        print(f"Response: {result['response']}")
        print(f" Time Taken: {result['time_taken']}s\n")

if __name__ == "__main__":
    print(f"Sending {NUM_REQUESTS} concurrent debit requests...")
    run_concurrent_requests()
