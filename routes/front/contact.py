from app import app, render_template
from flask import request, redirect, url_for, flash
from telagram.telegram import send_telegram_alert
import html
import logging

logger = logging.getLogger(__name__)



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

    # --- DEBUG: dump incoming request headers and form to a file for troubleshooting ---
    try:
        import os, json
        os.makedirs('tmp', exist_ok=True)
        debug_path = os.path.join('tmp', 'contact_debug.log')
        with open(debug_path, 'a', encoding='utf-8') as fh:
            fh.write('\n--- REQUEST %s ---\n' % __import__('datetime').datetime.utcnow().isoformat())
            fh.write('remote_addr: %s\n' % (request.remote_addr,))
            fh.write('headers: %s\n' % json.dumps({k: v for k, v in request.headers.items()}))
            fh.write('form: %s\n' % json.dumps({k: v for k, v in request.form.items()}))
    except Exception:
        logger.exception('Failed to write debug file for contact request')

    # Extract variables (or use form_data[...] directly) and escape for HTML
    name = html.escape((request.form.get('name') or '').strip())
    email = html.escape((request.form.get('email') or '').strip())
    message = html.escape((request.form.get('message') or '').strip())

    # 2. Format the Telegram alert message - plain text only
    from datetime import datetime

    parts = ["New Contact Form Submission"]
    parts.append(f"Received: {datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S')} UTC")

    if name:
        parts.append(f"Name: {name}")
    if email:
        parts.append(f"Email: {email}")
    if message:
        parts.append("Message:")
        parts.append(message)

    telegram_message = "\n\n".join(parts)

    # 3. Send Telegram alert and log the result for debugging
    logger.debug("Contact form received: name=%s email=%s message_len=%d", name, email, len(message))
    ok = send_telegram_alert(telegram_message)
    if ok:
        logger.info("Telegram alert sent for contact form (name=%s email=%s).", name, email)
        flash('Thank you! Your message has been sent successfully.', 'success')
    else:
        logger.error("Failed to send Telegram alert for contact form (name=%s email=%s).", name, email)
        flash('Sorry, there was an error sending your message. Please try again.', 'error')

    return redirect(url_for('contact_page'))
