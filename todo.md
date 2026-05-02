# Ecometer Fix List

## CRITICAL
- [x] 1. **`tek603` module missing** — `__init__.py:12` imports `from tek603 import TEK603` but `tek603/` deleted from root, not added to `custom_components/ecometer/`. Move `tek603/` → `custom_components/ecometer/tek603/`, change import to `from .tek603 import TEK603`.
- [x] 2. **`DOMAIN` case mismatch** — `const.py:1` has `DOMAIN = 'Ecometer'` but manifest says `"domain": "ecometer"` and dir is `custom_components/ecometer/`. Fix: `DOMAIN = 'ecometer'`.

## HIGH
- [x] 3. **`state` → `native_value`** — `sensor.py:79` overrides `state` while `_attr_native_unit_of_measurement` set. HA unit conversion hooks into `native_value`. Rename property.
- [x] 4. **`pyserial` missing from requirements** — `pyserial-asyncio-fast` declares `pyserial` as dependency, so `serial.tools.list_ports` always available. No explicit manifest entry needed.

## MEDIUM
- [x] 5. **`manifest.json` missing `iot_class`** — Add `"iot_class": "local_push"`.
- [x] 6. **Config flow aborts on no CP2102** — `config_flow.py:36` aborts if device not detected at config time. Show full port dropdown instead.

## LOW
- [x] 7. **`round(value, 0)` returns float** — `sensor.py:82`. Use `round(value)` for int.
- [ ] 8. **Stale git state** — Root-level files deleted, `custom_components/` untracked. Run `git add custom_components/` and commit restructure.
