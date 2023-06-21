import re
import curses


class ItemSelector:
    """Select an option in the menu, changes the state to print it"""

    def __init__(self, stdscr, fixed_widths, items):
        self.stdscr = stdscr
        self.fixed_widths = fixed_widths
        self.items = items
        self.current_item = 0
        self.search = ''
        self.search_style = curses.A_NORMAL
        self.mutable_items = items

    def filter_items(self, items, search):

        def item_match(item):
            return re.search(search, item[1]) is not None

        found = filter(item_match, items)
        return list(found) if found is not None else []

    def selection_loop(self, display_items_callback):

        while True:

            # Print search pattern
            self.stdscr.addstr(0, 0, self.search, self.search_style)

            if self.search != '':
                filter_params = self.items, self.search
                self.mutable_items = self.filter_items(*filter_params)
            else:
                self.mutable_items = self.items

            items_length = len(self.mutable_items)

            if items_length > 0:
                self.current_item = self.current_item % items_length
                display_data = self.mutable_items, self.current_item, self.fixed_widths
                display_items_callback(self.stdscr, *display_data)
                current_item_string = self.mutable_items[self.current_item]

            # Key handling
            key = self.stdscr.getch()
            self.search_style = curses.A_NORMAL
            invalid_keys = ['\\', '[', ']', '*', '(', ')', '|']

            if key == ord('\n') and items_length > 0:
                return current_item_string

            elif key == ord('\n') and items_length == 0:
                self.search_style = curses.color_pair(3)

            elif key == curses.KEY_UP:
                self.current_item -= 1

            elif key == curses.KEY_DOWN:
                self.current_item += 1

            elif key == curses.KEY_BACKSPACE:
                self.search = self.search[0:-1]

            elif invalid_keys.count(chr(key)) == 0:
                self.search += chr(key)

            self.stdscr.clear()
            self.stdscr.refresh()
            curses.napms(0)
