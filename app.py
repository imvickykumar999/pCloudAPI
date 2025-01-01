from flask import Flask, render_template_string, request, send_from_directory, url_for
import os

app = Flask(__name__)

# Folder path to list files
FOLDER_PATH = "./"  # Replace with your folder path


@app.route('/')
def list_files():
    try:
        # Get the list of files and directories in the folder
        entries = os.listdir(FOLDER_PATH)
        directories = []
        files = []
        for entry in entries:
            entry_path = os.path.join(FOLDER_PATH, entry)
            if os.path.isdir(entry_path):
                directories.append(f"{entry}/")
            else:
                files.append(entry)

        # Sort the lists alphabetically (case-insensitive)
        directories.sort(key=lambda x: x.lower())
        files.sort(key=lambda x: x.lower())

        # Combine directories and files, with directories first
        files_and_dirs = directories + files

        return render_template_string(
            """<!doctype html>
            <html>
            <head>
                <title>{{ title }}</title>
                <style>
                    body {
                        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
                        background: #f9f9f9;
                        color: #333;
                        margin: 0;
                        padding: 0;
                    }

                    .container {
                        max-width: 900px;
                        margin: 50px auto;
                        padding: 20px;
                        background: #ffffff;
                        box-shadow: 0 8px 20px rgba(0, 0, 0, 0.1);
                        border-radius: 10px;
                        text-align: left;
                    }

                    h1 {
                        font-size: 1.8rem;
                        margin-bottom: 20px;
                        text-align: center;
                    }

                    .file-list {
                        list-style: none;
                        padding: 0;
                    }

                    .file-list li {
                        display: flex;
                        justify-content: space-between;
                        padding: 10px 15px;
                        border-bottom: 1px solid #ddd;
                    }

                    .file-name {
                        font-size: 1rem;
                    }

                    .folder-name {
                        color: blue;
                        font-weight: bold;
                    }

                    .open-button {
                        text-decoration: none;
                        padding: 8px 15px;
                        border: 1px solid #28a745;
                        background-color: #28a745;
                        color: white;
                        border-radius: 5px;
                        font-size: 0.9rem;
                        transition: all 0.3s ease;
                    }

                    .open-button:hover {
                        background-color: #1e7e34;
                        border-color: #1e7e34;
                    }

                    .view-button {
                        text-decoration: none;
                        padding: 8px 15px;
                        border: 1px solid #007BFF;
                        background-color: #007BFF;
                        color: white;
                        border-radius: 5px;
                        font-size: 0.9rem;
                        transition: all 0.3s ease;
                    }

                    .view-button:hover {
                        background-color: #0056b3;
                        border-color: #0056b3;
                    }
                </style>
            </head>
            <body>
                <div class="container">
                    <h1>{{ title }}</h1>
                    <ul class="file-list">
                        {% for entry in files_and_dirs %}
                            <li>
                                <span class="file-name {% if entry.endswith('/') %}folder-name{% endif %}">{{ entry }}</span>
                                {% if entry.endswith('/') %}
                                    <a href="/folder/{{ current_path + '/' if current_path else '' }}{{ entry[:-1] }}" class="open-button">Open</a>
                                {% else %}
                                    <a href="/file/{{ current_path + '/' if current_path else '' }}{{ entry }}" class="view-button">View</a>
                                {% endif %}
                            </li>
                        {% endfor %}
                    </ul>
                </div>
            </body>
            </html>""",
            title=f"Files in {FOLDER_PATH}",
            files_and_dirs=files_and_dirs,
            current_path=""  # Root path
        )
    except Exception as e:
        return f"An error occurred: {e}"


@app.route('/file/<path:filename>')
def serve_file(filename):
    try:
        requested_file = os.path.join(FOLDER_PATH, filename)
        abs_requested_file = os.path.abspath(requested_file)
        abs_folder_path = os.path.abspath(FOLDER_PATH)

        if not abs_requested_file.startswith(abs_folder_path):
            return "Access denied", 403

        if not os.path.isfile(abs_requested_file):
            return "File not found", 404

        return send_from_directory(FOLDER_PATH, filename)
    except Exception as e:
        return f"An error occurred while opening the file: {e}"


@app.route('/folder/<path:foldername>')
def list_folder_contents(foldername):
    try:
        requested_path = os.path.join(FOLDER_PATH, foldername)
        abs_requested_path = os.path.abspath(requested_path)
        abs_folder_path = os.path.abspath(FOLDER_PATH)

        if not abs_requested_path.startswith(abs_folder_path):
            return "Access denied", 403

        if not os.path.isdir(abs_requested_path):
            return "Folder not found", 404

        entries = os.listdir(abs_requested_path)
        directories = []
        files = []
        for entry in entries:
            entry_path = os.path.join(abs_requested_path, entry)
            if os.path.isdir(entry_path):
                directories.append(f"{entry}/")
            else:
                files.append(entry)

        directories.sort(key=lambda x: x.lower())
        files.sort(key=lambda x: x.lower())

        files_and_dirs = directories + files

        current_path = foldername

        return render_template_string(
            """<!doctype html>
            <html>
            <head>
                <title>{{ title }}</title>
                <style>
                    body {
                        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
                        background: #f9f9f9;
                        color: #333;
                        margin: 0;
                        padding: 0;
                    }

                    .container {
                        max-width: 900px;
                        margin: 50px auto;
                        padding: 20px;
                        background: #ffffff;
                        box-shadow: 0 8px 20px rgba(0, 0, 0, 0.1);
                        border-radius: 10px;
                        text-align: left;
                    }

                    h1 {
                        font-size: 1.8rem;
                        margin-bottom: 20px;
                        text-align: center;
                    }

                    .file-list {
                        list-style: none;
                        padding: 0;
                    }

                    .file-list li {
                        display: flex;
                        justify-content: space-between;
                        padding: 10px 15px;
                        border-bottom: 1px solid #ddd;
                    }

                    .file-name {
                        font-size: 1rem;
                    }

                    .folder-name {
                        color: blue;
                        font-weight: bold;
                    }

                    .open-button {
                        text-decoration: none;
                        padding: 8px 15px;
                        border: 1px solid #28a745;
                        background-color: #28a745;
                        color: white;
                        border-radius: 5px;
                        font-size: 0.9rem;
                        transition: all 0.3s ease;
                    }

                    .open-button:hover {
                        background-color: #1e7e34;
                        border-color: #1e7e34;
                    }

                    .view-button {
                        text-decoration: none;
                        padding: 8px 15px;
                        border: 1px solid #007BFF;
                        background-color: #007BFF;
                        color: white;
                        border-radius: 5px;
                        font-size: 0.9rem;
                        transition: all 0.3s ease;
                    }

                    .view-button:hover {
                        background-color: #0056b3;
                        border-color: #0056b3;
                    }
                </style>
            </head>
            <body>
                <div class="container">
                    <h1>{{ title }}</h1>
                    <ul class="file-list">
                        {% for entry in files_and_dirs %}
                            <li>
                                <span class="file-name {% if entry.endswith('/') %}folder-name{% endif %}">{{ entry }}</span>
                                {% if entry.endswith('/') %}
                                    <a href="/folder/{{ current_path + '/' if current_path else '' }}{{ entry[:-1] }}" class="open-button">Open</a>
                                {% else %}
                                    <a href="/file/{{ current_path + '/' if current_path else '' }}{{ entry }}" class="view-button">View</a>
                                {% endif %}
                            </li>
                        {% endfor %}
                    </ul>
                </div>
            </body>
            </html>""",
            title=f"Files in {foldername}",
            files_and_dirs=files_and_dirs,
            current_path=current_path
        )
    except Exception as e:
        return f"An error occurred: {e}"


if __name__ == '__main__':
    app.run(host="0.0.0.0", debug=True)
