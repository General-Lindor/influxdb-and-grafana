# Auslastung & Frequenz in 2 Tabellen
queryAll = '''data = from(bucket: "system_monitoring")
    |> range(start: -15m)
    |> filter(fn: (r) => (r._measurement == "CPU") and ((r._field == "Auslastung") or (r._field == "Frequenz")))
    |> group(columns: ["_field"], mode: "by")
    |> keep(columns: ["_time", "_field", "_value"])
    |> yield(name: "_results") |> pivot(rowKey:["_time"], columnKey: ["_field"], valueColumn: "_value")'''

# Auslastung in 1 Tabelle
queryA = '''data = from(bucket: "system_monitoring")
    |> range(start: -15m)
    |> filter(fn: (r) => (r._measurement == "CPU") and (r._field == "Auslastung"))
    |> keep(columns: ["_time", "_field", "_value"])
    |> yield(name: "_resultsA") |> pivot(rowKey:["_time"], columnKey: ["_field"], valueColumn: "_value")'''

# Frequenz in 1 Tabelle
queryF = '''data = from(bucket: "system_monitoring")
    |> range(start: -15m)
    |> filter(fn: (r) => (r._measurement == "CPU") and (r._field == "Frequenz"))
    |> keep(columns: ["_time", "_field", "_value"])
    |> yield(name: "_resultsF") |> pivot(rowKey:["_time"], columnKey: ["_field"], valueColumn: "_value")'''