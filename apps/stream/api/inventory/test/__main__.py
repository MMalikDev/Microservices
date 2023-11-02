import sys
from pathlib import Path

path = str(Path.cwd())
sys.path.append(path)

from test.test_products import products_tests


def main():
    products_tests.run()


if __name__ == "__main__":
    main()
