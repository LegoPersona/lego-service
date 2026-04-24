from pathlib import Path
import requests


BASE_URL = "http://127.0.0.1:8004/persona"

PERSONA_PAYLOAD = {
    "persona": {
        "beard": "no_beard",
        "eyebrows": "black_round_eyebrows",
        "eyes": "brown_eyes",
        "hair": "bald_hair",
        "nose": "round_nose",
        "pants": "blue_pants",
        "shirt": "red_shirt",
    }
}


def test_generate():
    try:
        response = requests.post(f"{BASE_URL}/generate", json=PERSONA_PAYLOAD, timeout=10)
        print(f"[generate] Status: {response.status_code}")
        ldr_file = response.json()["ldr_file"]
        print("LDR file:")
        print(ldr_file)
        return ldr_file
    except requests.RequestException as exc:
        print(f"[generate] Error: {exc}")
        return None


def test_instructions(ldr_file: str):
    try:
        response = requests.post(
            f"{BASE_URL}/instructions",
            json={"ldr_file": ldr_file},
            timeout=60,
        )
        print(f"[instructions] Status: {response.status_code}")
        if response.status_code == 200:
            out_path = Path("instructions.pdf")
            out_path.write_bytes(response.content)
            print(f"PDF saved to {out_path}")
        else:
            print(response.text)
    except requests.RequestException as exc:
        print(f"[instructions] Error: {exc}")


def main():
    ldr_file = test_generate()
    if ldr_file:
        test_instructions(ldr_file)


if __name__ == "__main__":
    main()
