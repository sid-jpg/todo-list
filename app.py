from flask import Flask, render_template, request, redirect, url_for
import sqlite3

app = Flask(__name__)


# Database setup
def setup_database():
    conn = sqlite3.connect('tracker.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS tasks (
            id INTEGER PRIMARY KEY,
            task TEXT NOT NULL,
            completed BOOLEAN NOT NULL CHECK (completed IN (0, 1))
        )
    ''')
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS expenses (
            id INTEGER PRIMARY KEY,
            amount REAL NOT NULL,
            category TEXT NOT NULL,
            description TEXT
        )
    ''')
    conn.commit()
    conn.close()


# Routes
@app.route('/')
def index():
    conn = sqlite3.connect('tracker.db')
    cursor = conn.cursor()
    cursor.execute('SELECT id, task FROM tasks WHERE completed = 0')
    tasks = cursor.fetchall()

    cursor.execute('SELECT id, amount, category, description FROM expenses')
    expenses = cursor.fetchall()

    # Calculate total expenses
    total_expenses = sum(expense[1] for expense in expenses) if expenses else 0.0

    conn.close()
    return render_template('index.html', tasks=tasks, expenses=expenses, total_expenses=total_expenses)


@app.route('/add_task', methods=['POST'])
def add_task():
    task = request.form['task']
    if task:
        conn = sqlite3.connect('tracker.db')
        cursor = conn.cursor()
        cursor.execute('INSERT INTO tasks (task, completed) VALUES (?, ?)', (task, 0))
        conn.commit()
        conn.close()
    return redirect(url_for('index'))


@app.route('/delete_task/<int:task_id>')
def delete_task(task_id):
    conn = sqlite3.connect('tracker.db')
    cursor = conn.cursor()
    cursor.execute('DELETE FROM tasks WHERE id = ?', (task_id,))
    conn.commit()
    conn.close()
    return redirect(url_for('index'))


@app.route('/add_expense', methods=['POST'])
def add_expense():
    amount = request.form['amount']
    category = request.form['category']
    description = request.form['description']
    if amount and category and description:
        conn = sqlite3.connect('tracker.db')
        cursor = conn.cursor()
        cursor.execute('INSERT INTO expenses (amount, category, description) VALUES (?, ?, ?)',
                       (amount, category, description))
        conn.commit()
        conn.close()
    return redirect(url_for('index'))


@app.route('/delete_expense/<int:expense_id>')
def delete_expense(expense_id):
    conn = sqlite3.connect('tracker.db')
    cursor = conn.cursor()
    cursor.execute('DELETE FROM expenses WHERE id = ?', (expense_id,))
    conn.commit()
    conn.close()
    return redirect(url_for('index'))


if __name__ == '__main__':
    setup_database()
    app.run(debug=True)