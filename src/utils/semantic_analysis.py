import torch
import pandas as pd
from torch.nn import CosineSimilarity
from sklearn.metrics import confusion_matrix
from transformers import CLIPTokenizer, CLIPTextModel

from utils.plotter import plot_matrix, scatter_plot
from utils.diagnoser import Diagnoser


class SemanticAnalysis(Diagnoser):
    def __init__(self, annotations: pd.DataFrame, predictions: pd.DataFrame):
        super().__init__(annotations, predictions)
        self.clip_model = "openai/clip-vit-large-patch14"
        self.tokenizer = CLIPTokenizer.from_pretrained(self.clip_model)
        self.device = "cuda" if torch.cuda.is_available() else "cpu"
        self.text_encoder = CLIPTextModel.from_pretrained(self.clip_model).to(
            self.device
        )
        self.cossim = CosineSimilarity(dim=0, eps=1e-6)

    def analyze(self):
        confusion_matrix = self.compute_confusion()
        plot_matrix(confusion_matrix, "Confusion Matrix", "plots/conf.png")

        classes = self.load_classes()
        text_embeddings = self.tokenize(classes)
        similarity_matrix = self.compute_similarity(classes, text_embeddings)
        similarity_matrix = self.align_matrices(similarity_matrix, confusion_matrix)
        plot_matrix(similarity_matrix, "Similarity Matrix", "plots/sim.png")

        scatter_plot(
            confusion_matrix.to_numpy().flatten(),
            similarity_matrix.to_numpy().flatten(),
            "Confusion-Similarity Correlation",
            "plots/scat.png",
        )

    def align_matrices(self, current_matrix, target_matrix):
        return current_matrix[target_matrix.columns].reindex(target_matrix.columns)

    def load_classes(self):
        classes = set(self.annotations.label.unique().tolist())
        classes.update(self.predictions.label.unique().tolist())
        return list(classes)

    def dist(self, v1, v2):
        return self.cossim(v1, v2)

    def tokenize(self, prompts):
        text_inputs = self.tokenizer(
            prompts, padding="max_length", return_tensors="pt"
        ).to(self.device)
        return torch.flatten(
            self.text_encoder(text_inputs.input_ids.to(self.device))[
                "last_hidden_state"
            ],
            1,
            -1,
        )

    def compute_similarity(self, prompts, text_embeddings):
        _dict = {}
        for i1, label1 in enumerate(prompts):
            _dict[label1] = {}
            for i2, label2 in enumerate(prompts):
                sim = self.dist(text_embeddings[i1], text_embeddings[i2]).item()
                _dict[label1][label2] = sim
        return pd.DataFrame.from_dict(_dict)

    def compute_confusion(self):
        merged = pd.merge(
            self.annotations, self.predictions, on="video_id", how="inner"
        )

        class_map = {v: i for (i, v) in enumerate(merged["label_x"].unique())}
        merged["label_x"] = merged["label_x"].map(lambda x: class_map[x])
        merged["label_y"] = merged["label_y"].map(lambda x: class_map[x])

        y_test = merged["label_x"]
        y_pred = merged["label_y"]

        df = pd.DataFrame(
            confusion_matrix(y_test, y_pred, normalize="pred"),
            columns=list(class_map.keys()),
        )
        df["id"] = list(class_map.keys())
        df.set_index("id", drop=False, inplace=True)

        return df.drop("id", axis=1)
