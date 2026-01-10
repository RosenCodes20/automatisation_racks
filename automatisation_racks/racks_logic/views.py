import os

from django.core.files.uploadedfile import UploadedFile
from django.shortcuts import render
import pandas as pd
# Create your views here.

def load_all_racks(file_name, message):
    file_path = file_name

    df_raw = pd.read_excel(file_path, header=None)
    print(df_raw)
    header_row = df_raw.index[
        df_raw.astype(str).apply(
            lambda row: row.str.contains(message, na=False).any(),
            axis=1
        )
    ][0]

    df = pd.read_excel(file_path, header=header_row)
    df.columns = df.columns.str.strip()

    return df

def add_racks(all_racks, racks, counter, occupied_cells, letter, number):
    for _, row in all_racks.iterrows():
        if type(row['Код']) == str and row['Код'].startswith("W") and row['Код'].split('-')[1][0] == letter and row['Код'].split('-')[2] == str(number):
            racks.append({
                    "cell_code": row["Код"],
                    "status": "заета" if row['Код'] in occupied_cells else "свободна",
                    "counter": counter,
                    "rack_id": row['Код'].split('-')[1],
                    "main_letter": letter
                })

            if row['Код'] in occupied_cells:
                counter[1] += 1
            else:
                counter[0] += 1

    return counter

def racks_logic(request):
    df = load_all_racks("racks.xlsx", "Код клетка")
    all_racks = load_all_racks("all_racks.xlsx", "Код")

    if request.method == "POST" and request.FILES.get("rack_file"):
        print("HI")
        uploaded_file = request.FILES["rack_file"]

        temp_path = "racks.xlsx" + ".tmp"
        with open(temp_path, "wb+") as destination:
            for chunk in uploaded_file.chunks():
                destination.write(chunk)

        os.replace(temp_path, "racks.xlsx")

    occupied_cells = set(df["Код клетка"].dropna())
    counter = [0, 0]

    rack_groups = {
        "A": {1: [], 2: [], 3: []},
        "B": {1: [], 2: [], 3: []},
        "C": {1: [], 2: [], 3: []},
        "D": {1: [], 2: [], 3: []},
        "E": {1: [], 2: [], 3: []},
        "F": {1: [], 2: [], 3: []},
    }


    for letter in ["A", "B", "C", "D", "E", "F"]:
        for number in [1, 2, 3]:
            counter = add_racks(
                all_racks,
                rack_groups[letter][number],
                counter,
                occupied_cells,
                letter,
                number
            )

    context = {
        "rack_groups": rack_groups,
        'free_places': counter[0],
        "not_free_places": counter[1]
    }

    return render(request, "index.html", context)
