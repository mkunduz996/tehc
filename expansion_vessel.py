import math
from iapws import IAPWS97

def water_density(temp_c, pressure_bar):
    """Return water density in kg/m^3 at given temperature (C) and pressure (bar)."""
    # Convert to Kelvin and MPa
    T = temp_c + 273.15
    P = pressure_bar * 0.1
    w = IAPWS97(T=T, P=P)
    return w.rho

def expansion_vessel_volume(fluid, system_volume_l, p_min_bar, p_max_bar, t_initial_c, t_final_c):
    if fluid.lower() != "water":
        raise ValueError("Only water is supported")
    # Convert pressures to absolute
    p_min_abs = p_min_bar + 1.0
    p_max_abs = p_max_bar + 1.0
    if p_max_abs <= p_min_abs:
        raise ValueError("Maximum pressure must be greater than minimum pressure")

    rho_i = water_density(t_initial_c, p_min_abs)
    rho_f = water_density(t_final_c, p_max_abs)

    # expansion volume due to temperature increase
    v_expansion = system_volume_l * (rho_i / rho_f - 1)

    # vessel volume from Boyle's law
    v_vessel = (p_max_abs * v_expansion) / (p_max_abs - p_min_abs)
    return v_vessel


def main():
    fluid = input("Fluid type (water): ") or "water"
    system_volume = float(input("Total system volume [L]: "))
    p_min = float(input("Minimum working pressure [bar]: "))
    p_max = float(input("Maximum working pressure [bar]: "))
    t_initial = float(input("Initial temperature [C]: "))
    t_final = float(input("Final temperature [C]: "))
    vol = expansion_vessel_volume(fluid, system_volume, p_min, p_max, t_initial, t_final)
    print(f"Required expansion vessel volume: {vol:.2f} L")

if __name__ == "__main__":
    main()
