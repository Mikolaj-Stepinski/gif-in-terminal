import argparse

def common_args() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(add_help=False)
    parser.add_argument('-H', type=int, default=20,
        help='image height in pixels')
    parser.add_argument('-W', type=int, default=20,
        help='image width in pixels')
    return parser

def image_args() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        add_help=True,
        parents=[common_args()],
    )
    parser.add_argument('--file', type=str, required=True,
        help='file path to image, supported formats .jpg .png')
    return parser

def slides_args() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        add_help=True,
        parents=[common_args()],
    )
    parser.add_argument('--iter', '-i', type=int, default=5, help='number of iterations')
    parser.add_argument('--refresh', '-r', type=float, default=0.1, help='seconds per slide')
    files = parser.add_mutually_exclusive_group(required=True)
    files.add_argument('--dir', type=str, help='path to directory with images')
    files.add_argument('--gif', type=str, help='path to .gif file')
    return parser