.. _examples_misc_admmcnsns:

ADMM Consensus Example
======================

A simple example demonstrating how to construct a solver for an ADMM
Consensus problem by specialising :class:`.admm.ADMMConsensus`.

.. code:: ipython3

    from __future__ import print_function
    from builtins import input

    import numpy as np

    from sporco.admm import admm
    import sporco.linalg as sl
    import sporco.prox as sp
    from sporco import plot
    plot.config_notebook_plotting()

Define class solving a simple synthetic problem demonstrating the
construction of an ADMM Consensus solver derived from
:class:`.admm.ADMMConsensus`.

.. code:: ipython3

    class ConsensusTest(admm.ADMMConsensus):
        r"""
        Solve the problem

        .. math::
           \mathrm{argmin}_\mathbf{x} \;
           (1/2) \sum_k \| A_k \mathbf{x} - \mathbf{s}_k \|_2^2 + \lambda
           \| \mathbf{x} \|_1

       via an ADMM consensus problem

       .. math::
           \mathrm{argmin}_{\mathbf{x}_k, \mathbf{y}} \;
           (1/2) \sum_k \| A_k \mathbf{x}_k - \mathbf{s}_k \|_2^2 + \lambda
           \| \mathbf{y} \|_1 \;\; \text{s.t.} \;\;
           \mathbf{x}_k = \mathbf{y} \; \forall k
        """

        def __init__(self, A, s, lmbda, opt=None):
            """
            Initialise a ConsensusTest object with problem parameters.

            Parameters
            ----------
            A : list of ndarray
              A list of arrays representing matrices :math:`A_k`
            S : list of ndarray
              A list of arrays representing vectors :math:`\mathbf{s}_k`
            opt : :class:`.ADMMConsensus.Options` object
              Algorithm options
            """

            # Default solver options if none provided
            if opt is None:
                opt = admm.ADMMConsensus.Options()

            # Set object attributes corresponding to initialiser parameters
            self.A = A
            self.s = s
            self.lmbda = lmbda
            self.rho = opt['rho']
            # The number of separate components of the consensus problem
            Nb = len(A)
            # Construct a tuple representing the shape of the auxiliary
            # variable Y in the consensus problem
            shpY = (A[0].shape[1], s[0].shape[1] if s[0].ndim > 1 else 1)
            # Call parent class initialiser
            super(ConsensusTest, self).__init__(Nb, shpY, s[0].dtype, opt)

            # Construct list of products A_k^T s_k
            self.ATS = [A[i].T.dot(s[i]) for i in range(Nb)]
            # Compute an LU factorisation for each A_k
            self.rhochange()

            # Initialise working variables
            self.X = np.zeros(shpY + (Nb,))
            self.Y = np.zeros(shpY)
            self.U = np.zeros(shpY + (Nb,))



        def rhochange(self):
            r"""
            This method is called when the penalty parameter :math:`\rho` is
            updated by the parent class solve method. It computes an LU
            factorisation of :math:`A_k^T A_k + \rho I`.
            """

            self.lu = []
            self.piv = []
            for i in range(self.Nb):
                lu, piv = sl.lu_factor(self.A[i], self.rho)
                self.lu.append(lu)
                self.piv.append(piv)



        def obfn_fi(self, Xi, i):
            r"""
            Compute :math:`(1/2) \sum_k \| A_k \mathbf{x}_k - \mathbf{s}_k
            \|_2^2`.
            """

            return 0.5*np.linalg.norm(self.A[i].dot(Xi) - self.s[i])**2



        def obfn_g(self, Y):
            r"""
            Compute :math:`\lambda \| \mathbf{x} \|_1`.
            """

            return self.lmbda * np.sum(np.abs(Y))



        def xistep(self, i):
            r"""
            Minimise Augmented Lagrangian with respect to :math:`\mathbf{x}`
            component :math:`\mathbf{x}_i`.
            """

            self.X[..., i] = sl.lu_solve_ATAI(self.A[i], self.rho,
                        self.ATS[i] + self.rho*(self.Y - self.U[..., i]),
                        self.lu[i], self.piv[i])



        def prox_g(self, X, rho):
            r"""
            Proximal operator of :math:`(\lambda/\rho) \|\cdot\|_1`.
            """

            return sp.prox_l1(X, (self.lmbda/rho))

Construct random sparse vector :math:`\mathbf{x}`, random
:math:`A_k`\ \` matrices, and vectors :math:`\mathbf{s}_k` such that
:math:`A_k \mathbf{x} = \mathbf{s}_k`.

.. code:: ipython3

    np.random.seed(12345)
    x = np.random.randn(64,1)
    x[np.abs(x) < 1.25] = 0
    A = [np.random.randn(8, 64) for i in range(8)]
    s = [A[i].dot(x) for i in range(8)]

Initialise and run ``ConsensusTest`` solver.

.. code:: ipython3

    lmbda = 1e-1
    opt = ConsensusTest.Options({'Verbose': True, 'MaxMainIter': 250,
                                'AutoRho': {'Enabled': False},
                                'rho': 2e-1, 'RelaxParam': 1.2,
                                'fEvalX': False})
    b = ConsensusTest(A, s, lmbda, opt)
    yr = b.solve()
    print("ConsensusTest solve time: %.2fs" % b.timer.elapsed('solve'))


.. parsed-literal::

    Itn   Fnc       f         g         r         s
    ------------------------------------------------------
       0  1.02e+03  1.02e+03  4.98e-01  8.93e-01  3.74e-01
       1  3.81e+02  3.79e+02  1.55e+00  5.04e-01  4.44e-01
       2  1.56e+02  1.53e+02  2.70e+00  1.86e-01  4.24e-01
       3  2.25e+02  2.22e+02  3.54e+00  1.54e-01  3.58e-01
       4  2.94e+02  2.90e+02  4.02e+00  1.54e-01  2.83e-01
       5  2.58e+02  2.54e+02  4.15e+00  1.42e-01  2.42e-01
       6  1.71e+02  1.67e+02  4.09e+00  1.21e-01  2.34e-01
       7  1.06e+02  1.02e+02  3.91e+00  9.69e-02  2.43e-01
       8  8.91e+01  8.54e+01  3.72e+00  8.67e-02  2.27e-01
       9  8.71e+01  8.36e+01  3.58e+00  8.72e-02  1.97e-01
      10  7.12e+01  6.77e+01  3.51e+00  8.12e-02  1.72e-01
      11  5.60e+01  5.25e+01  3.49e+00  6.85e-02  1.55e-01
      12  4.67e+01  4.32e+01  3.52e+00  6.25e-02  1.38e-01
      13  3.67e+01  3.32e+01  3.51e+00  5.29e-02  1.36e-01
      14  2.65e+01  2.30e+01  3.47e+00  4.55e-02  1.38e-01
      15  1.90e+01  1.56e+01  3.43e+00  4.19e-02  1.22e-01
      16  1.50e+01  1.16e+01  3.40e+00  3.49e-02  1.18e-01
      17  1.52e+01  1.19e+01  3.36e+00  3.11e-02  1.13e-01
      18  1.71e+01  1.38e+01  3.32e+00  3.51e-02  8.42e-02
      19  1.75e+01  1.42e+01  3.30e+00  3.32e-02  6.56e-02
      20  1.59e+01  1.26e+01  3.27e+00  3.12e-02  6.14e-02
      21  1.28e+01  9.56e+00  3.24e+00  2.69e-02  6.65e-02
      22  9.67e+00  6.46e+00  3.21e+00  2.30e-02  7.37e-02
      23  7.33e+00  4.16e+00  3.17e+00  1.91e-02  7.84e-02
      24  6.21e+00  3.08e+00  3.12e+00  1.68e-02  7.78e-02
      25  5.70e+00  2.63e+00  3.07e+00  1.66e-02  7.39e-02
      26  5.28e+00  2.25e+00  3.02e+00  1.65e-02  6.43e-02
      27  5.03e+00  2.04e+00  2.99e+00  1.54e-02  5.53e-02
      28  4.98e+00  2.02e+00  2.96e+00  1.49e-02  4.64e-02
      29  4.88e+00  1.95e+00  2.93e+00  1.27e-02  4.23e-02
      30  4.77e+00  1.85e+00  2.91e+00  1.23e-02  3.89e-02
      31  4.66e+00  1.76e+00  2.90e+00  1.15e-02  3.57e-02
      32  4.59e+00  1.69e+00  2.90e+00  1.19e-02  2.96e-02
      33  4.40e+00  1.50e+00  2.90e+00  1.10e-02  2.74e-02
      34  4.10e+00  1.20e+00  2.90e+00  1.01e-02  2.76e-02
      35  3.79e+00  8.83e-01  2.91e+00  8.90e-03  2.95e-02
      36  3.56e+00  6.44e-01  2.91e+00  7.65e-03  3.09e-02
      37  3.43e+00  5.18e-01  2.92e+00  6.66e-03  3.14e-02
      38  3.41e+00  4.88e-01  2.92e+00  6.26e-03  3.05e-02
      39  3.43e+00  5.17e-01  2.92e+00  6.36e-03  2.85e-02
      40  3.54e+00  6.26e-01  2.92e+00  7.27e-03  2.18e-02
      41  3.62e+00  7.09e-01  2.92e+00  7.29e-03  1.74e-02
      42  3.62e+00  7.03e-01  2.91e+00  7.34e-03  1.45e-02
      43  3.52e+00  6.10e-01  2.91e+00  6.95e-03  1.44e-02
      44  3.38e+00  4.68e-01  2.91e+00  6.24e-03  1.61e-02
      45  3.24e+00  3.29e-01  2.91e+00  5.38e-03  1.81e-02
      46  3.13e+00  2.23e-01  2.91e+00  4.58e-03  1.94e-02
      47  3.07e+00  1.59e-01  2.91e+00  3.95e-03  2.00e-02
      48  3.05e+00  1.36e-01  2.91e+00  3.59e-03  1.98e-02
      49  3.06e+00  1.49e-01  2.91e+00  3.56e-03  1.87e-02
      50  3.11e+00  1.93e-01  2.91e+00  3.92e-03  1.67e-02
      51  3.16e+00  2.46e-01  2.92e+00  4.33e-03  1.40e-02
      52  3.20e+00  2.87e-01  2.92e+00  4.69e-03  1.09e-02
      53  3.22e+00  2.96e-01  2.92e+00  4.83e-03  8.37e-03
      54  3.19e+00  2.65e-01  2.92e+00  4.69e-03  7.78e-03
      55  3.13e+00  2.02e-01  2.92e+00  4.25e-03  9.46e-03
      56  3.05e+00  1.28e-01  2.93e+00  3.57e-03  1.18e-02
      57  2.99e+00  6.61e-02  2.93e+00  2.83e-03  1.37e-02
      58  2.96e+00  3.46e-02  2.93e+00  2.26e-03  1.45e-02
      59  2.96e+00  3.76e-02  2.92e+00  2.18e-03  1.41e-02
      60  2.99e+00  6.51e-02  2.92e+00  2.53e-03  1.26e-02
      61  3.02e+00  9.94e-02  2.92e+00  2.98e-03  1.04e-02
      62  3.04e+00  1.24e-01  2.92e+00  3.29e-03  7.95e-03
      63  3.04e+00  1.28e-01  2.92e+00  3.39e-03  6.27e-03
      64  3.03e+00  1.14e-01  2.91e+00  3.25e-03  6.27e-03
      65  3.00e+00  8.89e-02  2.91e+00  2.94e-03  7.51e-03
      66  2.97e+00  6.31e-02  2.91e+00  2.53e-03  8.90e-03
      67  2.95e+00  4.51e-02  2.91e+00  2.14e-03  9.83e-03
      68  2.95e+00  3.88e-02  2.91e+00  1.90e-03  1.01e-02
      69  2.95e+00  4.32e-02  2.91e+00  1.87e-03  9.74e-03
      70  2.96e+00  5.40e-02  2.91e+00  2.02e-03  8.81e-03
      71  2.97e+00  6.59e-02  2.91e+00  2.23e-03  7.50e-03
      72  2.98e+00  7.44e-02  2.91e+00  2.39e-03  6.03e-03
      73  2.99e+00  7.64e-02  2.91e+00  2.47e-03  4.80e-03
      74  2.98e+00  7.09e-02  2.91e+00  2.44e-03  4.31e-03
      75  2.97e+00  5.92e-02  2.91e+00  2.29e-03  4.78e-03
      76  2.96e+00  4.38e-02  2.91e+00  2.06e-03  5.78e-03
      77  2.94e+00  2.83e-02  2.91e+00  1.78e-03  6.76e-03
      78  2.93e+00  1.61e-02  2.92e+00  1.51e-03  7.44e-03
      79  2.93e+00  9.36e-03  2.92e+00  1.35e-03  7.66e-03
      80  2.93e+00  8.70e-03  2.92e+00  1.35e-03  7.38e-03
      81  2.93e+00  1.28e-02  2.92e+00  1.49e-03  6.62e-03
      82  2.94e+00  1.91e-02  2.92e+00  1.67e-03  5.50e-03
      83  2.94e+00  2.47e-02  2.92e+00  1.82e-03  4.22e-03
      84  2.95e+00  2.74e-02  2.92e+00  1.89e-03  3.12e-03
      85  2.95e+00  2.64e-02  2.92e+00  1.86e-03  2.75e-03
      86  2.94e+00  2.23e-02  2.92e+00  1.76e-03  3.28e-03
      87  2.94e+00  1.66e-02  2.92e+00  1.60e-03  4.13e-03
      88  2.93e+00  1.15e-02  2.92e+00  1.43e-03  4.85e-03
      89  2.93e+00  8.33e-03  2.92e+00  1.30e-03  5.25e-03
      90  2.93e+00  7.87e-03  2.92e+00  1.24e-03  5.30e-03
      91  2.93e+00  9.80e-03  2.92e+00  1.25e-03  5.03e-03
      92  2.93e+00  1.31e-02  2.92e+00  1.31e-03  4.53e-03
      93  2.93e+00  1.63e-02  2.91e+00  1.37e-03  3.95e-03
      94  2.93e+00  1.85e-02  2.91e+00  1.40e-03  3.47e-03
      95  2.93e+00  1.91e-02  2.91e+00  1.38e-03  3.27e-03
      96  2.93e+00  1.81e-02  2.91e+00  1.34e-03  3.37e-03
      97  2.93e+00  1.62e-02  2.91e+00  1.27e-03  3.62e-03
      98  2.93e+00  1.42e-02  2.91e+00  1.20e-03  3.84e-03
      99  2.93e+00  1.30e-02  2.91e+00  1.15e-03  3.92e-03
     100  2.93e+00  1.28e-02  2.91e+00  1.14e-03  3.78e-03
     101  2.93e+00  1.36e-02  2.91e+00  1.17e-03  3.45e-03
     102  2.93e+00  1.49e-02  2.91e+00  1.21e-03  2.96e-03
     103  2.93e+00  1.59e-02  2.91e+00  1.24e-03  2.44e-03
     104  2.93e+00  1.62e-02  2.91e+00  1.25e-03  2.05e-03
     105  2.93e+00  1.54e-02  2.91e+00  1.23e-03  2.01e-03
     106  2.93e+00  1.36e-02  2.91e+00  1.18e-03  2.30e-03
     107  2.92e+00  1.11e-02  2.91e+00  1.11e-03  2.73e-03
     108  2.92e+00  8.52e-03  2.91e+00  1.03e-03  3.12e-03
     109  2.92e+00  6.38e-03  2.91e+00  9.65e-04  3.38e-03
     110  2.92e+00  5.06e-03  2.91e+00  9.31e-04  3.45e-03
     111  2.92e+00  4.64e-03  2.91e+00  9.32e-04  3.33e-03
     112  2.92e+00  4.95e-03  2.92e+00  9.61e-04  3.03e-03
     113  2.92e+00  5.63e-03  2.92e+00  1.00e-03  2.59e-03
     114  2.92e+00  6.23e-03  2.92e+00  1.04e-03  2.06e-03
     115  2.92e+00  6.41e-03  2.92e+00  1.07e-03  1.55e-03
     116  2.92e+00  6.00e-03  2.92e+00  1.07e-03  1.22e-03
     117  2.92e+00  5.03e-03  2.92e+00  1.05e-03  1.25e-03
     118  2.92e+00  3.75e-03  2.92e+00  1.02e-03  1.55e-03
     119  2.92e+00  2.47e-03  2.92e+00  9.76e-04  1.91e-03
     120  2.92e+00  1.54e-03  2.92e+00  9.33e-04  2.19e-03
     121  2.92e+00  1.16e-03  2.92e+00  9.01e-04  2.36e-03
     122  2.92e+00  1.40e-03  2.92e+00  8.82e-04  2.40e-03
     123  2.92e+00  2.17e-03  2.92e+00  8.78e-04  2.34e-03
     124  2.92e+00  3.25e-03  2.92e+00  8.82e-04  2.19e-03
     125  2.92e+00  4.40e-03  2.92e+00  8.88e-04  2.02e-03
     126  2.92e+00  5.43e-03  2.91e+00  8.90e-04  1.88e-03
     127  2.92e+00  6.22e-03  2.91e+00  8.87e-04  1.79e-03
     128  2.92e+00  6.77e-03  2.91e+00  8.78e-04  1.77e-03
     129  2.92e+00  7.15e-03  2.91e+00  8.68e-04  1.77e-03
     130  2.92e+00  7.43e-03  2.91e+00  8.59e-04  1.75e-03
     131  2.92e+00  7.67e-03  2.91e+00  8.56e-04  1.68e-03
     132  2.92e+00  7.89e-03  2.91e+00  8.58e-04  1.54e-03
     133  2.92e+00  8.03e-03  2.91e+00  8.62e-04  1.34e-03
     134  2.92e+00  7.99e-03  2.91e+00  8.66e-04  1.13e-03
     135  2.92e+00  7.70e-03  2.91e+00  8.64e-04  9.86e-04
    ------------------------------------------------------
    ConsensusTest solve time: 0.08s


Plot reference and reconstructed sparse representations.

.. code:: ipython3

    plot.plot(np.hstack((x, yr)), title='Sparse representation',
            lgnd=['Reference', 'Reconstructed'])



.. image:: admmcnsns_files/admmcnsns_9_0.png


Plot functional value, residuals, and rho.

.. code:: ipython3

    its = b.getitstat()
    fig = plot.figure(figsize=(20, 5))
    plot.subplot(1, 3, 1)
    plot.plot(its.ObjFun, ptyp='semilogy', xlbl='Iterations', ylbl='Functional',
              fig=fig)
    plot.subplot(1, 3, 2)
    plot.plot(np.vstack((its.PrimalRsdl, its.DualRsdl)).T,
              ptyp='semilogy', xlbl='Iterations', ylbl='Residual',
              lgnd=['Primal', 'Dual'], fig=fig);
    plot.subplot(1, 3, 3)
    plot.plot(its.Rho, xlbl='Iterations', ylbl='Penalty Parameter', fig=fig)
    fig.show()



.. image:: admmcnsns_files/admmcnsns_11_0.png

