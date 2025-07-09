import pandas as pd
from pathlib import Path
import operator

op_map = {
    "<": operator.lt,
    "<=": operator.le,
    "==": operator.eq,
    ">=": operator.ge,
    ">": operator.gt,
    "!=": operator.ne
}

#load file
def load_file(file_path) -> pd.DataFrame:
    try:
        if isinstance(file_path, str):
            file_path = Path(file_path)
        if file_path.name.lower().endswith(('.xls','xlsx')):
            return pd.read_excel(file_path, sheet_name = None)
        return {'Sheet1' : pd.read_csv(file_path)}
    except Exception as e:
        print(f'Error loading file{ file_path}:{e}')
        return None

def load_multiple_files(folder_path):
    all_data = []
    folder = Path(folder_path)
    file_paths = list(folder.glob('*.csv') + folder.glob('*.xls')+ folder.glob('*.xlsx'))
    for file_path in file_paths:
        sheets = load_file(file_path)
        if sheets is not None:
            for sheet_name, df in sheets.items():
                all_data.append({'file': file_path, 'sheet': sheet_name, 'data': df})
    return all_data

def filter_df(df, col_index, op_str, value):
    col_series = df.iloc[:, col_index]
    return df[op_map[op_str](col_series, value)]

def process_data(input_folder, output_folder):
    folder = Path(input_folder)
    file_paths = list(folder.glob('*.csv')) + list(folder.glob('*.xls')) + list(folder.glob('*.xlsx'))
    all_summaries = []  # Collect all summaries here

    for file_path in file_paths:
        sheets = load_file(file_path)
        if sheets is not None:
            match_sheet = sheets['Matching']
            unmatch_sheet = sheets['Template_Only']
            #analyze fold change
            match_sig = filter_df(match_sheet, 5, '<', 0.05)
            match_sig_up = filter_df(match_sig, 1, '>', 0)
            match_sig_down = filter_df(match_sig, 1, '<', 0)
            match_nsig = filter_df(match_sheet, 5, '>=', 0.05)
            unmatch_sig = filter_df(unmatch_sheet, 5, '<', 0.05)
            unmatch_sig_up = filter_df(unmatch_sig, 1, '>', 0)
            unmatch_sig_down = filter_df(unmatch_sig, 1, '<', 0)
            unmatch_ng = filter_df(unmatch_sheet, 5, '>=', 0.05)
            #analyze bp 
            match_sig_up_bp0_9 = filter_df(match_sig_up, 27, '>=', 0.9)
            match_sig_up_bp1 = filter_df(match_sig_up, 27, '==', 1)
            match_sig_down_bp0_9 = filter_df(match_sig_down, 27, '>=', 0.9)
            match_sig_down_bp1 = filter_df(match_sig_down, 27, '==', 1)
            match_nsig_bp0_9 = filter_df(match_nsig, 27, '>=', 0.9)
            match_nsig_bp1 = filter_df(match_nsig, 27, '==', 1)
            dfs_to_export = {
                'match_sig_0.5': match_sig,
                'match_sig_up_0.5': match_sig_up,
                'match_sig_down_0.5': match_sig_down,
                'match_nsig_0.5': match_nsig,
                'unmatch_sig': unmatch_sig,
                'unmatch_sig_up': unmatch_sig_up,
                'unmatch_sig_down': unmatch_sig_down,
                'unmatch_ng' : unmatch_ng,
                'match_sig_up_0.9': match_sig_up_bp0_9,
                'match_sig_up_1': match_sig_up_bp1,
                'match_sig_down_0.9': match_sig_down_bp0_9,
                'match_sig_down_1': match_sig_down_bp1,
                'match_nsig_0.9': match_nsig_bp0_9,
                'match_nsig_1': match_nsig_bp1, 
                }
            output_file = Path(output_folder)/f'{file_path.stem}_analysis.xlsx'
            deduped_dfs = {k : v.drop_duplicates(subset = v.columns[0]) for k, v in dfs_to_export.items()}
            with pd.ExcelWriter(output_file) as writer:
                for sheet_name, df_unique in deduped_dfs.items():
                    df_unique.to_excel(writer, sheet_name = sheet_name, index = False)
            #prepare summary 
            thresholds = [0.5,0.9,1]
            summary_list =[]
            for i in thresholds:
                i_str = str(i)
                summary = {
                    'match':[
                        len(deduped_dfs.get(f'match_sig_down_{i}', [])),
                        len(deduped_dfs.get(f'match_sig_up_{i}', [])),
                        len(deduped_dfs.get(f'match_nsig_{i}', [])),
                        len(deduped_dfs.get(f'match_sig_up_{i}', [])) + len(deduped_dfs.get(f'match_nsig_{i}', []))
                    ],
                    'unmatch':[
                        len(deduped_dfs.get('unmatch_sig_down', [])),
                        len(deduped_dfs.get('unmatch_sig_up', [])),
                        len(deduped_dfs.get('unmatch_ng', [])),
                        len(deduped_dfs.get('unmatch_sig_up', [])) + len(deduped_dfs.get('unmatch_ng', [])) 
                    ],
                    'title': f'{file_path.stem}_bp>={i_str}'
                }
                summary_list.append(summary)
            all_summaries.extend(summary_list)  # Add this file's summaries to the master list

    summary_py_path = Path(output_folder)/'summary.py'
    with open(summary_py_path, 'w', encoding='utf-8') as f:
        f.write(f'summaries = [\n')
        for summary in all_summaries:
            f.write(f'    {summary},\n')
        f.write(']\n')

process_data(r'D:\wenjie\alignment', r'D:\wenjie\alignment')