
import matplotlib.pyplot as plt
import matplotlib.patches as patches

# Set up the figure styling
plt.figure(figsize=(14, 13)) 
ax = plt.gca()
ax.set_axis_off()
ax.set_xlim(0, 1)
ax.set_ylim(0, 1)

# Define box styles
style_kernel = dict(boxstyle='round,pad=0.6', facecolor='#2c3e50', edgecolor='black', linewidth=2) # Dark/Fundamental
style_stat = dict(boxstyle='round,pad=0.5', facecolor='#ecf0f1', edgecolor='#2980b9', linewidth=2) # Blue/Statistical
style_quant = dict(boxstyle='round,pad=0.5', facecolor='#fff5f5', edgecolor='#c0392b', linewidth=2) # Red/Quantum
style_obs = dict(boxstyle='round,pad=0.5', facecolor='#e8f6f3', edgecolor='#16a085', linewidth=2) # Green/Observable
style_newic = dict(boxstyle='round,pad=0.5', facecolor='#fef5e7', edgecolor='#d35400', linewidth=2) # Orange/New Physics
style_filter = dict(boxstyle='larrow,pad=0.3', facecolor='#f9e79f', edgecolor='#f39c12', linewidth=2) # Yellow/Filter

# Font changes
font_title = {'fontsize': 20, 'weight': 'bold', 'color': '#2c3e50'}

# Coordinates
y_kernel = 0.92
y_layer2 = 0.75
y_layer3 = 0.50
y_layer4 = 0.30
y_layer5 = 0.10

pos_kernel = (0.5, y_kernel)

pos_metric = (0.2, y_layer2)
pos_matter = (0.8, y_layer2)

pos_gravity = (0.2, y_layer3)
pos_fields = (0.8, y_layer3)

pos_filter = (0.5, y_layer4)

pos_obs_class = (0.15, y_layer5)
pos_obs_new = (0.5, y_layer5)
pos_obs_quant = (0.85, y_layer5)


# Draw functions
def draw_node(pos, text, style, text_color='black'):
    ax.text(pos[0], pos[1], text, ha='center', va='center', bbox=style, fontsize=10, color=text_color, weight='bold')

def draw_edge(start, end, label, color='black', style='->', connection='arc3,rad=0'):
    ax.annotate("",
                xy=end, xycoords='data',
                xytext=start, textcoords='data',
                arrowprops=dict(arrowstyle=style, color=color, lw=2, shrinkA=15, shrinkB=15, connectionstyle=connection),
                zorder=1
                )
    # Label placement
    if label:
        # Calculate mid point based on connection style roughly
        if 'rad' in connection:
            # Simple heuristic for curved lines label placement
            mid_x = (start[0] + end[0]) / 2
            mid_y = (start[1] + end[1]) / 2 + (0.05 if 'rad=-' in connection else -0.05)
        else:
            mid_x = (start[0] + end[0]) / 2
            mid_y = (start[1] + end[1]) / 2
            
        ax.text(mid_x, mid_y, label, ha='center', va='center', fontsize=8, color=color, 
                bbox=dict(boxstyle='round,pad=0.2', facecolor='white', edgecolor='none', alpha=0.9),
                zorder=2)

# -- Nodes --

# Root
draw_node(pos_kernel, "TAMESIS KERNEL\nH_kernel = Sum(J_ij sigma_i sigma_j)", style_kernel, 'white')

# Branch 1: Statistical Space (Left)
draw_node(pos_metric, "EMERGENT SPACETIME\nMetric g_uv ~ <Laplacian^-1>", style_stat)

# Branch 2: Topological Matter (Right)
draw_node(pos_matter, "QUANTUM MATTER\nPartcles = Defects pi_1(G)!=0", style_quant)

# Layer 3
draw_node(pos_gravity, "ENTROPIC GRAVITY\nG_uv ~ Stress(Info)", style_stat)
draw_node(pos_fields, "QUANTUM FIELDS\nYang-Mills / Dirac", style_quant)

# Filter
draw_node(pos_filter, "REALIZABILITY FILTER (Phi_R)\nBlocks Exp-Time Solutions", style_filter)

# Observables
draw_node(pos_obs_class, "CLASSICAL PROOFS\n(Lensing, Time Dilation)", style_obs)
draw_node(pos_obs_new, "NEW PREDICTIONS\n(Mod. Dispersion, Birefringence)", style_newic)
draw_node(pos_obs_quant, "QUANTUM SPECTRA\n(Mass Gap, SM Particles)", style_obs)

# -- Edges --

# Kernel -> Metric (Blue Path)
draw_edge(pos_kernel, pos_metric, "Statistical Average\n(Thermodynamic Limit)", color='#2980b9')
draw_edge(pos_metric, pos_gravity, "Curvature Cost", color='#2980b9')

# Kernel -> Matter (Red Path)
draw_edge(pos_kernel, pos_matter, "Topological Stability", color='#c0392b')
draw_edge(pos_matter, pos_fields, "Local Dynamics", color='#c0392b')

# Feedback / Coupling
# "Mass creates Congestion" (Matter -> Gravity)
draw_edge(pos_matter, pos_gravity, "Mass creates\nInfo Congestion", color='#8e44ad', style='->', connection='arc3,rad=-0.1')
# Backreaction (Matter -> Metric)
draw_edge(pos_matter, pos_metric, "Backreaction (T_uv)", color='#8e44ad', style='->', connection='arc3,rad=0.2')


# Gravity/Fields -> Filter
draw_edge(pos_gravity, pos_filter, "", color='#2980b9')
draw_edge(pos_fields, pos_filter, "", color='#c0392b')

# Filter -> Observables
draw_edge(pos_filter, pos_obs_class, "GR Limits")
draw_edge(pos_filter, pos_obs_quant, "QM Limits")
draw_edge(pos_filter, pos_obs_new, "Planck Scale Leakage", color='#d35400', style='->', connection='arc3')

# -- Legend --
legend_elements = [
    patches.Patch(facecolor='#2c3e50', edgecolor='black', label='Fundamental Substrate'),
    patches.Patch(facecolor='#ecf0f1', edgecolor='#2980b9', label='Statistical/Geometric Regime'),
    patches.Patch(facecolor='#fff5f5', edgecolor='#c0392b', label='Topological/Quantum Regime'),
    patches.Patch(facecolor='#fef5e7', edgecolor='#d35400', label='New Physics Predictions'),
    patches.Patch(facecolor='#f9e79f', edgecolor='#f39c12', label='Selection Mechanism')
]
ax.legend(handles=legend_elements, loc='lower center', ncol=3, frameon=False, bbox_to_anchor=(0.5, -0.05))

# Title
plt.text(0.5, 1.02, "THE TAMESIS OPERATIONAL FRAMEWORK", ha='center', **font_title)

# Save
output_path = "d:/TamesisTheoryCompleteResearchArchive/13_CANON/physics_pipeline.png"
plt.savefig(output_path, dpi=300, bbox_inches='tight')
print(f"Diagram saved to {output_path}")
