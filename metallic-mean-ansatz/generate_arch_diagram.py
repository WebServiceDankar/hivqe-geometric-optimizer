import os
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches

# Certificar que o diretório existe
os.makedirs("docs", exist_ok=True)

fig, ax = plt.subplots(figsize=(11, 6.5), dpi=300)
ax.set_xlim(0, 11)
ax.set_ylim(0, 11)
ax.axis('off')

# Title
plt.text(5.5, 10.3, "M$^{2}$QA Hybrid Quantum-Classical Pipeline for NDM-1 Metalloenzyme", 
         ha='center', va='center', fontsize=16, fontweight='bold', family='sans-serif')

# Separator Line
ax.plot([5.5, 5.5], [1, 9.5], linestyle='--', color='gray', linewidth=2, zorder=0)

# Domain Labels
b_classic = mpatches.FancyBboxPatch((1.6, 8.8), 2.3, 0.8, boxstyle="round,pad=0.1", facecolor="#f5f5f5", edgecolor="gray", linewidth=1.5)
b_quantum = mpatches.FancyBboxPatch((7.1, 8.8), 2.3, 0.8, boxstyle="round,pad=0.1", facecolor="#f5f5f5", edgecolor="gray", linewidth=1.5)
ax.add_patch(b_classic)
ax.add_patch(b_quantum)
plt.text(2.75, 9.2, "CLASSICAL DOMAIN", ha='center', va='center', fontsize=12, color='#333333', fontweight='bold')
plt.text(8.25, 9.2, "QUANTUM DOMAIN", ha='center', va='center', fontsize=12, color='#333333', fontweight='bold')

def draw_box(x, y, w, h, text, facecolor, edgecolor):
    box = mpatches.FancyBboxPatch((x, y), w, h, boxstyle="round,pad=0.2", 
                                  facecolor=facecolor, edgecolor=edgecolor, linewidth=2, zorder=3)
    ax.add_patch(box)
    plt.text(x+w/2, y+h/2, text, ha='center', va='center', fontsize=11, family='sans-serif', zorder=4)

# Boxes
draw_box(1, 6.2, 3.5, 2.0, "Classical Optimizer\n(e.g., COBYLA / SPSA)", "#e3f2fd", "#1565c0")
draw_box(1, 2.5, 3.5, 2.0, "Cost Function Evaluation\n(Check Chemical Accuracy)", "#f3e5f5", "#7b1fa2")
draw_box(6.5, 6.2, 3.5, 2.0, "M$^{2}$QA Quantum Ansatz\n(Borromean Topology)", "#e8f5e9", "#2e7d32")
draw_box(6.5, 2.5, 3.5, 2.0, "Hamiltonian Measurement\n(NDM-1 di-Zinc Core)", "#fff3e0", "#e65100")

# Extra Molecular Input
draw_box(8.7, 0.5, 2.0, 1.2, "Input:\nNDM-1 + Ligand\nGeometry", "#fafafa", "#9e9e9e")

# Arrows using Annotate
kw = dict(arrowprops=dict(arrowstyle="->,head_width=0.4,head_length=0.6", lw=2.5, color="#424242"), zorder=2)

# Opt -> Ansatz
ax.annotate("", xy=(6.5, 7.2), xytext=(4.5, 7.2), **kw)
plt.text(5.5, 7.5, "Update Parameters ($\\vec{\\theta}$)\nInit = Silver Ratio ($\\delta_S$)", ha='center', va='bottom', fontsize=10, fontweight='bold', color="#424242", zorder=4)

# Ansatz -> Measure
ax.annotate("", xy=(8.25, 4.5), xytext=(8.25, 6.2), **kw)
plt.text(8.4, 5.35, "Prepared State $|\\psi(\\vec{\\theta})\\rangle$", ha='left', va='center', fontsize=10, fontweight='bold', color="#424242")

# Measure -> Cost
ax.annotate("", xy=(4.5, 3.5), xytext=(6.5, 3.5), **kw)
plt.text(5.5, 3.8, "Expectation Value $\\langle E \\rangle$", ha='center', va='bottom', fontsize=10, fontweight='bold', color="#424242")

# Cost -> Opt
ax.annotate("", xy=(2.75, 6.2), xytext=(2.75, 4.5), **kw)
plt.text(2.6, 5.35, "Adjust $\\vec{\\theta}$ / Minimize $E$", ha='right', va='center', fontsize=10, fontweight='bold', color="#424242")

# Input -> Measure
ax.annotate("", xy=(8.25, 2.5), xytext=(9.2, 1.7), **kw)

# Author Credit
plt.text(10.8, 0.2, "Author: Daniel A. Palma (UNIFEI)\nGenerated via Hybrid Python/Matplotlib", ha='right', va='bottom', fontsize=7, color='gray')

plt.tight_layout()
plt.savefig("docs/arquitetura.png", bbox_inches='tight')
print("File docs/arquitetura.png successfully created.")
