import curses
import random
import time

w = 10
h = 20

grid = [["  " for _ in range(w)] for _ in range(h)]

items = [
    [["＃＃＃＃"], ['＃', '＃', '＃', '＃']],
    [[" ＃", " ＃", "＃＃"], ["＃  ", "＃＃＃"], ["＃＃", "＃ ", "＃ "], ["＃＃＃", "  ＃"]],
    [["＃ ", "＃ ", "＃＃"], ["＃＃＃", "＃  "], ["＃＃", " ＃", " ＃"], ["  ＃", "＃＃＃"]],
    [["＃＃", "＃＃"]],
    [[" ＃＃", "＃＃ "], ["＃ ", "＃＃", " ＃"]],
    [["＃＃＃", " ＃ "], [" ＃", "＃＃", " ＃"], [" ＃ ", "＃＃＃"], ["＃ ", "＃＃", "＃ "]],
    [["＃＃ ", " ＃＃"], [" ＃", "＃＃", "＃ "]]
]

current = None
p_x = 0
p_y = 0
r = 0

def draw(stdscr):
    stdscr.clear()
    temp_grid = [row[:] for row in grid]
    for y, row in enumerate(current[r % len(current)]):
        for x, cell in enumerate(row):
            if cell == '＃':
                gx = p_x + x
                gy = p_y + y
                if 0 <= gx < w and 0 <= gy < h:
                    temp_grid[gy][gx] = '＃'
    for row in temp_grid:
        stdscr.addstr("  |" + "".join(row) + "|\n")
    stdscr.addstr("  +" + "一" * w + "+\n")
    stdscr.refresh()

def spawn():
    global current, p_x, p_y, r
    current = random.choice(items)
    r = 0
    p_x = w // 2 - len(current[r % len(current)][0]) // 2
    p_y = 0
    if not check():
        raise Exception("Game Over!")

def check(dx=0, dy=0, rot=None):
    if rot is None:
        rot = r
    for y, row in enumerate(current[rot]):
        for x, cell in enumerate(row):
            if cell == '＃':
                gx = p_x + dx + x
                gy = p_y + dy + y
                if gx < 0 or gx >= w or gy < 0 or gy >= h:
                    return False
                if grid[gy][gx] == '＃':
                    return False
    return True

def freeze():
    for y, row in enumerate(current[r % len(current)]):
        for x, cell in enumerate(row):
            if cell == '＃':
                gx = p_x + x
                gy = p_y + y
                grid[gy][gx] = '＃'
    clearLine()

def clearLine():
    global grid
    new_grid = [row for row in grid if any(cell == '  ' for cell in row)]
    cleared = h - len(new_grid)
    for _ in range(cleared):
        new_grid.insert(0, ["  "] * w)
    grid = new_grid

def main(stdscr):
    global p_x, p_y, r
    curses.curs_set(0)
    stdscr.nodelay(True)
    stdscr.timeout(500)

    spawn()
    while True:
        draw(stdscr)

        key = stdscr.getch()
        if key == ord('q'):
            break
        elif key == ord('a') and check(dx=-1):
            p_x -= 1
        elif key == ord('d') and check(dx=1):
            p_x += 1
        elif key == ord('s') and check(dy=1):
            p_y += 1
        elif key == ord('w'):
            new_rot = (r + 1) % len(current)
            if check(rot=new_rot):
                r = new_rot
        
        if check(dy=1):
            p_y += 1
        else:
            freeze()
            try:
                spawn()
            except:
                draw(stdscr)
                stdscr.getch()
                break

curses.wrapper(main)
