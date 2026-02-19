import pygame
import vars


class Tile:
    def __init__(self, x: int, y: int, col: int, row: int):
        self.x = x
        self.y = y
        self.col = col
        self.row = row

        self.alive = False
        self.next_alive = False
        self.hover = False

        self.neighbors: list["Tile"] = []

    def draw(self, surf: pygame.Surface, layout: vars.Layout) -> None:
        if self.hover:
            color = vars.CELL_HOVER
        else:
            color = vars.CELL_ALIVE if self.alive else vars.CELL_DEAD

        pygame.draw.rect(surf, color, (self.x, self.y, layout.tile, layout.tile))

        # subtle inner sheen on alive cells
        if self.alive and not self.hover:
            inner = pygame.Rect(self.x + 2, self.y + 2, layout.tile - 4, layout.tile - 4)
            pygame.draw.rect(surf, (255, 255, 255, 20), inner, width=1, border_radius=4)

    def set_hover(self, mx: int, my: int, layout: vars.Layout) -> None:
        self.hover = (self.x <= mx < self.x + layout.tile) and (self.y <= my < self.y + layout.tile)

    def toggle_if_clicked(self, clicked: bool) -> None:
        if clicked and self.hover:
            self.alive = not self.alive

    def erase_if_right_click(self, right_clicked: bool) -> None:
        if right_clicked and self.hover:
            self.alive = False

    def compute_next(self) -> None:
        n = 0
        for t in self.neighbors:
            if t.alive:
                n += 1

        # Conway rules
        if self.alive:
            self.next_alive = (n == 2 or n == 3)
        else:
            self.next_alive = (n == 3)

    def apply_next(self) -> None:
        self.alive = self.next_alive


def create_tiles(layout: vars.Layout, tiles: list[Tile]) -> None:
    tiles.clear()
    for r in range(layout.rows):
        for c in range(layout.cols):
            x = layout.board_x + c * layout.tile
            y = layout.board_y + r * layout.tile
            tiles.append(Tile(x, y, c, r))


def link_neighbors(layout: vars.Layout, tiles: list[Tile], wrap: bool = True) -> None:
    """
    If wrap=True, the grid wraps at edges (toroidal topology).
    If wrap=False, edges have fewer neighbors (bounded grid).
    """
    by_pos = {(t.col, t.row): t for t in tiles}

    for t in tiles:
        t.neighbors.clear()
        for dr in (-1, 0, 1):
            for dc in (-1, 0, 1):
                if dc == 0 and dr == 0:
                    continue

                nc = t.col + dc
                nr = t.row + dr

                if wrap:
                    nc %= layout.cols
                    nr %= layout.rows
                    t.neighbors.append(by_pos[(nc, nr)])
                else:
                    if 0 <= nc < layout.cols and 0 <= nr < layout.rows:
                        t.neighbors.append(by_pos[(nc, nr)])


def clear(tiles: list[Tile]) -> None:
    for t in tiles:
        t.alive = False
        t.next_alive = False


def randomize(tiles: list[Tile], p: float = 0.22) -> None:
    import random
    for t in tiles:
        t.alive = (random.random() < p)


# import pygame
# import vars


# class Tile:
#     def __init__(self, x: int, y: int, col: int, row: int):
#         self.x = x
#         self.y = y
#         self.col = col
#         self.row = row

#         self.alive = False
#         self.next_alive = False
#         self.hover = False

#         self.neighbors: list["Tile"] = []

#     def draw(self, surf: pygame.Surface, layout: vars.Layout) -> None:
#         if self.hover:
#             color = vars.CELL_HOVER
#         else:
#             color = vars.CELL_ALIVE if self.alive else vars.CELL_DEAD

#         pygame.draw.rect(surf, color, (self.x, self.y, layout.tile, layout.tile))

#         # subtle inner sheen on alive cells
#         if self.alive and not self.hover:
#             inner = pygame.Rect(self.x + 2, self.y + 2, layout.tile - 4, layout.tile - 4)
#             pygame.draw.rect(surf, (255, 255, 255, 20), inner, width=1, border_radius=4)

#     def set_hover(self, mx: int, my: int, layout: vars.Layout) -> None:
#         self.hover = (self.x <= mx < self.x + layout.tile) and (self.y <= my < self.y + layout.tile)

#     def toggle_if_clicked(self, clicked: bool) -> None:
#         if clicked and self.hover:
#             self.alive = not self.alive

#     def erase_if_right_click(self, right_clicked: bool) -> None:
#         if right_clicked and self.hover:
#             self.alive = False

#     def compute_next(self) -> None:
#         n = 0
#         for t in self.neighbors:
#             if t.alive:
#                 n += 1

#         # Conway rules
#         if self.alive:
#             self.next_alive = (n == 2 or n == 3)
#         else:
#             self.next_alive = (n == 3)

#     def apply_next(self) -> None:
#         self.alive = self.next_alive


# def create_tiles(layout: vars.Layout, tiles: list[Tile]) -> None:
#     tiles.clear()
#     for r in range(layout.rows):
#         for c in range(layout.cols):
#             x = layout.board_x + c * layout.tile
#             y = layout.board_y + r * layout.tile
#             tiles.append(Tile(x, y, c, r))


# def link_neighbors(layout: vars.Layout, tiles: list[Tile], wrap: bool = True) -> None:
#     """
#     If wrap=True, the grid wraps at edges (toroidal topology).
#     If wrap=False, edges have fewer neighbors (bounded grid).
#     """
#     by_pos = {(t.col, t.row): t for t in tiles}

#     for t in tiles:
#         t.neighbors.clear()
#         for dr in (-1, 0, 1):
#             for dc in (-1, 0, 1):
#                 if dc == 0 and dr == 0:
#                     continue

#                 nc = t.col + dc
#                 nr = t.row + dr

#                 if wrap:
#                     nc %= layout.cols
#                     nr %= layout.rows
#                     t.neighbors.append(by_pos[(nc, nr)])
#                 else:
#                     if 0 <= nc < layout.cols and 0 <= nr < layout.rows:
#                         t.neighbors.append(by_pos[(nc, nr)])


# def clear(tiles: list[Tile]) -> None:
#     for t in tiles:
#         t.alive = False
#         t.next_alive = False


# def randomize(tiles: list[Tile], p: float = 0.22) -> None:
#     import random
#     for t in tiles:
#         t.alive = (random.random() < p)


# # import pygame
# # import vars


# # class Tile:
# #     def __init__(self, x: int, y: int, col: int, row: int):
# #         self.x = x
# #         self.y = y
# #         self.col = col
# #         self.row = row

# #         self.alive = False
# #         self.next_alive = False
# #         self.hover = False

# #         self.neighbors: list["Tile"] = []

# #     def draw(self, surf: pygame.Surface, layout: vars.Layout) -> None:
# #         if self.hover:
# #             color = vars.CELL_HOVER
# #         else:
# #             color = vars.CELL_ALIVE if self.alive else vars.CELL_DEAD

# #         pygame.draw.rect(surf, color, (self.x, self.y, layout.tile, layout.tile))

# #         # tiny inner sheen on alive cells (subtle “premium” look)
# #         if self.alive and not self.hover:
# #             inner = pygame.Rect(self.x + 2, self.y + 2, layout.tile - 4, layout.tile - 4)
# #             pygame.draw.rect(surf, (255, 255, 255, 20), inner, width=1, border_radius=4)

# #     def set_hover(self, mx: int, my: int, layout: vars.Layout) -> None:
# #         self.hover = (self.x <= mx < self.x + layout.tile) and (self.y <= my < self.y + layout.tile)

# #     def toggle_if_clicked(self, mx: int, my: int, clicked: bool) -> None:
# #         if clicked and self.hover:
# #             self.alive = not self.alive

# #     def erase_if_right_click(self, mx: int, my: int, right_clicked: bool) -> None:
# #         if right_clicked and self.hover:
# #             self.alive = False

# #     def compute_next(self) -> None:
# #         n = 0
# #         for t in self.neighbors:
# #             if t.alive:
# #                 n += 1

# #         # Conway rules
# #         if self.alive:
# #             self.next_alive = (n == 2 or n == 3)
# #         else:
# #             self.next_alive = (n == 3)

# #     def apply_next(self) -> None:
# #         self.alive = self.next_alive


# # def create_tiles(layout: vars.Layout, tiles: list[Tile]) -> None:
# #     tiles.clear()
# #     for r in range(layout.rows):
# #         for c in range(layout.cols):
# #             x = layout.board_x + c * layout.tile
# #             y = layout.board_y + r * layout.tile
# #             tiles.append(Tile(x, y, c, r))


# # def link_neighbors(layout: vars.Layout, tiles: list[Tile]) -> None:
# #     # Map for quick lookup
# #     by_pos = {(t.col, t.row): t for t in tiles}

# #     for t in tiles:
# #         t.neighbors.clear()
# #         for dr in (-1, 0, 1):
# #             for dc in (-1, 0, 1):
# #                 if dc == 0 and dr == 0:
# #                     continue
# #                 nc = t.col + dc
# #                 nr = t.row + dr
# #                 if 0 <= nc < layout.cols and 0 <= nr < layout.rows:
# #                     t.neighbors.append(by_pos[(nc, nr)])


# # def clear(tiles: list[Tile]) -> None:
# #     for t in tiles:
# #         t.alive = False
# #         t.next_alive = False


# # def randomize(tiles: list[Tile], p: float = 0.22) -> None:
# #     import random
# #     for t in tiles:
# #         t.alive = (random.random() < p)
