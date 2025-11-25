import matplotlib.pyplot as plt
import matplotlib.patches as patches

def generate_black_box_flowchart():
    print("Generating 'PLR_Black_Box_Workflow.png'...")
    
    fig, ax = plt.subplots(figsize=(12, 8))
    ax.set_xlim(0, 12)
    ax.set_ylim(0, 8)
    ax.axis('off')
    
    # Define Box Style
    box_style = dict(boxstyle="round,pad=0.5", ec="black", lw=2)
    
    # 1. Input
    ax.text(2, 6.5, "Input:\nInteger Sequence\n$1 \dots N$", ha="center", va="center", size=12,
            bbox=dict(facecolor="#e0e0e0", **box_style))
    
    # Arrow 1
    ax.annotate("", xy=(4, 6.5), xytext=(3, 6.5), arrowprops=dict(arrowstyle="->", lw=2))
    
    # 2. The Engine (Center)
    # Using raw string and manual mod formatting to be safe
    ax.text(6, 6.5, r"THE ENGINE" + "\n" + r"[PLR GEOMETRIC SIEVE]" + "\n\n" + r"Logic: $S_n$ (mod 6) Exclusion" + "\n" + r"(NO PNT Parameters)", 
            ha="center", va="center", size=12, fontweight='bold',
            bbox=dict(facecolor="#add8e6", **box_style))
            
    # Arrow 2
    ax.annotate("", xy=(9, 6.5), xytext=(8, 6.5), arrowprops=dict(arrowstyle="->", lw=2))
    
    # 3. Output
    ax.text(10.5, 6.5, "Output:\nFiltered Candidate\nStream", ha="center", va="center", size=12,
            bbox=dict(facecolor="#e0e0e0", **box_style))
            
    # Arrow 3 (Down)
    ax.annotate("", xy=(10.5, 5), xytext=(10.5, 5.8), arrowprops=dict(arrowstyle="->", lw=2))
    
    # 4. Measurement
    ax.text(10.5, 4, "Measurement:\nMeasured Density", ha="center", va="center", size=12,
            bbox=dict(facecolor="#ffffcc", **box_style))
            
    # 5. Comparison (Side Loop) - Coming from Left
    ax.text(2, 4, "Independent Theory:\nHardy-Littlewood\nPrediction ($1.32032...$)", ha="center", va="center", size=12,
            bbox=dict(facecolor="#ffcccc", **box_style))
            
    # Arrow 4 (Measurement Down)
#     ax.annotate("", xy=(10.5, 2.5), xytext=(10.5, 3.2), arrowprops=dict(arrowstyle="->", lw=2))
    
    # 6. Result
    ax.text(6, 1.5, "RESULT:\n[CONVERGENCE]", ha="center", va="center", size=14, fontweight='bold',
            bbox=dict(facecolor="#90ee90", **box_style))
            
    # Arrows connecting to Result
    # From Measurement
    ax.annotate("", xy=(7.5, 1.5), xytext=(10.5, 3.2), 
                arrowprops=dict(arrowstyle="->", connectionstyle="arc3,rad=-0.2", lw=2))
    
    # From Comparison
    ax.annotate("", xy=(4.5, 1.5), xytext=(2, 3.2), 
                arrowprops=dict(arrowstyle="->", connectionstyle="arc3,rad=0.2", lw=2))
                
    # Title/Caption
    plt.title('The "Black Box" Workflow (Non-Circularity Proof)', fontsize=16, fontweight='bold', pad=20)
    
    # Caption Text at bottom
    caption = ("The PLR Sieve generates the candidate stream using only local modular geometry,\n"
               "independent of asymptotic constants. The resulting convergence with the Hardy-Littlewood\n"
               "constant serves as an independent mechanical verification of the probabilistic theory.")
    ax.text(6, 0.2, caption, ha="center", va="center", size=11, style='italic', wrap=True)

    # Save
    output_file = "PLR_Black_Box_Workflow.png"
    plt.savefig(output_file, dpi=150, bbox_inches='tight')
    print(f"Graph saved to {output_file}")

if __name__ == "__main__":
    generate_black_box_flowchart()