import psycopg2
from psycopg2 import sql
from flask import Flask, jsonify, request




# connect to database
DB_NAME = "financial_tracker"
DB_USER = "postgres"
DB_PASSWORD = "armykid03"
DB_HOST = "localhost"
DB_PORT = "5432"

def connect_to_db():
    try:
        connection = psycopg2.connect(
            dbname=DB_NAME,
            user=DB_USER,
            password=DB_PASSWORD,
            host=DB_HOST,
            port=DB_PORT
        )
        print("Connected to database")
        return connection
    except Exception as e:
        print(f"Error connecting to the database: {e}")
        return None

# Test connection
if __name__ == "__main__":
    conn = connect_to_db()
    if conn:
        conn.close()

def insert_account(name, account_type, balance):
    connection = connect_to_db()
    if not connection:
        return

    try:
        cursor = connection.cursor()
        query = """
        INSERT INTO accounts (name, type, balance)
        VALUES (%s, %s, %s) RETURNING account_id;
        """
        cursor.execute(query, (name, account_type, balance))
        account_id = cursor.fetchone()[0]
        connection.commit()
        print(f"Account ID added: {account_id}")
    except Exception as e:
        print(f"Error inserting account: {e}")
    finally:
        cursor.close()
        connection.close()

# Example use
if __name__ == "__main__":
    insert_account("My Checking Account", "Checking", 1500.00)

def fetch_accounts():
    connection = connect_to_db()
    if not connection:
        return []

    try:
        cursor = connection.cursor()
        query = "SELECT * FROM accounts;"
        cursor.execute(query)
        accounts = cursor.fetchall()
        for account in accounts:
            print(account)
        return accounts
    except Exception as e:
        print(f"Error fetching accounts: {e}")
        return []
    finally:
        cursor.close()
        connection.close()

# Example use
if __name__ == "__main__":
    fetch_accounts()

app = Flask(__name__)

@app.route("/accounts", methods=["GET"])
def get_accounts():
    accounts = fetch_accounts()
    return jsonify(accounts)

@app.route("/accounts", methods=["POST"])
def add_account():
    data = request.json
    name = data["name"]
    account_type = data["type"]
    balance = data["balance"]
    insert_account(name, account_type, balance)
    return jsonify({"message": "Account added successfully!"}), 201

if __name__ == "__main__":
    app.run(debug=True)