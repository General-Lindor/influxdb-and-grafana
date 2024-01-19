do io.write("Please drag&drop the folder of influxd.exe: ") end
do io.flush() end
local s = io.read()
do s = string.gsub(s, "\\", "\\\\") end
do s = string.gsub(s, "\"", "\\\"") end
--powershell start cmd -v runas -ArgumentList {/c \"@echo on & cd C:\\Program Files\\InfluxData\\influxdb\\influxdb2-2.7.5-windows & influxd.exe"}
local file = io.open("influx.bat", "w")
do file:write('powershell start cmd -v runas -ArgumentList {/c \\\"@echo on & cd '..s..' & influxd.exe\\\"}') end
do file:close() end
do print("Successfully created influx.bat. Press ENTER to end the program") end
do io.read() end