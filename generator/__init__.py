from pathlib import Path


DATA_DIR = Path(__file__).parent.parent / Path("data")


if __name__ == "__main__":
    print(DATA_DIR)
