import os
import argparse
import pandas as pd
import numpy as np


def args_parse():
    "Parse the input argument, use '-h' for help."
    parser = argparse.ArgumentParser(
        usage='restidy -i < resfinder_result_directory > -o < output_file_directory > \n\nAuthor: Cui(Zhangqi Shen Lab, China Agricultural University)')
    parser.add_argument("-i", help="<input_path>: resfinder_result_path")
    parser.add_argument("-o", help="<output_file_path>: output_file_path")
    return parser.parse_args()


def cate_mapping_dict(file):
    df_map = pd.read_csv(file, names=['Database', 'Gene'], sep='\t')
    mapping_dict = dict(zip(df_map['Gene'], df_map['Database']))
    return mapping_dict


def drug_mapping_dict(file):
    """
    parse drug mapping files to dict
    """
    df_drug = pd.read_csv(file, sep='\t')
    drug_dict = dict(zip(df_drug['Gene'], df_drug['Phenotype']))
    return drug_dict


def drug_parse(df):
    # print("Input Dataframe")
    # print(df)
    df1 = df.groupby('Strain')['Drugs'].apply(
        lambda x: ', '.join(x.unique())).to_frame()
    # print(df1)
    df2 = df1['Drugs'].str.split(', ', expand=True).stack().to_frame().rename(
        columns={0: 'Drug'}).reset_index(level=1, drop=True).reset_index()
    df3 = df2.groupby(['Strain', 'Drug'])['Drug'].size(
    ).to_frame().rename(columns={'Drug': 'Count'})
    df3.reset_index(inplace=True)
    df4 = df3.pivot_table(index='Strain', columns='Drug', values='Count')
    df4[df4.notnull()] = 1
    return df4


def join(f):
    return os.path.join(os.path.dirname(__file__), f)


def res_concate(path):
    df_point_final = pd.DataFrame()
    df_resistance_final = pd.DataFrame()
    # print(path)
    for file in os.listdir(path):
        file_path = os.path.join(path, file)
        if os.path.isdir(file_path):
            point_file = os.path.join(file_path, 'PointFinder_results.txt')
            resistance_file = os.path.join(
                file_path, 'ResFinder_results_tab.txt')
            if os.path.isfile(point_file):
                # print(point_file)
                df_point_tmp = pd.read_csv(point_file, sep='\t')
                df_point_tmp['Strain'] = file
                df_point_final = pd.concat([df_point_final, df_point_tmp])
            if os.path.isfile(resistance_file):
                # print(resistance_file)
                df_resistance_tmp = pd.read_csv(resistance_file, sep='\t')
                df_resistance_tmp['Strain'] = file
                df_resistance_final = pd.concat(
                    [df_resistance_final, df_resistance_tmp])
    # print(df_point_final)
    return df_point_final, df_resistance_final


def main():
    args = args_parse()
    input_path = args.i
    input_path = os.path.abspath(input_path)
    # print('Input Path')
    # print(input_path)

    # check if the output directory exists
    if not os.path.exists(args.o):
        os.mkdir(args.o)

    # create output files handler
    output_file_path = os.path.abspath(args.o)
    output_resistance_file = os.path.join(
        output_file_path, 'resfinder_sum.csv')
    output_point_file = os.path.join(output_file_path, 'point_sum.csv')
    drug_output_file = os.path.join(output_file_path, 'drug_pivot.csv')

    # print info
    print('The results will be write into following files:\n')
    print(output_resistance_file + '\n')
    print(output_point_file + '\n')
    print(drug_output_file + '\n')

    # Get the directory of script and read mapping file
    cate_mapping_file = join("gene_db_mapping.tsv")
    cate_map_dict = cate_mapping_dict(cate_mapping_file)
    # print(cate_map_dict)

    # print(input_file)
    # process drugs parsing method
    drug_mapping_file = join("gene_drugs_mapping.tsv")
    drug_map_dict = drug_mapping_dict(drug_mapping_file)
    # print(drug_map_dict)

    df_point, df_resistance = res_concate(input_path)
    # print(df_resistance)

    # process drugs mapping
    # print(drug_map_dict)
    df_resistance['Drugs'] = df_resistance['Resistance gene'].map(
        drug_map_dict)

    # generate strain vs drugs pivot_table
    df_pivot_drugs = drug_parse(df_resistance)

    # mapping resistance gene to database
    df_resistance['Database'] = df_resistance['Resistance gene'].map(
        cate_map_dict)
    df_resistance_final = df_resistance.pivot_table(index='Strain', columns=[
        'Database', 'Resistance gene'], values='Identity', aggfunc=lambda x: ','.join(map(str, x)))

    # tidy point mutation results
    df_point_final = df_point.groupby(['Strain'])['Mutation'].apply(
        lambda x: ','.join(x)).to_frame()

    # print(df_final)
    df_resistance_final.to_csv(output_resistance_file)
    df_point_final.to_csv(output_point_file)
    df_pivot_drugs.to_csv(drug_output_file)


if __name__ == '__main__':
    main()
