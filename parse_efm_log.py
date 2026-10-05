import csv
import re


def parse_efm_log(input_file, output_file):
    # Updated pattern allows any characters for T, P, A, UV (including None)
    pattern = re.compile(
        r'\[(.*?)\]\s*'                    # ignored timestamp
        r'(.*?),\s*'                       # human timestamp
        r'T:(.*?),\s*'                     # T can be None or number
        r'P:(.*?),\s*'                     # P can be None or number
        r'A:\((.*?),(.*?)\),\s*'           # A_x, A_y can be values or None
        r'UV:(.*?),\s*'                    # UV can be None or number
        r'EFM:\(\((.*?)\),\s*\((.*?)\)\)'  # EFM tuples
    )

    with open(input_file, 'r') as f, open(output_file, 'w', newline='') as out:
        writer = csv.writer(out)

        writer.writerow([
            "timestamp", "T", "P", "A_x", "A_y", "UV",
            "EFM_raw_1", "EFM_raw_2", "EFM_raw_3", "EFM_raw_4",
            "EFM_val_1", "EFM_val_2", "EFM_val_3", "EFM_val_4"
        ])

        for line in f:
            match = pattern.search(line)
            if not match:
                continue

            (_, human_ts, T, P, A1, A2, UV, raw_tuple, val_tuple) = match.groups()

            raw_vals = [x.strip() for x in raw_tuple.split(',')]
            val_vals = [x.strip() for x in val_tuple.split(',')]

            writer.writerow([
                human_ts.strip(), T.strip(), P.strip(),
                A1.strip(), A2.strip(), UV.strip(),
                *raw_vals, *val_vals
            ])
