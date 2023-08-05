import matplotlib.pyplot as plt
import pandas as pd

def distribution_for(data: pd.DataFrame, bins=35, figsize=(10, 5)):

    fig, ax = plt.subplots(figsize=figsize)
    ax.hist(data["value"].dropna(), bins)

    return fig