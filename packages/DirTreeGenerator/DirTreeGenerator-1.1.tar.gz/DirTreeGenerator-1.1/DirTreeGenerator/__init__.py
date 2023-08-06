import os

tree_file = open('tree.txt', 'w', encoding='utf-8')


def write_tree(value):
    tree_file.write(value+'\n')


def generate_tree(dir: str, ignore_files: list, start=''):
    files_list = os.listdir(dir)
    for i in files_list:
        if i in ignore_files:
            write_tree(start + i, )
            continue
        if os.path.isdir(dir + '\\' + i):
            write_tree(start + i + ":")
            generate_tree(dir + "\\" + i, start=start + '|------', ignore_files=ignore_files)
        else:
            write_tree(start + i)
