import sys
import time

from libs.fm_index import FMIndex


def read_file(file_path: str) -> str:
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            return f.read()
    except FileNotFoundError:
        print(f"Unable to read specified input file")
        sys.exit(1)


def main():
    if len(sys.argv) < 2:
        print("Usage: python3 main.py <filepath>")
        sys.exit(1)

    file_path = sys.argv[1]

    print(f"Building an index from file content: {file_path}...")
    start_time = time.time()
    index = FMIndex(read_file(file_path))
    print(f"Index is ready. It took {time.time() - start_time:.2f} sec.")

    while True:
        try:
            pattern = input("Search pattern: ").strip()

            start_time = time.time()
            start, end = index.search(pattern)
            took_time = time.time() - start_time

            print(f"Found {max(0, end - start + 1)} matches")
            for start, end in index.generate_results(start, end, n=len(pattern), limit=10):
                print(f"Positions: [{start}; {end})")
            print(f"Took {took_time:.2f} sec. to process")

        except KeyboardInterrupt:
            print()
            break

if __name__ == "__main__":
    main()
