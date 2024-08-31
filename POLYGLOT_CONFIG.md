Linez Plugin (NodeServer)

The Linez Power Monitors were produced by the now defunt JLM Energy based in Rocklin California and were used, 1 per panel, mostly in residential, to monitor building, solar and grid usage.

This node server polls your Linez unit uning its ip address (ip_address/sensors) and parses the following data:

Grid Power
Solar Power
Building Power
Power A
Power B
Power AB
Power C
Power D
Power CD
Voltage A
Voltage B
Voltage AB
Current A
Current B
Current C
Current D
Power Factor
Frequency
Linez Serial Number

These values are then displayed on the IoX Node Page.
A Heartbeat value that alternates between 1 and -1 changes with each poll event

## Configuration

- Ensure the Linez unit is running and accessible.
- Install the node server via Polyglot.
- Enter the IP address of the Linez unit, example 192.168.0.123 
- Set shortPoll for the poll time (in seconds) that you wish.
- Monitor the IoX Node Page for updates.
- Pressing "Query" on the bottom of the node page in IoX will blank the node values then query the linez server and repopulate with new values. 


