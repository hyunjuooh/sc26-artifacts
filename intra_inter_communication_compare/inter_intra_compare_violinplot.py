import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import os
import glob

# The main directory containing your results folders
BASE_DIRECTORY = "." 

# Node counts tested
NODE_COUNTS = [2, 4, 8, 16, 32] 

# Payload size
MESSAGE_SIZE_MB = 256

all_data = []

# Loop through each node count directory
for nodes in NODE_COUNTS:
    data_path = os.path.join(BASE_DIRECTORY, f"{nodes}nodes")
    if not os.path.isdir(data_path):
        print(f"Warning: Directory not found, skipping: {data_path}")
        continue

    print(f"Processing directory: {data_path}")

    # Load Memcpy data
    # Use glob to find all memcpy files
    memcpy_files = glob.glob(os.path.join(data_path, "*_memcpy.csv"))
    if memcpy_files:
        df = pd.concat([pd.read_csv(f) for f in memcpy_files], ignore_index=True)
        df['type'] = 'Intra-Node Memcpy'
        df['nodes'] = f'{nodes} Nodes' # Convert to string for categorical plotting
        all_data.append(df)

    # Load Intra-node MPI_Get data
    intra_files = glob.glob(os.path.join(data_path, "rank0*_intra_mpiget.csv")) # or use "*_intra_mpiget.csv"
    if intra_files:
        df = pd.concat([pd.read_csv(f) for f in intra_files], ignore_index=True)
        df['type'] = 'Intra-Node MPI_Get'
        df['nodes'] = f'{nodes} Nodes'
        all_data.append(df)

    # Load Inter-node MPI_Get data
    inter_files = glob.glob(os.path.join(data_path, "rank0*_inter_mpiget.csv"))
    if inter_files:
        df = pd.concat([pd.read_csv(f) for f in inter_files], ignore_index=True)
        df['type'] = 'Inter-Node MPI_Get'
        df['nodes'] = f'{nodes} Nodes'
        all_data.append(df)

# Combine all loaded data into a single DataFrame
if not all_data:
    print("Error: No data was loaded. Check your directory structure and file names.")
    exit()

combined_df = pd.concat(all_data, ignore_index=True)

# Define an order for the plot categories
type_order = ['Intra-Node Memcpy', 'Intra-Node MPI_Get', 'Inter-Node MPI_Get']
combined_df['type'] = pd.Categorical(combined_df['type'], categories=type_order, ordered=True)

print("Data processing complete.")
print("Generating plot...")
plt.figure(figsize=(16, 9))

# Create the violin plot with swapped axes
# x='type': Groups the data by the communication type on the x-axis.
# y='time_s': The timing values to plot on the y-axis.
# hue='nodes': Creates separate, colored violins for each node count.
sns.violinplot(x='type', y='time_s', hue='nodes', data=combined_df, cut=0)

plt.title(f'Intra-Node vs. Inter-Node Communication Cost ({MESSAGE_SIZE_MB}MB Payload)', fontsize=32, pad=30)
plt.ylabel('Time per Operation (seconds)', fontsize=26, labelpad=30)
plt.xlabel('Communication Type', fontsize=26, labelpad=30)
plt.tick_params(axis='x', labelsize=24)
plt.tick_params(axis='y', labelsize=24)
plt.yscale('log') # Use a log scale for time, as values can vary widely
plt.grid(True, which="both", ls="--", alpha=0.6)
plt.legend(title='Node Count')
plt.tight_layout()

output_filename = "mpi_scaling_performance_256MB.pdf"
plt.savefig(output_filename, format='pdf', dpi=300, bbox_inches='tight')

print(f"Plot saved successfully to {output_filename}")