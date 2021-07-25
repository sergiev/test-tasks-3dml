from models import create_model
from data import DataLoader
from options.test_options import TestOptions

from sklearn.metrics import classification_report
import torch

if __name__ == "__main__":
    opt = TestOptions().parse()
    dataset = DataLoader(opt)
    model = create_model(opt)
    y_pred = []
    y_true = []
    for i, data in enumerate(dataset):
        model.set_input(data)
        with torch.no_grad():
            out = model.forward()
            y_pred += out.data.max(1)[1].cpu()
            y_true += model.labels.cpu()
    target_names = dataset.dataset.classes
    print(classification_report(y_true, y_pred, target_names=target_names))
