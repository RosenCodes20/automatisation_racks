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

    racks = []

    for _, row in df.iterrows():
        for none, all_racks_row in all_racks.iterrows():
            if row['Код клетка'] == all_racks_row['Код']:
                racks.append({
                    "cell_code": row["Код клетка"],
                    "rack": row["Код клетка"].rsplit("-", 1)[0],
                    "status": "блокирана",
                    "quantity": row["Количество"],
                })
            else:
                racks.append({
                    "cell_code": row["Код клетка"],
                    "rack": row["Код клетка"].rsplit("-", 1)[0],
                    "status": "свободна",
                    "quantity": row["Количество"],
                })

    context = {
        'racks': racks,
    }

    return render(request, "index.html", context)