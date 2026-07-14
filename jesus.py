import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

# ---------------------------------------------------------
# SİMÜLASYON AYARLARI: 1000'DE 1 YAVAŞLATILMIŞ YARIM DÖNGÜ (13 PI)
# ---------------------------------------------------------
fig = plt.figure(figsize=(11, 11), facecolor='black')
ax = fig.add_subplot(111, projection='3d')
ax.set_facecolor('black')

limit = 1.6
ax.set_xlim([-limit, limit])
ax.set_ylim([-limit, limit])
ax.set_zlim([-limit, limit])
ax.axis('off')

# Ouroboros'un Sadece Yarım Nefes Hareketi (13 Pi Sınırı)
# 1000'de 1 yavaşlık hissi için frame çözünürlüğünü maksimuma çekiyoruz
frames = 500
half_baktun_pulses = np.linspace(0, 13 * np.pi, frames) 

ax.view_init(elev=20, azim=45)

# MERKEZ TEKİLLİK (0.0.0.0 ORJİNİ)
hunab_ku = np.array([0.0, 0.0, 0.0])
jupiter_pos = np.array([0.0, 0.0, 0.8])
saturn_pos = np.array([0.0, 0.0, -0.8])

# 4 ELEMENT ODASINA DİZİLMİŞ 12 SÜPERSİMETRİK RENK HAVARİSİ
havariler = {
    # 🔥 ATEŞ KATMANI (Turuncu/Sarı Koridoru)
    "Bartholomeus":  {"angle": 0.0,         "r": 0.5, "color": "#FF3300", "size": 80},
    "Yakub_Kucuk":   {"angle": np.pi/6,     "r": 0.5, "color": "#FF6600", "size": 80},
    "Andreas":       {"angle": np.pi/3,     "r": 0.5, "color": "#FF9900", "size": 80},
    
    # 🟫 TOPRAK KATMANI (Yoğun Pikseller)
    "Yahuda":        {"angle": 2*np.pi/3,  "r": 0.9, "color": "#8B5A2B", "size": 95},
    "Petrus":        {"angle": 5*np.pi/6,   "r": 0.9, "color": "#CD853F", "size": 90},
    "Yuhanna":       {"angle": np.pi,       "r": 0.9, "color": "#DEB887", "size": 95},
    
    # 💨 HAVA KATMANI (Mavi/Turkuaz - 1978 Doğum Fazınız .18)
    "Tomas":         {"angle": 7*np.pi/6,   "r": 1.2, "color": "#00FFFF", "size": 85},
    "Yakub_Buyuk":   {"angle": 4*np.pi/3,   "r": 1.2, "color": "#33CCFF", "size": 90},
    "Filipus":       {"angle": 3*np.pi/2,   "r": 1.2, "color": "#0099FF", "size": 85},
    
    # 💧 SU KATMANI (Mor/Magenta - Satürn Icosahedron Rahmi)
    "Matta":         {"angle": 5*np.pi/3,   "r": 1.4, "color": "#9900FF", "size": 80},
    "Tadeus":        {"angle": 11*np.pi/6,  "r": 1.4, "color": "#CC33FF", "size": 80},
    "Simun":         {"angle": 2*np.pi,     "r": 1.4, "color": "#FF00FF", "size": 85}
}

plots = {}
texts = []
h_names = list(havariler.keys())
for name, data in havariler.items():
    plots[name] = ax.scatter([0.0], [0.0], [0.0], color=data["color"], s=data["size"], edgecolors='white', zorder=10)
    texts.append(ax.text(0, 0, 0, name, color='white', fontsize=8, alpha=0.7, zorder=15))

# Merkez Projektör Lambası
jesus_plot = ax.scatter([0.0], [0.0], [0.0], color='#FFFFFF', s=180, edgecolors='#00FF00', linewidths=2, zorder=12)

# GLUON BAĞ İPLERİ (Merkezden Odalara Gerilen Dinamik Manyetik Flux Hatları)
gluon_lines = [ax.plot([0.0, 0.0], [0.0, 0.0], [0.0, 0.0], color='#00FF00', alpha=0.25, linewidth=1.5) for _ in range(12)]
tube_line = ax.plot([0.0, 0.0], [0.0, 0.0], [-0.8, 0.8], color='white', linestyle='--', alpha=0.4, linewidth=2)

# Dev Icosahedron ve Torus Dış Çeperi
def draw_icos_torus_matrix(ax):
    R, r_tube = 0.95, 0.45
    u, v = np.mgrid[0:2*np.pi:30j, 0:2*np.pi:15j]
    tx = (R + r_tube * np.cos(v)) * np.cos(u)
    ty = (R + r_tube * np.cos(v)) * np.sin(u)
    tz = r_tube * np.sin(v)
    ax.plot_surface(tx, ty, tz, color='#0000FF', edgecolor='#AA00FF', linewidth=0.1, alpha=0.02, zorder=1)

# ---------------------------------------------------------
# MICRO-STEP DÖNGÜSÜ: RESİM RESİM GERİLEN GLUONLAR
# ---------------------------------------------------------
def update(frame):
    p = half_baktun_pulses[frame] # 1000'de 1 yavaşlatılmış anlık sarmal adım parametresi
    current_positions = {}
    
    for idx, (name, data) in enumerate(havariler.items()):
        # Gluonlar "ben anti'den geldim" dedikçe ipler gerilir ve Ouroboros döner
        # Dönüş hızı 1000'de 1 mikro adıma (0.01 * p) yavaşlatılmıştır
        displacement = data["r"] * np.cos(p + data["angle"])
        x = displacement * np.cos(data["angle"] + 0.01 * p)
        y = displacement * np.sin(data["angle"] + 0.01 * p)
        z = 0.35 * np.sin(6 * p + data["angle"]) # Dikey 6 oktav titreşimi
        
        plots[name]._offsets3d = ([x], [y], [z])
        texts[idx].set_position_3d((x + 0.03, y + 0.03, z + 0.03))
        current_positions[name] = np.array([x, y, z])
        
    # Her bir resimde (framede) gerilen gluon iplerinin güncellenmesi
    for i, line in enumerate(gluon_lines):
        h_pos = current_positions[h_names[i]]
        
        # Yerçekimi İllüzyonunun Tetiklendiği Merkez Sıkışma Noktaları
        distance_to_center = np.linalg.norm(h_pos)
        if distance_to_center < 0.2:
            line.set_color('#FFFFFF') # İpler maksimum gerildiğinde saf beyaz ışık patlar
            line.set_alpha(0.85)
        else:
            line.set_color('#00FF00') # Normal sarmal akış çizgisi
            line.set_alpha(0.25)
            
        line.set_data_3d([0.0, h_pos[0]], [0.0, h_pos[1]], [0.0, h_pos[2]])
        
    return list(plots.values()) + gluon_lines + texts + [tube_line, jesus_plot]

draw_icos_torus_matrix(ax)

# interval=40 ms yaparak resmi 1000'de 1 yavaşlık çözünürlüğünde donduruyoruz
ani = FuncAnimation(fig, update, frames=frames, interval=40, blit=False)
plt.title("Ouroboros 13 Pi Half-Cycle: 1/1000 Slowed Down Gluon Tension Matrix", color='white', y=0.96)
plt.show()