import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.axes_grid1 import make_axes_locatable
from scipy.io import loadmat
from scipy.linalg import eigh


def load_and_center_dataset(filename):
    dataset = loadmat(filename)
    x = dataset['fea']
    y = np.array(x)
    x = y - np.mean(y, axis=0)
    return x


def get_covariance(dataset):
    x = np.array(dataset)
    cov_matrix = np.dot(np.transpose(x), x)
    n = len(dataset)
    cov_matrix = np.divide(cov_matrix, n - 1)
    return cov_matrix


def get_eig(S, m):
    A = np.array(S)
    Lambda, eng_vector = eigh(A)
    dia = np.zeros([m, m])
    U = np.empty([len(eng_vector), m])
    for i in range(m):
        dia[i, i] = Lambda[len(Lambda) - i - 1]
        U[:, i] = eng_vector[:, len(eng_vector) - i - 1]
    return dia, U


def project_image(image, U):
    m = len(U[0])
    proj = np.zeros([len(U), 1])
    for i in range(m):
        eng_vector = []
        for j in range(len(U)):
            eng_vector.append(U[j, i])
        ele = np.dot(np.transpose(eng_vector), np.transpose(image))
        proj[:, 0] = proj[:, 0] + ele * U[:, i]
    proj = np.transpose(proj)
    one_dim_proj = proj[0]
    return one_dim_proj


def display_image(orig, proj):
    x = np.reshape(orig,(32,32))
    x = np.transpose(x)
    y = np.array(proj).reshape(32, 32)
    y = np.transpose(y)
    fig, (ax1, ax2) = plt.subplots(1, 2)
    img_orig = ax1.imshow(x, aspect='equal')
    ax1.set_title('Original')
    divider = make_axes_locatable(ax1)
    cax = divider.append_axes("right", size="5%", pad=0.05)
    plt.colorbar(img_orig, cax=cax)
    img_proj = ax2.imshow(y, aspect='equal')
    ax2.set_title('Projection')
    divider = make_axes_locatable(ax2)
    cax = divider.append_axes("right", size="5%", pad=0.05)
    plt.colorbar(img_proj, cax=cax)
    plt.tight_layout()
    plt.show()
