# <a name="first"></a>$${\color{teal} \underline{\mathbf{InfluxDB \space und \space Flux}}}$$

<p>von $${\color{teal} Pascal \space Pahl}$$ und $${\color{teal} Daniele-Elia \space Stock}$$</p>

---

## $${\color{teal}Inhaltsverzeichnis}$$

1. [Was ist InfluxDB?](#first)
2. [Wie speichert InfluxDB Daten?](#second)
3. [Wie sieht es mit der Sicherheit aus?](#third)
4. [Was ist Flux?](#fourth)
5. [Typischer Aufbau einer Flux-Query](#fifth)
6. [Wie kann man Daten schreiben und löschen?](#sixth)

---

## <a name="first"></a>$${\color{teal}Was \space ist \space InfluxDB?}$$

InfluxDB ist ein Datenbankmanagementsystem (DBMS), das sich auf Time-Series-Datenbanken (TSDB) spezialisiert hat.
Neben seiner Kernfunktionalität als TSDB bietet InfluxDB auch eine webbasierte Benutzeroberfläche zur Datenerfassung und -visualisierung an.
Darüber hinaus führt es die neue Programmiersprache Flux ein.
Es existieren mehrere Versionen, dabei existiert auch eine kostenlose Open-Source-Version.
Bevor man irgendwas machen kann, muss man die Datenbank allerdings starten.
Und zwar jedes Mal.
Dafür steht eine .exe zur Verfügung.

## <a name="second"></a>$${\color{teal}Wie \space speichert \space InfluxDB \space Daten?}$$

### BUCKET

≙SQL-Datenbank

### _measurement

≙SQL-Tabelle

### _field

≙SQL-Spalte

### _time

Zeit

## <a name="third"></a>$${\color{teal}Wie \space sieht \space es \space mit \space der \space Sicherheit \space aus?}$$

### Token

RSA

### Username

Man muss sich anmelden, bevor man Zugriffsrechte erhält.

### Password

Man muss sich anmelden, bevor man Zugriffsrechte erhält.

## <a name="fourth"></a>$${\color{teal}Was \space ist \space Flux?}$$

Flux ist das SQL von InfluxDB.
Während SQL jedoch gleichzeitig eine DDL (Data Definition Language), DML (Data Manipulation Language), DCL (Data Control Language) und TCL (Transaction Control Protocol) ist,
ist Flux eine reine Data Query Language.
Mit Flux kann man keine Struktur vorgeben, keine Daten einfügen oder löschen und keine Zugriffsrechte manipulieren.
Äquivalente Befehle zu CREATE, INSERT oder DELETE existieren nicht.
Dafür bietet Flux jedoch breite Funktionalität im Bereuch Datenanalyse.

## <a name="fifth"></a>$${\color{teal}Typischer \space Aufbau \space einer \space Flux \space Query}$$

Eine typische Flux query ist folgendermaßen aufgebaut:

```flux
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

sorgt dafür, dass die Daten ausgegeben werden.
Alles, was danach mit den Daten passiert (außer pivot) hat keinen Einfluss auf den Output.
Sollte in jeder Flux-Query vorhanden sein.

### keep

Alle Spalten außer die genannten werden beim yield-Befehl ignoriert.

### group

### drop

Entfernt eine spezifische Spalte aus der Output-Tabelle des yield-Befehles.

### pivot

### mean()

Berechnet den Durchschnitt der Daten

## <a name="sixth"></a>$${\color{teal}Wie \space kann \space man \space Daten \space schreiben \space und \space löschen?}$$

InfluxDB arbeitet über das http-Protokoll. Über http-GET- und http-POST-Methoden können Daten geschrieben und gelöscht werden.
Dabei existieren verschiedene libraries in verschiedenen Programmiersprachen, welche das Ganze vereinfachen.
