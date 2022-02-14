from flask import Flask, render_template, redirect, url_for, request
from flask_bootstrap import Bootstrap
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired
import requests



class ModyfyForm(FlaskForm):
    rating = StringField('Edit raiting for example: 8', [DataRequired()])
    review = StringField('Edit your reviev', [DataRequired()])
    submit = SubmitField('Done')

class AddMovie(FlaskForm):
    movie_title = StringField('Movie Title', [DataRequired()])
    submit = SubmitField("Add Movie")