import math

def rc_plane_performance(
    motor_kv: float,
    battery_voltage: float,
    prop_diameter_inch: float,
    prop_pitch_inch: float,
    weight_kg: float,
    battery_capacity_mAh: float,
    num_motors: int,
    esc_efficiency: float = 0.8
):
    # 1. RPM estimation
    rpm = motor_kv * battery_voltage * esc_efficiency
    
    # Unit conversions
    rho = 1.225
    n = rpm / 60
    D_m = prop_diameter_inch * 0.0254
    pitch_m = prop_pitch_inch * 0.0254
    
    # Coefficients
    Ct = 0.1
    Cp = 0.04
    
    # 2. Static Thrust
    thrust_single = Ct * rho * (n**2) * (D_m**4)
    static_thrust_N = thrust_single * num_motors

    # 3. Power & Current
    power_single = Cp * rho * (n**3) * (D_m**5)
    power_total = power_single * num_motors
    current_total_A = power_total / battery_voltage

    # 4. Flight Time (corrected)
    battery_Ah = battery_capacity_mAh / 1000
   avg_current_A = current_total_A * 0.6
flight_time_minutes = (battery_Ah / avg_current_A) * 60


    # 5. Pitch Speed
    pitch_speed_mps = rpm * pitch_m / 60

    # 6. Thrust-to-weight
    weight_N = weight_kg * 9.81
    thrust_to_weight = static_thrust_N / weight_N

    return {
        "rpm": rpm,
        "static_thrust_N": static_thrust_N,
        "current_draw_A": current_total_A,
        "max_pitch_speed_mps": pitch_speed_mps,
        "thrust_to_weight": thrust_to_weight,
        "estimated_flight_time_minutes": flight_time_minutes
    }
