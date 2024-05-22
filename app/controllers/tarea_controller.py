from flask import Blueprint, request, jsonify
from views.tarea_view import render_tak_list, render_tak_detail
from models.tarea_model import Tarea
from utils.decorators import jwt_required
from utils.decorators import role_required

tak_bp = Blueprint("tak", __name__)

@tak_bp.route("/taks", methods=["GET"])
@jwt_required
#@role_required("admin")
def taks():
    taks = Tarea.query.all()
    return jsonify(render_tak_list(taks))

@tak_bp.route("/taks/<int:id>", methods=["GET"])
@jwt_required
#@role_required("admin")
def get_tak(id):
    tak = Tarea.get_by_id(id)
    if tak:
        return jsonify(render_tak_detail(tak))
    return jsonify({"error":"tarea no encontrado"}), 404


@tak_bp.route("/taks", methods=["POST"])
@jwt_required
#@role_required("admin")
def create_tak():
    data = request.json
    title = data.get("title")
    description = data.get("description")
    status = data.get("status")
    created_at = data.get("created_at")
    assigned_to = data.get("assigned_to")

    if not title or not description or not status or not created_at or not assigned_to:
        return jsonify({"error":"faltan datos"}), 400
    
    tak = Tarea(title=title, description=description, status=status, created_at=created_at, assigned_to=assigned_to)
    tak.save()
    return jsonify(render_tak_detail(tak)), 201

@tak_bp.route("/taks/<int:id>", methods=["PUT"])
@jwt_required
#@role_required("admin")
def update_tak(id):
    tak = Tarea.get_by_id(id)

    if not tak:
        return jsonify({"error":"tarea no encontrada"}), 404
    
    data = request.json
    title = data.get("title")
    description = data.get("description")
    status = data.get("status")
    created_at = data.get("created_at")
    assigned_to = data.get("assigned_to")

    tak.update(title=title, description=description, status=status, created_at=created_at, assigned_to=assigned_to)
    return jsonify(render_tak_detail(tak)), 200

@tak_bp.route("/taks/<int:id>", methods=["DELETE"])
@jwt_required
#@role_required("admin")
def delete_tak(id):
    tak = Tarea.get_by_id(id)
    if not tak:
        return jsonify({"error":"tarea no encontrada"}), 404
    tak.delete()
    return jsonify({"message":"tarea eliminada"}), 200