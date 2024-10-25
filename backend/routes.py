from . import app
import os
import json
from flask import jsonify, request, make_response, abort, url_for  # noqa; F401

SITE_ROOT = os.path.realpath(os.path.dirname(__file__))
json_url = os.path.join(SITE_ROOT, "data", "pictures.json")
data: list = json.load(open(json_url))

######################################################################
# RETURN HEALTH OF THE APP
######################################################################


@app.route("/health")
def health():
    return jsonify(dict(status="OK")), 200

######################################################################
# COUNT THE NUMBER OF PICTURES
######################################################################


@app.route("/count")
def count():
    """return length of data"""
    if data:
        return jsonify(length=len(data)), 200

    return {"message": "Internal server error"}, 500


######################################################################
# GET ALL PICTURES
######################################################################
@app.route("/picture", methods=["GET"])
def get_pictures():
    if request.method == 'GET':
        return jsonify(data), 200
    return jsonify({"error": "Invalid request"}), 400

######################################################################
# GET A PICTURE
######################################################################


@app.route("/picture/<int:id>", methods=["GET"])
def get_picture_by_id(id):
    if request.method == 'GET':
        info = next((item for item in data if item["id"] == id), None)
        if info:
            return jsonify(info),200
        return jsonify({"error": "Not found"}), 404
    return jsonify({"error": "Invalid request"}), 400


######################################################################
# CREATE A PICTURE
######################################################################
@app.route("/picture", methods=["POST"])
def create_picture():
    picture = request.json
    if not picture or "id" not in picture or "pic_url" not in picture or "event_country" not in picture or "event_state" not in picture or "event_city" not in picture or "event_date" not in picture:
        return jsonify({"error": "Missing data"}), 400
    if any(item["id"] == picture["id"] for item in data ):
        return jsonify({"Message": f"picture with id {picture['id']} already present"}), 302
    data.append(picture)
    return jsonify(picture), 201

######################################################################
# UPDATE A PICTURE
######################################################################


@app.route("/picture/<int:id>", methods=["PUT"])
def update_picture(id):
    picture = request.json
    if not picture or "id" not in picture or "pic_url" not in picture or "event_country" not in picture or "event_state" not in picture or "event_city" not in picture or "event_date" not in picture:
        return jsonify({"error": "Missing data"}), 400
    existing_picture = next((item for item in data if item["id"] == id), None)
    if existing_picture is None:
        return jsonify({"message": "Picture not found"}), 404
    
    existing_picture["pic_url"] = picture["pic_url"]
    existing_picture["event_country"] = picture["event_country"]
    existing_picture["event_state"] = picture["event_state"]
    existing_picture["event_city"] = picture["event_city"]
    existing_picture["event_date"] = picture["event_date"]
    return jsonify({"message": "Picture updated successfully", "updated_picture": existing_picture}), 200


######################################################################
# DELETE A PICTURE
######################################################################
@app.route("/picture/<int:id>", methods=["DELETE"])
def delete_picture(id):
    if request.method == "DELETE":
        delete_item = next((item for item in data if item["id"] == id), None) 
        if delete_item:
            data.remove(delete_item)
            return "", 204
        return jsonify({"message": "picture not found"}), 404
        
