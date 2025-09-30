from pymongo import MongoClient
import json

client = MongoClient("mongodb+srv://gbogdanchirila:B5n7gCYxHoSqNt7p@carrentapp.bj7mk.mongodb.net/?retryWrites=true&w=majority")
db = client["CarRentApp"]
cars_collection = db["cars"]

with open('cars.json') as file:
    cars = json.load(file)
    
    for car in cars:
        car['image_url'] = f"/static/images/{car['make'].lower()}_{car['model'].lower()}.jpg"
        existing_car = cars_collection.find_one({"make": car["make"], "model": car["model"]})
        if not existing_car:
            cars_collection.insert_one(car)

print("Cars have been successfully loaded into the database.")