from flask import Blueprint,render_template,flash,request,redirect,session,url_for
from .database import Users,db
from app.database import Medicine

auth_bp = Blueprint("auth_bp", __name__)

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

@auth_bp.route("/auth/logout")
def logout():
    session.clear()
    return redirect(url_for('routes_bp.home')) 



@auth_bp.route("/add-medicine", methods=["POST"])
def add_medicine():
    if request.method == "POST":
        name = request.form.get("Medicinename")
        price = request.form.get("price")
        dosage = request.form.get("Dosage")
        description = request.form.get("medicinedescription")

        if not name or not price or not dosage or not description:
            flash("All fields are required", "error")
            return redirect(url_for("routes_bp.home"))  # adjust as needed

        try:
            new_medicine = Medicine(
                Medicinename=name,
                price=float(price),
                Dosage=dosage,
                medicinedescription=description
            )
            db.session.add(new_medicine)
            db.session.commit()
            flash("Medicine added successfully", "success")
        except Exception as e:
            db.session.rollback()
            flash(f"Error: {e}", "error")

        return redirect(url_for("pdahboard.home"))  # or wherever you want to go