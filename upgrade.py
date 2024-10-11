import json

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

        # Initialize bonuses to default values
        self.hp_bonus = 0
        self.attack_bonus = 0
        self.melee_armor_bonus = 0
        self.ranged_armor_bonus = 0
        self.cost = 0
        self.type = None  # Add the type attribute here

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
            self.cost = stats['cost']
            self.type = stats['type']  # Set the type attribute from stats

            if self.type == "Ageup" and self.unit_name:
                bonuses = stats['bonuses'].get(self.unit_name, None)
                if bonuses:
                    self.hp_bonus = bonuses['hp_bonus']
                    self.attack_bonus = bonuses['attack_bonus']
                    self.melee_armor_bonus = bonuses['melee_armor_bonus']
                    self.ranged_armor_bonus = bonuses['ranged_armor_bonus']
                else:
                    raise ValueError(
                        f"No specific bonuses found for unit '{self.unit_name}' in upgrade '{self.upgrade_name}'. Please check if the unit is valid for this upgrade.")
            elif self.type == "Research":
                self.attack_bonus = stats['attack_bonus']
                self.hp_bonus = stats['hp_bonus']
                self.melee_armor_bonus = stats['melee_armor_bonus']
                self.ranged_armor_bonus = stats['ranged_armor_bonus']
            else:
                raise ValueError(f"Upgrade '{self.upgrade_name}' requires a unit name for Ageup type upgrades.")
        else:
            raise ValueError(
                f"Upgrade '{self.upgrade_name}' not found in stats file. Please verify the upgrade name in 'upgrade_stats.json'.")

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
