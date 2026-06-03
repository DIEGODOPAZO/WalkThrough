# One Piece

This is a One Piece-themed CTF machine. In this case, the sections of this CTF will be divided based on the questions that must be answered:

## First Question: What is the name of the tree that contains the 1st Road Poneglyph?

I initially ran Nmap and discovered the following:

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
|      At session startup, client count was 1
|      vsFTPd 3.0.3 - secure, fast, stable
|_End of status
| ftp-anon: Anonymous FTP login allowed (FTP code 230)
|_-rw-r--r--    1 0        0             187 Jul 26  2020 welcome.txt
22/tcp open  ssh     OpenSSH 7.6p1 Ubuntu 4ubuntu0.3 (Ubuntu Linux; protocol 2.0)
80/tcp open  http    Apache httpd 2.4.29 ((Ubuntu))
```

The first thing I did was inspect the HTML code of the page and found the following clue:

![Web_page_clue](screenshots/clue_in_web_page.png)

I decoded it from base32 and then from base64 and it gave me the following clue:
`Nami ensures there are precisely 3472 possible places where she could have lost it.`

Then I inspected the FTP server and downloaded all its contents:

```bash
wget -m --no-passive ftp://anonymous:anonymous@10.10.125.150
```

Among the downloaded files, two were lore files (just One Piece-related content with no relevance for the CTF), but two others were important:

- A directory called `.the_whale_tree`, which is the answer to the first question.
- A file named `.road_poneglyph.jpeg`, from which I extracted its content using Steghide. It gave me the first Poneglyph content encoded (it is impossible to crack it now—I need the other three to understand the meaning).

## Second Question: What is the name of the 1st pirate you meet navigating the Apache Sea?

The THM platform gives the following hint: `Only Sea, It's Not Terrible`. This suggests I should try OSINT.

I searched: 

`"logpose" list THM` 

> I used this because of Nami’s clue—we need a logpose and we can assume a list, based on the number of possible locations.

This yielded the following result:

![Osint](screenshots/repository_log_pose.png)

In this repository, I found a list that I used as a dictionary for `ffuf`.

```bash
ffuf -u http://10.10.125.150/FUZZ -w logpose.txt -e .php,.html,.txt
```

I found the page: `dr3ssr0s4.html`.

In the page, we see the name of the pirate: **Donquixote Doflamingo**, which is the answer to this question.

## Third Question: What is the name of the 2nd island you reach navigating the Apache Sea?

To continue, I checked the image at the bottom of the page, but as its name suggested, it was a rabbit hole.

Inspecting the source code and the CSS, I found a URL to another image:

`../king_kong_gun.jpg`

Using `exiftool`, I discovered another image URL:

![King_kong](screenshots/dofi_ko_image.png)

New image: `/ko.jpg`

Analyzing this image with `strings`, I found the route to the next island:

![KO](screenshots/ko_clue.png)

The route is: `/wh0l3_c4k3.php`

The answer: **Whole Cake**

## Fourth Question: What is the name of the friend you meet navigating the Apache Sea?

On the page, there is a form. Inspecting the request in Burp Suite, I found a cookie: `NoCakeForYou`.

Changing the value of this cookie makes the webpage return the third Poneglyph and the route to the next island: `/r4nd0m.html`.

![Second_p](screenshots/second_poneglyph.png)

On the newly discovered page, the answer to the fourth question is: **Buggy the Clown**

## Fifth Question: What is the name of the 2nd Emperor you meet navigating the Apache Sea?

There are two games on this page. Inspecting the JavaScript for the brainteaser game, I found the logpose to the next island hardcoded: `/0n1g4sh1m4.php`

Visiting this path reveals the answer: **Kaido of the Beasts**

## Sixth Question: What is the hidden message of the 4 Road Poneglyphs?

There are two paths: one involving file upload (discarded, as there was no upload route), and another involving brute force, as hinted in the lore.

![Kaido_img](screenshots/bruteforce_kaido_image_clue.png)

The file `kaido.jpeg` stood out (since all others were .png), so I used Stegcracker:

```bash
stegcracker kaido.jpeg /usr/share/wordlists/rockyou.txt 
```

![Kaido_img_cracked](screenshots/kaido_image_cracked.png)

![Kaido_img_cracked_content](screenshots/contenit_image_kaido.png)

The password was `imabeast`. The contents revealed a user: `K1ng_0f_th3_B3@sts`.

I used Hydra to brute-force the password:

```bash
hydra -l K1ng_0f_th3_B3@sts -P /usr/share/wordlists/rockyou.txt 10.10.125.150 http-post-form "/0n1g4sh1m4.php:user=^USER^&password=^PASS^&submit_creds=Login:ERROR" -t 64 -v
```

The password: `thebeast`

Upon login, I saw the third Poneglyph and a clue to the final one at `/unspecified`.

![Third_p](screenshots/third_poneglyph.png)

I combined all the Poneglyph contents in CyberChef and decoded them:

![Pon_res](screenshots/poneglyphs_result.png)

Answer: `M0nk3y_D_7uffy:1_w1ll_b3_th3_p1r@t3_k1ng!`

## Seventh Question: Who is on Laugh Tale at the same time as Luffy?

Using the previous answer as SSH credentials, I found the answer (Marshall D. Teach) in a file in the user directory:

![Rival](screenshots/ssh_rival.png)

## Eighth Question: What allowed Luffy to win the fight?

Using the file `/usr/bin/gomugomunooo_king_kobraaa`, I was able to obtain credentials for the other user: `7uffy_vs_T3@ch:Wh0_w1ll_b3_th3_k1ng?`

![priv_esc](screenshots/priv_esc.png)

The answer was in a file in the new user’s home directory: **willpower**

## What is the One Piece?

To gain root access, I used `sudo -l`:

![sudo-l](screenshots/sudo-l.png)

I could run `/usr/local/bin/less` as sudo, but it was altered to print a message.

I checked it—it was likely a bash script:

![less_info](screenshots/less_no_binario_prueba.png)

I had **write** permissions but not **read**. I couldn’t overwrite it, so I appended a payload:

```bash
echo -e '
if [ "$EUID" -eq 0 ]; then
  /bin/bash
fi' >> /usr/local/bin/less
```

Executing `less` gave me root access:

![root](screenshots/root.png)

To find the One Piece, I ran:

```bash
grep -iRl "One Piece" /usr 2>/dev/null
```

![OnePiece](screenshots/one_piece.png)


The One Piece was: *S3cr3ts_0f_tH3_W0rlD_&_0f_Th3_P@st$*