import matplotlib.pyplot as plt
import math

# Define the linkage lengths and base position
L1 = 20
L2 = 12
base_x = 0
base_y = 37.5

fig, ax = plt.subplots()

# Set the axes
ax.set_xlim(-L1-L2, L1+L2+base_x)
ax.set_ylim(-L1-L2, L1+L2+base_y)
ax.set_aspect('equal', adjustable='box')

# Initial plot
line, = ax.plot([], [], 'ko-')
end_effector, = ax.plot([], [], 'ro')
target, = ax.plot([], [], 'bx')

# Add a text box in the bottom right corner
theta_text = ax.text(0.95, 0.01, '', transform=ax.transAxes, ha='right')

def get_angles(x, y, L1, L2, base_x=0, base_y=37.5):
    # Adjust the target coordinates
    x -= base_x
    y -= base_y

    if math.sqrt(x**2 + y**2) > (L1 + L2):
        raise ValueError("Target is not reachable")

    D = math.sqrt(x**2 + y**2)
    theta2 = math.acos((D**2 - L1**2 - L2**2) / (2 * L1 * L2))
    theta1 = math.atan2(y, x) - math.atan2(L2 * math.sin(theta2), L1 + L2 * math.cos(theta2))

    return math.degrees(theta1), math.degrees(theta2)

def plot_system(event):
    x, y = event.xdata, event.ydata

    if x is None or y is None:  # Ignore if mouse is out of the plot area
        return

    try:
        theta1, theta2 = get_angles(x, y, L1, L2, base_x, base_y)
    except ValueError as e:
        print(e)
        return

    joint1_x = base_x + L1 * math.cos(math.radians(theta1))
    joint1_y = base_y + L1 * math.sin(math.radians(theta1))
    joint2_x = joint1_x + L2 * math.cos(math.radians(theta1 + theta2))
    joint2_y = joint1_y + L2 * math.sin(math.radians(theta1 + theta2))

    # Update linkage plot
    line.set_data([base_x, joint1_x, joint2_x], [base_y, joint1_y, joint2_y])
    end_effector.set_data(joint2_x, joint2_y)

    # Update target position plot
    target.set_data(x, y)

    # Update text box
    theta_text.set_text('Theta1: {:.2f}, Theta2: {:.2f}'.format(theta1, theta2))

    plt.draw()


# Connect the function to the motion_notify_event
fig.canvas.mpl_connect('motion_notify_event', plot_system)

plt.show()
