import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from matplotlib.dates import DateFormatter
import matplotlib.dates as mdates
from datetime import datetime

def create_multi_stock_animation(stock_files):
    # Read and process all CSV files
    dfs = {}
    for file_path in stock_files:
        company = file_path.split('/')[-1].split('.')[0]  # Extract company name from filename
        df = pd.read_csv(file_path)
        df['Date'] = pd.to_datetime(df['Date'], format='%m/%d/%Y')
        df['Close/Last'] = df['Close/Last'].str.replace('$', '').astype(float)
        df = df.sort_values('Date')
        dfs[company] = df
    
    # Create figure and axis
    fig, ax = plt.subplots(figsize=(12, 6))
    
    # Colors for each company
    colors = {'nvidia': 'green', 'intel': 'blue', 'amd': 'red'}
    
    def animate(frame):
        ax.clear()
        
        # Plot data for each company up to current frame
        for company, df in dfs.items():
            data_subset = df.iloc[:frame+1]
            line = ax.plot(data_subset['Date'], data_subset['Close/Last'], 
                    color=colors[company], linewidth=2, marker='', label=company.upper())
            
            # Add price annotation for each company
            if not data_subset.empty:
                latest_price = data_subset['Close/Last'].iloc[-1]
                latest_date = data_subset['Date'].iloc[-1]
                ax.annotate(f'{company.upper()}: ${latest_price:.2f}', 
                           xy=(latest_date, latest_price),
                           xytext=(10, 10), textcoords='offset points',
                           color=colors[company],
                           bbox=dict(facecolor='white', edgecolor='none', alpha=0.7))
        
        # Customize plot
        ax.set_title('Stock Prices Comparison Over Time', fontsize=12, pad=20)
        ax.set_xlabel('Date')
        ax.set_ylabel('Price ($)')
        ax.xaxis.set_major_formatter(DateFormatter('%m/%d/%Y'))
        ax.tick_params(axis='x', rotation=45)
        ax.grid(True, linestyle='--', alpha=0.7)
        ax.legend(loc='upper left')
        
        # Set dynamic y-axis limits
        all_prices = pd.concat([df['Close/Last'] for df in dfs.values()])
        y_min = all_prices.min() * 0.95
        y_max = all_prices.max() * 1.05
        ax.set_ylim(y_min, y_max)
        
        # Set x-axis limits
        all_dates = pd.concat([df['Date'] for df in dfs.values()])
        
        ax.set_xlim(all_dates.min(), all_dates.max())
        
        plt.tight_layout()
    
    # Create animation
    max_frames = max(len(df) for df in dfs.values())
    anim = animation.FuncAnimation(fig, animate, 
                                 frames=max_frames,
                                 interval=50, # Number of ms between each frame
                                 repeat=True)
    
    return fig, anim

# Example usage:
stock_files = ['./data/nvidia.csv', './data/intel.csv', './data/amd.csv']
fig, anim = create_multi_stock_animation(stock_files)
anim.save('./outputs/stock_prices.mp4', writer='ffmpeg', fps=60)
plt.show()
