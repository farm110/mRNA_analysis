from scipy.stats import chi2_contingency, fisher_exact

input = [
    {'match': [97, 105, 870, 975], 'unmatch': [324, 280, 2970, 3250], 'title': 'FXR2_down_bp>=0.5'},
    {'match': [74, 74, 672, 746], 'unmatch': [324, 280, 2970, 3250], 'title': 'FXR2_down_bp>=0.9'},
    {'match': [44, 43, 402, 445], 'unmatch': [324, 280, 2970, 3250], 'title': 'FXR2_down_bp>=1'},
    {'match': [135, 119, 1137, 1256], 'unmatch': [286, 266, 2703, 2969], 'title': 'FXR2_up_bp>=0.5'},
    {'match': [115, 106, 946, 1052], 'unmatch': [286, 266, 2703, 2969], 'title': 'FXR2_up_bp>=0.9'},
    {'match': [80, 69, 601, 670], 'unmatch': [286, 266, 2703, 2969], 'title': 'FXR2_up_bp>=1'},
]
def chi_square(input):
    output = []
    for i in input:
        match = i['match']
        unmatch = i['unmatch']
        title = i['title']

        down_table = [[match[0],unmatch[0]],
                    [match[2], unmatch[2]]]
        up_table = [[match[1],unmatch[1]],
                    [match[2], unmatch[2]]]
        
        for label, table in [('Down VS NC', down_table), ('Up VS NC', up_table)]:
            print(f"{label} table: {table}")
            chi2, p_chi, dof, expected = chi2_contingency(table)
            print(f"chi2: {chi2}, p_chi: {p_chi}, dof: {dof}, expected: {expected}")
            if (expected < 5).any():
                odds, p_fisher = fisher_exact(table)
                print(f"Fisher odds: {odds}, p_fisher: {p_fisher}")
                output.append({'type': 'Fisher', 'chi2 or odds': round(float(odds), 5), 'p': float(p_fisher), 'label': label, 'title': title})
            else:
                output.append({'type': 'chi2', 'chi2 or odds': round(float(chi2), 5), 'p': float(p_chi), 'label': label, 'title': title})

    return output
def append_py(input, target_file, data_name):
    with open(target_file, 'a') as f:
        f.write(f'{data_name} = [\n')
        for i in input:
            f.write(f"{i}, \n")
        f.write(']\n')
        
