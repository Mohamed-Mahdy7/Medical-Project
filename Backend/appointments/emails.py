from django.core.mail import send_mail
from django.conf import settings


def send_booking_confirmation(appointment):
    patient = appointment.patient
    doctor = appointment.doctor
    patient_user = patient.user
    doctor_user = doctor.user

    subject = "Appointment Booking Confirmation"

    message = f"""
Hello {patient_user.first_name},

Your appointment has been successfully booked.

Details:
- Doctor: Dr. {doctor_user.first_name} {doctor_user.last_name}
- Specialty: {doctor.specialty.name if doctor.specialty else 'N/A'}
- Date & Time: {appointment.start_time.strftime('%A, %B %d, %Y at %I:%M %p')}
- End Time: {appointment.end_time.strftime('%I:%M %p')}
- Status: {appointment.get_status_display()}

If you need to cancel or reschedule, please log in to your account.

Thank you,
Medical Platform Team
"""

    send_mail(
        subject=subject,
        message=message,
        from_email=settings.DEFAULT_FROM_EMAIL,
        recipient_list=[patient_user.email],
        fail_silently=False,
    )