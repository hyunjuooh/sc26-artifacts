import matplotlib.pyplot as plt
import numpy as np

# Set random seed for reproducible jitter
np.random.seed(42)

# Node counts
nodes = [4, 8, 16, 32, 64]
node_labels = ['4', '8', '16', '32', '64']
color_ax1 = '#457B9D'

# Data exchange time box plot data (5 runs per node count) 
# Each inner list contains 5 time measurements for each node count
ax1_data  = [
    [],  # 4 nodes
    [],  # 8 nodes
    [],  # 16 nodes
    [],  # 32 nodes
    []   # 64 nodes
]

# Data exchange buffer size (5 runs per node count) 
# Each inner list contains 5 buffer size measurements for each node count
buffer_data = [
    # 4 nodes - 5 runs
    [],
    # 8 nodes - 5 runs
    [],
    # 16 nodes - 5 runs
    [],
    # 32 nodes - 5 runs
    [],
    # 64 nodes - 5 runs
    []
]

# Create figure with 2 subplots
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 5))

# 1. Data exchange time box plot generation 
positions_1 = range(1, len(nodes)+1)

bp1 = ax1.boxplot(ax1_data, positions=positions_1, patch_artist=True, 
                  widths=0.6, showfliers=False)

# Color the boxes
for patch in bp1['boxes']:
    patch.set_facecolor(color_ax1)
    patch.set_alpha(0.6)

# Add jitter points
for pos, samples in zip(positions_1, ax1_data):
    x = np.random.normal(pos, 0.05, size=len(samples))
    ax1.scatter(x, samples, alpha=0.8, s=50, color=color_ax1, 
               edgecolors='black', linewidth=0.5, zorder=3)

ax1.set_xlabel('Number of Nodes', fontsize=19, fontweight='bold')
ax1.set_ylabel('Time (sec)', fontsize=19, fontweight='bold')
ax1.set_ylim(0, 10)
ax1.set_xticks(positions_1)
ax1.set_xticklabels(node_labels, fontsize=18)
ax1.tick_params(axis='y', labelsize=18)
ax1.grid(axis='y', alpha=0.3, linestyle='--')
ax1.text(0.5, -0.3, '(a) Data Exchange Time (n=5)', transform=ax1.transAxes, 
         fontsize=20, fontweight='bold', ha='center')

# 2. Data buffer size bar plot generation
# Calculate mean and std for each node count
buffer_means = [np.mean(buffers) for buffers in buffer_data]
buffer_stds = [np.std(buffers) for buffers in buffer_data]

# Create bar graph with error bars
ax2.bar(range(len(nodes)), buffer_means, yerr=buffer_stds, 
        color='steelblue', alpha=0.7, edgecolor='black', linewidth=1.5,
        capsize=5, error_kw={'linewidth': 1.5})

ax2.set_xticks(range(len(nodes)))
ax2.set_xticklabels(node_labels, fontsize=18)
ax2.set_xlabel('Number of Nodes', fontsize=19, fontweight='bold')
ax2.set_ylabel('Data Exchange Buffer Size (GB)', fontsize=19, fontweight='bold')
ax2.grid(axis='y', alpha=0.3, linestyle='--')
ax2.tick_params(axis='both', labelsize=18)
ax2.text(0.5, -0.3, '(b) Peak Buffer Allocation (Node 0)', transform=ax2.transAxes, 
         fontsize=20, fontweight='bold', ha='center')

# Adjust layout
plt.tight_layout()
plt.subplots_adjust(top=0.90, bottom=0.12, wspace=0.3)

# Save the figure
plt.savefig('bdcats_dataexchange_plot.pdf', bbox_inches='tight')
print("Plot saved successfully!")

plt.show()
