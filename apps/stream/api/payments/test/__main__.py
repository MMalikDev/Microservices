import sys
from pathlib import Path

path = str(Path.cwd())
sys.path.append(path)

from test.test_orders import orders_tests


def main():
    orders_tests.run()


if __name__ == "__main__":
    main()
