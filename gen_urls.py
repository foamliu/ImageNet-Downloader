import os
import argparse
import codecs

import pandas as pd


def get_categories(words, categories):
    """
    return: pandas DataFrame
    """
    all_list = pd.read_csv(words, header=None, delimiter='\t')
    all_list.columns = ['id', 'name']
    all_list['name'] = [str(c).strip() for c in all_list['name']]

    category_list = pd.read_csv(categories, header=None, delimiter='\t')
    category_list.columns = ['name']
    category_list = category_list.drop_duplicates()
    category_list['name'] = [str(c).strip() for c in category_list['name']]

    categories = pd.merge(all_list, category_list, on='name')

    label = pd.DataFrame(categories['name'].unique())
    label.columns = ['name']
    label['label'] = label.index

    return pd.merge(categories, label, on='name')


def process_line(line, urls, c_ids):
    fileid, fileurl, *tmp = line.strip().split('\t')
    c_id, _ = fileid.split('_')

    if c_id not in c_ids.keys():
        return urls

    urls.append(fileurl)
    return urls


def main():
    parser = argparse.ArgumentParser(description='Generate URL list')
    parser.add_argument('--urls', '-i', default='list/fall11_urls.txt')
    parser.add_argument('--words', '-w', default='list/words.txt')
    parser.add_argument('--categories', '-c', default='list/ILSVRC2012.txt')
    parser.add_argument('--root', '-r', default='image/original/')
    parser.add_argument('--urllist', default='list/urllist.txt')
    parser.add_argument('--clist', default='list/clist.csv')
    args = parser.parse_args()

    df = get_categories(args.words, args.categories)
    df.to_csv(args.clist, index=False)
    c_ids = list(df['id'])

    urls = []
    with codecs.open(args.urls, 'r', 'utf-8', 'ignore') as f:
        for line in f:
            fileid, fileurl, *tmp = line.strip().split('\t')
            c_id, _ = fileid.split('_')

            if c_id not in c_ids:
                continue

            row = {
                'name': os.path.join(args.root, fileid + '.jpg'),
                'url': '"{}"'.format(fileurl)}
            urls.append(row)

    pd.DataFrame(urls).to_csv(
        args.urllist, index=False, header=False, sep=' ')


if __name__ == '__main__':
    main()