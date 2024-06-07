import matplotlib.pyplot as plt
plt.rcParams["figure.figsize"] = (12,8)

import numpy as np
import pandas as pd
import seaborn as sns

def plot_matrix(matrix, title, filepath):
    data = matrix.to_numpy()

    fig, ax = plt.subplots()
    im = plt.imshow(data, cmap='hot')

    cbar = ax.figure.colorbar(im, ax = ax)

    ax.set_xticks(np.arange(len(matrix.columns)), labels=matrix.columns)
    ax.set_yticks(np.arange(len(matrix.columns)), labels=matrix.columns)

    # Rotate the tick labels and set their alignment.
    plt.setp(ax.get_xticklabels(), rotation=45, ha="right", rotation_mode="anchor")

    ax.set_title(title)
    fig.tight_layout()

    plt.savefig(filepath)

def scatter_plot(similarities, confusion, title, filepath):
    fig, ax = plt.subplots(figsize=(5, 5), layout='constrained')
    print(similarities)
    print(confusion)
    ax.scatter(similarities, confusion)
    ax.set_xlabel('Similarity')
    ax.set_ylabel('Class Confusion')
    plt.savefig(filepath)