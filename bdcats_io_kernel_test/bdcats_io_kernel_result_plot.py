import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Patch

# Node counts
nodes = [4, 8, 16, 32, 64]
node_labels = ['4', '8', '16', '32', '64']

# Add the cold read latency result of five iterations
# HDF5
system_a_scenario1 = [
    [],  # 4 nodes
    [],  # 8 nodes
    [],  # 16 nodes
    [],  # 32 nodes
    []   # 64 nodes
]

# HDF5 Cache VOL
system_b_scenario1 = [
    [],  # 4 nodes
    [],  # 8 nodes
    [],  # 16 nodes
    [],  # 32 nodes
    []   # 64 nodes
]

# PDC
system_c_scenario1 = [
    [],  # 4 nodes
    [],  # 8 nodes
    [],  # 16 nodes
    [],  # 32 nodes
    []   # 64 nodes
]

# PDC with caching service
system_d_scenario1 = [
    [],  # 4 nodes
    [],  # 8 nodes
    [],  # 16 nodes
    [],  # 32 nodes
    []   # 64 nodes
]

# Add the warm read latency result of five iterations

# HDF5 
system_a_scenario2 = [
    [],  # 4 nodes
    [],  # 8 nodes
    [],  # 16 nodes
    [],  # 32 nodes
    []   # 64 nodes
]

# HDF5 Cache VOL
system_b_scenario2 = [
    [],  # 4 nodes
    [],  # 8 nodes
    [],  # 16 nodes
    [],  # 32 nodes
    []   # 64 nodes
]


# PDC
system_c_scenario2 = [
    [],  # 4 nodes
    [],  # 8 nodes
    [],  # 16 nodes
    [],  # 32 nodes
    []   # 64 nodes
]


# PDC with caching service
system_d_scenario2 = [
    [],  # 4 nodes
    [],  # 8 nodes
    [],  # 16 nodes
    [],  # 32 nodes
    []   # 64 nodes
]


# Calculate statistics for line plots
def calc_stats(data):
    means = [np.mean(d) for d in data]
    stds = [np.std(d) for d in data]
    return means, stds

# Create figure with 2 subplots
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(13, 6), sharey=True)

# Colors and markers for the four systems
color_a = '#1F77B4'
color_b = '#FF7F0E'
color_c = '#2CA02C'
color_d = '#D62728'
markers = ['o', 's', '^', 'D']

# Cold read latency plot generation
systems_s1 = [system_a_scenario1, system_b_scenario1, system_c_scenario1, system_d_scenario1]
colors = [color_a, color_b, color_c, color_d]
labels = ['System A', 'System B', 'System C', 'System D']

for system_data, color, marker, label in zip(systems_s1, colors, markers, labels):
    means, stds = calc_stats(system_data)
    
    # Plot individual data points
    for i, samples in enumerate(system_data):
        ax1.scatter([nodes[i]] * len(samples), samples, color=color, 
                   s=35, alpha=0.5, edgecolors='black', linewidth=0.5, zorder=2)
    
    # Plot line connecting means
    ax1.plot(nodes, means, marker=marker, color=color, label=label, 
             linewidth=2.5, markersize=10, alpha=0.9, zorder=3)

ax1.set_xlabel('Number of Nodes', fontsize=16, fontweight='bold')
ax1.set_ylabel('Latency (log scale, sec)', fontsize=16, fontweight='bold')
ax1.set_xticks(nodes)
ax1.set_yscale('log')
ax1.set_xticklabels(node_labels, fontsize=16)
ax1.tick_params(axis='y', labelsize=16)
ax1.grid(True, alpha=0.3, linestyle='--')
ax1.text(0.5, -0.27, '(a) Cold Read Latency', transform=ax1.transAxes, 
         fontsize=20, fontweight='bold', ha='center')

# Warm read latency plot generation
systems_s2 = [system_a_scenario2, system_b_scenario2, system_c_scenario2, system_d_scenario2]

for system_data, color, marker, label in zip(systems_s2, colors, markers, labels):
    means, stds = calc_stats(system_data)
    
    # Plot individual data points
    for i, samples in enumerate(system_data):
        ax2.scatter([nodes[i]] * len(samples), samples, color=color, 
                   s=35, alpha=0.5, edgecolors='black', linewidth=0.5, zorder=2)
    
    # Plot line connecting means
    ax2.plot(nodes, means, marker=marker, color=color, label=label, 
             linewidth=2.5, markersize=10, alpha=0.9, zorder=3)

ax2.set_xlabel('Number of Nodes', fontsize=16, fontweight='bold')
ax2.set_ylabel('Latency (log scale, sec)', fontsize=16, fontweight='bold')
ax2.set_xticks(nodes)
ax2.set_yscale('log')
ax2.yaxis.set_tick_params(labelleft=True)
ax2.set_xticklabels(node_labels, fontsize=16)
ax2.tick_params(axis='y', labelsize=16)
ax2.grid(True, alpha=0.3, linestyle='--')
ax2.text(0.5, -0.27, '(b) Warm Read Latency', transform=ax2.transAxes, 
         fontsize=20, fontweight='bold', ha='center')

# Add a single legend at the top of the figure
from matplotlib.lines import Line2D
legend_elements = [
    Line2D([0], [0], marker='o', color=color_a, label='HDF5', 
           markersize=5, linewidth=2.5),
    Line2D([0], [0], marker='s', color=color_b, label='HDF5 Cache Vol', 
           markersize=5, linewidth=2.5),
    Line2D([0], [0], marker='^', color=color_c, label='PDC', 
           markersize=5, linewidth=2.5),
    Line2D([0], [0], marker='D', color=color_d, label='PDC with Caching Service', 
           markersize=5, linewidth=2.5)
]
fig.legend(handles=legend_elements, loc='upper center', bbox_to_anchor=(0.5, 1.05), 
          ncol=4, fontsize=16, framealpha=0.9)

# Add main title
# plt.suptitle('System Comparison: Node Scaling (n=5 runs per configuration)', 
#              fontsize=16, fontweight='bold', y=0.995)

# Adjust layout
plt.tight_layout()
plt.subplots_adjust(top=0.92, wspace=0.23)

# Save the figure
plt.savefig('bdcats_lineplot.pdf', dpi=300, bbox_inches='tight')
print("Line plot comparison saved successfully!")
plt.show()
