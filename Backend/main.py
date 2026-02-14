from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI
from pydantic import BaseModel
from drone_calculations import calc_drone_performance
from plane_calculations import rc_plane_performance  # <-- NEW FUNCTION

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class DroneInput(BaseModel):
    motor_kv: float
    battery_voltage: float
    prop_diameter_inch: float
    prop_pitch_inch: float
    weight_kg: float
    battery_capacity_mAh: float
    num_motors: int

# ------------------------------
# RC PLANE INPUT FIXED HERE
# ------------------------------
class RCPlaneInput(BaseModel):
    motor_kv: float
    battery_voltage: float
    prop_diameter_inch: float
    prop_pitch_inch: float
    weight_kg: float
    battery_capacity_mAh: float
    num_motors: int = 1   # usually single motor RC plane

@app.post("/drone")
def drone_mode(data: DroneInput):
    return calc_drone_performance(
        data.motor_kv,
        data.battery_voltage,
        data.prop_diameter_inch,
        data.prop_pitch_inch,
        data.weight_kg,
        data.battery_capacity_mAh,
        data.num_motors
    )

@app.post("/plane")
def plane_mode(data: RCPlaneInput):
    return rc_plane_performance(
        data.motor_kv,
        data.battery_voltage,
        data.prop_diameter_inch,
        data.prop_pitch_inch,
        data.weight_kg,
        data.battery_capacity_mAh,
        data.num_motors
    )
