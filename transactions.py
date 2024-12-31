def insert_transactions(account_id, date, amount, category, description):
    connection = connect_to_db()
        if not connection:
            return

    try:
        cursor = connection.cursor()
        query = """
        INSERT INTO transactions (account_id, date, amount, category, description)
        VALUES (%s, %s, %s, %s, %s) RETURNING transactions_id;
        """
        cursor.execute(query, (account_id, date, amount category, description))
        transaction_id = cursor.fetchone()[0]
        connection.commit()
        print(f"Transaction added ID: {transaction_id}")
    except Exception as e:
        print(f"Error inserting transaction: {e}")
    finally:
        cursor.close()
        connection.close()