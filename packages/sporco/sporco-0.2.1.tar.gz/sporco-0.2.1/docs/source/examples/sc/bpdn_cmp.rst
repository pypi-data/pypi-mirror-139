.. _examples_sc_bpdn_cmp:

Basis Pursuit DeNoising
=======================

This example demonstrates the use of classes :class:`.admm.bpdn.BPDN`
and :class:`.pgm.bpdn.BPDN` to solve the Basis Pursuit DeNoising
(BPDN) problem :cite:`chen-1998-atomic`

.. math:: \mathrm{argmin}_\mathbf{x} \; (1/2) \| D \mathbf{x} - \mathbf{s} \|_2^2 + \lambda \| \mathbf{x} \|_1 \;,

where :math:`D` is the dictionary, :math:`\mathbf{x}` is the sparse
representation, and :math:`\mathbf{s}` is the signal to be represented.
In this example the BPDN problem is used to estimate the reference
sparse representation that generated a signal from a noisy version of
the signal.

.. code:: ipython3

    from __future__ import print_function
    from builtins import input

    import numpy as np

    import sporco.admm.bpdn as abpdn
    import sporco.pgm.bpdn as pbpdn
    from sporco.pgm.backtrack import BacktrackRobust
    from sporco import plot
    plot.config_notebook_plotting()

Configure problem size, sparsity, and noise level.

.. code:: ipython3

    N = 512      # Signal size
    M = 4*N      # Dictionary size
    L = 32       # Number of non-zero coefficients in generator
    sigma = 0.5  # Noise level

Construct random dictionary, reference random sparse representation, and
test signal consisting of the synthesis of the reference sparse
representation with additive Gaussian noise.

.. code:: ipython3

    # Construct random dictionary and random sparse coefficients
    np.random.seed(12345)
    D = np.random.randn(N, M)
    x0 = np.zeros((M, 1))
    si = np.random.permutation(list(range(0, M-1)))
    x0[si[0:L]] = np.random.randn(L, 1)

    # Construct reference and noisy signal
    s0 = D.dot(x0)
    s = s0 + sigma*np.random.randn(N,1)

Set regularisation parameter.

.. code:: ipython3

    lmbda = 2.98e1

Set options for ADMM solver.

.. code:: ipython3

    opt_admm = abpdn.BPDN.Options({'Verbose': False, 'MaxMainIter': 500,
                            'RelStopTol': 1e-3, 'AutoRho': {'RsdlTarget': 1.0}})

Initialise and run ADMM solver object.

.. code:: ipython3

    ba = abpdn.BPDN(D, s, lmbda, opt_admm)
    xa = ba.solve()

    print("ADMM BPDN solve time: %.2fs" % ba.timer.elapsed('solve'))


.. parsed-literal::

    ADMM BPDN solve time: 0.17s


Set options for PGM solver.

.. code:: ipython3

    opt_pgm = pbpdn.BPDN.Options({'Verbose': True, 'MaxMainIter': 50, 'L': 9e2,
                                  'Backtrack': BacktrackRobust()})

Initialise and run PGM solver.

.. code:: ipython3

    bp = pbpdn.BPDN(D, s, lmbda, opt_pgm)
    xp = bp.solve()

    print("PGM BPDN solve time: %.2fs" % bp.timer.elapsed('solve'))


.. parsed-literal::

    Itn   Fnc       DFid      Regℓ1     Rsdl      F         Q         It_Bt  L
    ---------------------------------------------------------------------------------
       0  3.09e+03  1.61e+03  4.98e+01  1.68e+00  1.61e+03  2.27e+03      3  3.24e+03
       1  2.41e+03  7.88e+02  5.45e+01  2.01e+00  7.88e+02  9.97e+02      1  2.92e+03
       2  2.12e+03  4.33e+02  5.65e+01  9.08e-01  4.33e+02  5.07e+02      1  2.62e+03
       3  1.93e+03  3.20e+02  5.39e+01  6.26e-01  3.20e+02  3.70e+02      1  2.36e+03
       4  1.78e+03  2.45e+02  5.14e+01  5.64e-01  2.45e+02  2.81e+02      1  2.13e+03
       5  1.64e+03  2.31e+02  4.74e+01  5.60e-01  2.31e+02  2.63e+02      1  1.91e+03
       6  1.52e+03  1.99e+02  4.43e+01  5.78e-01  1.99e+02  2.25e+02      1  1.72e+03
       7  1.40e+03  1.94e+02  4.05e+01  6.01e-01  1.94e+02  2.17e+02      1  1.55e+03
       8  1.29e+03  1.67e+02  3.77e+01  6.33e-01  1.67e+02  1.85e+02      1  1.39e+03
       9  1.18e+03  1.71e+02  3.39e+01  6.61e-01  1.71e+02  1.88e+02      1  1.26e+03
      10  1.08e+03  1.26e+02  3.22e+01  6.88e-01  1.26e+02  1.35e+02      1  1.13e+03
      11  9.91e+02  1.61e+02  2.79e+01  7.11e-01  1.61e+02  1.63e+02      1  1.02e+03
      12  9.32e+02  1.20e+02  2.72e+01  5.64e-01  1.20e+02  1.29e+02      2  1.83e+03
      13  8.82e+02  1.11e+02  2.59e+01  4.89e-01  1.11e+02  1.19e+02      1  1.65e+03
      14  8.45e+02  9.68e+01  2.51e+01  4.46e-01  9.68e+01  1.03e+02      1  1.48e+03
      15  8.27e+02  8.55e+01  2.49e+01  3.94e-01  8.55e+01  9.20e+01      1  1.33e+03
      16  8.24e+02  7.91e+01  2.50e+01  2.93e-01  7.91e+01  8.54e+01      1  1.20e+03
      17  8.26e+02  7.74e+01  2.51e+01  1.89e-01  7.74e+01  8.32e+01      1  1.08e+03
      18  8.25e+02  7.82e+01  2.50e+01  1.59e-01  7.82e+01  8.17e+01      1  9.73e+02
      19  8.22e+02  8.35e+01  2.48e+01  1.76e-01  8.35e+01  8.46e+01      1  8.75e+02
      20  8.20e+02  8.68e+01  2.46e+01  1.36e-01  8.68e+01  8.70e+01      1  7.88e+02
      21  8.20e+02  8.90e+01  2.45e+01  8.70e-02  8.90e+01  8.91e+01      1  7.09e+02
      22  8.20e+02  8.86e+01  2.45e+01  5.12e-02  8.86e+01  8.87e+01      1  6.38e+02
      23  8.20e+02  9.02e+01  2.45e+01  3.57e-02  9.02e+01  9.02e+01      1  5.74e+02
      24  8.20e+02  8.89e+01  2.45e+01  3.13e-02  8.89e+01  8.90e+01      2  1.03e+03
      25  8.19e+02  8.89e+01  2.45e+01  2.08e-02  8.89e+01  8.89e+01      1  9.30e+02
      26  8.19e+02  8.86e+01  2.45e+01  1.76e-02  8.86e+01  8.86e+01      1  8.37e+02
      27  8.19e+02  8.86e+01  2.45e+01  1.38e-02  8.86e+01  8.86e+01      1  7.54e+02
      28  8.19e+02  8.83e+01  2.45e+01  9.18e-03  8.83e+01  8.83e+01      1  6.78e+02
      29  8.19e+02  8.86e+01  2.45e+01  6.69e-03  8.86e+01  8.86e+01      1  6.10e+02
      30  8.19e+02  8.85e+01  2.45e+01  5.76e-03  8.85e+01  8.85e+01      2  1.10e+03
      31  8.19e+02  8.85e+01  2.45e+01  4.05e-03  8.85e+01  8.85e+01      1  9.89e+02
      32  8.19e+02  8.85e+01  2.45e+01  3.62e-03  8.85e+01  8.85e+01      1  8.90e+02
      33  8.19e+02  8.86e+01  2.45e+01  3.22e-03  8.86e+01  8.86e+01      1  8.01e+02
      34  8.19e+02  8.86e+01  2.45e+01  2.43e-03  8.86e+01  8.86e+01      1  7.21e+02
      35  8.19e+02  8.86e+01  2.45e+01  1.63e-03  8.86e+01  8.86e+01      1  6.49e+02
      36  8.19e+02  8.86e+01  2.45e+01  1.47e-03  8.86e+01  8.86e+01      1  5.84e+02
      37  8.19e+02  8.86e+01  2.45e+01  1.60e-03  8.86e+01  8.86e+01      1  5.26e+02
      38  8.19e+02  8.86e+01  2.45e+01  1.36e-03  8.86e+01  8.86e+01      1  4.73e+02
      39  8.19e+02  8.86e+01  2.45e+01  7.28e-04  8.86e+01  8.86e+01      2  8.51e+02
    ---------------------------------------------------------------------------------
    PGM BPDN solve time: 0.09s


Plot comparison of reference and recovered representations.

.. code:: ipython3

    plot.plot(np.hstack((x0, xa, xp)), alpha=0.5, title='Sparse representation',
              lgnd=['Reference', 'Reconstructed (ADMM)',
                    'Reconstructed (PGM)'])



.. image:: bpdn_cmp_files/bpdn_cmp_17_0.png


Plot functional value, residual, and L

.. code:: ipython3

    itsa = ba.getitstat()
    itsp = bp.getitstat()
    fig = plot.figure(figsize=(21, 7))
    plot.subplot(1, 3, 1)
    plot.plot(itsa.ObjFun, xlbl='Iterations', ylbl='Functional', fig=fig)
    plot.plot(itsp.ObjFun, xlbl='Iterations', ylbl='Functional',
              lgnd=['ADMM', 'PGM'], fig=fig)
    plot.subplot(1, 3, 2)
    plot.plot(itsa.PrimalRsdl, ptyp='semilogy', xlbl='Iterations', ylbl='Residual',
              fig=fig)
    plot.plot(itsa.DualRsdl, ptyp='semilogy', fig=fig)
    plot.plot(itsp.Rsdl, ptyp='semilogy', lgnd=['Primal Residual (ADMM)',
              'Dual Residual (ADMM)','Residual (PGM)'], fig=fig)
    plot.subplot(1, 3, 3)
    plot.plot(itsa.Rho, xlbl='Iterations', ylbl='Algorithm Parameter', fig=fig)
    plot.plot(itsp.L, lgnd=[r'$\rho$ (ADMM)', '$L$ (PGM)'], fig=fig)
    fig.show()



.. image:: bpdn_cmp_files/bpdn_cmp_19_0.png

