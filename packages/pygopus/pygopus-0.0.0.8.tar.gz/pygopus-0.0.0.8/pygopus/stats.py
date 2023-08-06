from ssl import OP_ENABLE_MIDDLEBOX_COMPAT
from typing import Callable, Union
from pygopus.core import Sheet
from pygopus.models import _RowContainer


class Stat:
    def __init__(
        self,
        object: Union[Sheet, _RowContainer],
        colname: str,
        filter: Callable = None,
    ) -> None:
        self.data = self._get_data(object=object)
        self._colname = colname
        self._filter = filter if filter else lambda x: x
        self._vals = []

        self._calc()

    def _get_data(self, object: Union[Sheet, _RowContainer]):
        if isinstance(object, Sheet):
            return object.rows
        if isinstance(object, _RowContainer):
            return object
        else:
            raise ValueError(f"{type(object)} is unsupported type")

    def _calc(self):
        from .utils import colname_to_index

        col_index = colname_to_index(self._colname)

        for row in self.data:
            try:
                row = self._filter(row)
                if row:
                    val = row[col_index]
                    self._vals.append(val)

            except IndexError:
                continue

    def __str__(self) -> str:
        return str(self.dict())

    def dict(self):
        raise NotImplementedError


class Count(Stat):
    def __init__(
        self,
        object: Union[Sheet, _RowContainer],
        colname: str,
        filter: Callable = None,
    ) -> None:
        super().__init__(object, colname, filter)

    def dict(self):
        return {e: self._vals.count(e) for e in set(self._vals)}


class DateCount(Stat):
    def __init__(
        self,
        object: Union[Sheet, _RowContainer],
        colname: str,
        keyfmt: str = "%Y-%m-%d",
        filter: Callable = None,
    ) -> None:
        super().__init__(object, colname, filter)
        self.fmt = keyfmt

    def by_date(self):
        self.fmt = "%Y-%m-%d"

    def by_month(self):
        self.fmt = "%Y-%m"

    def by_year(self):
        self.fmt = "%Y"

    def by_quarter(self):
        self.fmt = "Q"

    def dict(self):
        from dateutil import parser

        quarter_map = {
            "01": 1,
            "02": 1,
            "03": 1,
            "04": 2,
            "05": 2,
            "06": 2,
            "07": 3,
            "08": 3,
            "09": 3,
            "10": 4,
            "11": 4,
            "12": 4,
        }

        if self.fmt == "Q":
            vals = [parser.parse(d).strftime("%Y-%m") for d in self._vals]

            quarter = {}
            for k in vals:
                y, m = k.split("-")
                if not quarter.get(y):
                    for i in "1234":
                        quarter[y + f"-Q{i}"] = 0
            for k in vals:
                y, m = k.split("-")
                q = f"{y}-Q{quarter_map[m]}"

                quarter[q] += 1
            return quarter

        vals = [parser.parse(d).strftime(self.fmt) for d in self._vals]

        return {d: vals.count(d) for d in set(vals)}


class Sum(Stat):
    def __init__(
        self,
        object: Union[Sheet, _RowContainer],
        colname: str,
        keyfrom: str,
        filter: Callable = None,
    ) -> None:
        super().__init__(object, colname, filter)
        self._keyfrom = keyfrom

    def _get_bind(self):
        from .utils import colname_to_index

        _bd_vals = []

        if self._keyfrom:
            for row in self.data:
                bd_col = colname_to_index(self._keyfrom)
                bd_val = row[bd_col]
                _bd_vals.append(bd_val)
        return _bd_vals

    def dict(self):
        keys = self._get_bind()
        d = dict.fromkeys(keys, 0.0)

        for val, key in zip(self._vals, keys):
            d[key] += float(val)
        return d


class DateSum(Sum):
    def __init__(
        self,
        object: Union[Sheet, _RowContainer],
        colname: str,
        keyfrom: str,
        keyfmt: str = "%Y-%m-%d",
        filter: Callable = None,
    ) -> None:
        self.fmt = keyfmt
        super().__init__(object, colname, keyfrom, filter)

    def by_date(self):
        self.fmt = "%Y-%m-%d"

    def by_month(self):
        self.fmt = "%Y-%m"

    def by_year(self):
        self.fmt = "%Y"

    def dict(self):
        from dateutil.parser import parse

        timekeys = [parse(t) for t in self._get_bind()]

        raw_sum = dict.fromkeys(timekeys, 0.0)
        for val, key in zip(self._vals, timekeys):
            raw_sum[key] += float(val)

        fmt_dict = {}
        # fmt_keys = [t.strftime(self.fmt) for t in timekeys]

        for k, v in raw_sum.items():
            fmt_k = k.strftime(self.fmt)
            if not fmt_dict.get(fmt_k):
                fmt_dict[fmt_k] = 0.0

            fmt_dict[fmt_k] += v
        return fmt_dict
