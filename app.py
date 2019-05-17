from flask import Flask, render_template, request, url_for, redirect
from datetime import datetime

from flask_sqlalchemy import SQLAlchemy 


app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database/blog.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS']= False

db = SQLAlchemy(app)

class BlogPost(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	titre = db.Column(db.String(255))
	sous_titre = db.Column(db.String(255))
	auteur = db.Column(db.String(20))
	data_post = db.Column(db.DateTime)
	contenu = db.Column(db.Text)
	
	

@app.route('/')
def index():
	cont = BlogPost.query.order_by(BlogPost.data_post.desc()).all()
	return render_template('index.html', contenu=cont)

@app.route('/about/')
def about():
	return render_template('about.html')


@app.route('/post/<int:post_id>/')
def post(post_id):
	post = BlogPost.query.filter_by(id=post_id).one()
	data_post = post.data_post.strftime(" %B %d, %Y ")

	return render_template('post.html', post=post, data_post=data_post)

@app.route('/add/')
def add():
	return render_template('add.html')

@app.route('/addpost/', methods=['POST'])
def addpost():
	titre = request.form['titre']
	sous_titre = request.form['sous_titre']
	auteur = request.form['auteur']
	contenu = request.form['contenu']

	post = BlogPost(titre=titre, sous_titre=sous_titre, auteur=auteur, contenu=contenu, data_post=datetime.now())

	db.session.add(post)
	db.session.commit()

	return redirect(url_for('index'))

if __name__=='__main__':
	db.create_all()
	app.run(debug=True)
