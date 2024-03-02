# Was macht dieses Projekt?

Speicherung von Hardware-related Daten in einer zeitbasierten Influx-Datenbank und Realtime-Visualisierung der Daten.
Zur Zeit: CPU-Frequenz & Auslastung

# Wie initialisiere / installiere ich das Projekt?

1. Richte dir Influxdb ein, sodass du influxd.exe hast, token, passwort, username, bucket etc. hast
2. speichere die Daten in einer .env im Folder, folgende Struktur:\
INFLUXDB_USERNAME=myusername\
INFLUXDB_PASSWORD=mypassword\
INFLUXDB_TOKEN=myoken\
INFLUXDB_URL=myurl\
INFLUXDB_ORG=myorg\
INFLUXDB_BUCKET=system_monitoring
3. pip install pandas
4. starte influx.exe und folge den Anweisungen
5. You're ready to go: starte einfach nur influxdb.py

# Was machen die einzelnen files?

## influx.exe

Öffnet einen Command-Prompt.

Nach Ziehen der auf dem PC installierten influxd.exe,
welche sich der Client vorher eingerichtet haben muss,
um influxdb benutzen zu können,
kreiert influx.exe eine Batch-Datei,
welche automatisch die Datenbank initialisiert.

Die Batch-Datei ist Notwendig,
da sie Problemlos vom Python-Script aus gestartet werden kann.

Es handelt sich hierbei quasi um eine Anwendung zur Setup-Initialisierung.

## influxd.bat

Führt influxd.exe aus,
die sich irgendwo auf dem Client-System befinden muss,
und startet damit die Datenbank.

Diese Datei wird vom python script aus ausgeführt.

## influxdb.py

Das Herzstück;
führt bei Starten automatisch die Batch-Datei aus und beginnt sofort,
die Hardware-Daten in die Datenbank zu schreiben.

Die Daten werden in realtime auf dem Desktop geplotted.

Dabei wird mittels multithreading dafür gesorgt,
dass gleichzeitig geschrieben und geplotted werden kann.

## .env

Daten für die Datenbankverbindung, username, password etc.
Sollte nicht present sein im github, musste selber einrichten

# To-Do-List

- Auswahl der Daten, die gespeichert werden sollen
- flux language implementation: queries über flux
- docker?
- Warum werden die Labels \/ Achsenbeschriftungen nicht angezeit? Warum ist der Titel "Figure 1"? Fix That PLS.