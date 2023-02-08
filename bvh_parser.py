import io

import numpy as np

from BVHnode import BVHnode


def parse_file(file: str | io.TextIOBase) -> tuple[BVHnode, float, np.ndarray]:
    if isinstance(file, str) and file.endswith('.bvh'):
        with open(file, 'r') as f:
            text = f.read()
    elif isinstance(file, str):
        text = file
    elif isinstance(file, io.TextIOBase):
        text = file.read()
    else:
        raise TypeError('file must be a string or a file-like object')

    text_lines = [[token.strip() for token in line.split()] for line in text.splitlines()]
    text_lines = [[token for token in line if token] for line in text_lines if line]

    root = None
    frame_time = None

    joint_stack = []

    for line_index, line in enumerate(text_lines):
        token_index = 0
        while token_index < len(line):
            token = line[token_index]
            if token.upper() in ('HIERARCHY', 'MOTION', '{'):
                token_index += 1
            elif token == 'ROOT':
                root = BVHnode(line[token_index + 1])
                joint_stack.append(root)
                token_index += 2
            elif token == 'OFFSET':
                joint_stack[-1].offset = tuple(float(x) for x in line[token_index + 1:token_index + 4])
                token_index += 4
            elif token == 'CHANNELS':
                channel_count = int(line[token_index + 1])
                joint_stack[-1].channels = line[token_index + 2:token_index + 2 + channel_count]
                token_index += 2 + channel_count
            elif token in ('JOINT', 'End'):
                node = BVHnode(line[token_index + 1], parent=joint_stack[-1])
                joint_stack.append(node)
                token_index += 2
            elif token == '}':
                joint_stack.pop()
                token_index += 1
            elif token == 'Frames:':
                frames = int(line[token_index + 1])
                token_index += 2
            elif token == 'Frame':
                frame_time = float(line[token_index + 2])
                break
            else:
                raise ValueError(f'Unknown token: {token}')
        if frame_time is not None:
            break

    motion = np.array([[float(x) for x in line] for line in text_lines[line_index + 1:]])

    return root, frame_time, motion
