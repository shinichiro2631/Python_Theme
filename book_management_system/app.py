from flask import Flask, render_template, request, session, redirect, url_for
import db, string, random

app = Flask(__name__)
app.secret_key = ''.join(random.choices(string.ascii_letters, k=256))

@app.route('/', methods=['GET'])
def index():
    return render_template('login.html')

@app.route('/login')
def user_login_index():
    msg = request.args.get('msg')
    if msg == None:
        return render_template('login.html')
    else:
        return render_template('login.html', msg=msg)
    
@app.route('/login', methods=['POST'])
def login():
    mail = request.form.get('mail')
    password = request.form.get('password')
    if db.login(mail, password):
        session['user'] = True
        return redirect(url_for('mypage'))
    else:
        error = '名前またはパスワードが違います。'
        input_data = {'mail':mail, 'password':password}
        return render_template('login.html', error=error, data=input_data)

@app.route('/mypage')
def mypage():
    if session['user']:
        return render_template('mypage.html')
    else:
        redirect(url_for('index'))
    return render_template('mypage.html')

@app.route('/register')
def register_form():
    return render_template('register_user.html')

@app.route('/register_exe', methods=['POST'])
def register_exe():
    user_name = request.form.get('username')
    mail = request.form.get('mail')
    password = request.form.get('password')
    
    count = db.insert_user(user_name, mail, password)
    
    if count == 1:
        msg = '登録が完了しました。'
        return render_template('index.html', msg=msg)
    else:
        error = '登録に失敗しました。'
        return render_template('register_user.html', error=error)

@app.route('/list_book', methods=['GET'])
def list_book():
    list_book = db.register_list()
    if 'user' in session:
        return render_template('list_book.html', list_book=list_book)
    else:
        redirect(url_for('index'))
        
@app.route('/register_book_form', methods=['GET'])
def register_book_form():
    if 'user' in session:
        return render_template('register_book.html', list_book=list_book)
    else:
        redirect(url_for('index'))
        

@app.route('/register_exe2', methods=['POST'])
def register_exe2():
    # book_id = request.form.get('book_id')
    book_name = request.form.get('book_name')
    book_author = request.form.get('book_author')
    ISBN = request.form.get('ISBN')
    
    count = db.insert_book(book_name, book_author, ISBN)
    
    if count == 1 and 'user' in session:
        return render_template('mypage.html')
    elif 'user' in session:
        return render_template('register_book.html')
    else:
        redirect(url_for('index'))


if __name__ == '__main__':
    app.run(debug=True)