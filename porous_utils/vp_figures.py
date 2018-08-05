import pandas as pd
import matplotlib.pyplot as plt
import argparse
import numpy as np



def main(filename):
    df = pd.read_csv(filename, sep = ';', decimal = ',', index_col = False).dropna(how = 'all')
    df.index = pd.to_datetime(df['Date']+' '+df['Time'])
    df = df.loc[df.index.dropna()]
    df =df[df.columns[2:11]]
    df =df.astype(float)

    fig, axes = plt.subplots(nrows = 3, ncols = 1, figsize = (15,9))
    for i in range(3):
        dfi = df[df.columns[3*i:3*i+3]]
        dfi.plot(ax = axes[i])

    axes[0].set_title(f"file: {filename}")
    fig.tight_layout()
    fig.savefig(filename[:-3]+'png', dpi = 300)

__all__ = ['main']    

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="""Script to figures of pump parameters work from csv file 
        
        Example:
        vp_figures.py 20.03A.csv
        
        """,
        formatter_class=argparse.RawDescriptionHelpFormatter)
    
    parser.add_argument('filename', help='name of file')
    args = parser.parse_args()
    
    main(args.filename)
    




