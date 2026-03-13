from homeassistant.helpers.entity import Entity
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant

from .wikipedia_api import get_wikipedia_fact
from datetime import date

DOMAIN = "wikipedia_fact"

async def async_setup_entry(hass: HomeAssistant, config_entry: ConfigEntry, async_add_entities):
    """Configurer le capteur via une entrée de configuration."""
    # Récupère la langue depuis la configuration
    language = config_entry.data.get("language", "fr")
    sensor = WikipediaFactSensor("Wikipedia Fact", language)
    async_add_entities([sensor], update_before_add=True)

class WikipediaFactSensor(Entity):
    """Capteur pour récupérer un fait aléatoire lié au jour courant depuis Wikipedia."""

    def __init__(self, name, language):
        self._name = name
        self._state = None
        self._attributes = {}
        self._last_update = None
        self._language = language

    @property
    def name(self):
        return self._name

    @property
    def state(self):
        return self._state

    @property
    def extra_state_attributes(self):
        return self._attributes

    @property
    def icon(self):
        return "mdi:book-open-page-variant"

    async def async_update(self):
        # Ne mettre à jour que si la date a changé
        today = date.today()
        if self._last_update == today:
            return

        self._last_update = today

        result = await get_wikipedia_fact(self._language)

        if "error" in result:
            self._state = f"Erreur : {result['error']}"
            return

        # Définir un résumé court pour l'état et des détails dans les attributs
        self._state = result["resume"]  # Résumé limité à 100 caractères
        self._attributes = {
            "texte_complet": result["texte_complet"],
            "lien": result.get("lien"),
            "année": result["annee"],
        } if result.get("lien") else {"texte_complet": result["texte_complet"], "année": result["annee"]}
