#!/usr/bin/env python3
"""Script standalone pour récupérer un fait aléatoire Wikipedia du jour."""
import aiohttp
import random
import asyncio
from datetime import date


async def get_wikipedia_fact(language: str = "fr") -> dict:
    """Récupère un fait aléatoire lié au jour courant depuis Wikipedia."""
    today = date.today()
    month = today.strftime("%m")
    day = today.strftime("%d")
    url = f"https://{language}.wikipedia.org/api/rest_v1/feed/onthisday/events/{month}/{day}"

    headers = {
        "User-Agent": "WikipediaFactScript/1.0 (Python/aiohttp; https://github.com/example)",
        "Accept": "application/json",
    }
    async with aiohttp.ClientSession() as session:
        async with session.get(url, headers=headers) as response:
            if response.status != 200:
                return {"error": f"Erreur HTTP {response.status}"}

            data = await response.json()
            events = data.get("events", [])

            if not events:
                return {"error": "Aucun événement trouvé."}

            event = random.choice(events)
            year = event.get("year", "Année inconnue")
            text = event.get("text", "Description indisponible")
            pages = event.get("pages", [])
            link = (
                pages[0].get("content_urls", {}).get("desktop", {}).get("page", "")
                if pages
                else None
            )

            return {
                "resume": f"En {year}: {text[:100]}...",
                "texte_complet": f"En {year}: {text}",
                "lien": link,
                "annee": year,
            }


async def main():
    import argparse

    parser = argparse.ArgumentParser(description="Fait aléatoire Wikipedia du jour")
    parser.add_argument(
        "--lang", "-l", default="fr", help="Langue (fr, en, es, etc.)"
    )
    args = parser.parse_args()

    result = await get_wikipedia_fact(args.lang)

    if "error" in result:
        print(f"Erreur: {result['error']}")
        return

    print(f"\n{result['resume']}\n")
    print(f"Texte complet: {result['texte_complet']}")
    if result["lien"]:
        print(f"Lien: {result['lien']}")


if __name__ == "__main__":
    asyncio.run(main())
