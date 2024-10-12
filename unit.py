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
        self.applied_upgrades = []  # List to track applied upgrades

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
            self.type = stats['type']
            self.hp = stats['hp']
            self.ranged_attack_damage = stats['ranged_attack_damage']
            self.melee_attack_damage = stats['melee_attack_damage']
            self.melee_armor = stats['melee_armor']
            self.ranged_armor = stats['ranged_armor']
            self.cost = stats['cost']
        else:
            raise ValueError(f"Unit '{self.unit_name}' not found in stats file.")

    def apply_upgrade(self, upgrade):
        """
        Applies the bonuses from the upgrade to the unit and tracks the applied upgrade.

        Parameters:
        upgrade (Upgrade): The upgrade to be applied to the unit.
        """
        if self.has_upgrade_been_applied(upgrade):
            raise ValueError(f"Upgrade '{upgrade.upgrade_name}' has already been applied to unit '{self.unit_name}'.")

        if upgrade.unit_name is None or upgrade.unit_name == self.unit_name:
            self.hp += upgrade.hp_bonus
            if(self.type == 'Ranged'):
                self.ranged_attack_damage += upgrade.ranged_attack_bonus
            else:
                self.melee_attack_damage += upgrade.melee_attack_bonus
            self.melee_armor += upgrade.melee_armor_bonus
            self.ranged_armor += upgrade.ranged_armor_bonus
            self.applied_upgrades.append(upgrade.upgrade_name)  # Track the applied upgrade
        else:
            raise ValueError(f"Upgrade '{upgrade.upgrade_name}' is not applicable to unit '{self.unit_name}'.")

    def list_applied_upgrades(self):
        """
        Returns a list of applied upgrades.

        Returns:
        list: A list of upgrade names that have been applied to the unit.
        """
        return self.applied_upgrades

    def has_upgrade_been_applied(self, upgrade):
        """
        Checks if the given upgrade has been applied to the unit.

        Parameters:
        upgrade (Upgrade): The upgrade to check.

        Returns:
        bool: True if the upgrade has been applied, False otherwise.
        """
        return upgrade.upgrade_name in self.applied_upgrades

    def getAttack(self):
        if(self.type == 'Ranged'):
            return self.ranged_attack_damage
        return self.melee_attack_damage