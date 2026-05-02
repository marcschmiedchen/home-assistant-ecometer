# Proteus Ecometer

Home Assistant integration for the **Proteus TEK603 Ecometer** ultrasonic liquid level sensor.

Connects via USB (Silicon Labs CP2102) and provides the following sensors:

| Sensor | Unit | Description |
|--------|------|-------------|
| Temperatur | °C | Fluid temperature |
| Fluessigkeitspegel | cm | Liquid level |
| Nutzkapazitaet | l | Usable volume |
| Gesamtkapazitaet | l | Total vessel capacity |

The device is auto-detected on setup. Reconnects automatically after USB disconnection.
