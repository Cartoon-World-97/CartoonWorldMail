from flask import Flask, request, jsonify
from flask_mail import Mail, Message
from dotenv import load_dotenv
import os

load_dotenv()

app = Flask(__name__)

# Mail configuration
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = os.getenv("MAIL_USERNAME")
app.config['MAIL_PASSWORD'] = os.getenv("MAIL_PASSWORD")
app.config['MAIL_DEFAULT_SENDER'] = os.getenv("MAIL_USERNAME")

mail = Mail(app)

@app.route("/send-mail", methods=["POST"])
def send_mail():
    data = request.get_json(silent=True)

    if not data or "to" not in data:
        return jsonify({
            "success": False,
            "error": "'to' field is required"
        }), 400

    msg = Message(
        subject=data.get("subject", "Hello from Flask"),
        recipients=[data.get("to")],
        body=data.get("message", "This is a test email")
    )
    mail.send(msg)
    return jsonify({"success": True, "message": "Email sent successfully"})

if __name__ == "__main__":
    app.run(debug=True)
