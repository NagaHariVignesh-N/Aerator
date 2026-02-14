import math

def calc_drone_performance(
    motor_kv,
    battery_voltage,
    prop_diameter_inch,
    prop_pitch_inch,
    weight_kg,
    battery_capacity_mAh,
    num_motors
):

    # ------------------------------------------------
    # SAFETY LOW VOLTAGE
    # ------------------------------------------------
    if battery_voltage < 10:
        return {
            "battery_status": "SAFE LANDING – LOW VOLTAGE",
            "rpm": 0,
            "thrust_per_motor": 0,
            "total_thrust": 0,
            "thrust_to_weight": 0,
            "hover_current": 0,
            "flight_time_min": 0,
            "rpm_graph": [],
            "speed_graph": []
        }

    # ------------------------------------------------
    # RPM UNDER LOAD
    # ------------------------------------------------
    rpm = motor_kv * battery_voltage * 0.85
    n = rpm / 60  # rev/s

    # ------------------------------------------------
    # PROP GEOMETRY
    # ------------------------------------------------
    rho = 1.225
    D = prop_diameter_inch * 0.0254
    pitch_m = prop_pitch_inch * 0.0254

    # ------------------------------------------------
    # UNIVERSAL Ct MODEL (REALISTIC)
    # ------------------------------------------------
    pitch_ratio = prop_pitch_inch / prop_diameter_inch

    # 5" props have higher Ct, 30" props have lower Ct
    Ct_base = 0.25 / math.sqrt(prop_diameter_inch)

    # adjust for pitch
    Ct = Ct_base * (0.6 + pitch_ratio)

    # clamp realistic range
    Ct = max(0.02, min(Ct, 0.14))

    # ------------------------------------------------
    # STATIC THRUST FORMULA
    # ------------------------------------------------
    thrust_per_motor = Ct * rho * (n ** 2) * (D ** 4)
    total_thrust = thrust_per_motor * num_motors

    weight_N = weight_kg * 9.81
    thrust_to_weight = total_thrust / weight_N if weight_N else 0

    # ------------------------------------------------
    # HOVER CURRENT MODEL
    # ------------------------------------------------
    max_current = (rpm / 1000) * (D * 25)   # scales with prop load

    hover_current = (weight_N / total_thrust) * max_current if total_thrust > 0 else 0
    hover_current = max(0.5, hover_current)

    # ------------------------------------------------
    # FLIGHT TIME
    # ------------------------------------------------
    usable_Ah = (battery_capacity_mAh / 1000) * 0.8
    flight_time_min = (usable_Ah / hover_current) * 60 if hover_current else 0

    flight_time_min = max(0, min(flight_time_min, 35))  # universal cap

    # ------------------------------------------------
    # GRAPHS
    # ------------------------------------------------
    rpm_graph = []
    for val in range(3000, int(rpm), 500):
        n_val = val / 60
        t_val = Ct * rho * (n_val ** 2) * (D ** 4)
        rpm_graph.append({"rpm": val, "thrust": t_val})

    speed_graph = []
    for val in range(3000, int(rpm), 500):
        speed = (val * pitch_m) / 60
        power = speed * thrust_per_motor
        speed_graph.append({"speed": speed, "power": power})

    return {
        "battery_status": "NORMAL",
        "rpm": rpm,
        "thrust_per_motor": thrust_per_motor,
        "total_thrust": total_thrust,
        "thrust_to_weight": thrust_to_weight,
        "hover_current": hover_current,
        "flight_time_min": flight_time_min,
        "rpm_graph": rpm_graph,
        "speed_graph": speed_graph
    }
