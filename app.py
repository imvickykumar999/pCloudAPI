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

        # Optional: Sort the lists alphabetically (case-insensitive)
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
                    * {
                        margin: 0;
                        padding: 0;
                        box-sizing: border-box;
                    }

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
                        color: #333;
                        text-align: center;
                    }

                    .breadcrumb {
                        margin-bottom: 20px;
                        font-size: 0.9rem;
                        text-align: center;
                    }

                    .breadcrumb a {
                        color: #007BFF;
                        text-decoration: none;
                    }

                    .breadcrumb a:hover {
                        text-decoration: underline;
                    }

                    .file-list {
                        list-style: none;
                        padding: 0;
                    }

                    .file-list li {
                        display: flex;
                        justify-content: space-between;
                        align-items: center;
                        padding: 10px 15px;
                        border-bottom: 1px solid #ddd;
                    }

                    .file-list li:last-child {
                        border-bottom: none;
                    }

                    .file-name {
                        font-size: 1rem;
                        color: #555;
                    }

                    .folder-name {
                        color: blue; /* Sets folder names to blue */
                        font-weight: bold; /* Optional: Makes folder names bold */
                    }

                    .view-button {
                        text-decoration: none;
                        padding: 8px 15px;
                        border: 1px solid #007BFF;
                        background-color: #007BFF;
                        color: #ffffff;
                        border-radius: 5px;
                        font-size: 0.9rem;
                        font-weight: bold;
                        transition: all 0.3s ease;
                    }

                    .view-button:hover {
                        background-color: #0056b3;
                        border-color: #0056b3;
                        cursor: pointer;
                    }
                </style>
            </head>
            <body>
                <div class="container">
                    <h1>{{ title }}</h1>
                    <div class="breadcrumb">
                        {% if current_path %}
                            <a href="{{ url_for('list_files') }}">Home</a>
                            {% set path_parts = current_path.split('/') %}
                            {% for i in range(path_parts|length) %}
                                &gt;
                                <a href="{{ url_for('list_folder_contents', foldername='/'.join(path_parts[:i+1])) }}">{{ path_parts[i] }}</a>
                            {% endfor %}
                        {% else %}
                            <a href="{{ url_for('list_files') }}">Home</a>
                        {% endif %}
                    </div>
                    {% if files_and_dirs %}
                        <ul class="file-list">
                            {% for entry in files_and_dirs %}
                                <li>
                                    <span class="file-name {% if entry.endswith('/') %}folder-name{% endif %}">{{ entry }}</span>
                                    {% if entry.endswith('/') %}
                                        <a href="/folder/{{ current_path + '/' if current_path else '' }}{{ entry[:-1] }}" class="view-button">View</a>
                                    {% else %}
                                        <a href="/file/{{ current_path + '/' if current_path else '' }}{{ entry }}" class="view-button">View</a>
                                    {% endif %}
                                </li>
                            {% endfor %}
                        </ul>
                    {% else %}
                        <p>No files or folders found in this directory.</p>
                    {% endif %}
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
        # Secure the file path
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
        # Secure the folder path
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

        # Optional: Sort the lists alphabetically (case-insensitive)
        directories.sort(key=lambda x: x.lower())
        files.sort(key=lambda x: x.lower())

        # Combine directories and files, with directories first
        files_and_dirs = directories + files

        # Calculate the relative current path for breadcrumb and URL generation
        current_path = foldername  # Relative path

        return render_template_string(
            """<!doctype html>
            <html>
            <head>
                <title>{{ title }}</title>
                <style>
                    * {
                        margin: 0;
                        padding: 0;
                        box-sizing: border-box;
                    }

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
                        color: #333;
                        text-align: center;
                    }

                    .breadcrumb {
                        margin-bottom: 20px;
                        font-size: 0.9rem;
                        text-align: center;
                    }

                    .breadcrumb a {
                        color: #007BFF;
                        text-decoration: none;
                    }

                    .breadcrumb a:hover {
                        text-decoration: underline;
                    }

                    .file-list {
                        list-style: none;
                        padding: 0;
                    }

                    .file-list li {
                        display: flex;
                        justify-content: space-between;
                        align-items: center;
                        padding: 10px 15px;
                        border-bottom: 1px solid #ddd;
                    }

                    .file-list li:last-child {
                        border-bottom: none;
                    }

                    .file-name {
                        font-size: 1rem;
                        color: #555;
                    }

                    .folder-name {
                        color: blue; /* Sets folder names to blue */
                        font-weight: bold; /* Optional: Makes folder names bold */
                    }

                    .view-button {
                        text-decoration: none;
                        padding: 8px 15px;
                        border: 1px solid #007BFF;
                        background-color: #007BFF;
                        color: #ffffff;
                        border-radius: 5px;
                        font-size: 0.9rem;
                        font-weight: bold;
                        transition: all 0.3s ease;
                    }

                    .view-button:hover {
                        background-color: #0056b3;
                        border-color: #0056b3;
                        cursor: pointer;
                    }
                </style>
            </head>
            <body>
                <div class="container">
                    <h1>{{ title }}</h1>
                    <div class="breadcrumb">
                        {% if current_path %}
                            <a href="{{ url_for('list_files') }}">Home</a>
                            {% set path_parts = current_path.split('/') %}
                            {% for i in range(path_parts|length) %}
                                &gt;
                                <a href="{{ url_for('list_folder_contents', foldername='/'.join(path_parts[:i+1])) }}">{{ path_parts[i] }}</a>
                            {% endfor %}
                        {% else %}
                            <a href="{{ url_for('list_files') }}">Home</a>
                        {% endif %}
                    </div>
                    {% if files_and_dirs %}
                        <ul class="file-list">
                            {% for entry in files_and_dirs %}
                                <li>
                                    <span class="file-name {% if entry.endswith('/') %}folder-name{% endif %}">{{ entry }}</span>
                                    {% if entry.endswith('/') %}
                                        <a href="/folder/{{ current_path + '/' if current_path else '' }}{{ entry[:-1] }}" class="view-button">View</a>
                                    {% else %}
                                        <a href="/file/{{ current_path + '/' if current_path else '' }}{{ entry }}" class="view-button">View</a>
                                    {% endif %}
                                </li>
                            {% endfor %}
                        </ul>
                    {% else %}
                        <p>No files or folders found in this directory.</p>
                    {% endif %}
                </div>
            </body>
            </html>""",
            title=f"Files in {foldername}",
            files_and_dirs=files_and_dirs,
            current_path=current_path  # Relative path
        )
    except Exception as e:
        return f"An error occurred: {e}"


if __name__ == '__main__':
    app.run(host="0.0.0.0", debug=True)
