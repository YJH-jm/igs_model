import os
from glob import glob
import argparse


def make_file_list(directory, output):
    """훈련이미지를 파일 목록

    Args:
        directory ([str]): 이미지 파일이 있는 경로
        output ([str]): 저장할 파일명
    """
    img_file_list = glob(os.path.join(directory, '*.jpg'))
    img_file_list = [os.path.abspath(filename) for filename in img_file_list] #절대 경로로 변환
    with open(output, 'wt') as f:
        f.write('\n'.join(img_file_list))


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--directory', default='train', help='목록을 생성할 이미지가 있는 디렉토리')
    parser.add_argument('--output', default='train.txt', help='파일경로 목록 파일을 저장할 파일경로-파일명포함')

    args = parser.parse_args()

    make_file_list(args.directory, args.output)