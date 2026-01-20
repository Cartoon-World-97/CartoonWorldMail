from flask import Flask, request, jsonify
from flask_mail import Mail, Message
from dotenv import load_dotenv
import os

# Load .env for local development ONLY
load_dotenv()

app = Flask(__name__)

# ===============================
# Mail Configuration
# ===============================
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = os.getenv("MAIL_USERNAME")
app.config['MAIL_PASSWORD'] = os.getenv("MAIL_PASSWORD")

# IMPORTANT: Default sender (fixes your error)
app.config['MAIL_DEFAULT_SENDER'] = (
    f"Flask App <{app.config['MAIL_USERNAME']}>"
)

mail = Mail(app)

# ===============================
# Health Check
# ===============================
@app.route("/", methods=["GET"])
def home():
    return jsonify({"status": "Flask Mail App Running ✅"})

# ===============================
# Send Mail API
# ===============================
@app.route("/send-mail", methods=["POST"])
def send_mail():
    data = request.get_json(silent=True)

    if not data:
        return jsonify({"error": "JSON body required"}), 400

    if "to" not in data:
        return jsonify({"error": "'to' field is required"}), 400

    if not app.config["MAIL_USERNAME"]:
        return jsonify({"error": "Mail server not configured"}), 500

    try:
        msg = Message(
            subject=data.get("subject", "Hello from Flask"),
            sender=app.config["MAIL_USERNAME"],   # 🔥 FIX
            recipients=[data["to"]],
            body=data.get("message", "Test email from Flask")
        )

        mail.send(msg)
        return jsonify({"success": True, "message": "Email sent successfully"})

    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500
