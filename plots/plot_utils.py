import matplotlib.pyplot as plt
import matplotlib.patches as patches

def create_pitch():
    fig, ax = plt.subplots(figsize=(10, 7))

    # Pitch Outline & Centre Line
    plt.plot([0, 0], [0, 90], color="black")
    plt.plot([0, 130], [90, 90], color="black")
    plt.plot([130, 130], [90, 0], color="black")
    plt.plot([130, 0], [0, 0], color="black")
    plt.plot([65, 65], [0, 90], color="black")

    # Left Penalty Area
    plt.plot([16.5, 16.5], [65, 25], color="black")
    plt.plot([0, 16.5], [65, 65], color="black")
    plt.plot([16.5, 0], [25, 25], color="black")

    # Right Penalty Area
    plt.plot([130, 113.5], [65, 65], color="black")
    plt.plot([113.5, 113.5], [65, 25], color="black")
    plt.plot([113.5, 130], [25, 25], color="black")

    # Left 6-yard Box
    plt.plot([0, 5.5], [54, 54], color="black")
    plt.plot([5.5, 5.5], [54, 36], color="black")
    plt.plot([5.5, 0], [36, 36], color="black")

    # Right 6-yard Box
    plt.plot([130, 124.5], [54, 54], color="black")
    plt.plot([124.5, 124.5], [54, 36], color="black")
    plt.plot([124.5, 130], [36, 36], color="black")

    # Prepare Circles
    centreCircle = plt.Circle((65, 45), 9.15, color="black", fill=False)
    centreSpot = plt.Circle((65, 45), 0.8, color="black")
    leftPenSpot = plt.Circle((11, 45), 0.8, color="black")
    rightPenSpot = plt.Circle((119, 45), 0.8, color="black")

    # Draw Circles
    ax.add_patch(centreCircle)
    ax.add_patch(centreSpot)
    ax.add_patch(leftPenSpot)
    ax.add_patch(rightPenSpot)

    # Draw Arcs
    leftArc = patches.Arc((11, 45), height=18.3, width=18.3, angle=0, theta1=308, theta2=52, color="black")
    rightArc = patches.Arc((119, 45), height=18.3, width=18.3, angle=0, theta1=128, theta2=232, color="black")

    ax.add_patch(leftArc)
    ax.add_patch(rightArc)

    # Tidy Axes
    plt.axis('off')

    return fig, ax


def update_plot(frame, ax, player_positions):
    ax.clear()
    fig, ax = create_pitch()

    for (x, y) in player_positions:
        ax.plot(x, y, 'o', color='blue')

    plt.draw()