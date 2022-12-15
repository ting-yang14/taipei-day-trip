from flask import *
from api.category import category
from api.attraction import attraction
from api.user import user
from api.booking import booking

app = Flask(__name__, static_url_path = '/', static_folder = 'static')
app.config["JSON_AS_ASCII"] = False
app.config["TEMPLATES_AUTO_RELOAD"] = True
app.register_blueprint(category, url_prefix="/api")
app.register_blueprint(attraction, url_prefix="/api")
app.register_blueprint(user, url_prefix="/api")
app.register_blueprint(booking, url_prefix="/api")

@app.route("/")
def index():
	return render_template("index.html")
@app.route("/attraction/<id>")
def attraction(id):
	return render_template("attraction.html")
@app.route("/booking")
def booking():
	return render_template("booking.html")
@app.route("/thankyou")
def thankyou():
	return render_template("thankyou.html")

if __name__ == '__main__':
	app.run(host = '0.0.0.0', port = 3000, debug = True)