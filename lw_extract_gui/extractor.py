from numpy.typing import NDArray

from lw_extract_gui.extractor_utils import create_xw_workbook, excel_to_df, exit_xw_workbook


def calc_t_30_avg(file_path: str) -> NDArray:
    """Calculate average echo in 3rd-octaves.

    Args:
        file_path (str): path to file

    Returns:
        pd.DataFrame: dataframe of calculate averages.

    """
    df_echo = excel_to_df(file_path)
    return df_echo.iloc[:, 1:].mean(axis=1).to_numpy().reshape(-1, 1)


def export_xlsm(output_file: str) -> None:
    """Export sound data, background noise, and T30 to a template Excel file.

    Args:
        output_file (str): file path to save.

    """
    t_avg = calc_t_30_avg("data/T30 [s].txt")
    background = excel_to_df("data/meetdag 2 - achtergrond blower.xlsx")
    sound_data = excel_to_df("data/meetdag 2 - rond toevoer 1.xlsx")

    app, wb, ws = create_xw_workbook(output_file)

    ws.range("D15").value = t_avg
    ws.range("D43").options(index=False, header=False).value = sound_data.iloc[:, 1:]
    ws.range("D72").options(index=False, header=False).value = background.iloc[:, 1:]

    exit_xw_workbook(app, wb, save=False)


def main():
    export_xlsm("data/test.xlsm")


if __name__ == "__main__":
    main()
