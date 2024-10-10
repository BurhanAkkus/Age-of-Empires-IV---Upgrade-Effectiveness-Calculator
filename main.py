def calculate_upgrade_effectiveness(upgrade_cost, unit_cost, powerup_factor):
    """
    Calculates the minimum standing army count required to make the upgrade effective.

    Parameters:
    upgrade_cost (float): The cost of the upgrade.
    unit_cost (float): The cost of a single unit.
    powerup_factor (float): The factor by which the unit power is increased by the upgrade.

    Returns:
    float: The minimum standing army count that makes the upgrade effective.
    """
    effectiveness_threshold = upgrade_cost / (unit_cost * (powerup_factor - 1))
    return effectiveness_threshold

# Example usage
upgrade_cost = 300
unit_cost = 50
powerup_factor = 1.2

minimum_army_count = calculate_upgrade_effectiveness(upgrade_cost, unit_cost, powerup_factor)
print("Minimum standing army count to make the upgrade effective:", minimum_army_count)