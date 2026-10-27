import numpy as np
import matplotlib.pyplot as plt
from rocketpy import Environment, GenericMotor, Rocket, Flight, Function

def create_rocket():
    """Funkcja pomocnicza generująca model rakiety ciekłej."""
    motor = GenericMotor(
        thrust_source="zawisza_9k.eng",
        burn_time=11.0,
        dry_mass=12.0,
        dry_inertia=(0.5, 0.5, 0.05),
        propellant_initial_mass=22.0,
        chamber_radius=0.09,
        chamber_height=1.2,
        chamber_position=0.6,
        nozzle_radius=0.045,
        nozzle_position=0.0,
        coordinate_system_orientation="nozzle_to_combustion_chamber"
    )

    rocket = Rocket(
        radius=0.10,
        mass=31.4,
        inertia=(1.2, 58.0, 58.0),
        power_off_drag="drag_curve_clean.csv",
        power_on_drag="drag_curve_clean.csv",
        center_of_mass_without_motor=2.20,
        coordinate_system_orientation="tail_to_nose"
    )
    rocket.add_motor(motor, position=0.0)

    #Układ odzysku (Dual-Deployment)
    rocket.add_parachute(
        name="Drogue",
        cd_s=0.85,
        trigger="apogee",
        sampling_rate=100,
        lag=1.5
    )
    rocket.add_parachute(
        name="Main",
        cd_s=11.08,
        trigger=lambda p, h, y: h <= 610 and y[5] < 0,
        sampling_rate=100,
        lag=2.0
    )
    return rocket

#analiza na wiatr boczny 0,3,5,6,9
wind_speeds = [0, 3, 6, 9]
apogees_wind = []
drifts_wind = []

print("\n" + "="*70)
print(" 1. ANALIZA WPŁYWU WIATRU BOCZNEGO (KĄT RAMPY: 84°)")
print("="*70)
print(f"{'Wiatr [m/s]':<12} | {'Apogeum [m AGL]':<16} | {'Znoszenie [m]':<14} | {'V zejścia [m/s]':<16}")
print("-" * 70)

for w in wind_speeds:
    env = Environment(latitude=39.39, longitude=-8.29, elevation=160)
    env.set_atmospheric_model(type="standard_atmosphere")
    #Wiatr boczny w osi X
    env.wind_velocity_x = Function(w)
    env.wind_velocity_y = Function(0)

    rocket = create_rocket()
    flight = Flight(
        rocket=rocket,
        environment=env,
        rail_length=12.0,
        inclination=84,
        heading=0
    )

    apogee_agl = flight.apogee - env.elevation
    drift_distance = np.sqrt(flight.x_impact**2 + flight.y_impact**2)
    v_rail = flight.out_of_rail_velocity

    apogees_wind.append(apogee_agl)
    drifts_wind.append(drift_distance)

    print(f"{w:<12} | {apogee_agl:<16.1f} | {drift_distance:<14.1f} | {v_rail:<16.2f}")

#Analiza kątu rapy 82,84,96 
angles = [82, 84, 86]
apogees_angle = []
drifts_angle = []

print("\n" + "="*70)
print(" 2. ANALIZA WPŁYWU KĄTA RAMPY STARTOWEJ (WIATR: 0 m/s)")
print("="*70)
print(f"{'Kąt [°]':<12} | {'Apogeum [m AGL]':<16} | {'Znoszenie [m]':<14} | {'V zejścia [m/s]':<16}")
print("-" * 70)

for ang in angles:
    env = Environment(latitude=39.39, longitude=-8.29, elevation=160)
    env.set_atmospheric_model(type="standard_atmosphere")

    rocket = create_rocket()
    flight = Flight(
        rocket=rocket,
        environment=env,
        rail_length=12.0,
        inclination=ang,
        heading=0
    )

    apogee_agl = flight.apogee - env.elevation
    drift_distance = np.sqrt(flight.x_impact**2 + flight.y_impact**2)
    v_rail = flight.out_of_rail_velocity

    apogees_angle.append(apogee_agl)
    drifts_angle.append(drift_distance)

    print(f"{ang:<12} | {apogee_agl:<16.1f} | {drift_distance:<14.1f} | {v_rail:<16.2f}")

#Generuje obrazki
plt.figure(figsize=(12, 5))

#Wykres 1: Wpływ wiatru na pułap i znoszenie
plt.subplot(1, 2, 1)
plt.plot(wind_speeds, apogees_wind, 'ro-', linewidth=2, label="Pułap apogeum (AGL)")
plt.axhline(9000, color='gray', linestyle='--', label="Cel EuRoC (9000 m)")
plt.title("Wpływ wiatru bocznego (Weathercocking)")
plt.xlabel("Prędkość wiatru bocznego [m/s]")
plt.ylabel("Wysokość apogeum [m]")
plt.grid(True, linestyle=":")
plt.legend()

#Wykres 2: Wpływ kąta rampy na apogeum
plt.subplot(1, 2, 2)
plt.plot(angles, apogees_angle, 'bs-', linewidth=2, label="Pułap apogeum (AGL)")
plt.axhline(9000, color='gray', linestyle='--', label="Cel EuRoC (9000 m)")
plt.title("Wpływ kąta pochylenia szyny startowej")
plt.xlabel("Kąt rampy startowej [°]")
plt.ylabel("Wysokość apogeum [m]")
plt.grid(True, linestyle=":")
plt.legend()

plt.tight_layout()
plt.savefig("sensitivity_results.png", dpi=300)
print("\n[OK] Zapisano zbiorczy wykres wrażliwości do pliku: sensitivity_results.png")
plt.show()