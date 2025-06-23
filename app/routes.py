from flask import Blueprint,render_template, request,flash,redirect,url_for
from .database import Pharmacist,db,Medicine
routes_bp = Blueprint("routes_bp", __name__)


@routes_bp.route('/profile')
def profile():
    return render_template('profile.html')

@routes_bp.route("/")
def home():
    return render_template('index.html')

@routes_bp.route('/pdashboard')
def pdashboard():
    return render_template('pdashboard.html')



@routes_bp.route('/medicine')
def medicine():
    return render_template('medicine.html')



@routes_bp.route("/search<query>")
def search():
    result=""
    return render_template("search.html",result=result)