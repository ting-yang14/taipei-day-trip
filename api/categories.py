from flask import Blueprint, make_response
from .models.categories import Categories

categories = Blueprint("categories", __name__)
model_categories = Categories()       
headers={"Content-Type": "application/json"}

@categories.route("/categories", methods = ["GET"])
def get():
    try:
        category_list = model_categories.get_categories()
        response = make_response({"data": category_list}, 200, headers)
        return response
    except Exception as e:
        print(e)
        response = make_response({"error": True, "message": "伺服器內部錯誤"}, 500, headers)
        return response
