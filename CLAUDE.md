This is a home assistant integration prototype for an PROTEUS ECOMETER USB sensor. It measures distance to liquidity via ultrasonic measurements and reports current level , temperature and some other values from some vessel.

The integration consists of two parts, which will later be split up: the communcation with the hardware via USB (in the tek603 directory) and the home assistent integration which handles HA entities.

THe integration should be sleek and minimal, with the least amount of external libraries/dependencies in Python. It should be stable when USB connection fails / or is disconnected / reconnected. It should be fully async with callbacks due to Home Assistant requirements.

the protocol is fully reverse-engineered.
sarnau.info — canonical protocol reference including full frame structure, flag bits, EEPROM layout, and 365-day history buffer format. Your current parser only handles live data bytes at fixed offsets — it should validate the header flags and CRC-16.
wlemkens/domoticz-ecometers — Python Domoticz plugin implementing full packet parsing with CRC-16/XMODEM verification. Good reference for porting to async HA style.
