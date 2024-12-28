import numpy as np
from matplotlib.figure import Figure
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QVBoxLayout, QWidget, QLabel, QLineEdit, QPushButton, QCheckBox
)

class DiceCalculator(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Dice Roll Calculator")
        self.setGeometry(100, 100, 500, 400)

        layout = QVBoxLayout()

        # Inputs
        self.hitchance_label = QLabel("Chance to hit (e.g., 65 for 65%):")
        layout.addWidget(self.hitchance_label)
        self.hitchance_input = QLineEdit(self)
        layout.addWidget(self.hitchance_input)

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
        hitchance = self.hitchance_input.text().strip()
        hasadvantage = self.advantage_label.isChecked()
        hitchancemod = self.hitchancemod_input.text().strip()
        dmgdice = self.dmgdice_input.text().strip()
        dmgmodifier = self.dmgmodifier_input.text().strip()

        try:
            # Parse chance to hit
            hitchance = int(hitchance)
            if hitchance < 1 or hitchance > 100:
                raise ValueError("Invalid hit chance.")

            # Apply chance modifiers (only if not empty)
            if hitchancemod:
                hitchancemod = sum(map(float, hitchancemod.split(",")))
                hitchance += hitchancemod * 5
            hitchance = min(max(hitchance, 0), 100)  # Clamp to [0, 100]

            # Apply advantage (if checked)
            hitchance /= 100  # Normalize hit chance to decimal
            if hasadvantage:
                hitchance = hitchance + (1 - hitchance) * hitchance  # Advantage formula

            # Parse damage dice (e.g., "1d10")
            if "d" not in dmgdice:
                raise ValueError("Invalid dice format.")
            num, sides = map(int, dmgdice.split("d"))
            avg_dmgroll = (num * (1 + sides)) / 2  # Average roll for each die

            # Parse damage modifiers (only if not empty)
            if dmgmodifier:
                if ',' in dmgmodifier:
                    dmgmodifier = sum(map(int, dmgmodifier.split(",")))
                else:
                    dmgmodifier = int(dmgmodifier)
            else:
                dmgmodifier = 0  # Default to 0 if no modifier is provided

            # Calculate and display result
            total_avg = avg_dmgroll + dmgmodifier
            self.result1_label.setText(f"Chance to Hit: {hitchance:.0%}")
            self.result_label.setText(f"Average Damage: {total_avg:.0f}")

            # Plot the damage distribution graph
            self.plot_damage_distribution(num, sides, dmgmodifier)

        except Exception as e:
            self.result_label.setText(f"Error: {str(e)}")

    def plot_damage_distribution(self, num, sides, modifier):
        # Plots a bar chart for the damage distribution.
        max_damage = num * sides + modifier
        rolls = np.arange(num, max_damage + 1)
    
        # Simulate the damage rolls
        simulated_rolls = np.random.randint(1, sides + 1, size=(10000, num))
        total_rolls = simulated_rolls.sum(axis=1) + modifier
        
        # Calculate probabilities for each possible damage value
        probabilities = [np.sum(total_rolls == r) / 10000 * 100 for r in rolls]  # Convert to percentage

        # Calculate mean and standard deviation of the damage distribution
        mean = np.mean(total_rolls)
        std_dev = np.std(total_rolls)

        # Clear previous figure
        self.figure.clear()
        ax = self.figure.add_subplot(111)

        # Plot the bar chart
        ax.bar(rolls, probabilities, width=0.8, label="Damage Distribution")

        # Add a vertical line for the mean
        ax.axvline(mean, color="r", linestyle="--", label=f"Mean: {mean:.2f}")
        
        # Set Y-axis ticks in steps of 2.5
        ax.set_yticks(np.arange(0, 12.5, 2.5))  # Y-axis from 0 to 100, in steps of 2.5

        # Set chart labels and title
        ax.set_title("Damage Distribution")
        ax.set_xlabel("Damage")
        ax.set_ylabel("%")  # Y-axis label
        ax.legend()

        # Redraw the canvas
        self.canvas.draw()


if __name__ == "__main__":
    app = QApplication([])
    window = DiceCalculator()
    window.show()
    app.exec_()
