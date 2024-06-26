from flask import Flask, render_template, url_for
from markupsafe import escape
from forms import RegistrationForm, LoginForm

app = Flask(__name__)

app.config['SECRET_KEY'] = 'f5f3e9a5875dabc5b96c185ecec1cd374bdfcf67deecef1c9de698799fe0cabce89e19de1159f3a1a73da9f4070f9e1bcfd77c61c876102a6353d268993a8060fc743350c9efebc1e3e66373a1b4f020'

@app.route('/')
@app.route('/home')
def home():
    return render_template('home.html', title = 'Home') #mágica???
    
@app.route('/about')
def about():
    return render_template('about.html', title = 'About')
    
@app.route('/user/<username>')
def user(username):
    return f'<h1> Usuário: {escape(username)} </h1>'
   
@app.route('/register', methods = ['GET', 'POST'])
def register():
    
    form = RegistrationForm()
    
    return render_template('register.html', title = 'Registrar', form = form)

@app.route('/login')
def login():
    
    form = LoginForm()
    
    return render_template('login.html', title = 'Entrar', form = form)
    
if __name__ == '__main__':
    
    app.run(debug = True)