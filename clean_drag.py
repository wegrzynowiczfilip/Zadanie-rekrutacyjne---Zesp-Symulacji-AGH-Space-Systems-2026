import numpy as np

mach_list = []
cd_list = []

with open("drag_curve.csv", "r", encoding="utf-8") as f:
    for line in f:
        line = line.strip()
        if not line or line.startswith("#"):
            continue
        parts = line.split(",")
        if len(parts) == 2:
            try:
                cd_val = float(parts[0])
                mach_val = float(parts[1])
                if mach_val > 0.001:
                    mach_list.append(mach_val)
                    cd_list.append(cd_val)
            except ValueError:
                continue

data = sorted(zip(mach_list, cd_list), key=lambda x: x[0])
unique_mach = []
unique_cd = []

last_m = -1.0
for m, cd in data:
    if m > last_m + 1e-4:
        unique_mach.append(m)
        unique_cd.append(cd)
        last_m = m

clean_matrix = np.column_stack((unique_mach, unique_cd))
np.savetxt("drag_curve_clean.csv", clean_matrix, delimiter=",", fmt="%.5f")

print(f"Sukces: Wygenerowano drag_curve_clean.csv ({len(unique_mach)} punktow).")