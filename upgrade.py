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
        self.ranged_attack_bonus = 0
        self.melee_attack_bonus = 0
        self.melee_armor_bonus = 0
        self.ranged_armor_bonus = 0
        self.cost = 0
        self.type = None  # Add the type attribute here
        self.prerequisite = None  # Prerequisite upgrade

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
            self.type = stats['type']
            self.prerequisite = stats.get('prerequisites')  # Load prerequisite if available

            if self.type == "UnitUpgrade":
                stats= stats['bonuses'][self.unit_name]
                self.ranged_attack_bonus = stats['ranged_attack_bonus']
                self.melee_attack_bonus = stats['melee_attack_bonus']
                self.hp_bonus = stats['hp_bonus']
                self.melee_armor_bonus = stats['melee_armor_bonus']
                self.ranged_armor_bonus = stats['ranged_armor_bonus']
            elif self.type == "Research":
                self.ranged_attack_bonus = stats['ranged_attack_bonus']
                self.melee_attack_bonus = stats['melee_attack_bonus']
                self.hp_bonus = stats['hp_bonus']
                self.melee_armor_bonus = stats['melee_armor_bonus']
                self.ranged_armor_bonus = stats['ranged_armor_bonus']
        else:
            raise ValueError(
                f"Upgrade '{self.upgrade_name}' not found in stats file. Please verify the upgrade name in 'upgrade_stats.json'.")

    def add_upgrade(self, other_upgrade):
        """
        Combines the effects of another upgrade with this one, including prerequisites.

        Parameters:
        other_upgrade (Upgrade): The upgrade to be combined with this one.
        """
        self.ranged_attack_bonus += other_upgrade.ranged_attack_bonus
        self. melee_attack_bonus += other_upgrade.melee_attack_bonus
        self.hp_bonus += other_upgrade.hp_bonus
        self.melee_armor_bonus += other_upgrade.melee_armor_bonus
        self.ranged_armor_bonus += other_upgrade.ranged_armor_bonus
        self.cost += other_upgrade.cost

        # Add prerequisite if the other upgrade has one
        if other_upgrade.has_prerequisite() and other_upgrade.prerequisite not in self.get_prerequisites():
            if self.prerequisite is None:
                self.prerequisite = []
            if isinstance(self.prerequisite, str):
                self.prerequisite = [self.prerequisite]
            self.prerequisite.append(other_upgrade.prerequisite)

    def has_prerequisite(self):
        """
        Checks if the upgrade has a prerequisite.

        Returns:
        bool: True if the upgrade has a prerequisite, False otherwise.
        """
        return self.prerequisite is not None

    def get_prerequisites(self):
        """
        Returns the names of the prerequisite upgrades, if any.

        Returns:
        list: A list of prerequisite upgrade names, or an empty list if there are no prerequisites.
        """
        if self.prerequisite is None:
            return []
        if isinstance(self.prerequisite, str):
            return [self.prerequisite]
        return self.prerequisite