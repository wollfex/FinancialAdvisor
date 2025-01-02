from flask import Flask, jsonify, request
from accounts import insert_account, fetch_accounts # Pulls functions from accounts.py
from transactions import insert_transactions, fetch_transactions # Pulls functions from transactions.py

app = Flask(__name__)

# Endpoint: Fetch all accounts
@app.route("/accounts", methods=["GET"])
def get_accounts():
    accounts = fetch_accounts()
    result = [
        {
            "account_id": account[0],
            "name": account[1],
            "type": account[2],
            "balance": float(account[3]), # Converts decimal to a float
            "created_at": account[4].isoformat() # Formats timestamp for JSON
        }
        for account in accounts
    ]
    return jsonify(result)

# Endpoint: Adds a new account
@app.route("/accounts", methods=["POST"])
def add_accounts():
    data = request.json
    if not all(key in data for key in ("name", "type", "balance")):
        return jsonify({"error": "Missing required fields: name, type, balance"}), 400

    name = data["name"]
    account_type = data["type"]
    balance = data["balance"]
    insert_account(name, account_type, balance)
    return jsonify({"message": "Account added"}), 201

# Endpoint: Fetch all or filtered transactions
@app.route("/transactions", methods=["GET"])
def get_transactions():
    account_id = request.agrs.get("account_id")
    if account_id:
        transactions = fetch_transactions(int(account_id))
    else:
        transactions = fetch_transactions()

    result = [
        {
            "transaction_id": transactions[0],
            "account_id": transactions[1],
            "date": transactions[2],
            "amount": transactions[3],
            "category": transactions[4],
            "description": transactions[5]
        }
    ]
    return jsonify(result)

# Endpoint: Add a new transaction
@app.route("/transactions", methods=["POST"])
def add_transaction():
    data = request.json
    if not all(key in data for key in ("account_id", "date", "amount", "category", "description")):
        return jsonify({"error": "Missing required fields: account_id, date, amount, category, description"}), 400

    account_id = data["account_id"]
    date = data["date"]
    amount = data["amount"]
    category = data["category"]
    description = data["description"]
    insert_transactions(account_id, date, amount, category, description)
    return jsonify({"message": "Transaction added"}), 201
