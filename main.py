import json
import math
import copy

from unit import Unit
from upgrade import Upgrade


def basic_effectiveness(unit):
    """
    Calculates the basic effectiveness of the unit.

    Parameters:
    unit (Unit): The unit whose effectiveness is to be calculated.

    Returns:
    float: The effectiveness value, which is the product of unit's HP and attack damage.
    """
    return unit.hp * unit.attack_damage

def calculate_upgrade_effectiveness(upgrade, unit):
    """
    Calculates the minimum standing army count required to make the upgrade effective.

    Parameters:
    upgrade (Upgrade): The upgrade being considered.
    unit (Unit): The unit being upgraded.

    Returns:
    int: The minimum standing army count that makes the upgrade effective (rounded up).
    """
    # Create a copy of the unit and apply the upgrade to the copy
    upgraded_unit = copy.deepcopy(unit)
    upgraded_unit.apply_upgrade(upgrade)

    # Calculate powerup factor as the ratio of upgraded effectiveness to original effectiveness
    powerup_factor = basic_effectiveness(upgraded_unit) / basic_effectiveness(unit)
    print(f"Powerup Factor: {powerup_factor}")

    # Calculate the effectiveness threshold
    effectiveness_threshold = upgrade.cost / (unit.cost * (powerup_factor - 1))
    return math.ceil(effectiveness_threshold)

# Example usage
unit = Unit("LongBowman")
Veteran_LB_upgrade = Upgrade("VeteranUpgrade", unit_name="LongBowman")

# Do not apply the upgrade to the unit, just calculate effectiveness
minimum_army_count = calculate_upgrade_effectiveness(Veteran_LB_upgrade, unit)
print("Minimum standing army count to make the upgrade effective:", minimum_army_count)

# Example usage for research upgrade
upgrade_research = Upgrade("BlackSmithFeudalRangedArmor")

# Combine two upgrades
general_upgrade = Upgrade("VeteranUpgrade", unit_name="LongBowman")
general_upgrade.add_upgrade(upgrade_research)
print(f"Combined Upgrade - HP Bonus: {general_upgrade.hp_bonus}, Attack Bonus: {general_upgrade.attack_bonus}, Melee Armor Bonus: {general_upgrade.melee_armor_bonus}, Ranged Armor Bonus: {general_upgrade.ranged_armor_bonus}, Cost: {general_upgrade.cost}")

# Calculate and print unit effectiveness
effectiveness_value = basic_effectiveness(unit)
print(f"Effectiveness of the unit: {effectiveness_value}")