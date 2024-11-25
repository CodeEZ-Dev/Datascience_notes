import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import matplotlib.ticker as ticker
from matplotlib.offsetbox import OffsetImage, AnnotationBbox
import numpy as np
from PIL import Image

def load_flag_images(df, flag_folder):
    """Load and resize all flag images once at startup"""
    flag_images = {}
    for iso_code in df['ISO3_code'].unique():
        try:
            img = Image.open(f"{flag_folder}/{iso_code}.png")
            img.thumbnail((50, 30), Image.Resampling.LANCZOS)
            flag_images[iso_code] = img
        except:
            print(f"Could not load flag for {iso_code}")
    return flag_images

def setup_plot_style(ax):
    """Apply consistent plot styling"""
    ax.set_yticks([])
    ax.set_xlabel('Population (in millions)')
    ax.xaxis.set_major_formatter(ticker.FuncFormatter(lambda x, p: format(int(x), ',')))
    ax.grid(True, axis='x', linestyle='--', alpha=0.7)
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.set_title('Top 10 Populations created by Muralidharan V', pad=20, fontsize=14, fontweight='bold')

def add_timestamp_text(ax, current_time):
    """Add year and month text to plot"""
    plt.text(0.75, 0.15, f'Year: {current_time.year}',
            transform=ax.transAxes, fontsize=12, fontweight='bold',
            bbox=dict(facecolor='white', edgecolor='none', alpha=0.7))
    plt.text(0.75, 0.09, f'Month: {current_time.strftime("%B")}', 
            transform=ax.transAxes, fontsize=12, fontweight='bold',
            bbox=dict(facecolor='white', edgecolor='none', alpha=0.7))

def create_animation(df, flag_folder):
    # Initial setup
    fig, ax = plt.subplots(figsize=(12, 6))
    flag_images = load_flag_images(df, flag_folder)
    
    # Prepare timeline
    df['timestamp'] = pd.to_datetime(df['Time'].astype(str) + '-' + df['Month'].astype(str), format='%Y-%m')
    timestamps = sorted(df['timestamp'].unique())

    # Countries needing extra space to prevent jitter
    unstable_names = {'Germany', 'Mexico', 'Ethiopia', 'Bangladesh'}
    
    def animate(frame):
        ax.clear()
        
        # Get current data
        current_time = timestamps[frame]
        top_10 = df[df['timestamp'] == current_time].nlargest(10, 'Population')
        top_10 = top_10.sort_values('Population', ascending=True).reset_index(drop=True)
        
        # Create base bars
        bars = ax.barh(top_10['Location'], top_10['Population'], alpha=0.3)
        
        # Add visual elements for each country
        for i, row in top_10.iterrows():
            # Add flag
            if row['ISO3_code'] in flag_images:
                img_box = OffsetImage(flag_images[row['ISO3_code']], zoom=0.5)
                ab = AnnotationBbox(img_box, (0, i),
                                  frameon=False,
                                  box_alignment=(0, 0.5),
                                  xybox=(-50, 0),
                                  xycoords=('data', 'data'),
                                  boxcoords="offset points")
                ax.add_artist(ab)
            
            # Add labels
            ax.text(row['Population'], i,
                   f' {row["Population"]:,.2f}',
                   va='center', ha='left', fontweight='bold')
            
            country_name = f"{row['Location']}  " if row['Location'] in unstable_names else row['Location']
            ax.text(-0.1, i, country_name, 
                   ha='right', va='center', transform=ax.get_yaxis_transform())
            
        
        # Style the plot
        setup_plot_style(ax)
        add_timestamp_text(ax, current_time)
        plt.tight_layout()
    
    # Create and return animation
    return animation.FuncAnimation(
        fig, animate, frames=len(timestamps),
        interval=50, repeat=False
    )

# Main execution
if __name__ == "__main__":
    df = pd.read_csv('./data/populations-cleaned.csv')
    anim = create_animation(df, "./flags")
    anim.save('outputs/population_animation.mp4', writer='ffmpeg', fps=30)
    plt.show()