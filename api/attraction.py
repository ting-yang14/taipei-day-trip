from flask import Blueprint, request, make_response
from .models.attraction import Attraction

attraction = Blueprint("attraction", __name__)
model_attraction = Attraction()
headers = {"Content-Type": "application/json"}

@attraction.route("/attractions", methods = ["GET"])
def get_attractions():
    page = request.args.get('page')
    keyword = request.args.get('keyword')
    try:
        attractions = model_attraction.get_attractions(keyword, page)
        response = make_response(attractions, 200, headers)
        return response
    except Exception as e:
        print(e)
        response = make_response({"error": True, "message": "伺服器內部錯誤"}, 500, headers)
        return response
    
@attraction.route("/attraction/<int:attractionId>", methods = ["GET"])
def get_attraction(attractionId):
    try:
        attraction = model_attraction.get_attraction(attractionId)
        if attraction:
            response = make_response({"data": attraction}, 200, headers)
        else:
            response = make_response({"error": True, "message": "景點編號不正確"}, 400, headers)
        return response   
    except Exception as e:
        print(e)
        response = make_response({"error": True, "message": "伺服器內部錯誤"}, 500, headers)
        return response
    
