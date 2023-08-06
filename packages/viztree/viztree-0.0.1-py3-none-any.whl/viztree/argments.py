import argparse


def create_base_parser():
    parser = argparse.ArgumentParser(prog='viztree',
                                     add_help=True,
                                     description='generate a tree html file to visualize a directory structure')

    parser.add_argument('path', nargs='?',
                        type=str, default='.',
                        help='directory path')

    parser.add_argument('--save', '-s',
                        type=str, default='index.html',
                        help='html file name to save the result')

    parser.add_argument('--skin',
                        type=str, default='xp',
                        choices=['xp', 'vista', 'win7', 'win8', 'win8-n', 'win8-xxl', 'lion'],
                        help='selecte skin that applies to the visualization')

    return parser.parse_args()
