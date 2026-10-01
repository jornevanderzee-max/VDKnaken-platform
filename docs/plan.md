# Plan: VDK Arbeidsvoorwaardenplatform

## Context

VDK Groep (±50 zelfstandige bedrijven) heeft centrale arbeidsvoorwaarden ("VDKnaken") en per bedrijf eigen regelingen. Nu staat dat versnipperd over mail, intranet en flyers, en een medewerker heeft geen vaste plek waar hij kan zien "wat heb ik eigenlijk allemaal?".

Het platform lost dat op. Elk bedrijf stelt in een paar stappen een eigen arbeidsvoorwaardenpagina samen, in de eigen huisstijl, met drie weergaven:
- een afgeschermde **medewerkerspagina**;
- een vindbare **wervingspagina**;
- een verzorgde **PDF met QR-code**.

Jij beheert als superbeheerder de centrale VDKnaken en volgt in een portaal welke bedrijven wat gebruiken en hoe vaak alles bekeken wordt.

Er is nog geen bestaande code. De huidige map (`DOS'46\Coachcore`) hoort bij een ander project en wordt niet gebruikt.

## Genomen besluiten

| Onderwerp | Besluit |
|---|---|
| Techniek | **Django 5.2 LTS (Python)**, één applicatie, PostgreSQL-database |
| Werkplek | **In de cloud**: GitHub Codespaces, niets installeren op de laptop |
| Taal | Focus op Nederland. Alle interfaceteksten staan wel in aparte tekstbestanden, zodat Duits later kan. |
| Nieuw verplicht veld bij een knaak die al live staat | Knaak **blijft zichtbaar** met de bestaande info. Het bedrijf krijgt een openstaande taak en een mail. |

## Uitgangspunten (zeg het als iets anders moet)

1. Publiceren legt alleen de **keuzes van het bedrijf** vast. De centrale VDKnaak-tekst wordt altijd live getoond, dus jouw wijziging staat meteen overal.
2. Een verlopen VDKnaak wordt vanaf de einddatum **niet meer getoond**. Verleng je de datum, dan komt hij vanzelf terug. Er komt een mail aan de superbeheerders 60 en 14 dagen vooraf. Op de einddatum zelf krijgen de beheerders van de betrokken bedrijven een korte melding.
3. De **takenlijst wordt berekend** uit de gegevens en niet apart bijgehouden.
4. **Kleuren krijgen een vaste rol.** Het systeem kiest zelf witte of donkere tekst op elke kleur en verdonkert kleuren die als tekst op wit te licht zijn. Daardoor is een onleesbare pagina onmogelijk.
5. Beheerders worden **uitgenodigd** en kiezen zelf hun wachtwoord. "Resetten" stuurt een nieuwe link, dus niemand kent andermans wachtwoord.
6. Er kunnen **meerdere superbeheerders** zijn. Bedrijfsbeheerders kunnen **zelf collega's uitnodigen**.
7. Eén persoon kan **beheerder zijn van meerdere bedrijven** (bijvoorbeeld een HR-dienst die meerdere bedrijven bedient). Diegene wisselt dan met een keuzemenu van bedrijf.
8. Een nieuw aangevinkte VDKnaak met ontbrekende verplichte velden **wordt bij publiceren overgeslagen**, met een duidelijke melding. De rest van de pagina gaat wel live, zodat één ontbrekende link niet alles blokkeert.
9. **Wervingsversie**: naam, logo, "wat is het" en "wat heb je eraan". "Hoe start je", links, codes en bedrijfsvelden staan alleen op de medewerkerspagina. Per voorwaarde is "niet tonen bij werving" in te stellen.
10. Teksten krijgen **eenvoudige opmaak** (vet, cursief, opsomming, link). Alles wordt opgeschoond opgeslagen, dus zonder vrije HTML.
11. **Kleine toevoegingen** in stap 4, allemaal optioneel:
    - een korte welkomsttekst;
    - een contactregel ("Vragen? Mail hr@…");
    - een link naar de vacaturepagina. Dat is de enige link die wél op de wervingspagina en in de PDF staat.
12. **Volgorde** bepaal je met slepen én met knoppen "omhoog/omlaag". Met alleen slepen werkt het niet met het toetsenbord.
13. **Wizard de eerste keer, daarna tabbladen.** Bovenin staat altijd een balk met de publicatiestatus.
14. Gepubliceerde versies worden bewaard (wie en wanneer). Een knop om een oude versie terug te zetten komt niet in de eerste versie.
15. Tot het superbeheerdersportaal af is (stap 9) gebruik je de **standaard Django-beheeromgeving** om VDKnaken, bedrijven en accounts te beheren.

## Techniek in één oogopslag

- **Django 5.2 LTS** (ondersteund tot april 2028), Python 3.12, PostgreSQL.
- Pagina's worden op de server gemaakt (Django-templates) met gewone CSS en een kleurthema per bedrijf. Er is **geen bouwstap** en er zijn geen npm-pakketten.
- Kleine hulpbibliotheken staan in het project zelf, zonder externe CDN:
  - **HTMX** om op te slaan zonder de pagina te herladen;
  - **SortableJS** voor slepen;
  - **Trix** als eenvoudige teksteditor.
- De overige Python-pakketten:

  | Pakket | Waarvoor |
  |---|---|
  | `argon2-cffi` | Wachtwoorden veilig opslaan |
  | `django-axes` | Blokkade na te veel mislukte inlogpogingen |
  | `weasyprint` | PDF maken |
  | `segno` | QR-code (scherp in print) |
  | `openpyxl` | Export naar Excel |
  | `nh3` | Tekst opschonen |
  | `pillow` | Afbeeldingen controleren en verkleinen |
  | `whitenoise`, `gunicorn`, `psycopg` | Draaien in productie |

- **Vertalingen**: de teksten in de code zijn Engelse sleutels. Alle Nederlandse interfaceteksten staan in `locale/nl/LC_MESSAGES/django.po`, te bewerken met het gratis programma Poedit. Duits wordt later `locale/de/…` zonder codewijziging.
- **Hosting** (vanaf stap 4): voorstel **Render, regio Frankfurt**. Dat is een webservice met een Docker-image, beheerde PostgreSQL met back-ups, een kleine schijf voor logo's en een dagelijkse geplande taak. Ongeveer €15 per maand. De definitieve keuze maken we in stap 4.
- **Projectindeling**:
  ```
  vdk-arbeidsvoorwaarden/
    .devcontainer/        Codespace-configuratie (Python, Postgres, Mailpit, PDF-bibliotheken)
    config/               instellingen en URL's
    accounts/             gebruikers, inloggen, uitnodigen, rechten per bedrijf
    catalogus/            centrale VDKnaken en hun velden
    bedrijven/            editor voor bedrijfsbeheerders, concept en publiceren
    publiek/              medewerkerspagina, wervingspagina, PDF en tellers
    portaal/              superbeheerdersportaal en export
    templates/  static/  locale/nl/
    docs/plan.md          dit plan
    CLAUDE.md             werkafspraken voor Claude
    Dockerfile            productie-image (zelfde basis als de Codespace)
  ```

## Werkplek in de cloud (stap 0, eenmalig)

**Wat je zelf doet (±15 minuten, ik loop het met je door):**
1. Maak een GitHub-account aan, bij voorkeur op een **zakelijk VDK-mailadres**. Zo is het project van VDK en niet van een persoon.
2. Maak een **private repository** aan, bijvoorbeeld `vdk-arbeidsvoorwaarden`.
3. Upload het **startpakket** (de inhoud van de map `C:\Users\JornevanderZee\vdk-arbeidsvoorwaarden`) door het op de GitHub-pagina te slepen. Daarin zitten de Codespace-configuratie, dit plan (`docs/plan.md`) en de werkafspraken voor Claude (`CLAUDE.md`).
4. Klik op **Code → Codespaces → Create**. Er opent een VS Code in je browser. Database, testpostvak, PDF-onderdelen en Claude Code worden automatisch geïnstalleerd.
5. Typ `claude` in de terminal en log in.

Vanaf dat moment bouw ik verder in de Codespace. De app draait daar en je opent hem via een link in je browser. Een persoonlijk account heeft ongeveer 60 uur per maand gratis Codespace-gebruik. Een Codespace stopt vanzelf na 30 minuten zonder activiteit.

Voordat het project live gaat, verhuizen we de repository naar een GitHub-organisatie van VDK.

## Datamodel

```
Gebruiker ──< Lidmaatschap >── Bedrijf ──< BedrijfsVoorwaarde >── VDKnaak ──< KnaakVeld
                                  │               │                                │
                                  │               └──< Veldwaarde >────────────────┘
                                  ├──< Publicatie
                                  ├──< Weergaveteller
                                  └──< OudeSlug
VDKnaak ──< Melding
```

**Gebruiker**: e-mailadres (om in te loggen), naam, wachtwoord (Argon2), superbeheerder ja/nee, actief, laatste login.

**Lidmaatschap**: gebruiker en bedrijf. Dit bepaalt welke bedrijven iemand mag beheren.

**VDKnaak** (centraal, alleen door jou te beheren):
- naam, logo, actief ja/nee, einddatum (optioneel);
- "Wat is het" en "Wat heb je eraan": tekst, ook zichtbaar bij werving;
- "Hoe start je": tekst, alleen voor medewerkers;
- centrale link met knoptekst en centrale code (optioneel), alleen voor medewerkers.

**KnaakVeld** (velden die een bedrijf zelf moet aanleveren, per VDKnaak):
- label ("Eigen aanmeldlink"), type (tekst / link / bestand), verplicht ja/nee;
- uitleg voor HR ("Plak hier de link van jullie Alleo-omgeving");
- knoptekst (bij een link), volgorde.
- Deze velden staan altijd alleen op de medewerkerspagina.

**Bedrijf**:
- naam en slug (het leesbare deel van de wervingslink);
- medewerkerssleutel: het willekeurige, onraadbare deel van de medewerkerslink, te vernieuwen;
- paginawachtwoord (optioneel, versleuteld opgeslagen);
- logo, kleur 1 t/m 3;
- welkomsttekst, contactregel en vacaturelink (alle drie optioneel);
- taal (standaard `nl`, voor later).

**BedrijfsVoorwaarde**: één lijst per bedrijf voor zowel VDKnaken als eigen regelingen, zodat ze samen te ordenen zijn.
- soort: vdknaak of eigen;
- bij soort vdknaak: welke VDKnaak;
- bij soort eigen: naam, omschrijving, afbeelding (optioneel), link met knoptekst (optioneel);
- actief ja/nee, volgorde, tonen bij werving ja/nee.

**Veldwaarde**: de ingevulde waarde (tekst, link of bestand) van één KnaakVeld bij één BedrijfsVoorwaarde.

**Publicatie**:
- een momentopname (JSON) van de bedrijfskeuzes: welke voorwaarden, volgorde, veldwaarden, eigen teksten, huisstijl;
- datum en door wie gepubliceerd;
- de PDF die daarbij hoort.

**Weergaveteller**: bedrijf, maand, soort (medewerkerspagina / wervingspagina / PDF-download) en aantal. Alleen tellers, geen IP-adressen of cookies.

**OudeSlug**: vroegere wervingslinks die doorverwijzen naar de huidige, zodat QR-codes op papier blijven werken.

**Melding**: welke einddatumwaarschuwing al verstuurd is (60 dagen, 14 dagen of verlopen), zodat niemand dubbel gemaild wordt.

Wat er bewust niet in staat: gegevens van medewerkers. Er is ook geen aparte takentabel, want taken worden berekend.

## Hoe concept, publiceren en centrale teksten samenwerken

- **Concept**: alles wat de beheerder aanpast, gaat direct in de gewone tabellen. Online verandert er niets.
- **Publiceren**: het concept wordt vastgelegd als nieuwe Publicatie en de PDF wordt gemaakt. De publieke pagina's lezen alleen de laatste Publicatie.
- **Weergave**: een publieke pagina combineert drie dingen:
  - de momentopname van het bedrijf;
  - de **actuele** centrale teksten van de VDKnaken;
  - de einddatum- en actief-controle (verlopen of gedeactiveerde knaken vallen weg).
- **"Wijzigingen klaar?"**: het concept wordt vergeleken met de laatste Publicatie. Zijn ze verschillend, dan toont de balk bovenin "Er staan wijzigingen klaar".
- **Nieuw aangevinkte knaak met lege verplichte velden**: wordt bij publiceren overgeslagen. Een knaak die al live stond en een nieuw verplicht veld krijgt, blijft staan (jouw keuze) en levert een taak op.
- **Wijzigt de centrale tekst**, dan verandert de PDF mee. De PDF's van betrokken bedrijven worden automatisch opnieuw gemaakt.
- **Geüploade bestanden** worden nooit overschreven. Een nieuw logo krijgt een nieuwe bestandsnaam, zodat de live pagina het oude logo houdt tot er gepubliceerd wordt.

## Schermen

**Iedereen**: inloggen, wachtwoord vergeten, wachtwoord instellen via de uitnodigingslink.

**Bedrijfsbeheerder**
- **Startscherm**:
  - status (gepubliceerd op …, wel of geen wijzigingen klaar);
  - takenlijst ("Alleo: aanmeldlink ontbreekt", "Nog geen logo");
  - de drie links, met kopieerknop;
  - de knop "Publiceren".
- **Stap 1, VDKnaken**:
  - kaarten met logo, naam en korte omschrijving, plus een vinkje;
  - de standaardtekst is uit te klappen en duidelijk gemarkeerd als "centraal vastgesteld, niet aan te passen";
  - onder elke aangevinkte knaak het formulier met de bedrijfsvelden en een status (compleet / ontbreekt iets).
- **Stap 2, eigen voorwaarden**: een lijst plus de knop "Eigen arbeidsvoorwaarde toevoegen" (naam, omschrijving, afbeelding, link).
- **Stap 3, volgorde**: één lijst met sleepgreep, knoppen omhoog/omlaag, een schakelaar actief/inactief en een schakelaar "tonen bij werving".
- **Stap 4, huisstijl**:
  - logo uploaden;
  - drie kleurkiezers met hun rol ("Hoofdkleur: kopbalk en knoppen");
  - een live mini-voorbeeld met uitleg over het contrast;
  - welkomsttekst, contactregel en vacaturelink.
- **Stap 5, bekijken en publiceren**:
  - voorbeeld in drie tabbladen (Medewerkers / Werving / PDF), met de balk "Voorbeeld, nog niet gepubliceerd";
  - een samenvatting van wat er overgeslagen wordt en waarom;
  - de knop "Publiceren".
- **Instellingen**: paginawachtwoord aan of uit, "medewerkerslink vernieuwen" (met waarschuwing), beheerders van dit bedrijf (collega uitnodigen of verwijderen).

**Publiek**
- **Medewerkerspagina** (`…/m/<willekeurige-sleutel>/`), eerst voor mobiel ontworpen:
  - kopbalk in de hoofdkleur met logo en welkomsttekst;
  - bij veel voorwaarden een korte inhoudsopgave;
  - per voorwaarde een kaart met logo, teksten, knoppen, en codes met een kopieerknop;
  - een contactregel onderaan.
- **Wachtwoordscherm**, als het bedrijf dat heeft ingesteld.
- **Wervingspagina** (`…/werken-bij/<bedrijfsnaam>/`): dezelfde opbouw zonder links, codes en aanmeldknoppen. Wel een knop naar de vacatures (als ingesteld) en een knop "Download als PDF".
- **PDF**, A4 en ontworpen voor print:
  - bovenaan een band in de huisstijl met logo en titel;
  - de voorwaarden als verzorgde blokken in twee kolommen;
  - onderaan een QR-code naar de wervingspagina met "Scan voor meer informatie", en paginanummers.

**Superbeheerder (portaal, stap 9)**
- **Overzicht**: kerncijfers (bedrijven, gepubliceerd, open taken, knaken die binnen 60 dagen aflopen) en een tabel met alle bedrijven (status, aantal voorwaarden, open taken, weergaven deze maand).
- **Bedrijf**:
  - welke VDKnaken live en welke in concept;
  - open taken;
  - tellers per maand (12 maanden);
  - beheerders (uitnodigen, resetlink sturen, deactiveren);
  - links naar de pagina's.
- **VDKnaken**: een lijst met adoptie ("31 van 50 bedrijven") en einddatum-badges.
- **VDKnaak bewerken**:
  - teksten, logo, centrale link en code, einddatum, actief;
  - velden toevoegen, verplaatsen en instellen;
  - voorbeeld;
  - lijst van bedrijven die de knaak gebruiken.
- **Bedrijf aanmaken**: naam plus e-mailadres van de eerste beheerder. De uitnodiging gaat automatisch.
- **Superbeheerders**: beheren wie er superbeheerder is.
- **Export naar Excel**, met drie tabbladen:
  - Bedrijven;
  - Adoptie (bedrijf × VDKnaak);
  - Weergaven per maand.

## Beveiliging en AVG

- **Afscherming per bedrijf**:
  - elke bedrijfspagina loopt via één controle ("is deze gebruiker lid van dit bedrijf?");
  - alle gegevens worden via het bedrijf opgehaald, nooit los op nummer;
  - een geautomatiseerde test loopt **alle** bedrijfs-URL's langs en controleert dat een beheerder van bedrijf A niets van bedrijf B kan zien of wijzigen, ook niet van URL's die later worden toegevoegd.
- **Wachtwoorden en accounts**:
  - Argon2-versleuteling en Nederlandse wachtwoordeisen;
  - resetlinks zijn eenmalig en verlopen;
  - blokkade na herhaalde mislukte pogingen;
  - beveiligde cookies en CSRF-bescherming (standaard in Django).
- **Medewerkerspagina**:
  - onraadbare sleutel (±128 bits);
  - `noindex` in zowel een header als een meta-tag;
  - `Referrer-Policy: no-referrer`, zodat de link niet meelekt naar leveranciers;
  - de pagina wordt niet opgeslagen in gedeelde caches;
  - optioneel een wachtwoord (versleuteld, met pogingenlimiet);
  - de link is te vernieuwen.
- **Uploads**:
  - alleen PNG, JPG en WebP (geen SVG, omdat daar scripts in kunnen zitten) en PDF bij bestandsvelden;
  - grootte beperkt en afbeeldingen verkleind;
  - willekeurige bestandsnamen.
- **AVG**:
  - alleen bedrijfsgegevens en contactgegevens van beheerders;
  - geen cookies voor bezoekers behalve het sessiecookie van het paginawachtwoord, dus geen cookiebanner;
  - hosting in de EU met een verwerkersovereenkomst.

## Bouwstappen

Na elke stap is er iets te zien en uit te proberen. Ik laat per stap weten wat je kunt testen.

| # | Stap | Wat je daarna kunt uitproberen |
|---|---|---|
| 0 | Werkplek, projectbasis en tekstbestanden. Met Mailpit als testpostvak, zodat je alle uitgaande mails in de browser ziet. | De app opent in de Codespace, met de eerste Nederlandse teksten uit het `.po`-bestand |
| 1 | Accounts: inloggen, uitnodigen, wachtwoord vergeten, lidmaatschappen, test voor afscherming per bedrijf. Acht voorbeeld-VDKnaken als startdata. | Via Django-beheer een bedrijf en beheerder aanmaken, de uitnodiging openen in Mailpit, inloggen |
| 2 | Stap 1 van de editor: VDKnaken aanvinken, velden invullen, takenlijst | Knaken aanvinken en zien hoe taken verschijnen en verdwijnen |
| 3 | Publiceren en de medewerkerspagina (nog met standaardstijl), plus de statusbalk | Publiceren, de medewerkerslink openen, een centrale tekst aanpassen en zien dat die doorwerkt |
| 4 | **Testomgeving online** (hosting, database, mail) | De medewerkerspagina op je eigen telefoon bekijken en een collega laten meekijken |
| 5 | Eigen voorwaarden, volgorde (slepen en toetsenbord), actief/inactief | Een eigen regeling toevoegen en bovenaan zetten |
| 6 | Huisstijl met contrastbewaking, wizard voor de eerste keer, voorbeeldscherm, paginawachtwoord, link vernieuwen, collega uitnodigen | Een pagina volledig in eigen stijl, en proberen hem onleesbaar te maken (lukt niet) |
| 7 | Wervingspagina en tellers | De wervingspagina bekijken, controleren dat er geen codes op staan, tellers zien oplopen |
| 8 | **PDF met QR-code**, eerst ontwerp en dan afwerking | De PDF downloaden, afdrukken en de QR scannen met je telefoon |
| 9 | Superbeheerdersportaal: overzicht, bedrijven, VDKnaken-editor, adoptie, tellers, accounts, Excel-export | Een VDKnaak aanmaken met eigen velden, zonder code; exporteren |
| 10 | Einddatummeldingen (geplande taak) en klaar maken voor livegang | Een knaak laten verlopen in de test en de mails in het postvak zien |

## Controle en testen

- **Geautomatiseerde tests** (`python manage.py test`), die draaien na elke stap:
  - afscherming per bedrijf over alle bedrijfs-URL's;
  - een testcode (bijvoorbeeld `GEHEIM-TEST-123`) staat wél op de medewerkerspagina en **niet** in de HTML van de wervingspagina en niet in de tekst van de PDF;
  - verlopen of gedeactiveerde VDKnaken verdwijnen, en verschijnen weer na verlengen;
  - een centrale tekstwijziging is zichtbaar zonder opnieuw te publiceren;
  - een onvolledige nieuwe knaak wordt overgeslagen, een al gepubliceerde knaak met een nieuw verplicht veld blijft staan;
  - contrastberekening: elke kleurinvoer levert tekst van minimaal 4,5:1 op;
  - de medewerkerspagina stuurt `noindex` en `no-referrer` mee, de wervingspagina niet;
  - paginawachtwoord en pogingenlimiet;
  - tellers tellen bots en voorbeeldweergaven niet mee.
- **Handmatig per stap**:
  - uitproberen in de Codespace;
  - vanaf stap 4 op een echte telefoon;
  - toetsenbordcontrole: alles bereikbaar met Tab en Enter, zichtbare focus;
  - automatische toegankelijkheidscontrole (axe) op de publieke pagina's.
- **PDF**: afdrukken op A4, de QR scannen en controleren op pagina-afbreking bij veel voorwaarden.

## Nog nodig vóór livegang (niet nu)

- **Domein**, bijvoorbeeld `arbeidsvoorwaarden.vdkgroep.nl` via IT.
- **Maildienst** voor uitnodigingen, resets en meldingen, met DNS-instellingen (SPF en DKIM) door IT.
- **Echte inhoud**: teksten en logo's van de acht VDKnaken.
- **Accounts op naam van VDK**: GitHub-organisatie, hosting, maildienst, plus een verwerkersovereenkomst met de hoster.
- **Eindcontrole** op beveiliging en toegankelijkheid.

## Later (bewust buiten de eerste versie)

- Duitse taal.
- Een oude versie terugzetten.
- Een "canteenposter"-PDF met QR naar de medewerkerspagina.
- Bedrijven automatisch laten weten dat er een nieuwe VDKnaak beschikbaar is.
