import matplotlib.pyplot as plt

amino_colors = {
    'P': 'black',
    'H': 'blue',
    'C': 'red'
}

def plot_path(protein):
    ''' visualisation of folded protein '''
    x_positions = []
    y_positions = []
    point_markers = []
    for amino, position in protein.path:
        x = position[0]
        y = position[1]
        x_positions.append(x)
        y_positions.append(y)

        plt.text(x, y, amino, horizontalalignment='center', verticalalignment='center', color=amino_colors[amino])
    plt.title(f"stability: {protein.stability}")
    plt.plot(x_positions, y_positions, 'ko-', markerfacecolor='white', markersize=15)
    plt.axis('off')
    plt.show()
