from flask import Flask, render_template, redirect
from flask_pymongo import PyMongo
import scrape_mars

# Create an instance of Flask
app = Flask(__name__)

# Use PyMongo to establish Mongo connection
mongo = PyMongo(app, uri="mongodb://localhost:27017/mission_mars_db")

# Route to render index.html template using data from Mongo


@app.route("/")
def home():

    # Find one record of data from the mongo database
    mars_entry = mongo.db.mars.find_one()

    # Return template and data
    return render_template("index.html", findings=mars_entry)

# Route that will trigger the scrape function


@app.route("/scrape")
def scraper():

    # Run the scrape function
    mars_scraped_final = scrape_mars.scrape()

    # Update the Mongo database using update and upsert=True
    mongo.db.mars.update({}, mars_scraped_final, upsert=True)

    # Redirect back to home page
    return redirect("/")


if __name__ == "__main__":
    app.run(debug=True)
