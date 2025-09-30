from flask import Flask, jsonify, render_template, request, session, redirect, url_for
from pymongo import MongoClient
from werkzeug.security import generate_password_hash, check_password_hash
from bson.objectid import ObjectId
import json
from datetime import datetime
from collections import defaultdict, Counter

app = Flask(__name__)
app.secret_key = 'your_secret_key'

client = MongoClient("mongodb+srv://gbogdanchirila:B5n7gCYxHoSqNt7p@carrentapp.bj7mk.mongodb.net/?retryWrites=true&w=majority")

db = client["CarRentApp"]
cars_collection = db["cars"]
rentals_collection = db["rentals"]
users_collection = db["users"]
messages_collection = db["messages"]
reviews_collection = db["reviews"]

def load_cars():
    if cars_collection.count_documents({}) == 0:
        with open('cars.json') as f:
            cars = json.load(f)
            for car in cars:
                car['image_url'] = f"static/images/{car['make'].lower()}_{car['model'].lower()}.jpg"
            cars_collection.insert_many(cars)

@app.route('/cars', methods=['GET'])
def get_cars():
    cars = list(cars_collection.find({}, {"_id": 0}))
    return jsonify(cars)

@app.route('/admin/dashboard')
def dashboard_admin():
    total_cars = cars_collection.count_documents({})
    total_users = users_collection.count_documents({})
    total_rentals = rentals_collection.count_documents({})

    rentals = list(rentals_collection.find({}))

    rentals_by_month = defaultdict(int)
    for r in rentals:
        if 'created_at' in r and isinstance(r['created_at'], datetime):
            label = r['created_at'].strftime("%Y-%m")
            rentals_by_month[label] += 1
    sorted_months = sorted(rentals_by_month)
    rental_months = [m for m in sorted_months]
    rental_counts = [rentals_by_month[m] for m in sorted_months]

    brand_counter = Counter()
    for r in rentals:
        car_id = r.get("car_id", "")
        brand = car_id.split()[0] if car_id else "Necunoscut"
        brand_counter[brand] += 1
    brand_labels = list(brand_counter.keys())
    brand_counts = list(brand_counter.values())

    model_counter = Counter()
    for r in rentals:
        model = r.get("car_id", "")
        if model:
            model_counter[model] += 1
    top_5 = model_counter.most_common(5)
    top_models = [x[0] for x in top_5]
    top_model_counts = [x[1] for x in top_5]

    return render_template('dashboard_admin.html',
                           total_cars=total_cars,
                           total_users=total_users,
                           total_rentals=total_rentals,
                           rental_months=rental_months,
                           rental_counts=rental_counts,
                           brand_labels=brand_labels,
                           brand_counts=brand_counts,
                           top_models=top_models,
                           top_model_counts=top_model_counts)

@app.route('/admin/cars')
def admin_cars():
    cars = list(cars_collection.find())
    return render_template('manage_cars.html', cars=cars)

@app.route('/admin/add', methods=['GET', 'POST'])
def add_car():
    if request.method == 'POST':
        car = {
            "make": request.form['make'],
            "model": request.form['model'],
            "year": int(request.form['year']),
            "price_per_day": float(request.form['price_per_day']),
            "seats": int(request.form['seats']),
            "engine": request.form['engine'],
            "horse_power": int(request.form['horse_power']),
            "stock": int(request.form['stock']),
            "image_url": f"/static/images/{request.form['make'].lower()}_{request.form['model'].lower()}.jpg"
        }
        cars_collection.insert_one(car)
        return redirect(url_for('admin_cars'))
    return render_template('add_car.html')

@app.route('/admin/edit/<car_id>', methods=['GET', 'POST'])
def edit_car(car_id):
    car = cars_collection.find_one({"_id": ObjectId(car_id)})
    if request.method == 'POST':
        updated_car = {
            "make": request.form['make'],
            "model": request.form['model'],
            "year": int(request.form['year']),
            "price_per_day": float(request.form['price_per_day']),
            "seats": int(request.form['seats']),
            "engine": request.form['engine'],
            "horse_power": int(request.form['horse_power']),
            "stock": int(request.form['stock']),
            "image_url": f"/static/images/{request.form['make'].lower()}_{request.form['model'].lower()}.jpg"
        }
        cars_collection.update_one({"_id": ObjectId(car_id)}, {"$set": updated_car})
        return redirect(url_for('admin_cars'))
    return render_template('edit_car.html', car=car)

@app.route('/admin/delete/<car_id>')
def delete_car(car_id):
    cars_collection.delete_one({"_id": ObjectId(car_id)})
    return redirect(url_for('admin_cars'))

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        data = request.form
        email = data.get('email')
        password = data.get('password')
        name = data.get('name')

        if users_collection.find_one({'email': email}):
            return render_template('register.html', error="Email deja folosit.")
        
        hashed_password = generate_password_hash(password)
        user = {'name': name, 'email': email, 'password': hashed_password}
        users_collection.insert_one(user)
        return redirect(url_for('login'))

    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        data = request.form
        email = data.get('email')
        password = data.get('password')

        user = users_collection.find_one({'email': email})
        if not user or not check_password_hash(user['password'], password):
            return render_template('login.html', error="Email sau parolă incorectă.")

        session['user_id'] = str(user['_id'])
        session['user_name'] = user['name']
        session['user_email'] = user['email']  

        return redirect(url_for('my_account'))

    return render_template('login.html')

@app.route('/logout', methods=['GET'])
def logout():
    session.clear()
    return redirect(url_for('index'))

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        if request.is_json:
            data = request.get_json()
        else:
            data = request.form

        name = data.get('name')
        car_id = data.get('car_id')
        start_date = data.get('start_date')
        end_date = data.get('end_date')
        payment_method = data.get('payment_method')

        rental = {
            'name': name,
            'car_id': car_id,
            'start_date': start_date,
            'end_date': end_date,
            'payment_method': payment_method,
            'created_at': datetime.now()
        }

        make_model = car_id.split(" ", 1)
        if len(make_model) != 2:
            return jsonify({'error': 'Format invalid pentru car_id'}), 
        make, model = make_model

        result = cars_collection.find_one_and_update(
            {"make": make, "model": model, "stock": {"$gt": 0}},
            {"$inc": {"stock": -1}}
        )

        if not result:
            return jsonify({'error': 'Mașina nu este disponibilă'}), 

        rentals_collection.insert_one(rental)
        return jsonify({'message': 'Închiriere efectuată cu succes!'})

    cars = list(cars_collection.find({"stock": {"$gt": 0}}, {"_id": 0}))
    rentals = list(rentals_collection.find({'name': session.get('user_name')}, {"_id": 0}))
    return render_template('index.html', cars=cars, rentals=rentals)

@app.route('/rentals', methods=['GET', 'POST'])
def rentals():
    if 'user_id' not in session:
        return redirect(url_for('login'))

    rentals = []
    success_message = None

    if request.method == 'POST':
        name = request.form.get('name')
        rentals_data = list(rentals_collection.find({'name': name}, {"_id": 0}))

        for r in rentals_data:
            car = cars_collection.find_one(
                {"make": {"$regex": r["car_id"].split()[0], "$options": "i"},
                 "model": {"$regex": r["car_id"].split()[1], "$options": "i"}},
                {"image_url": 1, "_id": 0}
            )
            r["image_url"] = car.get("image_url") if car else "/static/images/default.jpg"
        rentals = rentals_data

    return render_template('rentals.html', rentals=rentals, success=success_message)

@app.route('/my_account', methods=['GET'])
def my_account():
    if 'user_id' not in session:
        return redirect(url_for('login'))

    user_name = session.get('user_name')
    user_rentals = list(rentals_collection.find({'name': user_name}, {"_id": 0}))

    for rental in user_rentals:
        car = cars_collection.find_one(
            {"make": {"$regex": rental["car_id"].split()[0], "$options": "i"},
             "model": {"$regex": rental["car_id"].split()[1], "$options": "i"}},
            {"image_url": 1, "_id": 0}
        )
        rental["image_url"] = car.get("image_url") if car else "/static/images/default.jpg"

    return render_template(
        'my_account.html',
        user_name=user_name,
        user_email=session.get('user_email'),
        rentals=user_rentals
    )

@app.route('/plata', methods=['GET', 'POST'])
def plata():
    if request.method == 'POST':
        nume = request.form.get("nume")
        card = request.form.get("card")
        expirare = request.form.get("expirare")
        cvc = request.form.get("cvc")

        if not all([nume, card, expirare, cvc]):
            return render_template("plata.html", error="Completează toate câmpurile!")

        return render_template("plata_succes.html", nume=nume)

    return render_template("plata.html")

@app.route('/termeni', methods=['GET'])
def termeni():
    return render_template('termeni.html')

@app.route('/contact', methods=['GET', 'POST'])
def contact():
    if request.method == 'POST':
        nume = request.form.get('nume')
        email = request.form.get('email')
        mesaj = request.form.get('mesaj')

        mesaj_document = {
            "nume": nume,
            "email": email,
            "mesaj": mesaj,
            "data": datetime.now()
        }

        messages_collection.insert_one(mesaj_document)

        return render_template('contact.html', success=True)

    return render_template('contact.html', success=False)

@app.route('/recenzii', methods=['GET', 'POST'])
def recenzii():
    if request.method == 'POST':
        nume = request.form.get('nume')
        rating = int(request.form.get('rating'))
        comentariu = request.form.get('comentariu')

        if nume and comentariu and (1 <= rating <= 5):
            reviews_collection.insert_one({
                "nume": nume,
                "rating": rating,
                "comentariu": comentariu,
                "data": datetime.now()
            })

    rating_filter = request.args.get('filter')
    if rating_filter and rating_filter.isdigit():
        recenzii = list(reviews_collection.find({"rating": int(rating_filter)}).sort("data", -1))
    else:
        recenzii = list(reviews_collection.find().sort("data", -1))

    total = reviews_collection.count_documents({})
    medie = reviews_collection.aggregate([{"$group": {"_id": None, "avg": {"$avg": "$rating"}}}])
    medie_val = round(list(medie)[0]["avg"], 1) if total > 0 else 0

    return render_template('recenzii.html', recenzii=recenzii, total=total, medie=medie_val)

@app.route('/rental_form', methods=['GET', 'POST'])
def rental_form():
    car_make = request.args.get('car_make')
    car_model = request.args.get('car_model')

    if request.method == 'POST':
        rental_data = {
            'name': request.form.get('name'),
            'car_id': f"{car_make} {car_model}",
            'start_date': request.form.get('start_date'),
            'end_date': request.form.get('end_date'),
            'payment_method': request.form.get('payment_method'),
        }
        rentals_collection.insert_one(rental_data)
        return redirect(url_for('rentals', success="Închiriere efectuată cu succes"))

    return render_template('rental_form.html', car_make=car_make, car_model=car_model)

if __name__ == '__main__':
    load_cars()
    app.run(debug=True)
