from flask import Flask, request, render_template_string
import requests

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        url = request.form.get('url')
        method = request.form.get('method')
        headers = {}

        # Add headers to the dictionary
        header_count = int(request.form.get('header_count', 0))
        for i in range(header_count):
            header_key = request.form.get(f'header_key_{i}')
            header_value = request.form.get(f'header_value_{i}')
            if header_key and header_value:
                headers[header_key] = header_value

        body = request.form.get('body')
        files = None

        # Handle file uploads for POST request
        if 'file' in request.files:
            file = request.files['file']
            files = {'file': (file.filename, file.stream, file.content_type)}

        try:
            if method == 'GET':
                response = requests.get(url, headers=headers)
            elif method == 'POST':
                if files:
                    response = requests.post(url, headers=headers, files=files)
                else:
                    response = requests.post(url, headers=headers, data=body)

            # Return response details in the HTML response
            return render_template_string(HTML_TEMPLATE, 
                                           response=response.text,
                                           status_code=response.status_code, 
                                           url=url, 
                                           method=method,
                                           headers=headers, 
                                           body=body,
                                           header_count=header_count)
        except Exception as e:
            return render_template_string(HTML_TEMPLATE, 
                                           error=str(e), 
                                           header_count=header_count)
    
    return render_template_string(HTML_TEMPLATE, response=None, header_count=1)

HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>API Tester</title>
    <style>
        /* General Reset */
        * {
            margin: 1;
            padding: 0;
            box-sizing: border-box;
        }

        /* Body */
        body {
            font-family: 'Arial', sans-serif;
            background-color: #2d2d2d; /* Dark background color */
            color: #fff;
            padding: 20px;
        }

        /* Container */
        .container {
            width: 80%;
            margin: auto;
            background-color: #333;
            border-radius: 8px;
            padding: 20px;
            box-shadow: 0 2px 10px rgba(0, 0, 0, 0.2);
        }

        /* Header */
        h2 {
            color: #ff6f00; /* Postman orange */
            font-size: 26px;
            margin-bottom: 20px;
        }

        /* Form Controls */
        .form-control {
            margin-bottom: 20px; /* Add space between form controls */
        }

        /* Label Style */
        label {
            display: block;
            font-size: 14px;
            margin-bottom: 8px; /* Space between label and input */
        }

        /* Input Fields */
        input[type="text"], textarea, select, input[type="file"] {
            background-color: #444;
            border: 1px solid #666;
            color: #fff;
            padding: 10px;
            font-size: 14px;
            width: 100%;
            margin-bottom: 10px;
            border-radius: 4px;
        }

        input[type="text"]:focus, textarea:focus, select:focus, input[type="file"]:focus {
            outline: none;
            border-color: #ff6f00;
        }

        /* Buttons */
        button {
            background-color: #ff6f00;
            color: #fff;
            padding: 12px 20px;
            font-size: 16px;
            border: none;
            border-radius: 4px;
            cursor: pointer;
            width: 100%;
        }

        button:hover {
            background-color: #e65c00;
        }

        /* Response Section */
        .response-container {
            margin-top: 30px;
            padding: 15px;
            background-color: #1e1e1e;
            border-radius: 8px;
        }

        .response-container h3 {
            font-size: 20px;
            margin-bottom: 10px;
            color: #ff6f00;
        }

        .response-container pre {
            background-color: #333;
            padding: 15px;
            border-radius: 5px;
            color: #fff;
            font-size: 14px;
            overflow-x: auto;
        }

        /* Error Message */
        .error {
            color: #ff3d00;
            font-size: 14px;
            margin-top: 20px;
        }

        /* Table Style for Headers */
        table {
            width: 100%;
            margin-top: 20px;
            border-collapse: collapse;
        }

        table, th, td {
            border: 1px solid #666;
        }

        th, td {
            padding: 12px;
            text-align: left;
        }

        th {
            background-color: #444;
            color: #fff;
        }

        tr:nth-child(even) {
            background-color: #555;
        }

        tr:hover {
            background-color: #666;
        }

        /* Container for header input fields */
        .header-inputs {
            display: flex;
            gap: 10px; /* Adds space between the fields */
        }

        /* Style for each input field */
        .header-inputs input {
            flex: 1; /* Ensures each input takes equal width */
        }
    </style>
</head>
<body>

<div class="container">

    <a href="/" style="text-decoration: none; color: #ff6f00;">
            <h2 style="text-align: center;">API Tester</h2>
    </a>

    <form method="POST" enctype="multipart/form-data">
        <div class="form-control">
            <label for="url">API URL:</label>
            <input type="text" id="url" name="url" required class="form-control" value="{{ request.form.get('url') }}">
        </div>

        <div class="form-control">
            <label for="method">Request Method:</label>
            <select name="method" id="method" required class="form-control">
                <option value="GET" {% if request.form.get('method') == 'GET' %}selected{% endif %}>GET</option>
                <option value="POST" {% if request.form.get('method') == 'POST' %}selected{% endif %}>POST</option>
            </select>
        </div>

        <div id="headers">
            <h4>Headers:</h4>
            {% for i in range(header_count) %}
            <div class="form-control">
                <div class="header-inputs">
                    <input type="text" name="header_key_{{ i }}" placeholder="Header Key" class="form-control" value="{{ request.form.get('header_key_' + i|string) }}">
                    <input type="text" name="header_value_{{ i }}" placeholder="Header Value" class="form-control" value="{{ request.form.get('header_value_' + i|string) }}">
                </div>
            </div>
            {% endfor %}
        </div>

        <div class="form-control">
            <label for="body">Request Body (for POST only):</label>
            <textarea name="body" id="body" class="form-control">{{ request.form.get('body') }}</textarea>
        </div>

        <div class="form-control">
            <label for="file">File (for POST only):</label>
            <input type="file" name="file" class="form-control">
        </div>

        <div class="form-control">
            <button type="submit">Send Request</button>
        </div>
    </form>

    {% if response %}
    <div class="response-container">
        <h3>Response:</h3>
        <p><strong>Status Code:</strong> {{ status_code }}</p>
        <p><strong>Response Body:</strong></p>
        <pre>{{ response }}</pre>
    </div>
    {% endif %}

    {% if error %}
    <div class="error">{{ error }}</div>
    {% endif %}
</div>

</body>
</html>
"""

if __name__ == '__main__':
    app.run(debug=True)
