from flask import Flask,render_template, request, session,redirect,url_for
import sqlite3

app = Flask(__name__)
app.secret_key = 'havit'

def connect_db():
    conn = sqlite3.connect('database/employee.db')
    return conn

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/employee')
def employee():
    return render_template('employee/employee.html')

@app.route('/employee_form')
def employee_form():
    return render_template('employee/employee_form.html')


@app.route('/register_employees', methods=['GET', 'POST'])
def register_employees():
    if request.method == 'POST':
        username = request.form['username'] 
        email = request.form['email']
        password = request.form['password']
        
        session['username'] = username 
        
        conn = connect_db() 
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM user WHERE username=? OR email=?', (username, email))
        user = cursor.fetchone()
        
        if user:
            conn.close() 
            return render_template('auth/registel.html')
        else:
            cursor.execute('INSERT INTO user (username, email, password) VALUES (?, ?, ?)', (username, email, password))
            conn.commit() 
            conn.close() 

            return redirect(url_for('index'))
    return render_template('auth/register.html')

@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(debug=True)