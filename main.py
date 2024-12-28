import numpy as np
from matplotlib.figure import Figure
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QVBoxLayout, QWidget, QLabel, QLineEdit, QPushButton, QCheckBox
)
from scipy.stats import gaussian_kde

class DiceCalculator(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Dice Roll Calculator")
        self.setGeometry(100, 100, 500, 400)

        layout = QVBoxLayout()

        # Inputs
        self.enemy_ac_label = QLabel("Enemy AC:")
        layout.addWidget(self.enemy_ac_label)
        self.enemy_ac_input = QLineEdit(self)
        layout.addWidget(self.enemy_ac_input)

        self.weapon_hitdie_label = QLabel("Weapon Hit Die (e.g., 1d20):")
        layout.addWidget(self.weapon_hitdie_label)
        self.weapon_hitdie_input = QLineEdit(self)
        layout.addWidget(self.weapon_hitdie_input)

        self.advantage_label = QCheckBox("Has advantage")
        layout.addWidget(self.advantage_label)

        self.hitchancemod_label = QLabel("Enter chance modifiers, separated by commas:")
        layout.addWidget(self.hitchancemod_label)
        self.hitchancemod_input = QLineEdit(self)
        layout.addWidget(self.hitchancemod_input)

        self.dmgdice_label = QLabel("Enter damage die (e.g., 1d10):")
        layout.addWidget(self.dmgdice_label)
        self.dmgdice_input = QLineEdit(self)
        layout.addWidget(self.dmgdice_input)

        self.dmgmodifier_label = QLabel("Enter damage modifiers, separated by commas:")
        layout.addWidget(self.dmgmodifier_label)
        self.dmgmodifier_input = QLineEdit(self)
        layout.addWidget(self.dmgmodifier_input)

        # Calculate button
        self.calculate_button = QPushButton("Calculate Average")
        self.calculate_button.clicked.connect(self.calculate_average)
        layout.addWidget(self.calculate_button)

        # Result Labels
        self.result1_label = QLabel("Chance to Hit: ")
        layout.addWidget(self.result1_label)

        self.result_label = QLabel("Average Damage: ")
        layout.addWidget(self.result_label)

        # Matplotlib Figure for Graph
        self.figure = Figure()
        self.canvas = FigureCanvas(self.figure)
        layout.addWidget(self.canvas)

        # Set central widget
        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)

    def calculate_average(self):
        enemy_ac = self.enemy_ac_input.text().strip()
        weapon_hitdie = self.weapon_hitdie_input.text().strip()
        hasadvantage = self.advantage_label.isChecked()
        hitchancemod = self.hitchancemod_input.text().strip()
        dmgdice = self.dmgdice_input.text().strip()
        dmgmodifier = self.dmgmodifier_input.text().strip()

        try:
            # Parse enemy AC
            enemy_ac = int(enemy_ac)

            # Parse weapon hit die (e.g., "1d20")
            if "d" not in weapon_hitdie:
                raise ValueError("Invalid weapon hit die format.")
            num_hitdie, sides_hitdie = map(int, weapon_hitdie.split("d"))

            # Calculate base chance to hit
            base_hit_chance = (sides_hitdie - (enemy_ac - 1)) / sides_hitdie

            # Apply chance modifiers (only if not empty)
            if hitchancemod:
                hitchancemod = sum(map(float, hitchancemod.split(",")))
                base_hit_chance += hitchancemod / sides_hitdie
            base_hit_chance = min(max(base_hit_chance, 0), 1)  # Clamp to [0, 1]

            # Apply advantage (if checked)
            if hasadvantage:
                base_hit_chance = base_hit_chance + (1 - base_hit_chance) * base_hit_chance  # Advantage formula

            # Parse damage dice (e.g., "1d10")
            if "d" not in dmgdice:
                raise ValueError("Invalid damage dice format.")
            num_dmgdie, sides_dmgdie = map(int, dmgdice.split("d"))
            avg_dmgroll = (num_dmgdie * (1 + sides_dmgdie)) // 2  # Average roll for each die (rounded down)

            # Parse damage modifiers (only if not empty)
            if dmgmodifier:
                if ',' in dmgmodifier:
                    dmgmodifier = sum(map(int, dmgmodifier.split(",")))
                else:
                    dmgmodifier = int(dmgmodifier)
            else:
                dmgmodifier = 0  # Default to 0 if no modifier is provided

            # Calculate and display result
            total_avg = int(base_hit_chance * (avg_dmgroll + dmgmodifier))  # Round down
            self.result1_label.setText(f"Chance to Hit: {base_hit_chance:.0%}")
            self.result_label.setText(f"Average Damage: {total_avg}")

            # Plot the damage distribution graph
            self.plot_damage_distribution(num_dmgdie, sides_dmgdie, dmgmodifier, base_hit_chance)

        except Exception as e:
            self.result_label.setText(f"Error: {str(e)}")

    def plot_damage_distribution(self, num, sides, modifier, hit_chance):
        # Simulate the damage rolls
        simulated_rolls = np.random.randint(1, sides + 1, size=(10000, num))
        total_rolls = simulated_rolls.sum(axis=1) + modifier
        hit_rolls = total_rolls[np.random.rand(10000) < hit_chance]
        
        # Clear previous figure
        self.figure.clear()
        ax = self.figure.add_subplot(111)

        # Fit a kernel density estimation to smooth the curve
        kde = gaussian_kde(hit_rolls, bw_method=0.5)  # Bandwidth adjusts smoothness
        x_vals = np.linspace(hit_rolls.min(), hit_rolls.max(), 500)
        y_vals = kde(x_vals)

        # Plot the smoothed curve
        ax.plot(x_vals, y_vals, label="Damage Distribution", color="blue")

        # Add mean and standard deviation lines
        mean = np.mean(hit_rolls)
        std_dev = np.std(hit_rolls)
        ax.axvline(mean, color="red", linestyle="--", label=f"Mean: {mean:.2f}")
        ax.axvline(mean + std_dev, color="green", linestyle=":", label=f"Std Dev: {std_dev:.2f}")
        ax.axvline(mean - std_dev, color="green", linestyle=":", label="")

        # Set chart labels and title
        ax.set_title("Damage Distribution (Normalized)")
        ax.set_xlabel("Damage")
        ax.set_ylabel("Probability Density")
        ax.legend()

        # Redraw the canvas
        self.canvas.draw()

if __name__ == "__main__":
    app = QApplication([])
    window = DiceCalculator()
    window.show()
    app.exec_()
