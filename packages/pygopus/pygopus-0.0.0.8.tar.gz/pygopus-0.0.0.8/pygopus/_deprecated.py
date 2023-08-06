# class RowContainer(UserList):
#     _pid: int
#     sheet_name: str

#     def info(self, sheet_name: str, pid):
#         self.sheet_name = sheet_name
#         self._pid = pid
#         return self

#     def _set_operation(
#         self,
#         type: Literal["inter", "diff"],
#         other,
#         look_at: Union[int, Tuple[int, int]],
#     ):
#         self_look_at: int
#         other_look_at: int
#         self_match_col = []
#         other_match_col = []

#         if isinstance(look_at, int):
#             self_match_col = [d[look_at] for d in self.data]
#             other_match_col = [d[look_at] for d in other.data]
#             self_map = {f"{d.row_axis}-{d[look_at]}": d for d in self.data}
#         if isinstance(look_at, tuple):
#             self_look_at, other_look_at = look_at
#             self_match_col = [d[self_look_at] for d in self.data]
#             other_match_col = [d[other_look_at] for d in other.data]
#             self_map = {f"{d.row_axis}-{d[self_look_at]}": d for d in self.data}

#         assert isinstance(self_map, dict)

#         set_operation_res: set = set()
#         if type == "inter":
#             set_operation_res = set(self_match_col).intersection(set(other_match_col))

#         if type == "diff":
#             set_operation_res = set(self_match_col).difference(set(other_match_col))
#         _res = []
#         for i in set_operation_res:
#             for item in self_map.items():
#                 k, v = item
#                 assert isinstance(k, str)
#                 suffix = k.split("-")[-1]
#                 if str(i) == suffix:
#                     _res.append(v)
#         return _res

#     def intersection(self, other, look_at):
#         return self._set_operation(
#             type="inter",
#             other=other,
#             look_at=look_at,
#         )

#     def difference(self, other, look_at):
#         return self._set_operation(
#             type="diff",
#             other=other,
#             look_at=look_at,
#         )

# def highlight(self, color="#FEF9B0", at: int = None):

#     color = [color]
#     targets = self.get_cell_axis()
#     # targets = [f"{int_to_colname(i+1)}{self.row_axis}" for i, d in enumerate(self.data)]
#     # this should work(well it do works)
#     # the line top here will be changed in future for a header caused data offset

#     if at != None:
#         # targets = [f"{int_to_colname(at+1)}{self.row_axis}"]
#         targets = [self.get_cell_axis()[at]]
#         res = HighLight(
#             pid=self._pid,
#             sheet_name=self.sheet_name,
#             tar_type="cell",
#             targets=targets,
#             color=color,
#         ).post()
#         return res

#     res = HighLight(
#         pid=self._pid,
#         sheet_name=self.sheet_name,
#         tar_type="row",
#         targets=targets,
#         color=color,
#     ).post()

#     return res


# if isinstance(look_at, int):
#     self_match_col = [d[look_at] for d in self.data]
#     other_match_col = [d[look_at] for d in other.data]
#     self_map = {f"{d.axis_pos[1]}-{d[look_at]}": d for d in self.data}
# if isinstance(look_at, tuple):
#     self_look_at, other_look_at = look_at
#     self_match_col = [d[self_look_at] for d in self.data]
#     other_match_col = [d[other_look_at] for d in other.data]
#     self_map = {f"{d.axis_pos[1]}-{d[self_look_at]}": d for d in self.data}


# from typing import Callable, Union
# from pygopus.core import Sheet
# from pygopus.models import _RowContainer


# class Stat:
#     def __init__(
#         self,
#         object: Union[Sheet, _RowContainer],
#         colname: str,
#         bind: str = None,
#         filter: Callable = None,
#     ) -> None:
#         self.data = self._get_data(object=object)
#         self._colname = colname
#         self._filter = filter if filter else lambda x: x
#         self._bind = bind
#         self._vals = []

#         self._calc()

#     def _get_data(self, object: Union[Sheet, _RowContainer]):
#         if isinstance(object, Sheet):
#             return object.rows
#         if isinstance(object, _RowContainer):
#             return object
#         else:
#             raise ValueError(f"{type(object)} is unsupported type")

#     def _calc(self):
#         from .utils import colname_to_index

#         col_index = colname_to_index(self._colname)

#         for row in self.data:
#             try:
#                 row = self._filter(row)
#                 if row:
#                     val = row[col_index]
#                     if self._bind:
#                         bd_col = colname_to_index(self._bind)
#                         bd_val = row[bd_col]
#                         self._vals.append((val, bd_val))
#                         continue
#                     self._vals.append(val)

#             except IndexError:
#                 continue

#     def dict(self):
#         raise NotImplementedError


# class Count(Stat):
#     def __init__(
#         self,
#         object: Union[Sheet, _RowContainer],
#         colname: str,
#         filter: Callable = None,
#     ) -> None:
#         super().__init__(object, colname, None, filter)

#     def dict(self):
#         return {e: self._vals.count(e) for e in set(self._vals)}


# class DateCount(Stat):
#     def __init__(
#         self,
#         object: Union[Sheet, _RowContainer],
#         colname: str,
#         keyfmt: str = "%Y-%m-%d",
#         filter: Callable = None,
#     ) -> None:
#         super().__init__(object, colname, None, filter)
#         self.fmt = keyfmt

#     def by_date(self):
#         self.fmt = "%Y-%m-%d"

#     def by_month(self):
#         self.fmt = "%Y-%m"

#     def by_year(self):
#         self.fmt = "%Y"

#     def dict(self):
#         from dateutil import parser

#         vals = [parser.parse(d).strftime(self.fmt) for d in self._vals]

#         return {d: vals.count(d) for d in set(vals)}


# class Sum(Stat):
#     def __init__(
#         self,
#         object: Union[Sheet, _RowContainer],
#         colname: str,
#         keyfrom: str,
#         filter: Callable = None,
#     ) -> None:
#         super().__init__(object, colname, keyfrom, filter)

#     def dict(self):
#         keys = [key for _, key in self._vals]
#         # print(keys)
#         d = dict.fromkeys(keys, 0.0)

#         for val, key in self._vals:
#             # val, key = item
#             d[key] += float(val)
#         return d


# class DateSum(Sum):
#     ...
