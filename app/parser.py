import re
import html


def esc(s: str) -> str:
    return html.escape(str(s), quote=False)


def span(cls: str, text: str) -> str:
    return f'<span class="{cls}">{esc(text)}</span>'


ASCII_ART = r"""
   ____          _ _               ____                 _
  / ___|___   __| (_)_ __   __ _  |  _ \ ___  ___  ___ | |_   _____ _ __
 | |   / _ \ / _` | | '_ \ / _` | | |_) / _ \/ __|/ _ \| \ \ / / _ \ '__|
 | |__| (_) | (_| | | | | | (_| | |  _ <  __/\__ \ (_) | |\ V /  __/ |
  \____\___/ \__,_|_|_| |_|\__, | |_| \_\___||___/\___/|_| \_/ \___|_|
                           |___/
                                                       by Mezentsev Roman
"""


def GREEN(t="Activated"):
    return span("green", t)


def YELLOW(t="Unknown Bit"):
    return span("yellow", t)


def RED(t="NOT OK"):
    return span("red", t)


def CYAN(t="Deactivated"):
    return span("cyan", t)


SCALE = 16
BITS = 8

unknown_bit = YELLOW("Unknown Bit")
activated = GREEN("Enabled")
deactivated = CYAN("Disabled")

engine_codes = {
    "40": "2.0 TFSI",
    "48": "2.0 TDI",
    "14": "3.0 TFSI",
    "6C": "2.9 TFSI",
    "3A": "4.0 TDI",
}
car_model = {"99": "A4", "97": "A6", "9A": "S5", "BE": "Q5", "B2": "Q7"}
transmission_codes = {
    "2C": "0CJ (quattro ultra)",
    "10": "0CK (fwd)",
    "30": "0D5 (8-gears qauttro)",
    "28": "0CL (quattro)",
    "20": "Manual-400Nm",
    "08": "Manual-380Nm",
}

brakes_codes = {
    "12": "Brakes front 338(1LF)x330(1KJ)",
    "0E": "Brakes front 338(1LE)x330(1KF, 1KJ)",
    "32": "Brakes front 375(1LM,1LX,1LY,1LZ)X330(1KP,1KR,1KQ,1KY)",
    "04": "Brakes front 314(1LD,1LG)x300(1KD,1KI,1KE)",
    "0C": "Brakes front 318(1LC)x300(1KD)",
    "14": "Brakes front 338(1LE)x330(1KF/1KJ)",
    "18": "Brakes front 338(1LF)x330(1KJ)",
    "08": "Brakes front 314(1LB)x300(1KE)",
    "1C": "Brakes front 350(????)x330(???)",
    "50": "Brakes front 375(????)x330(????)",
}

byte_6 = {
    0: "FlexRay Kanal",
    1: "XDS",
    2: "HBA Low (Hydraulic Brake Assist)",
    3: "HBA High (Hydraulic Brake Assist)",
    4: "unknow bit",
    5: "Derivat low",
    6: "Derivat.",
    7: "Derivat High",
}
byte_8 = {
    0: "Passivtastung",
    1: "Charisma",
    2: "BAP Journal",
    3: "PLA",
    4: "Prefill low",
    5: "Prefill high",
    6: "TOL - (Trailer stabilizer)",
    7: "HDC - (Hill Descent Control Assistance)",
}
byte_10 = {
    0: "PP (Parkpilot)",
    1: "STP Staupilot (Start/Stop)",
    2: "KAS Kreuzungsassistent (Intersection Assist)",
    3: "KDS Kickdownschalter (kickdown)",
    4: "DTE (Roof rack detection)",
    5: "unknow bit",
    6: "VAC Low",
    7: "VAC High",
}
byte_12 = {
    0: "ABC - (active body control)",
    1: "unknow bit",
    2: "RSC - (Roll Stability Control (RSC)",
    3: "CDC - (Dynamic Chassis Control)",
    4: "Lufe - (Air Suspensions)",
    5: "Quattro on demand",
    6: "quattro sport",
    7: "HA-Q - (Rear axle transverse lock)",
}
byte_14 = {
    0: "IPA - (Intelligent Parking Assistant)",
    1: "DSR -(Driver Steering Recommendation)",
    2: "HAL - (Rear Axle Control)",
    3: "ADS -(Audi dynamic steering)",
    4: "LWR - (Headlight corrector)",
    5: "SSt-R - (pressure relief after emergency stop)",
    6: "RKA+ - (Pressure control systems based on ESP)",
    7: "RLE - (Control of wheel bolts tightening)",
}
byte_15 = {
    0: "HSP - (Rear Spoiler)",
    1: "S/S - (start/stop)",
    2: "NV - (Night Vision)",
    3: "ARA - (Trailer Maneuvering Assistant)",
    4: "GRA - (Speed Limiter PLA)",
    5: "ACC - (Adaptive Cruise Control)",
    6: "PCF - (Pre-Crash Function)",
    7: "MKB - (Multi-collision Braking System)",
}
byte_16 = {
    0: "OBD - (On Board Diagnostics)",
    1: "EPB - (Electronic Parking Brake)",
    2: "HHC - (Hill Hold Control)",
    3: "HHE - (Hill Hold extended)",
    4: "HBB - (Brake booster via control (set) point)",
    5: "BSW - (Brake Disc Wiper,brake disc drying cleaning)",
    6: "HBC - (Hill Brake Control/Hydraulic Brake Control)",
    7: "LBF - (Salt scale removal function)",
}
byte_17 = {
    0: "EPB - (Actor low)",
    1: "EPB - (Actor high)",
    2: "DoA - (Driver out apply low)",
    3: "DoA - (Driver out apply high)",
    4: "GDP - (Gradient dependent Electronic Parking Brake (EPB))",
    5: "DAA - (Dyn.StartAssist low)",
    6: "DAA - (Dyn.StartAssist high)",
    7: "DAA - (Indication)",
}
byte_18 = {
    0: "EA - (Emergency Assist)",
    1: "FCW - (Forward Collision Warning)",
    2: "ESL - (Engine Stall Logic)",
    3: "RCTA - (Rear Cross Traffic Alert with Auto-Brake when reversing with SWA (3C))",
    4: "vFGS - (Pedestrian Protection with Auto-Brake PreSense via camera)",
    5: "AVH - (Auto Vehicle Hold low)",
    6: "AVH - (Auto Vehicle Hold high Auto Hold)",
    7: "FBA - (Driver Downhill Warning always active)",
}

BYTE_MAP = {
    6: byte_6,
    8: byte_8,
    10: byte_10,
    12: byte_12,
    14: byte_14,
    15: byte_15,
    16: byte_16,
    17: byte_17,
    18: byte_18,
}


def _hex_to_bin2(s: str) -> str:
    return bin(int(s, SCALE))[2:].zfill(BITS)


def validate_code(raw: str) -> str:
    code = raw.strip().upper().replace(" ", "")
    if not code:
        raise ValueError("Empty line")
    if len(code) % 2 != 0:
        raise ValueError("Line should be devided by 2 ")
    if not re.fullmatch(r"[0-9A-F]+", code):
        raise ValueError("Only allowed 0-9 и A-F")
    return code


def parse_code(code: str) -> dict:
    """
    Returns a dictionary with the following keys:
      {
        "text": <text witn no colors>,
        "html": <HTML line for template>,
      }
    """
    code = validate_code(code)
    code_list = [code[i : i + 2] for i in range(0, len(code), 2)]

    text_lines = []
    html_lines = []

    # ASCII art: экранируем для HTML
    text_lines.append(ASCII_ART)
    html_lines.append(esc(ASCII_ART))

    text_lines.append(f"Your long coding: {code}\n")
    html_lines.append(f"{esc('Your long coding: ')}{esc(code)}\n")

    b_raw = {}

    for i, byte in enumerate(code_list):
        if i == 0:
            b_raw[0] = _hex_to_bin2(byte)
            desc = brakes_codes.get(byte, "Unknown brakes")
            text_lines.append(f"Brakes Code: {byte} => {desc}")
            html_lines.append(
                f"{esc('Brakes Code: ')}{esc(byte)}{esc(' => ')}{esc(desc)}"
            )
        elif i == 2:
            b_raw[2] = _hex_to_bin2(byte)
            desc = engine_codes.get(byte, "Unknown Engine")
            text_lines.append(f"Engine Code: {byte} => {desc}")
            html_lines.append(
                f"{esc('Engine Code: ')}{esc(byte)}{esc(' => ')}{esc(desc)}"
            )
        elif i == 3:
            desc = car_model.get(byte, "Unknown Model")
            text_lines.append(f"Car Model Code: {byte} => {desc}")
            html_lines.append(
                f"{esc('Car Model Code: ')}{esc(byte)}{esc(' => ')}{esc(desc)}"
            )
        elif i == 4:
            b_raw[4] = _hex_to_bin2(byte)
            desc = transmission_codes.get(byte, "Unknown Transmission")
            text_lines.append(f"Transmission Code: {byte} => {desc}")
            html_lines.append(
                f"{esc('Transmission Code: ')}{esc(byte)}{esc(' => ')}{esc(desc)}"
            )
        elif i in BYTE_MAP:
            raw_bits = _hex_to_bin2(byte)
            b_raw[i] = raw_bits
            text_lines.append(f"Byte {i}: {byte}, [{raw_bits}]")
            html_lines.append(
                f"{esc(f'Byte {i}: ')}{esc(byte)}{esc(', [')}{esc(raw_bits)}{esc(']')}"
            )

            bits = list(raw_bits)
            for j in range(len(bits) - 1, -1, -1):
                bit_no = (len(bits) - 1) - j
                desc = BYTE_MAP[i].get(bit_no, "Unknown Bit")
                is_on = bits[j] == "1"
                state_text = "Activated" if is_on else "Deactivated"
                state_html = GREEN(state_text) if is_on else CYAN(state_text)

                text_lines.append(f"  Bit {bit_no}: {desc} - {state_text}")
                # html_lines.append(
                #     f"&nbsp;&nbsp;{esc('Bit ')}{esc(bit_no)}{esc(': ')}{esc(desc)}{esc(' - ')}# {state_html}"
                # )
                html_lines.append(
                    f"&nbsp;&nbsp;{esc('Bit ')}{esc(bit_no)}{esc(': ')}{esc(desc)}{esc(' - ')} {state_html}"
                )

    # Mirror checks
    text_lines.append("\nMirror checks for bytes 19-30:")
    html_lines.append("<br>" + esc("Mirror checks for bytes 19-30:"))

    mirror_map = {
        19: 0,
        20: 2,
        21: 4,
        22: 6,
        23: 8,
        24: 10,
        25: 12,
        26: 14,
        27: 15,
        28: 16,
        29: 17,
        30: 18,
    }
    for i, byte in enumerate(code_list):
        if i in mirror_map:
            current = _hex_to_bin2(byte)
            mirrored = current[::-1]
            orig_idx = mirror_map[i]
            orig_val = b_raw.get(orig_idx)

            if orig_val is None:
                text_lines.append(
                    f"Byte {i}: {byte}, curr:[{current}] mirr:[{mirrored}] = SKIPPED (no base byte {orig_idx})"
                )
                html_lines.append(
                    f"{esc(f'Byte {i}: ')}{esc(byte)}{esc(', curr:[')}{esc(current)}{esc('] mirr:[')}{esc(mirrored)}{esc('] = ')}{YELLOW(f'SKIPPED (no base byte {orig_idx})')}"
                )
            else:
                ok = mirrored == orig_val
                status_text = "OK" if ok else f"NOT OK (byte {orig_idx} ↔ byte {i})"
                status_html = (
                    GREEN("OK") if ok else RED(f"NOT OK (byte {orig_idx} ↔ byte {i})")
                )

                text_lines.append(
                    f"Byte {i}: {byte}, curr:[{current}]  mirr:[{mirrored}] = {status_text}"
                )
                html_lines.append(
                    f"{esc(f'Byte {i}: ')}{esc(byte)}{esc(', curr:[')}{esc(current)}{esc(']  mirr:[')}{esc(mirrored)}{esc('] = ')}{status_html}"
                )

    # Итоговые строки
    text = "\n".join(text_lines)
    html_out = "\n".join(html_lines)

    return {"text": text, "html": html_out}
