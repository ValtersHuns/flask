from flask import Flask, json, jsonify, render_template, url_for, request, redirect

import chats


app = Flask('app')

ENV = 'prod'

if ENV == 'dev':
    app.debug = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgres://postgres:valtersh26@localhost/posts'
else:
    app.debug = False
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgres://qxjnzonbylcpsu:5345f4eaa942791f5b2b718eef3414b1b58177637e3b52c1b205b5ed876c0c0d@ec2-54-195-247-108.eu-west-1.compute.amazonaws.com:5432/d5qem9lmnv7j9b'

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

class BlogPost(db.Model):
    __tablename__ = 'posts'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    content = db.Column(db.Text, nullable=False)
    author = db.Column(db.String(20), nullable=False, default='N/A')
    date_posted = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    def __repr__(self):
        return 'Blog post ' + str(self.id)



@app.route('/posts', methods=['GET', 'POST'])
def posts():

    if request.method == 'POST':
        post_title = request.form['title']
        post_content = request.form['content']
        post_author = request.form['author']
        new_post = BlogPost(title=post_title, content=post_content, author=post_author)
        db.session.add(new_post)
        db.session.commit()
        return redirect('/posts')
    else:
        all_posts = BlogPost.query.order_by(BlogPost.date_posted).all()
        return render_template('posts.html', posts=all_posts)

@app.route('/posts/delete/<int:id>')
def delete(id):
    post = BlogPost.query.get_or_404(id)
    db.session.delete(post)
    db.session.commit()
    return redirect('/posts')

@app.route('/posts/edit/<int:id>', methods=['GET', 'POST'])
def edit(id):
    
    post = BlogPost.query.get_or_404(id)

    if request.method == 'POST':
        post.title = request.form['title']
        post.author = request.form['author']
        post.content = request.form['content']
        db.session.commit()
        return redirect('/posts')
    else:
        return render_template('edit.html', post=post)

@app.route('/posts/new', methods=['GET', 'POST'])
def new_post():
    if request.method == 'POST':
        post.title = request.form['title']
        post.author = request.form['author']
        post.content = request.form['content']
        new_post = BlogPost(title=post_title, content=post_content, author=post_author)
        db.session.add(new_post)
        db.session.commit()
        return redirect('/posts')
    else:
        return render_template('new_post.html')


@app.route('/')
def home():
  return render_template('home.html')

@app.route('/lapa')
def lapa():
  return render_template('lapa.html')

@app.route('/results')
def results():
  return render_template('results.html')


@app.route('/about')
def contact():
  return render_template('contact.html')


@app.route('/chats')
def index_lapa():
  return render_template('chats.html')


@app.route('/health')
def health_check():
  return "OK"


@app.route('/chats/lasi')
def ielasit_chatu():
  return chats.lasi()


@app.route('/chats/suuti', methods=['POST'])
def suutiit_zinju():
  dati = request.json
  
  chats.pieraksti_zinju(dati)

  return chats.lasi()
  
  

if __name__ == "__main__":
    app.run(threaded=True, port=5000)