import json
import re
from io import BytesIO

import pandas as pd
import requests
from PIL import Image, ImageOps

import os
from dotenv import load_dotenv


CSV_FILE = "Eduskuntavaalit_Perusraportti.csv"
OUTPUT_FILE = "candidates_import.json"

ELECTION_EXTERNAL_ID = "eduskuntavaalit"

load_dotenv()

STRAPI_URL = os.getenv("STRAPI_URL", "http://localhost:1337")
LOGIN_EMAIL = os.getenv("STRAPI_LOGIN_EMAIL")
LOGIN_PASSWORD = os.getenv("STRAPI_LOGIN_PASSWORD")
IMAGE_COLUMN = "Lisää tähän kuvasi"

PARTY_MAP = {
    "Keskusta": "keskusta",
    "Kokoomus": "kokoomus",
    "Kristillisdemokraatit": "kristillisdemokraatit",
    "Liike Nyt": "liike-nyt",
    "Perussuomalaiset": "perussuomalaiset",
    "RKP": "rkp",
    "SDP": "sdp",
    "Vasemmistoliitto": "vasemmistoliitto",
    "Vihreät": "vihreat"
}   

CONSTITUENCY_MAP = {
    "Helsinki": "01-helsinki",
    "Uusimaa": "02-uusimaa",
    "Varsinais-Suomi": "03-varsinais-suomi",
    "Satakunta": "04-satakunta",
    "Ahvenanmaa": "05-ahvenanmaa",
    "Häme": "06-hame",
    "Pirkanmaa": "07-pirkanmaa",
    "Kaakkois-Suomi": "08-kaakkois-suomi",
    "Savo-Karjala": "09-savo-karjala",
    "Vaasa": "10-vaasa",
    "Keski-Suomi": "11-keski-suomi",
    "Oulu": "12-oulu",
    "Lappi": "13-lappi"
}
QUESTION_MAP = {
    "Hyvinvointialueiden tulee vähentää ostopalveluiden käyttöä ja tuottaa palvelut pääosin itse.": {
        "externalId": "q-ostopalvelut",
        "infoColumn": "Vapaaehtoiset perustelut äänestäjälle"
    },
    "Yritysten yhteisöveron alentamisesta tulee luopua, jos sillä voidaan välttää sosiaalihuollon leikkauksia.": {
        "externalId": "q-yhteisovero-sosiaalihuolto",
        "infoColumn": "Vapaaehtoiset perustelut äänestäjälle.1"
    },
    "Hyvinvointialueiden pitäisi saada enemmän rahoitusta, jos alueella on paljon köyhyyttä, työttömyyttä ja sosiaalipalvelujen tarvetta.": {
        "externalId": "q-rahoitus-sosiaalinen-tarve",
        "infoColumn": "Vapaaehtoiset perustelut äänestäjälle.2"
    },
    "Nykyinen työntekijän oikeussuoja epäkohdasta ilmoittamistilanteissa on riittävä.": {
        "externalId": "q-oikeussuoja-epakohdat",
        "infoColumn": "Vapaaehtoiset perustelut äänestäjälle.3"
    },
    "Sosiaalihuollon ammattilaisten tulee voida nykyistä laajemmin toimia toistensa tehtävissä.": {
        "externalId": "q-ammattiryhmien-tehtavat",
        "infoColumn": "Vapaaehtoiset perustelut äänestäjälle.4"
    },
    "Sosiaalihuollossa tulee lailla rajoittaa, kuinka monta asiakasta yhdellä sosiaalityöntekijällä voi olla.": {
        "externalId": "q-asiakasmitoitus",
        "infoColumn": "Vapaaehtoiset perustelut äänestäjälle.5"
    },
    "Sosionomi (YAMK) -tutkinnon tulee antaa kelpoisuus päiväkodin johtajan tehtävään ilman erillisiä 60 opintopisteen kasvatustieteen lisäopintoja.": {
        "externalId": "q-yamk-paivakodin-johtaja",
        "infoColumn": "Vapaaehtoiset perustelut äänestäjälle.6"
    },
    "Sosiaalihuollon ammattilaisilla tulee olla nykyistä enemmän harkintavaltaa asiakkaan palveluista päätettäessä, vaikka se vähentäisi hyvinvointialueiden mahdollisuuksia ohjata kustannuksia.": {
        "externalId": "q-ammatillinen-harkintavalta",
        "infoColumn": "Vapaaehtoiset perustelut äänestäjälle.7"
    },
    "Lapsia tulee ohjata nykyistä useammin lastensuojelun sijasta sosiaalihuollon palveluihin.": {
        "externalId": "q-lastensuojelusta-sosiaalihuoltoon",
        "infoColumn": "Vapaaehtoiset perustelut äänestäjälle.8"
    },
    "Alle 15-vuotias rikoksesta epäilty tulee voida ottaa poliisin säilöön enintään 72 tunniksi esitutkinnan turvaamiseksi.": {
        "externalId": "q-alle15-sailoonotto",
        "infoColumn": "Vapaaehtoiset perustelut äänestäjälle.9"
    },

    # Taustakysymykset
    "Kotikunta": {
        "externalId": "q-kotikunta",
        "infoColumn": None
    },
    "Ammatti": {
        "externalId": "q-ammatti",
        "infoColumn": None
    },
    "Koulutus": {
        "externalId": "q-koulutus",
        "infoColumn": None
    },
    "Esittely": {
        "externalId": "q-esittely",
        "infoColumn": None
    },
    "Vaalilupauksesi": {
        "externalId": "q-vaalilupaus",
        "infoColumn": None
    },
    "Ikä:HUOM! Ikäsi vaalipäivänä 18.4.2027": {
        "externalId": "q-ika",
        "infoColumn": None
    },
    "Vaaliteemat": {
        "externalId": "q-vaaliteemat",
        "infoColumn": None
    }
}

def clean_text(value):
    if pd.isna(value):
        return None
    text = str(value).replace("\xa0", " ").strip()
    return text if text else None


def clean_answer_value(value):
    if pd.isna(value):
        return None
    if isinstance(value, float) and value.is_integer():
        return str(int(value))
    return str(value).strip()


def make_external_id(first_name, last_name):
    raw = f"{first_name}-{last_name}".lower()
    raw = raw.replace("ä", "a").replace("ö", "o").replace("å", "a")
    raw = re.sub(r"[^a-z0-9]+", "-", raw)
    return raw.strip("-")


def parse_webropol_time(value):
    if pd.isna(value):
        return None
    dt = pd.to_datetime(value, dayfirst=True)
    return dt.isoformat() + "Z"


def get_jwt():
    response = requests.post(
        f"{STRAPI_URL}/api/auth/local",
        json={
            "identifier": LOGIN_EMAIL,
            "password": LOGIN_PASSWORD
        },
        timeout=20
    )

    print("Login status:", response.status_code)

    if response.status_code != 200:
        print(response.text)
        raise Exception("Kirjautuminen Strapiin epäonnistui")

    return response.json()["jwt"]


def download_and_fix_image(image_url):
    image_response = requests.get(image_url, allow_redirects=True, timeout=30)

    print("Download status:", image_response.status_code)
    print("Content-Type:", image_response.headers.get("content-type"))
    print("Content-Disposition:", image_response.headers.get("content-disposition"))

    if image_response.status_code != 200:
        print(image_response.text)
        raise Exception(f"Kuvan lataus Webropolista epäonnistui: {image_url}")

    image = Image.open(BytesIO(image_response.content))

    # Korjaa puhelimella otettujen kuvien EXIF-orientaation
    image = ImageOps.exif_transpose(image)

    # Varmistetaan, että kuva on uploadiin sopivassa RGB-muodossa
    if image.mode not in ("RGB", "L"):
        image = image.convert("RGB")

    output = BytesIO()
    image.save(output, format="JPEG", quality=90)
    output.seek(0)

    return output


def upload_image_from_url(image_url, jwt, filename):
    if not image_url:
        return None

    fixed_image = download_and_fix_image(image_url)

    headers = {
        "Authorization": f"Bearer {jwt}"
    }

    files = {
        "files": (filename, fixed_image, "image/jpeg")
    }

    upload_response = requests.post(
        f"{STRAPI_URL}/api/upload",
        headers=headers,
        files=files,
        timeout=60
    )

    print("Upload status:", upload_response.status_code)

    if upload_response.status_code != 201:
        print(upload_response.text)
        raise Exception(f"Kuvan upload Strapiin epäonnistui: {filename}")

    uploaded_file = upload_response.json()[0]

    print("Upload onnistui")
    print("Image id:", uploaded_file["id"])
    print("Image documentId:", uploaded_file["documentId"])
    print("Image url:", uploaded_file["url"])

    return uploaded_file["id"]


df = pd.read_csv(CSV_FILE, encoding="utf-8", sep=";")
df.columns = df.columns.str.strip()

df.columns = df.columns.str.replace("\xa0", " ", regex=False)
df.columns = df.columns.str.replace(r":$", "", regex=True)

missing_columns = []

for question_column, config in QUESTION_MAP.items():
    if question_column not in df.columns:
        missing_columns.append(question_column)

if missing_columns:
    print("CSV:stä puuttuu seuraavia kysymyssarakkeita, ohitetaan ne tässä ajossa:")
    for column in missing_columns:
        print("-", repr(column))
    print("\nCSV:n sarakkeet ovat:")
    for column in df.columns:
        print("-", repr(column))
    print("\nJatketaan importtia CSV:ssä olevilla sarakkeilla. Tarkista, että tämä on tarkoituksellinen osittaispäivitys.")

jwt = get_jwt()

candidates = []
nominations = []

for _, row in df.iterrows():
    first_name = clean_text(row["Etunimi"])
    last_name = clean_text(row["Sukunimi"])
    election_symbol = clean_answer_value(row["Ehdokasnumerosi"])
    party_name = clean_text(row.get("Puolue"))
    constituency_name = clean_text(row.get("Vaalipiiri"))

    party = PARTY_MAP[party_name] if party_name else None
    constituency = CONSTITUENCY_MAP[constituency_name] if constituency_name else None

    candidate_external_id = make_external_id(first_name, last_name)

    answers = {}

    for question_column, config in QUESTION_MAP.items():
        if question_column not in row.index:
            continue

        if config["externalId"] == "q-ika":
            answer_value = None if pd.isna(row[question_column]) else int(row[question_column])
        else:
            answer_value = clean_answer_value(row[question_column])

        if answer_value is None:
            continue

        answer = {
            "value": answer_value
        }

        info_column = config.get("infoColumn")

        if info_column and info_column in row.index:
            info_text = clean_text(row[info_column])
            if info_text:
                answer["info"] = {
                    "fi": info_text
                }

        answers[config["externalId"]] = answer

    image_url = clean_text(row.get(IMAGE_COLUMN))
    image_id = None

    if image_url:
        image_filename = f"{candidate_external_id}.jpg"
        image_id = upload_image_from_url(image_url, jwt, image_filename)
        print(f"Kuva ladattu ehdokkaalle {first_name} {last_name}: image id {image_id}")

    candidate = {
        "externalId": candidate_external_id,
        "firstName": first_name,
        "lastName": last_name,
        "termsOfUseAccepted": parse_webropol_time(row["Vastausaika"]),
        "answersByExternalId": answers
    }

    if image_id:
        candidate["image"] = image_id

    candidates.append(candidate)

    # Osittaispäivityksissä CSV:ssä ei välttämättä ole Puolue- ja Vaalipiiri-sarakkeita.
    # Tällöin päivitetään vain Candidate ja jätetään Nomination luomatta/päivittämättä.
    if party and constituency:
        nomination = {
            "externalId": f"{ELECTION_EXTERNAL_ID}-{constituency}-{candidate_external_id}",
            "electionSymbol": election_symbol,
            "electionRound": 1,
            "unconfirmed": False,
            "candidate": {
                "externalId": candidate_external_id
            },
            "election": {
                "externalId": ELECTION_EXTERNAL_ID
            },
            "constituency": {
                "externalId": constituency
            },
            "party": {
                "externalId": party
            }
        }

        nominations.append(nomination)


import_data = {
    "candidates": candidates,
    "nominations": nominations
}

with open(OUTPUT_FILE, "w", encoding="utf-8") as file:
    json.dump(import_data, file, ensure_ascii=False, indent=2)

print(f"Luotu tiedosto: {OUTPUT_FILE}")
print(f"Ehdokkaita: {len(candidates)}")
print(f"Nominationeja: {len(nominations)}")