from jsonLoader import JsonLoader
import sys

DATA_FILE = sys.argv[1] if len(sys.argv) > 1 else "./data/it5.json"
if __name__ == "__main__":
    loader = JsonLoader(DATA_FILE)
    burden = loader.load_burden()
    print(burden.listTask.__str__())
    burden.show()
