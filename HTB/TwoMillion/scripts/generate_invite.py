import base64
import codecs
import requests

BASE_URL = "http://2million.htb"


def make_invite_code():
    # Step 1: Get instructions for generating the invite code
    response = requests.post(
        f"{BASE_URL}/api/v1/invite/how/to/generate"
    )

    response.raise_for_status()

    data = response.json()["data"]["data"]
    encryption_type = response.json()["data"]["enctype"]

    print(f"[+] Encryption type: {encryption_type}")

    # Step 2: Decrypt the instructions
    if encryption_type == "ROT13":
        endpoint = codecs.decode(data, "rot_13")
    else:
        raise ValueError(f"Unsupported encryption type: {encryption_type}")

    print(f"[+] Decrypted instructions: {endpoint}")

    # The decrypted message contains the endpoint
    endpoint = endpoint.split(" ")[-1]

    # Step 3: Generate the invite code
    response = requests.post(
        f"{BASE_URL}{endpoint}"
    )

    response.raise_for_status()

    encoded_code = response.json()["data"]["code"]

    print(f"[+] Encoded invite code: {encoded_code}")

    # Step 4: Decode the Base64 invite code
    invite_code = base64.b64decode(encoded_code).decode()

    print(f"[+] Invite code: {invite_code}")

    return invite_code


if __name__ == "__main__":
    make_invite_code()