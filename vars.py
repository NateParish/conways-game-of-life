import pygame
from dataclasses import dataclass

pygame.font.init()


# ----------------------------
# Theme (polished dark UI)
# ----------------------------
BG = (14, 15, 18)
PANEL_BG = (22, 24, 29)
PANEL_STROKE = (40, 42, 48)

TEXT = (238, 238, 240)
TEXT_MUTED = (175, 180, 188)

ACCENT = (235, 220, 140)     # warm gold
ACCENT_2 = (21, 225, 90)   # subtle cyan for highlight

GRID_LINE = (38, 40, 46)

CELL_DEAD = (30, 32, 38)
CELL_ALIVE = (235, 220, 140)
CELL_HOVER = (120, 190, 210)

BTN_BG = (46, 48, 56)
BTN_BG_HOVER = (58, 60, 70)
BTN_BG_DOWN = (72, 74, 86)
BTN_TEXT = (238, 238, 240)

SLIDER_TRACK = (34, 36, 42)
SLIDER_KNOB = (238, 238, 240)

SHADOW_RGBA = (0, 0, 0, 95)


@dataclass
class Layout:
    screen_w: int
    screen_h: int

    panel_w: int
    pad: int

    tile: int
    cols: int
    rows: int

    board_x: int
    board_y: int
    board_w: int
    board_h: int

    font_title: pygame.font.Font
    font_ui: pygame.font.Font
    font_small: pygame.font.Font


CAPTION = "Conway's Game of Life"
FPS = 60


def choose_window_size() -> tuple[int, int]:
    """Pick a reasonable window size based on the user's display."""
    info = pygame.display.Info()
    dw, dh = info.current_w, info.current_h

    w = int(dw * 0.82)
    h = int(dh * 0.82)

    # Clamp to sane range
    w = max(940, min(w, 1500))
    h = max(680, min(h, 980))
    return w, h


def build_layout(screen_w: int, screen_h: int) -> Layout:
    pad = 14
    panel_w = 290

    # Tile size: aim for a nice density; adjust if you want
    tile = 10

    board_w = screen_w - panel_w - pad * 3
    board_h = screen_h - pad * 2

    cols = max(10, board_w // tile)
    rows = max(10, board_h // tile)

    board_w = cols * tile
    board_h = rows * tile

    board_x = panel_w + pad * 2
    board_y = pad

    font_title = pygame.font.SysFont("arial", 28, bold=True)
    font_ui = pygame.font.SysFont("arial", 18)
    font_small = pygame.font.SysFont("arial", 14)

    return Layout(
        screen_w=screen_w,
        screen_h=screen_h,
        panel_w=panel_w,
        pad=pad,
        tile=tile,
        cols=cols,
        rows=rows,
        board_x=board_x,
        board_y=board_y,
        board_w=board_w,
        board_h=board_h,
        font_title=font_title,
        font_ui=font_ui,
        font_small=font_small,
    )
