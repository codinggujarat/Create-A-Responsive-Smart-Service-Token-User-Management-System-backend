from flask_mail import Message
from flask import current_app
import traceback

def send_confirmation_email(mail, user_data):
    try:
        # Log email attempt
        current_app.logger.info(f"Attempting to send confirmation email to {user_data['email']}")
        
        msg = Message(
            subject=f"Service Request Confirmed - Token #{user_data['token_number']}",
            recipients=[user_data['email']],
            html=f"""
            <html>
                <body style="font-family: Arial, sans-serif; max-width: 600px; margin: 0 auto; padding: 20px;">
                    <div style="background-color: #4F46E5; color: white; padding: 20px; border-radius: 8px 8px 0 0;">
                        <h1 style="margin: 0;">Service Request Confirmed</h1>
                    </div>
                    <div style="background-color: #f9fafb; padding: 30px; border: 1px solid #e5e7eb; border-radius: 0 0 8px 8px;">
                        <h2 style="color: #1f2937;">Hello {user_data['name']},</h2>
                        <p style="color: #4b5563; font-size: 16px;">Your service request has been successfully registered!</p>
                        
                        <div style="background-color: white; padding: 20px; border-radius: 8px; margin: 20px 0; border-left: 4px solid #4F46E5;">
                            <h3 style="margin-top: 0; color: #4F46E5;">Token Number: #{user_data['token_number']}</h3>
                            <p style="margin: 5px 0;"><strong>Name:</strong> {user_data['name']}</p>
                            <p style="margin: 5px 0;"><strong>Email:</strong> {user_data['email']}</p>
                            <p style="margin: 5px 0;"><strong>Contact:</strong> {user_data['contact_number']}</p>
                            <p style="margin: 5px 0;"><strong>Address:</strong> {user_data['address']}</p>
                            <p style="margin: 5px 0;"><strong>Work Description:</strong> {user_data['work_description']}</p>
                        </div>
                        
                        <p style="color: #6b7280;">Please keep this token number for your records. We will contact you soon regarding your service.</p>
                        
                        <p style="color: #9ca3af; font-size: 14px; margin-top: 30px;">Thank you for choosing our service!</p>
                    </div>
                </body>
            </html>
            """
        )
        mail.send(msg)
        current_app.logger.info(f"Successfully sent confirmation email to {user_data['email']}")
        return True
    except Exception as e:
        error_msg = f"Failed to send confirmation email to {user_data['email']}: {str(e)}"
        current_app.logger.error(error_msg)
        current_app.logger.error(f"Traceback: {traceback.format_exc()}")
        return False

def send_reminder_email(mail, user_data):
    try:
        # Log email attempt
        current_app.logger.info(f"Attempting to send reminder email to {user_data['email']}")
        
        msg = Message(
            subject=f"Service Reminder - Token #{user_data['token_number']}",
            recipients=[user_data['email']],
            html=f"""
            <html>
                <body style="font-family: Arial, sans-serif; max-width: 600px; margin: 0 auto; padding: 20px;">
                    <div style="background-color: #10B981; color: white; padding: 20px; border-radius: 8px 8px 0 0;">
                        <h1 style="margin: 0;">Service Reminder</h1>
                    </div>
                    <div style="background-color: #f9fafb; padding: 30px; border: 1px solid #e5e7eb; border-radius: 0 0 8px 8px;">
                        <h2 style="color: #1f2937;">Hello {user_data['name']},</h2>
                        <p style="color: #4b5563; font-size: 16px;">This is a reminder that your service will begin in approximately <strong>15 minutes</strong>.</p>
                        
                        <div style="background-color: white; padding: 20px; border-radius: 8px; margin: 20px 0; border-left: 4px solid #10B981;">
                            <h3 style="margin-top: 0; color: #10B981;">Token Number: #{user_data['token_number']}</h3>
                            <p style="margin: 5px 0;"><strong>Work Description:</strong> {user_data['work_description']}</p>
                        </div>
                        
                        <p style="color: #6b7280;">Please be ready for your scheduled service. If you have any questions, feel free to contact us.</p>
                        
                        <p style="color: #9ca3af; font-size: 14px; margin-top: 30px;">Thank you for your patience!</p>
                    </div>
                </body>
            </html>
            """
        )
        mail.send(msg)
        current_app.logger.info(f"Successfully sent reminder email to {user_data['email']}")
        return True
    except Exception as e:
        error_msg = f"Failed to send reminder email to {user_data['email']}: {str(e)}"
        current_app.logger.error(error_msg)
        current_app.logger.error(f"Traceback: {traceback.format_exc()}")
        return False