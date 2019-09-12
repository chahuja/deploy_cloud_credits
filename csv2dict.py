import pandas
import pickle as pkl
import argparse
import pdb

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-i', type=str,
                    help='csvfile')
    args = parser.parse_args()

    aws_codes = read_codes(args.i)
    outfile = '.'.join(args.i.split('.')[:-1] + ['pkl'])
    f = open(outfile,'wb')
    pkl.dump(aws_codes,f)
    f.close()

def read_codes(csvfile):
    df = pandas.read_csv(csvfile)
    aws_codes = {}
    for i, row in df.iterrows():
        aws_codes[row['Andrew ID']] = list(row[['Code 1 ($50)','Code 2 ($50)','Code 3 ($50)']].values)
    return aws_codes
