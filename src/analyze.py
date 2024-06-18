import argparse
from utils.loaders import load_json, load_teal, load_csv
from utils.semantic_analysis import SemanticAnalysis


def main(args):
    annotations = load_json(args.annotations_path)
    predictions = load_teal(args.predictions_path)

    confusion_matrix = load_csv(args.confusion_path)

    sa = SemanticAnalysis(annotations, predictions)
    # sa.analyze()
    sa._analyze(confusion_matrix)


if __name__ == "__main__":
    # Create the argument parser
    parser = argparse.ArgumentParser(description="Load and process a JSON file.")

    # Add an argument for the JSON file path
    parser.add_argument(
        "--annotations_path", type=str, help="The path to the JSON file to be loaded."
    )
    # Add an argument for the JSON file path
    parser.add_argument(
        "--predictions_path", type=str, help="The path to the JSON file to be loaded."
    )
    # Add an argument for the JSON file path
    parser.add_argument(
        "--confusion_path", type=str, help="The path to the JSON file to be loaded."
    )

    # Parse the arguments
    args = parser.parse_args()

    # Call the main function with the parsed arguments
    main(args)
