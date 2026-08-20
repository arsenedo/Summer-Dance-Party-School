from enum import Enum

class ShoeType(Enum):
    BOOTS = 0
    SNEAKERS = 1


class PantsType(Enum):
    JEANS = 0
    SHORTS = 1


class TopType(Enum):
    T_SHIRT = 0
    TANK_TOP = 1

def _draw_tshirt(shape, w, h, main, detail):
    sleeve_h = int(h * 0.35)
    sleeve_w = max(1, int(w * 0.30))
    shape.draw_rectangle(0, 0, sleeve_w, sleeve_h, main)
    shape.draw_rectangle(w - sleeve_w, 0, sleeve_w, sleeve_h, main)
    neck_h = int(h * 0.15)
    shape.draw_rectangle(0, neck_h, w, h - neck_h, main)


def _draw_tank(shape, w, h, main, detail):
    strap_w = max(1, int(w * 0.25))
    strap_h = int(h * 0.25)
    shape.draw_rectangle(0, 0, strap_w, strap_h, main)
    shape.draw_rectangle(w - strap_w, 0, strap_w, strap_h, main)
    shape.draw_rectangle(0, strap_h, w, h - strap_h, main)


def _draw_jeans(shape, w, h, main, detail):
    shape.draw_rectangle(0, 0, w, h, main)
    band_h = max(1, int(h * 0.06))
    shape.draw_rectangle(0, 0, w, band_h, detail)


def _draw_shorts(shape, w, h, main, detail):
    shape.draw_rectangle(0, 0, w, int(h * 0.45), main)
    band_h = max(1, int(h * 0.06))
    shape.draw_rectangle(0, 0, w, band_h, detail)


def _draw_boots(shape, w, h, main, detail):
    shape.draw_rectangle(0, 0, w, h, main)
    sole = max(2, int(h * 0.15))
    shape.draw_rectangle(0, h - sole, w, sole, detail)


def _draw_sneakers(shape, w, h, main, detail):
    shape.draw_rectangle(0, 0, w, h, main)
    sole = max(2, int(h * 0.30))
    shape.draw_rectangle(0, h - sole, w, sole, detail)


TOP_DESIGNS = {
    TopType.T_SHIRT: _draw_tshirt,
    TopType.TANK_TOP: _draw_tank,
}

PANTS_DESIGNS = {
    PantsType.JEANS: _draw_jeans,
    PantsType.SHORTS: _draw_shorts,
}

SHOE_DESIGNS = {
    ShoeType.BOOTS: _draw_boots,
    ShoeType.SNEAKERS: _draw_sneakers,
}

SHOE_HEIGHT_RATIOS = {
    ShoeType.BOOTS: 0.30,
    ShoeType.SNEAKERS: 0.18,
}


class Clothing:
    def __init__(self, clothing_type, design, main_color, detail_color):
        self.clothing_type = clothing_type
        self.design = design
        self.main_color = main_color
        self.detail_color = detail_color


class Top(Clothing):
    def __init__(self, top_type, main_color, detail_color):
        super().__init__(
            top_type, TOP_DESIGNS[top_type], main_color, detail_color
        )


class Pants(Clothing):
    def __init__(self, pants_type, main_color, detail_color):
        super().__init__(
            pants_type, PANTS_DESIGNS[pants_type], main_color, detail_color
        )


class Shoe(Clothing):
    def __init__(self, shoe_type, main_color, detail_color):
        super().__init__(
            shoe_type, SHOE_DESIGNS[shoe_type], main_color, detail_color
        )
        self.height_ratio = SHOE_HEIGHT_RATIOS[shoe_type]
