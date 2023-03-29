from flask import Flask, render_template, flash, redirect, url_for, session, logging, request, make_response
import psycopg2
from datetime import date

app = Flask(__name__)
app.secret_key = 'secret'

# Connecting to postgresql database


def db_connection():
    """Connect to Postgresql Database"""
    conn = psycopg2.connect(host='localhost',
                            database='library',
                            user='postgres',
                            password='password'
                            )
    return conn

@app.route('/', methods=['GET', 'POST'])
def add_book():
    if request.method == 'POST':
        book_title = request.form['book_title']
        author = request.form['author']
        published_year = request.form['published_year']
        genre = request.form['genre']
        description = request.form['description']
        isbn = request.form['isbn']
        total_copies = request.form['total_copies']
        available_copies = request.form['available_copies']

        conn = db_connection()
        cur = conn.cursor()

        # Insert inputs into database to add new dish
        cur.execute('INSERT INTO books (title, author, published_year, genre, description, isbn, total_copies, available_copies)'
                    'VALUES (%s, %s, %s, %s, %s, %s, %s, %s)',
                    (book_title, author, published_year, genre, description, isbn, total_copies, available_copies)
                    )

        conn.commit()
        cur.close()
        conn.close()

    return render_template('index.html')

@app.route('/borrower', methods=['GET', 'POST'])
def borrower():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        phone = request.form['phone']
        address = request.form['address']

        conn = db_connection()
        cur = conn.cursor()

        # Insert inputs into database to add new dish
        cur.execute('INSERT INTO borrowers (name, email, phone, address)'
                        'VALUES (%s, %s, %s, %s)',
                        (name, email, phone, address)
                        )
        conn.commit()
        cur.close()
        conn.close()

    return render_template('borrower.html')

@app.route('/issue', methods=['GET', 'POST'])
def issue():
    if request.method == 'POST':
        book_id = request.form['book_id']
        borrower_id = request.form['borrower_id']
        loan_date = request.form['loan_date']
        due_date = request.form['due_date']

        conn = db_connection()
        cur = conn.cursor()

        # Insert inputs into database to add new dish
        cur.execute('INSERT INTO loans (book_id, borrower_id, loan_date, due_date)'
                        'VALUES (%s, %s, %s, %s)',
                        (book_id, borrower_id, loan_date, due_date)
                        )
        conn.commit()
        cur.close()
        conn.close()

    return render_template('issue.html')

@app.route('/return', methods=['GET', 'POST'])
def return_page():
    if request.method == 'POST':
        pass

    conn = db_connection()
    cur = conn.cursor()
    
    # cur.execute('SELECT * from loans WHERE return_date is NULL;')
    cur.execute('''SELECT books.book_id, books.title, loans.borrower_id, loans.loan_id, borrowers.name, borrowers.phone, loans.loan_date, loans.due_date FROM books JOIN loans ON books.book_id = loans.book_id JOIN borrowers ON borrowers.borrower_id = loans.borrower_id WHERE return_date is NULL;
            ''')
    loans = cur.fetchall()
    conn.commit()
    cur.close()
    conn.close()
    
    app.logger.info(loans)

    return render_template('return.html', data=[loans])

@app.route('/returned/<string:id>', methods=['POST'])
def returned(id):
    conn = db_connection()
    cur = conn.cursor()

    cur.execute('''UPDATE loans SET return_date=(%s) WHERE loan_id=(%s);''', (date.today(), id))
    
    conn.commit()
    cur.close()
    conn.close()

    return redirect(url_for('return_page'))