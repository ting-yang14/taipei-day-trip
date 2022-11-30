from flask import Blueprint, jsonify, request
from .api_function import *
api = Blueprint("api", __name__)

@api.route("/attractions", methods = ["GET"])
def api_attractions():
	page = request.args.get('page')
	keyword = request.args.get('keyword')
	result = get_attractions(page, keyword)
	if "data" in result:
		return jsonify(result), 200
	return jsonify(result), 500
	
@api.route("/attraction/<int:attractionId>", methods = ["GET"])
def api_attraction(attractionId):
	result = get_attraction(attractionId)
	if "data" in result:
		return jsonify(result), 200
	elif result["message"] == "attractionID not found":
		return jsonify(result), 400
	return jsonify(result), 500
		
@api.route("/categories", methods = ["GET"])
def api_categories():
	result = get_categories()
	if "data" in result:
		return jsonify(result), 200
	return jsonify(result), 500