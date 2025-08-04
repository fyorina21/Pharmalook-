from flask import Blueprint,render_template, request, redirect, url_for, flash, session
from .database import Pharmacist, db, Medicine
from sqlalchemy import delete


routes_bp = Blueprint("routes_bp", __name__)

@routes_bp.route('/psignup', methods=['GET', 'POST'])
def psignup():
    if request.method == 'POST':
        name = request.form.get('name')
        location = request.form.get('location')
        email = request.form.get('email')
        password = request.form.get('password')
        confirm = request.form.get('confirmPassword')

        if password != confirm:
            flash('Passwords do not match.')
            return redirect(url_for('routes_bp.psignup'))

        if Pharmacist.query.filter_by(email=email).first():
            flash('Email already exists.')
            return redirect(url_for('routes_bp.psignup'))

        pharmacist = Pharmacist(name=name, location=location, email=email)
        pharmacist.set_password(password)
        pharmacist.status = 'pending'
        pharmacist.admin_approved = False

        db.session.add(pharmacist)
        db.session.commit()
        flash("Signup complete! Wait for admin approval.")
        
        return redirect(url_for('routes_bp.status', email=pharmacist.email))

    return render_template('psignup.html')



@routes_bp.route('/approve/<int:pharmacy_id>', methods=['POST'])
def approve_pharmacy(pharmacy_id):
    pharmacist = Pharmacist.query.get(pharmacy_id)
    if pharmacist:
        pharmacist.admin_approved = True
        pharmacist.status = 'approved'
        db.session.commit()
    return redirect(url_for('routes_bp.accept_reject'))

@routes_bp.route('/reject/<int:pharmacy_id>', methods=['POST'])
def reject_pharmacy(pharmacy_id):
    pharmacist = Pharmacist.query.get(pharmacy_id)
    if pharmacist:
        db.session.delete(pharmacist)
        db.session.commit()
    return redirect(url_for('routes_bp.accept_reject'))



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
        # JOIN Medicine with Pharmacist to get location and pharmacy name
        results = db.session.query(
            Medicine.Medicinename,
            Medicine.Dosage,
            Medicine.price,
            Medicine.medicinedescription,
            Pharmacist.name.label("pharmacyname"),
            Pharmacist.location
        ).join(Pharmacist, Medicine.pharmacist_id == Pharmacist.id
        ).filter(Medicine.Medicinename.ilike(f"%{search_query}%")).all()

   
    return render_template(
        "look.html",
        medicines=results,
        query=search_query
    )

@routes_bp.route("/user_search", methods=["GET", "POST"])
def user_search():
    if request.method == "POST":
        medication = request.form.get("medication")
        location = request.form.get("location")  # optional, not used now

        results = []
        if medication:
            results = db.session.query(
                Medicine.Medicinename,
                Medicine.Dosage,
                Medicine.price,
                Medicine.medicinedescription,
                Pharmacist.name.label("pharmacyname"),
                Pharmacist.location
            ).join(Pharmacist, Medicine.pharmacist_id == Pharmacist.id
            ).filter(Medicine.Medicinename.ilike(f"%{medication}%")).all()

        return render_template("look.html", medicines=results, query=medication)
    return render_template('user_search.html')


@routes_bp.route('/status', endpoint='status')
def status_page():
    email = request.args.get('email')

    if not email:
        flash('No email provided.')
        return redirect(url_for('routes_bp.psignup'))

    pharmacist = Pharmacist.query.filter_by(email=email).first()

    if not pharmacist:
        flash('Pharmacist not found.')
        return redirect(url_for('routes_bp.psignup'))

    # ✅ FIXED: Pass the whole object, not just .name
    return render_template('status.html', pharmacist=pharmacist)


@routes_bp.route('/inventory')
def inventory_page():
    medicines = Medicine.query.all()
    return render_template('inventory.html', medicines=medicines)




@routes_bp.route('/medicine')
def medicine():
    medicines = Medicine.query.all()
    return render_template('medicine.html', medicines=medicines)    







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


@routes_bp.route("/who")
def who():
    return render_template("who_are_you.html")

@routes_bp.route("/admin/pending", methods=["GET"])

def view_pending():
    pharmacists = Pharmacist.query.filter_by(status='pending').all()
    return render_template("accRej.html", pharmacists=pharmacists)



@routes_bp.route("/search")
def search():
    result=""
    return render_template("look.html",result=result)

@routes_bp.route("/pdashboard")
def pdashboard():
    return render_template("pdashboard.html")

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
    pending_pharmacists = Pharmacist.query.filter_by(admin_approved=False).all()
    print("PENDING PHARMACISTS:", pending_pharmacists)  # DEBUG print

    return render_template("accRej.html", pharmacists=pending_pharmacists)



@routes_bp.route('/who_are_you')
def who_are_you():
    return render_template("who_are_you.html")

@routes_bp.route('/admin-dashboard')
def admin_dashboard():  # <- Rename for clarity
    pharmacist = Pharmacist.query.filter_by(admin_approved=True).all()
    pending_count = Pharmacist.query.filter_by(admin_approved=False).count()
    return render_template("admin-dashboard.html", pharmacist=pharmacist, pending_count=pending_count)


@routes_bp.route('/delete/<int:pharmacy_id>', methods=['POST'])
def delete_pharmacy(pharmacy_id):
    pharmacist = Pharmacist.query.get(pharmacy_id)
    if pharmacist:
        db.session.delete(pharmacist)
        db.session.commit()
    return redirect(url_for('routes_bp.admin_dashboard'))
 



# @routes_bp.route('/status')
# def status():
#     pharmacist = Pharmacist.query.get(session['id'])
#     if pharmacist:
#         return render_template("status.html", pharmacist=pharmacist)
    
    return render_template("admin-dashboard.html", pharmacist=pharmacist)

@routes_bp.route('/pprofile')
def pprofile():
    return render_template("pprofile.html")

@routes_bp.route('/delete/<int:pharmacy_id>', methods=['POST'])
def delete_pharmacy(pharmacy_id):
    pharmacist = Pharmacist.query.get(pharmacy_id)
    if pharmacist:
        db.session.delete(pharmacist)
        db.session.commit()
    return redirect(url_for('routes_bp.admin_dashboard'))
 



# @routes_bp.route('/status')
# def status():
#     pharmacist = Pharmacist.query.get(session['id'])
#     if pharmacist:
#         return render_template("status.html", pharmacist=pharmacist)
    
#     else:
#         flash("Pharmacist not found.")
        # return redirect(url_for("auth_bp.login"))
