import matplotlib.pyplot as plt
import numpy as np

# Set random seed for reproducible jitter
np.random.seed(42)

# Node counts
nodes = [4, 8, 16, 32, 64]
node_labels = ['4', '8', '16', '32', '64']
step_colors = ['#457B9D', '#F77F00', '#9B59B6', '#06A77D']

# 1. Data exchange time data (3 runs per node count) 
# Each inner list contains 3 time measurements for each node count
ax1_data = [
    # 4 nodes
    [
        [],  # Epoch 1-2 (3 runs)
        [],  # Epoch 2-3 (3 runs)
        [],  # Epoch 3-4 (3 runs)
        []   # Epoch 4-5 (3 runs)
    ],
    # 8 nodes
    [
        [],  # Epoch 1-2 (3 runs)
        [],  # Epoch 2-3 (3 runs)
        [],  # Epoch 3-4 (3 runs)
        []   # Epoch 4-5 (3 runs)
    ],
    # 16 nodes
    [
        [],  # Epoch 1-2 (3 runs)
        [],  # Epoch 2-3 (3 runs)
        [],  # Epoch 3-4 (3 runs)
        []   # Epoch 4-5 (3 runs)
    ],
    # 32 nodes 
    [
        [],  # Epoch 1-2 (3 runs)
        [],  # Epoch 2-3 (3 runs)
        [],  # Epoch 3-4 (3 runs)
        []   # Epoch 4-5 (3 runs)
    ],
    # 64 nodes 
    [
        [],  # Epoch 1-2 (3 runs)
        [],  # Epoch 2-3 (3 runs)
        [],  # Epoch 3-4 (3 runs)
        []   # Epoch 4-5 (3 runs)
    ]
]

# 2. Data exchange buffer size data (3 runs per node count)
# Each inner list contains 3 buffer size measurements for each node count
buffer_data = [
    # 4 nodes - 3 runs
    [],
    # 8 nodes - 3 runs
    [],
    # 16 nodes - 3 runs
    [],
    # 32 nodes - 3 runs
    [],
    # 64 nodes - 3 runs
    []
]

# Create figure with 2 subplots
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 5))

# 1. Bar plot generation for data exchange time
x_pos = np.arange(len(nodes))
bar_width = 0.18
num_steps = 4

for step_idx in range(num_steps):
    means = []
    stds = []
    for node_idx in range(len(nodes)):
        samples = ax1_data[node_idx][step_idx]
        means.append(np.mean(samples))
        stds.append(np.std(samples))
    
    # Position bars for this step
    positions = x_pos + (step_idx - 1.5) * bar_width
    
    ax1.bar(positions, means, bar_width, yerr=stds, 
            label=f'Epoch {step_idx+1}-{step_idx+2} ', color=step_colors[step_idx], 
            alpha=0.8, capsize=3, error_kw={'linewidth': 1.5})

ax1.set_xlabel('Number of Nodes', fontsize=19, fontweight='bold')
ax1.set_ylabel('Time (sec)', fontsize=19, fontweight='bold')
ax1.set_xticks(x_pos)
ax1.set_xticklabels(node_labels, fontsize=18)
ax1.tick_params(axis='y', labelsize=18)
ax1.legend(fontsize=14, loc='lower center', bbox_to_anchor=(0.5, 1.02), ncol=2)  # Above plot, horizontal
ax1.grid(axis='y', alpha=0.3, linestyle='--')
ax1.text(0.5, -0.3, '(a) Data Exchange Time (n=3)', transform=ax1.transAxes, 
         fontsize=20, fontweight='bold', ha='center')

# 2. Bar plot generation for data exchange buffer size
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
plt.savefig('trainingio_dataexchange_plot.pdf', bbox_inches='tight')

plt.show()
