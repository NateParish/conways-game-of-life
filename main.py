import pygame
import vars
import creatures
import gameboard


def main() -> None:
    pygame.init()

    w, h = vars.choose_window_size()
    win = pygame.display.set_mode((w, h))
    pygame.display.set_caption(vars.CAPTION)

    layout = vars.build_layout(w, h)

    clock = pygame.time.Clock()
    tiles: list[creatures.Tile] = []
    gridlines: list[gameboard.GridLine] = []

    creatures.create_tiles(layout, tiles)

    # --- Wrapping toggle state ---
    wrap_enabled = True
    creatures.link_neighbors(layout, tiles, wrap=wrap_enabled)

    gameboard.create_grid(layout, gridlines)

    # --- State ---
    sim_running = False
    tick_accum = 0.0
    generation = 0

    # Optional starting pattern
    creatures.clear(tiles)

    def at(c, r):
        return tiles[r * layout.cols + c]

    if layout.cols > 12 and layout.rows > 12:
        at(6, 6).alive = True
        at(7, 7).alive = True
        at(5, 8).alive = True
        at(6, 8).alive = True
        at(7, 8).alive = True

    # --- UI layout ---
    pad = layout.pad
    panel = pygame.Rect(pad, pad, layout.panel_w, layout.screen_h - pad * 2)

    x = panel.x + 16
    y = panel.y + 86
    bw = panel.w - 32
    bh = 44
    gap = 10

    btn_run = gameboard.Button(x, y, bw, bh, "Start (Space)")
    y += bh + gap

    btn_step = gameboard.Button(x, y, bw, bh, "Step (N)")
    y += bh + gap

    btn_clear = gameboard.Button(x, y, bw, bh, "Clear (C)")
    y += bh + gap

    btn_rand = gameboard.Button(x, y, bw, bh, "Randomize (R)")
    y += bh + gap
    
    btn_wrap = gameboard.Button(x, y, bw, 40, "Wrap: On (W)")
    y += bh + gap
    y += 40

    div_y = y + 20

    speed = 10.0
    slider = gameboard.Slider(x, y, bw, 1.0, 60.0, speed)

    # --- Mouse state (for drag paint/erase) ---
    mouse_down = False
    mouse_released = False
    left_down = False
    right_down = False

    def step_once() -> None:
        nonlocal generation
        for t in tiles:
            t.compute_next()
        for t in tiles:
            t.apply_next()
        generation += 1

    def alive_count() -> int:
        return sum(1 for t in tiles if t.alive)

    def apply_wrap_setting() -> None:
        creatures.link_neighbors(layout, tiles, wrap=wrap_enabled)

    def redraw(mx: int, my: int) -> None:
        win.fill(vars.BG)

        # Panel
        panel_rect = gameboard.draw_panel(win, layout)

        # Status
        status = "Running" if sim_running else "Paused"
        st = layout.font_small.render(status, True, vars.TEXT_MUTED)
        win.blit(st, (panel_rect.x + 18, panel_rect.y + 65))

        gameboard.draw_divider(win, panel_rect.x + 16, div_y, panel_rect.w - 32)

        # Labels
        btn_run.label = "Pause (Space)" if sim_running else "Start (Space)"
        btn_wrap.label = f"Wrap: {'On' if wrap_enabled else 'Off'} (W)"

        # Hover/press states
        btn_run.update(mx, my, mouse_down)
        btn_step.update(mx, my, mouse_down)
        btn_clear.update(mx, my, mouse_down)
        btn_rand.update(mx, my, mouse_down)
        btn_wrap.update(mx, my, mouse_down)

        # Draw buttons
        btn_run.draw(win, layout)
        btn_step.draw(win, layout)
        btn_clear.draw(win, layout)
        btn_rand.draw(win, layout)

        btn_wrap.draw(win, layout)
        slider.draw(win, layout, "Speed")

        # Tiles
        for t in tiles:
            t.set_hover(mx, my, layout)
            t.draw(win, layout)

        # Grid
        for gl in gridlines:
            gl.draw(win)

        # Footer help + stats (lifted upward a bit)
        help1 = layout.font_small.render("LMB drag: paint   RMB drag: erase", True, vars.TEXT_MUTED)
        help2 = layout.font_small.render("Space: start/pause   N: step   W: wrap", True, vars.TEXT_MUTED)

        stats_lines = [
            f"Generation: {generation}",
            f"Alive: {alive_count()}",
            f"Grid: {layout.cols} x {layout.rows}",
            f"Speed: {slider.value:.1f} gen/s",
            f"Wrap: {'On' if wrap_enabled else 'Off'}",
        ]
        stats_surfs = [layout.font_small.render(s, True, vars.TEXT_MUTED) for s in stats_lines]

        # Raise the block: bigger bottom padding
        bottom_pad = 42
        stats_block_h = sum(s.get_height() for s in stats_surfs) + 6 * (len(stats_surfs) - 1)
        help_block_h = help1.get_height() + 6 + help2.get_height()

        stats_y0 = panel_rect.y + panel_rect.h - bottom_pad - stats_block_h
        help_y0 = stats_y0 - 14 - help_block_h

        win.blit(help1, (panel_rect.x + 18, help_y0))
        win.blit(help2, (panel_rect.x + 18, help_y0 + help1.get_height() + 6))

        yy = stats_y0
        for s in stats_surfs:
            win.blit(s, (panel_rect.x + 18, yy))
            yy += s.get_height() + 6

        pygame.display.flip()

    while True:
        dt = clock.tick(vars.FPS) / 1000.0
        mx, my = pygame.mouse.get_pos()

        mouse_released = False

        for event in pygame.event.get():
            slider.handle_event(event)

            if event.type == pygame.QUIT:
                pygame.quit()
                return

            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_down = True
                if event.button == 1:
                    left_down = True
                if event.button == 3:
                    right_down = True

            if event.type == pygame.MOUSEBUTTONUP:
                mouse_down = False
                mouse_released = True
                if event.button == 1:
                    left_down = False
                if event.button == 3:
                    right_down = False

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    sim_running = not sim_running
                elif event.key == pygame.K_c:
                    creatures.clear(tiles)
                    generation = 0
                elif event.key == pygame.K_r:
                    creatures.randomize(tiles, p=0.22)
                    generation = 0
                elif event.key == pygame.K_n:
                    sim_running = False
                    step_once()
                elif event.key == pygame.K_w:
                    wrap_enabled = not wrap_enabled
                    apply_wrap_setting()

        # UI clicks (release-based)
        if btn_run.clicked(mx, my, mouse_released):
            sim_running = not sim_running

        if btn_step.clicked(mx, my, mouse_released):
            sim_running = False
            step_once()

        if btn_clear.clicked(mx, my, mouse_released):
            creatures.clear(tiles)
            generation = 0

        if btn_rand.clicked(mx, my, mouse_released):
            creatures.randomize(tiles, p=0.22)
            generation = 0

        if btn_wrap.clicked(mx, my, mouse_released):
            wrap_enabled = not wrap_enabled
            apply_wrap_setting()

        # Drag paint/erase (ignore while dragging slider)
        if not slider.dragging:
            if left_down or right_down:
                for t in tiles:
                    if t.hover:
                        if left_down:
                            t.alive = True
                        elif right_down:
                            t.alive = False

        # Simulation update
        speed = float(slider.value)
        if sim_running:
            tick_accum += dt
            step_interval = 1.0 / max(0.1, speed)
            while tick_accum >= step_interval:
                step_once()
                tick_accum -= step_interval
        else:
            tick_accum = 0.0

        redraw(mx, my)


if __name__ == "__main__":
    main()
