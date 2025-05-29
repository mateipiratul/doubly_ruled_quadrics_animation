import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation, PillowWriter

# --- parametrii hiperboloidului ---
a = 2.0          # semiaxa asociata x pentru elipsa din z=0
b = 1.5          # semiaxa asociata y pentru elipsa din z=0
c_eq = 2.0       # parametrul 'c' din x^2/a^2 + y^2/b^2 - z^2/c_eq^2 = 1
                 # Smaller c_eq -> more pronounced waist/skew.
                 # micsorarea parametrului c_eq modifica inclinatia dreptelor

z_max = 3.0      # lungimea unei drepte
num_lines = 20   # numarul de drepte dintr-o familie
num_points_per_line = 50 # arbitrar, numarul de puncte de pe o dreapta

# --- parametrii animatiei ---
num_frames = 360         # numarul total de frame-uri pentru o rotatie completa
fps = 60                 # cadre pe secunda
initial_elevation = 25   # unghiul de elevatie
output_filename_gif = "animatie_cuadrica_dubluriglata.gif"

# --- setup axe 3D ---
fig = plt.figure(figsize=(9, 8)) # ajustare marime
ax = fig.add_subplot(111, projection='3d')
fig.patch.set_facecolor('white') # fundal alb
ax.set_facecolor('white') # axe de reprezentare albe

# --- generarea datelor despre linii ---
s_values = np.linspace(-z_max, z_max, num_points_per_line)
alpha_values = np.linspace(0, 2 * np.pi, num_lines, endpoint=False)

lines_data = []

# familia 1
for alpha in alpha_values:
    x_line1 = a * (np.cos(alpha) - (s_values / c_eq) * np.sin(alpha))
    y_line1 = b * (np.sin(alpha) + (s_values / c_eq) * np.cos(alpha))
    z_line1 = s_values
    lines_data.append({'x': x_line1, 'y': y_line1, 'z': z_line1, 'color': 'blue', 'linewidth': 1.2})

# familia 2
for alpha in alpha_values:
    x_line2 = a * (np.cos(alpha) + (s_values / c_eq) * np.sin(alpha))
    y_line2 = b * (np.sin(alpha) - (s_values / c_eq) * np.cos(alpha))
    z_line2 = s_values
    lines_data.append({'x': x_line2, 'y': y_line2, 'z': z_line2, 'color': 'red', 'linewidth': 1.2})

# --- functia de animare ---

def update_frame(frame_number): # functia de desenare a unui singur cadru
    ax.clear() # reimprospatarea cadrului
    ax.set_facecolor('white') # reaplicarea fundalului alb

    for line_props in lines_data: # improspatarea pozitiilor liniilor
        ax.plot(line_props['x'], line_props['y'], line_props['z'],
                color=line_props['color'], linewidth=line_props['linewidth'])

    ax.set_xticks([])
    ax.set_yticks([])
    ax.set_zticks([])
    ax.set_xlabel("")
    ax.set_ylabel("")
    ax.set_zlabel("")
    ax.set_title("")
    ax.grid(False)
    ax.set_title("Cuadrică dublu-riglată")

    # extinderea maxima a liniilor pana la  s = z_max
    # pentru x: a * (cos(alpha) - (z_max/c_eq) * sin(alpha)). valoarea maxima este: a * sqrt(1 + (z_max/c_eq)^2)
    max_coord_factor = np.sqrt(1 + (z_max/c_eq)**2)
    axis_limit_x = a * max_coord_factor * 1.1
    axis_limit_y = b * max_coord_factor * 1.1
    axis_limit_z = z_max * 1.1

    ax.set_xlim([-axis_limit_x, axis_limit_x])
    ax.set_ylim([-axis_limit_y, axis_limit_y])
    ax.set_zlim([-axis_limit_z, axis_limit_z])
    ax.grid(True)

    azimuth_angle_deg = frame_number * (360 / num_frames)
    ax.view_init(elev=initial_elevation, azim=azimuth_angle_deg)

    return fig,

print("generarea cadrelor animatiei")
animation = FuncAnimation(fig, update_frame, frames=num_frames,
                          interval=(1000 / fps), blit=False)

try:
    print(f"salvarea animatiei ca: {output_filename_gif}")
    writer = PillowWriter(fps=fps)
    animation.save(output_filename_gif, writer=writer)
    print(f"animatie salvata ca: {output_filename_gif}")
except Exception as e:
    print(f"eroare salvare: {e}")

print("script terminat")