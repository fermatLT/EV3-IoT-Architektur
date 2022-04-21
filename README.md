# EV3-IoT-Architektur
Eine praktische Implementierung eines Lego EV3 Roboters in eine IoT Umgebung mit der Verknüpfung zu einem Content Delivery Network. In diesem Projekt kommuniziert ein LEGO EV3 Mindtsorms Roboter über MQTT mit einem Raspberry Pi und gibt Status Meldungen über Störungen. Die Webanwendung empfängt die Meldungen des EV3 und bezieht aus dem Content Delivery Network Lösungevorschläge und die nötigen Anleitungen, um die Störung zu beseitigen. Im folgenden wird beschrieben wie das Setup der IoT Umgebung aufgebaut ist und gibt zudem Anleitungen, um diese nachzubauen. 

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
Als IDE eignet sich Visual Studio Code mit der Extension LEGO MINDSTORMS EV3 MicroPython, falls man in Python bzw. MicroPython schreiben möchte. Alle verfügbaren Programme in diesem Repository sind in Python geschrieben. 


<h2> Veranschaulichung der IoT Architektur</h2>
 <img src="https://github.com/fermatLT/EV3-IoT-Architektur/blob/main/EV3-IoT.svg">
 
 <h2> Vorbereitung des Rasperry Pi</h2>
 <p>Nachdem der Raspberry Pi startklar ist, müssen voher ein Paar Pakete installiert werden und der Raspberry muss auf den aktuellen Stand gebracht werden.
 Mit diesen Befehlen brint man den Raspberry auf den aktuellen Stand und installiert die neuen Pakete.</p>
 
<pre> sudo apt-get update </br> sudo apt-get upgrade</pre>

<h3>Installation von Mosquitto MQTT</h3>
<p>Message Queuing Telemetry Transport, kurz MQTT, ist ein Protokoll für die Machine-to-Machine Kommuniktaion und dient in diesen Fall, dass der EV3 über das Internet mit dem Raspberry bzw. der Nodered App kommunizieren kann. Vor allem für IoT Devices findet MQTT eine wichtige Verwendung. Um MQTT nutzen zu können, muss ein Broker installiert werden. In diesem Fall nutzen wir Mosquitto. Der Broker dient als zentrale Stelle, wodurch sich andere Devices und User verbinden lassen und entweder die Rolle als Subscriber bzw. Publisher einnehmen können. In diesem Fall ist der Raspberry der Broker, der EV3 der Publisher und die Nodered App der Subscriber.</p>

<pre>sudo apt-get install mosquitto </br>
sudo apt-get install mosquitto-clients</pre>

<p>Mit diesem Befehl lässt sich Mosquitto starten</p>

<pre>sudo service mosquitto start</pre>

<p>Mit diesem Befehl lässt sich der Status von Mosquitto wiedergeben</p>

<pre>sudo systemctl status mosquitto</pre>

<p>Mit dem Release von MicroPython für den LEGO Mindstorms kommen schon zwei integrierte Pakete für MQTT mit. 'umqtt.simple' and 'umqtt.robust'. Dadurch lässt sich ein EV3 schnell in eine IoT Umgebung einbinden.
  
<pre>from umqtt.robust import MQTTClient
client = MQTTClient(MQTT_ClientID, MQTT_Broker)
client.connect()</pre>
