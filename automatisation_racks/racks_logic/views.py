import os

from django.shortcuts import render
import pandas as pd
# Create your views here.

def load_all_racks(file_name, message):
    file_path = file_name

    df_raw = pd.read_excel(file_path, header=None)

    header_row = df_raw.index[
        df_raw.astype(str).apply(
            lambda row: row.str.contains(message, na=False).any(),
            axis=1
        )
    ][0]

    df = pd.read_excel(file_path, header=header_row)
    df.columns = df.columns.str.strip()

    return df

def racks_logic(request):
    df = load_all_racks("racks.xlsx", "Код клетка")
    all_racks = load_all_racks("all_racks.xlsx", "Код")

    occupied_cells = set(df["Код клетка"].dropna())

    racks = []

    counter = 1

    for _, row in all_racks.iterrows():
            if type(row['Код']) == str and row['Код'].startswith("W"):
                racks.append({
                    "cell_code": row["Код"],
                    "status": "заета" if row['Код'] in occupied_cells else "свободна",
                    "counter": counter,
                })

                counter += 1

    context = {
        'racks': racks,
        'counter': counter,
    }

    return render(request, "index.html", context)
