import json
import math

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

class Upgrade:
    def __init__(self, attack_bonus, hp_bonus, melee_armor_bonus, ranged_armor_bonus, cost):
        """
        Represents an upgrade in Age of Empires IV.

        Parameters:
        attack_bonus (int): The additional attack bonus provided by the upgrade.
        hp_bonus (int): The additional HP bonus provided by the upgrade.
        melee_armor_bonus (int): The additional melee armor bonus provided by the upgrade.
        ranged_armor_bonus (int): The additional ranged armor bonus provided by the upgrade.
        cost (float): The cost of the upgrade.
        """
        self.attack_bonus = attack_bonus
        self.hp_bonus = hp_bonus
        self.melee_armor_bonus = melee_armor_bonus
        self.ranged_armor_bonus = ranged_armor_bonus
        self.cost = cost

def calculate_upgrade_effectiveness(upgrade, unit):
    """
    Calculates the minimum standing army count required to make the upgrade effective.

    Parameters:
    upgrade (Upgrade): The upgrade being considered.
    unit (Unit): The unit being upgraded.

    Returns:
    int: The minimum standing army count that makes the upgrade effective (rounded up).
    """
    powerup_factor = ((unit.hp + upgrade.hp_bonus) * (unit.attack_damage + upgrade.attack_bonus)) / (unit.hp * unit.attack_damage)
    print(f"Powerup Factor: {powerup_factor}")
    effectiveness_threshold = upgrade.cost / (unit.cost * (powerup_factor - 1))
    return math.ceil(effectiveness_threshold)

# Example usage
unit = Unit("LongBowman", "Feudal")
upgrade = Upgrade(attack_bonus=1, hp_bonus=0, melee_armor_bonus=0, ranged_armor_bonus=0, cost=175)

minimum_army_count = calculate_upgrade_effectiveness(upgrade, unit)
print("Minimum standing army count to make the upgrade effective:", minimum_army_count)