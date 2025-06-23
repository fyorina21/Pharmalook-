from flask import Blueprint,render_template,flash,request,redirect,session,url_for
from .database import Users,db
auth_bp = Blueprint("auth_bp", __name__)
from .database import Pharmacist

routes_bp = Blueprint("routes_bp", __name__)

@auth_bp.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form.get("email")
        password = request.form.get("password")

        user = Users.query.filter_by(email=email).first()

        if not user:
            print("No account found with this email")
            return render_template("login.html", error="Invalid email or password")

        if not user.check_password(password):
            print("Invalid password")
            return render_template("login.html", error="Invalid email or password")

        session['id'] = user.id
        session['username'] = user.name

        print("Logged in successfully")
        return redirect(url_for("routes_bp.home"))

    return render_template("login.html")



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


        session['id'] = user.id
        session['username'] = user.name
        flash("Registered successfully", "success")
        return redirect(url_for("routes_bp.home"))
    print("error")
    return render_template("signup.html")



@auth_bp.route("/psignup", methods=["GET", "POST"])
def psignup():
    if request.method == "POST":
        name = request.form.get("name")
        location = request.form.get("location")
        email = request.form.get("email")
        password = request.form.get("password")

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

    return render_template("psignup.html")


@auth_bp.route("/admin/pending", methods=["GET"])
def view_pending():
    pending_list = Pharmacist.query.filter_by(status='pending').all()
    return render_template("admin_pending.html", pharmacists=pending_list)

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
def logout():
    session.clear()
    return redirect(url_for('routes_bp.home')) 