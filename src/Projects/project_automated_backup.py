import os
import subprocess
import smtplib
from email.message import EmailMessage
import datetime

def send_email_report(subject, body, recipient_email):
    sender_email = "your_email@example.com"  # Replace with your email
    sender_password = "your_password"  # Replace with your email password (or use an app-specific password)

    msg = EmailMessage()
    msg.set_content(body)
    msg["Subject"] = subject
    msg["From"] = sender_email
    msg["To"] = recipient_email

    try:
        with smtplib.SMTP("smtp.example.com", 587) as server:  # Replace with your SMTP server
            server.starttls()
            server.login(sender_email, sender_password)
            server.send_message(msg)
    except Exception as e:
        print(f"Failed to send email: {e}")


def backup_to_remote_server(local_directory, remote_user, remote_host, remote_directory):
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    report = f"Backup Report - {timestamp}\n"

    command = [
        "rsync", "-avz", local_directory,
        f"{remote_user}@{remote_host}:{remote_directory}"
    ]

    try:
        result = subprocess.run(command, check=True, capture_output=True, text=True)
        report += "Backup completed successfully.\n"
        report += result.stdout
        success = True
    except subprocess.CalledProcessError as e:
        report += "Backup failed.\n"
        report += e.stderr
        success = False

    # Save the report to a local file
    report_file = f"backup_report_{timestamp}.txt"
    with open(report_file, "w") as file:
        file.write(report)

    return success, report_file


if __name__ == "__main__":
    # Configuration (replace with actual values)
    LOCAL_DIRECTORY = "/path/to/local/directory"
    REMOTE_USER = "remote_user"
    REMOTE_HOST = "remote_host.example.com"
    REMOTE_DIRECTORY = "/path/to/remote/directory"
    REPORT_RECIPIENT_EMAIL = "recipient@example.com"

    success, report_file = backup_to_remote_server(LOCAL_DIRECTORY, REMOTE_USER, REMOTE_HOST, REMOTE_DIRECTORY)

    if success:
        subject = "Backup Successful"
        body = f"The backup was completed successfully. See the attached report for details."
    else:
        subject = "Backup Failed"
        body = f"The backup operation failed. See the attached report for details."

    with open(report_file, "r") as file:
        body += "\n\n" + file.read()

    send_email_report(subject, body, REPORT_RECIPIENT_EMAIL)

    print(f"Backup operation completed. Report saved as {report_file}.")
