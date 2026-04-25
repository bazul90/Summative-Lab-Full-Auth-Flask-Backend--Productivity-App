from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from models import db, Note

resource_bp = Blueprint('resources', __name__)

@resource_bp.route('/resources', methods=['GET'])
@jwt_required()
def get_notes():
    user_id = get_jwt_identity()

    # Pagination parameters
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 10, type=int)
    per_page = min(per_page, 100)  # Max 100 items per page

    # Filter by current user only
    pagination = Note.query.filter_by(user_id=user_id)\
        .order_by(Note.updated_at.desc())\
        .paginate(page=page, per_page=per_page, error_out=False)

    notes = [note.to_dict() for note in pagination.items]

    return jsonify({
        'notes': notes,
        'total': pagination.total,
        'page': pagination.page,
        'per_page': pagination.per_page,
        'pages': pagination.pages,
        'has_next': pagination.has_next,
        'has_prev': pagination.has_prev
    }), 200

@resource_bp.route('/resources', methods=['POST'])
@jwt_required()
def create_note():
    user_id = get_jwt_identity()
    data = request.get_json()

    if not data:
        return jsonify({'error': 'No input data provided'}), 400

    title = data.get('title', '').strip()
    content = data.get('content', '').strip()

    if not title:
        return jsonify({'error': 'Title is required'}), 400

    note = Note(
        title=title,
        content=content if content else None,
        user_id=user_id
    )

    db.session.add(note)
    db.session.commit()

    return jsonify({
        'message': 'Note created successfully',
        'note': note.to_dict()
    }), 201

@resource_bp.route('/resources/<int:note_id>', methods=['GET'])
@jwt_required()
def get_note(note_id):
    user_id = get_jwt_identity()
    note = Note.query.filter_by(id=note_id, user_id=user_id).first()

    if not note:
        return jsonify({'error': 'Note not found'}), 404

    return jsonify({'note': note.to_dict()}), 200

@resource_bp.route('/resources/<int:note_id>', methods=['PATCH'])
@jwt_required()
def update_note(note_id):
    user_id = get_jwt_identity()
    note = Note.query.filter_by(id=note_id, user_id=user_id).first()

    if not note:
        return jsonify({'error': 'Note not found'}), 404

    data = request.get_json()
    if not data:
        return jsonify({'error': 'No input data provided'}), 400

    title = data.get('title', '').strip()
    content = data.get('content', '').strip()

    if title:
        note.title = title
    if content is not None:
        note.content = content

    db.session.commit()

    return jsonify({
        'message': 'Note updated successfully',
        'note': note.to_dict()
    }), 200

@resource_bp.route('/resources/<int:note_id>', methods=['DELETE'])
@jwt_required()
def delete_note(note_id):
    user_id = get_jwt_identity()
    note = Note.query.filter_by(id=note_id, user_id=user_id).first()

    if not note:
        return jsonify({'error': 'Note not found'}), 404

    db.session.delete(note)
    db.session.commit()

    return jsonify({'message': 'Note deleted successfully'}), 200
