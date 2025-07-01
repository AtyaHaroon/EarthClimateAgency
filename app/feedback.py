from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_mail import Message, Mail
from .mongo import mongo  # Assuming you are using MongoDB
import re

feedback_bp = Blueprint('feedback', __name__)

@feedback_bp.route('/feedback', methods=['GET', 'POST'])
def submit_feedback():
    if request.method == 'POST':
        email = request.form.get('email')
        user_feedback = request.form.get('feedback')
        
        try:
            # Save feedback to MongoDB
            mongo.db.feedback.insert_one({'email': email, 'feedback': user_feedback})

            # Send feedback to admin's email
            send_feedback_to_admin(email, user_feedback)

            # Flash a success message
            flash('Thank you for your feedback!', 'success')

            # Redirect to thank you page or index page after feedback is submitted
            return redirect(url_for('feedback.thank_you'))

        except Exception as e:
            # Flash error message if saving feedback fails
            flash('An error occurred while submitting your feedback. Please try again later.', 'danger')
            return redirect(url_for('feedback.submit_feedback'))

    return render_template('feedback.html')

# Function to send feedback to admin's email
def send_feedback_to_admin(user_email, user_feedback):
    try:
        # Create the email message
        msg = Message("New Feedback Submission", recipients=["aseefahmed@aptechnorth.edu.pk"])
        msg.body = f"New feedback submitted:\n\nEmail: {user_email}\nFeedback: {user_feedback}"

        # Send the email
        Mail.send(msg)
    except Exception as e:
        print(f"Error sending email: {str(e)}")

# Route for the thank you page
@feedback_bp.route('/thank_you', methods=['GET'])
def thank_you():
    return render_template('thank_you.html')