# send_emails.py
import base64
import os
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.image import MIMEImage
from email.mime.base import MIMEBase
from email import encoders
from email.utils import formataddr
import time
from google.oauth2.credentials import Credentials
from google.auth.transport.requests import Request
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

SCOPES = ['https://www.googleapis.com/auth/gmail.send']


def get_gmail_service():
    # Construye las credenciales desde variables de entorno.
    # El access token se obtiene automáticamente vía refresh_token.
    creds = Credentials(
        token=None,
        refresh_token=os.getenv('GMAIL_REFRESH_TOKEN'),
        token_uri='https://oauth2.googleapis.com/token',
        client_id=os.getenv('GMAIL_CLIENT_ID'),
        client_secret=os.getenv('GMAIL_CLIENT_SECRET'),
        scopes=SCOPES,
    )
    creds.refresh(Request())
    return build('gmail', 'v1', credentials=creds)


def build_message(to: str  , subject: str, body_html: str, body_text: str = None):
    message = MIMEMultipart('alternative')
    message['to'] = to
    message['subject'] = subject

    if body_text:
        message.attach(MIMEText(body_text, 'plain'))
    message.attach(MIMEText(body_html, 'html'))

    raw = base64.urlsafe_b64encode(message.as_bytes()).decode()
    return { 'raw': raw }


def send_email(service, to: str, subject: str, body_html: str):
    try:
        message = build_message(to, subject, body_html)
        result = service.users().messages().send(
            userId='me',  # 'me' = la cuenta autorizada
            body=message
        ).execute()
        print(f"✅ Enviado a {to} | Message ID: {result['id']}")
        return result
    except HttpError as e:
        print(f"❌ Error enviando a {to}: {e}")
        return None


def send_bulk(recipients: list[dict]):
    """
    recipients: lista de dicts con keys: email, subject, body_html
    Ejemplo: [{'email': 'x@x.com', 'subject': 'Hola', 'body_html': '<p>...</p>'}]
    """
    service = get_gmail_service()
    results = []

    for i, recipient in enumerate(recipients):
        result = send_email(
            service,
            to=recipient['email'],
            subject=recipient['subject'],
            body_html=recipient['body_html']
        )
        results.append({
            'email': recipient['email'],
            'success': result is not None,
            'message_id': result.get('id') if result else None
        })

    # Resumen
    sent = sum(1 for r in results if r['success'])
    print(f"\n📊 Resumen: {sent}/{len(recipients)} correos enviados")
    return results


def send_email_with_pdf(
    service,
    to: str,
    subject: str,
    body_text: str,
    pdf_path: str,
    signature_path: str | None = None,
    sender_name: str | None = None,
) -> dict | None:
    """
    Send an email with a PDF attachment and an optional inline signature image.

    The body is rendered as minimal HTML so the signature image can appear
    inline below the text. A plain-text fallback is also included for
    clients that do not render HTML.

    sender_name: display name shown to the recipient (e.g. "Frida Chávez").
                 The actual sending address is always the authenticated Gmail account.
    """
    # Outer container — holds the body+signature block and the PDF attachment
    message = MIMEMultipart("mixed")
    message["to"] = to
    message["subject"] = subject
    if sender_name:
        # formataddr("Nombre", "") lets Gmail fill in the real address
        message["from"] = formataddr((sender_name, ""))

    # Build the HTML body, converting newlines to <br> tags
    html_lines = "".join(
        f"<p>{line}</p>" if line.strip() else "<br>"
        for line in body_text.splitlines()
    )
    signature_tag = (
        '<img src="cid:firma_melissa" alt="Firma">'
        if signature_path else ""
    )
    html_body = (
        "<html><body style='font-family:sans-serif;font-size:14px;'>"
        f"{html_lines}"
        f"{signature_tag}"
        "</body></html>"
    )

    if signature_path and os.path.isfile(signature_path):
        # multipart/related groups the HTML with its inline image
        related = MIMEMultipart("related")
        related.attach(MIMEText(html_body, "html", "utf-8"))

        with open(signature_path, "rb") as f:
            img = MIMEImage(f.read())
        img.add_header("Content-ID", "<firma_melissa>")
        img.add_header(
            "Content-Disposition", "inline",
            filename=os.path.basename(signature_path),
        )
        related.attach(img)
        message.attach(related)
    else:
        message.attach(MIMEText(html_body, "html", "utf-8"))

    # Plain-text fallback (shown by clients that strip HTML)
    # message.attach(MIMEText(body_text, "plain", "utf-8"))

    # PDF attachment
    with open(pdf_path, "rb") as f:
        pdf_part = MIMEBase("application", "pdf")
        pdf_part.set_payload(f.read())
    encoders.encode_base64(pdf_part)
    pdf_part.add_header(
        "Content-Disposition", "attachment",
        filename=os.path.basename(pdf_path),
    )
    message.attach(pdf_part)

    raw = base64.urlsafe_b64encode(message.as_bytes()).decode()

    # Retry once on 429 (rate limit): wait 60 s then try again
    for attempt in (1, 2):
        try:
            result = service.users().messages().send(
                userId="me", body={"raw": raw}
            ).execute()
            print(f"✅ Enviado a {to} | Message ID: {result['id']}")
            return result
        except HttpError as e:
            if e.status_code == 429 and attempt == 1:
                print(f"⏳ Rate limit alcanzado. Esperando 60 s antes de reintentar ({to})...")
                time.sleep(60)
            else:
                print(f"❌ Error enviando a {to}: {e}")
                return None


# --- Ejemplo de uso ---
if __name__ == '__main__':
    recipients = [
        {
            'email': 'rickrebel@gmail.com',
            'subject': 'Primer asunto rickrebel',
            'body_html': '<h1>Hola</h1><p>Cuerpo del correo</p>'
        },
        {
            'email': 'ricardo@yeeko.org',
            'subject': 'Otro asunto yeeko',
            'body_html': '<p>Otro mensaje</p>'
        },
    ]

    send_bulk(recipients)