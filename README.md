# Age of Empires IV Upgrade Effectiveness Calculator

This repository contains a Python tool designed to help Age of Empires IV players evaluate the cost-effectiveness of unit upgrades. The tool allows you to calculate the minimum standing army count required to justify the cost of upgrades, helping you make informed strategic decisions.

## Features
- **Unit and Upgrade Definition**: Define units and their stats.
- **Upgrade Impact Calculation**: Calculate the basic effectiveness of units and how different upgrades affect them.
- **Combine Upgrades**: Combine multiple upgrades and evaluate their cumulative effects on units.
- **Customizable JSON Files**: Easily modify JSON files to add or update units and upgrades.

## Usage
1. Clone this repository.
2. Install the necessary dependencies using:
   ```sh
   pip install -r requirements.txt
   ```
3. Edit the `unit_stats.json` and `upgrade_stats.json` files to define your units and upgrades.
4. Run the script to calculate upgrade effectiveness and minimum army count.

## Example
Here's a basic example of how to use the tool:
```python
unit = Unit("LongBowman", "Feudal")
upgrade = Upgrade("FeudalUpgrade", unit_name="LongBowman")
minimum_army_count = calculate_upgrade_effectiveness(upgrade, unit)
print("Minimum standing army count to make the upgrade effective:", minimum_army_count)
```

## Future Plans
In the future, I plan to add the following features to enhance the upgrade effectiveness calculator:

1. **Unit Types**: Add unit categorization as Ranged or Melee to better simulate different combat scenarios.

2. **Scaling Factor (Unit, NumberOfUnits)**: Implement a scaling factor to handle the nonlinear relationship between army effectiveness and unit count, considering effects such as:
   - Overkilling for ranged units.
   - Pathing and crowding issues for melee units.

3. **Upgrade Effectiveness Against Enemies**: Extend the `calculate_upgrade_effectiveness` function to take into account the enemy's armor and attack damage, providing a more comprehensive evaluation of the effectiveness of upgrades in various combat situations.

These features will bring more depth and accuracy to the calculations, making the tool a more powerful resource for players seeking strategic insights.

## Contributing
Contributions are welcome! Feel free to submit issues or pull requests to enhance the tool.

## License
This project is licensed under the MIT License.
