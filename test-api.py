import requests


API_URL = "http://127.0.0.1:8080/persona/generate"


def main() :
    payload = {
        "beard": "no_beard",
        "eyebrows": "black_round_eyebrows",
        "eyes": "brown_eyes",
        "hair": "bald_hair",
        "nose": "round_nose",
        "pants": "blue_pants",
        "shirt": "red_shirt",
    }

    try:
        response = requests.post(API_URL, json=payload, timeout=10)
        print(f"Status: {response.status_code}")
        print("LDR file:")
        print(response.json()['ldr_file'])
    except requests.RequestException as exc:
        print(exc)


if __name__ == "__main__":
    main()
