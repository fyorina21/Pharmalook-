from flask import Blueprint,render_template, request, redirect, url_for, flash
from .database import Pharmacist, db, Medicine


routes_bp = Blueprint("routes_bp", __name__)

# @routes_bp.route('/signup', methods=['GET', 'POST'])
# def signup():
#     if request.method == 'POST':
#         name = request.form.get('firstName')
#         location = request.form.get('Location')
#         email = request.form.get('email')
#         password = request.form.get('password')
#         confirm = request.form.get('confirmPassword')

#         if password != confirm:
#             flash('Passwords do not match.')
#             return redirect(url_for('routes_bp.signup'))
#         if Pharmacist.query.filter_by(email=email).first():
#             flash('Email already exists.')
#             return redirect(url_for('routes_bp.signup'))

#         pharmacist = Pharmacist(name=name, location=location, email=email)
#         pharmacist.set_password(password)
#         db.session.add(pharmacist)
#         db.session.commit()
#         return redirect(url_for('routes_bp.status_page', email=pharmacist.email))
    
#     return render_template('signup.html')



@routes_bp.route('/profile')
def profile():
    return render_template('pprofile.html')

@routes_bp.route("/")
def home():
    return render_template('index.html')

@routes_bp.route('/status')
def status_page():
    email = request.args.get('email')
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



@routes_bp.route('/medicine')
def medicine():
    return render_template('medicine.html')

@routes_bp.route('/medicines')
def medicine_list():
    medicines = Medicine.query.all()
    return render_template('medicine_list.html', medicines=medicines)

@routes_bp.route('/medicines/add', methods=['GET', 'POST'])
def add_medicine():
    if request.method == 'POST':
        medicinename = request.form.get('Medicinename')
        price = request.form.get('price')
        dosage = request.form.get('Dosage')
        description = request.form.get('medicinedescription')

        if not all([medicinename, price, dosage, description]):
            flash('All fields are required!', 'error')
        else:
            try:
                new_medicine = Medicine(
                    Medicinename=medicinename,
                    price=float(price),
                    Dosage=dosage,
                    medicinedescription=description
                )
                db.session.add(new_medicine)
                db.session.commit()
                flash('Medicine added successfully!', 'success')
                return redirect(url_for('routes_bp.medicine_list'))
            except ValueError:
                flash('Invalid price format', 'error')
            except Exception as e:
                db.session.rollback()
                flash(f'Error adding medicine: {str(e)}', 'error')

    return render_template('add_medicine.html')

# @routes_bp.route('/phamacist',methods=["GET","POST"])
# def medicine():
#     if request.method == "POST":
#         name = request.form.get("name")
#         price = request.form.get("price")
#         dosage = request.form.get("dosage")
#         description = request.form.get("description")

#         new_me
#     return render_template('medicine.html')

@routes_bp.route("/search")
def search():
    query = request.args.get("query")  # gets ?query=value from URL
    result = []

    if query:
        # Example SQLAlchemy model query
        result = Medicine.query.filter(Medicine.name.ilike(f"%{query}%")).all()

    return render_template("search.html", result=result)


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



