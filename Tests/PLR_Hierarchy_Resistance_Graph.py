import matplotlib.pyplot as plt
import numpy as np

def generate_hierarchy_chart():
    print("Generating 'PLR_Hierarchy_of_Resistance.png'...")
    
    # Data
    channels = [
        "Messy Channel\n(Mod 6)", 
        "Clean Channel\n(Mod 6)", 
        "Super-Clean\n(Mod 30)", 
        "The Vacuum\n(Mod 210)"
    ]
    
    failure_rates = [21.60, 1.45, 0.14, 0.00008]
    
    colors = ['#d62728', '#bcbd22', '#2ca02c', '#1f77b4'] # Red, Yellow-Green, Green, Blue
    
    plt.figure(figsize=(10, 7))
    
    # Logarithmic Bar Chart
    bars = plt.bar(channels, failure_rates, color=colors, alpha=0.8, edgecolor='black')
    
    plt.yscale('log') # Critical for seeing 21% and 0.00008% on same chart
    
    plt.ylabel('Structural Resistance (Failure Rate %)', fontsize=12)
    plt.title('The Hierarchy of Resistance: Collapse of the Composite Noise', fontsize=14, pad=20)
    
    # Add Text Labels on top of bars
    for bar, rate in zip(bars, failure_rates):
        height = bar.get_height()
        # Adjust text position for log scale
        plt.text(bar.get_x() + bar.get_width()/2., height * 1.2,
                f'{rate}%',
                ha='center', va='bottom', fontsize=11, fontweight='bold')

    # Add annotation for the drop
    plt.annotate('1,700x Improvement', 
                xy=(3, 0.00008), xytext=(2, 0.005),
                arrowprops=dict(facecolor='black', shrink=0.15, width=1, headwidth=8))

    plt.grid(axis='y', linestyle='--', alpha=0.3, which='both')
    
    # Save
    output_file = "PLR_Hierarchy_of_Resistance.png"
    plt.savefig(output_file, dpi=150, bbox_inches='tight')
    print(f"Graph saved to {output_file}")

if __name__ == "__main__":
    generate_hierarchy_chart()