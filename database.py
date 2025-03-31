import sqlite3

def add_customer(name, email, phone):

    conn = sqlite3.connect("chatbot.db")
    cursor = conn.cursor()
    try:
        cursor.execute("INSERT INTO customers (name, email, phone) VALUES (?, ?, ?)", (name, email, phone))
        conn.commit()
        print(f"{name} successfully added!")
    except sqlite3.IntegrityError:
        print("This e-mail already exists!")

    conn.close()


def save_message(customer_email, sender, message):
    connection = sqlite3.connect("chatbot.db")
    cursor = connection.cursor()


    cursor.execute("SELECT id FROM customers WHERE email = ?", (customer_email,))
    customer = cursor.fetchone()

    if customer is None:
        print(f"Error: No customer found with email {customer_email}")
        connection.close()
        return

    customer_id = customer[0]

    cursor.execute(
        "INSERT INTO messages (customer_id, sender, message) VALUES (?, ?, ?)",
        (customer_id, sender, message)
    )

    connection.commit()
    connection.close()


def get_chat_history(customer_email):

    conn = sqlite3.connect("chatbot.db")
    cursor = conn.cursor()


    cursor.execute("SELECT id FROM customers WHERE email = ?", (customer_email,))
    customer = cursor.fetchone()

    if customer:
        customer_id = customer[0]
        cursor.execute("SELECT sender, message, created_at FROM messages WHERE customer_id = ? ORDER BY created_at",
                       (id,))
        messages = cursor.fetchall()

        print("\n--- Past Messages ---")
        for msg in messages:
            print(f"{msg[0]} ({msg[2]}): {msg[1]}")
        print("------------------------\n")
    else:
        print("No message found for this customer.")

    conn.close()
def customer_exists(email):
    conn = sqlite3.connect("chatbot.db")
    cursor = conn.cursor()

    cursor.execute("SELECT id FROM customers WHERE email = ?", (email,))
    result = cursor.fetchone()

    conn.close()

    return result is not None
