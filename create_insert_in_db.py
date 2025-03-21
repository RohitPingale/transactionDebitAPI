import psycopg2

def create_insert_dummy():
    connection = psycopg2.connect(database = "postgres", user = "postgres", password = "postgres", host  = 'localhost', port = 5432)

    cursor = connection.cursor()

    cursor.execute(
        """
        CREATE TABLE IF NOT EXIST account (
        id SERIAL PRIMARY KEY,
        balance DECIMAL(15,2) NOT NULL DEFAULT 0.00,
        version INT NOT  NULL DEFAULT 1,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP 
        )
        """
    )
    connection.commit()

    #DummyData
    for i in range(1, 21):
        cursor.execute(
            """
            INSERT INTO account (balance, version)
            VALUES (%s, %s)
            """,
            (round(1000 * i * 0.75, 2), 1)  
        )


    connection.commit()
    cursor.close()
    connection.close()
