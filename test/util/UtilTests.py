import glob
from unittest import TestCase

import pandas
from pandas import ExcelFile, DataFrame, Index
from numpy import nan
from src.util.prutils import drop_nan_cols, dropna_rows, drop_first_row


class UtilTests(TestCase):

    def setUp(self):
        f = ExcelFile('../resources/test.xlsx')
        self.df = f.parse('Hoja 1')

    def step_correct_parsing(self):
        self.assertTrue(self.df.equals(DataFrame({
            'COLUMNA_1': {0: 'columna_1', 1: 'a', 2: 'b', 3: 'c', 4: nan, 5: 'Z', 6: 'a'},
            'COLUMNA_2': {0: 'columna_2', 1: 4, 2: 3, 3: 4, 4: 3, 5: nan, 6: 3},
            'COLUMNA_3': {0: 'columna_3', 1: 456, 2: 123, 3: nan, 4: 10, 5: 74, 6: -210},
            'COLUMNA_4': {0: nan, 1: 'abc', 2: 'gfe', 3: 'sad', 4: 'e2sd', 5: 'wqw', 6: 'abc'}
            }))
        )

    def step_drop_first(self):
        self.df = drop_first_row(self.df)
        new_columns = Index(['columna_1', 'columna_2', 'columna_3', nan])
        self.assertTrue(self.df.columns.equals(new_columns))

    def step_dropna_cols(self):
        self.df = drop_nan_cols(self.df)
        new_columns = Index(['columna_1', 'columna_2', 'columna_3'])
        condition: bool = self.df.columns.equals(new_columns)
        if not condition:
            self.fail(f'{self.df.columns} is not {new_columns}')
        else:
            self.assertTrue(condition)

    def step_dropna_rows(self):
        self.df = dropna_rows(self.df, 'columna_1', 'columna_2', 'columna_3')
        self.assertEqual(self.df.shape, (3, 3))

    def _steps(self):
        for name in dir(self):  # dir() result is implicitly sorted
            if name.startswith("step"):
                yield name, getattr(self, name)

    def test_steps(self):
        for name, step in self._steps():
            try:
                step()
            except Exception as e:
                self.fail(f'{step.__name__} -- {e}')
