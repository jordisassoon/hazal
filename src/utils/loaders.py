import json
import pandas as pd
import pickle


video_keys = {
    "annotations",
}

annotations_keys = {
    "segment",
    "label",
}


def sanity_check(annotations):
    for video in annotations.values():
        for key in video_keys:
            assert key in video
        for annotation in video["annotations"]:
            for key in annotations_keys:
                assert key in annotation

    return annotations


def load_json(file_path: str) -> pd.DataFrame:
    with open(file_path, "r") as file:
        annotations = json.load(file)

    sanity_check(annotations)
    return convert_to_dataframe(annotations)


def load_pickle(file_path: str) -> pd.DataFrame:
    with open(file_path, "rb") as file:
        annotations = pickle.load(file)

    sanity_check(annotations)
    return convert_to_dataframe(annotations)


def load_actionformer(file_path: str) -> pd.DataFrame:
    with open(file_path, "rb") as file:
        annotations = pickle.load(file)

    classdict = {
        "CricketBowling": 5,
        "CricketShot": 6,
        "VolleyballSpiking": 19,
        "JavelinThrow": 12,
        "Shotput": 15,
        "TennisSwing": 17,
        "GolfSwing": 9,
        "ThrowDiscus": 18,
        "Billiards": 2,
        "CleanAndJerk": 3,
        "LongJump": 13,
        "Diving": 7,
        "CliffDiving": 4,
        "BasketballDunk": 1,
        "HighJump": 11,
        "HammerThrow": 10,
        "SoccerPenalty": 16,
        "BaseballPitch": 0,
        "FrisbeeCatch": 8,
        "PoleVault": 14,
    }
    inv_classes = {v: k for k, v in classdict.items()}

    df = pd.DataFrame(annotations)
    df = df.rename(columns={'video-id': 'video_id', 't-end': 'end', 't-start': 'start'})
    df['label'] = df['label'].map(lambda x: inv_classes[x])
    return df

def load_teal(file_path: str) -> pd.DataFrame:
    df = pd.read_csv(file_path)
    df = df.rename(columns={'video-id': 'video_id', 't-start': 'start', 't-end': 'end'})
    return df

def load_csv(file_path: str) -> pd.DataFrame:
    return pd.read_csv(file_path)

def convert_to_dataframe(nested_dict: dict) -> pd.DataFrame:
    """
    Convert a nested dictionary into a Pandas DataFrame.

    Parameters:
    nested_dict (dict): The nested dictionary to convert.

    Returns:
    pd.DataFrame: The resulting DataFrame.
    """
    flat_dict_list = []

    for video_id, values in nested_dict.items():
        for annotation in values["annotations"]:
            new_entry = {
                "video_id": video_id,
                "start": float(annotation["segment"][0]),
                "end": float(annotation["segment"][1]),
                "label": annotation["label"],
            }
            if 'score' in annotation:
                new_entry["score"] = annotation["score"]
            flat_dict_list.append(new_entry)

    # Create DataFrame from the list of flattened dictionaries
    df = pd.DataFrame(flat_dict_list)

    return df