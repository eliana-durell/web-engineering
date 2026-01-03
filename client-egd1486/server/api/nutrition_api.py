from flask import jsonify
from flask_restful import Resource

from flask_restful import request
from flask_restful import reqparse
import json
from .swen_344_db_utils import *

class NutritionApi(Resource):
    # get ALL the data from the server
    def get(self):
    # NOTE: No need to replicate code; use the util function!
        sql = "SELECT n.item, n.calories, n.totalFat, n.saturatedFat, n.transFat, n.protein, n.carbohydrate, c.category_name \
            FROM category_items i \
            JOIN nutrition n ON n.id=i.nutrition_id \
            JOIN categories c ON c.id=i.category_id \
            ORDER BY c.id ASC;"
        result = exec_get_all(sql)
        return result

    # modify nutrition data for existing food items
    def put(self):
        parser = reqparse.RequestParser()
        parser.add_argument("calories", int)
        parser.add_argument("totalFat", int)
        parser.add_argument("saturatedFat", int)
        parser.add_argument("transFat", int)
        parser.add_argument("protein", int)
        parser.add_argument("carbohydrate", int)
        parser.add_argument("item", str)
        args = parser.parse_args()

        calories = args["calories"]
        totalFat = args["totalFat"]
        saturatedFat = args["saturatedFat"]
        transFat = args["transFat"]
        protein = args["protein"]
        carbohydrate = args["carbohydrate"]
        item = args["item"]
        
        sql = "UPDATE nutrition \
            SET "
        params = []
        addComma = False
        comma = ", "
        if calories is not None:
            sql = sql + "calories=%s"
            params.append(calories)
            addComma = True
        if totalFat is not None:
            if addComma:
                sql = sql + comma
            sql = sql + "totalFat=%s"
            params.append(totalFat)
            addComma = True
        if saturatedFat is not None:
            if addComma:
                sql = sql + comma
            sql = sql + "saturatedFat=%s"
            params.append(saturatedFat)
            addComma = True
        if transFat is not None:
            if addComma:
                sql = sql + comma
            sql = sql + "transFat=%s"
            params.append(transFat)
            addComma = True
        if protein is not None:
            if addComma:
                sql = sql + comma
            sql = sql + "protein=%s"
            params.append(protein)
            addComma = True
        if carbohydrate is not None:
            if addComma:
                sql = sql + comma
            sql = sql + "carbohydrate=%s"
            params.append(carbohydrate)
        sql = sql + " WHERE item=%s;"
        params.append(item)
        
        if not params:
            return {"message": "No fields to update", "status": 304} # Not Modified
        exec_commit(sql, params)
        
        sql = "SELECT item, calories, totalFat, saturatedFat, transFat, protein, carbohydrate \
            FROM nutrition \
            WHERE item=%s;"
        result = exec_get_one(sql, (item, ))
        return jsonify({ #do else it will do "0": result[0]
            "item": result[0],
            "calories": result[1],
            "totalFat": result[2],
            "saturatedFat": result[3],
            "transFat": result[4],
            "protein": result[5],
            "carbohydrate": result[6]
        }) # client expecting JSON object in .then(json => ) call
            
        
    # create new food items in an existing category
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument("item", str)
        parser.add_argument("calories", int)
        parser.add_argument("totalFat", int)
        parser.add_argument("saturatedFat", int)
        parser.add_argument("transFat", int)
        parser.add_argument("protein", int)
        parser.add_argument("carbohydrate", int)
        parser.add_argument("category", str)
        args = parser.parse_args()

        item = args["item"]
        calories = args["calories"]
        totalFat = args["totalFat"]
        saturatedFat = args["saturatedFat"]
        transFat = args["transFat"]
        protein = args["protein"]
        carbohydrate = args["carbohydrate"]
        category = args["category"]
        
        sql = "INSERT INTO nutrition (item, calories, totalFat, saturatedFat, transFat, protein, carbohydrate) VALUES \
            (%s, %s, %s, %s, %s, %s, %s);"
        exec_commit(sql, (item, calories, totalFat, saturatedFat, transFat, protein, carbohydrate))
        sql = "SELECT id \
            FROM nutrition \
            WHERE item=%s;"
        nutrition_id = exec_get_one(sql, (item, ))[0]
        sql = "SELECT id \
            FROM categories \
            WHERE category_name=%s;"
        category_id = exec_get_one(sql, (category, ))[0]
        sql = "INSERT INTO category_items (category_id, nutrition_id) VALUES \
            (%s, %s);"
        exec_commit(sql, (category_id, nutrition_id))
        # get updated db
        sql = "SELECT item, calories, totalFat, saturatedFat, transFat, protein, carbohydrate \
            FROM nutrition \
            WHERE item=%s;"
        result = exec_get_one(sql, (item, ))
        return jsonify({ #do else it will do "0": result[0]
            "item": result[0],
            "calories": result[1],
            "totalFat": result[2],
            "saturatedFat": result[3],
            "transFat": result[4],
            "protein": result[5],
            "carbohydrate": result[6]
        })
        
    # delete a particular food item 
    def delete(self):
        item = request.args.get("item")
        sql = "SELECT id \
            FROM nutrition \
            WHERE item=%s;"
        id = exec_get_one(sql, (item, ))
        sql = "DELETE FROM category_items \
            WHERE nutrition_id=%s;"
        exec_commit(sql, (id, ))
        sql = "DELETE FROM nutrition \
            WHERE item=%s;"
        exec_commit(sql, (item, ))
        return {}



