import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np

# Set seaborn style
sns.set_style("whitegrid")
sns.set_palette("husl")

# Set random seed for reproducibility
np.random.seed(42)

# X-axis labels (4 ticks for both subplots)
x_labels = ['50%', '75%', '100%']
x_pos = np.arange(len(x_labels))

# Line graph - Cache Hit Ratio Data
# Single line for one system
cache_hit_ratio = []  # Cache hit ratio for each config

# Grouped bar graph - Time Data
# Each x-tick has 3 bars (e.g., 3 different metrics or methods)
bar1_data = []  # min time data
bar2_data = []  # average time data
bar3_data = []  # max time data

fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 5))

# 1. Line Graph (Cache Hit Ratio) Generation
# Plot single line
ax1.plot(x_pos, cache_hit_ratio, marker='o', linewidth=2.5, 
         markersize=8, color='#1F77B4')

# Add value labels above each data point
for i, value in enumerate(cache_hit_ratio):
    ax1.text(x_pos[i], value+0.03, f'{value:.2f}',
            ha='center', va='bottom', fontsize=12, fontweight='bold')

# Customize ax1
ax1.set_xlabel('Cache Capacity Ratio (%)', fontsize=18, fontweight='bold')
ax1.set_ylabel('Cache Hit Ratio', fontsize=18, fontweight='bold')
ax1.set_xticks(x_pos)
ax1.set_xticklabels(x_labels, fontsize=16)
ax1.set_ylim([0.0, 1.05])  # Cache hit ratio typically 0-1
ax1.tick_params(axis='both', labelsize=16)
ax1.grid(True, alpha=0.3, linestyle='--')
ax1.text(0.5, -0.3, '(a) Cache Hit Ratio', transform=ax1.transAxes,
         fontsize=20, fontweight='bold', ha='center')

# 2. Grouped Bar Graph (Time) Generation
bar_width = 0.25  # Width of each bar

# Create positions for the 3 bars at each x-tick
positions_bar1 = x_pos - bar_width
positions_bar2 = x_pos
positions_bar3 = x_pos + bar_width

# Plot the 3 grouped bars
bars1 = ax2.bar(positions_bar1, bar1_data, bar_width, 
                label='Min', color='#2CA02C', alpha=0.8)
bars2 = ax2.bar(positions_bar2, bar2_data, bar_width, 
                label='Average', color='#D62728', alpha=0.8)
bars3 = ax2.bar(positions_bar3, bar3_data, bar_width, 
                label='Max', color='#9467BD', alpha=0.8)

# Add value labels on top of bars (optional)
for bars in [bars1, bars2, bars3]:
    for bar in bars:
        height = bar.get_height()
        ax2.text(bar.get_x() + bar.get_width()/2., height,
                f'{height:.3f}',
                ha='center', va='bottom', fontsize=12, fontweight='bold')

# Customize ax2
ax2.set_xlabel('Cache Capacity Ratio (%)', fontsize=18, fontweight='bold')
ax2.set_ylabel('Read Latency (sec, log scale)', fontsize=18, fontweight='bold')
ax2.set_xticks(x_pos)
ax2.set_xticklabels(x_labels, fontsize=16)
ax2.tick_params(axis='both', labelsize=16)
ax2.set_yscale('log')
ax2.legend(fontsize=16, loc='lower center', bbox_to_anchor=(0.5, 1.02), ncol=3, frameon=True)
ax2.grid(axis='y', alpha=0.3, linestyle='--')
ax2.text(0.5, -0.3, '(b) Warm Read Latency', transform=ax2.transAxes,
         fontsize=20, fontweight='bold', ha='center')

plt.tight_layout()
plt.subplots_adjust(top=0.90, bottom=0.12, wspace=0.3)

# Save the figure
plt.savefig('bdcats_cache_hit_plot.pdf', dpi=300, bbox_inches='tight')

plt.show()
