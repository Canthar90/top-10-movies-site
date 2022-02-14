from flask import Flask, render_template, redirect, url_for, request
from flask_bootstrap import Bootstrap
from flask_sqlalchemy import SQLAlchemy

import requests
import os


from forms import ModyfyForm, AddMovie

API_KEY = os.getenv('API_KEY')
MOVIE_SEARCH_URL = "https://api.themoviedb.org/3/search/movie"
POSTER_URL = "https://image.tmdb.org/t/p/original"
adding_bufor = []

app = Flask(__name__)
app.config['SECRET_KEY'] = '8BYkEfBA6O6donzWlSihBXox7C0sKR6b'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///movie-data.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
Bootstrap(app)
db = SQLAlchemy(app)

class MoviesDatabase(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), unique=True, nullable=False)
    year = db.Column(db.Integer, unique=False, nullable=False)
    description = db.Column(db.String(250), unique=False, nullable=False)
    rating = db.Column(db.Integer, unique=False, nullable=False)
    ranking = db.Column(db.Integer, unique=False, nullable=True)
    review = db.Column(db.String(500), unique=False, nullable=False)
    img_url = db.Column(db.String(500), unique=True, nullable=False)

    def __init__(self, title, year, description, rating, ranking, review, img_url):
        self.title = title
        self.year = year
        self.description = description
        self.rating = rating
        self.ranking = ranking
        self.review = review
        self.img_url = img_url

    def __repr__(self):
        return '<MoviesDatabase %r>' % self.username



db.create_all()

@app.route("/")
def home():
    movies = db.session.query(MoviesDatabase).all()
    '''this element gets alll records sort them by rating and then add for every movie nev ranking number '''
    all_movies = MoviesDatabase.query.order_by(MoviesDatabase.rating).all()
    for movie in all_movies:
        movie.ranking = all_movies.index(movie)+1
    db.session.commit()

    return render_template("index.html", movies=all_movies)


@app.route('/update<int:id>', methods=['GET', 'POST'])
def update(id):
    '''This element updates the database elements froem Flask WTForms'''
    form = ModyfyForm()
    movie = MoviesDatabase.query.filter_by(id=id).first()

    if form.validate_on_submit():
        edited = MoviesDatabase.query.get(id)
        edited.rating = float(form.rating.data)
        edited.review = form.review.data
        db.session.commit()
        return home()
    else:
        return render_template("edit.html", form=form, movie=movie)


@app.route('/delete<int:id>')
def delete(id):
    """This element deletes selected item"""
    to_be_deleted = MoviesDatabase.query.get(id)
    db.session.delete(to_be_deleted)
    db.session.commit()
    return redirect(url_for('home'))


@app.route('/add_movie', methods=['GET', 'POST'])
def add_movie():
    '''This function take Movie Name passes it to another function with use API to get data'''
    form = AddMovie()
    if form.validate_on_submit():
        movie_title = form.movie_title.data
        print(movie_title)
        return redirect(url_for('select', title=movie_title))
        # select(movie_title)
    else:
        return render_template('add.html', form=form)


@app.route('/select<title>')
def select(title):
    '''Geting data From API giving ready data to work on to the next function
    In Html you are choosing onley one list element with one movie '''
    global adding_bufor
    partameters={
        "api_key": API_KEY,
        "query": title
    }
    movies = requests.get(MOVIE_SEARCH_URL, params=partameters)
    redy_data = movies.json()["results"]
    adding_bufor = redy_data
    print("select ok")
    return render_template('select.html', data=redy_data)


@app.route('/selected<int:nr>')
def selected(nr):
    '''Taking data from choosen record and adding them to database and returning to update function'''
    data_to_add = MoviesDatabase(title=adding_bufor[nr]['original_title'],
                                 year=adding_bufor[nr]['release_date'],
                                 description=adding_bufor[nr]['overview'],
                                 rating=float(adding_bufor[nr]['vote_average']),
                                 ranking=0,
                                 review='',
                                 img_url=(POSTER_URL + adding_bufor[nr]['poster_path']))
    db.session.add(data_to_add)
    db.session.commit()
    movie = MoviesDatabase.query.filter_by(title=adding_bufor[nr]['original_title']).first()
    id = movie.id
    print(id)

    # db.session.commit()
    return redirect(url_for('update', id=id))
        # update(id)




if __name__ == '__main__':
    app.run(debug=True)
