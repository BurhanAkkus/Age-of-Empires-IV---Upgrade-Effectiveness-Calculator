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

def main():
    print("Welcome to the Age of Empires IV Upgrade Effectiveness Calculator!")

    # List of available units
    unit_names = ["LongBowman", "RoyalKnight"]
    upgrade_names = ["VeteranUpgrade", "BlackSmithFeudalRangedArmor"]

    while True:
        try:
            # User selects a unit
            print("\nAvailable units:")
            for i, name in enumerate(unit_names, 1):
                print(f"{i}. {name}")

            unit_choice = input("\nEnter the number of the unit you want to select or 'quit' to exit: ").strip()
            if unit_choice.lower() == 'quit':
                break

            if not unit_choice.isdigit() or int(unit_choice) < 1 or int(unit_choice) > len(unit_names):
                print("\nInvalid choice. Please select a valid number.")
                continue

            unit_name = unit_names[int(unit_choice) - 1]
            unit = Unit(unit_name)
            print(f"Selected unit: {unit.unit_name}, HP: {unit.hp}, Attack Damage: {unit.attack_damage}")

            # User selects an upgrade
            print("\nAvailable upgrades:")
            for i, name in enumerate(upgrade_names, 1):
                print(f"{i}. {name}")

            upgrade_choice = input("\nEnter the number of the upgrade you want to select: ").strip()
            if not upgrade_choice.isdigit() or int(upgrade_choice) < 1 or int(upgrade_choice) > len(upgrade_names):
                print("\nInvalid choice. Please select a valid number.")
                continue

            upgrade_name = upgrade_names[int(upgrade_choice) - 1]
            upgrade = Upgrade(upgrade_name, unit_name=unit_name)

            # Check if the upgrade has been applied before
            if unit.has_upgrade_been_applied(upgrade):
                print(f"\nUpgrade '{upgrade_name}' has already been applied to unit '{unit_name}'.")
            else:
                # Calculate minimum standing army count for effectiveness
                minimum_army_count = calculate_upgrade_effectiveness(upgrade, unit)
                print(f"\nMinimum standing army count to make the upgrade effective: {minimum_army_count}")

                # Apply the upgrade if the user wants
                apply_upgrade = input(f"\nDo you want to apply the upgrade '{upgrade_name}' to unit '{unit_name}'? (yes/no): ").strip().lower()
                if apply_upgrade == 'yes':
                    unit.apply_upgrade(upgrade)
                    print(f"Upgrade '{upgrade_name}' applied successfully.")

            # List applied upgrades
            print("\nApplied upgrades:")
            for applied_upgrade in unit.list_applied_upgrades():
                print(f"- {applied_upgrade}")

        except ValueError as e:
            print(f"\nError: {e}")
        except Exception as e:
            print(f"\nAn unexpected error occurred: {e}")

    print("\nThank you for using the Age of Empires IV Upgrade Effectiveness Calculator! Goodbye!")

if __name__ == "__main__":
    main()