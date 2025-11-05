from flask import Blueprint, request, jsonify, send_file, current_app
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from backend.models import db, User, CompletedWork
from backend.utils.export_service import export_to_excel, export_to_csv, export_to_pdf
from datetime import datetime

admin_bp = Blueprint('admin', __name__)

@admin_bp.route('/api/admin/login', methods=['POST'])
def admin_login():
    try:
        data = request.json
        username = data.get('username')
        password = data.get('password')
        
        admin_username = current_app.config.get('ADMIN_USERNAME')
        admin_password = current_app.config.get('ADMIN_PASSWORD')
        
        if username == admin_username and password == admin_password:
            access_token = create_access_token(identity=username)
            return jsonify({
                'success': True,
                'access_token': access_token,
                'username': username
            }), 200
        else:
            return jsonify({'error': 'Invalid credentials'}), 401
            
    except Exception as e:
        current_app.logger.error(f"Login error: {str(e)}")
        return jsonify({'error': 'Login failed'}), 500

@admin_bp.route('/api/admin/users', methods=['GET'])
@jwt_required()
def get_all_users():
    try:
        search = request.args.get('search', '')
        status = request.args.get('status', '')
        
        query = User.query
        
        if search:
            search_filter = f"%{search}%"
            query = query.filter(
                (User.name.like(search_filter)) |
                (User.email.like(search_filter)) |
                (User.contact_number.like(search_filter)) |
                (User.token_number == int(search) if search.isdigit() else False)
            )
        
        if status and status != 'All':
            query = query.filter(User.status == status)
        
        users = query.order_by(User.token_number.desc()).all()
        
        return jsonify({
            'success': True,
            'users': [user.to_dict() for user in users],
            'total': len(users)
        }), 200
        
    except Exception as e:
        current_app.logger.error(f"Error fetching users: {str(e)}")
        return jsonify({'error': 'Failed to fetch users'}), 500

@admin_bp.route('/api/admin/users/<int:user_id>', methods=['PUT'])
@jwt_required()
def update_user_status(user_id):
    try:
        data = request.json
        new_status = data.get('status')
        
        if new_status not in ['Pending', 'Completed']:
            return jsonify({'error': 'Invalid status'}), 400
        
        user = User.query.get(user_id)
        if not user:
            return jsonify({'error': 'User not found'}), 404
        
        old_status = user.status
        user.status = new_status
        user.updated_at = datetime.utcnow()
        
        if old_status == 'Pending' and new_status == 'Completed':
            completed_work = CompletedWork.query.first()
            if not completed_work:
                completed_work = CompletedWork(count=0)
                db.session.add(completed_work)
            completed_work.count += 1
            completed_work.last_updated = datetime.utcnow()
        
        db.session.commit()
        
        return jsonify({
            'success': True,
            'message': 'User status updated successfully',
            'user': user.to_dict()
        }), 200
        
    except Exception as e:
        db.session.rollback()
        current_app.logger.error(f"Error updating user: {str(e)}")
        return jsonify({'error': 'Failed to update user'}), 500

@admin_bp.route('/api/admin/stats', methods=['GET'])
@jwt_required()
def get_stats():
    try:
        total_users = User.query.count()
        pending = User.query.filter_by(status='Pending').count()
        completed = User.query.filter_by(status='Completed').count()
        
        completed_work = CompletedWork.query.first()
        completed_works_count = completed_work.count if completed_work else 0
        
        return jsonify({
            'success': True,
            'stats': {
                'total': total_users,
                'pending': pending,
                'completed': completed,
                'completed_works': completed_works_count
            }
        }), 200
        
    except Exception as e:
        current_app.logger.error(f"Error fetching stats: {str(e)}")
        return jsonify({'error': 'Failed to fetch stats'}), 500

@admin_bp.route('/api/admin/export/excel', methods=['GET'])
@jwt_required()
def export_excel():
    try:
        users = User.query.order_by(User.token_number).all()
        output = export_to_excel(users)
        
        return send_file(
            output,
            mimetype='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
            as_attachment=True,
            download_name=f'service_tokens_{datetime.now().strftime("%Y%m%d_%H%M%S")}.xlsx'
        )
        
    except Exception as e:
        current_app.logger.error(f"Error exporting to Excel: {str(e)}")
        return jsonify({'error': 'Failed to export to Excel'}), 500

@admin_bp.route('/api/admin/export/csv', methods=['GET'])
@jwt_required()
def export_csv():
    try:
        users = User.query.order_by(User.token_number).all()
        output = export_to_csv(users)
        
        return send_file(
            output,
            mimetype='text/csv',
            as_attachment=True,
            download_name=f'service_tokens_{datetime.now().strftime("%Y%m%d_%H%M%S")}.csv'
        )
        
    except Exception as e:
        current_app.logger.error(f"Error exporting to CSV: {str(e)}")
        return jsonify({'error': 'Failed to export to CSV'}), 500

@admin_bp.route('/api/admin/export/pdf', methods=['GET'])
@jwt_required()
def export_pdf():
    try:
        users = User.query.order_by(User.token_number).all()
        output = export_to_pdf(users)
        
        return send_file(
            output,
            mimetype='application/pdf',
            as_attachment=True,
            download_name=f'service_tokens_{datetime.now().strftime("%Y%m%d_%H%M%S")}.pdf'
        )
        
    except Exception as e:
        current_app.logger.error(f"Error exporting to PDF: {str(e)}")
        return jsonify({'error': 'Failed to export to PDF'}), 500
