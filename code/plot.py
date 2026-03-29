import matplotlib.pyplot as plt
import numpy as np


experiments = ['1 DN, 1 Worker\nBaseline', '1 DN, 1 Worker\nOptimized', '3 DN, 1 Worker\nBaseline', '3 DN, 1 Worker\nOptimized', '3 DN, 3 Workers\nBaseline', '3 DN, 3 Workers\nOptimized']

action_time_sec = [10.84, 2.59, 9.63, 2.55, 7.27, 2.31]
total_time_sec = [51.50, 57.69, 43.23, 54.50, 34.44, 39.32]
ram_mb = [28.93, 28.97, 28.90, 28.96, 28.78, 28.81]

fig, axes = plt.subplots(1, 3, figsize=(24, 6))
fig.suptitle('Baseline vs Optimized (Hadoop/Spark)', fontsize=16)

x = np.arange(len(experiments))
width = 0.6

# Action time
bars1 = axes[0].bar(x, action_time_sec, width, color=['#e74c3c', '#2ecc71', '#c0392b', '#27ae60', "#ac2e20", "#1d924e"])
axes[0].set_title('Aggregation execution time (Action)')
axes[0].set_ylabel('Seconds')
axes[0].set_xticks(x)
axes[0].set_xticklabels(experiments)
axes[0].grid(axis='y', linestyle='--', alpha=0.7)
for bar in bars1:
    yval = bar.get_height()
    axes[0].text(bar.get_x() + bar.get_width()/2, yval + 0.1, f'{yval}s', ha='center', va='bottom')

# Total time
bars2 = axes[1].bar(x, total_time_sec, width, color=['#3498db', '#9b59b6', '#2980b9', '#8e44ad', "#1c6a9e", "#752f92"])
axes[1].set_title('Общее время работы скрипта')
axes[1].set_ylabel('Seconds')
axes[1].set_xticks(x)
axes[1].set_xticklabels(experiments)
axes[1].grid(axis='y', linestyle='--', alpha=0.7)
for bar in bars2:
    yval = bar.get_height()
    axes[1].text(bar.get_x() + bar.get_width()/2, yval + 1, f'{yval}s', ha='center', va='bottom')

# RAM consumption
bars3 = axes[2].bar(x, ram_mb, width, color='#95a5a6')
axes[2].set_title('RAM Consumption (Driver Node)')
axes[2].set_ylabel('Memory (MB)')
axes[2].set_xticks(x)
axes[2].set_xticklabels(experiments)
axes[2].set_ylim(0, 40)
axes[2].grid(axis='y', linestyle='--', alpha=0.7)
for bar in bars3:
    yval = bar.get_height()
    axes[2].text(bar.get_x() + bar.get_width()/2, yval + 0.5, f'{yval:.2f} MB', ha='center', va='bottom')

plt.tight_layout()
plt.subplots_adjust(top=0.88)

plt.savefig('spark_experiments_results.png', dpi=300)
print("Done. Saved to 'spark_experiments_results.png'")
