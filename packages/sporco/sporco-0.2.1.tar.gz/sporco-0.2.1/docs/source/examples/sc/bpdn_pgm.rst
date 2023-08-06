.. _examples_sc_bpdn_pgm:

Basis Pursuit DeNoising
=======================

This example demonstrates the use of class :class:`.pgm.bpdn.BPDN` to
solve the Basis Pursuit DeNoising (BPDN) problem
:cite:`chen-1998-atomic`

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

    from sporco.pgm import bpdn
    from sporco import plot
    plot.config_notebook_plotting()
    from sporco.pgm.backtrack import BacktrackStandard, BacktrackRobust

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

Set regularisation parameter and options for BPDN solver with standard
PGM backtracking.

.. code:: ipython3

    lmbda = 2.98e1
    L_sc = 9.e2
    opt = bpdn.BPDN.Options({'Verbose': True, 'MaxMainIter': 50,
                             'Backtrack': BacktrackStandard(), 'L': L_sc})

Initialise and run BPDN object

.. code:: ipython3

    b1 = bpdn.BPDN(D, s, lmbda, opt)
    x1 = b1.solve()

    print("BPDN standard PGM backtracking solve time: %.2fs" %
          b1.timer.elapsed('solve'))


.. parsed-literal::

    Itn   Fnc       DFid      Regℓ1     Rsdl      F         Q         It_Bt  L
    ---------------------------------------------------------------------------------
       0  3.08e+03  1.59e+03  5.00e+01  1.68e+00  1.59e+03  2.24e+03      8  3.22e+03
       1  2.45e+03  8.43e+02  5.39e+01  4.96e-01  8.43e+02  1.05e+03      1  3.22e+03
       2  2.16e+03  4.93e+02  5.61e+01  2.61e-01  4.93e+02  5.69e+02      1  3.22e+03
       3  1.99e+03  3.48e+02  5.52e+01  1.79e-01  3.48e+02  3.94e+02      1  3.22e+03
       4  1.86e+03  2.77e+02  5.31e+01  1.48e-01  2.77e+02  3.09e+02      1  3.22e+03
       5  1.75e+03  2.40e+02  5.07e+01  1.31e-01  2.40e+02  2.66e+02      1  3.22e+03
       6  1.65e+03  2.21e+02  4.81e+01  1.20e-01  2.21e+02  2.42e+02      1  3.22e+03
       7  1.56e+03  2.08e+02  4.55e+01  1.11e-01  2.08e+02  2.27e+02      1  3.22e+03
       8  1.48e+03  1.97e+02  4.31e+01  1.05e-01  1.97e+02  2.13e+02      1  3.22e+03
       9  1.41e+03  1.86e+02  4.09e+01  9.78e-02  1.86e+02  2.00e+02      1  3.22e+03
      10  1.33e+03  1.77e+02  3.88e+01  9.04e-02  1.77e+02  1.90e+02      1  3.22e+03
      11  1.26e+03  1.69e+02  3.67e+01  8.70e-02  1.69e+02  1.81e+02      1  3.22e+03
      12  1.20e+03  1.61e+02  3.49e+01  8.39e-02  1.61e+02  1.71e+02      1  3.22e+03
      13  1.14e+03  1.51e+02  3.32e+01  8.11e-02  1.51e+02  1.60e+02      1  3.22e+03
      14  1.09e+03  1.42e+02  3.17e+01  7.88e-02  1.42e+02  1.51e+02      1  3.22e+03
      15  1.03e+03  1.34e+02  3.02e+01  7.34e-02  1.34e+02  1.42e+02      1  3.22e+03
      16  9.86e+02  1.28e+02  2.88e+01  6.89e-02  1.28e+02  1.35e+02      1  3.22e+03
      17  9.43e+02  1.21e+02  2.76e+01  7.12e-02  1.21e+02  1.29e+02      1  3.22e+03
      18  9.04e+02  1.13e+02  2.66e+01  6.89e-02  1.13e+02  1.20e+02      1  3.22e+03
      19  8.72e+02  1.05e+02  2.57e+01  6.23e-02  1.05e+02  1.11e+02      1  3.22e+03
      20  8.49e+02  9.79e+01  2.52e+01  6.41e-02  9.79e+01  1.04e+02      1  3.22e+03
      21  8.34e+02  8.95e+01  2.50e+01  6.70e-02  8.95e+01  9.57e+01      1  3.22e+03
      22  8.27e+02  8.40e+01  2.49e+01  5.62e-02  8.40e+01  8.83e+01      1  3.22e+03
      23  8.26e+02  7.99e+01  2.50e+01  6.01e-02  7.99e+01  8.49e+01      1  3.22e+03
      24  8.28e+02  7.75e+01  2.52e+01  5.90e-02  7.75e+01  8.24e+01      1  3.22e+03
      25  8.30e+02  7.62e+01  2.53e+01  4.73e-02  7.62e+01  7.94e+01      1  3.22e+03
      26  8.30e+02  7.62e+01  2.53e+01  3.76e-02  7.62e+01  7.81e+01      1  3.22e+03
      27  8.28e+02  7.68e+01  2.52e+01  3.18e-02  7.68e+01  7.82e+01      1  3.22e+03
      28  8.26e+02  7.86e+01  2.51e+01  2.39e-02  7.86e+01  7.95e+01      1  3.22e+03
      29  8.23e+02  8.17e+01  2.49e+01  1.82e-02  8.17e+01  8.21e+01      1  3.22e+03
      30  8.22e+02  8.53e+01  2.47e+01  1.33e-02  8.53e+01  8.56e+01      1  3.22e+03
      31  8.21e+02  8.89e+01  2.46e+01  1.06e-02  8.89e+01  8.91e+01      1  3.22e+03
      32  8.20e+02  9.16e+01  2.45e+01  1.06e-02  9.16e+01  9.18e+01      1  3.22e+03
      33  8.20e+02  9.31e+01  2.44e+01  1.02e-02  9.31e+01  9.32e+01      1  3.22e+03
      34  8.20e+02  9.34e+01  2.44e+01  9.82e-03  9.34e+01  9.35e+01      1  3.22e+03
      35  8.20e+02  9.28e+01  2.44e+01  9.05e-03  9.28e+01  9.29e+01      1  3.22e+03
      36  8.20e+02  9.19e+01  2.44e+01  8.34e-03  9.19e+01  9.20e+01      1  3.22e+03
      37  8.20e+02  9.08e+01  2.45e+01  8.33e-03  9.08e+01  9.09e+01      1  3.22e+03
      38  8.20e+02  8.98e+01  2.45e+01  8.47e-03  8.98e+01  8.99e+01      1  3.22e+03
      39  8.20e+02  8.92e+01  2.45e+01  6.82e-03  8.92e+01  8.93e+01      1  3.22e+03
      40  8.20e+02  8.89e+01  2.45e+01  5.97e-03  8.89e+01  8.90e+01      1  3.22e+03
      41  8.20e+02  8.87e+01  2.45e+01  5.24e-03  8.87e+01  8.88e+01      1  3.22e+03
      42  8.20e+02  8.85e+01  2.45e+01  4.90e-03  8.85e+01  8.86e+01      1  3.22e+03
      43  8.20e+02  8.83e+01  2.45e+01  4.37e-03  8.83e+01  8.84e+01      1  3.22e+03
      44  8.20e+02  8.83e+01  2.45e+01  3.19e-03  8.83e+01  8.83e+01      1  3.22e+03
      45  8.20e+02  8.82e+01  2.45e+01  3.12e-03  8.82e+01  8.82e+01      1  3.22e+03
      46  8.20e+02  8.81e+01  2.45e+01  3.90e-03  8.81e+01  8.82e+01      1  3.22e+03
      47  8.20e+02  8.80e+01  2.45e+01  3.57e-03  8.80e+01  8.80e+01      1  3.22e+03
      48  8.20e+02  8.79e+01  2.46e+01  2.87e-03  8.79e+01  8.79e+01      1  3.22e+03
      49  8.20e+02  8.79e+01  2.46e+01  2.65e-03  8.79e+01  8.79e+01      1  3.22e+03
    ---------------------------------------------------------------------------------
    BPDN standard PGM backtracking solve time: 0.07s


Set options for BPDN solver with robust PGM backtracking.

.. code:: ipython3

    opt = bpdn.BPDN.Options({'Verbose': True, 'MaxMainIter': 50, 'L': L_sc,
                'Backtrack': BacktrackRobust()})

Initialise and run BPDN object

.. code:: ipython3

    b2 = bpdn.BPDN(D, s, lmbda, opt)
    x2 = b2.solve()

    print("BPDN robust PGM backtracking solve time: %.2fs" %
          b2.timer.elapsed('solve'))


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
    BPDN robust PGM backtracking solve time: 0.04s


Plot comparison of reference and recovered representations.

.. code:: ipython3

    plot.plot(np.hstack((x0, x1, x2)), alpha=0.5, title='Sparse representation',
              lgnd=['Reference', 'Reconstructed (Std Backtrack)',
                    'Reconstructed (Robust Backtrack)'])



.. image:: bpdn_pgm_files/bpdn_pgm_15_0.png


Plot functional value, residual, and L

.. code:: ipython3

    its1 = b1.getitstat()
    its2 = b2.getitstat()
    fig = plot.figure(figsize=(21, 7))
    plot.subplot(1, 3, 1)
    plot.plot(its1.ObjFun, xlbl='Iterations', ylbl='Functional', fig=fig)
    plot.plot(its2.ObjFun, xlbl='Iterations', ylbl='Functional',
              lgnd=['Std Backtrack', 'Robust Backtrack'], fig=fig)
    plot.subplot(1, 3, 2)
    plot.plot(its1.Rsdl, ptyp='semilogy', xlbl='Iterations', ylbl='Residual',
              fig=fig)
    plot.plot(its2.Rsdl, ptyp='semilogy', xlbl='Iterations', ylbl='Residual',
              lgnd=['Std Backtrack', 'Robust Backtrack'], fig=fig)
    plot.subplot(1, 3, 3)
    plot.plot(its1.L, xlbl='Iterations', ylbl='Inverse of Step Size', fig=fig)
    plot.plot(its2.L, xlbl='Iterations', ylbl='Inverse of Step Size',
              lgnd=['Std Backtrack', 'Robust Backtrack'], fig=fig)
    fig.show()



.. image:: bpdn_pgm_files/bpdn_pgm_17_0.png

