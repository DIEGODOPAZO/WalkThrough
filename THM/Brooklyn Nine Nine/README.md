# Brooklyn Nine Nine - CTF Walkthrough

---

## Enumeration

Initial reconnaissance was carried out using **Nmap**, which revealed the following open ports and services:

```
PORT   STATE SERVICE VERSION
21/tcp open  ftp     vsftpd 3.0.3
| ftp-syst: 
|   STAT: 
| FTP server status:
|      Connected to ::ffff:10.23.124.231
|      Logged in as ftp
|      TYPE: ASCII
|      No session bandwidth limit
|      Session timeout in seconds is 300
|      Control connection is plain text
|      Data connections will be plain text
|      At session startup, client count was 4
|      vsFTPd 3.0.3 - secure, fast, stable
|_End of status
| ftp-anon: Anonymous FTP login allowed (FTP code 230)
|_-rw-r--r--    1 0        0             119 May 17  2020 note_to_jake.txt
22/tcp open  ssh     OpenSSH 7.6p1 Ubuntu 4ubuntu0.3 (Ubuntu Linux; protocol 2.0)
| ssh-hostkey: 
|   2048 16:7f:2f:fe:0f:ba:98:77:7d:6d:3e:b6:25:72:c6:a3 (RSA)
|   256 2e:3b:61:59:4b:c4:29:b5:e8:58:39:6f:6f:e9:9b:ee (ECDSA)
|_  256 ab:16:2e:79:20:3c:9b:0a:01:9c:8c:44:26:01:58:04 (ED25519)
80/tcp open  http    Apache httpd 2.4.29 ((Ubuntu))
|_http-title: Site doesn't have a title (text/html).
|_http-server-header: Apache/2.4.29 (Ubuntu)
```

The system appears to be running Linux kernel 4.15 and is accessible over HTTP, SSH, and FTP.

---

### Web Service Enumeration

A web server is running on port 80, but after running **FFUF** for content discovery, no useful endpoints were found.

---

### FTP Access

Anonymous FTP login is allowed. Using `wget`, I mirrored the FTP content:

```bash
wget -m --no-passive ftp://anonymous:anonymous@10.10.139.57
```

This yielded a file named `note_to_jake.txt`, which included a message advising user `jake` to change his weak password — a good hint for a brute-force attempt.

---

## Gaining Shell Access

To gain shell access, I performed a **brute-force attack** against the SSH service for the user `jake` using **Hydra**.

![Shell_passwd](screenshots/shell_access.png)

Once valid credentials were obtained, I successfully logged in via SSH and found the **user flag** in another user's home directory:

![User_flag](screenshots/user_txt.png)

---

## Privilege Escalation to Root

While checking `sudo -l`, I found that the `less` command could be run as root without a password. Since `less` allows reading any file, I used it to open the root flag:

```bash
sudo less /root/root.txt
```

![Root_flag](screenshots/root_flag.png)

---

## Summary

- **Initial Access**: Anonymous FTP ➜ `note_to_jake.txt`
- **Credentials**: Brute-forced SSH login for `jake`
- **Privilege Escalation**: `less` command allowed with `sudo`g

---