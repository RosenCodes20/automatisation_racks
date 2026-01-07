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

def add_racks(all_racks, racks, counter, occupied_cells, letter):
    for _, row in all_racks.iterrows():
        if type(row['Код']) == str and row['Код'].startswith("W") and row['Код'].split('-')[1][0] == letter:
            racks.append({
                    "cell_code": row["Код"],
                    "status": "заета" if row['Код'] in occupied_cells else "свободна",
                    "counter": counter,
                    "rack_id": row['Код'].split('-')[1],
                    "main_letter": letter
                })

            counter += 1

    return counter

def racks_logic(request):
    df = load_all_racks("racks.xlsx", "Код клетка")
    all_racks = load_all_racks("all_racks.xlsx", "Код")

    occupied_cells = set(df["Код клетка"].dropna())

    a_racks = []
    b_racks = []
    c_racks = []
    d_racks = []
    e_racks = []
    f_racks = []


    counter = 1

    counter = add_racks(all_racks, a_racks, counter, occupied_cells, "A")
    counter = add_racks(all_racks, b_racks, counter, occupied_cells, "B")
    counter = add_racks(all_racks, c_racks, counter, occupied_cells, "C")
    counter = add_racks(all_racks, d_racks, counter, occupied_cells, "D")
    counter = add_racks(all_racks, e_racks, counter, occupied_cells, "E")
    counter = add_racks(all_racks, f_racks, counter, occupied_cells, "F")

    context = {
        "rack_groups": {
            "A": a_racks,
            "B": b_racks,
            "C": c_racks,
            "D": d_racks,
            "E": e_racks,
            "F": f_racks,
        },
        'counter': counter,
    }

    return render(request, "index.html", context)
