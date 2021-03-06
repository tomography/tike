import time

import numpy as np

__author__ = "Daniel Ching, Viktor Nikitin"
__copyright__ = "Copyright (c) 2020, UChicago Argonne, LLC."
__docformat__ = 'restructuredtext en'


def random_complex(*args):
    """Return a complex random array in the range (-0.5, 0.5)."""
    return (np.random.rand(*args) - 0.5 + 1j * (np.random.rand(*args) - 0.5))


def inner_complex(x, y):
    """Return the complex inner product; the order of the operands matters."""
    return (x.conj() * y).sum()


class OperatorTests():
    """Provide operator tests for correct adjoint and normalization."""

    def setUp(self):
        self.operator = None
        self.operator.__enter__()
        self.xp = self.operator.xp
        np.random.seed(0)
        self.m = None
        self.m_name = ''
        self.d = None
        self.d_name = ''
        self.kwargs = {}
        print(self.operator)
        raise NotImplementedError()

    def tearDown(self):
        self.operator.__exit__(None, None, None)

    def test_adjoint(self):
        """Check that the adjoint operator is correct."""
        d = self.operator.fwd(**{self.m_name: self.m}, **self.kwargs)
        assert d.shape == self.d.shape
        m = self.operator.adj(**{self.d_name: self.d}, **self.kwargs)
        assert m.shape == self.m.shape
        a = inner_complex(d, self.d)
        b = inner_complex(self.m, m)
        print()
        print('<Fm,   m> = {:.6f}{:+.6f}j'.format(a.real.item(), a.imag.item()))
        print('< d, F*d> = {:.6f}{:+.6f}j'.format(b.real.item(), b.imag.item()))
        self.xp.testing.assert_allclose(a.real, b.real, rtol=1e-5)
        self.xp.testing.assert_allclose(a.imag, b.imag, rtol=1e-5)

    def test_normalized(self):
        """Check that the adjoint operator is normalized."""
        d = self.operator.fwd(**{self.m_name: self.m}, **self.kwargs)
        m = self.operator.adj(**{self.d_name: d}, **self.kwargs)
        a = inner_complex(m, m)
        b = inner_complex(self.m, self.m)
        print()
        print('<F*Fm, F*Fm> = {:.6f}{:+.6f}j'.format(a.real.item(),
                                                     a.imag.item()))
        print('<   m,    m> = {:.6f}{:+.6f}j'.format(b.real.item(),
                                                     b.imag.item()))
        self.xp.testing.assert_allclose(a.real, b.real, rtol=1e-5)

    def test_fwd_time(self):
        """Time the forward operation."""
        start = time.perf_counter()
        d = self.operator.fwd(**{self.m_name: self.m}, **self.kwargs)
        elapsed = time.perf_counter() - start
        print(f"\n{elapsed:1.3e} seconds")

    def test_adj_time(self):
        """Time the adjoint operation."""
        start = time.perf_counter()
        m = self.operator.adj(**{self.d_name: self.d}, **self.kwargs)
        elapsed = time.perf_counter() - start
        print(f"\n{elapsed:1.3e} seconds")
