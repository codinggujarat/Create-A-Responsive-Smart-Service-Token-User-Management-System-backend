from flask import Blueprint, request, jsonify
from backend.models import db, User, CompletedWork
from backend.utils.email_service import send_confirmation_email
from flask import current_app
import traceback

user_bp = Blueprint('user', __name__)

@user_bp.route('/api/submit', methods=['POST'])
def submit_user():
    try:
        data = request.json
        
        # Check if data exists
        if not data:
            return jsonify({'error': 'No data provided'}), 400
            
        name = data.get('name')
        email = data.get('email')
        address = data.get('address')
        contact_number = data.get('contact_number')
        work_description = data.get('work_description')
        
        if not all([name, email, address, contact_number, work_description]):
            return jsonify({'error': 'All fields are required'}), 400
        
        last_user = User.query.order_by(User.token_number.desc()).first()
        new_token_number = (last_user.token_number + 1) if last_user else 1
        
        new_user = User(
            token_number=new_token_number,
            name=name,
            email=email,
            address=address,
            contact_number=contact_number,
            work_description=work_description,
            status='Pending'
        )
        
        db.session.add(new_user)
        db.session.commit()
        
        # Try to send confirmation email, but don't fail the request if it doesn't work
        user_data = {
            'token_number': new_token_number,
            'name': name,
            'email': email,
            'contact_number': contact_number,
            'address': address,
            'work_description': work_description
        }
        
        mail = current_app.extensions.get('mail')
        if mail:
            current_app.logger.info("Mail extension is available, attempting to send confirmation email")
            email_sent = send_confirmation_email(mail, user_data)
            if email_sent:
                current_app.logger.info(f"Confirmation email sent successfully to {email}")
            else:
                current_app.logger.warning(f"Failed to send confirmation email to {email}")
        else:
            current_app.logger.warning("Mail extension not available, skipping email confirmation")
            current_app.logger.info("Check if MAIL_USERNAME and MAIL_PASSWORD are set in environment variables")
        
        return jsonify({
            'success': True,
            'message': 'User registered successfully',
            'token_number': new_token_number,
            'user': new_user.to_dict()
        }), 201
        
    except Exception as e:
        db.session.rollback()
        current_app.logger.error(f"Error submitting user: {str(e)}")
        current_app.logger.error(f"Traceback: {traceback.format_exc()}")
        return jsonify({'error': 'Failed to submit user data. Please try again.'}), 500

@user_bp.route('/api/next-token', methods=['GET'])
def get_next_token():
    try:
        last_user = User.query.order_by(User.token_number.desc()).first()
        next_token = (last_user.token_number + 1) if last_user else 1
        return jsonify({'next_token': next_token}), 200
    except Exception as e:
        current_app.logger.error(f"Error getting next token: {str(e)}")
        current_app.logger.error(f"Traceback: {traceback.format_exc()}")
        return jsonify({'error': 'Failed to get next token'}), 500