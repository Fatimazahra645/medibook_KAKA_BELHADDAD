from django.test import TestCase
from django.contrib.auth import get_user_model
from doctors.models import Doctor, Speciality, Availability
from patients.models import Patient
from appointments.services import get_available_slots, book_appointment
from datetime import date, time

User = get_user_model()


class AppointmentServiceTests(TestCase):

    def setUp(self):
        # Créer un utilisateur médecin
        self.doctor_user = User.objects.create_user(
            username="doctor1", password="testpass123", role="DOCTOR",
            first_name="Jean", last_name="Dupont"
        )
        self.speciality = Speciality.objects.create(name="Cardiologie")
        self.doctor = Doctor.objects.get(user=self.doctor_user)
        self.doctor.speciality = self.speciality
        self.doctor.save()

        # Disponibilité lundi 09h–11h
        Availability.objects.create(
            doctor=self.doctor,
            day_of_week="MONDAY",
            start_time=time(9, 0),
            end_time=time(11, 0),
        )

        # Créer un utilisateur patient
        self.patient_user = User.objects.create_user(
            username="patient1", password="testpass123", role="PATIENT"
        )
        self.patient = Patient.objects.get(user=self.patient_user)

    def _next_weekday(self, weekday):
        """Retourne la prochaine date correspondant au jour de la semaine (0=lundi)."""
        today = date.today()
        days_ahead = weekday - today.weekday()
        if days_ahead <= 0:
            days_ahead += 7
        return today.replace(day=today.day + days_ahead) if False else \
               date.fromordinal(today.toordinal() + days_ahead)

    def test_slots_available_on_monday(self):
        next_monday = self._next_weekday(0)
        slots = get_available_slots(self.doctor, next_monday)
        self.assertIn("09:00", slots)
        self.assertIn("09:30", slots)
        self.assertIn("10:30", slots)
        self.assertNotIn("11:00", slots)  # heure de fin non incluse

    def test_no_slots_on_sunday(self):
        next_sunday = self._next_weekday(6)
        slots = get_available_slots(self.doctor, next_sunday)
        self.assertEqual(slots, [])

    def test_book_appointment_success(self):
        next_monday = self._next_weekday(0)
        appt, msg = book_appointment(
            patient=self.patient,
            doctor=self.doctor,
            speciality=self.speciality,
            date=next_monday,
            time=time(9, 0),
            reason="Douleur thoracique",
        )
        self.assertIsNotNone(appt)
        self.assertEqual(appt.status, "PENDING")

    def test_book_appointment_slot_conflict(self):
        next_monday = self._next_weekday(0)
        book_appointment(
            patient=self.patient, doctor=self.doctor,
            speciality=self.speciality, date=next_monday,
            time=time(9, 0), reason="Premier rendez-vous",
        )
        appt2, msg2 = book_appointment(
            patient=self.patient, doctor=self.doctor,
            speciality=self.speciality, date=next_monday,
            time=time(9, 0), reason="Doublon",
        )
        self.assertIsNone(appt2)

    def test_book_appointment_invalid_slot(self):
        next_monday = self._next_weekday(0)
        appt, msg = book_appointment(
            patient=self.patient, doctor=self.doctor,
            speciality=self.speciality, date=next_monday,
            time=time(14, 0),  # hors disponibilité
            reason="Hors créneau",
        )
        self.assertIsNone(appt)

    def test_authenticated_patient_can_access_book_page(self):
        self.client.login(username="patient1", password="testpass123")
        response = self.client.get(f"/appointments/book/{self.doctor.id}/")
        self.assertEqual(response.status_code, 200)

    def test_unauthenticated_redirected_from_book(self):
        response = self.client.get(f"/appointments/book/{self.doctor.id}/")
        self.assertEqual(response.status_code, 302)
        self.assertIn("/login/", response.url)
