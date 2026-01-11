from . import app
import os
import json
from flask import jsonify, request, abort

# Load data
SITE_ROOT = os.path.realpath(os.path.dirname(__file__))
json_url = os.path.join(SITE_ROOT, "data", "pictures.json")
with open(json_url) as f:
    data: list = json.load(f)

# Keep a copy of the original dataset to allow reset
original_data = data.copy()

######################################################################
# HEALTH & COUNT (Exercises 1 & 2)
######################################################################
@app.route("/health")
def health():
    return jsonify({"status": "OK"}), 200

@app.route("/count")
def count():
    return jsonify(length=len(data)), 200

######################################################################
# GET ALL PICTURES (Exercise 2)
######################################################################
@app.route("/picture", methods=["GET"])
def get_pictures():
    return jsonify(data), 200

######################################################################
# GET A PICTURE BY ID (Exercise 3)
######################################################################
@app.route("/picture/<int:id>", methods=["GET"])
def get_picture_by_id(id):
    picture = next((item for item in data if item["id"] == id), None)
    if picture:
        return jsonify(picture), 200
    return {"message": "Picture not found"}, 404

######################################################################
# CREATE A PICTURE (Exercise 4)
######################################################################
@app.route("/picture", methods=["POST"])
def create_picture():
    picture_data = request.get_json()
    
    # Check for duplicate id
    for picture in data:
        if picture['id'] == picture_data['id']:
            # Requirement: Return 302 and specific Message format
            return jsonify({"Message": f"picture with id {picture['id']} already present"}), 302

    data.append(picture_data)
    return jsonify(picture_data), 201

######################################################################
# UPDATE A PICTURE (Exercise 5)
######################################################################
@app.route("/picture/<int:id>", methods=["PUT"])
def update_picture(id):
    picture_data = request.get_json()
    picture = next((item for item in data if item["id"] == id), None)

    if picture:
        # Update the dictionary in place
        picture.update(picture_data)
        return jsonify(picture), 200
    
    return {"message": "picture not found"}, 404

######################################################################
# DELETE A PICTURE (Exercise 6)
######################################################################
@app.route("/picture/<int:id>", methods=["DELETE"])
def delete_picture(id):
    global data
    picture = next((item for item in data if item["id"] == id), None)
    
    if picture:
        # Rebuild list excluding the target id
        data = [item for item in data if item["id"] != id]
        # Return empty body with 204 No Content
        return "", 204
    
    return {"message": "picture not found"}, 404

######################################################################
# RESET DATA (For Testing Consistency)
######################################################################
@app.route("/reset", methods=["POST"])
def reset_data():
    global data
    data = original_data.copy()
    return "", 200