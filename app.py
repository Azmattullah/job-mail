from flask import Flask, render_template, request, redirect, flash
from send_email import SendEmailClass
from models import db, EmailSendLog
from dotenv import load_dotenv
import os

load_dotenv()

app = Flask(__name__)
app.secret_key = os.getenv("APP_PASSWORD")
sender_email = os.getenv("SENDER_EMAIL")

# Config SQLite database
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv("DATABASE_URL")
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)

# File uploads
UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        receiver_email_ids = request.form["receiver_email"]
        subject = request.form["subject"]
        body = request.form["body"]
        file = request.files["pdf_file"]

        if file and file.filename.endswith(".pdf"):
            pdf_path = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
            file.save(pdf_path)

            # Clean and split emails
            receiver_emails = [email.strip() for email in receiver_email_ids.split(",") if email.strip()]
            
            for receiver_email in receiver_emails:
                email_sender = SendEmailClass(sender_email, receiver_email, subject, body, pdf_path)
                email_sender.send_email_fun()

                # Extract Name and Company Name form Receiver Email Id
                receiver_email_id = receiver_email.split('@')
                receiver_name = ''.join(i for i in receiver_email_id[0] if not i.isdigit())
                company_name = receiver_email_id[1].split('.')[0]

                # Save to DB
                new_log = EmailSendLog(receiver_email=receiver_email, receiver_name=receiver_name, company_name=company_name)
                db.session.add(new_log)
            
            db.session.commit()
            flash("Email sent successfully!", "success")
        else:
            flash("Please upload a valid PDF file.", "danger")
        
        return redirect("/")
    return render_template("form.html")


@app.route("/table")
def view_logs():
    logs = EmailSendLog.query.order_by(EmailSendLog.timestamp.desc()).all()
    return render_template("table.html", logs=logs)




if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True)