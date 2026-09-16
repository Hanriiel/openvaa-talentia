# Webropol-tuonti

Tämän kansion työkaluja käytetään ehdokastietojen siirtämiseen Webropolista Talentian vaalikoneeseen.

## Tuontiprosessi

Ehdokastiedot kerätään Webropol-lomakkeella ja viedään Webropolista CSV-tiedostona.

Tuontiprosessi:

**Webropol → CSV → Python-skripti → JSON → Strapi**

Python-skripti:

- lukee Webropolista ladatun CSV-aineiston
- muuntaa ehdokkaiden tiedot ja vastaukset OpenVAA:n käyttämään muotoon
- käsittelee Webropolin kautta toimitetut ehdokaskuvat ja lataa ne Strapiin
- muodostaa `candidates_import.json`-tiedoston

Muodostettu JSON-tiedosto tuodaan Strapiin OpenVAA Admin Toolsin Import Data -toiminnolla.

## Kansion tiedostot

- `create_import_json.py` – Webropol-aineiston muuntava Python-skripti
- `Kaynnista_tuonti.bat` – käynnistää tuontiskriptin Windowsissa
- `requirements.txt` – skriptin tarvitsemat Python-paketit
- `.env.example` – malli tarvittavista ympäristöasetuksista
- `vaalipiiri-import.json` – vaalipiirien tuontiaineisto
- `puolue-import.example.json` – esimerkki puolueiden tuontitiedoston rakenteesta
- `kategoria-import.example.json` – esimerkki kysymyskategorioiden tuontitiedoston rakenteesta
- `kysymys-import.example.json` – esimerkki kysymysten tuontitiedoston rakenteesta

## Uuden vaalin valmistelu

Ennen uuden vaalin ehdokasaineiston tuontia skriptin vaalikohtaiset asetukset on tarkistettava.

Tarkistettavia tietoja ovat ainakin:

- vaalin `externalId`
- mukana olevat puolueet ja niiden `externalId`-tunnisteet
- vaalipiirit ja niiden `externalId`-tunnisteet
- Webropol-lomakkeen kysymykset ja niitä vastaavat OpenVAA-kysymystunnisteet
- Webropol-exportin sarakkeiden nimet
- ehdokaskuvan sisältävän sarakkeen nimi

Nämä tarkistukset ja mahdolliset koodimuutokset kuuluvat tekniselle ylläpidolle. Tavallisen aineiston tuonnin yhteydessä skriptiä ei tarvitse muokata.

Puolueiden tuontia varten kansiossa on `puolue-import.example.json`, jota voidaan käyttää uuden vaalin puoluelistan pohjana. Vaalipiirit voidaan tuoda `vaalipiiri-import.json`-tiedostosta.

## Asennus

Skripti tarvitsee Python 3:n sekä `requirements.txt`-tiedostossa määritellyt Python-paketit.

Riippuvuudet asennetaan komennolla:

    pip install -r requirements.txt

Asennus tehdään käyttöönoton yhteydessä. Paketteja ei tarvitse asentaa uudelleen jokaisella tuontikerralla.

## Ympäristöasetukset

`.env.example` sisältää mallin tarvittavista asetuksista:

    STRAPI_URL=http://localhost:1337
    STRAPI_LOGIN_EMAIL=
    STRAPI_LOGIN_PASSWORD=

Kopioi `.env.example` nimelle `.env` ja täydennä käytettävän Strapi-ympäristön osoite ja kirjautumistiedot.

Skripti kirjautuu Strapiin ajon yhteydessä ja hakee tarvitsemansa JWT-tokenin automaattisesti. Tokenia ei tarvitse luoda tai tallentaa käsin.

## Ehdokasaineiston tuonti

Kun skripti ja ympäristö on valmisteltu kyseistä vaalia varten:

1. Vie ehdokkaiden vastaukset Webropolista CSV-muodossa.
2. Tallenna Webropolin muodostama `Eduskuntavaalit_Perusraportti.csv` tähän kansioon.
3. Käynnistä tuonti kaksoisklikkaamalla `Kaynnista_tuonti.bat`.
4. Skripti muodostaa `candidates_import.json`-tiedoston.
5. Tuo `candidates_import.json` Strapiin OpenVAA Admin Toolsin Import Data -toiminnolla.
6. Tarkista vaalikoneen käyttöliittymästä, että ehdokkaiden tiedot, vastaukset ja kuvat näkyvät oikein.

## Huomioitavaa

`candidates_import.json` on väliaikainen tuontitiedosto. Varsinainen lähtöaineisto on Webropolista ladattu CSV-aineisto, ja JSON voidaan muodostaa skriptillä uudelleen.

Jos Webropol-lomakkeen rakenne, puolueet, vaalipiirit tai OpenVAA:n tietomalli muuttuvat, tuontiskriptin asetukset ja mappaukset on tarkistettava ennen seuraavaa tuontia.