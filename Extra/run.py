from send_email import SendEmailClass



if __name__ == "__main__":
    sender_email = "azmat711@yahoo.com"
    pdf_path = "azmat-cloud-devops.pdf"

    receiver_email = "azmattullah0@gmail.com"
    subject = "Sample PDF Attachment 2"
    body = "<H1> Please find the attached PDF file. </H1>"

    sendEmail = SendEmailClass(sender_email, receiver_email, subject, body, pdf_path)
    sendEmail.send_email_fun()
