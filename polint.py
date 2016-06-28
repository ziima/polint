import argparse


def get_parser():
    parser = argparse.ArgumentParser(description="Validates PO files")
    return parser


def main():
    parser = get_parser()
    parser.parse_args()


if __name__ == '__main__':
    main()
