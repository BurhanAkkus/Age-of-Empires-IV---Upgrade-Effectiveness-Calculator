import json
import math
import copy

from unit import Unit
from upgrade import Upgrade

unit_names = ["LongBowman", "RoyalKnight"]
upgrade_names = [
    "VeteranUpgrade", "EliteUpgrade", "BlackSmithFeudalMeleeArmor",
    "BlackSmithFeudalRangedArmor", "BlackSmithFeudalRangedAttack",
    "BlackSmithCastleMeleeArmor", "BlackSmithCastleRangedArmor",
    "BlackSmithCastleRangedAttack", "BlackSmithImperialRangedArmor",
    "BlackSmithImperialMeleeArmor", "BlackSmithImperialRangedAttack"
]

def get_applicable_upgrades(unit,selected_upgrades):
    applicable_upgrades = []
    for upgrade_name in upgrade_names:
        upgrade = Upgrade(upgrade_name, unit_name=unit.unit_name)
        prerequisites = upgrade.get_prerequisites()
        if ((not prerequisites
            or all(prerequisite in unit.list_applied_upgrades() or prerequisite in [selected_upgrade.upgrade_name for selected_upgrade in selected_upgrades] for prerequisite in prerequisites))
            and not unit.has_upgrade_been_applied(upgrade)
            and not upgrade_name in [selected_upgrade.upgrade_name for selected_upgrade in selected_upgrades]):
            applicable_upgrades.append(upgrade)
    return applicable_upgrades

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
    Calculates the minimum standing army count required to make the upgrades effective.

    Parameters:
    upgrades (list of Upgrade): The upgrades being considered.
    unit (Unit): The unit being upgraded.

    Returns:
    int: The minimum standing army count that makes the upgrades effective (rounded up).
    """
    # Create a copy of the unit and apply the upgrades to the copy
    upgraded_unit = copy.deepcopy(unit)
    for upgrade in upgrades:
        upgraded_unit.apply_upgrade(upgrade)

    # Calculate powerup factor as the ratio of upgraded effectiveness to original effectiveness
    powerup_factor = basic_effectiveness(upgraded_unit) / basic_effectiveness(unit)
    print(f"Powerup Factor: {powerup_factor}")

    # Calculate the effectiveness threshold
    effectiveness_threshold = sum(upgrade.cost for upgrade in upgrades) / (unit.cost * (powerup_factor - 1))
    return math.ceil(effectiveness_threshold)

def main():
    print("Welcome to the Age of Empires IV Upgrade Effectiveness Calculator!")

    # List of available units


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

            while True:# User selects upgrades to combine
                selected_upgrades = []
                while True:
                    applicable_upgrades = get_applicable_upgrades(unit,selected_upgrades)

                    print("\nSelected upgrades:")
                    for i, upgrade in enumerate(selected_upgrades, 1):
                        print(f"{i}. {upgrade.upgrade_name}")
                    print("\nAvailable upgrades:")
                    for i, upgrade in enumerate(applicable_upgrades, 1):
                        print(f"{i}. {upgrade.upgrade_name}")

                    upgrade_choice = input(
                        "\nEnter the number of the upgrade you want to select, 'done' to finish selecting upgrades, or 'back' to choose another unit: ").strip()
                    if upgrade_choice.lower() == 'back':
                        break
                    if upgrade_choice.lower() == 'done':
                        if not selected_upgrades:
                            print("\nYou must select at least one upgrade before proceeding.")
                        else:
                            break

                    if not upgrade_choice.isdigit() or int(upgrade_choice) < 1 or int(upgrade_choice) > len(applicable_upgrades):
                        print("\nInvalid choice. Please select a valid number.")
                        continue
                    else:
                        upgrade = applicable_upgrades[int(upgrade_choice) - 1]
                        selected_upgrades.append(upgrade)
                        applicable_upgrades.remove(upgrade)

                if not selected_upgrades:
                    break

                # Calculate minimum standing army count for effectiveness
                minimum_army_count = calculate_upgrade_effectiveness(selected_upgrades, unit)
                print(f"\nMinimum standing army count to make the selected upgrades effective: {minimum_army_count}")

                # Apply the upgrades if the user wants
                apply_upgrades = input(
                    f"\nDo you want to apply the selected upgrades to unit '{unit_name}'? (yes/no): ").strip().lower()
                if apply_upgrades == 'yes':
                    for upgrade in selected_upgrades:
                        unit.apply_upgrade(upgrade)
                    print(f"Selected upgrades applied successfully.")

                # List applied upgrades
                print("\nApplied upgrades:")
                for applied_upgrade in unit.list_applied_upgrades():
                    print(f"- {applied_upgrade}")
                unit_continue = input("\ndo you want to continue with this unit or select a new one?: (continue/new)").strip()
                if unit_continue.lower() == 'continue':
                    continue
                else:
                    break

        except ValueError as e:
            print(f"\nError: {e}")
        except Exception as e:
            print(f"\nAn unexpected error occurred: {e}")

    print("\nThank you for using the Age of Empires IV Upgrade Effectiveness Calculator! Goodbye!")

if __name__ == "__main__":
    main()