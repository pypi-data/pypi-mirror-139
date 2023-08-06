.. _examples_cdl_onlinecdl_gry:

Online Convolutional Dictionary Learning
========================================

This example demonstrates the use of
:class:`.dictlrn.onlinecdl.OnlineConvBPDNDictLearn` for learning a
convolutional dictionary from a set of training images. The dictionary
is learned using the online dictionary learning algorithm proposed in
:cite:`liu-2018-first`.

.. code:: ipython3

    from __future__ import print_function
    from builtins import input

    import pyfftw   # See https://github.com/pyFFTW/pyFFTW/issues/40
    import numpy as np

    from sporco.dictlrn import onlinecdl
    from sporco import util
    from sporco import signal
    from sporco import cuda
    from sporco import plot
    plot.config_notebook_plotting()

Load training images.

.. code:: ipython3

    exim = util.ExampleImages(scaled=True, zoom=0.25, gray=True)
    S1 = exim.image('barbara.png', idxexp=np.s_[10:522, 100:612])
    S2 = exim.image('kodim23.png', idxexp=np.s_[:, 60:572])
    S3 = exim.image('monarch.png', idxexp=np.s_[:, 160:672])
    S4 = exim.image('sail.png', idxexp=np.s_[:, 210:722])
    S5 = exim.image('tulips.png', idxexp=np.s_[:, 30:542])
    S = np.dstack((S1, S2, S3, S4, S5))

Highpass filter training images.

.. code:: ipython3

    npd = 16
    fltlmbd = 5
    sl, sh = signal.tikhonov_filter(S, fltlmbd, npd)

Construct initial dictionary.

.. code:: ipython3

    np.random.seed(12345)
    D0 = np.random.randn(8, 8, 64)

Set regularization parameter and options for dictionary learning solver.

.. code:: ipython3

    lmbda = 0.2
    opt = onlinecdl.OnlineConvBPDNDictLearn.Options({
                    'Verbose': True, 'ZeroMean': False, 'eta_a': 10.0,
                    'eta_b': 20.0, 'DataType': np.float32,
                    'CBPDN': {'rho': 5.0, 'AutoRho': {'Enabled': True},
                        'RelaxParam': 1.8, 'RelStopTol': 1e-4, 'MaxMainIter': 50,
                        'FastSolve': False, 'DataType': np.float32}})
    if cuda.device_count() > 0:
        opt['CUDA_CBPDN'] = True

Create solver object and solve.

.. code:: ipython3

    d = onlinecdl.OnlineConvBPDNDictLearn(D0, lmbda, opt)

    iter = 50
    d.display_start()
    for it in range(iter):
        img_index = np.random.randint(0, sh.shape[-1])
        d.solve(sh[..., [img_index]])

    d.display_end()
    D1 = d.getdict()
    print("OnlineConvBPDNDictLearn solve time: %.2fs" % d.timer.elapsed('solve'))


.. parsed-literal::

    Itn   X r       X s       X ρ       D cnstr   D dlt     D η
    ----------------------------------------------------------------
       0  0.00e+00  0.00e+00  0.00e+00  2.19e+01  2.21e+00  5.00e-01
       1  0.00e+00  0.00e+00  0.00e+00  1.38e+01  1.26e+00  4.76e-01
       2  0.00e+00  0.00e+00  0.00e+00  1.69e+01  1.55e+00  4.55e-01
       3  0.00e+00  0.00e+00  0.00e+00  1.58e+01  1.05e+00  4.35e-01
       4  0.00e+00  0.00e+00  0.00e+00  1.23e+01  9.21e-01  4.17e-01
       5  0.00e+00  0.00e+00  0.00e+00  1.19e+01  7.16e-01  4.00e-01
       6  0.00e+00  0.00e+00  0.00e+00  1.21e+01  6.27e-01  3.85e-01
       7  0.00e+00  0.00e+00  0.00e+00  1.09e+01  7.06e-01  3.70e-01
       8  0.00e+00  0.00e+00  0.00e+00  1.06e+01  5.59e-01  3.57e-01
       9  0.00e+00  0.00e+00  0.00e+00  1.10e+01  5.90e-01  3.45e-01
      10  0.00e+00  0.00e+00  0.00e+00  1.21e+01  9.16e-01  3.33e-01
      11  0.00e+00  0.00e+00  0.00e+00  9.64e+00  5.41e-01  3.23e-01
      12  0.00e+00  0.00e+00  0.00e+00  1.17e+01  7.33e-01  3.12e-01
      13  0.00e+00  0.00e+00  0.00e+00  1.06e+01  6.20e-01  3.03e-01
      14  0.00e+00  0.00e+00  0.00e+00  8.78e+00  4.96e-01  2.94e-01
      15  0.00e+00  0.00e+00  0.00e+00  8.62e+00  4.16e-01  2.86e-01
      16  0.00e+00  0.00e+00  0.00e+00  3.95e+00  4.14e-01  2.78e-01
      17  0.00e+00  0.00e+00  0.00e+00  8.55e+00  5.15e-01  2.70e-01
      18  0.00e+00  0.00e+00  0.00e+00  7.93e+00  3.89e-01  2.63e-01
      19  0.00e+00  0.00e+00  0.00e+00  9.75e+00  7.09e-01  2.56e-01
      20  0.00e+00  0.00e+00  0.00e+00  3.62e+00  3.75e-01  2.50e-01
      21  0.00e+00  0.00e+00  0.00e+00  7.37e+00  3.72e-01  2.44e-01
      22  0.00e+00  0.00e+00  0.00e+00  7.25e+00  3.18e-01  2.38e-01
      23  0.00e+00  0.00e+00  0.00e+00  7.96e+00  4.86e-01  2.33e-01
      24  0.00e+00  0.00e+00  0.00e+00  3.32e+00  3.31e-01  2.27e-01
      25  0.00e+00  0.00e+00  0.00e+00  8.57e+00  6.04e-01  2.22e-01
      26  0.00e+00  0.00e+00  0.00e+00  6.86e+00  4.30e-01  2.17e-01
      27  0.00e+00  0.00e+00  0.00e+00  3.17e+00  3.07e-01  2.13e-01
      28  0.00e+00  0.00e+00  0.00e+00  6.79e+00  3.93e-01  2.08e-01
      29  0.00e+00  0.00e+00  0.00e+00  7.07e+00  4.01e-01  2.04e-01
      30  0.00e+00  0.00e+00  0.00e+00  7.05e+00  3.28e-01  2.00e-01
      31  0.00e+00  0.00e+00  0.00e+00  5.87e+00  3.54e-01  1.96e-01
      32  0.00e+00  0.00e+00  0.00e+00  7.45e+00  5.40e-01  1.92e-01
      33  0.00e+00  0.00e+00  0.00e+00  2.83e+00  2.82e-01  1.89e-01
      34  0.00e+00  0.00e+00  0.00e+00  5.59e+00  3.17e-01  1.85e-01
      35  0.00e+00  0.00e+00  0.00e+00  6.41e+00  3.35e-01  1.82e-01
      36  0.00e+00  0.00e+00  0.00e+00  2.72e+00  2.61e-01  1.79e-01
      37  0.00e+00  0.00e+00  0.00e+00  6.88e+00  4.73e-01  1.75e-01
      38  0.00e+00  0.00e+00  0.00e+00  6.82e+00  3.93e-01  1.72e-01
      39  0.00e+00  0.00e+00  0.00e+00  5.39e+00  3.47e-01  1.69e-01
      40  0.00e+00  0.00e+00  0.00e+00  5.90e+00  3.17e-01  1.67e-01
      41  0.00e+00  0.00e+00  0.00e+00  4.94e+00  3.06e-01  1.64e-01
      42  0.00e+00  0.00e+00  0.00e+00  5.24e+00  3.21e-01  1.61e-01
      43  0.00e+00  0.00e+00  0.00e+00  2.42e+00  2.42e-01  1.59e-01
      44  0.00e+00  0.00e+00  0.00e+00  5.19e+00  2.98e-01  1.56e-01
      45  0.00e+00  0.00e+00  0.00e+00  5.43e+00  2.88e-01  1.54e-01
      46  0.00e+00  0.00e+00  0.00e+00  5.09e+00  2.84e-01  1.52e-01
      47  0.00e+00  0.00e+00  0.00e+00  5.30e+00  2.61e-01  1.49e-01
      48  0.00e+00  0.00e+00  0.00e+00  5.28e+00  2.25e-01  1.47e-01
      49  0.00e+00  0.00e+00  0.00e+00  5.25e+00  2.02e-01  1.45e-01
    ----------------------------------------------------------------
    OnlineConvBPDNDictLearn solve time: 5.84s


Display initial and final dictionaries.

.. code:: ipython3

    D1 = D1.squeeze()
    fig = plot.figure(figsize=(14, 7))
    plot.subplot(1, 2, 1)
    plot.imview(util.tiledict(D0), title='D0', fig=fig)
    plot.subplot(1, 2, 2)
    plot.imview(util.tiledict(D1), title='D1', fig=fig)
    fig.show()



.. image:: onlinecdl_gry_files/onlinecdl_gry_13_0.png


Get iterations statistics from solver object and plot functional value.

.. code:: ipython3

    its = d.getitstat()
    fig = plot.figure(figsize=(7, 7))
    plot.plot(np.vstack((its.DeltaD, its.Eta)).T, xlbl='Iterations',
              lgnd=('Delta D', 'Eta'), fig=fig)
    fig.show()



.. image:: onlinecdl_gry_files/onlinecdl_gry_15_0.png

