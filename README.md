# Age of Empires IV Upgrade Effectiveness Calculator

This repository contains a Python tool designed to help Age of Empires IV players evaluate the cost-effectiveness of unit upgrades. The tool allows you to calculate the minimum standing army count required to justify the cost of upgrades, helping you make informed strategic decisions.

## Features
- **Unit and Upgrade Definition**: Define units and their stats for different ages (Dark Age, Feudal, Castle, Imperial).
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

## Contributing
Contributions are welcome! Feel free to submit issues or pull requests to enhance the tool.

## License
This project is licensed under the MIT License.

