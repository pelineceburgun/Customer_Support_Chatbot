
import nltk
import requests
import json
import random
import tkinter as tk
from tkinter import scrolledtext
import customtkinter as ctk
from nltk.tokenize import word_tokenize

from database import add_customer, save_message, get_chat_history

nltk.download('punkt')

import os
os.environ['TCL_LIBRARY'] = r"C:\Users\pelin\AppData\Local\Programs\Python\Python313\tcl\tcl8.6"
os.environ['TK_LIBRARY'] = r"C:\Users\pelin\AppData\Local\Programs\Python\Python313\tcl\tk8.6"

api_key = "YOUR_OWN_API_KEY"

url = "FIND_URL_YOURSELF"
fallback_responses = [
    "Sorry,I couldn't understand. Can you ask more clearly?",
    "I'm not sure about that. How can i help you?",
    "I can't answer right now, but i still continue to learn!"
]

customer_name = "Pelin"
customer_email = "pelin@example.com"
customer_phone = "555-1234"

from database import add_customer, save_message, get_chat_history, customer_exists


if not customer_exists(customer_email):
    add_customer(customer_name, customer_email, customer_phone)


def classify_message(message):
    tokens = word_tokenize(message.lower())
    if any(word in tokens for word in ["hello", "hi", "greetings", "hiya", "morning"]):
        return "greetings"

    elif any(word in tokens for word in ["faq", "question", "info", "what"]):
        return "faqs"

    elif any(word in tokens for word in ["support", "help", "please", "need"]):
        return "support_ticket"

    elif any(word in tokens for word in ["agent", "human", "representative", "person"]):
        return "human_agent"

    return "unknown"


def chatbot_response(user_message):
    category = classify_message(user_message)

    if category == "greetings":
        messages = [{"role": "user", "content": "Hello, how are you?"}]

    elif category == "faqs":
        messages = [{"role": "user", "content": "Can you tell me about your store hours and return policy?"}]

    elif category == "support_ticket":
        messages = [{"role": "user", "content": "I need help with a refund. How can I get started?"}]

    elif category == "human_agent":
        return "I'm routing you to a human representative. Please wait a few seconds..."

    else:
        return random.choice(fallback_responses)

    response = requests.post(
        url=url,
        headers={
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json",
        },
        data=json.dumps({
            "model": "deepseek/deepseek-r1:free",
            "messages": messages
        })
    )
    if response.status_code == 200:
        response_data = response.json()
        return response_data.get("choices", [{}])[0].get("message", {}).get("content", "No response received.")
    else:
        return f"Error: {response.status_code} - {response.text}"


def send_message():
    user_input = entry.get().strip()
    if not user_input:
        return


    add_message(user_input, "user")


    save_message(customer_email, "user", user_input)

    entry.delete(0, ctk.END)


    bot_reply = chatbot_response(user_input)


    add_message(bot_reply, "bot")


    save_message(customer_email, "bot", bot_reply)


def add_message(text, sender):

    frame = ctk.CTkFrame(chat_scrollable, fg_color=("gray90" if sender == "bot" else "dodgerblue"), corner_radius=15)
    frame.pack(anchor="w" if sender == "bot" else "e", padx=5, pady=2, fill="none")

    label = ctk.CTkLabel(frame, text=text, wraplength=350, justify="left" if sender == "bot" else "right",
                         fg_color=("gray90" if sender == "bot" else "dodgerblue"),
                         text_color="black" if sender == "bot" else "white",
                         corner_radius=10, padx=8, pady=5)
    label.pack(padx=5, pady=2)

    chat_scrollable.update_idletasks()
    chat_scrollable._parent_canvas.yview_moveto(1.0)



ctk.set_appearance_mode("Dark")
ctk.set_default_color_theme("blue")

window = ctk.CTk()
window.title("Customer Support Chatbot")
window.geometry("500x600")

chat_frame = ctk.CTkFrame(window)
chat_frame.pack(pady=10, padx=10, fill="both", expand=True)

chat_scrollable = ctk.CTkScrollableFrame(chat_frame, width=400, height=350)
chat_scrollable.pack(fill="both", expand=True)

entry = ctk.CTkEntry(window, width=300, height=40, corner_radius=10)
entry.pack(pady=5)

send_button = ctk.CTkButton(window, text="Send", command=send_message)
send_button.pack(pady=10)

def open_user_registration():

    register_window = ctk.CTkToplevel(window)
    register_window.title("Customer Registration")
    register_window.geometry("400x300")
    register_window.grab_set()


    title_label = ctk.CTkLabel(register_window, text="Please enter your details", font=("Arial", 16))
    title_label.pack(pady=10)


    name_label = ctk.CTkLabel(register_window, text="Name:")
    name_label.pack()
    name_entry = ctk.CTkEntry(register_window)
    name_entry.pack(pady=5)


    email_label = ctk.CTkLabel(register_window, text="Email:")
    email_label.pack()
    email_entry = ctk.CTkEntry(register_window)
    email_entry.pack(pady=5)


    phone_label = ctk.CTkLabel(register_window, text="Phone:")
    phone_label.pack()
    phone_entry = ctk.CTkEntry(register_window)
    phone_entry.pack(pady=5)

    def submit_registration():
        name = name_entry.get().strip()
        email = email_entry.get().strip()
        phone = phone_entry.get().strip()

        if not name or not email or not phone:
            error_label.configure(text="Please fill in all fields!", text_color="red")
            return


        add_customer(name, email, phone)


        register_window.destroy()


    error_label = ctk.CTkLabel(register_window, text="")
    error_label.pack()


    submit_button = ctk.CTkButton(register_window, text="Submit", command=submit_registration)
    submit_button.pack(pady=10)


open_user_registration()



window.mainloop()
