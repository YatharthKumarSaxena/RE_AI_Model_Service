import os
import pandas as pd


# ============================================================
# SPREADSHEET PARSER
# ============================================================

def parse_spreadsheet(file_path, extension):

    try:

        # ----------------------------------------------------
        # READ SPREADSHEET
        # ----------------------------------------------------

        extension = extension.lower()

        if extension == ".csv":

            dataframe = pd.read_csv(
                file_path,
                dtype=object
            )

        elif extension in [".xls", ".xlsx"]:

            dataframe = pd.read_excel(
                file_path,
                dtype=object
            )

        else:

            return {
                "success": False,
                "reason": (
                    f"Unsupported file format '{extension}'."
                )
            }

        # ----------------------------------------------------
        # EMPTY FILE CHECK
        # ----------------------------------------------------

        if dataframe.empty and len(dataframe.columns) == 0:

            return {
                "success": False,
                "reason": "The uploaded file is empty."
            }

        # ----------------------------------------------------
        # HEADERS
        # ----------------------------------------------------

        headers = [
            str(column).strip()
            if column is not None
            else ""
            for column in dataframe.columns
        ]

        # ----------------------------------------------------
        # INVALID HEADER CHECK
        # ----------------------------------------------------

        if (
            len(headers) == 0
            or all(header == "" for header in headers)
        ):

            return {
                "success": False,
                "reason": "Invalid spreadsheet format."
            }

        # ----------------------------------------------------
        # CLEAN ROWS
        # ----------------------------------------------------

        rows = []

        for _, row in dataframe.iterrows():

            row_values = row.tolist()

            # Check whether row contains any actual value
            has_value = any(
                pd.notna(cell) and str(cell) != ""
                for cell in row_values
            )

            if not has_value:
                continue

            row_object = {}

            for index, header in enumerate(headers):

                value = (
                    row_values[index]
                    if index < len(row_values)
                    else ""
                )

                # Convert NaN → ""
                if pd.isna(value):
                    value = ""

                row_object[header] = value

            rows.append(row_object)

        # ----------------------------------------------------
        # SHEET NAME
        # ----------------------------------------------------

        sheet_name = None

        if extension in [".xls", ".xlsx"]:

            excel_file = pd.ExcelFile(
                file_path
            )

            if not excel_file.sheet_names:

                return {
                    "success": False,
                    "reason": (
                        "The uploaded file contains "
                        "no worksheets."
                    )
                }

            sheet_name = excel_file.sheet_names[0]

        else:

            # CSV does not have worksheets
            sheet_name = None

        # ----------------------------------------------------
        # SUCCESS
        # ----------------------------------------------------

        return {
            "success": True,
            "parser": "Spreadsheet Parser",
            "data": {
                "headers": headers,
                "rows": rows,
                "sheetName": sheet_name
            }
        }

    except Exception as error:

        return {
            "success": False,
            "reason": str(error)
        }


# ============================================================
# PARSER CONFIGURATION
# ============================================================

spreadsheet_parser = {
    "name": "Spreadsheet Parser",

    "supported_extensions": [
        ".csv",
        ".xls",
        ".xlsx"
    ],

    "parse": parse_spreadsheet
}