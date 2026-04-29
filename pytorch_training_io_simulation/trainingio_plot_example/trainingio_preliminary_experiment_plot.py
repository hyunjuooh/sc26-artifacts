import matplotlib.pyplot as plt
import numpy as np
import matplotlib.ticker as ticker

# Colors
colors_systems = ['#457B9D', '#F77F00', '#9B59B6', '#06A77D']
colors_ax4 = ['#E63946', '#06A77D', '#457B9D']


systems = ['Strategy 1', 'Strategy 2', 'Strategy 3', 'Strategy 4']

# 1. Data exchange time data (n=3)
ax1_data = [
    [],  # Strategy 1 - 3 runs
    [],  # Strategy 2 - 3 runs
    [],  # Strategy 3 - 3 runs
    []   # Strategy 4 - 3 runs
]

# 2. Peak memory allocation data (n=3)
ax2_data = []  # Single value for each system

# 3. Per sample access latency data for each strategy
ax3_data = [] 

# 4. Target Cache scope data
x_labels_ax4 = ['Process-Local', 'Intra-Node', 'Inter-Node']

# Each configuration has 1 value (1 bar)
ax4_data = []  # Process-Local, Intra-Node, Inter-Node

# Create figure with 2x2 subplots
fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, figsize=(12,11))

# 1. Data exchange time plot generation
positions_1 = range(1, len(systems)+1)

bp1 = ax1.boxplot(ax1_data, positions=positions_1, patch_artist=True, 
                  widths=0.6, showfliers=False)

# Color the boxes
for patch, color in zip(bp1['boxes'], colors_systems):
    patch.set_facecolor(color)
    patch.set_alpha(0.6)

# Add jitter points
for pos, samples, color in zip(positions_1, ax1_data, colors_systems):
    x = np.random.normal(pos, 0.05, size=len(samples))
    ax1.scatter(x, samples, alpha=0.8, s=60, color=color, 
               edgecolors='black', linewidth=0.5, zorder=3)

# ax1.set_xlabel('Strategy', fontsize=16, fontweight='bold')
ax1.set_ylabel('Time (sec)', fontsize=16, fontweight='bold')
ax1.set_xticks(positions_1)
ax1.set_xticklabels(systems, fontsize=14)
ax1.tick_params(axis='y', labelsize=14)
ax1.grid(axis='y', alpha=0.3, linestyle='--')
ax1.text(0.5, -0.2, '(a) Data Exchange Time (n=3)', transform=ax1.transAxes,
         fontsize=17, fontweight='bold', ha='center')

# 2. Peak memory allocation plot generation
x_pos_ax2 = np.arange(len(systems))
bars_ax2 = ax2.bar(x_pos_ax2, ax2_data, color=colors_systems, alpha=0.8)

# Add value labels on top of bars
for bar in bars_ax2:
    height = bar.get_height()
    ax2.text(bar.get_x() + bar.get_width()/2., height,
            f'{height:.1f}',
            ha='center', va='bottom', fontsize=11, fontweight='bold')

# ax2.set_xlabel('System', fontsize=14, fontweight='bold')
ax2.set_ylabel('Data Exchange Buffer Size (GB)', fontsize=16, fontweight='bold')
ax2.set_xticks(x_pos_ax2)
ax2.set_xticklabels(systems, fontsize=14)
# ax2.set_yscale('log')
ax2.tick_params(axis='y', labelsize=14)
ax2.grid(axis='y', alpha=0.3, linestyle='--')
ax2.text(0.5, -0.2, '(b) Peak Memory Allocation (Node 0)', transform=ax2.transAxes,
         fontsize=17, fontweight='bold', ha='center')

# 3. Per sample access latency plot generation
x_pos_ax3 = np.arange(len(systems))
bars_ax3 = ax3.bar(x_pos_ax3, ax3_data, color=colors_systems, alpha=0.8)

# Add value labels on top of bars - using data directly
for i, (bar, value) in enumerate(zip(bars_ax3, ax3_data)):
    height = bar.get_height()
    ax3.text(bar.get_x() + bar.get_width()/2., height,
            f'{value:.3f}',
            ha='center', va='bottom', fontsize=11, fontweight='bold')

# ax3.set_xlabel('System', fontsize=14, fontweight='bold')
ax3.set_ylabel('Average Acess Latency (sec)', fontsize=16, fontweight='bold')
ax3.set_xticks(x_pos_ax3)
ax3.set_xticklabels(systems, fontsize=14)
ax3.tick_params(axis='y', labelsize=14)
ax3.set_yscale('log')
ax3.set_ylim(0.001, 1)
# ax3.yaxis.set_major_formatter(ticker.LogFormatterExponent())
ax3.grid(axis='y', alpha=0.3, linestyle='--')
ax3.text(0.5, -0.33, '(c) Per Sample Access Latency\n(Epoch2, Process 0)', transform=ax3.transAxes,
         fontsize=17, fontweight='bold', ha='center')

# 4. Target cache scope plot generation
x_pos_ax4 = np.arange(len(x_labels_ax4))
bars_ax4 = ax4.bar(x_pos_ax4, ax4_data, color='#457B9D', alpha=0.8, width=0.6)

# Add value labels on top of bars
for bar, value in zip(bars_ax4, ax4_data):
    height = bar.get_height()
    ax4.text(bar.get_x() + bar.get_width()/2., height,
            f'{value:.0f}',
            ha='center', va='bottom', fontsize=11, fontweight='bold')

ax4.set_xlabel('Data Residency', fontsize=16, fontweight='bold')
ax4.set_ylabel('Sample Count', fontsize=16, fontweight='bold')
ax4.set_xticks(x_pos_ax4)
ax4.set_xticklabels(x_labels_ax4, fontsize=14)
ax4.tick_params(axis='y', labelsize=14)
ax4.grid(axis='y', alpha=0.3, linestyle='--')
ax4.text(0.5, -0.33, '(d) Target Cache Scope for Epoch 2\n(Process 0)', transform=ax4.transAxes,
         fontsize=17, fontweight='bold', ha='center')

# Adjust layout
plt.tight_layout()
plt.subplots_adjust(top=0.94, bottom=0.10, hspace=0.4, wspace=0.25)

# Save the figure
plt.savefig('preliminary_analysis_plot.pdf', dpi=300, bbox_inches='tight')

plt.show()
