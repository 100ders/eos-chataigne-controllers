# ShuttleXpress → ETC Eos (Chataigne)

🇫🇷 [Version française](README.md)

Ready-to-use [Chataigne](https://github.com/benkuper/Chataigne) project to control **ETC Eos / ETCnomad** with a **Contour ShuttleXpress**, through the [ShuttleXpressOSC](https://github.com/100ders/shuttleXpress-OSC) bridge. No script: everything lives in Chataigne States.

```
ShuttleXpress ──USB──▶ ShuttleOSC ──OSC :9000──▶ Chataigne ──OSC :8000──▶ Eos
                                                    ▲                       │
                                                    └──── OSC :9000 ────────┘ (optional)
```

## Features
| Control | Action |
|---|---|
| Button 1 | **Intensity** mode (Eos encoder page: Intensity) |
| Button 2 | **Pan** mode (Focus page) |
| Button 3 | **Home** on selection (`/eos/at/home`) |
| Button 4 | **Tilt** mode (Focus page) |
| Button 5 | **Zoom** mode (Form page) |
| Jog wheel | Step adjustment of the active parameter |
| Shuttle ring (spring) | Continuous movement of the active parameter; stops on release |

Only one mode is active at a time (Pan at startup). Each mode change first stops any running ring movement and switches the Eos encoder page to show the controlled parameter.

## Requirements
- [Chataigne](https://github.com/benkuper/Chataigne) **1.9.24** (tested with this version): [download page](https://benjamin.kuperberg.fr/chataigne/en).
- ETC Eos / ETCnomad (tested with ETCnomad on Windows, Offline mode).
- The **ShuttleOSC** bridge running and sending to port **9000**.

## Eos setup
See also the [Eos OSC setup](../docs/eos-osc-setup.en.md), with the `Tab 99` check.

In Eos: **Setup › System Settings › Show Control › OSC**

| Setting | Value | Purpose |
|---|---|---|
| OSC RX | **Enabled** | Eos receives commands from Chataigne |
| OSC UDP RX Port | **8000** | Eos receive port |
| OSC TX | Enabled *(optional)* | Feedback to Chataigne |
| OSC UDP TX IP Address | `127.0.0.1` *(if Chataigne runs on the same computer, otherwise its IP)* | Feedback destination |
| OSC UDP TX Port | **9000** | Chataigne listening port |

Notes:
- This project works **without** OSC TX. TX is only required for `/eos/active/wheel/…` commands and to display Eos information in Chataigne.
- On Windows, allow Chataigne (and Eos) through the firewall on first launch.
- **Diagnostics**: `Tab 99` in Eos shows received (`RECV`) and sent (`SEND`) OSC messages.
- Commands apply to the **selected channels**: select a fixture before using the Shuttle.

## Chataigne setup
1. Open `Shuttle-EOS.noisette`.
2. **OSC** module:
   - *Input*: local port **9000**;
   - *Output*: host `127.0.0.1` (or the Eos computer's IP), port **8000**.
3. Start ShuttleOSC, select a fixture in Eos, turn the jog wheel.

## Customization
| To… | Change |
|---|---|
| Change jog speed | The argument of the `JOG +` / `JOG -` Actions in each State (2 / -2 by default) |
| Change ring speed | The **Remap** filter of the `BAGUE …` Mapping (output -3…3; -1…1 for intensity) |
| Control another parameter | The `/eos/wheel/coarse/<parameter>` and `/eos/switch/<parameter>` addresses in a JOG State |
| Finer control | Replace `coarse` with `fine` and raise the argument (one *fine* step is very small) |
| Reassign a button | The `/shuttle/button/<n>` condition of the Action in the **BOUTONS** State |

## Troubleshooting
| Symptom | Check |
|---|---|
| Nothing moves | ShuttleOSC running? OSC module on port 9000? Fixture selected? OSC RX enabled? |
| Messages received in `Tab 99` but no movement | One *fine* step is barely visible: use *coarse* or a larger argument |
| `invalid active parameter` in `Tab 99` | Applies to `/eos/active/wheel/…`: enable **OSC TX** in Eos and reselect the fixture |
| Encoder page does not change | Check in `Tab 99` that `/eos/key/encoder_category_…` is received |
| Parameter keeps moving | Return the ring to center; as a fallback, send `/eos/reset` |

## Known limitations
- **Home** returns all selected parameters to their default, not only pan/tilt.
- **Intensity** mode (`/eos/wheel/level`, `/eos/switch/level`) is the least tested.

---

📜 GPL v3 · Independent project, not affiliated with Contour Design, ETC or Chataigne.
