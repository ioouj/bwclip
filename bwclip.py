import sys
import json
import curses
import subprocess

from selector import ItemSelector


def format_item(item):
    """Extract the attributes if an item as a tuple"""

    attributes = None
    item_name = item.get('name')
    if item.get('login') is not None:
        username = item.get('login').get('username')
        password = item.get('login').get('password')
        return ('login', item_name, username, password)

    return ('note?', item_name)


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

        x = 0

        fixed = ""
        for col_index, attr in enumerate(item[0:2]):
            offset = fixed_widths[col_index]
            fixed = f"{attr:<{offset}}" + (" " * space_between)

            style = [curses.A_NORMAL]
            set_row_style(style, row_index, current_item)
            set_column_stye(style, row_index, col_index, current_item, attr)

            stdscr.addstr(row_index + 1, x, fixed, style[0])
            x += offset + space_between


def string_to_clipboard(string):
    """Uses xclip to copy a string"""

    command = ['xclip', '-sel', 'clip']
    subprocess.run(command, input=string, check=True)
    print('Copied to the clipboard!')


def calculate_columns_width(items):
    """Given a matrix of strings (item atributes), obtains the wider columns of every row on the matrix.
    Group them together, so that it can be used to create a table with enough space for every item.
    """

    largest_row = max([len(item) for item in items])
    fixed_widths = [0] * largest_row

    # Every width of every item
    widths = [[len(attr) for attr in item] for item in items]

    for row in widths:

        for i, col in enumerate(row):
            if col > fixed_widths[i]:
                fixed_widths[i] = col

    return fixed_widths


def main():
    """Wraps the initialization of curses and input validation"""

    items = None

    if len(sys.argv) > 1:
        try:
            data = sys.argv[1]
            items = json.loads(data)
            items = [format_item(item) for item in items]
        except json.JSONDecodeError as e:
            print("Bad JSON format: ", e)

    def init_menu(stdscr):
        """Initializes the configuration"""

        # Initial Settings
        curses.curs_set(0)
        curses.start_color()
        curses.use_default_colors()
        curses.init_pair(1, 128, curses.COLOR_BLACK)
        curses.init_pair(2, 84, curses.COLOR_BLACK)
        curses.init_pair(3, curses.COLOR_RED, curses.COLOR_BLACK)

        fixed_widths = calculate_columns_width(items)

        selector = ItemSelector(stdscr, fixed_widths, items)
        return selector.selection_loop(display_items)

        stdscr.clear()
        stdscr.refresh()
        curses.napms(0)

    if items is not None:
        selected = curses.wrapper(init_menu)
        password = selected[-1].encode('utf-8')
        string_to_clipboard(password)


if __name__ == "__main__":
    main()

    pass
