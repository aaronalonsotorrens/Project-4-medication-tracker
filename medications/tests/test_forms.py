from django.test import TestCase
from medications.forms import MedicationForm, SideEffectForm
from django.contrib.auth.models import User
from medications.models import Medication


class TestMedicationForm(TestCase):

    def test_medication_form_is_valid(self):
        form = MedicationForm(data={
            'name': 'Ibuprofen',
            'category': 'Joints',
            'dosage': '400mg',
            'frequency': 2,
            'start_date': '2023-01-01',
            'end_date': '2023-01-10'
        })
        self.assertTrue(form.is_valid(), msg="Medication form should be valid with correct data")

    def test_medication_form_is_invalid(self):
        form = MedicationForm(data={
            'name': '',
            'category': 'Joints',
            'dosage': '',
            'frequency': '',
            'start_date': '',
            'end_date': ''
        })
        self.assertFalse(form.is_valid(), msg="Medication form should be invalid with missing fields")


class TestSideEffectForm(TestCase):

    def test_side_effect_form_is_valid(self):
        form = SideEffectForm(data={
            'category': 'Nausea',
            'description': 'Mild nausea after taking medication'
        })
        self.assertTrue(form.is_valid(), msg="Side effect form should be valid with proper data")

    def test_side_effect_form_is_invalid(self):
        form = SideEffectForm(data={
            'category': '',
            'description': ''
        })
        self.assertFalse(form.is_valid(), msg="Side effect form should be invalid with empty fields")
