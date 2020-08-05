# Importing Dependencies and Tools
from flask import Flask, render_template
import scraping 
from flask_pymongo import PyMongo 

# Setting up Flask
app = Flask(__name__) 

# Instructing Python to connect to Mongo using PyMongo
app.config["MONGO_URI"] = "mongodb://localhost:27017/mars_app" 
mongo = PyMongo(app) 

# Defining the route for the HTML page
@app.route("/") 
def index():
    mars = mongo.db.mars.find_one() 
    return render_template("index.html", mars=mars)

# Set up scraping route
@app.route("/scrape") 
def scrape():
    mars = mongo.db.mars 
    mars_data = scraping.scrape_all()
    mars.update({}, mars_data, upsert=True)
    return "Scraping Successful!"

if __name__ == "__main__":
    app.run()

