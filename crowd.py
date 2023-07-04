import matplotlib.pyplot as plt
import numpy as np


class Person:
    def __init__(self, x, y, vx, vy, radius = 1):
        self.x = x
        self.y = y
        self.vx = vx
        self.vy = vy
        self.radius = radius

    def update_position(self):
        self.x += self.vx*0.1
        self.y += self.vy*0.1

        # Check boundaries and reverse velocity if needed
        if self.x <= self.radius or self.x >= 100 - self.radius:
            self.vx *= -1
        if self.y <= self.radius or self.y >= 100 - self.radius:
            self.vy *= -1

    def check_collision(self, other):
        if np.sqrt((other.x - self.x)**2 + (other.y - self.y)**2) < self.radius + other.radius:
            return True
        return False
    
def simulate_crowd(grid_size, num_steps, num_people):
    fig, ax = plt.subplots()
    ax.set_xlim(0, grid_size)
    ax.set_ylim(0, grid_size)
    ax.set_aspect('equal')

    crowd = []
    for i in range(num_people):
        x = np.random.randint(0, grid_size)
        y = np.random.randint(0, grid_size)
        vx = np.random.randint(-5, 5)
        vy = np.random.randint(-5, 5)
        crowd.append(Person(x, y, vx, vy))

    ax.set_title("Step: 0")
    ax.set_xlabel("X")
    ax.set_ylabel("Y")

    for person in crowd:
        ax.plot(person.x, person.y, 'o', color='blue')

    for step in range(num_steps):
        for person in crowd:
            person.update_position()
            for other in crowd:
                if person != other:
                    if person.check_collision(other):
                        person.vx *= -1
                        person.vy *= -1
                        other.vx *= -1
                        other.vy *= -1
        ax.clear()
        ax.set_title(f"Step: {step+1}")
        ax.set_xlabel("X")
        ax.set_ylabel("Y")
        ax.set_xlim(0, grid_size)
        ax.set_ylim(0, grid_size)
        ax.set_aspect('equal')
        for person in crowd:
            ax.plot(person.x, person.y, 'o', color='blue')
        plt.pause(0.01)

simulate_crowd(100, 2000, 40)
