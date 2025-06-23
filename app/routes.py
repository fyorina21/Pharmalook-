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

# @routes_bp.route("/pdashboard")
# def pharmadashboard():
#         name = request.form.get("Medicinename")
#         price = request.form.get("price")
#         dosage = request.form.get("Dosage")
#         description = request.form.get("medicinedescription")

#         if not name or not price or not dosage or not description:
#             flash("All fields are required", "error")
#             return redirect(url_for("routes_bp.pharmadashboard"))  # or adjust if needed

#         try:
#             new_medicine = Medicine(
#                 Medicinename=name,
#                 price=float(price),
#                 Dosage=dosage,
#                 medicinedescription=description
#             )
#             db.session.add(new_medicine)
#             db.session.commit()
#             flash("✅ Medicine added successfully!", "success")
#         except Exception as e:
#             db.session.rollback()
#             flash(f"❌ Error adding medicine: {e}", "error")


#         # return redirect(url_for("routes_bp.pharmadashboard"))
#         return render_template('pdashboard.html')


@routes_bp.route('/medicine')
def medicine():
    return render_template('medicine.html')



@routes_bp.route("/search<query>")
def search():
    result=""
    return render_template("search.html",result=result)