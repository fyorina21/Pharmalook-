from flask import Blueprint,render_template,flash,request,redirect,session,url_for
from .database import Users,db
auth_bp = Blueprint("auth_bp", __name__)

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
            return redirect(url_for("routes_bp.pharmacies"))


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
        return redirect(url_for("routes_bp.search"))

    return render_template("login.html")



@auth_bp.route("/psignup", methods=["GET", "POST"])
def psignup():
    if request.method == "POST":
        name = request.form.get("name")
        location = request.form.get("loaction")
        email = request.form.get("email")
        password = request.form.get("password")

        user = Users.query.filter_by(email=email).first()
        if pharmacist:
            print("User exists with this email. Try logging in.", "error")
            return redirect(url_for("auth_bp.signup"))

        pharmacist = Users(name=name,location=location, email=email)
        user.set_password(password)
        db.session.add(pharmacist)
        db.session.commit()


        if user:
            session['id'] = user.id
            session['username'] = user.name
            flash("Registered successfully", "success")
            # maybe redirect or return success
            
        else:
            flash("User not found. Please check your email or sign up.")
            return redirect(url_for("auth_bp.psignup"))  # or wherever your signup route is

        return redirect(url_for("routes_bp.search"))
    print("error")
    return render_template("psignup.html")


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
            # maybe redirect or return success
            
        else:
            flash("User not found. Please check your email or sign up.")
            return redirect(url_for("auth_bp.signup"))  # or wherever your signup route is

        return redirect(url_for("routes_bp.search"))
    print("error")
    return render_template("signup.html")


@auth_bp.route("/logout")
def logout():
    session.clear()
    return redirect(url_for('routes_bp.home')) 