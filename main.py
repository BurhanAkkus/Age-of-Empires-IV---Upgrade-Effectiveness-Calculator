import json
import math
import copy

class Unit:
    _unit_stats_cache = None

    def __init__(self, unit_name, age):
        """
        Represents a unit in Age of Empires IV.

        Parameters:
        unit_name (str): The name of the unit.
        age (str): The age in which the unit exists (Dark Age, Feudal, Castle, Imperial).
        """
        self.unit_name = unit_name
        self.age = age
        self.lookup_stats()

    @classmethod
    def load_unit_stats(cls):
        """
        Loads unit stats from the JSON file if not already loaded.
        """
        if cls._unit_stats_cache is None:
            with open('unit_stats.json', 'r') as f:
                cls._unit_stats_cache = json.load(f)

    def lookup_stats(self):
        """
        Looks up unit stats from a predefined JSON file based on unit name and age.
        """
        Unit.load_unit_stats()
        if self.unit_name in Unit._unit_stats_cache:
            age_stats = Unit._unit_stats_cache[self.unit_name].get(self.age, None)
            if age_stats:
                self.hp = age_stats['hp']
                self.attack_damage = age_stats['attack_damage']
                self.melee_armor = age_stats['melee_armor']
                self.ranged_armor = age_stats['ranged_armor']
                self.cost = age_stats['cost']
            else:
                raise ValueError(f"Stats for unit '{self.unit_name}' in age '{self.age}' not found.")
        else:
            raise ValueError(f"Unit '{self.unit_name}' not found in stats file.")

    def apply_upgrade(self, upgrade):
        """
        Applies the bonuses from the upgrade to the unit.

        Parameters:
        upgrade (Upgrade): The upgrade to be applied to the unit.
        """
        if upgrade.type == "Ageup" and upgrade.unit_name == self.unit_name:
            self.hp += upgrade.hp_bonus
            self.attack_damage += upgrade.attack_bonus
            self.melee_armor += upgrade.melee_armor_bonus
            self.ranged_armor += upgrade.ranged_armor_bonus
        elif upgrade.type == "Research":
            self.hp += upgrade.hp_bonus
            self.attack_damage += upgrade.attack_bonus
            self.melee_armor += upgrade.melee_armor_bonus
            self.ranged_armor += upgrade.ranged_armor_bonus
        else:
            raise ValueError(f"Upgrade '{upgrade.upgrade_name}' is not applicable to unit '{self.unit_name}'.")

class Upgrade:
    _upgrade_stats_cache = None

    def __init__(self, upgrade_name, unit_name=None):
        """
        Represents an upgrade in Age of Empires IV.

        Parameters:
        upgrade_name (str): The name of the upgrade.
        unit_name (str, optional): The name of the unit associated with the upgrade.
        """
        self.upgrade_name = upgrade_name
        self.unit_name = unit_name
        self.lookup_stats()

    @classmethod
    def load_upgrade_stats(cls):
        """
        Loads upgrade stats from the JSON file if not already loaded.
        """
        if cls._upgrade_stats_cache is None:
            with open('upgrade_stats.json', 'r') as f:
                cls._upgrade_stats_cache = json.load(f)

    def lookup_stats(self):
        """
        Looks up upgrade stats from a predefined JSON file based on upgrade name.
        """
        Upgrade.load_upgrade_stats()
        if self.upgrade_name in Upgrade._upgrade_stats_cache:
            stats = Upgrade._upgrade_stats_cache[self.upgrade_name]
            self.type = stats['type']
            self.cost = stats['cost']
            if self.type == "Ageup" and self.unit_name:
                bonuses = stats['bonuses'].get(self.unit_name, None)
                if bonuses:
                    self.hp_bonus = bonuses['hp_bonus']
                    self.attack_bonus = bonuses['attack_bonus']
                    self.melee_armor_bonus = bonuses['melee_armor_bonus']
                    self.ranged_armor_bonus = bonuses['ranged_armor_bonus']
                else:
                    raise ValueError(f"No specific bonuses found for unit '{self.unit_name}' in upgrade '{self.upgrade_name}'.")
            elif self.type == "Research":
                self.attack_bonus = stats['attack_bonus']
                self.hp_bonus = stats['hp_bonus']
                self.melee_armor_bonus = stats['melee_armor_bonus']
                self.ranged_armor_bonus = stats['ranged_armor_bonus']
            else:
                raise ValueError(f"Upgrade '{self.upgrade_name}' requires a unit name for Ageup type upgrades.")
        else:
            raise ValueError(f"Upgrade '{self.upgrade_name}' not found in stats file.")

    def add_upgrade(self, other_upgrade):
        """
        Combines the effects of another upgrade with this one.

        Parameters:
        other_upgrade (Upgrade): The upgrade to be combined with this one.
        """
        self.attack_bonus += other_upgrade.attack_bonus
        self.hp_bonus += other_upgrade.hp_bonus
        self.melee_armor_bonus += other_upgrade.melee_armor_bonus
        self.ranged_armor_bonus += other_upgrade.ranged_armor_bonus
        self.cost += other_upgrade.cost

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
unit = Unit("LongBowman", "Feudal")
upgrade = Upgrade("FeudalUpgrade", unit_name="LongBowman")

# Do not apply the upgrade to the unit, just calculate effectiveness
minimum_army_count = calculate_upgrade_effectiveness(upgrade, unit)
print("Minimum standing army count to make the upgrade effective:", minimum_army_count)

# Example usage for research upgrade
upgrade_research = Upgrade("BlackSmithFeudalRangedArmor")

# Combine two upgrades
general_upgrade = Upgrade("FeudalUpgrade", unit_name="LongBowman")
general_upgrade.add_upgrade(upgrade_research)
print(f"Combined Upgrade - HP Bonus: {general_upgrade.hp_bonus}, Attack Bonus: {general_upgrade.attack_bonus}, Melee Armor Bonus: {general_upgrade.melee_armor_bonus}, Ranged Armor Bonus: {general_upgrade.ranged_armor_bonus}, Cost: {general_upgrade.cost}")

# Calculate and print unit effectiveness
effectiveness_value = basic_effectiveness(unit)
print(f"Effectiveness of the unit: {effectiveness_value}")