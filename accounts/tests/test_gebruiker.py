from django.contrib.auth import authenticate, get_user_model
from django.test import TestCase


class GebruikerTests(TestCase):
    def test_eigen_gebruikersmodel_is_actief(self):
        self.assertEqual(get_user_model()._meta.label, "accounts.Gebruiker")

    def test_inloggen_met_emailadres(self):
        get_user_model().objects.create_user("Beheerder@Voorbeeld.nl", "een-lang-wachtwoord")
        gebruiker = authenticate(email="beheerder@voorbeeld.nl", password="een-lang-wachtwoord")
        self.assertIsNotNone(gebruiker)

    def test_wachtwoord_wordt_met_argon2_opgeslagen(self):
        gebruiker = get_user_model().objects.create_user("a@voorbeeld.nl", "een-lang-wachtwoord")
        self.assertTrue(gebruiker.password.startswith("argon2"))

    def test_alleen_superbeheerder_mag_in_beheeromgeving(self):
        gewoon = get_user_model().objects.create_user("a@voorbeeld.nl", "een-lang-wachtwoord")
        superbeheerder = get_user_model().objects.create_superuser("b@voorbeeld.nl", "een-lang-wachtwoord")
        self.assertFalse(gewoon.is_staff)
        self.assertTrue(superbeheerder.is_staff)
        self.assertTrue(superbeheerder.is_superbeheerder)
