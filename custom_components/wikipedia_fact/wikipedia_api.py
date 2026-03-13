"""Module utilitaire pour l'API Wikipedia."""

import aiohttp
import random
from datetime import date


def validate_language(language: str) -> None:
    """Valider que la langue n'est pas vide.

    Args:
        language: La code de langue à valider.

    Raises:
        ValueError: Si la langue est vide ou None.
    """
    if not language:
        raise ValueError("La langue ne peut pas être vide.")


def build_wikipedia_url(language: str) -> str:
    """Construire l'URL de l'API Wikipedia pour le jour courant.

    Args:
        language: Le code de langue (ex: 'fr', 'en', 'es').

    Returns:
        L'URL complète de l'API Wikipedia.
    """
    today = date.today()
    month = today.strftime("%m")
    day = today.strftime("%d")
    return f"https://{language}.wikipedia.org/api/rest_v1/feed/onthisday/events/{month}/{day}"


def parse_wikipedia_response(data: dict) -> dict:
    """Parser la réponse JSON de l'API Wikipedia.

    Args:
        data: La réponse JSON brute de l'API.

    Returns:
        Un dictionnaire contenant le fait et les métadonnées.
    """
    events = data.get("events", [])

    if not events:
        return {"error": "Aucun événement trouvé."}

    # Choisir un événement aléatoire
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


async def get_wikipedia_fact(language: str) -> dict:
    """Récupérer un fait aléatoire lié au jour courant depuis Wikipedia.

    Args:
        language: Le code de langue (ex: 'fr', 'en', 'es').

    Returns:
        Un dictionnaire contenant soit le fait avec ses métadonnées,
        soit une erreur.

    Raises:
        ValueError: Si la langue est invalide.
        aiohttp.ClientError: En cas d'erreur réseau.
    """
    validate_language(language)

    url = build_wikipedia_url(language)

    headers = {
        "User-Agent": "WikipediaFact/1.0 (Python/aiohttp)",
        "Accept": "application/json",
    }

    async with aiohttp.ClientSession() as session:
        async with session.get(url, headers=headers) as response:
            if response.status != 200:
                print(response)
                return {"error": f"Erreur HTTP {response.status}"}

            data = await response.json()
            return parse_wikipedia_response(data)
