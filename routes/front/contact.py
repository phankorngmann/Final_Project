from app import app, render_template
from flask import request, redirect, url_for, flash
from telagram.telegram import send_telegram_alert



@app.route('/contact')
def contact_page():
    success = request.args.get('success') == 'true'
    return render_template('contact.html', success=success)

@app.route('/submit-contact', methods=['POST'])
def submit_contact():
    # 1. Get the form data
    # form_data = {
    #     'name': request.form.get('inputName'),
    #     'email': request.form.get('inputEmail'),
    #     'message': request.form.get('inputMessage')
    # }

    # Extract variables (or use form_data[...] directly)
    name = request.form.get('name')
    email = request.form.get('email')
    message = request.form.get('message')

    # 2. Format the Telegram alert message
    telegram_message = f"""
🔔 <b>New Contact Form Submission</b>

👤 <b>Name:</b> {name}
📧 <b>Email:</b> {email}
💬 <b>Message:</b>
{message}
"""

    # 3. Send Telegram alert
    if send_telegram_alert(telegram_message):
        flash('Thank you! Your message has been sent successfully.', 'success')
    else:
        flash('Sorry, there was an error sending your message. Please try again.', 'error')

    return redirect(url_for('contact_page'))
