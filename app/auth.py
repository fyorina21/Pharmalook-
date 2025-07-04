from flask import Blueprint,render_template,flash,request,redirect,session,url_for
from .database import Users,db,Pharmacist, Medicine

auth_bp = Blueprint("auth_bp", __name__)
from .database import Pharmacist

routes_bp = Blueprint("routes_bp", __name__)

@auth_bp.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form.get("email")
        password = request.form.get("password")

        ADMIN_EMAIL = "admin@example.com"
        ADMIN_PASSWORD = "admin123"

        # Check if login is for admin
        if email == ADMIN_EMAIL and password == ADMIN_PASSWORD:
            session['id'] = 0  # Optional: distinguish admin with ID 0
            session['username'] = "Admin"
            session['is_admin'] = True

            print("Admin logged in successfully")
            return redirect(url_for("routes_bp.admin_dashboard"))


        user = Users.query.filter_by(email=email).first()
        if user and user.check_password(password):
            session['id'] = user.id
            session['username'] = user.name
            session['role'] = 'user'
            print("User logged in successfully")
            return redirect(url_for("routes_bp.search"))


        pharmacist = Pharmacist.query.filter_by(email=email).first()
        if pharmacist and pharmacist.check_password(password):
                
            if pharmacist.status == 'rejected':
                flash("Your pharmacy registration has been rejected. Please contact admin for details.")
                return redirect(url_for("auth_bp.login"))
        
            elif pharmacist.status == 'pending':
                flash("Your pharmacy registration is still pending approval. Please wait.")
                return redirect(url_for("routes_bp.status"))

            elif pharmacist.admin_approved:
                if pharmacist.status == 'pending':
                    pharmacist.status = 'accepted'
                    db.session.commit()

                session['id'] = pharmacist.id
                session['username'] = pharmacist.name
                session['role'] = 'pharmacist'
                print("Pharmacist logged in successfully")
                return redirect(url_for("routes_bp.pdashboard")) 
            
        flash("Invalid email or password. Please try again.")
        return redirect(url_for("auth_bp.login"))
               
    return render_template("login.html")



# @auth_bp.route("/psignup", methods=["GET", "POST"])
# def psignup():
#     if request.method == "POST":
#         name = request.form.get("name")
#         location = request.form.get("location")
#         email = request.form.get("email")
#         password = request.form.get("password")

#         user = Pharmacist.query.filter_by(email=email).first()
#         if user:
#             print("User exists with this email. Try logging in.", "error")
#             return redirect(url_for("auth_bp.psignup"))

#         pharmacist = Pharmacist(name=name,location=location, email=email)
#         pharmacist.set_password(password)
#         db.session.add(pharmacist)
#         db.session.commit()


#         if user:
#             session['id'] = user.id
#             session['username'] = user.name
#             flash("Registered successfully", "success")
#             # maybe redirect or return success
            
#         else:
#             flash("User not found. Please check your email or sign up.")
#             return redirect(url_for("auth_bp.psignup"))  # or wherever your signup route is

#         return redirect(url_for("routes_bp.search"))
#     print("error")
#     return render_template("psignup.html")


@auth_bp.route("/signup", methods=["GET", "POST"])
def signup():
    if request.method == "POST":
        name = request.form.get("name")
        lastname = request.form.get("lastname")
        email = request.form.get("email")
        password = request.form.get("password")

        user = Users.query.filter_by(email=email).first()
        if user:
            print("User exists with this email. Try logging in.", "error")
            return redirect(url_for("auth_bp.signup"))

        new_user = Users(name=name,lastname=lastname, email=email)
        new_user.set_password(password)
        db.session.add(new_user)
        db.session.commit()


        if user:
            session['id'] = user.id
            session['username'] = user.name
            flash("Registered successfully", "success")
            return redirect(url_for('pdashboard'))
            # maybe redirect or return success
            
        else:
            flash("User not found. Please check your email or sign up.")
            return redirect(url_for("auth_bp.signup"))  # or wherever your signup route is

        return redirect(url_for("routes_bp.search"))
    print("error")
    return render_template("signup.html")


@auth_bp.route("/psignup", methods=["GET", "POST"])
def psignup():
    if request.method == "POST":
        name = request.form.get("name")
        location = request.form.get("location")
        email = request.form.get("email")
        password = request.form.get("password")

<<<<<<< HEAD
        pharmacist = Pharmacist.query.filter_by(email=email).first()
        if pharmacist:
            print("Pharmacist already exists with this email.", "error")
            return redirect(url_for("auth_bp.psignup"))

        new_pharmacist = Pharmacist(name=name, location=location, email=email)
        new_pharmacist.set_password(password)
        db.session.add(new_pharmacist)
        db.session.commit()

        flash("Signed up successfully, pending admin approval.", "success")
        return redirect(url_for("routes_bp.home"))
=======
        # Check if the email already exists
        user = Pharmacist.query.filter_by(email=email).first()
        if user:
            print("Pharmacist already registered with this email. Please log in.", "error")
            return redirect(url_for("auth_bp.psignup"))

        # Create a new pharmacist user
        new_user = Pharmacist(name=name, location=location, email=email)
        new_user.set_password(password)
        db.session.add(new_user)
        db.session.commit()

        session['id'] = new_user.id
        session['username'] = new_user.name

        flash("Pharmacist registered successfully", "success")
        return redirect(url_for("auth_bp.login"))
>>>>>>> 2e5175dec2eb79e5986c0a13e896e20eaec6473f

    return render_template("psignup.html")


@auth_bp.route("/admin/pending", methods=["GET"])
def view_pending():
    pending_list = Pharmacist.query.filter_by(status='pending').all()
    return render_template("admin_pending.html", pharmacists=pending_list)

<<<<<<< HEAD
@auth_bp.route("/admin/accept/<int:id>", methods=["POST"])
def accept_pharmacist(id):
    pharmacist = Pharmacist.query.get(id)
    if pharmacist:
        pharmacist.status = 'accepted'
        db.session.commit()
    return redirect(url_for("auth_bp.view_pending"))

@auth_bp.route("/admin/reject/<int:id>", methods=["POST"])
def reject_pharmacist(id):
    pharmacist = Pharmacist.query.get(id)
    if pharmacist:
        db.session.delete(pharmacist)
        db.session.commit()
    return redirect(url_for("auth_bp.view_pending"))


@routes_bp.route("/pharmacist/<int:pharmacist_id>")
def pharmacist_home(pharmacist_id):
    pharmacist = Pharmacist.query.get(pharmacist_id)
    if pharmacist and pharmacist.status == "accepted":
        return render_template("pharmacist_home.html", pharmacist=pharmacist)
    return redirect(url_for("auth_bp.login"))  # fallback


@auth_bp.route("/pharmacist/login", methods=["GET", "POST"])
def pharmacist_login():
    if request.method == "POST":
        email = request.form.get("email")
        password = request.form.get("password")

        pharmacist = Pharmacist.query.filter_by(email=email).first()

        if not pharmacist or not pharmacist.check_password(password):
            return render_template("pharmacist_login.html", error="Invalid credentials")

        if pharmacist.status != "accepted":
            return render_template("pharmacist_login.html", error="Pending approval")

        session['pharmacist_id'] = pharmacist.id
        return redirect(url_for("routes_bp.pharmacist_home", pharmacist_id=pharmacist.id))

    return render_template("pharmacist_login.html")


@auth_bp.route("/auth/logout")
=======
@auth_bp.route("/logout")
>>>>>>> 2e5175dec2eb79e5986c0a13e896e20eaec6473f
def logout():
    session.clear()
    return redirect(url_for('routes_bp.home')) 


# @auth_bp.route("/add-medicine", methods=["POST"])
# def add_medicine():
#     name = request.form.get("Medicinename")
#     price = request.form.get("price")
#     dosage = request.form.get("Dosage")
#     description = request.form.get("medicinedescription")

#     if not name or not price or not dosage or not description:
#         flash("All fields are required", "error")
#         return redirect(url_for("routes_bp.pdashboard"))

#     try:
#         new_med = Medicine(
#             Medicinename=name,
#             price=float(price),
#             Dosage=dosage,
#             medicinedescription=description
#         )
#         db.session.add(new_med)
#         db.session.commit()
#         flash("Medicine added successfully", "success")
#     except Exception as e:
#         db.session.rollback()
#         flash(f"Error: {str(e)}", "error")

#     return redirect(url_for("routes_bp.pdashboard"))


@auth_bp.route("/add-medicine", methods=["POST"])
def add_medicine():
    name = request.form.get("Medicinename")
    price = request.form.get("price")
    dosage = request.form.get("Dosage")
    description = request.form.get("medicinedescription")

    # Check for required fields
    if not name or not price or not dosage or not description:
        flash("All fields are required.", "error")
        return redirect(url_for("routes_bp.pdashboard"))

    # Check if the medicine already exists
    existing = Medicine.query.filter_by(Medicinename=name).first()
    if existing:
        flash("This medicine already exists. You cannot add it again.", "error")
        return redirect(url_for("routes_bp.pdashboard"))

    # Add new medicine
    try:
        new_medicine = Medicine(
            Medicinename=name,
            price=float(price),
            Dosage=dosage,
            medicinedescription=description
        )
        db.session.add(new_medicine)
        db.session.commit()
        flash("Medicine added successfully!", "success")
    except Exception as e:
        db.session.rollback()
        flash(f"Error while adding medicine: {e}", "error")

    return redirect(url_for("routes_bp.pdashboard"))



@auth_bp.route("/remove-medicine", methods=["POST"])
def remove_medicine():
    name = request.form.get("medicine_name")
    if not name:
        flash("Please enter a medicine name.", "error")
        return redirect(url_for("routes_bp.pdashboard"))

    med = Medicine.query.filter_by(Medicinename=name).first()
    if not med:
        flash("Medicine not found.", "error")
        
    else:
        db.session.delete(med)
        db.session.commit()
        flash("Medicine removed successfully.", "success")

    return redirect(url_for("routes_bp.pdashboard"))



