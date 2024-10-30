from typing import overload, TypeVar, Callable
from pathlib import Path
from csv import reader as csv_reader
from utils import range_slice_to_int

class AbstractData:
  def __init__(self, path: Path | str):
    self._path = Path(path)
    self.__csv_reader = csv_reader(open(self._path, "r"))
    self._columns = next(self.__csv_reader)
    self.__data: list[list[str]] = []
    self.__len_lines = 0
    self.__is_stop_iteration_lines = False

  def _get_index_column(self, column: str):
    try:
      return self._columns.index(column)
    except ValueError:
      raise ValueError(f"Nombre de columna '{column}' no encontrado en el archivo: {self._path.name}")
  
  def _get_lines(self, lines: slice):
    lines: int = range_slice_to_int(lines)
    if lines < 0: lines = 0
    
    if self.__len_lines < lines and not self.__is_stop_iteration_lines:
      for _ in range(lines - self.__len_lines):
        try:
          self.__data.append(next(self.__csv_reader))
        except StopIteration:
          self.__is_stop_iteration_lines = True
          break

      self.__len_lines = len(self.__data)
    return self.__data

  def _get_rows(self, lines: slice, column: str) -> list[str]:
    try:
      index_column = self._get_index_column(column)
      data_lines = self._get_lines(lines)
    except ValueError:
      return []
    except KeyError:
      lines = self.__len_lines - 1
      data_lines = self.__data

    return [data_line[index_column] for data_line in data_lines[lines]]

  
T = TypeVar("T")

class DataRows:
  def __init__(self, data: AbstractData, column: str):
    self.__data = data
    self.__column = column


  @overload
  def rows(self, line: int = 1) -> str | None: pass
  @overload
  def rows(self, lines: slice) -> list[str]:  pass
  def rows(self, lines: slice | int):
    if (isOneRow := not type(lines) is slice):
      if lines < 1: lines = 1
      lines: slice = slice(lines)
    rows = self.__data._get_rows(lines, self.__column)

    if isOneRow:
      len_rows = len(rows)
      if len_rows == 0 or len_rows < lines.stop: return
      return rows[-1]
    return rows

  @property
  def row(self):
    return self.rows(1)
  
  def __repr__(self):
    return str(self.row)
  
  def __str__(self):
    return self.__repr__()
  
  def __getitem__(self, lines: slice | int) -> str | None | list[str]:
    if type(lines) is int: lines += 1
    return self.rows(lines)
  

  @overload
  def rows_cast_to_type(self, line: int, func_cast_to_type: Callable[[str], T] = str) -> T | None: pass
  @overload
  def rows_cast_to_type(self, lines: slice, func_cast_to_type: Callable[[str], T] = str) -> list[T]: pass
  def rows_cast_to_type(self, lines: slice | int, func_cast_to_type: Callable[[str], T] = str):
    rows = self.rows(lines)
    if rows is None: return
    if (isOneRow := type(rows) is str):
      rows: list[str] = [rows]
    
    try:
      rows_cast = list(map(func_cast_to_type, rows))
      return rows_cast[0] if isOneRow else rows_cast
    except:
      return None if isOneRow else []

