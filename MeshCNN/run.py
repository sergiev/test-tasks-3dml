"""
TODO:
3. wrap mp into webpage
4. Input via webpage form (upload button or something)
5. 'Load another file' button
6. Docker
7. Github Actions
"""
import numpy as np
import meshplot as mp
import torch

from models import create_model
from models.layers.mesh import Mesh
from data import DataLoader
from options.test_options import TestOptions
from util.util import pad

SCORE_THD = 0.5


def obj_data_to_mesh3d(odata):
    # Источник: https://chart-studio.plotly.com/~empet/15040/plotly-mesh3d-from-a-wavefront-obj-f/#/
    # odata is the string read from an obj file
    vertices = []
    faces = []
    lines = odata.splitlines()

    for line in lines:
        slist = line.split()
        if slist:
            if slist[0] == 'v':
                vertex = np.array(slist[1:], dtype=float)
                vertices.append(vertex)
            elif slist[0] == 'f':
                face = []
                for k in range(1, len(slist)):
                    face.append([int(s) for s in slist[k].replace('//', '/').split('/')])
                if len(face) > 3:  # triangulate the n-polyonal face, n>3
                    faces.extend([[face[0][0] - 1, face[k][0] - 1, face[k + 1][0] - 1] for k in
                                  range(1, len(face) - 1)])
                else:
                    faces.append([face[j][0] - 1 for j in range(len(face))])
            else:
                pass

    return np.array(vertices), np.array(faces)


def display_mesh_verdict(obj_data, verdict):
    """
    :param obj_data: содержимое obj-файла как строка
    :param verdict: строка, содержащая вывод модели (human-readable form)
    """
    vertices, faces = obj_data_to_mesh3d(obj_data)
    mp.offline()
    plot = mp.plot(vertices, faces, return_plot=True)
    print(verdict)
    # TODO #3


def get_verdict(model, path):
    mesh = Mesh(file=path, opt=opt, hold_history=False)
    # get edge features
    edge_features = mesh.extract_features()
    edge_features = pad(edge_features, opt.ninput_edges)
    edge_features = (edge_features - dataset.dataset.mean) / dataset.dataset.std
    edge_features = torch.from_numpy(edge_features).float().to(model.device).requires_grad_(
        model.is_train).unsqueeze(0)
    probs = model.net(edge_features, [mesh]).data.softmax(1)
    score = probs.max(1)[0][0] * 100
    if score < SCORE_THD:
        return "The model is unsure that uploaded object belongs to any of predefined classes :("

    label = dataset.dataset.classes[probs.max(1)[1]]

    return f"The model is {score:.3f}% sure it's {label}"


if __name__ == "__main__":
    obj_path = "../MeshCNN/primitives/torus/valid/Torus.1777.obj"
    with open(obj_path, 'rt') as file:
        obj_data = file.read()
    opt = TestOptions().parse()
    dataset = DataLoader(opt)
    model = create_model(opt)
    verdict = get_verdict(model, obj_path)
    display_mesh_verdict(obj_data, verdict)
