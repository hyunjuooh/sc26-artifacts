import numpy as np
import matplotlib.pyplot as plt

# X-axis labels (3 categories)
categories = ['50%', '75%', '100%']
x_pos = np.arange(len(categories))

# Cache hit ratio % for the system for each cache capacity configuration
cache_hit_ratio = []

# Execution time in seconds for each cache capacity configuration
execution_time = []

# Create figure with 2 subplots side by side
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 6))

# Color for the system
color = '#1F77B4'  # Blue

# 1. Cache Hit Ratio (Line Graph) Generation
ax1.plot(x_pos, cache_hit_ratio, marker='o', color=color, 
         linewidth=2.5, markersize=10)

for i, value in enumerate(cache_hit_ratio):
    ax1.text(x_pos[i], value+0.03, f'{value:.2f}',
            ha='center', va='bottom', fontsize=12, fontweight='bold')

ax1.set_xlabel('Cache Capacity Ratio (%)', fontsize=18, fontweight='bold')
ax1.set_ylabel('Cache Hit Ratio', fontsize=18, fontweight='bold')
ax1.set_xticks(x_pos)
ax1.set_xticklabels(x_labels, fontsize=16)
ax1.set_ylim([0.0, 1.05])  # Cache hit ratio typically 0-1
ax1.tick_params(axis='both', labelsize=16)
ax1.grid(True, alpha=0.3, linestyle='--')
ax1.text(0.5, -0.27, '(a) Cache Hit Ratio', transform=ax1.transAxes,
         fontsize=20, fontweight='bold', ha='center')

# 2. Execution Time (Bar Graph) Generation
bars = ax2.bar(x_pos, execution_time, width=0.5, color=color, 
        alpha=0.8, edgecolor='black', linewidth=1)

# Add value labels on top of bars
for bar in bars:
    height = bar.get_height()
    ax2.text(bar.get_x() + bar.get_width()/2., height,
             f'{height:.1f}',
             ha='center', va='bottom', fontsize=12, fontweight='bold')

ax2.set_xlabel('Cache Capacity Ratio (%)', fontsize=18, fontweight='bold')
ax2.set_ylabel('Total Data Read Latency (sec)', fontsize=18, fontweight='bold')
ax2.set_xticks(x_pos)
ax2.set_xticklabels(x_labels, fontsize=16)
ax2.set_ylim([0, 100]) 
ax2.tick_params(axis='both', labelsize=16)
ax2.grid(axis='y', alpha=0.3, linestyle='--')
ax2.text(0.5, -0.34, '(b) Total Data Read Latency\n(Epoch 2)', transform=ax2.transAxes,
         fontsize=20, fontweight='bold', ha='center')


# Adjust layout
plt.tight_layout()
plt.subplots_adjust(top=0.90, wspace=0.5)

# Save the figure
plt.savefig('cache-mlperf-sc26.pdf', dpi=300, bbox_inches='tight')
print("Cache hit ratio and execution time plot saved successfully!")
plt.show()
