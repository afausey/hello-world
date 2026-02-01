#!/usr/bin/env python3
"""
ADV OU Knowledge Base Query Functions

Provides programmatic access to the Gen 3 OU knowledge base data.
"""

import json
import os
from pathlib import Path
from typing import Dict, List, Optional, Any

# Determine base path
BASE_DIR = Path(__file__).parent.parent
KNOWLEDGE_BASE_DIR = BASE_DIR / "knowledge_base"


def load_pokemon_data() -> Dict[str, Any]:
    """Load Pokemon sets and data from JSON."""
    path = KNOWLEDGE_BASE_DIR / "pokemon_sets.json"
    with open(path, 'r') as f:
        return json.load(f)


def load_metagame_data() -> Dict[str, Any]:
    """Load metagame overview data from JSON."""
    path = KNOWLEDGE_BASE_DIR / "metagame_overview.json"
    with open(path, 'r') as f:
        return json.load(f)


class KnowledgeBase:
    """Query interface for ADV OU knowledge base."""

    def __init__(self):
        self._pokemon_data = None
        self._metagame_data = None

    @property
    def pokemon_data(self) -> Dict[str, Any]:
        if self._pokemon_data is None:
            self._pokemon_data = load_pokemon_data()
        return self._pokemon_data

    @property
    def metagame_data(self) -> Dict[str, Any]:
        if self._metagame_data is None:
            self._metagame_data = load_metagame_data()
        return self._metagame_data

    # -------------------------
    # Pokemon Query Functions
    # -------------------------

    def get_pokemon(self, name: str) -> Optional[Dict[str, Any]]:
        """
        Get Pokemon data by name (case-insensitive).

        Args:
            name: Pokemon name (e.g., 'Tyranitar', 'tyranitar')

        Returns:
            Pokemon data dict or None if not found
        """
        name_lower = name.lower().replace(' ', '').replace('-', '')
        pokemon = self.pokemon_data.get('pokemon', {})

        for key, data in pokemon.items():
            if key.lower() == name_lower or data['name'].lower().replace(' ', '').replace('-', '') == name_lower:
                return data
        return None

    def get_pokemon_set(self, pokemon_name: str, set_name: str) -> Optional[Dict[str, Any]]:
        """
        Get a specific set for a Pokemon.

        Args:
            pokemon_name: Pokemon name
            set_name: Set name or key (e.g., 'dragon_dance', 'Dragon Dance')

        Returns:
            Set data dict or None if not found
        """
        pokemon = self.get_pokemon(pokemon_name)
        if not pokemon or 'sets' not in pokemon:
            return None

        set_name_lower = set_name.lower().replace(' ', '_').replace('-', '_')

        for key, set_data in pokemon['sets'].items():
            if key.lower() == set_name_lower or set_data['name'].lower() == set_name.lower():
                return set_data
        return None

    def list_pokemon(self, tier: Optional[str] = None) -> List[str]:
        """
        List all Pokemon names, optionally filtered by tier.

        Args:
            tier: Optional viability tier ('S', 'A', 'B')

        Returns:
            List of Pokemon names
        """
        pokemon = self.pokemon_data.get('pokemon', {})
        result = []

        for key, data in pokemon.items():
            if tier is None or data.get('viability') == tier:
                result.append(data['name'])

        return sorted(result)

    def list_sets(self, pokemon_name: str) -> List[str]:
        """
        List all available sets for a Pokemon.

        Args:
            pokemon_name: Pokemon name

        Returns:
            List of set names
        """
        pokemon = self.get_pokemon(pokemon_name)
        if not pokemon or 'sets' not in pokemon:
            return []

        return [s['name'] for s in pokemon['sets'].values()]

    def get_base_stats(self, pokemon_name: str) -> Optional[Dict[str, int]]:
        """
        Get base stats for a Pokemon.

        Args:
            pokemon_name: Pokemon name

        Returns:
            Dict with hp, atk, def, spa, spd, spe or None
        """
        pokemon = self.get_pokemon(pokemon_name)
        if pokemon:
            return pokemon.get('base_stats')
        return None

    def get_types(self, pokemon_name: str) -> Optional[List[str]]:
        """
        Get types for a Pokemon.

        Args:
            pokemon_name: Pokemon name

        Returns:
            List of type strings or None
        """
        pokemon = self.get_pokemon(pokemon_name)
        if pokemon:
            return pokemon.get('types')
        return None

    def get_checks_counters(self, pokemon_name: str) -> Optional[Dict[str, Any]]:
        """
        Get checks and counters for a Pokemon.

        Args:
            pokemon_name: Pokemon name

        Returns:
            Dict with hard_counters, soft_checks, notes or None
        """
        pokemon = self.get_pokemon(pokemon_name)
        if pokemon:
            return pokemon.get('checks_and_counters')
        return None

    def search_pokemon(self, query: str) -> List[Dict[str, Any]]:
        """
        Search Pokemon by name, type, or role.

        Args:
            query: Search string

        Returns:
            List of matching Pokemon data dicts
        """
        query_lower = query.lower()
        pokemon = self.pokemon_data.get('pokemon', {})
        results = []

        for key, data in pokemon.items():
            # Search in name
            if query_lower in data['name'].lower():
                results.append(data)
                continue

            # Search in types
            if any(query_lower in t.lower() for t in data.get('types', [])):
                results.append(data)
                continue

            # Search in role
            if query_lower in data.get('role', '').lower():
                results.append(data)
                continue

        return results

    # -------------------------
    # Metagame Query Functions
    # -------------------------

    def get_archetype(self, name: str) -> Optional[Dict[str, Any]]:
        """
        Get archetype data by name.

        Args:
            name: Archetype name or key (e.g., 'tss_balance', 'TSS Balance')

        Returns:
            Archetype data dict or None
        """
        archetypes = self.metagame_data.get('archetypes', {})
        name_lower = name.lower().replace(' ', '_').replace('-', '_')

        for key, data in archetypes.items():
            if key.lower() == name_lower or data['name'].lower() == name.lower():
                return data
        return None

    def list_archetypes(self) -> List[str]:
        """List all archetype names."""
        archetypes = self.metagame_data.get('archetypes', {})
        return [a['name'] for a in archetypes.values()]

    def get_core(self, name: str) -> Optional[Dict[str, Any]]:
        """
        Get core data by name.

        Args:
            name: Core name or key (e.g., 'skarmbliss', 'Skarmory + Blissey')

        Returns:
            Core data dict or None
        """
        cores = self.metagame_data.get('key_cores', {})
        name_lower = name.lower().replace(' ', '').replace('+', '')

        for key, data in cores.items():
            if key.lower() == name_lower:
                return data
            # Check if pokemon names match
            core_pokemon = ''.join(data['pokemon']).lower().replace(' ', '')
            if name_lower in core_pokemon:
                return data
        return None

    def list_cores(self) -> List[Dict[str, Any]]:
        """List all cores with their Pokemon."""
        cores = self.metagame_data.get('key_cores', {})
        return [{'name': k, 'pokemon': v['pokemon'], 'type': v['type']}
                for k, v in cores.items()]

    def get_clauses(self) -> Dict[str, str]:
        """Get all tier clauses."""
        return self.metagame_data.get('clauses', {})

    def get_gen3_mechanics(self) -> Dict[str, Any]:
        """Get unique Gen 3 mechanics."""
        return self.metagame_data.get('unique_gen3_mechanics', {})

    def get_viability_rankings(self) -> Dict[str, Any]:
        """Get viability rankings by tier."""
        return self.metagame_data.get('viability_rankings', {})

    def get_trapping_guide(self) -> Dict[str, Any]:
        """Get trapping guide for Dugtrio and Magneton."""
        return self.metagame_data.get('trapping_guide', {})

    # -------------------------
    # Utility Functions
    # -------------------------

    def format_set(self, pokemon_name: str, set_name: str) -> str:
        """
        Format a set for display (Pokemon Showdown format).

        Args:
            pokemon_name: Pokemon name
            set_name: Set name

        Returns:
            Formatted set string
        """
        pokemon = self.get_pokemon(pokemon_name)
        set_data = self.get_pokemon_set(pokemon_name, set_name)

        if not pokemon or not set_data:
            return f"Set not found: {pokemon_name} - {set_name}"

        lines = [
            f"{pokemon['name']} @ {set_data['item']}",
            f"Ability: {pokemon.get('ability', 'Unknown')}",
            f"EVs: {set_data['evs']}",
            f"{set_data['nature']} Nature",
        ]

        for move in set_data['moves']:
            lines.append(f"- {move}")

        return '\n'.join(lines)

    def export_set(self, pokemon_name: str, set_name: str) -> str:
        """Alias for format_set - exports in Showdown format."""
        return self.format_set(pokemon_name, set_name)


# Singleton instance for convenience
_kb = None

def get_kb() -> KnowledgeBase:
    """Get singleton KnowledgeBase instance."""
    global _kb
    if _kb is None:
        _kb = KnowledgeBase()
    return _kb


# Convenience functions using singleton
def pokemon(name: str) -> Optional[Dict[str, Any]]:
    """Get Pokemon data by name."""
    return get_kb().get_pokemon(name)


def pokemon_set(pokemon_name: str, set_name: str) -> Optional[Dict[str, Any]]:
    """Get a specific set for a Pokemon."""
    return get_kb().get_pokemon_set(pokemon_name, set_name)


def stats(pokemon_name: str) -> Optional[Dict[str, int]]:
    """Get base stats for a Pokemon."""
    return get_kb().get_base_stats(pokemon_name)


def types(pokemon_name: str) -> Optional[List[str]]:
    """Get types for a Pokemon."""
    return get_kb().get_types(pokemon_name)


def checks(pokemon_name: str) -> Optional[Dict[str, Any]]:
    """Get checks and counters for a Pokemon."""
    return get_kb().get_checks_counters(pokemon_name)


def archetype(name: str) -> Optional[Dict[str, Any]]:
    """Get archetype data by name."""
    return get_kb().get_archetype(name)


def core(name: str) -> Optional[Dict[str, Any]]:
    """Get core data by name."""
    return get_kb().get_core(name)


def showdown_set(pokemon_name: str, set_name: str) -> str:
    """Export set in Pokemon Showdown format."""
    return get_kb().format_set(pokemon_name, set_name)


# CLI interface
if __name__ == '__main__':
    import sys

    kb = KnowledgeBase()

    if len(sys.argv) < 2:
        print("ADV OU Knowledge Base")
        print("=" * 40)
        print("\nUsage:")
        print("  python knowledge_base.py pokemon <name>")
        print("  python knowledge_base.py set <pokemon> <set_name>")
        print("  python knowledge_base.py list [tier]")
        print("  python knowledge_base.py archetypes")
        print("  python knowledge_base.py cores")
        print("  python knowledge_base.py export <pokemon> <set_name>")
        print("\nExamples:")
        print("  python knowledge_base.py pokemon tyranitar")
        print("  python knowledge_base.py set tyranitar dragon_dance")
        print("  python knowledge_base.py list S")
        print("  python knowledge_base.py export salamence mixed")
        sys.exit(0)

    cmd = sys.argv[1].lower()

    if cmd == 'pokemon' and len(sys.argv) >= 3:
        name = ' '.join(sys.argv[2:])
        data = kb.get_pokemon(name)
        if data:
            print(f"\n{data['name']} ({'/'.join(data['types'])})")
            print(f"Viability: {data['viability']} Tier")
            print(f"Role: {data['role']}")
            print(f"\nBase Stats: HP {data['base_stats']['hp']} / Atk {data['base_stats']['atk']} / "
                  f"Def {data['base_stats']['def']} / SpA {data['base_stats']['spa']} / "
                  f"SpD {data['base_stats']['spd']} / Spe {data['base_stats']['spe']}")
            print(f"\nSets: {', '.join(kb.list_sets(name))}")
        else:
            print(f"Pokemon not found: {name}")

    elif cmd == 'set' and len(sys.argv) >= 4:
        pokemon_name = sys.argv[2]
        set_name = ' '.join(sys.argv[3:])
        set_data = kb.get_pokemon_set(pokemon_name, set_name)
        if set_data:
            print(f"\n{set_data['name']}")
            print(f"Item: {set_data['item']}")
            print(f"Nature: {set_data['nature']}")
            print(f"EVs: {set_data['evs']}")
            print(f"Moves: {', '.join(set_data['moves'])}")
            print(f"\n{set_data['description']}")
            if set_data.get('usage_tips'):
                print(f"\nTips: {set_data['usage_tips']}")
        else:
            print(f"Set not found: {pokemon_name} - {set_name}")

    elif cmd == 'list':
        tier = sys.argv[2].upper() if len(sys.argv) >= 3 else None
        pokemon_list = kb.list_pokemon(tier)
        tier_str = f" ({tier} Tier)" if tier else ""
        print(f"\nPokemon{tier_str}: {len(pokemon_list)}")
        print(', '.join(pokemon_list))

    elif cmd == 'archetypes':
        print("\nTeam Archetypes:")
        for name in kb.list_archetypes():
            arch = kb.get_archetype(name)
            print(f"\n  {name}")
            print(f"    {arch['description'][:80]}...")

    elif cmd == 'cores':
        print("\nKey Cores:")
        for core_info in kb.list_cores():
            print(f"  {' + '.join(core_info['pokemon'])} ({core_info['type']})")

    elif cmd == 'export' and len(sys.argv) >= 4:
        pokemon_name = sys.argv[2]
        set_name = ' '.join(sys.argv[3:])
        print(kb.format_set(pokemon_name, set_name))

    else:
        print("Invalid command. Run without arguments for help.")
