[![Validate with hassfest](https://github.com/marcschmiedchen/home-assistant-ecometer/actions/workflows/hassfest.yaml/badge.svg)](https://github.com/marcschmiedchen/home-assistant-ecometer/actions/workflows/hassfest.yaml)
[![Validate with HACS](https://github.com/marcschmiedchen/home-assistant-ecometer/actions/workflows/hacs.yaml/badge.svg)](https://github.com/marcschmiedchen/home-assistant-ecometer/actions/workflows/hacs.yaml)
[![HACS](https://img.shields.io/badge/HACS-Custom-41BDF5.svg)](https://github.com/hacs/integration)


[English](#english) | [Deutsch](#deutsch)

---

<a name="english"></a>
# Proteus Ecometer — Home Assistant Integration

Custom component for [Home Assistant](https://www.home-assistant.io/) that integrates the **Proteus TEK603 Ecometer** ultrasonic liquid level sensor via USB or TCP.

## About the Device

The [Proteus Ecometer](https://www.proteus.de/produkte/fuellstandsmessung/ecometer/) is an ultrasonic sensor for measuring liquid levels in tanks and vessels. It connects via USB (Silicon Labs CP2102 adapter) at 115200 baud.


## Sensors

| Sensor | Unit | Description |
|--------|------|-------------|
| Temperatur | °C | Fluid temperature |
| Fluessigkeitspegel | cm | Distance / liquid level |
| Nutzkapazitaet | l | Usable volume |
| Gesamtkapazitaet | l | Total vessel capacity |

## Installation

1. Copy `custom_components/ecometer/` into your HA config `custom_components/` directory.
2. Restart Home Assistant.
3. Go to **Settings → Integrations → Add Integration** and search for **Proteus Ecometer**.
4. Provide the connection details.

### Via HACS

Add this repository as a custom repository in [HACS](https://hacs.xyz/), then install **Proteus Ecometer** from the integration list.

## Requirements

- Home Assistant 2024.1+
- Python packages (installed automatically): `pyserial-asyncio-fast`, `tek603`

## Protocol Reference

- [sarnau.info](https://sarnau.info) — full frame structure, flag bits, EEPROM layout, 365-day history buffer
- [wlemkens/domoticz-ecometers](https://github.com/wlemkens/domoticz-ecometers) — Domoticz plugin with full packet parsing reference implementation

## License

MIT

---

<a name="deutsch"></a>
# Proteus Ecometer — Home Assistant Integration

Benutzerdefinierte Komponente für [Home Assistant](https://www.home-assistant.io/), die den **Proteus TEK603 Ecometer** Ultraschall-Füllstandssensor per USB einbindet.

## Über das Gerät

Der [Proteus Ecometer](https://www.proteus.de/produkte/fuellstandsmessung/ecometer/) ist ein Ultraschallsensor zur Füllstandsmessung in Tanks und Behältern. Die Verbindung erfolgt per USB oder TCP (Silicon Labs CP2102) mit 115200 Baud.


## Sensoren

| Sensor | Einheit | Beschreibung |
|--------|---------|--------------|
| Temperatur | °C | Flüssigkeitstemperatur |
| Fluessigkeitspegel | cm | Abstand / Füllstand |
| Nutzkapazitaet | l | Nutzvolumen |
| Gesamtkapazitaet | l | Gesamtvolumen des Behälters |

## Installation

1. Den Ordner `custom_components/ecometer/` in das `custom_components/`-Verzeichnis der HA-Konfiguration kopieren.
2. Home Assistant neu starten.
3. Unter **Einstellungen → Integrationen → Integration hinzufügen** nach **Proteus Ecometer** suchen.
4. Verbindung konfigurieren

### Über HACS

Dieses Repository als benutzerdefiniertes Repository in [HACS](https://hacs.xyz/) hinzufügen und **Proteus Ecometer** aus der Integrationsliste installieren.

## Voraussetzungen

- Home Assistant 2024.1+
- Python-Pakete (werden automatisch installiert): `pyserial-asyncio-fast`, `tek603`

## Protokoll-Referenzen

- [sarnau.info](https://sarnau.info) — vollständige Frame-Struktur, Flag-Bits, EEPROM-Layout, 365-Tage-Verlaufspuffer
- [wlemkens/domoticz-ecometers](https://github.com/wlemkens/domoticz-ecometers) — Domoticz-Plugin als Referenzimplementierung für die vollständige Paketverarbeitung

## Lizenz

MIT
