from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse, JSONResponse, PlainTextResponse
from fastapi.templating import Jinja2Templates
from .parser import parse_code, validate_code

app = FastAPI(title="ESP Long Coding Decoder", version="1.0.0")
templates = Jinja2Templates(directory="app/templates")
CAR_FEATURES = [
    (
        "ESP",
        "Electronic Stability Program - helps maintain control during skidding",
        "✔",
    ),
    (
        "ABS",
        "Anti-lock Braking System - prevents wheels from locking during braking",
        "✔",
    ),
    ("TPMS", "Tire Pressure Monitoring System - monitors tire pressure levels", "✔"),
    ("ACC", "Adaptive Cruise Control - adjusts speed to maintain safe distance", "✔"),
    ("LKA", "Lane Keeping Assist - helps keep vehicle within lane lines", "✔"),
    (
        "AEB",
        "Autonomous Emergency Braking - automatically applies brakes to avoid collisions",
        "✔",
    ),
    ("TSR", "Traffic Sign Recognition - detects and displays road signs", "✔"),
    ("HUD", "Head-Up Display - projects information onto the windshield", "✔"),
    (
        "LDWS",
        "Lane Departure Warning System - alerts driver when leaving lane unintentionally",
        "✔",
    ),
    ("FLEXRAY", "FlexRay Kanal - fast and reliable vehicle communication bus", "✔"),
    ("XDS", "Electronic Differential Lock - improves traction during cornering", "✔"),
    ("HBA_L", "Hydraulic Brake Assist - low variant", "✔"),
    ("HBA_H", "Hydraulic Brake Assist - high variant", "✔"),
    ("DRV_L", "Vehicle configuration coding (low)", "?"),
    ("DRV", "Vehicle configuration coding (base)", "?"),
    ("DRV_H", "Vehicle configuration coding (high)", "?"),
    ("PASS", "Passive key detection (e.g. keyless entry polling)", "?"),
    ("CHARISMA", "Drive Profile Selection (e.g. Comfort/Sport)", "✔"),
    ("BAP", "Body Application Protocol - vehicle body communication", "?"),
    ("PLA", "Park Assist - assists in parking maneuvers", "✔"),
    ("PREFILL_L", "Brake pre-fill function - low variant", "✔"),
    ("PREFILL_H", "Brake pre-fill function - high variant", "✔"),
    ("TOL", "Trailer stabilizer - improves trailer stability", "✔"),
    ("HDC", "Hill Descent Control - assists braking on downhill slopes", "✔"),
    ("PP", "Parkpilot - visual/audio parking assist system", "✔"),
    ("STP", "Traffic Jam Pilot - low-speed driving assist in traffic", "✔"),
    ("KAS", "Intersection Assist - warns/acts at intersections", "✔"),
    ("KDS", "Kickdown Switch - full throttle detection switch", "✔"),
    ("DTE", "Roof rack detection - detects roof loads", "✔"),
    ("VAC_L", "Vacuum brake assist - low variant", "?"),
    ("VAC_H", "Vacuum brake assist - high variant", "?"),
    ("ABC", "Active Body Control - advanced suspension control", "?"),
    ("RSC", "Roll Stability Control - prevents rollover during cornering", "✔"),
    ("CDC", "Dynamic Chassis Control - adapts damping to road conditions", "✔"),
    ("LUFE", "Air Suspensions - adjustable suspension height", "✔"),
    ("QUAT_OD", "Quattro on demand - AWD only when needed", "✔"),
    ("QUAT_S", "Quattro sport - performance-oriented AWD", "✔"),
    ("HA_Q", "Rear axle transverse lock - improved traction on rear axle", "✔"),
    ("IPA", "Intelligent Parking Assistant - automates parking tasks", "✔"),
    ("DSR", "Driver Steering Recommendation - suggests corrective steering", "✔"),
    ("HAL", "Rear Axle Control - controls rear wheel steering", "✔"),
    ("ADS", "Audi Dynamic Steering - variable steering ratio", "✔"),
    ("LWR", "Headlight leveling - adjusts based on load", "✔"),
    ("SSTR", "Brake pressure relief after emergency stop", "✔"),
    ("RKA+", "Tire pressure monitoring integrated into ESP", "✔"),
    ("RLE", "Wheel bolt loosening detection", "✔"),
    ("HSP", "Rear Spoiler - active aerodynamic control", "✔"),
    ("S/S", "Start/Stop - engine shutdown at idle", "✔"),
    ("NV", "Night Vision - detects pedestrians/animals at night", "✔"),
    ("ARA", "Trailer Maneuvering Assistant - aids reversing with trailer", "✔"),
    (
        "GRA",
        "Cruise Control/Speed Limiter - keep speed/restricts max vehicle speed",
        "✔",
    ),
    ("PCF", "Pre-Crash Function - prepares vehicle for impact", "✔"),
    ("MKB", "Multi-collision Brake - auto-brake after initial crash", "✔"),
    ("OBD", "On-Board Diagnostics - diagnostic access to systems", "✔"),
    ("EPB", "Electronic Parking Brake - replaces manual handbrake", "✔"),
    ("HHC", "Hill Hold Control - prevents rollback on inclines", "✔"),
    ("HHE", "Extended Hill Hold - longer hold duration", "✔"),
    ("HBB", "Brake booster via control point - electronic brake pressure assist", "✔"),
    ("BSW", "Brake Disc Wiper - removes water from brake discs", "✔"),
    ("HBC", "Brake booster failure fallback control", "✔"),
    ("LBF", "Salt deposit removal function - prevents corrosion", "✔"),
    ("EPB_L", "EPB actuator - low variant", "✔"),
    ("EPB_H", "EPB actuator - high variant", "✔"),
    ("DOA_L", "Driver-out apply - activates EPB if driver exits (low)", "✔"),
    ("DOA_H", "Driver-out apply - activates EPB if driver exits (high)", "✔"),
    ("GDP", "Gradient dependent EPB - adapts to slope", "✔"),
    ("DAA_L", "Dynamic Start Assist - hill-start help (low)", "✔"),
    ("DAA_H", "Dynamic Start Assist - hill-start help (high)", "✔"),
    ("DAA_IND", "Dynamic Start Assist indication - visual feedback", "✔"),
    ("EA", "Emergency Assist - auto-stop if driver unresponsive", "✔"),
    ("FCW", "Forward Collision Warning - alerts before front impact", "✔"),
    ("ESL", "Engine Stall Logic or Electronic Steering Lock", "?"),
    ("RCTA", "Rear Cross Traffic Alert - warns during reverse", "✔"),
    ("VFGS", "Pedestrian Protection - brakes if person detected", "✔"),
    ("AVH_L", "Auto Vehicle Hold - basic hill hold", "✔"),
    ("AVH_H", "Auto Vehicle Hold - full-feature auto-hold", "✔"),
    ("FBA", "Driver Downhill Warning - downhill speed reminder", "✔"),
]


@app.get("/healthz", response_class=PlainTextResponse)
def healthz():
    return "ok"


@app.get("/", response_class=HTMLResponse)
async def index(request: Request):
    return templates.TemplateResponse(
        "index.html", {"request": request, "car_features": CAR_FEATURES}
    )


@app.post("/decode", response_class=HTMLResponse)
async def decode_form(request: Request, code: str = Form(...)):
    try:
        data = parse_code(code)
        html_text = data["html"]
        return templates.TemplateResponse(
            "index.html",
            {
                "request": request,
                "result": html_text,
                "error": None,
                "car_features": CAR_FEATURES,  # ✅ добавляем!
            },
        )
    except Exception as e:
        return templates.TemplateResponse(
            "index.html",
            {
                "request": request,
                "result": None,
                "error": str(e),
                "car_features": CAR_FEATURES,  # ✅ добавляем!
            },
        )


@app.post("/api/decode")
async def decode_api(payload: dict):
    code = payload.get("code", "")
    try:
        validate_code(code)
        data = parse_code(code)
        return JSONResponse({"ok": True, "output": data})
    except Exception as e:
        return JSONResponse({"ok": False, "error": str(e)}, status_code=400)
