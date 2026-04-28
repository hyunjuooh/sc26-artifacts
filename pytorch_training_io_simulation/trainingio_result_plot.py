import numpy as np
import matplotlib.pyplot as plt

# Define colors for the three systems
color_a = '#1f77b4'  # Blue
color_b = '#2ca02c'  # Orange
color_c = '#D62728'  # Green

# Define steps and labels
steps = [0, 1, 2, 3, 4]
step_labels = ['4', '8', '16', '32', '64']

# Each array requires three iteration results.

# For system_a array put the HDF5 results.
# Epoch 1 
system_a_scenario1 = [
    [],  # 4 nodes
    [],  # 8 nodes
    [],  # 16 nodes
    [],  # 32 nodes
    []   # 64 nodes
]

# Epoch 2 
system_a_scenario2 = [
    [],  # 4 nodes
    [],  # 8 nodes
    [],  # 16 nodes
    [],  # 32 nodes
    []   # 64 nodes
]

# Epoch 3 
system_a_scenario3 = [
    [],  # 4 nodes
    [],  # 8 nodes
    [],  # 16 nodes
    [],  # 32 nodes
    []   # 64 nodes
]

# Epoch 4 
system_a_scenario4 = [
    [],  # 4 nodes
    [],  # 8 nodes
    [],  # 16 nodes
    [],  # 32 nodes
    []   # 64 nodes
]

# Epoch 5 
system_a_scenario5 = [
    [],  # 4 nodes
    [],  # 8 nodes
    [],  # 16 nodes
    [],  # 32 nodes
    []   # 64 nodes
]


# For system_a array put the PDC results.

# Epoch 1
system_b_scenario1 = [
    [],  # 4 nodes
    [],  # 8 nodes
    [],  # 16 nodes
    [],  # 32 nodes
    []   # 64 nodes
]

# Epoch 2
system_b_scenario2 = [
    [],  # 4 nodes
    [],  # 8 nodes
    [],  # 16 nodes
    [],  # 32 nodes
    []   # 64 nodes
]

# Epoch 3
system_b_scenario3 = [
    [],  # 4 nodes
    [],  # 8 nodes
    [],  # 16 nodes
    [],  # 32 nodes
    []   # 64 nodes
]

# Epoch 4
system_b_scenario4 = [
    [],  # 4 nodes
    [],  # 8 nodes
    [],  # 16 nodes
    [],  # 32 nodes
    []   # 64 nodes
]

# Epoch 5
system_b_scenario5 = [
    [],  # 4 nodes
    [],  # 8 nodes
    [],  # 16 nodes
    [],  # 32 nodes
    []   # 64 nodes
]


# For system_c array put the PDC with caching service results.

# Epoch 1
system_c_scenario1 = [
    [],  # 4 nodes
    [],  # 8 nodes
    [],  # 16 nodes
    [],  # 32 nodes
    []   # 64 nodes
]

# Epoch 2
system_c_scenario2 = [
    [],  # 4 nodes
    [],  # 8 nodes
    [],  # 16 nodes
    [],  # 32 nodes
    []   # 64 nodes
]

# Epoch 3
system_c_scenario3 = [
    [],  # 4 nodes
    [],  # 8 nodes
    [],  # 16 nodes
    [],  # 32 nodes
    []   # 64 nodes
]

# Epoch 4
system_c_scenario4 = [
    [],  # 4 nodes
    [],  # 8 nodes
    [],  # 16 nodes
    [],  # 32 nodes
    []   # 64 nodes
]
# Epoch 5
system_c_scenario5 = [
    [],  # 4 nodes
    [],  # 8 nodes
    [],  # 16 nodes
    [],  # 32 nodes
    []   # 64 nodes
]


# Store all scenarios
scenarios = [
    (system_a_scenario1, system_b_scenario1, system_c_scenario1, 'Epoch 1'),
    (system_a_scenario2, system_b_scenario2, system_c_scenario2, 'Epoch 2'),
    (system_a_scenario3, system_b_scenario3, system_c_scenario3, 'Epoch 3'),
    (system_a_scenario4, system_b_scenario4, system_c_scenario4, 'Epoch 4'),
    (system_a_scenario5, system_b_scenario5, system_c_scenario5, 'Epoch 5')
]

# Create figure with 5 subplots
fig, axes = plt.subplots(1, 5, figsize=(30, 6))

step_positions = np.arange(len(steps))

# Calculate global min and max across all scenarios for shared y-axis
all_values_a = []
all_values_b = []
all_values_c = []
for system_a_data, system_b_data, system_c_data, _ in scenarios:
    for samples in system_a_data:
        all_values_a.extend(samples)
    for samples in system_b_data:
        all_values_b.extend(samples)
    for samples in system_c_data:
        all_values_c.extend(samples)

all_values = all_values_a + all_values_b + all_values_c
global_min = min(all_values)
global_max = max(all_values)

# Add some padding for better visualization (in log space)
y_min = global_min * 0.8
y_max = global_max * 1.2

# Loop through each scenario and create subplot
for idx, (system_a_data, system_b_data, system_c_data, title) in enumerate(scenarios):
    ax = axes[idx]
    
    # Calculate medians, mins, and maxs for HDF5
    medians_a = np.array([np.median(samples) for samples in system_a_data])
    mins_a = np.array([np.min(samples) for samples in system_a_data])
    maxs_a = np.array([np.max(samples) for samples in system_a_data])
    
    # Calculate medians, mins, and maxs for PDC
    medians_b = np.array([np.median(samples) for samples in system_b_data])
    mins_b = np.array([np.min(samples) for samples in system_b_data])
    maxs_b = np.array([np.max(samples) for samples in system_b_data])
    
    # Calculate medians, mins, and maxs for PDC with caching service
    medians_c = np.array([np.median(samples) for samples in system_c_data])
    mins_c = np.array([np.min(samples) for samples in system_c_data])
    maxs_c = np.array([np.max(samples) for samples in system_c_data])
    
    # Calculate error bar sizes
    errors_a = [maxs_a - medians_a, medians_a - mins_a]
    errors_b = [maxs_b - medians_b, medians_b - mins_b]
    errors_c = [maxs_c - medians_c, medians_c - mins_c]
    
    # Offset positions for three systems
    offset = 0.15
    pos_a = step_positions - offset
    pos_b = step_positions
    pos_c = step_positions + offset
    
    # Plot HDF5
    # Plot individual data points for HDF5
    for i, samples in enumerate(system_a_data):
        x_jitter = np.random.normal(pos_a[i], 0.03, size=len(samples))
        ax.scatter(x_jitter, samples, s=50, color=color_a, alpha=0.7, 
                   edgecolors='black', linewidth=0.5, zorder=3)
    
    # Connect medians with line for HDF5
    ax.plot(pos_a, medians_a, linewidth=2, color=color_a, alpha=0.8, zorder=2)
    
    # Plot PDC
    # Plot individual data points for PDC
    for i, samples in enumerate(system_b_data):
        x_jitter = np.random.normal(pos_b[i], 0.03, size=len(samples))
        ax.scatter(x_jitter, samples, s=50, color=color_b, alpha=0.7, 
                   edgecolors='black', linewidth=0.5, zorder=3)
    
    # Connect medians with line for PDC
    ax.plot(pos_b, medians_b, linewidth=2, color=color_b, alpha=0.8, zorder=2)
    
    # Plot PDC with caching service
    # Plot individual data points for PDC with caching service
    for i, samples in enumerate(system_c_data):
        x_jitter = np.random.normal(pos_c[i], 0.03, size=len(samples))
        ax.scatter(x_jitter, samples, s=50, color=color_c, alpha=0.7, 
                   edgecolors='black', linewidth=0.5, zorder=3)
    
    # Connect medians with line for System C
    ax.plot(pos_c, medians_c, linewidth=2, color=color_c, alpha=0.8, zorder=2)
    
    # Customize subplot
    if idx == 0:
        ax.set_ylabel('Total Data Read Latency\n(sec, log scale)', fontsize=28, fontweight='bold')

    # ax.set_xlabel('Epoch', fontsize=28, fontweight='bold')
    ax.set_xlabel('Number of Nodes', fontsize=28, fontweight='bold')
    ax.set_xticks(step_positions)
    ax.set_xticklabels(step_labels, fontsize=18, rotation=0)
    ax.tick_params(axis='both', labelsize=25)
    ax.set_yscale('log')
    ax.set_ylim([y_min, y_max])  # Set shared y-axis limits
    ax.grid(axis='both', alpha=0.3, linestyle='--', which='both')
    ax.text(0.5, -0.4, f'({chr(97+idx)}) {title}', transform=ax.transAxes, 
            fontsize=30, fontweight='bold', ha='center')

# Add shared legend at the top with three systems
legend_elements = [plt.Line2D([0], [0], color=color_a, linewidth=3, label='HDF5'),
                   plt.Line2D([0], [0], color=color_b, linewidth=3, label='PDC'),
                   plt.Line2D([0], [0], color=color_c, linewidth=3, label='PDC with Caching Service')]
fig.legend(handles=legend_elements, loc='upper center', bbox_to_anchor=(0.5, 1.05), 
          ncol=3, fontsize=25, frameon=True)

# Adjust layout
plt.tight_layout()
plt.subplots_adjust(top=0.85, bottom=0.15, wspace=0.2)

# Save the figure
plt.savefig('trainingio_epoch_comparison.pdf', dpi=300, bbox_inches='tight')
# print("Five scenarios comparison plot with three systems saved successfully!")

plt.show()
