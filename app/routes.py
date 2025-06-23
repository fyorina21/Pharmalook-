from flask import Blueprint,render_template, request
from .database import Pharmacist
routes_bp = Blueprint("routes_bp", __name__)


@routes_bp.route('/profile')
def profile():
    return render_template('pprofile.html')

@routes_bp.route("/")
def home():
    return render_template('index.html')


@routes_bp.route('/medicine')
def medicine():
    return render_template('medicine.html')

# @routes_bp.route('/phamacist',methods=["GET","POST"])
# def medicine():
#     if request.method == "POST":
#         name = request.form.get("name")
#         price = request.form.get("price")
#         dosage = request.form.get("dosage")
#         description = request.form.get("description")

#         new_me
#     return render_template('medicine.html')

@routes_bp.route("/who")
def who():
    return render_template("who_are_you.html")

@routes_bp.route("/admin/pending", methods=["GET"])

def view_pending():
    pharmacists = Pharmacist.query.filter_by(status='pending').all()
    return render_template("accRej.html", pharmacists=pharmacists)



@routes_bp.route("/search<query>")
def search():
    result=""
    return render_template("search.html",result=result)