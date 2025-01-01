import tkinter as tk
from tkinter import ttk
import requests

# Function to send API request
def send_request():
    url = url_entry.get()
    method = method_combobox.get()
    headers = {}
    body = body_text.get("1.0", tk.END)
    
    # Get headers from the header entries
    for header_entry in header_entries:
        header_key = header_entry[0].get()
        header_value = header_entry[1].get()
        if header_key and header_value:
            headers[header_key] = header_value
    
    try:
        # Send GET or POST request
        if method == "GET":
            response = requests.get(url, headers=headers)
        elif method == "POST":
            response = requests.post(url, headers=headers, data=body)
        
        # Display the response
        response_text.delete("1.0", tk.END)
        response_text.insert(tk.END, f"Status Code: {response.status_code}\n")
        response_text.insert(tk.END, f"Response Body:\n{response.text}")
    except Exception as e:
        response_text.delete("1.0", tk.END)
        response_text.insert(tk.END, f"Error: {e}")

# Function to add new header fields dynamically
def add_header_field():
    header_frame = ttk.Frame(headers_frame)
    header_key = ttk.Entry(header_frame, width=25)
    header_value = ttk.Entry(header_frame, width=25)
    
    header_key.grid(row=0, column=0, padx=5, pady=5)
    header_value.grid(row=0, column=1, padx=5, pady=5)
    
    header_frame.grid(row=len(header_entries), column=0, sticky="w", padx=10)
    header_entries.append((header_key, header_value))

# Creating the main window
root = tk.Tk()
root.title("API Tester")
root.geometry("800x600")

# URL entry
url_label = ttk.Label(root, text="API URL:")
url_label.pack(pady=5)
url_entry = ttk.Entry(root, width=100)
url_entry.pack(pady=5)

# Request Method dropdown
method_label = ttk.Label(root, text="Request Method:")
method_label.pack(pady=5)
method_combobox = ttk.Combobox(root, values=["GET", "POST"], state="readonly")
method_combobox.set("GET")
method_combobox.pack(pady=5)

# Headers Section
headers_frame = ttk.Frame(root)
headers_frame.pack(pady=10, anchor="w")

headers_label = ttk.Label(headers_frame, text="Headers:")
headers_label.grid(row=0, column=0, sticky="w")
header_entries = []

add_header_button = ttk.Button(root, text="Add Header", command=add_header_field)
add_header_button.pack(pady=5)

# Request Body (for POST requests)
body_label = ttk.Label(root, text="Request Body (for POST only):")
body_label.pack(pady=5)
body_text = tk.Text(root, height=10, width=80)
body_text.pack(pady=5)

# Send Request Button
send_button = ttk.Button(root, text="Send Request", command=send_request)
send_button.pack(pady=10)

# Response Section
response_label = ttk.Label(root, text="Response:")
response_label.pack(pady=5)
response_text = tk.Text(root, height=15, width=80)
response_text.pack(pady=5)

# Run the GUI
root.mainloop()
