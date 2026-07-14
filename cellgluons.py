import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

# ---------------------------------------------------------
# SİMÜLASYON AYARLARI VE 9 KATMANLI HÜCRE DOĞUM ALGORİTMASI
# ---------------------------------------------------------
fig = plt.figure(figsize=(10, 10), facecolor='black')
ax = fig.add_subplot(111, projection='3d')
ax.set_facecolor('black')

limit = 1.6
ax.set_xlim([-limit, limit])
ax.set_ylim([-limit, limit])
ax.set_zlim([-limit, limit])
ax.axis('off')

frames = 360
time_steps = np.linspace(0, 4 * np.pi, frames)

# İlk kamera açısı (Sağa panlayarak Jüpiter-Satürn ve Hücre eksenini döndürebilirsiniz!)
ax.view_init(elev=20, azim=45)

# Z EKSENİNDE DOĞAN 2 MERKEZ GLUON (JÜPİTER & SATÜRN / İĞ İPLİKLERİ)
jupiter_pos = np.array([0, 0, 0.8])
saturn_pos = np.array([0, 0, -0.8])

# ---------------------------------------------------------
# GÜNCELLENMİŞ VE NETLEŞTİRİLMİŞ HÜCRE ÇEPERLERİ (CELL WALL BRIGHTNESS)
# ---------------------------------------------------------
def draw_cellular_spheres(ax):
    u, v = np.mgrid[0:2*np.pi:20j, 0:np.pi:10j]
    
    # 1. Üst Hücre Odası (Jüpiter / Turuncu-Sarı Çeper)
    x1 = 0.7 * np.cos(u) * np.sin(v)
    y1 = 0.7 * np.sin(u) * np.sin(v)
    z1 = 0.7 * np.cos(v) + 0.4
    ax.plot_surface(x1, y1, z1, color='#FFAA00', edgecolor='#FFAA00', linewidth=0.2, alpha=0.15)
    
    # 2. Alt Hücre Odası (Satürn / Mavi-Mor Çeper)
    x2 = 0.7 * np.cos(u) * np.sin(v)
    y2 = 0.7 * np.sin(u) * np.sin(v)
    z2 = 0.7 * np.cos(v) - 0.4
    ax.plot_surface(x2, y2, z2, color='#0055FF', edgecolor='#0055FF', linewidth=0.2, alpha=0.15)
    
    # 3. Ortak Yaşam Çemberi Çeperi (Dünya-Mars / Yeşil Çakra Hücre Zarı)
    x3 = 0.8 * np.cos(u) * np.sin(v)
    y3 = 0.8 * np.sin(u) * np.sin(v)
    z3 = 0.8 * np.cos(v)
    ax.plot_surface(x3, y3, z3, color='#00FF00', edgecolor='#00FF00', linewidth=0.1, alpha=0.08)

# ---------------------------------------------------------
# Y-Z EKSENİ DOĞUM DENGELİ GLUON MATRİSİ
# ---------------------------------------------------------
planets = {
    "Merkür": {"r": 0.4, "color": "orange", "angle": 0,       "phase": 0,       "size": 60},
    "Venüs":   {"r": 0.4, "color": "yellow", "angle": 0,       "phase": np.pi,   "size": 80},
    "Dünya":   {"r": 0.8, "color": "green",  "angle": 2*np.pi/3, "phase": 0,       "size": 90},
    "Mars":    {"r": 0.8, "color": "red",    "angle": 2*np.pi/3, "phase": np.pi,   "size": 70},
    "Uranüs":  {"r": 1.2, "color": "cyan",   "angle": 4*np.pi/3, "phase": 0,       "size": 100},
    "Neptün":  {"r": 1.2, "color": "purple", "angle": 4*np.pi/3, "phase": np.pi,   "size": 95}
}

plots = {}
for name, data in planets.items():
    plots[name] = ax.scatter([], [], [], color=data["color"], s=data["size"], edgecolors='white', zorder=10)

# SYNTAX HATASI DÜZELTİLDİ: Boş virgüller [0, 0] ve [0, 0] matrisleriyle dolduruldu.
tube_line = ax.plot([0, 0], [0, 0], [-0.8, 0.8], color='white', linestyle='--', alpha=0.6, linewidth=2.5)
jup_point = ax.scatter([0], [0], [0.8], color='white', s=140, edgecolors='black', zorder=12)
sat_point = ax.scatter([0], [0], [-0.8], color='gray', s=140, edgecolors='white', zorder=12)

# Sarkaçların Doğrusal Enerji Yollarını Gösteren Karşıt Eksen Çizgileri
for name, data in planets.items():
    if data["phase"] == 0:
        x_line = [-data["r"] * np.cos(data["angle"]), data["r"] * np.cos(data["angle"])]
        y_line = [-data["r"] * np.sin(data["angle"]), data["r"] * np.sin(data["angle"])]
        ax.plot(x_line, y_line, [0, 0], color=data["color"], linestyle=':', alpha=0.25, linewidth=1.2)

# Merkaba Dinamik Işık Hatları
merkaba_lines = [ax.plot([], [], [], color='green', alpha=0.4, linewidth=1.8) for _ in range(6)]

# ---------------------------------------------------------
# ANİMASYON GÜNCELLEME DÖNGÜSÜ
# ---------------------------------------------------------
def update(frame):
    t = time_steps[frame]
    current_positions = {}
    
    for name, data in planets.items():
        # r * cos(t + phase) ile doğrusal sarkaç mekanizması
        displacement = data["r"] * np.cos(t + data["phase"])
        
        x = displacement * np.cos(data["angle"])
        y = displacement * np.sin(data["angle"])
        z = 0.3 * np.sin(2 * t + data["phase"])
        
        plots[name]._offsets3d = ([x], [y], [z])
        current_positions[name] = np.array([x, y, z])
        
    d_pos = current_positions["Dünya"]
    m_pos = current_positions["Mars"]
    
    # Kuantum Sıçrama Parlaması: Dünya ve Mars merkeze yaklaştıkça Merkaba çizgileri beyaza döner
    distance_to_center = np.linalg.norm(d_pos)
    if distance_to_center < 0.2:
        line_color = '#FFFFFF'  # Merkez kuantum parlaması (Saf Işık)
        line_alpha = 0.85
    else:
        line_color = '#00FF00'  # Normal yeşil yaşam potansiyeli
        line_alpha = 0.35
    
    nodes = [
        [d_pos, m_pos],
        [d_pos, jupiter_pos], 
        [m_pos, saturn_pos],
        [d_pos, saturn_pos],
        [m_pos, jupiter_pos],
        [d_pos, -d_pos]
    ]
    
    for line, node in zip(merkaba_lines, nodes):
        line.set_data_3d([node[0], node[1]], [node[0], node[1]], [node[2], node[2]])
        line.set_color(line_color)
        line.set_alpha(line_alpha)
        
    return list(plots.values()) + [tube_line, jup_point, sat_point] + merkaba_lines

draw_cellular_spheres(ax)

ani = FuncAnimation(fig, update, frames=frames, interval=30, blit=False)
plt.title("Z Kanserli Hücre Doğumu: 1'den 2'ye Geçiş ve 3. Çift Yaşam Kıvılcımı", color='white', y=0.95)
plt.show()
