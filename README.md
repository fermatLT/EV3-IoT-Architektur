# EV3-IoT-Architektur
Eine praktische Implementierung eines Lego EV3 Roboters in eine IoT Umgebung mit der Verknüpfung zu einem Content Delivery Network

<h1>Anforderungen</h1>
Zur Umsetzung der IoT Architektur sind folgende Elemente erforderlich.

<h3> Bestandteile für den LEGO EV3 </h3>
<ul>
  <li> LEGO EV3 </li>
  <li> Eine microSD oder microSDHC Karte. MicroSDXC wird vom EV3 nicht unterstützt. Die maximale Speicherkapazität darf 32 GB nicht überschreiten. In diesem Tutorial wurde eine 16GB microSDHC Karte benutzt. </li>
  <li> Image File von ev3dev https://www.ev3dev.org/downloads/ </li>
  <li> WIFI USB Adapter. Eine Liste mit unterstützen Adpatern finden Sie hier https://github.com/ev3dev/ev3dev/wiki/USB-Wi-Fi-Dongles
    In diesem Tutorial wurde ein TP-Link WIFI Adapter verwendet. https://www.tp-link.com/de/home-networking/adapter/tl-wn722n/ </li>
  <li>LEGO Mindstorms RFID Reader https://www.generationrobots.com/de/403699-rfid-chip-leser-mit-einem-satz-chips-fur-lego-mindstorms-nxt-ev3.html </li>
  <li> Eine Möglichkeit mit dem EV3 zu kommunizieren. </li>
  <ul>
    <li> USB Kabel </li>
    <li> WIFI </li>
    <li> Ethernet Adapter </li>
    <li> Bluetooth </li>
  </ul>
 </ul>
  Eine Anleitung zur Erstellung einer bootfähigen SD Karte für den EV3 finden Sie hier.
   https://www.ev3dev.org/docs/getting-started/
 <h3> Bestandteile für den Raspberry Pi</h3>
<ul>
  <li> Raspberry Pi (In diesem Fall wurde ein Model 4b verwendet) </li>
  <li> Eine microSD Karte mit mindestens 8GB Speicherkapazität </li>
  <li> Image File des aktuellen Raspbian OS (In diesem Fall wurde Bullseye Version 11 verwendet) </li>
  <li> Ein Netzteil mit micro USB Kabel </li>
  
  Eine Anleitung, um den Raspberry Pi startklar zu machen, finden Sie hier. https://projects.raspberrypi.org/de-DE/projects/raspberry-pi-setting-up/0
 </ul>
 
<h3> Kommunikation zwischen dem Raspberry Pi, dem EV3 und dem Computer über SSH </h3>
PuTTY ermöglicht es einem, schnell und reibungslos eine Verbindung zu sowohl dem EV3 und dem Raspberry Pi herzustellen https://www.putty.org/

<h3> IDE für den EV3 </h3>

Nach der Installation des ev3dev Images auf dem EV3, lassen sich nun Programme in diversen Progammiersprachen schreiben, z.B. Python, Java, C++ und C. Eine vollständige Liste aller möglichen Sprachen finden Sie unter https://www.ev3dev.org/docs/programming-languages/.
Als IDE eignet sich Visual Studio Code mit der Extension LEGO MINDSTORMS EV3 MIcroPython, falls man in Python bzw. MicroPython schreiben möchte. Alle verfügbaren Programme in diesem Repo sind in Python geschrieben. 
