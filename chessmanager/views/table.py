import numpy as np
from termcolor import colored as _c


class Table:
    def __init__(self, body):
        self.head_text_color = "grey"
        self.head_background_color = "on_white"
        self.body = body
        self.string_body = ""
        self.max_char_per_cell = 32
        self.columns = []
        self.string_columns = []
        self.make_string_table()

    def make_string_table(self):
        self.make_columns()
        body = np.array(self.string_columns)
        rows = body.transpose().tolist()
        string_rows = list(map(lambda x: "".join(x) + "|", rows))
        self.string_body = "\n".join(string_rows)
        return self.string_body

    @staticmethod
    def text_to_cell(text, width=0):
        hmany_dots_left = int(width/2)
        dots_left = " " * hmany_dots_left
        dots_right = " " * (width - hmany_dots_left)

        return f"| {dots_left}{text}{dots_right} "

    def make_columns(self):
        body = np.array(self.body)
        self.columns = body.transpose().tolist()
        string_columns = []
        column_count = 0
        for column in self.columns:
            index_none = True
            while index_none:
                try:
                    index_none_value = column.index(None)
                    column[index_none_value] = " "
                except ValueError:
                    index_none = False

            max_width = len(max(column, key=len))
            if max_width > self.max_char_per_cell:
                max_width = self.max_char_per_cell
            string_column = []
            cell_count = 0
            for cell in column:
                offset = self.max_char_per_cell
                if len(cell) > offset:
                    cell = cell[0:(offset - 3)] + "..."
                has_longer = max_width - len(cell)
                cell_string = self.text_to_cell(cell, has_longer)
                if cell_count == 0:
                    if "* " in cell_string:
                        cell_string = cell_string.replace("* ", _c("* ", 'cyan'))
                    cell_string = f"|{_c(cell_string[1:], self.head_text_color, self.head_background_color)}"
                string_column.append(cell_string)
                cell_count += 1
            string_columns.append(string_column)
            column_count += 1

        self.string_columns = string_columns
        return string_columns

    def __str__(self):

        return self.string_body
