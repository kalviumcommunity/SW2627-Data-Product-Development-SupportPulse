import os
import smtplib
from email.message import EmailMessage


def send_report_email(
    recipient,
    subject,
    report_content
):
    """
    Send a SupportPulse insight report by email.

    SMTP credentials are read from environment variables.
    Returns True on success and False on failure.
    """

    # ==========================================
    # READ SMTP CONFIGURATION
    # ==========================================

    smtp_host = os.getenv(
        "SMTP_HOST"
    )

    smtp_port = int(
        os.getenv(
            "SMTP_PORT",
            "587"
        )
    )

    smtp_username = os.getenv(
        "SMTP_USERNAME"
    )

    smtp_password = os.getenv(
        "SMTP_PASSWORD"
    )

    sender_email = os.getenv(
        "SENDER_EMAIL"
    )

    # ==========================================
    # VALIDATE CONFIGURATION
    # ==========================================

    required_values = {
        "SMTP_HOST": smtp_host,
        "SMTP_USERNAME": smtp_username,
        "SMTP_PASSWORD": smtp_password,
        "SENDER_EMAIL": sender_email
    }

    missing_values = [
        key
        for key, value in required_values.items()
        if not value
    ]

    if missing_values:

        print(
            "Email configuration is missing: "
            + ", ".join(missing_values)
        )

        return False

    # ==========================================
    # CREATE EMAIL
    # ==========================================

    message = EmailMessage()

    message["From"] = sender_email
    message["To"] = recipient
    message["Subject"] = subject

    message.set_content(
        report_content
    )

    # ==========================================
    # SEND EMAIL
    # ==========================================

    try:

        with smtplib.SMTP(
            smtp_host,
            smtp_port,
            timeout=20
        ) as server:

            server.starttls()

            server.login(
                smtp_username,
                smtp_password
            )

            server.send_message(
                message
            )

        return True

    except Exception as error:

        # Email failure must not crash the application.
        print(
            f"Email sending failed: {error}"
        )

        return False