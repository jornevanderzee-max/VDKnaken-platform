# CLAUDE.md — VDK Arbeidsvoorwaardenplatform

Lees eerst `docs/plan.md`. Dat is het goedgekeurde plan met het datamodel, de schermen en de bouwstappen. Wijk er niet van af zonder het eerst te vragen.

## Over de opdrachtgever
- Superbeheerder bij VDK Groep, geen fulltime developer. Communiceer in het Nederlands, in gewone taal, zonder vakjargon.
- Werkt volledig in GitHub Codespaces (in de browser). Op de eigen laptop is niets geïnstalleerd.
- Wil na elke bouwstap iets kunnen zien en uitproberen. Sluit elke stap af met een korte lijst **"Zo probeer je het uit"**.

## Werkwijze
- Bouw in de volgorde van de bouwstappen in het plan, één stap tegelijk.
- Een stap is af als: de tests groen zijn, alles gecommit is, je hebt uitgelegd wat er is gebouwd, en de opdrachtgever akkoord heeft gegeven.
- Werk "Stand van zaken" onderaan dit bestand bij na elke stap.
- Kies eenvoud boven slimheid. De code moet jarenlang te onderhouden zijn door een niet-developer met Claude. Voeg geen pakketten toe zonder duidelijke reden, en noem die reden.

## Techniek en conventies
- **Basis**: Django 5.2 LTS, Python 3.12, PostgreSQL.
- **Frontend**: server-rendered templates en gewone CSS. HTMX, SortableJS en Trix staan als bestanden in `static/vendor/`. Geen CDN, geen npm, geen bouwstap.
- **Namen**: domeinnamen in het Nederlands, zoals in het plan (`Bedrijf`, `VDKnaak`, `BedrijfsVoorwaarde`, …). Commentaar ook in het Nederlands.
- **Interfaceteksten**:
  - Altijd via `gettext` of `{% translate %}`, met een Engelse msgid.
  - De Nederlandse tekst staat in `locale/nl/LC_MESSAGES/django.po`. Zet nooit Nederlandse tekst hard in templates of Python.
  - Na elke wijziging: `python manage.py makemessages -l nl`, vertalen, dan `python manage.py compilemessages`.
  - Een test bewaakt dat er geen onvertaalde teksten zijn.
- **Instellingen**: via omgevingsvariabelen (zie `.devcontainer/docker-compose.yml`). Nooit geheimen in de code.
- **Gebruikersmodel**: een eigen model `accounts.Gebruiker` dat inlogt met e-mailadres. Dit moet bestaan vóór de allereerste migratie.

## Beveiligingsregels (niet onderhandelbaar)
- **Toegang bedrijfskant**:
  - Alles loopt via één toegangscontrole ("is deze gebruiker lid van dit bedrijf?").
  - Gegevens worden altijd via het bedrijf opgehaald, nooit los op id.
  - Elke bedrijfs-URL valt automatisch onder de afschermingstest. Die test wordt nooit overgeslagen of uitgezet.
- **Medewerkerspagina**: stuurt `X-Robots-Tag: noindex, nofollow`, een robots-meta-tag, `Referrer-Policy: no-referrer` en `Cache-Control: private` mee.
- **Wervingspagina en PDF**: bevatten nooit links, codes of bedrijfsvelden. De enige uitzondering is de vacaturelink. Een test controleert dit.
- **Uploads**:
  - Afbeeldingen alleen als PNG, JPG of WebP; bij bestandsvelden ook PDF.
  - De grootte is beperkt.
  - Bestanden krijgen willekeurige namen en worden nooit overschreven.
- **Opgemaakte tekst**: altijd opschonen met `nh3`.
- **AVG**: geen persoonsgegevens van medewerkers. Bezoekerstellers gebruiken geen IP-adressen en geen cookies.

## Handige opdrachten
- App starten: `python manage.py runserver 0.0.0.0:8000` en dan tabblad **Ports**, poort 8000.
- Testpostvak (alle uitgaande mail): tabblad **Ports**, poort 8025.
- Tests draaien: `python manage.py test`
- Superbeheerder aanmaken: `python manage.py createsuperuser`. Het beheer staat op `/beheer/`.
- Database: PostgreSQL in de container `db`. De verbinding staat in `DATABASE_URL`.

## Stand van zaken
- **Stap 0 is gebouwd en gecontroleerd in de echte Codespace (01-10-2026). Wacht op akkoord van de opdrachtgever.**
  - Klaar: Django-project (`config/`), de vijf apps uit het plan, `accounts.Gebruiker` (inloggen met e-mail, Argon2) met de eerste migratie, vertaalbestanden (`locale/nl/`), Nederlandse startpagina, Django-beheer op `/beheer/`, vaste versies in `requirements.txt`. 8 tests groen.
  - Tests bewaken de vertalingen: geen onvertaalde teksten, `django.po` bevat alle teksten uit de code, `django.mo` is bijgewerkt.
  - Omgeving: `.devcontainer/Dockerfile` gebruikt `mcr.microsoft.com/devcontainers/python:3-3.12-bookworm` en verwijdert de Yarn-pakketbron (die liet `apt-get update` mislukken, waardoor de Codespace in recovery mode startte).
  - Gecontroleerd: Postgres bereikbaar (`db`), Mailpit op poort 8025, pango/harfbuzz aanwezig (proef-PDF met WeasyPrint gelukt). Het pakket `weasyprint` zelf komt pas in `requirements.txt` bij de stap die PDF's maakt.
- **Volgende:** akkoord op stap 0, dan door naar stap 1.
