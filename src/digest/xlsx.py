from pandas import ExcelFile
from unidecode import unidecode

from src.util.oututils import export_uptime_downtime, file
from src.util.prutils import ExcelParser

from src.util.lista import *


def clean(x: str) -> str:
    return unidecode(x).replace(' ', '-').lower()


def export_dataframes(dfs):
    for dia, df in dfs.items():
        with open(file(f'./output/dataframes/{dia}.dataframe.json'), 'w', encoding='utf-8') as f:
            df.to_json(f, force_ascii=False, indent=3)


def export_timetables(dfs):
    for aula, df in dfs.items():
        export_uptime_downtime(dfs[aula], aula)


def convert_from_excel(excel_filename: str):
    filename = 'resources/' + excel_filename
    excel = ExcelFile(filename)
    parse = ExcelParser.get(excel)
    dfs = {nombre: df for nombre, df in
           lista(excel.sheet_names)
           .map(str)  # (Optional: Type-Safety) Convert all sheet names to str (int|str -> str)
           .zip_maps(clean, parse)  # Clean names and parse worksheets
           }

    #for x in tuple({lista(df.columns) for (_, df) in dfs.items()}): print(x)

    export_dataframes(dfs)
    export_timetables(dfs)
