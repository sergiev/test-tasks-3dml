"""
TODO:
4. Input via webpage form (upload button or something)
5. 'Load another file' button
6. Docker
7. Github Actions
"""
import numpy as np
import plotly.graph_objects as go
from plotly.offline import iplot

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
    Украденный из интернета способ по интерактивного отображения мешей в окне браузера
    Также отображает
    Источник: https://chart-studio.plotly.com/~empet/15040/plotly-mesh3d-from-a-wavefront-obj-f/#/

    :param obj_data: содержимое obj-файла как строка
    :param verdict: строка, содержащая вывод модели (human-readable form)
    """
    vertices, faces = obj_data_to_mesh3d(obj_data)

    x, y, z = vertices[:, :3].T
    I, J, K = faces.T

    mesh = go.Mesh3d(x=-x, y=-y, z=z, vertexcolor=vertices[:, 3:],
                     i=I, j=J, k=K, name='', showscale=False)

    mesh.update(lighting=dict(ambient=0.18, diffuse=1, fresnel=.1, specular=1, roughness=.1),
                lightposition=dict(x=100, y=200, z=150))

    layout = go.Layout(title=verdict, font=dict(size=14, color='black'), width=900, height=800,
                       scene=dict(xaxis=dict(visible=False),
                                  yaxis=dict(visible=False),
                                  zaxis=dict(visible=False),
                                  aspectratio=dict(x=1.5, y=0.9, z=0.5),
                                  camera=dict(eye=dict(x=1., y=1., z=0.5)), ),
                       paper_bgcolor='rgb(235,235,235)', margin=dict(t=175))

    fig = go.Figure(data=[mesh], layout=layout)
    iplot(fig)


def get_verdict(model, path):
    mesh = Mesh(file=path, opt=opt, hold_history=False)
    # get edge features
    edge_features = mesh.extract_features()
    edge_features = pad(edge_features, opt.ninput_edges)
    edge_features = (edge_features - dataset.dataset.mean) / dataset.dataset.std

    probs = model.net(mesh, edge_features).data.softmax(1)
    score = probs.max(1)[0]
    if score < SCORE_THD:
        return "The model is unsure that uploaded object belongs to any of predefined classes :("

    label = dataset.dataset.classes[probs.max(1)[1]]

    return f"The model is {score:2f}% sure it's {label}"


if __name__ == "__main__":
    obj_path = "../MeshCNN/primitives/torus/valid/Torus.1777.obj"
    with open(obj_path, 'rt') as file:
        obj_data = file.read()
    opt = TestOptions().parse()
    dataset = DataLoader(opt)
    model = create_model(opt)
    verdict = get_verdict(model, obj_path)
    display_mesh_verdict(obj_data, verdict)
