import random

from sdps.frontend.components.entities.dancer.clothing import (
    Pants,
    PantsType,
    Shoe,
    ShoeType,
    Top,
    TopType,
)
from sdps.frontend.components.entities.dancer.dancer import Dancer
from sdps.frontend.components.entities.dancer.skin import Skin

SKIN_TONES = [
    (255, 224, 189),
    (241, 194, 125),
    (224, 172, 105),
    (198, 134, 66),
    (141, 85, 36),
    (89, 47, 23),
]

FABRIC_COLORS = [
    (231, 76, 60),
    (46, 204, 113),
    (52, 152, 219),
    (241, 196, 15),
    (155, 89, 182),
    (26, 188, 156),
    (236, 240, 241),
]

DETAIL_COLORS = [
    (44, 62, 80),
    (52, 73, 94),
    (127, 140, 141),
    (236, 240, 241),
]


def generate_top():
    top_type = random.choice(list(TopType))
    return Top(
        top_type,
        random.choice(FABRIC_COLORS),
        random.choice(DETAIL_COLORS),
    )


def generate_pants():
    pants_type = random.choice(list(PantsType))
    return Pants(
        pants_type,
        random.choice(FABRIC_COLORS),
        random.choice(DETAIL_COLORS),
    )


def generate_shoes():
    shoe_type = random.choice(list(ShoeType))
    return Shoe(
        shoe_type,
        random.choice(FABRIC_COLORS),
        random.choice(DETAIL_COLORS),
    )


def generate_skin():
    return Skin(
        random.choice(SKIN_TONES),
        generate_top(),
        generate_pants(),
        generate_shoes(),
    )


def generate_dancer(groups, pos):
    return Dancer(groups, pos, generate_skin())
