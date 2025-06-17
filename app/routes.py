from flask import Blueprint,render_template, request
from .database import Pharmacist, db
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

@routes_bp.route("/search<query>")
def search():
    result=""
    return render_template("search.html",result=result)

@routes_bp.route('/accRej')
def accept_reject():
    return render_template("accRej.html")



@routes_bp.route('/who_are_you')
def who_are_you():
    return render_template("who_are_you.html")


@routes_bp.route('/admin-dashboard')
def pharmacies():
    # Query all pharmacists where is_accepted is True
    pharmacist = Pharmacist.query.filter_by(admin_approved=True).all()
    
    return render_template("admin-dashboard.html", pharmacist=pharmacist)



