from django.test import TestCase
from django.urls import reverse


class StartpaginaTests(TestCase):
    def test_startpagina_is_nederlands(self):
        antwoord = self.client.get(reverse("start"))
        self.assertEqual(antwoord.status_code, 200)
        self.assertContains(antwoord, '<html lang="nl">')
        # Deze tekst komt uit locale/nl/LC_MESSAGES/django.po, niet uit de template.
        self.assertContains(antwoord, "VDK Arbeidsvoorwaardenplatform")
        self.assertNotContains(antwoord, "VDK working conditions platform")
