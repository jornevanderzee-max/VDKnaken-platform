"""Bewaakt dat alle interfaceteksten een Nederlandse vertaling hebben.

Faalt deze test, voer dan uit:
    python manage.py makemessages -l nl
    (vertaal de nieuwe teksten in locale/nl/LC_MESSAGES/django.po)
    python manage.py compilemessages
"""

import gettext
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

from django.conf import settings
from django.test import SimpleTestCase

PO_BESTAND = settings.BASE_DIR / "locale" / "nl" / "LC_MESSAGES" / "django.po"
MO_BESTAND = PO_BESTAND.with_suffix(".mo")
OVERSLAAN = shutil.ignore_patterns(".git", "__pycache__", "staticfiles", "media", "venv", ".venv")


def lees_mo(pad):
    with open(pad, "rb") as bestand:
        return gettext.GNUTranslations(bestand)._catalog


class VertalingenTests(SimpleTestCase):
    def test_alle_teksten_zijn_vertaald(self):
        uitkomst = subprocess.run(
            ["msgfmt", "--check", "--statistics", "-o", "/dev/null", str(PO_BESTAND)],
            capture_output=True, text=True,
        )
        self.assertEqual(uitkomst.returncode, 0, uitkomst.stderr)
        self.assertNotIn("untranslated", uitkomst.stderr, "Er zijn onvertaalde teksten.")
        self.assertNotIn("fuzzy", uitkomst.stderr, "Er zijn vertalingen gemarkeerd als 'fuzzy'.")

    def test_po_bestand_bevat_alle_teksten_uit_de_code(self):
        # Draai makemessages in een kopie van het project en vergelijk met het echte .po-bestand.
        with tempfile.TemporaryDirectory() as tijdelijk:
            kopie = Path(tijdelijk) / "project"
            shutil.copytree(settings.BASE_DIR, kopie, ignore=OVERSLAAN)
            subprocess.run(
                [sys.executable, "manage.py", "makemessages", "-l", "nl"],
                cwd=kopie, check=True, capture_output=True,
            )
            vers = kopie / "locale" / "nl" / "LC_MESSAGES" / "django.po"
            uitkomst = subprocess.run(
                ["msgcmp", "--use-untranslated", str(PO_BESTAND), str(vers)],
                capture_output=True, text=True,
            )
        self.assertEqual(
            uitkomst.returncode, 0,
            "Er staan teksten in de code die nog niet in django.po staan. "
            "Voer makemessages uit.\n" + uitkomst.stderr,
        )

    def test_mo_bestand_is_bijgewerkt(self):
        with tempfile.TemporaryDirectory() as tijdelijk:
            nieuw = Path(tijdelijk) / "django.mo"
            subprocess.run(["msgfmt", "-o", str(nieuw), str(PO_BESTAND)], check=True)
            self.assertEqual(
                lees_mo(MO_BESTAND), lees_mo(nieuw),
                "django.mo loopt achter op django.po. Voer compilemessages uit.",
            )
