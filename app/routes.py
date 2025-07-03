from flask import Blueprint,render_template, request, redirect, url_for, flash, session
from .database import Pharmacist, db, Medicine
from sqlalchemy import delete


routes_bp = Blueprint("routes_bp", __name__)

# @routes_bp.route('/psignup', methods=['GET', 'POST'])
# def signup():
#     if request.method == 'POST':
#         name = request.form.get('name')
#         location = request.form.get('location')
#         email = request.form.get('email')
#         password = request.form.get('password')
#         confirm = request.form.get('confirmPassword')

#         if password != confirm:
#             flash('Passwords do not match.')
#             return redirect(url_for('routes_bp.signup'))
#         if Pharmacist.query.filter_by(email=email).first():
#             flash('Email already exists.')
#             return redirect(url_for('routes_bp.psignup'))

#         pharmacist = Pharmacist(name=name, location=location, email=email)
#         pharmacist.set_password(password)
#         db.session.add(pharmacist)
#         db.session.commit()
#         return redirect(url_for('routes_bp.status_page', email=pharmacist.email))
    
#     return render_template('psignup.html')



@routes_bp.route('/profile')
def profile():
    if 'id' not in session:
        return redirect(url_for('auth_bp.login'))  # User not logged in

    pharmacies = Pharmacist.query.get(session['id'])

    if not pharmacies:
        return "Pharmacist not found", 404

    return render_template('pprofile.html', pharmacies=pharmacies)

@routes_bp.route("/")
def home():
    return render_template('index.html')

@routes_bp.route("/user", methods=["GET"])
def user_homepage():
    # Get search query from URL parameters (default to empty string if none)
    search_query = request.args.get("q", "").strip()
    results = []
    if search_query:
        # Search for medicines by name (case-insensitive)
        results = Medicine.query.filter(Medicine.Medicinename.ilike(f"%{search_query}%")).all()
    else:
        # If no search, show all medicines
        results = Medicine.query.all()
    return render_template(
        "look.html",
        medicines=results,
        query=search_query
    )


@routes_bp.route('/status')
def status_page():
    email = request.args.get('email')

    if not email:
        flash('No email provided.')
        return redirect(url_for('routes_bp.signup'))

    pharmacist = Pharmacist.query.filter_by(email=email).first()

    if not pharmacist:
        flash('Pharmacist not found.')
        return redirect(url_for('routes_bp.signup'))

    return render_template('status.html', pharmacy_name=pharmacist.name,
                           request_date=pharmacist.created_at.strftime('%Y-%m-%d'),
                           status=pharmacist.status)

@routes_bp.route('/inventory')
def inventory_page():
    medicines = Medicine.query.all()
    return render_template('inventory.html', medicines=medicines)

@routes_bp.route('/pdashboard')
def pdashboard():
    return render_template('pdashboard.html')


@routes_bp.route('/medicine')
def medicine():
    medicines = Medicine.query.all()
    return render_template('medicine.html', medicines=medicines)




@routes_bp.route('/pdashboard')
def pdashboard():
    return render_template('pdashboard.html')


# @routes_bp.route('/medicines')
# def medicine_list():
#     medicines = Medicine.query.all()
#     return render_template('medicine_list.html', medicines=medicines)



# @routes_bp.route('/phamacist',methods=["GET","POST"])
# def medicine():
#     if request.method == "POST":
#         name = request.form.get("name")
#         price = request.form.get("price")
#         dosage = request.form.get("dosage")
#         description = request.form.get("description")


<<<<<<< HEAD
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
=======

# @routes_bp.route("/search")
# def search():
#     query = request.args.get("query")  # gets ?query=value from URL
#     result = []

#     if query:
#         # Example SQLAlchemy model query
#         result = Medicine.query.filter(Medicine.name.ilike(f"%{query}%")).all()

#     return render_template("search.html", result=result)


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

@routes_bp.route('/delete/<int:pharmacy_id>', methods=['POST'])
def delete_pharmacy(pharmacy_id):
    with db.connect() as conn:
        stmt = delete(Pharmacist).where(Pharmacist.c.id == pharmacy_id)
        conn.execute(stmt)
        conn.commit()
    return redirect(url_for('pharmacies'))


@routes_bp.route('/status')
def status():
    pharmacist = Pharmacist.query.get(session['id'])
    if pharmacist:
        return render_template("status.html", pharmacist=pharmacist)
    
    else:
        flash("Pharmacist not found.")
        return redirect(url_for("auth_bp.login"))
>>>>>>> 2e5175dec2eb79e5986c0a13e896e20eaec6473f
