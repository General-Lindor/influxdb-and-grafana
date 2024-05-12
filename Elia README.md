# Was ist InfluxDB?

InfluxDB ist ein Datenbankmanagementsystem (DBMS), das sich auf Time-Series-Datenbanken (TSDB) spezialisiert hat. Neben seiner Kernfunktionalität als TSDB bietet InfluxDB auch eine webbasierte Benutzeroberfläche zur Datenerfassung und -visualisierung an. Darüber hinaus führt es die neue Programmiersprache Flux ein. Es existieren mehrere Versionen, dabei existiert auch eine kostenlose Open-Source-Version.

## InfluxDB Tools

Um Entwicklern die Arbeit mit Daten in InfluxDB zu erleichtern, bietet InfluxDB eine breite Palette an Tools an.

### <a name="first"></a>$${\color{teal} \underline{\mathbf{InfluxDB \space UI}}}$$

Die InfluxDB UI bietet eine vollständige Weboberfläche für die Arbeit mit InfluxDB. Die InfluxDB-Weboberfläche ermöglicht es:

- Abfragen erstellen um Daten visuell darzustellen.
- Flux-Code im Flux-Script-Editor zu bearbeiten
- Dashboards und Notizbücher zu erstellen
- Benutzer verwalten
- Tasks erstellen und  verwalten
- Checks und Alerts erstellen.

Die InfluxDB-Weboberfläche ermöglicht das Schreiben sowohl mit dem "Line Protocol" als auch mit "Annotated CSV Files" in InfluxDB. Und die Verwaltung von Telegraf-Konfigurationen.
  
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

## InfluxDB Daten Elemente

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

## Daten schreiben

InfluxDB bietet Tools an, die das Schreiben von Daten in InfluxDB unterstützen, einschließlich:

### Tool 1: [siehe InfluxDB UI](#first)

#### Line Protocol
>
> <br>Die InfluxDB-Weboberfläche ermöglicht das direkte Schreiben von Daten in die Datenbank, ohne dass Code geschrieben oder Tools verwendet werden müssen. Dies ist sehr nützlich für Prototyping- und Testzwecke.
>
> Es handelt sich um ein textbasiertes Format, welches das Measurement, die Tags, das Field und den Timestamp eines Datenpunkts angibt.
>
> #### *Syntax Beispiel*
>
>
> ![alt](images\line.png)<br><br>

### Tool 2: InfluxDB CLI

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
>
> Oder eine Text Datei mit mehreren Line Protocol Sätzen
>
> ```properties
> influx write --bucket-id 58eba9c8e6f6ac91 -file air-sensor-data.lìne.txt
>```
>
><br>

### Tool 3: InfluxDB REST-API

Über die API hat man die vollständige Kontrolle über Schreib- und Abfragevorgänge in InfluxDB und es werden mehr Funktionen angeboten als über die UI, CLI oder Client-Bibliotheken.

><br> Um Daten im Line Protocol Format an InfluxDB mit der API v2 zu schreiben, benutzt man einen POST-Request:
>
> ```ps
>curl -X POST 'http://127.0.0.1:8086/api/v2/write?bucket=WEATHER&precision=ns&orgID=d55d7051cce44707'
>-H"Authorization: Token <TOKEN>"
>-H 'accept: application/json'
>-d 'airSensors,sensor_id=TLM0101 temperature=71.83125302870145,humidity=34.87843425604827,co=0.5177653332811699'
>```
>
>Wichtig ist hier die Query-Paramenter in der URL richtig zu bennen.
><br><br>

### Tool 4: Flux

Mithilfe der Funktionen csv.from() oder array.from() kann ein annotiertes CSV generiert und anschließend mit der Funktion to() in die InfluxDB geschrieben werden.

!TODO

### Tool 5: Client-Bibliotheken

InfluxDB bietet 13 Client-Bibliotheken zur Auswahl an. Darunter Python, C#, Java, und mehr.

!TODO

### Tool 6: Telegraf

Mit dem Plugin-System von Telegraf & den über 200 Plugins lassen sich schnell Anbindungen zu den verschiedestend Schnittstellen einrichten. Die Daten können dann von Telegraf in die InfluxDB geschrieben werden & die Datenquellen lassen sich einfach über eine Konfigurationsdatei definieren.

!TODO

## Flux Query Language

!TODO

## Tasks

!TODO

???!TODO???
