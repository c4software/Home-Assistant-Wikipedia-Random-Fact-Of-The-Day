#!/usr/bin/env python3
"""Script standalone pour récupérer un fait aléatoire Wikipedia du jour."""

import sys
from pathlib import Path

# Ajouter le répertoire parent au chemin pour importer wikipedia_api
sys.path.insert(0, str(Path(__file__).parent.parent))

import asyncio
from wikipedia_api import get_wikipedia_fact


async def main():
    import argparse

    parser = argparse.ArgumentParser(description="Fait aléatoire Wikipedia du jour")
    parser.add_argument(
        "--lang", "-l", default="fr", help="Langue (fr, en, es, etc.)"
    )
    args = parser.parse_args()

    result = await get_wikipedia_fact(args.lang)

    if "error" in result:
        print(f"Erreur : {result['error']}")
        return

    print(f"\n{result['resume']}\n")
    print(f"Texte complet : {result['texte_complet']}")
    if result.get("lien"):
        print(f"Lien : {result['lien']}")


if __name__ == "__main__":
    asyncio.run(main())
