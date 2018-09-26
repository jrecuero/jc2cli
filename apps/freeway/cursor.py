class Cursor:

    ESC = '\x1b'

    @staticmethod
    def print(seq):
        print(seq, end='', flush=True)

    @staticmethod
    def escape(_format, *args):
        return '{0}{1}'.format(Cursor.ESC, _format.format(*args))

    @staticmethod
    def show():
        '''show returns ANSI escape sequence to show the cursor.
        '''
        return Cursor.escape("[?25h")

    @staticmethod
    def hide():
        '''Hide returns ANSI escape sequence to hide the cursor
        '''
        return Cursor.escape("[?25l")

    @staticmethod
    def move_to(line, col):
        '''MoveTo returns ANSI escape sequence to move cursor to specified
        position on screen.
        '''
        return Cursor.escape("[{};{}H", line, col)

    @staticmethod
    def move_up(n):
        '''MoveUp returns ANSI escape sequence to move cursor up n lines.
        '''
        return Cursor.escape("[{}A", n)

    @staticmethod
    def move_down(n):
        '''MoveDown returns ANSI escape sequence to move cursor down n lines.
        '''
        return Cursor.escape("[{}B", n)

    @staticmethod
    def move_right(n):
        '''MoveRight returns ANSI escape sequence to move cursor right
        n columns.
        '''
        return Cursor.escape("[{}C", n)

    @staticmethod
    def move_left(n):
        '''MoveLeft returns ANSI escape sequence to move cursor left
        n columns.
        '''
        return Cursor.escape("[{}D", n)

    @staticmethod
    def move_upper_left(n):
        '''move_upper_left returns ANSI escape sequence to move cursor to
        upper left corner of screen.
        '''
        return Cursor.escape("[{}H", n)

    @staticmethod
    def move_next_line():
        '''move_next_line returns ANSI escape sequence to move cursor to next
        line.
        '''
        return Cursor.escape("E")

    @staticmethod
    def clear_line_right():
        '''clear_line_right returns ANSI escape sequence to clear line from
        right of the cursor.
        '''
        return Cursor.escape("[0K")

    @staticmethod
    def clear_line_left():
        '''clear_line_left returns ANSI escape sequence to clear line from
        left of the cursor.
        '''
        return Cursor.escape("[1K")

    @staticmethod
    def clear_entire_line():
        '''clear_entire_line returns ANSI escape sequence to clear current
        line.
        '''
        return Cursor.escape("[2K")

    @staticmethod
    def clear_screen_down():
        ''' clear_screen_down returns ANSI escape sequence to clear screen
        below the cursor.
        '''
        return Cursor.escape("[0J")

    @staticmethod
    def clear_screen_up():
        '''clear_screen_up returns ANSI escape sequence to clear screen above
        the cursor.
        '''
        return Cursor.escape("[1J")

    @staticmethod
    def clear_entire_screen():
        '''clear_entire_screen returns ANSI escape sequence to clear the
        screen.
        '''
        return Cursor.escape("[2J")

    @staticmethod
    def save_attributes():
        '''save_attributes returns ANSI escape sequence to save current
        position and attributes of the cursor.
        '''
        return Cursor.escape("7")

    @staticmethod
    def restore_attributes():
        '''restore_attributes returns ANSI escape sequence to restore saved
        position and attributes of the cursor.
        '''
        return Cursor.escape("8")

    @staticmethod
    def reset():
        return Cursor.escape('[0m')

    @staticmethod
    def bold_on():
        return Cursor.escape('[1m')

    @staticmethod
    def italics_on():
        return Cursor.escape('[3m')

    @staticmethod
    def underline_on():
        return Cursor.escape('[4m')

    @staticmethod
    def inverse_on():
        return Cursor.escape('[7m')

    @staticmethod
    def strike_through_on():
        return Cursor.escape('[9m')

    @staticmethod
    def bold_off():
        return Cursor.escape('[22m')

    @staticmethod
    def italics_off():
        return Cursor.escape('[23m')

    @staticmethod
    def underline_off():
        return Cursor.escape('[24m')

    @staticmethod
    def underline_off():
        return Cursor.escape('[27m')

    @staticmethod
    def strike_through_off():
        return Cursor.escape('[29m')

    @staticmethod
    def fg_red():
        return Cursor.escape('[31m')

    @staticmethod
    def fg_green():
        return Cursor.escape('[32m')

    @staticmethod
    def fg_yellow():
        return Cursor.escape('[33m')

    @staticmethod
    def fg_blue():
        return Cursor.escape('[34m')

    @staticmethod
    def fg_magenta():
        return Cursor.escape('[35m')

    @staticmethod
    def fg_cyan():
        return Cursor.escape('[36m')

    @staticmethod
    def fg_white():
        return Cursor.escape('[37m')

    @staticmethod
    def fg_default():
        return Cursor.escape('[39m')

    @staticmethod
    def fg_black():
        return Cursor.escape('[40m')

    @staticmethod
    def bg_red():
        return Cursor.escape('[41m')

    @staticmethod
    def bg_green():
        return Cursor.escape('[42m')

    @staticmethod
    def bg_yellow():
        return Cursor.escape('[43m')

    @staticmethod
    def bg_blue():
        return Cursor.escape('[44m')

    @staticmethod
    def bg_magenta():
        return Cursor.escape('[45m')

    @staticmethod
    def bg_cyan():
        return Cursor.escape('[46m')

    @staticmethod
    def bg_white():
        return Cursor.escape('[47m')

    @staticmethod
    def bg_default():
        return Cursor.escape('[49m')
