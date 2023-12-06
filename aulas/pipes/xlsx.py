import json

from pandas import ExcelFile
from unidecode import unidecode

from aulas.pipes.excel_parser import ExcelParser, clean
from aulas.pipes.freetime import extract_uptime_downtime
from aulas.util.files.inout import file
from aulas.util.structs import lista
from aulas.util.structs.time import TimeRange


def export_dataframes(dfs, folder='./output/dataframes/'):
    for dia, df in dfs.items():
        with open(file(f'{folder}{dia}.dataframe.json'), 'w', encoding='utf-8') as f:
            df.to_json(f, force_ascii=False, indent=3)


def export_timetables(dfs, folder='./output/timetables/'):
    for aula, df in dfs.items():
        df, filename = dfs[aula], aula
        with open(file(f'{folder}{filename}.timetable.json'), 'w') as f:
            json.dump(fp=f,
                      obj=extract_uptime_downtime(df),
                      cls=TimeRange.CustomEncoder,
                      indent=3)


def convert_from_excel(excel_filename: str, outfolder='./resources/'):
    filename = outfolder + excel_filename
    excel = ExcelFile(filename)
    parse = ExcelParser.get(excel)
    dfs = {nombre: df for nombre, df in
            lista(excel.sheet_names)
                .map(str)  # (Optional: Type-Safety) Convert all sheet names to str (int|str -> str)
                .zip_maps(clean, parse)  # Clean names and parse worksheets
           }

    # for x in tuple({lista(df.columns) for (_, df) in dfs.items()}): print(x)

    export_dataframes(dfs, folder='./resources/dataframes/')
    export_timetables(dfs, folder='./resources/timetables/')
