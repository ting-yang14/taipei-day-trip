from flask import *
from api_function import get_categories, get_attraction, get_attractions
app = Flask(__name__)
app.config["JSON_AS_ASCII"] = False
app.config["TEMPLATES_AUTO_RELOAD"] = True

# Pages
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

# api
@app.route("/api/attractions", methods = ["GET"])
def api_attractions():
	page = request.args.get('page')
	keyword = request.args.get('keyword')
	result = get_attractions(page, keyword)
	if "data" in result:
		return jsonify(result), 200
	return jsonify(result), 500
	
@app.route("/api/attraction/<int:attractionId>", methods = ["GET"])
def api_attraction(attractionId):
	result = get_attraction(attractionId)
	if "data" in result:
		return jsonify(result), 200
	elif result["message"] == "attractionID not found":
		return jsonify(result), 400
	return jsonify(result), 500
		
@app.route("/api/categories", methods = ["GET"])
def api_categories():
	result = get_categories()
	if "data" in result:
		return jsonify(result), 200
	return jsonify(result), 500

if __name__ == '__main__':
	app.run(port = 3000)