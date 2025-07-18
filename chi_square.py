from scipy.stats import chi2_contingency, fisher_exact

input = [
    {'match': [7, 15, 70, 95], 'unmatch': [4, 28, 70, 50], 'title': xxx'},
    {'match': [7, 7, 672, 76], 'unmatch': [4, 0, 20, 35], 'title': 'xxxx'},
    {'match': [4, 4, 402, 45], 'unmatch': [32, 20, 70, 30], 'title': 'xxx'},
    {'match': [35, 19, 37, 5], 'unmatch': 6, 266, 3,69], 'title': 'xxxx'},
    {'match': [15, 16, 9, 12], 'unmatch': [2, 266, 23, 9], 'title': 'xxx'},
    {'match': [0, 6, 1,670], 'unmatch': [86, 2, 23, 2], 'title': 'xxxx'},
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
        
