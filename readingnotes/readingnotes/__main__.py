import sys

from .reader import process


def main():
    process(sys.argv[1], sys.argv[2])
