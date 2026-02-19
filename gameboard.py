import pygame
import vars


def _shadow_round_rect(surf: pygame.Surface, rect: pygame.Rect, radius: int = 14) -> None:
    shadow = pygame.Surface((rect.w, rect.h), pygame.SRCALPHA)
    pygame.draw.rect(shadow, vars.SHADOW_RGBA, shadow.get_rect(), border_radius=radius)
    surf.blit(shadow, (rect.x, rect.y + 3))


def draw_panel(surf: pygame.Surface, layout: vars.Layout) -> pygame.Rect:
    panel = pygame.Rect(layout.pad, layout.pad, layout.panel_w, layout.screen_h - layout.pad * 2)

    _shadow_round_rect(surf, panel, radius=16)
    pygame.draw.rect(surf, vars.PANEL_BG, panel, border_radius=16)
    pygame.draw.rect(surf, vars.PANEL_STROKE, panel, width=1, border_radius=16)

    # Title
    title = layout.font_title.render("Game of Life", True, vars.TEXT)
    surf.blit(title, (panel.x + 16, panel.y + 14))

    # Accent underline
    y = panel.y + 14 + title.get_height() + 10
    pygame.draw.line(surf, vars.ACCENT_2, (panel.x + 16, y), (panel.x + panel.w - 16, y), 2)

    return panel


def draw_divider(surf: pygame.Surface, x: int, y: int, w: int) -> None:
    pygame.draw.line(surf, vars.PANEL_STROKE, (x, y), (x + w, y), 1)


class Button:
    def __init__(self, x: int, y: int, width: int, height: int, label: str):
        self.rect = pygame.Rect(x, y, width, height)
        self.label = label
        self.hover = False
        self.down = False

    def update(self, mx: int, my: int, mouse_down: bool) -> None:
        self.hover = self.rect.collidepoint(mx, my)
        self.down = self.hover and mouse_down

    def clicked(self, mx: int, my: int, mouse_released: bool) -> bool:
        return mouse_released and self.rect.collidepoint(mx, my)

    def draw(self, surf: pygame.Surface, layout: vars.Layout) -> None:
        if self.down:
            fill = vars.BTN_BG_DOWN
        elif self.hover:
            fill = vars.BTN_BG_HOVER
        else:
            fill = vars.BTN_BG

        # subtle shadow
        shadow_rect = self.rect.copy()
        shadow_rect.y += 2
        pygame.draw.rect(surf, (0, 0, 0, 60), shadow_rect, border_radius=12)

        pygame.draw.rect(surf, fill, self.rect, border_radius=12)
        pygame.draw.rect(surf, vars.PANEL_STROKE, self.rect, width=1, border_radius=12)

        text = layout.font_ui.render(self.label, True, vars.BTN_TEXT)
        surf.blit(
            text,
            (self.rect.centerx - text.get_width() // 2,
             self.rect.centery - text.get_height() // 2),
        )


class Slider:
    """Simple horizontal slider. Value in [min_val, max_val]."""

    def __init__(self, x: int, y: int, w: int, min_val: float, max_val: float, value: float):
        self.rect = pygame.Rect(x, y, w, 16)
        self.min_val = min_val
        self.max_val = max_val
        self.value = max(min_val, min(max_val, value))
        self.dragging = False

    def value01(self) -> float:
        return (self.value - self.min_val) / (self.max_val - self.min_val)

    def set_from_mouse(self, mx: int) -> None:
        t = (mx - self.rect.x) / max(1, self.rect.w)
        t = max(0.0, min(1.0, t))
        self.value = self.min_val + t * (self.max_val - self.min_val)

    def handle_event(self, e: pygame.event.Event) -> None:
        if e.type == pygame.MOUSEBUTTONDOWN and e.button == 1:
            if self.rect.collidepoint(e.pos):
                self.dragging = True
                self.set_from_mouse(e.pos[0])
        elif e.type == pygame.MOUSEBUTTONUP and e.button == 1:
            self.dragging = False
        elif e.type == pygame.MOUSEMOTION and self.dragging:
            self.set_from_mouse(e.pos[0])

    def draw(self, surf: pygame.Surface, layout: vars.Layout, label: str) -> None:
        lab = layout.font_small.render(f"{label}: {self.value:.1f} gen/s", True, vars.TEXT_MUTED)
        surf.blit(lab, (self.rect.x, self.rect.y - lab.get_height() - 8))

        pygame.draw.rect(surf, vars.SLIDER_TRACK, self.rect, border_radius=10)
        pygame.draw.rect(surf, vars.PANEL_STROKE, self.rect, width=1, border_radius=10)

        fill_w = int(self.rect.w * self.value01())
        fill = pygame.Rect(self.rect.x, self.rect.y, fill_w, self.rect.h)
        pygame.draw.rect(surf, vars.ACCENT_2, fill, border_radius=10)

        knob_x = self.rect.x + fill_w
        knob = pygame.Rect(0, 0, 16, self.rect.h + 10)
        knob.center = (knob_x, self.rect.centery)
        pygame.draw.rect(surf, vars.SLIDER_KNOB, knob, border_radius=8)
        pygame.draw.rect(surf, (0, 0, 0), knob, width=1, border_radius=8)


class GridLine:
    def __init__(self, start: tuple[int, int], end: tuple[int, int]):
        self.start = start
        self.end = end

    def draw(self, surf: pygame.Surface) -> None:
        pygame.draw.line(surf, vars.GRID_LINE, self.start, self.end, 1)


def create_grid(layout: vars.Layout, gridlines: list[GridLine]) -> None:
    gridlines.clear()

    x0, y0 = layout.board_x, layout.board_y
    x1, y1 = x0 + layout.board_w, y0 + layout.board_h

    for c in range(layout.cols + 1):
        x = x0 + c * layout.tile
        gridlines.append(GridLine((x, y0), (x, y1)))

    for r in range(layout.rows + 1):
        y = y0 + r * layout.tile
        gridlines.append(GridLine((x0, y), (x1, y)))

    # board border
    gridlines.append(GridLine((x0, y0), (x1, y0)))
    gridlines.append(GridLine((x1, y0), (x1, y1)))
    gridlines.append(GridLine((x1, y1), (x0, y1)))
    gridlines.append(GridLine((x0, y1), (x0, y0)))
