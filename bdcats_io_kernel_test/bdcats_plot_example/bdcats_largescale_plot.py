import numpy as np
import matplotlib.pyplot as plt

# X-axis labels (2 categories)
categories = ['Baseline PDC', 'PDC with Caching Service']
x_pos = np.arange(len(categories))

# Data for stacked bars (3 segments per bar)
# Within the intter list provide two values each for PDC and PDC with caching service
# Category A values
segment1_values = []  # Cold Read
segment2_values = []  # Data Exchange Time
segment3_values = []  # Warm Read

# Create figure
fig, ax = plt.subplots(figsize=(6,4))

# Colors for the three segments
color1 = '#1F77B4'  # Blue
color2 = '#FF7F0E'  # Orange
color3 = '#2CA02C'  # Green

bar_width = 0.25
positions_1 = x_pos - bar_width
positions_2 = x_pos
positions_3 = x_pos + bar_width

# Create grouped bars
bars1 = ax.bar(positions_1, segment1_values, bar_width, label='Cold Read Latency', 
               color=color1, alpha=0.8, edgecolor='black', linewidth=1)
bars2 = ax.bar(positions_2, segment2_values, bar_width, label='Data Exchange Time', 
               color=color2, alpha=0.8, edgecolor='black', linewidth=1)
bars3 = ax.bar(positions_3, segment3_values, bar_width, label='Warm Read Latency', 
               color=color3, alpha=0.8, edgecolor='black', linewidth=1)

# Add values on top of each bar
for bars in [bars1, bars2, bars3]:
    for bar in bars:
        height = bar.get_height()
        ax.text(bar.get_x() + bar.get_width()/2., height,
                f'{height}',
                ha='center', va='bottom', fontsize=11, fontweight='bold', color='black')
# Formatting
# ax.set_xlabel('Categories', fontsize=16, fontweight='bold')
ax.set_ylabel('Total Execution Time (sec)', fontsize=16, fontweight='bold')
ax.set_ylim(0, 150) 
ax.set_xticks(x_pos)
ax.set_xticklabels(categories, fontsize=14)
ax.tick_params(axis='y', labelsize=14)
# ax.set_yscale('log')

ax.grid(axis='y', alpha=0.3, linestyle='--', zorder=0)
ax.legend(fontsize=10, loc='upper right', framealpha=0.9)

# Adjust layout
plt.tight_layout()

# Save the figure
plt.savefig('bdcats_largescale_plot.pdf', dpi=300, bbox_inches='tight')
plt.show()
