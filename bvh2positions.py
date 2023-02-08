import sys

from bvh_parser import parse_file


def compute_positions(root, offset=(0, 0, 0)):
    root.position = offset
    root.absolute_transformation = (root.position, root.rotation)
    for child in root:
        compute_positions(child, root.position)


def main(path='./'):
    root, frame_time, motion = parse_file(path)
    compute_positions(root)


if __name__ == '__main__':
    main(*sys.argv[1:])
