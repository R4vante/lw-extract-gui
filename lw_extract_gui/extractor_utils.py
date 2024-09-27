import shutil

import pandas as pd
import xlwings as xw
from xlwings.main import App, Book, Sheet


def excel_to_df(file: str) -> pd.DataFrame:
    """Convert an excel, csv or txt file into a pandas DataFrame.

    Args:
        file (str): path to the file

    Returns:
        pd.DataFrame: dataframe containing the data

    """
    if file.endswith(".csv") | file.endswith(".txt"):
        df = pd.read_csv(file, header=1, sep="\t", nrows=24, decimal=",")
    else:
        df = pd.read_excel(file, header=2, nrows=24)

    return drop_unnamed_cols(df)


def drop_unnamed_cols(df: pd.DataFrame) -> pd.DataFrame:
    """Drop columns if they are unnamed.

    Args:
        df (pd.DataFrame): dataframe to drop columns from

    Returns:
        pd.DataFrame: exported dataframe with dropped columns

    """
    unnamed_cols = [col for col in df.columns if "Unnamed" in col]
    return df.drop(columns=unnamed_cols)


def create_xw_workbook(output_file: str) -> tuple[App, Book, Sheet]:
    """Create an Xlwings workbook.

    Args:
        output_file (str): path to save

    Returns:
        _type_: _description_

    """
    shutil.copy("data/template.xlsm", output_file)

    app = xw.App(visible=False)

    wb = app.books.open(output_file)

    return app, wb, wb.sheets["Invoer"]


def exit_xw_workbook(app: App, wb: Book, save: bool) -> None:
    """Close the Xlwings workbook.

    Args:
        app (xw.App): App
        wb (xw.App.wb): Workbook
        save (bool): save state (True or False)

    """
    if save:
        wb.save()
    wb.close()
    app.quit()
