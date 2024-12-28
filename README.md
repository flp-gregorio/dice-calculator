# Dice Roll Calculator

A simple dice roll calculator application built using **PyQt5** and **Matplotlib**. This tool helps you calculate the average damage and chance to hit based on user input, while also providing a graphical distribution of damage probabilities.

## Features

- **Chance to Hit**: Input the chance to hit in percentage.
- **Advantage**: Option to account for advantage when rolling.
- **Chance Modifiers**: Add modifiers to the chance to hit (e.g., +10).
- **Damage Dice**: Specify the damage dice (e.g., `1d10`).
- **Damage Modifiers**: Add modifiers to the damage (e.g., +5).
- **Damage Distribution Plot**: Visualizes the damage distribution and shows the probability of each damage outcome.

## Requirements

- Python 3.x

## Usage

1. **Chance to Hit**: Enter the chance to hit as a percentage (e.g., 65 for 65%).
2. **Advantage**: Check the box if you have advantage on the roll.
3. **Chance Modifiers**: Enter any chance modifiers (e.g., `+5,-2`) separated by commas.
4. **Damage Dice**: Enter the damage die (e.g., `1d10`).
5. **Damage Modifiers**: Enter any damage modifiers (e.g., `+3`) separated by commas.
6. **Calculate**: Click the "Calculate Average" button to see the average damage and chance to hit.

The program will calculate and display the **Chance to Hit** and **Average Damage**. It will also generate a bar chart showing the distribution of possible damage values.

## Example

- **Chance to Hit**: 65%
- **Has Advantage**: Checked
- **Chance Modifiers**: `+5`
- **Damage Die**: `1d10`
- **Damage Modifiers**: `+3`

### Output

- **Chance to Hit**: 77%
- **Average Damage**: 8

Additionally, a bar chart will display the probability distribution of damage rolls.

## Code Explanation

The code defines a `DiceCalculator` class that:
- Takes user inputs for hit chance, advantage, modifiers, and damage dice.
- Computes the adjusted hit chance based on advantage and modifiers.
- Calculates the average damage based on the provided dice and modifiers.
- Displays a bar chart of the damage distribution for the specified dice and modifiers.

### Damage Distribution Plot

The plot shows the likelihood of each possible damage value based on the number of dice and modifiers, generated from 10,000 simulated rolls.

## License

This project is licensed under the MIT License.

## Contributing

Feel free to fork and contribute to the project. To report bugs or suggest improvements, open an issue on GitHub.

---

Enjoy using the **Dice Roll Calculator**!
