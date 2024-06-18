from utils.conformers import conform_to_detad
from utils.savers import save_to_json
from utils.loaders import load_teal
import argparse

def main(args):
    df = load_teal(args.origin_path)
    _dict = conform_to_detad(df)
    save_to_json(args.destination_path, _dict)


if __name__ == "__main__":
    # Create the argument parser
    parser = argparse.ArgumentParser(description="Load and process a JSON file.")

    # Add an argument for the JSON file path
    parser.add_argument(
        "--origin_path", type=str, help="The path to the JSON file to be loaded."
    )
    # Add an argument for the JSON file path
    parser.add_argument(
        "--destination_path", type=str, help="The path to the JSON file to be loaded."
    )

    # Parse the arguments
    args = parser.parse_args()

    # Call the main function with the parsed arguments
    main(args)
