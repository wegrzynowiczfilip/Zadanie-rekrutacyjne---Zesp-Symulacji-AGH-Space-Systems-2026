import numpy as np
from rocketpy import Environment, GenericMotor, Rocket, Flight

#Środowisko startowe (Poligon EuRoC - Santa Margarida, Portugalia)
env = Environment(
    latitude=39.39,
    longitude=-8.29,
    elevation=160
)
env.set_atmospheric_model(type="standard_atmosphere")

#Silnik Zawisza 9k (GenericMotor pod pliki .eng i paliwa ciekłe)
motor = GenericMotor(
    thrust_source="zawisza_9k.eng",
    burn_time=11.0,
    dry_mass=12.0,                  #Masa silnika (kg)
    dry_inertia=(0.5, 0.5, 0.05),   #Moment bezwładności silnika
    propellant_initial_mass=22.0,   #Masa paliwa (kg)
    chamber_radius=0.09,            #r komory (m)
    chamber_height=1.2,             #Długość komory silnika (m)
    chamber_position=0.6,           #Pozycja środka komory od dna (m)
    nozzle_radius=0.045,            #Promień wylotu dyszy (m)
    nozzle_position=0.0,            #Pozycja dyszy na dnie kadłuba
    coordinate_system_orientation="nozzle_to_combustion_chamber"
)

#Płatowiec rakiety
rocket = Rocket(
    radius=0.10,                    #r=10 cm (średnica 20 cm)
    mass=31.4,                      #Masa bez silnika 
    inertia=(1.2, 58.0, 58.0),      #Szacunkowe momenty bezwładności
    power_off_drag="drag_curve_clean.csv",
    power_on_drag="drag_curve_clean.csv",
    center_of_mass_without_motor=2.20,
    coordinate_system_orientation="tail_to_nose"
)
rocket.add_motor(motor, position=0.0)

#Dwustopniowy układ odzysku (Dual-Deployment)
rocket.add_parachute(
    name="Drogue",
    cd_s=0.85,                      #Mniejszy spadochron hamujący w apogeum
    trigger="apogee",
    sampling_rate=100,
    lag=1.5
)

rocket.add_parachute(
    name="Main",
    cd_s=11.08,                     #Głowny spadochron według planu w OpenRocket otwiera sie na 450m
    trigger=lambda p, h, y: h <= 450 + 160 and y[5] < 0, #+ 160m bo z na takiej znajduje sie poligon EuRoC
    sampling_rate=100,
    lag=2.0
)

#6-DOF (szyna 12 m, kąt 84° względem poziomu)
flight = Flight(
    rocket=rocket,
    environment=env,
    rail_length=12.0,
    inclination=84,
    heading=0
)

flight.plots.trajectory_3d()
flight.plots.linear_kinematics()
flight.plots.flight_path()