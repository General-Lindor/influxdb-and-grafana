# InfluxDB & Flux
<p>by Pascal Pahl und Daniele-Elia Stock</p>

---

## Inhaltsverzeichnis
1. [Was ist InfluxDB?](#first)
2. [Platzhalter](#second)
3. [Platzhalter](#third)
4. [Platzhalter](#fourth)
5. [Platzhalter](#fifth)

---

## <a name="first"></a>Was ist InfluxDB?

InfluxDB ist ein Datenbankmanagementsystem (DBMS), das sich auf Time-Series-Datenbanken (TSDB) spezialisiert hat.
Neben seiner Kernfunktionalität als TSDB bietet InfluxDB auch eine webbasierte Benutzeroberfläche zur Datenerfassung und -visualisierung an.
Darüber hinaus führt es die neue Programmiersprache Flux ein.
Es existieren mehrere Versionen, dabei existiert auch eine kostenlose Open-Source-Version.

## Wie speichert InfluxDB Daten?

### BUCKET

### _measurement

### _field

### _time

## Wie sieht es mit der Sicherheit aus?

### Token

### Username

### Password

## <a name="second"></a>Was ist Flux?

Flux ist das SQL von InfluxDB.
Während SQL jedoch gleichzeitig eine DDL (Data Definition Language), DML (Data Manipulation Language), DCL (Data Control Language) und TCL (Transaction Control Protocol) ist,
ist Flux eine reine Data Query Language.
Mit Flux kann man keine Struktur vorgeben, keine Daten einfügen oder löschen und keine Zugriffsrechte manipulieren.
Äquivalente Befehle zu CREATE, INSERT oder DELETE existieren nicht.
Dafür bietet Flux jedoch breite Funktionalität im Bereuch Datenanalyse.

## <a name="third"></a>Aufbau einer Flux-Query?

Eine typische Flux query ist folgendermaßen aufgebaut:
```
```

### Filter

### Yield

### Keep

### GROUP

### DROP

### PIVOT

### MEAN

## <a name="fourth"></a>Wie kann man Daten schreiben und löschen?

InfluxDB arbeitet über das http-Protokoll. Über http-GET- und http-POST-Methoden können Daten geschrieben und gelöscht werden.
Dabei existieren verschiedene libraries in verschiedenen Programmiersprachen, welche das Ganze vereinfachen.

## <a name="fifth"></a>Hurwitz?