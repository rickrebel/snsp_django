import time

from send_mail.pdf_generator import ConstanciaGenerator
from send_mail.send_emails import get_gmail_service, send_email_with_pdf

SUBJECT = "Constancia capacitación +Comunidad +Salud"
SIGNATURE_PATH = "send_mail/firma_melissa.png"
SENDER_NAME = "Frida Melissa Chávez Torcuato"

DELAY_SECONDS = 3       # Pausa entre cada correo
MAX_FAILURES = 50       # Abortar si se acumulan esta cantidad de errores

generator = ConstanciaGenerator(
    doc_name="Participación",
    template_path="send_mail/template_participacion.pdf",
    json_path="send_mail/asistentes.json",
    output_dir="media",
    font_regular_path="media/fonts/Patria_Regular.ttf",
    font_light_path="media/fonts/Patria_Light.ttf",
    font_description_path="media/fonts/NotoSans-Regular.ttf",
)

service = get_gmail_service()
attendees = generator.load_attendees()

# Limitar a N asistentes durante pruebas; quitar el slice para producción
attendees = attendees[:2]
print(f"Asistentes a procesar: {len(attendees)}")

generated = 0
failed = 0

for i, attendee in enumerate(attendees, start=1):
    pdf_path = generator.generate_one(attendee)

    body = (
        f"Hola {attendee.full_name}, espero que el siguiente correo le encuentre bien.\n"
        "Por medio del presente le comparto la Constancia por su participación "
        "como asistente en el curso \"+Comunidad +Salud\".\n"
        "Quedo a su disposición por cualquier duda o comentario.\n"
        "\n"
        "Saludos cordiales"
    )

    result = send_email_with_pdf(
        service=service,
        to=attendee.email,
        subject=SUBJECT,
        body_text=body,
        pdf_path=pdf_path,
        signature_path=SIGNATURE_PATH,
        sender_name=SENDER_NAME,
    )

    if result:
        generated += 1
    else:
        failed += 1
        if failed >= MAX_FAILURES:
            print(f"\n🛑 Se alcanzaron {MAX_FAILURES} errores acumulados. Proceso interrumpido.")
            break

    if i < len(attendees):
        time.sleep(DELAY_SECONDS)

print(f"\n📊 Resumen: {generated} enviados, {failed} fallidos de {len(attendees)} asistentes")