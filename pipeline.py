import os
import glob
import pandas as pd

folder_path = "/content"
all_files = glob.glob(os.path.join(folder_path, "*.xlsx")) + glob.glob(os.path.join(folder_path, "*.csv"))
target_files = [f for file_path in all_files if "WGOR" in (f := os.path.basename(file_path)) or "pay" in f.lower()]

print(f"Found {len(target_files)} matching ONS data files. Executing self-healing pipeline...\n")
master_data_frames = []

for file_path in target_files:
    file_name = os.path.basename(file_path)
    data_category = file_name.replace(".xlsx", "").replace(".csv", "").strip()

    if file_path.endswith('.xlsx'):
        try:
            excel_file = pd.ExcelFile(file_path)
            for sheet in excel_file.sheet_names:
                if sheet.lower() in ['contents', 'notes', 'disclaimer', 'index']:
                    continue

                df_scan = pd.read_excel(file_path, sheet_name=sheet, header=None, nrows=15)

                header_row_idx = None
                for idx, row in df_scan.iterrows():
                    row_str = [str(val).strip().lower() for val in row.values]
                    if any('description' in val or 'region' in val or 'area' in val for val in row_str if val):
                        header_row_idx = idx
                        break

                skip_rows = header_row_idx if header_row_idx is not None else 5

                df = pd.read_excel(file_path, sheet_name=sheet, skiprows=skip_rows)
                df.columns = [str(col).strip() for col in df.columns]

                desc_col = [c for c in df.columns if c.lower() in ['description', 'region', 'area', 'name']]
                med_col = [c for c in df.columns if c.lower() in ['median', 'med']]
                mean_col = [c for c in df.columns if c.lower() in ['mean', 'avg']]
                code_col = [c for c in df.columns if c.lower() in ['code', 'id']]

                if desc_col and med_col:
                    df_temp = pd.DataFrame()
                    df_temp['Description'] = df[desc_col[0]]
                    df_temp['Median'] = df[med_col[0]]
                    df_temp['Mean'] = df[mean_col[0]] if mean_col else None
                    df_temp['Code'] = df[code_col[0]] if code_col else None
                    df_temp['Source_File'] = data_category
                    df_temp['Age_Group'] = sheet

                    master_data_frames.append(df_temp)
        except Exception as e:
            print(f" Warning: Could not parse Excel file {file_name} due to: {e}")

if master_data_frames:
    master_df = pd.concat(master_data_frames, ignore_index=True)

    master_df['Description'] = master_df['Description'].astype(str).str.strip()
    master_df['Median'] = pd.to_numeric(master_df['Median'], errors='coerce')
    master_df['Mean'] = pd.to_numeric(master_df['Mean'], errors='coerce')
    master_df = master_df.dropna(subset=['Median', 'Description'])

    region_keywords = "London|South East|South West|East|Midlands|Yorkshire|North West|North East|Wales|Scotland|Ireland|United Kingdom"
    master_df = master_df[master_df['Description'].str.contains(region_keywords, case=False, na=False)]

    master_df = master_df[~master_df['Description'].str.contains("Inner|Outer|London borough", case=False, na=False)]

    output_path = os.path.join(folder_path, "ons_master_regional_earnings.csv")
    master_df.to_csv(output_path, index=False)

    print("\n----------------------------------------------------------------------")
    print(f"SUCCESS! The self-healing pipeline has executed perfectly.")
    print(f"Compiled database total: {len(master_df)} rows of clean regional records.")
    print(f"Saved production dataset to: {output_path}")
    print("----------------------------------------------------------------------\n")

    print("Quick preview of your production-ready dataset columns:")
    print(master_df.head(5))
else:
    print("\nFinal Check Failed: No tables found matching core data configurations.")
