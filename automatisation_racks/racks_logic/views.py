import os

from django.shortcuts import render
import pandas as pd
# Create your views here.

def load_all_racks():
    file_path = "racks.xlsx"

    df_raw = pd.read_excel(file_path, header=None)

    header_row = df_raw.index[
        df_raw.astype(str).apply(
            lambda row: row.str.contains("Код клетка", na=False).any(),
            axis=1
        )
    ][0]

    df = pd.read_excel(file_path, header=header_row)
    df.columns = df.columns.str.strip()

    return df

def racks_logic(request):
    df = load_all_racks()

    racks = []

    for _, row in df.iterrows():
        racks.append({
            "cell_code": row["Код клетка"],
            "rack": row["Код клетка"].rsplit("-", 1)[0],
            "status": "blocked" if row["Вид блокиране"] else "free",
            "quantity": row["Количество"],
        })

    context = {
        'racks': racks,
    }

    return render(request, "index.html", context)