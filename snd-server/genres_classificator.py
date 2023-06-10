import json
from transformers import AutoModelForSequenceClassification, AutoTokenizer

from context import Context


class GenresClassificator:
    def __init__(self, ctx: Context):
        self.config = ctx.config
        self.tokenizer = AutoTokenizer.from_pretrained("bert-base-uncased")
        self.ids_to_labels = dict()

    async def load_model(self):
        self.model = AutoModelForSequenceClassification.from_pretrained(
            self.config.archive_bert_model_path
        )
        with open(f"{self.config.archive_bert_model_path}/config.json", "r") as file:
            self.ids_to_labels = json.load(file)["id2label"]

    async def predict(self, prompt_text: str):
        encoding = self.tokenizer(prompt_text, return_tensors="pt")
        outputs = self.model(**encoding)

        probs = outputs[0].softmax(1).flatten().cpu()
        predictions = probs.detach().numpy()

        predicted_labels = dict()
        for idx, label in enumerate(predictions):
            predicted_labels.update({self.ids_to_labels[str(idx)]: label})

        predicted_labels = {
            k: v
            for k, v in sorted(
                predicted_labels.items(), key=lambda item: item[1], reverse=True
            )
        }

        return predicted_labels
