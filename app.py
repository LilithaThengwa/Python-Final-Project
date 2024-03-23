from flask import Flask, jsonify, render_template, request

home_cards = [
    {
       "Title": "Car Insurance",
       "image": "https://previews.123rf.com/images/enginakyurt/enginakyurt1810/enginakyurt181000239/110640624-toy-cars-close-up-background.jpg",
       "alt": "placeholder image",
       "short_desc": "Lorem ipsum dolor sit amet consectetur adipisicing elit.\nRepudiandae quaerat nobis dignissimos corrupti.\nVoluptatibus deleniti, quisquam est ex possimus nam magni voluptas, eveniet excepturi cupiditate sint cumque vel qui alias.",
       "link": "\car",
    },
    {
       "Title": "Legal Insurance",
       "image": "https://previews.123rf.com/images/captainvector/captainvector1703/captainvector170312356/74877203-scales-of-justice.jpg",
       "alt": "placeholder image",
       "short_desc": "Lorem ipsum dolor sit amet consectetur adipisicing elit.\nRepudiandae quaerat nobis dignissimos corrupti.\nVoluptatibus deleniti, quisquam est ex possimus nam magni voluptas, eveniet excepturi cupiditate sint cumque vel qui alias.",
       "link": "\legal",
    },
    {
       "Title": "Health Insurance",
       "image": "https://previews.123rf.com/images/captainvector/captainvector1703/captainvector170312356/74877203-scales-of-justice.jpg",
       "alt": "placeholder image",
       "short_desc": "Lorem ipsum dolor sit amet consectetur adipisicing elit.\nRepudiandae quaerat nobis dignissimos corrupti.\nVoluptatibus deleniti, quisquam est ex possimus nam magni voluptas, eveniet excepturi cupiditate sint cumque vel qui alias.",
       "link": "\health",
    },
    {
       "Title": "Niche Insurance",
       "image": "https://previews.123rf.com/images/enginakyurt/enginakyurt1810/enginakyurt181000239/110640624-toy-cars-close-up-background.jpg",
       "alt": "placeholder image",
       "short_desc": "Lorem ipsum dolor sit amet consectetur adipisicing elit.\nRepudiandae quaerat nobis dignissimos corrupti.\nVoluptatibus deleniti, quisquam est ex possimus nam magni voluptas, eveniet excepturi cupiditate sint cumque vel qui alias.",
       "link": r"\niche",
    },
    {
       "Title": "High Value Insurance",
       "image": "https://previews.123rf.com/images/captainvector/captainvector1703/captainvector170312356/74877203-scales-of-justice.jpg",
       "alt": "placeholder image",
       "short_desc": "Lorem ipsum dolor sit amet consectetur adipisicing elit.\nRepudiandae quaerat nobis dignissimos corrupti.\nVoluptatibus deleniti, quisquam est ex possimus nam magni voluptas, eveniet excepturi cupiditate sint cumque vel qui alias.",
       "link": "\highvalue",
    },     
]
app = Flask(__name__)

@app.route("/")
def home():
    return render_template("home.html", cards=home_cards)

@app.route("/contact")
def conntact():
    return render_template("contact.html")

@app.route("/about")
def about():
    return render_template("about.html")

@app.route("/login")
def login():
    return render_template("login.html")

@app.route("/signup")
def signup():
    return render_template("signup.html")

@app.route("/car")
def car():
    return render_template("car.html")

@app.route("/legal")
def legal():
    return render_template("legal.html")

@app.route("/niche")
def niche():
    return render_template("niche.html")

@app.route("/health")
def health():
    return render_template("health.html")

@app.route("/highvalue")
def high_value():
    return render_template("high_value.html")

if __name__ == "__main__":
    app.run(debug = True)