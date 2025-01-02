import psycopg2
from psycopg2 import sql
from accounts import connect_to_db # This imports from accounts.py


# Function inserts transaction into the transactions table in PostgreSQL
def insert_transactions(account_id, date, amount, category, description):
    connection = connect_to_db()
    if not connection:
        return

    try:
        cursor = connection.cursor()
        query = """
        INSERT INTO transactions (account_id, date, amount, category, description)
        VALUES (%s, %s, %s, %s, %s) RETURNING transaction_id;
        """
        cursor.execute(query, (account_id, date, amount, category, description))
        transaction_id = cursor.fetchone()[0]
        connection.commit()
        print(f"Added Transaction ID: {transaction_id}")
    except Exception as e:
        print(f"Error inserting transaction: {e}")
    finally:
        cursor.close()
        connection.close()

# Function fetches the transactions
def fetch_transactions(account_id=None):
    connection = connect_to_db()
    if not connection:
        return

    try:
        cursor = connection.cursor()
        if account_id:
            query = "SELECT * FROM transactions WHERE account_id = %s;"
            cursor.execute(query, (account_id,))
        else:
            query = "SELECT * FROM transactions;"
            cursor.execute(query)
        transactions = cursor.fetchall()
        for transaction in transactions:
            transaction_id, account_id, date, amount, category, description = transaction
            print(f"Transaction ID: {transaction_id}")
            print(f"  Account ID: {account_id}")
            print(f"  Date: {date}")
            print(f"  Amount: ${amount}")
            print(f"  Category: {category}")
            print(f"  Description: {description}\n")
        return transactions
    except Exception as e:
        print(f"Error fetching transactions: {e}")
        return []
    finally:
        cursor.close()
        connection.close()