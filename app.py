from flask import Flask, render_template, request, redirect, flash
from send_email import SendEmailClass
from dotenv import load_dotenv
import os

load_dotenv()

app = Flask(__name__)
app.secret_key = os.getenv("APP_PASSWORD")
UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
sender_email = os.getenv("SENDER_EMAIL")


@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        receiver_email = request.form["receiver_email"]
        subject = request.form["subject"]
        body = request.form["body"]
        file = request.files["pdf_file"]

        if file and file.filename.endswith(".pdf"):
            pdf_path = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
            file.save(pdf_path)

            email_sender = SendEmailClass(sender_email, receiver_email, subject, body, pdf_path)
            email_sender.send_email_fun()
            flash("Email sent successfully!", "success")
        else:
            flash("Please upload a valid PDF file.", "danger")

        return redirect("/")
    return render_template("form.html")



if __name__ == "__main__":
    app.run(debug=True)
