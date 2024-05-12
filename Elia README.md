# Was ist InfluxDB?
InfluxDB ist ein Datenbankmanagementsystem (DBMS), das sich auf Time-Series-Datenbanken (TSDB) spezialisiert hat. Neben seiner Kernfunktionalität als TSDB bietet InfluxDB auch eine webbasierte Benutzeroberfläche zur Datenerfassung und -visualisierung an. Darüber hinaus führt es die neue Programmiersprache Flux ein. Es existieren mehrere Versionen, dabei existiert auch eine kostenlose Open-Source-Version.

# InfluxDB Tools
Um Entwicklern die Arbeit mit Daten in InfluxDB zu erleichtern, bietet InfluxDB eine breite Palette an Tools an.

### InfluxDB UI
Die InfluxDB UI bietet eine vollständige Weboberfläche für die Arbeit mit InfluxDB. Die InfluxDB-Weboberfläche ermöglicht es:
- Abfragen erstellen um Daten visuell darzustellen.
- Flux-Code im Flux-Script-Editor zu bearbeiten
- Dashboards und Notizbücher zu erstellen
- Benutzer verwalten
- Tasks erstellen und  verwalten
- Checks und Alerts erstellen.
  
### Flux
Flux ist eine funktionale Skriptsprache, die darauf ausgelegt ist, Abfragen, Daten-Transformation, Analyse und das Reagieren auf Daten in einer einzigen Syntax zu vereinen.

- Daten transformieren und analysieren
- Tasks schreiben
- ...

### Task Engine
Die Task-Engine führt Flux-Skripte gemäß einem festgelegtem Zeitplan aus.

- Datenverarbeitung zur Beschleunigung von Visualisierungen
- Benachrichtigungen erhalten, wenn Daten nicht mehr geschrieben werden oder bestimmte Schwellenwerte überschritten werden
- Aufrufen externer Dienste

### Rest API
InfluxDB ist vollständig in eine REST-API integriert. Die API ermöglicht natürlich das Schreiben und Abfragen von Daten, bietet aber auch alles, was zur Verwaltung der Datenbank benötigt wird, einschließlich der Erstellung von Ressourcen wie Authentifizierungstoken, Buckets, Benutzern usw.

### Client Bibliotheken
Man ist nicht darauf beschränkt, REST-Aufrufe selbst durchzuführen. InfluxDB bietet Client-Bibliotheken in 13 Sprachen an. Mit diesen Client-Bibliotheken können InfluxDB-Funktionen problemlos in eine bestehende Codebasis integriert oder eine neue Codebasis erstellt werden.
- Python
- C#
- Java
- ...

### Telegraf
Telegraf ist ein agent-basiertes Tool, das Daten aus verschiedenen Quellen sammelt und weiterverarbeitet. Es verfügt über ein erweiterbares Plugin-System mit über 200 Plugins, die bei der Anbindung unterschiedlicher Schnittstellen helfen. Die Daten können von Telegraf in die InfluxDB geschrieben werden. Die Datenquellen lassen sich über die Konfigurationsdatei definieren.

# InfluxDB Daten Elemente
### Bucket
Alle Daten in InfluxDB werden in sogenannten Buckets geschriben. Ein Bucket ist ein Container, der so viele Measurements wie gewünscht speichern kann.

Zudem können Tokens erstellt werden, wodurch die Lese- und Schreibberechtigungen für einen bestimmten Bucket gesteuert werden können.

Des Weiteren muss beim Erstellen eines Buckets eine Aufbewahrungsfrist (Retention Period) festgelegt werden. Diese bestimmt, wie lange die Daten in einem Bucket gespeichert werden.

### Measurement
Measurements sind die höchste Datenstruktur innerhalb eines Buckets. Sie können wie Tabellen in einer traditionellen SQL-Datenbank betrachtet werden.

Sie sind eine logische Gruppierung der Daten und enthalten mehrere Tags & Fields, außerdem sollten alle Punkte eines Measurements dieselben Tags haben. 

Ein Bespiel:

> Sie entwickeln eine Wetter-App und schreiben Wetterdaten für mehrere Städte in einen Bucket. Für diesen Fall könnten Sie ein Measurement namens "air_temperature" erstellen und ein zweites Measurement z.B. "water_temperature".

### Tag
Ein Tag besteht aus einem Key-Value-Pair und enthält wichtige Metadaten. Diese beinhalten typischerweise Informationen über die Datenquelle.

Ein Bespiel:

> Sie entwickeln eine Wetter-App und speichern Wetterdaten für mehrere Städte in einem Bucket. In diesem Fall könnten Sie einen Tag mit dem Schlüssel "location" erstellen, wobei die Tag-Werte die jeweiligen Standorte wie "Berlin", "Hamburg", "Köln". ... enthalten.

### Field
Ein Field besteht aus einem Key-Value-Paar und enthält die tatsächlichen Daten, die gespeichert, visualisiert und für Berechnungen usw. verwendet werden.

Ein Bespiel:

> Sie entwickeln eine Wetter-App und speichern Wetterdaten. In diesem Fall könnten Sie einen Field mit dem Schlüssel "temperature", "humidity" oder z.B. "co2" erstellen werden, wobei die Field-Werte die tatsächlichen Messwerte enthalten.

### Timestamp
Ein Zeitstempel, der mit den Daten verknüpft ist.

# Daten schreiben
InfluxDB bietet Tools an, die das Schreiben von Daten in InfluxDB unterstützen, einschließlich:

### InfluxDB UI
Die InfluxDB-Weboberfläche ermöglicht das Schreiben sowohl mit dem "Line Protocol" als auch mit "Annotated CSV Files" in InfluxDB. Und die Verwaltung von Telegraf-Konfigurationen.

##### Line Protocol
> <br>Die InfluxDB-Weboberfläche ermöglicht das direkte Schreiben von Daten in die Datenbank, ohne dass Code geschrieben oder Tools verwendet werden müssen. Dies ist sehr nützlich für Prototyping- und Testzwecke.
> 
> Es handelt sich um ein textbasiertes Format, welches das Measurement, die Tags, das Field und den Timestamp eines Datenpunkts angibt.
> ##### *Syntax Beispiel*
>
> 
> ![alt](images\line.png)<br><br>

### InfluxDB CLI
Die CLI ist einfach zu bedienen und perfekt für Entwickler, die normalerweise nicht GUIs bevorzugen.

*Beispiel:*
> <br>Die ID vom Bucket in den geschrieben werden soll mithilfe dem Befehl ``` influx bucket list ``` herrausfinden.
> 
> ![alt](images\bucket_list.png)
> <sup>*Da der Bucket & Organisations Name Special Chars beinhalten kann & mutable sind wird die ID verwendet*</sub>
> 
> Jetzt können wir mit dem Befehl ``` influx write ``` & dem Line Protocol Daten in den Bucket schreiben. 
> 
> ```properties
> influx write --bucket-id 58eba9c8e6f6ac91 "airSensors,sensor_id=TLM0101 temperature=71.83125302870145,humidity=34.87843425604827,co=0.5177653332811699"
>```
> Oder eine Text Datei mit mehreren Line Protocol Sätzen
> 
> ```properties
> influx write --bucket-id 58eba9c8e6f6ac91 -file air-sensor-data.lìne.txt
>```
><br>

### InfluxDB REST-API
Über die API hat man die vollständige Kontrolle über Schreib- und Abfragevorgänge in InfluxDB und es werden mehr Funktionen angeboten als über die UI, CLI oder Client-Bibliotheken.

><br> Um Daten im Line Protocol Format an InfluxDB mit der API v2 zu schreiben, benutzt man einen POST-Request:
> ```ps
>curl -X POST 'http://127.0.0.1:8086/api/v2/write?bucket=WEATHER&precision=ns&orgID=d55d7051cce44707'
>-H"Authorization: Token <TOKEN>"
>-H 'accept: application/json'
>-d 'airSensors,sensor_id=TLM0101 temperature=71.83125302870145,humidity=34.87843425604827,co=0.5177653332811699'
>```
>Wichtig ist hier die Query-Paramenter in der URL richtig zu bennen.
><br><br>

### Flux
Mithilfe der Funktionen csv.from() oder array.from() kann ein annotiertes CSV generiert und anschließend mit der Funktion to() in die InfluxDB geschrieben werden.

> <br><sup> In diesem Beispiel importeren wir erst Sample Daten von InfluxDB und schreiben diese dann in den Bucket "WEATHER"</sup><br>
> ![alt](images\flux_write.png)<br>
> <br>

### Client-Bibliotheken
InfluxDB bietet 13 Client-Bibliotheken zur Auswahl an. Darunter Python, C#, Java, und mehr.

> <br><sup>Beispiel mit Python</sup><br>
> ![alt](images\py_sample.png)
> <br><br>

### Telegraf
Mit dem Plugin-System von Telegraf & den über 200 Plugins lassen sich schnell Anbindungen zu den verschiedestend Schnittstellen einrichten. Die Daten können dann von Telegraf in die InfluxDB geschrieben werden & die Datenquellen lassen sich einfach über eine Konfigurationsdatei definieren.

> <br>Beispiel <br><br>
> Als aller erstet muss das gewünschte Plugin gewählt werden. Um das Beispiel einfach zu halten benutzten wir das System Plugin da dies keine zusätlichen Konfigurationen braucht.<br>
> ![alt](images\telegraf_1.png)<br>
> <br><br>Nach dem das Plugin ausgewählt wurde können wir das Plugin im Normalfall konfigurieren.<br>
> ![alt](images\telegraf_2.png)<br>
> <br>Nun müssen wir unsere INFLUX_TOKEN Variable mit ```SET INFLUX_TOKEN=<TOKEN>``` oder ```export INFLUX_TOKEN=<TOKEN>``` setzten & danach Telegaf mit der im vorherigen erstellten Config start. ```telegraf --config http://localhost:8086/api/v2/telegrafs/<CONFIG_ID>```
> ![alt](images\telegraf_3.png)<br>
> ![alt](images\telegraf_4.png)<br>
> <br><br>Nun werden automatisch über Telegraf Daten in unseren System Bucket geschieben<br>
> ![alt](images\telegraf_5.png)<br>
> ![alt](images\telegraf_6.png)<br>

# Flux

Flux ist das SQL von InfluxDB. Während SQL jedoch gleichzeitig eine DDL (Data Definition Language), DML (Data Manipulation Language), DCL (Data Control Language) und TCL (Transaction Control Protocol) ist, ist Flux eine reine Data Query Language. Mit Flux kann man keine Struktur vorgeben, keine Daten einfügen oder löschen und keine Zugriffsrechte manipulieren. Äquivalente Befehle zu CREATE, INSERT oder DELETE existieren nicht. Dafür bietet Flux jedoch breite Funktionalität im Bereuch Datenanalyse.

### Typischer Aufbau einer Flux Query
Eine typische Flux query ist folgendermaßen aufgebaut:
```
data = from(bucket: "system_monitoring")
    |> range(start: -15m)
    |> filter(fn: (r) => (r._measurement == "CPU") and ((r._field == "Auslastung") or (r._field == "Frequenz")))
    |> group(columns: ["_field"], mode: "by")
    |> keep(columns: ["_time", "_field", "_value"])
    |> yield(name: "_results")
    |> pivot(rowKey:["_time"], columnKey: ["_field"], valueColumn: "_value")
```

Gehen wir die verschiedenen Befehle durch:

### range
Entspricht dem WHERE-Teil des SELECT-Statements

### filter
Entspricht dem Spalten-Teil und dem FROM-Teil des SELECT-Statements

### yield
sorgt dafür, dass die Daten ausgegeben werden. Alles, was danach mit den Daten passiert (außer pivot) hat keinen Einfluss auf den Output. Sollte in jeder Flux-Query vorhanden sein.

### keep
Alle Spalten außer die genannten werden beim yield-Befehl ignoriert.

### group
drop
Entfernt eine spezifische Spalte aus der Output-Tabelle des yield-Befehles.

### pivot
mean()
Berechnet den Durchschnitt der Daten

# Tasks
Die Task-Engine führt Flux-Skripte gemäß einem festgelegtem Zeitplan aus.

Einer der häufigsten Anwendungsfälle für InfluxDB-Tasks besteht darin, Daten zu reduzieren (downsampling), um die Speichernutzung zu reduzieren, während Daten im Laufe der Zeit gesammelt werden. 

><br>Beispiel Task
>
>Gehen wir davon aus wir möchten in unserem "Weather" Bucket das Measurement "airSensors" längerfristig archivieren und dabei unsere Speichernutzung reduzieren.
>
>Wir erstellen als erstes einen neuen Taks und geben als erstet an nach welchem Intervall das Script ausgeführt werden soll.
>
> 1. from(bucket: "Weather") - Da unser Measurement was wir archivieren wollen in diesem Bucket liegt
> 2. range(start: -7d) - Da unser Script alle 7 Tage ausgeführt wird brauchen wir alle Daten der letzten 7 Tage
> 3. aggregateWindow(every: 10m, fn: mean) - Wird reduzieren die Daten auf ein 10 Minuten Fenster und ermitteln dafür den Mittelwert. 
> 4. to(bucket: "Weather_Downsample") - Der Bucket in dem wir die Daten archivieren wollen.
> 
>![alt](images\tasks_1.png)
>
>Wie man sieht haben unsere airSensoren in der letzten Stunde 8640 Datensätze produziert.
>![alt](images\tasks_2.png)
>![alt](images\tasks_3.png)
>
>Nach dem wir unser Tasks ausgeführt haben sich unsere Datensätze auf 144 reduziert.
>![alt](images\tasks_4.png)
>![alt](images\tasks_5.png)
