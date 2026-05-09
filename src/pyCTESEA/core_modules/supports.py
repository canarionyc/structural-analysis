# %% SUPPORT CONDITIONS ENUMERATION
from enum import Enum


class SupportType(Enum):
    """
    Standard support types and their theoretical beta (β) factors
    according to DB SE-A / Eurocode 3.
    """
    FIXED = {"name_es": "Empotrado", "name_en": "Fixed", "beta": 0.5}
    PINNED = {"name_es": "Articulado", "name_en": "Pinned", "beta": 1.0}
    ROLLER = {"name_es": "Deslizante", "name_en": "Roller", "beta": 1.0}
    FREE = {"name_es": "Libre", "name_en": "Free", "beta": 2.0}
    FIXED_SLIDER = {"name_es": "Empotrado-Deslizante", "name_en": "Fixed-Slider", "beta": 1.0}
    PINNED_FIXED = {"name_es": "Articulado-Empotrado", "name_en": "Pinned-Fixed", "beta": 0.7}