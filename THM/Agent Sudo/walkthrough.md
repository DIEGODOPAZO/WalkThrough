# Agent Sudo - Walkthrough

---

## Enumeration

Initial service scan using **Nmap** revealed the following open ports:

```
PORT   STATE SERVICE
21/tcp open  ftp
22/tcp open  ssh
80/tcp open  http
```

I also used `ffuf` to look for hidden directories, but no useful results were found.

![Web Page](screenshots/Web_page.png)

While browsing the website, I changed the `User-Agent` header to `Agent R` and received a different HTTP response. The page hinted at there being 25 agents (same as letters in the alphabet), so I used **Burp Suite Intruder** to test all letters as the `User-Agent`. The letter **C** returned something interesting.

![Burp Suite](screenshots/burpsuite.png)

Navigating to `agent_C_attention.php` revealed the following content:

![Agent C Attention](screenshots/agent_C_attention_php.png)

I then attempted brute-force attacks on both SSH and FTP. Only the **FTP** credentials were successfully cracked:

![Hydra](screenshots/hydra.png)

- **Username:** `chris`  
- **Password:** `crystal`

---

## FTP Access

Using the FTP credentials, I downloaded the contents with:

```bash
wget -m --no-passive ftp://chris:crystal@10.10.46.190
```

Two images were retrieved. Using `exiftool`, one image appeared to contain metadata suggesting hidden content. I used `binwalk` to extract embedded files:

```bash
binwalk --extract cutie.png
```

This revealed a **password-protected ZIP file**. I cracked it using **John the Ripper**:

```bash
zip2john 8702.zip > hash.txt
john hash.txt
```

- **Password found:** `alien`

After unzipping, a `.txt` file was found with the word `Area51` encoded in Base64.

Using the second image (`cute-alien.jpg`), I extracted hidden data with `steghide` using the passphrase `Area51`:

```bash
steghide extract -sf cute-alien.jpg
```

This gave me new **SSH credentials**:

- **Username:** `james`  
- **Password:** `hackerrules!`

---

## Privilege Escalation

After logging in via SSH as `james`, I checked `sudo -l` and found this:

```
(ALL, !root) /bin/bash
```

This suggests `james` can run `/bin/bash` as any user **except root** — an unusual configuration. Researching this led to a known **privilege escalation technique**.

Running the following gave root access:

```bash
sudo -u#-1 /bin/bash
```

>  This exploits the fact that `-1` is interpreted as UID 4294967295, which bypasses the `!root` restriction on some systems.

![Privilege Escalation](screenshots/priv_escalation.png)

---

**Root access achieved!**

Now retrieve the flag from `/root/root.txt`.

