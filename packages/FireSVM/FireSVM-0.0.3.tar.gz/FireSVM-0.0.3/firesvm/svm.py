import numpy as np
import cvxopt
from firesvm.plots import *
from firesvm.kernels import *


class SVM:
    def __init__(self, kernel=rbf, C=1, tol = 1e-5, max_iter = 100, verbose = False):
        self.kernel = kernel
        self.C = C
        self.tol = tol
        self.max_iter = max_iter
        self.verbose = verbose

        if self.verbose == False:
            cvxopt.solvers.options['show_progress'] = False

    def fit(self, X, y):
        self.y = y
        self.X = X
        m, n = X.shape

        self.K = np.zeros((m, m))
        for i in range(m):
            self.K[i, :] = self.kernel(X[i, np.newaxis], self.X)

        P = cvxopt.matrix(np.outer(y, y) * self.K)
        q = cvxopt.matrix(-np.ones((m, 1)))
        G = cvxopt.matrix(np.vstack((np.eye(m) * -1, np.eye(m))))
        h = cvxopt.matrix(np.hstack((np.zeros(m), np.ones(m) * self.C)))
        A = cvxopt.matrix(y, (1, m), "d")
        b = cvxopt.matrix(np.zeros(1))
        cvxopt.solvers.options["max_iter"] = self.max_iter

        sol = cvxopt.solvers.qp(P, q, G, h, A, b)
        self.alphas = np.array(sol["x"])

    def predict(self, X):
        y_predict = np.zeros((X.shape[0]))
        sv = self.get_parameters(self.alphas)

        for i in range(X.shape[0]):
            y_predict[i] = np.sum(
                self.alphas[sv]
                * self.y[sv, np.newaxis]
                * self.kernel(X[i], self.X[sv])[:, np.newaxis]
            )

        return np.sign(y_predict + self.b)

    def get_parameters(self, alphas):
        sv = ((alphas > self.tol) * (alphas < self.C)).flatten()
        self.w = np.dot(self.X[sv].T, alphas[sv] * self.y[sv, np.newaxis])
        self.b = np.mean(
            self.y[sv, np.newaxis]
            - self.alphas[sv] * self.y[sv, np.newaxis] * self.K[sv, sv][:, np.newaxis]
        )
        return sv

class nuSVM:
    def __init__(self, kernel=linear, nu=0.1, verbose=True, tol=1e-5):
        self.kernel = kernel
        self.nu = float(nu)
        self.verbose = verbose
        self.tol = tol
        assert self.nu >= 0 and self.nu <= 1.0
        if self.verbose == False:
            cvxopt.solvers.options['show_progress'] = False

    def fit(self, X, y):
        self.y = y
        self.X = X
        m, n = X.shape
        unique_labels = np.unique(y)
        assert len(unique_labels) == 2

        self.K = X.dot(X.T)

        P = cvxopt.matrix(np.outer(y, y) * self.K)
        q = cvxopt.matrix(np.ones(m) * -1)
        A = cvxopt.matrix(y, (1, m), "d")
        b = cvxopt.matrix(np.zeros(1))

        G = cvxopt.matrix(np.vstack((np.diag(np.ones(m) * -1),
                                     np.identity(m),
                                     np.ones((1, m)))))
        h = cvxopt.matrix(np.hstack((np.zeros(m),
                                     np.ones(m)*1./ m,
                                     self.nu)))

        solution = cvxopt.solvers.qp(P, q, G, h, A, b)

        a = np.ravel(solution['x'])

        sv = a > self.tol
        ind = np.arange(len(a))[sv]
        self.a = a[sv]
        self.sv = X[sv]
        self.sv_y = y[sv]
        self.b = 0
        for n in range(len(self.a)):
            self.b += self.sv_y[n]
            self.b -= np.sum(self.a * self.sv_y * K[ind[n], sv])
        self.b /= len(self.a)

        if self.kernel == linear:
            self.w = np.zeros(n)
            for n in range(len(self.a)):
                self.w += self.a[n] * self.sv_y[n] * self.sv[n]
        else:
            self.w = None

    def predict(self, X):
        if self.w is not None:
            return np.sign(np.dot(X, self.w) + self.b)
        else:
            y_predict = np.zeros(len(X))
            for i in range(len(X)):
                s = 0
                for a, sv_y, sv in zip(self.a, self.sv_y, self.sv):
                    s += a * sv_y * self.kernel(X[i], sv)
                y_predict[i] = s
            return np.sign(y_predict + self.b)
