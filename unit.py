import json
class Unit:
    _unit_stats_cache = None

    def __init__(self, unit_name):
        """
        Represents a unit in Age of Empires IV.

        Parameters:
        unit_name (str): The name of the unit.
        """
        self.unit_name = unit_name
        self.lookup_stats()

    @classmethod
    def load_unit_stats(cls):
        """
        Loads unit stats from a predefined JSON file if not already loaded.
        """
        if cls._unit_stats_cache is None:
            with open('unit_stats.json', 'r') as f:
                cls._unit_stats_cache = json.load(f)

    def lookup_stats(self):
        """
        Looks up unit stats from a predefined JSON file based on unit name.
        """
        Unit.load_unit_stats()
        if self.unit_name in Unit._unit_stats_cache:
            stats = Unit._unit_stats_cache[self.unit_name]
            self.hp = stats['hp']
            self.attack_damage = stats['attack_damage']
            self.melee_armor = stats['melee_armor']
            self.ranged_armor = stats['ranged_armor']
            self.cost = stats['cost']
        else:
            raise ValueError(f"Unit '{self.unit_name}' not found in stats file.")\


    def apply_upgrade(self, upgrade):
        """
        Applies the bonuses from the upgrade to the unit.

        Parameters:
        upgrade (Upgrade): The upgrade to be applied to the unit.
        """
        if upgrade.unit_name is None or upgrade.unit_name == self.unit_name:
            self.hp += upgrade.hp_bonus
            self.attack_damage += upgrade.attack_bonus
            self.melee_armor += upgrade.melee_armor_bonus
            self.ranged_armor += upgrade.ranged_armor_bonus
        else:
            raise ValueError(f"Upgrade '{upgrade.upgrade_name}' is not applicable to unit '{self.unit_name}'.")
