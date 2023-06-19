import json
import curses
import subprocess

file = open('./items.json').read()
items = json.loads(file)


def format_item(item, secure=True):
    """Extract the attributes if an item as a tuple"""

    attributes = None
    item_name = item.get('name')
    if item.get('login') is not None:
        if secure:
            attributes = ('login', item_name)
        else:
            username = item.get('login').get('username')
            password = item.get('login').get('password')
            attributes = ('login', item_name, username, password)
    else:
        attributes = ('note?', item_name)

    return attributes


def set_row_style(default, row_index, current_item):
    """Change the style of the row if the conditions are true"""

    if row_index == current_item:
        default[0] = curses.A_REVERSE


def set_column_stye(default, row_index, col_index, current_item, attr):
    """Change the style of the column if the conditions are true"""

    if col_index == 0 and row_index is not current_item:
        if attr == 'login':
            default[0] = curses.color_pair(1)
        else:
            default[0] = curses.color_pair(2)


def display_items(stdscr, items, current_item, fixed_widths):
    """Display  the attributes if an item as a tuple"""

    space_between = 4

    for row_index, item in enumerate(items):

        attributes = format_item(item)
        x = 0

        fixed = ""
        for col_index, attr in enumerate(attributes):
            offset = fixed_widths[col_index]
            fixed = f"{attr:<{offset}}" + (" " * space_between)

            style = [curses.A_NORMAL]
            set_row_style(style, row_index, current_item)
            set_column_stye(style, row_index, col_index, current_item, attr)

            stdscr.addstr(row_index, x, fixed, style[0])
            x += offset + space_between


def calculate_columns_width(items):
    """Given a matrix of strings (item atributes), obtains the wider columns of every row on the matrix.
    Group them together, so that it can be used to create a table with enough space for every item.
    """

    largest_row = max([len(format_item(item)) for item in items])
    fixed_widths = [0] * largest_row

    # Every width of every item
    widths = [[len(attr) for attr in format_item(item)] for item in items]

    for row in widths:

        for i, col in enumerate(row):
            if col > fixed_widths[i]:
                fixed_widths[i] = col

    return fixed_widths


def select_from_menu(stdscr, fixed_widths):
    """Print, select in the menu"""

    current_item = 0
    while True:
        stdscr.clear()
        display_items(stdscr, items, current_item, fixed_widths)
        key = stdscr.getch()

        current_item_string = format_item(items[current_item], secure=False)

        if key == curses.KEY_UP:
            current_item = (current_item - 1) % len(items)
        elif key == curses.KEY_DOWN:
            current_item = (current_item + 1) % len(items)
        elif key == ord('\n'):
            return current_item_string


def init_menu(stdscr):
    """Initializes the configuration"""

    # Initial Settings
    curses.curs_set(0)
    curses.start_color()
    curses.use_default_colors()
    curses.init_pair(1, 128, curses.COLOR_BLACK)
    curses.init_pair(2, 84, curses.COLOR_BLACK)

    fixed_widths = calculate_columns_width(items)
    return select_from_menu(stdscr, fixed_widths)

    stdscr.clear()
    stdscr.refresh()
    curses.napms(0)


def string_to_clipboard(string):
    command = ['xclip', '-sel', 'clip']
    subprocess.run(command, input=string, check=True)
    print('Copied to the clipboard!')


def main():
    selected = curses.wrapper(init_menu)
    password = selected[-1].encode('utf-8')
    string_to_clipboard(password)


if __name__ == "__main__":
    main()
