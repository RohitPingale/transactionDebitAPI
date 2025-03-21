
from  fastapi import  FastAPI, HTTPException
from create_insert_in_db import create_insert_dummy
from pydantic import BaseModel
from psycopg2.extras import DictCursor
import psycopg2 
import uvicorn

app = FastAPI()

connection = psycopg2.connect(database = "postgres", user = "postgres", password = "postgres", host  = 'localhost', port = 5432)

cursor = connection.cursor()


class TransactionRequest(BaseModel):
    account_id: str
    amount: float

@app.post("/transaction/debit")
async def debit_account(request:TransactionRequest):
    cur = connection.cursor(cursor_factory = DictCursor)
    try:
        # on update will lock the execution
        cur.execute(
            "select  balance, version from account where id = %s for update;",(request.account_id,)
        )
        account  = cur.fetchone()
        # print(account)

        if not  account:
            raise HTTPException(status_code =404, deatil ="account not found")
        balance, current_version = account["balance"],account["version"]

        if balance < request.amount:
            raise HTTPException(status_code=400, detail="insufficient balance")

        cur.execute(
            """
            update account
            set balance  = balance- %s, version = version+1, updated_at = current_timestamp
            where id = %s and version = %s
            returning balance; 
            """,(request.amount,request.account_id,current_version))
        updated_account = cur.fetchone()

        if not updated_account:
            raise HTTPException(status_code=409,detail="concurrent request on same account")
        
        connection.commit()
        return {"message":"Debit Transacaction Sucessful","old_balance":account["balance"], "new_balance":updated_account["balance"]}
    except Exception as e:
        connection.rollback()
        raise HTTPException(status_code= 500, detail=str(e))

if __name__ == "__main__":
    #RUN it Once to see API working
    # create_insert_dummy()
    uvicorn.run(app, host = "0.0.0.0", port= 8000)