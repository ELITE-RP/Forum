import os

os.makedirs("templates", exist_ok=True)
os.makedirs("static", exist_ok=True)

with open("app.py", "w", encoding="utf-8") as f:
    f.write("from flask import Flask\napp = Flask(__name__)\n@app.route('/')\ndef index(): return 'Форум работает!'\nif __name__ == '__main__': app.run(debug=True)")

with open("requirements.txt", "w", encoding="utf-8") as f:
    f.write("Flask\nFlask-SQLAlchemy\nwerkzeug\ngunicorn")

print("Файлы созданы! Теперь просто создайте в папке templates файл index.html")