from flask import render_template, request, Blueprint, url_for
from flaskblog.models import Post
from flaskblog.posts.routes import view_blog

main = Blueprint('main', __name__)



@main.route("/")
@main.route("/home")
def home():
    page = request.args.get('page', 1, type=int)
    posts = Post.query.order_by(Post.date_posted.desc()).paginate(page=page, per_page=6)
    vector1 = url_for('static', filename='profile_pics/vector1.jpg')
    vector2 = url_for('static', filename='profile_pics/vector2.png')
    vector3 = url_for('static', filename='profile_pics/vector3.png')
    return render_template('home.html', posts = posts, vector1=vector1, vector2=vector2, vector3=vector3)



@main.route("/about")
def about():
    profle_pic = url_for('static', filename='profile_pics/Profile.jpg')
    return render_template('about.html', title='About', profle_pic=profle_pic)


@main.route("/search", methods=('GET', 'POST'))
def search():
    if request.method == 'POST':
        search = request.form['search']
        search_data = Post.query.filter_by(title=search).first_or_404()
        
        return render_template('view_blog.html', post=search_data)
