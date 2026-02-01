#!/usr/bin/env python3
"""
Simple HTTP server for ADV OU Knowledge Base and Damage Calculator.

Run with: python server.py
Then open http://localhost:8080 in your browser.
"""

import http.server
import socketserver
import json
import urllib.parse
import os
import sys
from pathlib import Path

# Add tools directory to path
SCRIPT_DIR = Path(__file__).parent
sys.path.insert(0, str(SCRIPT_DIR / 'tools'))

PORT = 8080


class ADVOUHandler(http.server.SimpleHTTPRequestHandler):
    """Custom handler that serves static files and provides API endpoints."""

    def __init__(self, *args, **kwargs):
        # Change to the adv-ou directory
        super().__init__(*args, directory=str(SCRIPT_DIR), **kwargs)

    def do_GET(self):
        """Handle GET requests."""
        parsed = urllib.parse.urlparse(self.path)

        # API endpoints
        if parsed.path == '/api/calc':
            self.handle_calc_request(parsed.query)
        elif parsed.path == '/api/pokemon':
            self.handle_pokemon_request(parsed.query)
        elif parsed.path == '/api/pokemon/list':
            self.handle_pokemon_list_request()
        else:
            # Serve static files
            super().do_GET()

    def handle_calc_request(self, query_string):
        """Handle damage calculation API request."""
        try:
            from damage_calc import pokemon_from_kb, calculate_damage, Weather

            params = urllib.parse.parse_qs(query_string)

            attacker_name = params.get('attacker', [''])[0]
            attacker_set = params.get('attacker_set', [None])[0]
            defender_name = params.get('defender', [''])[0]
            defender_set = params.get('defender_set', [None])[0]
            move_name = params.get('move', [''])[0]
            weather_str = params.get('weather', ['none'])[0].lower()

            weather_map = {'rain': Weather.RAIN, 'sun': Weather.SUN, 'sand': Weather.SAND}
            weather = weather_map.get(weather_str, Weather.NONE)

            attacker = pokemon_from_kb(attacker_name, attacker_set)
            defender = pokemon_from_kb(defender_name, defender_set)

            if not attacker:
                self.send_json_error(f"Attacker '{attacker_name}' not found")
                return

            if not defender:
                self.send_json_error(f"Defender '{defender_name}' not found")
                return

            result = calculate_damage(attacker, defender, move_name, weather=weather)

            response = {
                'success': True,
                'attacker': {
                    'name': attacker.name,
                    'types': attacker.types,
                    'set': attacker_set,
                    'item': attacker.item,
                    'nature': attacker.nature,
                    'stats': {
                        'hp': attacker.calc_stat('hp'),
                        'atk': attacker.calc_stat('atk'),
                        'def': attacker.calc_stat('def'),
                        'spa': attacker.calc_stat('spa'),
                        'spd': attacker.calc_stat('spd'),
                        'spe': attacker.calc_stat('spe'),
                    }
                },
                'defender': {
                    'name': defender.name,
                    'types': defender.types,
                    'set': defender_set,
                    'hp': defender.max_hp,
                },
                'move': move_name,
                'weather': weather_str,
                'result': {
                    'min_damage': result.min_damage,
                    'max_damage': result.max_damage,
                    'min_percent': round(result.min_percent, 1),
                    'max_percent': round(result.max_percent, 1),
                    'ko_chance': result.ko_chance,
                    'n_hit_ko': result.n_hit_ko,
                    'crit_min': result.crit_min,
                    'crit_max': result.crit_max,
                    'crit_min_percent': round(result.crit_min_percent, 1),
                    'crit_max_percent': round(result.crit_max_percent, 1),
                    'description': result.description,
                }
            }

            self.send_json_response(response)

        except Exception as e:
            self.send_json_error(str(e))

    def handle_pokemon_request(self, query_string):
        """Handle Pokemon data API request."""
        try:
            from knowledge_base import KnowledgeBase
            kb = KnowledgeBase()

            params = urllib.parse.parse_qs(query_string)
            name = params.get('name', [''])[0]

            pokemon = kb.get_pokemon(name)
            if pokemon:
                self.send_json_response({'success': True, 'pokemon': pokemon})
            else:
                self.send_json_error(f"Pokemon '{name}' not found")

        except Exception as e:
            self.send_json_error(str(e))

    def handle_pokemon_list_request(self):
        """Handle Pokemon list API request."""
        try:
            from knowledge_base import KnowledgeBase
            kb = KnowledgeBase()

            pokemon_list = []
            for tier in ['S', 'A', 'B']:
                for name in kb.list_pokemon(tier):
                    pokemon = kb.get_pokemon(name)
                    if pokemon:
                        pokemon_list.append({
                            'name': pokemon['name'],
                            'types': pokemon['types'],
                            'viability': pokemon['viability'],
                            'sets': list(pokemon.get('sets', {}).keys())
                        })

            self.send_json_response({'success': True, 'pokemon': pokemon_list})

        except Exception as e:
            self.send_json_error(str(e))

    def send_json_response(self, data):
        """Send JSON response."""
        self.send_response(200)
        self.send_header('Content-Type', 'application/json')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.end_headers()
        self.wfile.write(json.dumps(data).encode())

    def send_json_error(self, message):
        """Send JSON error response."""
        self.send_response(400)
        self.send_header('Content-Type', 'application/json')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.end_headers()
        self.wfile.write(json.dumps({'success': False, 'error': message}).encode())

    def log_message(self, format, *args):
        """Custom log format."""
        print(f"[{self.log_date_time_string()}] {args[0]}")


def main():
    os.chdir(SCRIPT_DIR)

    with socketserver.TCPServer(("", PORT), ADVOUHandler) as httpd:
        print(f"=" * 50)
        print(f"ADV OU Knowledge Base Server")
        print(f"=" * 50)
        print(f"\nServer running at http://localhost:{PORT}")
        print(f"Open this URL in your browser to view the knowledge base.")
        print(f"\nAPI Endpoints:")
        print(f"  /api/pokemon/list - List all Pokemon")
        print(f"  /api/pokemon?name=tyranitar - Get Pokemon data")
        print(f"  /api/calc?attacker=tyranitar&move=earthquake&defender=skarmory - Calculate damage")
        print(f"\nPress Ctrl+C to stop the server.")
        print()

        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print("\nShutting down server...")


if __name__ == '__main__':
    main()
