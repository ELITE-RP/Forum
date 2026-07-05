from flask import Flask, render_template, request, redirect, url_for
import datetime
import os

app = Flask(__name__)
app.secret_key = 'elite_rp_secret_key_2026'

CATEGORIES = [
    {
        "id": 1,
        "title": "Важная информация",
        "boards": [
            {"id": 101, "title": "Новости проекта", "desc": "Основные объявления и нововведения ELITE RP."},
            {"id": 102, "title": "Правила сервера", "desc": "Свод правил для игроков и администрации."}
        ]
    },
    {
        "id": 2,
        "title": "Игровой процесс",
        "boards": [
            {"id": 201, "title": "Жалобы на игроков", "desc": "Раздел для подачи жалоб на нарушения правил."},
            {"id": 202, "title": "Игровые обсуждения", "desc": "Общайтесь, делитесь скриншотами и историями."}
        ]
    }
]

THREADS = [
    {
        "id": 1,
        "board_id": 101,
        "title": "Добро пожаловать на форум ELITE RP!",
        "author": "Главный Администратор",
        "date": "05.07.2026",
        "replies_count": 1,
        "posts": [
            {"author": "Главный Администратор", "date": "05.07.2026", "text": "Приветствуем всех игроков! Рады видеть вас на обновленном форуме ELITE RP. Здесь вы можете найти актуальные новости, правила и оставить свои предложения.", "avatar": "⭐"}
        ]
    }
]

@app.route('/')
def index():
    return render_template('index.html', categories=CATEGORIES)

@app.route('/board/<int:board_id>')
def board(board_id):
    board_info = None
    for cat in CATEGORIES:
        for b in cat['boards']:
            if b['id'] == board_id:
                board_info = b
    board_threads = [t for t in THREADS if t['board_id'] == board_id]
    return render_template('board.html', board=board_info, threads=board_threads)

@app.route('/thread/<int:thread_id>', methods=['GET', 'POST'])
def thread(thread_id):
    thread_data = next((t for t in THREADS if t['id'] == thread_id), None)
    if not thread_data:
        return "Тема не найдена", 404
        
    if request.method == 'POST':
        author = request.form.get('author', 'Гость')
        text = request.form.get('text')
        if text:
            new_post = {
                "author": author,
                "date": datetime.datetime.now().strftime("%d.%m.%Y %H:%M"),
                "text": text,
                "avatar": "👤"
            }
            thread_data['posts'].append(new_post)
            thread_data['replies_count'] += 1
            return redirect(url_for('thread', thread_id=thread_id))
            
    return render_template('thread.html', thread=thread_data)

@app.route('/board/<int:board_id>/new', methods=['GET', 'POST'])
def new_thread(board_id):
    if request.method == 'POST':
        title = request.form.get('title')
        author = request.form.get('author', 'Гость')
        text = request.form.get('text')
        
        if title and text:
            new_id = len(THREADS) + 1
            new_t = {
                "id": new_id,
                "board_id": board_id,
                "title": title,
                "author": author,
                "date": datetime.datetime.now().strftime("%d.%m.%Y"),
                "replies_count": 0,
                "posts": [
                    {"author": author, "date": datetime.datetime.now().strftime("%d.%m.%Y %H:%M"), "text": text, "avatar": "👤"}
                ]
            }
            THREADS.append(new_t)
            return redirect(url_for('board', board_id=board_id))
            
    return render_template('new_thread.html', board_id=board_id)

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
