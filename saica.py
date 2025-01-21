#!/usr/bin/env python
# coding: utf-8

from abc import abstractmethod
import os
from typing import Optional, Final, final
import fontforge
import psMat

HALF_WIDTH: Final = 1024
WIDTH: Final = 2048
HALF_HEIGHT: Final = 1024
HEIGHT: Final = 2048
# ref: https://googlefonts.github.io/gf-guide/metrics.html#cjk-vertical-metrics
ASCENT: Final = 1640 # original: 820
DESCENT: Final = 408 # original: 204
EM: Final = 2048
VERSION: Final = "0.1.0"
FAMILY: Final = "Saica"

fonts = [
    {
         "family": FAMILY,
         "name": FAMILY + "-Regular",
         "filename": FAMILY + "-Regular.ttf",
         "weight": 400,
         "weight_name": "Regular",
         "style_name": "Regular",
         "hack": "Hack-Regular.ttf",
         "mgen_plus": "rounded-mgenplus-1m-regular.ttf",
         "italic": False,
     }, {
         "family": FAMILY,
         "name": FAMILY + "-RegularItalic",
         "filename": FAMILY + "-RegularItalic.ttf",
         "weight": 400,
         "weight_name": "Regular",
         "style_name": "Italic",
         "hack": "Hack-Regular.ttf",
         "mgen_plus": "rounded-mgenplus-1m-regular.ttf",
         "italic": True,
    }, {
        "family": FAMILY,
        "name": FAMILY + "-Bold",
        "filename": FAMILY + "-Bold.ttf",
        "weight": 700,
        "weight_name": "Bold",
        "style_name": "Bold",
        "hack": "Hack-Bold.ttf",
        "mgen_plus": "rounded-mgenplus-1m-bold.ttf",
        "italic": False,
    }, {
        "family": FAMILY,
        "name": FAMILY + "-BoldItalic",
        "filename": FAMILY + "-BoldItalic.ttf",
        "weight": 700,
        "weight_name": "Bold",
        "style_name": "Bold Italic",
        "hack": "Hack-Bold.ttf",
        "mgen_plus": "rounded-mgenplus-1m-bold.ttf",
        "italic": True,
    }
]

def read_copyright():
    with open("./COPYRIGHT", "r") as f:
        return f.read()

def read_license():
    with open("./LICENSE", "r") as f:
        return f.read()

COPYRIGHT: Final = read_copyright()
LICENSE: Final = read_license()

@final
class FontBase:
    def __init__(self, font_path: str, is_bold: bool, is_italic: bool):
        self.font: fontforge.font = fontforge.open(font_path)
        self.is_bold = is_bold
        self.is_italic = is_italic

    @abstractmethod
    def patch(self):
        pass

    def align_to_center(self, glyph: fontforge.glyph):
        """
        フォントを中央揃えにする (横幅 > 1400 の場合)
        """
        width = 0

        if glyph.width > 1400:
            width = WIDTH
        else:
            width = HALF_WIDTH

        glyph.width = width
        bearing = (glyph.left_side_bearing + glyph.right_side_bearing) / 2
        glyph.left_side_bearing = bearing
        glyph.right_side_bearing = bearing

    def align_to_left(self, glyph: fontforge.glyph):
        """
        フォントを左揃えにする
        """
        width_temp = glyph.width
        glyph.left_side_bearing = 0
        glyph.width = width_temp

    def align_to_right(self, glyph: fontforge.glyph):
        """
        フォントを右揃えにする
        """
        width_temp = glyph.width
        bb = glyph.boundingBox()
        left = width_temp - (bb[2] - bb[0])
        glyph.left_side_bearing = left
        glyph.width = width_temp

    def close(self):
        self.font.close()

@final
class Hack(FontBase):
    def __init__(self, font_path: str, is_bold: bool, is_italic: bool):
        super().__init__(font_path, is_bold, is_italic)

    def patch(self):
        """
        Hack にパッチを当てる
        """
        self._remove_glyph()
        self._transform()
        self._modify_m()
        self._modify_border()

    def _remove_glyph(self):
        """
        Rounded Mgen+ を採用したいグリフを Hack から削除
        """
        glyphs = [
            0x2026, # …
        ]

        for g in glyphs:
            self.font.selection.select(g)
            self.font.clear()

    def _transform(self):
        """
        Hack の大きさを変更
        """
        for g in self.font.glyphs():
            g.transform(psMat.scale(0.84)) # original: 0.42
            self.align_to_center(g)

    def _modify_border(self):
        """
        Hack の罫線を太くする? / Italic 処理
        """
        for g in self.font.glyphs():
            if g.isWorthOutputting:
                if self.is_italic:
                    g.transform(psMat.skew(0.25)) # original: 0.25
                if g.encoding >= 0x2500 and g.encoding <= 0x25af:
                    g.transform(psMat.compose(psMat.scale(2.048, 2.048), psMat.translate(0, -60))) # original: (1.024, 1.024), (0, -30)
                    self.align_to_center(g)

    def _modify_m(self, font_dir: str):
        """
        m を変更
        """
        m: fontforge.font
        if self.is_bold:
            m = fontforge.open(os.path.join(font_dir, "m-Bold.sfd"))
        else:
            m = fontforge.open(os.path.join(font_dir, "m-Regular.sfd"))
        m.selection.select(0x6d)
        m.copy()
        self.font.selection.select(0x6d)
        self.font.paste()
        for g in m.glyphs():
            if g.encoding == 0x6d:
                anchorPoints = g.anchorPoints
        for g in self.font.glyphs():
            if g.encoding == 0x6d:
                g.anchorPoints = anchorPoints
        m.close()

@final
class MgenPlus(FontBase):
    def __init__(self, font_path: str, is_bold: bool):
        super().__init__(font_path, is_bold)
        self.ignoring_center = [
            0x3001, 0x3002, 0x3008, 0x3009, 0x300a, 0x300b, 0x300c, 0x300d,
            0x300e, 0x300f, 0x3010, 0x3011, 0x3014, 0x3015, 0x3016, 0x3017,
            0x3018, 0x3019, 0x301a, 0x301b, 0x301d, 0x301e, 0x3099, 0x309a,
            0x309b, 0x309c,
        ]

    def patch(self):
        """
        Rounded Mgen+ にパッチを当てる
        """
        self._transform()

    def _transform(self):
        """
        Rounded Mgen+ の大きさを変更
        """
        for g in self.font.glyphs():
            g.transform(psMat.scale(1.82)) # original: 0.91

            width_threshold = 1400

            if self.is_italic:
                g.transform(psMat.skew(0.25))
                skew_amount = g.font.ascent * 1.82 * 0.50 # original: 0.91 * 0.25
                g.width = g.width + skew_amount
                width_threshold += skew_amount

            if g.width > width_threshold:
                width = WIDTH
            else:
                width = HALF_WIDTH

            g.transform(psMat.translate((width - g.width)/ 2, 0))
            g.width = width

            if g.encoding in self.ignoring_center:
                pass
            else:
                self.align_to_center(g)

            if g.encoding >= 0x2500 and g.encoding <= 0x257f:
                # 全角の罫線を 0xf0000 以降に退避 (0xf2500 - 0xf257f)
                self.font.selection.select(g.encoding)
                self.font.copy()
                self.font.selection.select(g.encoding + 0xf0000)
                self.font.paste()

    def _remove_glyph(self):
        """
        Hack を採用したいグリフを Rounded Mgen+ から削除
        """
        glyphs = [
            *range(0x2500, 0x257f + 1), # Box Drawing
        ]

        for g in glyphs:
            self.font.selection.select(g)
            self.font.clear()

@final
class Nerd(FontBase):
    def __init__(self, font_path: str):
        super().__init__(font_path, False, False)

    def patch(self):
        """
        Nerd にパッチを当てる
        """
        pass

@final
class NotoEmoji(FontBase):
    def __init__(self, font_path: str):
        super().__init__(font_path, False, False)

    def patch(self):
        """
        Noto Emoji にパッチを当てる
        """
        pass

    def transform(self):
        """
        Noto Emoji の大きさを変更
        """
        for g in self.font.glyphs():
            if g.isWorthOutputting and g.encoding > 0x04f9:
                g.transform(psMat.scale(0.84)) # original: 0.42
                self.align_to_center(g)

@final
class SaicaBuidler:
    def __init__(self):
        _font: fontforge.font = fontforge.font()

        # Set font properties
        _font.encoding = "UnicodeFull"
        _font.em = EM
        _font.ascent = ASCENT
        _font.descent = DESCENT
        _font.familyname = FAMILY
        _font.fontname = FAMILY
        _font.version = VERSION

        # Set OS/2 and Windows metrics
        _font.os2_width = 5
        _font.os2_fstype = 0
        _font.os2_version = 4
        _font.os2_vendor = "KASH"

        # ref: https://googlefonts.github.io/gf-guide/metrics.html#cjk-vertical-metrics
        _font.os2_winascent = ASCENT   # should be <= 1.16   * em (= 2375.68)
        _font.os2_winascent_add = False
        _font.os2_windescent = DESCENT # should be >= -0.288 * em (= -589.824)
        _font.os2_windescent_add = False

        _font.os2_typoascent = 1802 # 0.88 * em (= 1802.24)
        _font.os2_typoascent_add = False
        _font.os2_typodescent = 246 # -0.12 * em (= -245.76)
        _font.os2_typodescent_add = False
        _font.os2_typolinegap = 0

        _font.hhea_ascent = ASCENT
        _font.hhea_ascent_add = False
        _font.hhea_descent = DESCENT
        _font.hhea_descent_add = False
        _font.hhea_linegap = 0

        # Set name table
        # ref: https://developer.apple.com/fonts/TrueType-Reference-Manual/RM06/Chap6name.html
        _font.appendSFNTName(0x409,0, COPYRIGHT)
        _font.appendSFNTName(0x411,0, COPYRIGHT)
        _font.appendSFNTName(0x409,1, FAMILY)
        _font.appendSFNTName(0x411,1, FAMILY)
        _font.appendSFNTName(0x409,5, f"Version {VERSION}")
        _font.appendSFNTName(0x411,5, f"Version {VERSION}")
        _font.appendSFNTName(0x409,13, LICENSE)
        _font.appendSFNTName(0x411,13, LICENSE)
        _font.appendSFNTName(0x409,16, FAMILY)
        _font.appendSFNTName(0x411,16, FAMILY)

        # Property
        self.font = _font
        self.name: Optional[str] = None
        self.filename: Optional[str] = None

    def build(self, font_info: dict):
        name = font_info["name"]
        filename = font_info["filename"]
        weight = font_info["weight"]
        weight_name = font_info["weight_name"]
        style_name = font_info["style_name"]

        # Set font properties
        self.font.fullname = name
        self.font.weight = weight_name

        # Set OS/2 and Windows metrics
        self.font.os2_weight = weight

        if style_name == "Regular":
            self.font.os2_stylemap = 64
        elif style_name == "Bold":
            self.font.os2_stylemap = 32
        elif style_name == "Italic":
            self.font.os2_stylemap = 1
        elif style_name == "Bold Italic":
            self.font.os2_stylemap = 33

        self.font.os2_panose = (2, 11, int(weight / 100), 9, 2, 2, 3, 2, 2, 7)

        # Set name table
        # ref: https://developer.apple.com/fonts/TrueType-Reference-Manual/RM06/Chap6name.html
        self.font.appendSFNTName(0x409, 2, style_name)
        self.font.appendSFNTName(0x411, 2, style_name)
        self.font.appendSFNTName(0x409, 3, f"{name}; v{VERSION}")
        self.font.appendSFNTName(0x411, 3, f"{name}; v{VERSION}")
        self.font.appendSFNTName(0x409, 4, name)
        self.font.appendSFNTName(0x411, 4, name)
        self.font.appendSFNTName(0x409, 6, name)
        self.font.appendSFNTName(0x411, 6, name)
        self.font.appendSFNTName(0x409, 17, style_name)
        self.font.appendSFNTName(0x411, 17, style_name)

        # Property
        self.name = name
        self.filename = filename

        return self

    def add_font(self, hack: type[FontBase]):
        pass

    def generate(self, filename: str):
        with open(f"./dist/{filename}", "w") as f:
            pass

def main():
    pass
