# low_pass filter and high-pass filter.
# low_pass = [[1/16, 1/8, 1/16], [1/8, 1/4, 1/8], [1/16, 1/8, 1/16]]
# high_pass = [[-1/8, -1/8, -1/8], [-1/8, 2, -1/8], [-1/8, -1/8, -1/8]]


import numpy as np

low_pass = [[1, 2, 3], [4, 5, 6], [7, 8, 9]]
zero_pass = [[0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0]]

image = [[1, 1, 1], [1, 1, 1], [1, 1, 1]]


def main():
    print("test")

    a = 4

    print(a ** 2)


if __name__ == "__main__":
    main()
