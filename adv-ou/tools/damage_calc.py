#!/usr/bin/env python3
"""
ADV OU Damage Calculator

Implements the Generation 3 damage formula with all relevant modifiers.
Can be used standalone via CLI or imported as a module.
"""

import json
import math
import random
from dataclasses import dataclass, field
from enum import Enum
from pathlib import Path
from typing import Dict, List, Optional, Tuple, Any

# -------------------------
# Type Chart (Gen 3)
# -------------------------

TYPE_CHART = {
    'Normal':   {'Rock': 0.5, 'Ghost': 0, 'Steel': 0.5},
    'Fire':     {'Fire': 0.5, 'Water': 0.5, 'Grass': 2, 'Ice': 2, 'Bug': 2, 'Rock': 0.5, 'Dragon': 0.5, 'Steel': 2},
    'Water':    {'Fire': 2, 'Water': 0.5, 'Grass': 0.5, 'Ground': 2, 'Rock': 2, 'Dragon': 0.5},
    'Electric': {'Water': 2, 'Electric': 0.5, 'Grass': 0.5, 'Ground': 0, 'Flying': 2, 'Dragon': 0.5},
    'Grass':    {'Fire': 0.5, 'Water': 2, 'Grass': 0.5, 'Poison': 0.5, 'Ground': 2, 'Flying': 0.5, 'Bug': 0.5, 'Rock': 2, 'Dragon': 0.5, 'Steel': 0.5},
    'Ice':      {'Fire': 0.5, 'Water': 0.5, 'Grass': 2, 'Ice': 0.5, 'Ground': 2, 'Flying': 2, 'Dragon': 2, 'Steel': 0.5},
    'Fighting': {'Normal': 2, 'Ice': 2, 'Poison': 0.5, 'Flying': 0.5, 'Psychic': 0.5, 'Bug': 0.5, 'Rock': 2, 'Ghost': 0, 'Dark': 2, 'Steel': 2},
    'Poison':   {'Grass': 2, 'Poison': 0.5, 'Ground': 0.5, 'Rock': 0.5, 'Ghost': 0.5, 'Steel': 0},
    'Ground':   {'Fire': 2, 'Electric': 2, 'Grass': 0.5, 'Poison': 2, 'Flying': 0, 'Bug': 0.5, 'Rock': 2, 'Steel': 2},
    'Flying':   {'Electric': 0.5, 'Grass': 2, 'Fighting': 2, 'Bug': 2, 'Rock': 0.5, 'Steel': 0.5},
    'Psychic':  {'Fighting': 2, 'Poison': 2, 'Psychic': 0.5, 'Dark': 0, 'Steel': 0.5},
    'Bug':      {'Fire': 0.5, 'Grass': 2, 'Fighting': 0.5, 'Poison': 0.5, 'Flying': 0.5, 'Psychic': 2, 'Ghost': 0.5, 'Dark': 2, 'Steel': 0.5},
    'Rock':     {'Fire': 2, 'Ice': 2, 'Fighting': 0.5, 'Ground': 0.5, 'Flying': 2, 'Bug': 2, 'Steel': 0.5},
    'Ghost':    {'Normal': 0, 'Psychic': 2, 'Ghost': 2, 'Dark': 0.5, 'Steel': 0.5},
    'Dragon':   {'Dragon': 2, 'Steel': 0.5},
    'Dark':     {'Fighting': 0.5, 'Psychic': 2, 'Ghost': 2, 'Dark': 0.5, 'Steel': 0.5},
    'Steel':    {'Fire': 0.5, 'Water': 0.5, 'Electric': 0.5, 'Ice': 2, 'Rock': 2, 'Steel': 0.5},
}

# -------------------------
# Move Data (Common ADV OU moves)
# -------------------------

MOVES = {
    # Physical moves
    'Earthquake': {'type': 'Ground', 'power': 100, 'category': 'Physical', 'accuracy': 100},
    'Rock Slide': {'type': 'Rock', 'power': 75, 'category': 'Physical', 'accuracy': 90},
    'Meteor Mash': {'type': 'Steel', 'power': 100, 'category': 'Physical', 'accuracy': 85},
    'Focus Punch': {'type': 'Fighting', 'power': 150, 'category': 'Physical', 'accuracy': 100},
    'Brick Break': {'type': 'Fighting', 'power': 75, 'category': 'Physical', 'accuracy': 100},
    'Hidden Power Flying': {'type': 'Flying', 'power': 70, 'category': 'Physical', 'accuracy': 100},
    'Hidden Power Bug': {'type': 'Bug', 'power': 70, 'category': 'Physical', 'accuracy': 100},
    'Aerial Ace': {'type': 'Flying', 'power': 60, 'category': 'Physical', 'accuracy': 100, 'never_miss': True},
    'Double-Edge': {'type': 'Normal', 'power': 120, 'category': 'Physical', 'accuracy': 100, 'recoil': 1/3},
    'Return': {'type': 'Normal', 'power': 102, 'category': 'Physical', 'accuracy': 100},
    'Body Slam': {'type': 'Normal', 'power': 85, 'category': 'Physical', 'accuracy': 100},
    'Sludge Bomb': {'type': 'Poison', 'power': 90, 'category': 'Physical', 'accuracy': 100},
    'Shadow Ball': {'type': 'Ghost', 'power': 80, 'category': 'Physical', 'accuracy': 100},  # Physical in Gen 3!
    'Drill Peck': {'type': 'Flying', 'power': 80, 'category': 'Physical', 'accuracy': 100},
    'Megahorn': {'type': 'Bug', 'power': 120, 'category': 'Physical', 'accuracy': 85},
    'Cross Chop': {'type': 'Fighting', 'power': 100, 'category': 'Physical', 'accuracy': 80, 'high_crit': True},
    'Hi Jump Kick': {'type': 'Fighting', 'power': 85, 'category': 'Physical', 'accuracy': 90},
    'Dragon Claw': {'type': 'Dragon', 'power': 80, 'category': 'Physical', 'accuracy': 100},
    'Iron Tail': {'type': 'Steel', 'power': 100, 'category': 'Physical', 'accuracy': 75},
    'Explosion': {'type': 'Normal', 'power': 250, 'category': 'Physical', 'accuracy': 100, 'explosion': True},
    'Self-Destruct': {'type': 'Normal', 'power': 200, 'category': 'Physical', 'accuracy': 100, 'explosion': True},
    'Crunch': {'type': 'Dark', 'power': 80, 'category': 'Physical', 'accuracy': 100},

    # Special moves
    'Thunderbolt': {'type': 'Electric', 'power': 95, 'category': 'Special', 'accuracy': 100},
    'Thunder': {'type': 'Electric', 'power': 120, 'category': 'Special', 'accuracy': 70},
    'Ice Beam': {'type': 'Ice', 'power': 95, 'category': 'Special', 'accuracy': 100},
    'Blizzard': {'type': 'Ice', 'power': 120, 'category': 'Special', 'accuracy': 70},
    'Flamethrower': {'type': 'Fire', 'power': 95, 'category': 'Special', 'accuracy': 100},
    'Fire Blast': {'type': 'Fire', 'power': 120, 'category': 'Special', 'accuracy': 85},
    'Hydro Pump': {'type': 'Water', 'power': 120, 'category': 'Special', 'accuracy': 80},
    'Surf': {'type': 'Water', 'power': 95, 'category': 'Special', 'accuracy': 100},
    'Psychic': {'type': 'Psychic', 'power': 90, 'category': 'Special', 'accuracy': 100},
    'Giga Drain': {'type': 'Grass', 'power': 60, 'category': 'Special', 'accuracy': 100},
    'Hidden Power Grass': {'type': 'Grass', 'power': 70, 'category': 'Special', 'accuracy': 100},
    'Hidden Power Fire': {'type': 'Fire', 'power': 70, 'category': 'Special', 'accuracy': 100},
    'Hidden Power Ice': {'type': 'Ice', 'power': 70, 'category': 'Special', 'accuracy': 100},
    'Ice Punch': {'type': 'Ice', 'power': 75, 'category': 'Special', 'accuracy': 100},  # Special in Gen 3!
    'Fire Punch': {'type': 'Fire', 'power': 75, 'category': 'Special', 'accuracy': 100},  # Special in Gen 3!
    'Thunder Punch': {'type': 'Thunder', 'power': 75, 'category': 'Special', 'accuracy': 100},  # Special in Gen 3!
    'Seismic Toss': {'type': 'Fighting', 'power': 0, 'category': 'Special', 'accuracy': 100, 'fixed_damage': 100},

    # Status (for completeness)
    'Toxic': {'type': 'Poison', 'power': 0, 'category': 'Status', 'accuracy': 85},
    'Will-O-Wisp': {'type': 'Fire', 'power': 0, 'category': 'Status', 'accuracy': 75},
    'Thunder Wave': {'type': 'Electric', 'power': 0, 'category': 'Status', 'accuracy': 100},
    'Spikes': {'type': 'Ground', 'power': 0, 'category': 'Status', 'accuracy': 100},
}

# Nature modifiers
NATURES = {
    'Hardy': (None, None), 'Lonely': ('atk', 'def'), 'Brave': ('atk', 'spe'),
    'Adamant': ('atk', 'spa'), 'Naughty': ('atk', 'spd'),
    'Bold': ('def', 'atk'), 'Docile': (None, None), 'Relaxed': ('def', 'spe'),
    'Impish': ('def', 'spa'), 'Lax': ('def', 'spd'),
    'Timid': ('spe', 'atk'), 'Hasty': ('spe', 'def'), 'Serious': (None, None),
    'Jolly': ('spe', 'spa'), 'Naive': ('spe', 'spd'),
    'Modest': ('spa', 'atk'), 'Mild': ('spa', 'def'), 'Quiet': ('spa', 'spe'),
    'Bashful': (None, None), 'Rash': ('spa', 'spd'),
    'Calm': ('spd', 'atk'), 'Gentle': ('spd', 'def'), 'Sassy': ('spd', 'spe'),
    'Careful': ('spd', 'spa'), 'Quirky': (None, None),
}


class Weather(Enum):
    NONE = 'none'
    RAIN = 'rain'
    SUN = 'sun'
    SAND = 'sand'


@dataclass
class Pokemon:
    """Represents a Pokemon with stats, moves, and modifiers."""
    name: str
    types: List[str]
    base_stats: Dict[str, int]
    level: int = 100
    evs: Dict[str, int] = field(default_factory=lambda: {'hp': 0, 'atk': 0, 'def': 0, 'spa': 0, 'spd': 0, 'spe': 0})
    ivs: Dict[str, int] = field(default_factory=lambda: {'hp': 31, 'atk': 31, 'def': 31, 'spa': 31, 'spd': 31, 'spe': 31})
    nature: str = 'Hardy'
    item: str = ''
    ability: str = ''
    status: str = ''  # 'burn', 'paralysis', etc.
    stat_stages: Dict[str, int] = field(default_factory=lambda: {'atk': 0, 'def': 0, 'spa': 0, 'spd': 0, 'spe': 0})
    current_hp_percent: float = 100.0

    def calc_stat(self, stat: str) -> int:
        """Calculate final stat value."""
        base = self.base_stats[stat]
        ev = self.evs.get(stat, 0)
        iv = self.ivs.get(stat, 31)
        level = self.level

        if stat == 'hp':
            # HP formula
            return ((2 * base + iv + ev // 4) * level // 100) + level + 10

        # Other stats
        stat_value = ((2 * base + iv + ev // 4) * level // 100) + 5

        # Apply nature modifier
        boost, drop = NATURES.get(self.nature, (None, None))
        if boost == stat:
            stat_value = int(stat_value * 1.1)
        elif drop == stat:
            stat_value = int(stat_value * 0.9)

        return stat_value

    def get_stat_with_stages(self, stat: str, ignore_stages: bool = False) -> int:
        """Get stat with stage modifiers applied."""
        base_stat = self.calc_stat(stat)

        if ignore_stages:
            return base_stat

        stage = self.stat_stages.get(stat, 0)
        if stage >= 0:
            multiplier = (2 + stage) / 2
        else:
            multiplier = 2 / (2 - stage)

        return int(base_stat * multiplier)

    @property
    def max_hp(self) -> int:
        return self.calc_stat('hp')

    @property
    def current_hp(self) -> int:
        return int(self.max_hp * self.current_hp_percent / 100)


@dataclass
class DamageResult:
    """Result of a damage calculation."""
    min_damage: int
    max_damage: int
    min_percent: float
    max_percent: float
    rolls: List[int]
    crit_min: int
    crit_max: int
    crit_min_percent: float
    crit_max_percent: float
    ko_chance: str  # "Guaranteed OHKO", "50% chance to OHKO", etc.
    n_hit_ko: int  # Number of hits to KO (1 = OHKO, 2 = 2HKO, etc.)
    description: str


def get_type_effectiveness(move_type: str, defender_types: List[str]) -> float:
    """Calculate type effectiveness multiplier."""
    multiplier = 1.0
    chart = TYPE_CHART.get(move_type, {})

    for def_type in defender_types:
        multiplier *= chart.get(def_type, 1.0)

    return multiplier


def calculate_damage(
    attacker: Pokemon,
    defender: Pokemon,
    move_name: str,
    weather: Weather = Weather.NONE,
    is_crit: bool = False,
    reflect: bool = False,
    light_screen: bool = False,
    helping_hand: bool = False,
) -> DamageResult:
    """
    Calculate damage using the Gen 3 damage formula.

    Gen 3 Formula:
    Damage = ((((2 * Level / 5 + 2) * Power * A / D) / 50) + 2) * Modifier

    Where Modifier = STAB * Type * Critical * Random * Other
    """
    move = MOVES.get(move_name)
    if not move:
        # Try to find a similar move
        for m_name, m_data in MOVES.items():
            if move_name.lower() in m_name.lower():
                move = m_data
                break
        if not move:
            return DamageResult(0, 0, 0, 0, [], 0, 0, 0, 0, "Move not found", 0, f"Move '{move_name}' not found in database")

    # Fixed damage moves
    if move.get('fixed_damage'):
        dmg = move['fixed_damage']
        pct = dmg / defender.max_hp * 100
        return DamageResult(dmg, dmg, pct, pct, [dmg], dmg, dmg, pct, pct,
                           "Always deals 100 damage", 1 if dmg >= defender.current_hp else math.ceil(defender.current_hp / dmg),
                           f"{move_name}: {dmg} damage ({pct:.1f}%)")

    # Status moves
    if move['category'] == 'Status':
        return DamageResult(0, 0, 0, 0, [], 0, 0, 0, 0, "Status move", 0, f"{move_name} is a status move")

    power = move['power']
    move_type = move['type']
    is_physical = move['category'] == 'Physical'

    # Get attack and defense stats
    if is_physical:
        atk_stat = 'atk'
        def_stat = 'def'
        screen = reflect
    else:
        atk_stat = 'spa'
        def_stat = 'spd'
        screen = light_screen

    # Critical hits ignore stat stages in Gen 3 (both positive AND negative)
    attack = attacker.get_stat_with_stages(atk_stat, ignore_stages=is_crit)
    defense = defender.get_stat_with_stages(def_stat, ignore_stages=is_crit)

    # Gen 3 unique: Explosion/Self-Destruct halves defense
    if move.get('explosion'):
        defense = max(1, defense // 2)

    # Weather effects on Rock-type SpD (Sandstorm)
    if weather == Weather.SAND and 'Rock' in defender.types and not is_physical:
        defense = int(defense * 1.5)

    # Apply burn to physical attacks (halves attack)
    if attacker.status == 'burn' and is_physical and attacker.ability != 'Guts':
        attack = attack // 2

    # Item modifiers
    if attacker.item == 'Choice Band' and is_physical:
        attack = int(attack * 1.5)
    elif attacker.item == 'Soul Dew' and attacker.name in ['Latios', 'Latias'] and not is_physical:
        attack = int(attack * 1.5)

    # Ability modifiers
    if attacker.ability == 'Huge Power' or attacker.ability == 'Pure Power':
        if is_physical:
            attack = attack * 2

    # Thick Fat (halves Fire/Ice damage)
    if defender.ability == 'Thick Fat' and move_type in ['Fire', 'Ice']:
        power = power // 2

    # Flash Fire (immunity + boost)
    if defender.ability == 'Flash Fire' and move_type == 'Fire':
        return DamageResult(0, 0, 0, 0, [], 0, 0, 0, 0, "Immune (Flash Fire)", 0,
                           f"{defender.name}'s Flash Fire absorbs {move_name}")

    # Levitate
    if defender.ability == 'Levitate' and move_type == 'Ground':
        return DamageResult(0, 0, 0, 0, [], 0, 0, 0, 0, "Immune (Levitate)", 0,
                           f"{defender.name}'s Levitate makes it immune to {move_name}")

    # Water Absorb / Volt Absorb
    if defender.ability == 'Water Absorb' and move_type == 'Water':
        return DamageResult(0, 0, 0, 0, [], 0, 0, 0, 0, "Immune (Water Absorb)", 0,
                           f"{defender.name}'s Water Absorb absorbs {move_name}")
    if defender.ability == 'Volt Absorb' and move_type == 'Electric':
        return DamageResult(0, 0, 0, 0, [], 0, 0, 0, 0, "Immune (Volt Absorb)", 0,
                           f"{defender.name}'s Volt Absorb absorbs {move_name}")

    # Calculate base damage
    level = attacker.level

    # Base damage formula
    base_damage = ((2 * level // 5 + 2) * power * attack // defense) // 50 + 2

    # Screen modifier (applied before other modifiers in Gen 3)
    if screen and not is_crit:
        base_damage = base_damage // 2

    # Weather modifier
    weather_mod = 1.0
    if weather == Weather.RAIN:
        if move_type == 'Water':
            weather_mod = 1.5
        elif move_type == 'Fire':
            weather_mod = 0.5
    elif weather == Weather.SUN:
        if move_type == 'Fire':
            weather_mod = 1.5
        elif move_type == 'Water':
            weather_mod = 0.5

    # STAB
    stab = 1.5 if move_type in attacker.types else 1.0

    # Type effectiveness
    type_eff = get_type_effectiveness(move_type, defender.types)

    if type_eff == 0:
        return DamageResult(0, 0, 0, 0, [], 0, 0, 0, 0, "Immune", 0,
                           f"{defender.name} is immune to {move_name}")

    # Critical hit modifier (2x in Gen 3)
    crit_mod = 2.0 if is_crit else 1.0

    # Helping Hand
    helping_mod = 1.5 if helping_hand else 1.0

    # Calculate damage rolls (85% to 100%)
    rolls = []
    for r in range(85, 101):
        damage = int(base_damage * weather_mod * stab * type_eff * crit_mod * helping_mod * r / 100)
        damage = max(1, damage)  # Minimum 1 damage
        rolls.append(damage)

    min_damage = min(rolls)
    max_damage = max(rolls)

    # Calculate crit damage
    crit_rolls = []
    for r in range(85, 101):
        damage = int(base_damage * weather_mod * stab * type_eff * 2.0 * helping_mod * r / 100)
        damage = max(1, damage)
        crit_rolls.append(damage)

    crit_min = min(crit_rolls)
    crit_max = max(crit_rolls)

    # Calculate percentages
    defender_hp = defender.max_hp
    min_percent = min_damage / defender_hp * 100
    max_percent = max_damage / defender_hp * 100
    crit_min_percent = crit_min / defender_hp * 100
    crit_max_percent = crit_max / defender_hp * 100

    # Determine KO chance
    current_hp = defender.current_hp
    ko_rolls = sum(1 for d in rolls if d >= current_hp)
    ko_chance_pct = ko_rolls / len(rolls) * 100

    if ko_chance_pct == 100:
        ko_chance = "Guaranteed OHKO"
        n_hit_ko = 1
    elif ko_chance_pct > 0:
        ko_chance = f"{ko_chance_pct:.1f}% chance to OHKO"
        n_hit_ko = 1
    else:
        # Calculate n-hit KO
        avg_damage = sum(rolls) / len(rolls)
        n_hit_ko = math.ceil(defender_hp / avg_damage)

        if n_hit_ko == 2:
            # Check 2HKO
            two_hit_kos = sum(1 for d1 in rolls for d2 in rolls if d1 + d2 >= defender_hp)
            two_hit_pct = two_hit_kos / (len(rolls) ** 2) * 100
            if two_hit_pct == 100:
                ko_chance = "Guaranteed 2HKO"
            elif two_hit_pct > 0:
                ko_chance = f"{two_hit_pct:.1f}% chance to 2HKO"
            else:
                ko_chance = "3HKO or more"
        elif n_hit_ko == 3:
            ko_chance = "3HKO"
        else:
            ko_chance = f"{n_hit_ko}HKO"

    # Build description
    type_eff_str = ""
    if type_eff > 1:
        type_eff_str = " (super effective)"
    elif type_eff < 1:
        type_eff_str = " (not very effective)"

    description = (
        f"{attacker.name}'s {move_name} vs {defender.name}: "
        f"{min_damage}-{max_damage} ({min_percent:.1f}% - {max_percent:.1f}%){type_eff_str}\n"
        f"{ko_chance}"
    )

    return DamageResult(
        min_damage=min_damage,
        max_damage=max_damage,
        min_percent=min_percent,
        max_percent=max_percent,
        rolls=rolls,
        crit_min=crit_min,
        crit_max=crit_max,
        crit_min_percent=crit_min_percent,
        crit_max_percent=crit_max_percent,
        ko_chance=ko_chance,
        n_hit_ko=n_hit_ko,
        description=description
    )


def parse_evs(ev_string: str) -> Dict[str, int]:
    """Parse EV string like '252 HP / 252 Atk / 4 Spe' into dict."""
    evs = {'hp': 0, 'atk': 0, 'def': 0, 'spa': 0, 'spd': 0, 'spe': 0}
    stat_map = {
        'hp': 'hp', 'atk': 'atk', 'attack': 'atk',
        'def': 'def', 'defense': 'def',
        'spa': 'spa', 'spatk': 'spa', 'sp.atk': 'spa', 'special attack': 'spa', 'spatt': 'spa',
        'spd': 'spd', 'spdef': 'spd', 'sp.def': 'spd', 'special defense': 'spd',
        'spe': 'spe', 'speed': 'spe', 'spd': 'spd'
    }

    # Handle common SpD vs Spe confusion
    parts = ev_string.lower().replace('spd', 'SPDEF').replace('spe', 'SPE').split('/')
    for part in parts:
        part = part.strip().replace('SPDEF', 'spd').replace('SPE', 'spe')
        tokens = part.split()
        if len(tokens) >= 2:
            try:
                value = int(tokens[0])
                stat_name = tokens[1].lower().replace('.', '')
                if stat_name in stat_map:
                    evs[stat_map[stat_name]] = value
            except ValueError:
                continue

    return evs


def pokemon_from_kb(name: str, set_name: Optional[str] = None) -> Optional[Pokemon]:
    """Create a Pokemon instance from knowledge base data."""
    try:
        from knowledge_base import KnowledgeBase
        kb = KnowledgeBase()

        pokemon_data = kb.get_pokemon(name)
        if not pokemon_data:
            return None

        base_stats = pokemon_data['base_stats']

        # Default values
        evs = {'hp': 0, 'atk': 0, 'def': 0, 'spa': 0, 'spd': 0, 'spe': 0}
        nature = 'Hardy'
        item = ''
        ability = pokemon_data.get('ability', '')

        # Get set data if specified
        if set_name:
            set_data = kb.get_pokemon_set(name, set_name)
            if set_data:
                evs = parse_evs(set_data.get('evs', ''))
                nature = set_data.get('nature', 'Hardy').split('/')[0].strip()
                item = set_data.get('item', '')

        return Pokemon(
            name=pokemon_data['name'],
            types=pokemon_data['types'],
            base_stats=base_stats,
            evs=evs,
            nature=nature,
            item=item,
            ability=ability
        )

    except ImportError:
        return None


# CLI Interface
def main():
    import sys

    print("=" * 50)
    print("ADV OU Damage Calculator")
    print("=" * 50)

    if len(sys.argv) < 4:
        print("\nUsage:")
        print("  python damage_calc.py <attacker> <move> <defender> [options]")
        print("\nOptions:")
        print("  --atk-set <set>    Attacker's set name")
        print("  --def-set <set>    Defender's set name")
        print("  --weather <type>   rain, sun, sand, or none")
        print("  --crit             Calculate as critical hit")
        print("\nExamples:")
        print("  python damage_calc.py tyranitar earthquake skarmory")
        print("  python damage_calc.py tyranitar 'rock slide' zapdos --atk-set choice_band")
        print("  python damage_calc.py salamence 'hidden power flying' blissey --weather sand")
        return

    # Parse arguments
    attacker_name = sys.argv[1]
    move_name = sys.argv[2]
    defender_name = sys.argv[3]

    atk_set = None
    def_set = None
    weather = Weather.NONE
    is_crit = False

    i = 4
    while i < len(sys.argv):
        arg = sys.argv[i]
        if arg == '--atk-set' and i + 1 < len(sys.argv):
            atk_set = sys.argv[i + 1]
            i += 2
        elif arg == '--def-set' and i + 1 < len(sys.argv):
            def_set = sys.argv[i + 1]
            i += 2
        elif arg == '--weather' and i + 1 < len(sys.argv):
            w = sys.argv[i + 1].lower()
            weather = {'rain': Weather.RAIN, 'sun': Weather.SUN, 'sand': Weather.SAND}.get(w, Weather.NONE)
            i += 2
        elif arg == '--crit':
            is_crit = True
            i += 1
        else:
            i += 1

    # Create Pokemon
    attacker = pokemon_from_kb(attacker_name, atk_set)
    defender = pokemon_from_kb(defender_name, def_set)

    if not attacker:
        print(f"Error: Could not find attacker '{attacker_name}'")
        return
    if not defender:
        print(f"Error: Could not find defender '{defender_name}'")
        return

    # Calculate damage
    result = calculate_damage(attacker, defender, move_name, weather=weather, is_crit=is_crit)

    # Display results
    print(f"\n{result.description}")
    print(f"\nDamage rolls: {result.min_damage} - {result.max_damage}")
    print(f"Percentage:   {result.min_percent:.1f}% - {result.max_percent:.1f}%")
    print(f"\nCrit damage:  {result.crit_min} - {result.crit_max} ({result.crit_min_percent:.1f}% - {result.crit_max_percent:.1f}%)")

    if weather != Weather.NONE:
        print(f"\nWeather: {weather.value}")


if __name__ == '__main__':
    main()
