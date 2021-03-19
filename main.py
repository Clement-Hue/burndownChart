from jsonLoader import JsonLoader
import sys

DATA_FILE = sys.argv[1] if len(sys.argv) > 1 else "./data/tasks.json"
if __name__ == "__main__":
    loader = JsonLoader()
    burden = loader.load_burden(DATA_FILE)
    burden.show("ptrans")
