"""
References:
- https://en.wikipedia.org/wiki/Box-drawing_characters
┌─┬─┐╷╭─┬─╮
├─┼─┤│├─┼─┤╶╴
└─┴─┘╵╰─┴─╯
"""

from typing import Self
from span import Span


class Table:
    def __init__(self, cols: list[Span], header: list[str]):
        self.cols = cols
        self.header = header
        self.validate_state()

    @classmethod
    def from_pairs(cls, *pairs: tuple[str, Span]) -> Self:
        """Creates a new table from pairs of header labels and spans."""
        return cls(
            [col for _, col in pairs],
            [label for label, _ in pairs],
        )

    def validate_state(self) -> None:
        if len(self.cols) == 0:
            raise ValueError("Cannot create table with no columns.")
        if max(map(len, self.cols)) == 0:
            raise ValueError("Cannot create table with no non-empty columns.")
        if len(set(map(len, self.cols))) != 1:
            raise ValueError("All columns must be the same length.")
        if len(self.header) != len(self.cols):
            raise ValueError(
                "Number of header labels must match number of columns."
            )

    
    def __repr__(self) -> str:
        """Prints the table in a box-drawing style.

        Example:
        ┏━━━┯━━━┯━━━┓
        ┃ A │ B │ C ┃
        ┣━━━┿━━━┿━━━┫
        ┃ 1 │ 2 │ 3 ┃
        ┠───┼───┼───┨
        ┃ 4 │ 5 │ 6 ┃
        ┗━━━┷━━━┷━━━┛
        """
        self.validate_state()
        col_str_sets = [list(map(str, col)) for col in self.cols]
        row_str_sets = list(zip(*col_str_sets))
        col_widths = [
            max(max(map(len, col_strs)), len(label))
            for col_strs, label in zip(col_str_sets, self.header)
        ]
        top_row = (
            "┏" + "┯".join("━"*(max_len+2) for max_len in col_widths) + "┓\n"
        )
        header_row_delim = (
            "┣" + "┿".join("━"*(max_len+2) for max_len in col_widths) + "┫\n"
        )
        row_delim = (
            "┠" + "┼".join("─"*(max_len+2) for max_len in col_widths) + "┨\n"
         )
        bottom_row = (
            "┗" + "┷".join("━"*(max_len+2) for max_len in col_widths) + "┛"
        )
        s = top_row
        formatted_label_strs = (
            label.center(col_width)
            for label, col_width in zip(self.header, col_widths)
        )
        s += "┃ " + " │ ".join(formatted_label_strs) + " ┃\n"
        s += header_row_delim
        for i, row_strs in enumerate(row_str_sets):
            if i != 0:
                s += row_delim
            formatted_row_strs = (
                val_str.rjust(col_width)
                for val_str, col_width in zip(row_strs, col_widths)
            )
            s += "┃ " + " │ ".join(formatted_row_strs) + " ┃\n"
        s += bottom_row
        return s

    def __str__(self) -> str:
        return repr(self)


if __name__ == "__main__":
    tb = Table.from_pairs(
        ("Year", Span([1, 2, 3])),
        ("Cash Flow", Span([4, 5, 6]).as_currency()),
        ("idk", Span([7, 8, 9]).as_percent()),
    )
    print(tb)
