from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_mail import Message, Mail


app = Flask(__name__)
app.config['SECRET_KEY'] = 'mysecretkey'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///blog.db'
db = SQLAlchemy(app)
login_manager = LoginManager(app)


# configuration of mail
app.config['MAIL_SERVER']='smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USERNAME'] = 'gadimaliyev.y@gmail.com'

# use the app password created 
app.config['MAIL_PASSWORD'] = 'qfxrmmfzvdezrbmc'
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USE_SSL'] = False

# instantiating the mail service only after the 'app.config' to avoid error   
mail = Mail(app)


from blog import routes
