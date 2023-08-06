.. _examples_csc_cbpdnin_gry:

Single-channel CSC With Lateral Inhibition / No Self Inhibition
===============================================================

This example demonstrates solving a convolutional sparse coding problem
with a greyscale signal

.. math:: \mathrm{argmin}_\mathbf{x} \; \frac{1}{2} \left\| \sum_m \mathbf{d}_m * \mathbf{x}_{m} - \mathbf{s} \right\|_2^2 + \lambda \sum_m \| \mathbf{x}_{m} \|_1 + \sum_m \boldsymbol{\omega}^T_m | \mathbf{x}_m | + \sum_m \mathbf{z}^T_m | \mathbf{x}_m | \;,

where :math:`\mathbf{d}_{m}` is the :math:`m^{\text{th}}` dictionary
filter, :math:`\mathbf{x}_{m}` is the coefficient map corresponding to
the :math:`m^{\text{th}}` dictionary filter, :math:`\mathbf{s}` is the
input image, and :math:`\boldsymbold{\omega}^T_m` and
:math:`\mathbf{z}^T_m` are inhibition weights corresponding to lateral
and self inhibition, respectively (see
:class:`.admm.cbpdnin.ConvBPDNInhib`).

.. code:: ipython3

    from __future__ import print_function
    from builtins import input

    import numpy as np

    from sporco import util
    from sporco import signal
    from sporco import plot
    plot.config_notebook_plotting()
    import sporco.metric as sm
    from sporco.admm import cbpdnin

Load example image.

.. code:: ipython3

    img = util.ExampleImages().image('kodim23.png', scaled=True, gray=True,
                                     idxexp=np.s_[160:416, 60:316])

Highpass filter example image.

.. code:: ipython3

    npd = 16
    fltlmbd = 10
    sl, sh = signal.tikhonov_filter(img, fltlmbd, npd)

Load dictionary and display it.

.. code:: ipython3

    D = util.convdicts()['G:12x12x36']
    # Repeat the dictionary twice, adding noise to each respective pair
    D = np.append(D + 0.01 * np.random.randn(*D.shape),
                  D + 0.01 * np.random.randn(*D.shape), axis=-1)
    plot.imview(util.tiledict(D), fgsz=(10, 10))



.. image:: cbpdnin_gry_files/cbpdnin_gry_7_0.png


Set :class:`.admm.cbpdnin.ConvBPDNInhib` solver options.

.. code:: ipython3

    lmbda = 5e-2
    mu = 5e-2
    opt = cbpdnin.ConvBPDNInhib.Options({'Verbose': True, 'MaxMainIter': 200,
                                         'RelStopTol': 5e-3, 'AuxVarObj': False})

Initialise and run CSC solver.

.. code:: ipython3

    # Create the Ng x M grouping matrix, where Ng is the number of groups,
    # and M is the number of dictionary elements. A non-zero entry at
    # Wg(n, m), means that element m belongs to group n. Our dictionary
    # was repeated contiguously, so elements i and i + 36 are paired for
    # i = 0, ..., 35.
    Wg = np.append(np.eye(36), np.eye(36), axis=-1)
    # We additionally choose a rectangular inhibition window of sample
    # diameter 12.
    b = cbpdnin.ConvBPDNInhib(D, sh, Wg, 12, ('boxcar'),
                              lmbda, mu, None, opt, dimK=0)
    X = b.solve()
    print("ConvBPDN solve time: %.2fs" % b.timer.elapsed('solve'))


.. parsed-literal::

    Itn   Fnc       DFid      Regℓ1     RegLat    RegSelf   r         s         ρ
    ------------------------------------------------------------------------------------
       0  7.64e+01  2.38e-01  1.50e+03  2.20e+01  0.00e+00  9.82e-01  6.16e-02  3.50e+00
       1  6.94e+01  1.40e+00  1.32e+03  3.60e+01  0.00e+00  8.54e-01  2.05e-01  3.50e+00
       2  6.02e+01  2.72e+00  1.10e+03  4.52e+01  0.00e+00  4.24e-01  2.86e-01  6.00e+00
       3  5.93e+01  3.50e+00  1.05e+03  6.98e+01  0.00e+00  2.75e-01  2.36e-01  6.00e+00
       4  5.85e+01  3.76e+00  1.01e+03  8.61e+01  0.00e+00  2.38e-01  1.68e-01  5.44e+00
       5  5.25e+01  4.07e+00  8.82e+02  8.69e+01  0.00e+00  2.06e-01  1.39e-01  5.44e+00
       6  4.90e+01  4.47e+00  8.03e+02  8.74e+01  0.00e+00  1.80e-01  1.08e-01  5.44e+00
       7  4.71e+01  4.82e+00  7.56e+02  9.02e+01  0.00e+00  1.49e-01  8.85e-02  5.44e+00
       8  4.55e+01  5.05e+00  7.15e+02  9.49e+01  0.00e+00  1.21e-01  7.86e-02  5.44e+00
       9  4.44e+01  5.18e+00  6.85e+02  9.86e+01  0.00e+00  1.02e-01  7.14e-02  5.44e+00
      10  4.37e+01  5.25e+00  6.67e+02  1.01e+02  0.00e+00  8.90e-02  6.15e-02  5.44e+00
      11  4.24e+01  5.33e+00  6.40e+02  1.01e+02  0.00e+00  7.88e-02  5.34e-02  5.44e+00
      12  4.07e+01  5.43e+00  6.06e+02  9.99e+01  0.00e+00  6.95e-02  4.96e-02  5.44e+00
      13  3.96e+01  5.52e+00  5.82e+02  9.95e+01  0.00e+00  6.15e-02  4.57e-02  5.44e+00
      14  3.90e+01  5.60e+00  5.67e+02  1.00e+02  0.00e+00  5.49e-02  4.07e-02  5.44e+00
      15  3.84e+01  5.65e+00  5.54e+02  1.00e+02  0.00e+00  4.92e-02  3.72e-02  5.44e+00
      16  3.77e+01  5.69e+00  5.40e+02  9.96e+01  0.00e+00  4.43e-02  3.51e-02  5.44e+00
      17  3.71e+01  5.72e+00  5.30e+02  9.87e+01  0.00e+00  4.04e-02  3.26e-02  5.44e+00
      18  3.66e+01  5.74e+00  5.19e+02  9.75e+01  0.00e+00  3.71e-02  3.07e-02  5.44e+00
      19  3.60e+01  5.77e+00  5.08e+02  9.61e+01  0.00e+00  3.42e-02  2.97e-02  5.44e+00
      20  3.56e+01  5.79e+00  5.01e+02  9.48e+01  0.00e+00  3.39e-02  2.85e-02  4.91e+00
      21  3.54e+01  5.81e+00  4.98e+02  9.35e+01  0.00e+00  3.20e-02  2.70e-02  4.91e+00
      22  3.51e+01  5.81e+00  4.94e+02  9.19e+01  0.00e+00  3.02e-02  2.59e-02  4.91e+00
      23  3.48e+01  5.81e+00  4.90e+02  8.99e+01  0.00e+00  3.04e-02  2.52e-02  4.45e+00
      24  3.46e+01  5.81e+00  4.88e+02  8.77e+01  0.00e+00  2.90e-02  2.44e-02  4.45e+00
      25  3.44e+01  5.80e+00  4.87e+02  8.55e+01  0.00e+00  2.78e-02  2.34e-02  4.45e+00
      26  3.41e+01  5.79e+00  4.84e+02  8.32e+01  0.00e+00  2.66e-02  2.29e-02  4.45e+00
      27  3.38e+01  5.78e+00  4.81e+02  8.08e+01  0.00e+00  2.73e-02  2.24e-02  4.03e+00
      28  3.36e+01  5.76e+00  4.79e+02  7.83e+01  0.00e+00  2.63e-02  2.19e-02  4.03e+00
      29  3.34e+01  5.75e+00  4.78e+02  7.57e+01  0.00e+00  2.53e-02  2.11e-02  4.03e+00
      30  3.32e+01  5.74e+00  4.76e+02  7.29e+01  0.00e+00  2.43e-02  2.08e-02  4.03e+00
      31  3.29e+01  5.73e+00  4.74e+02  7.00e+01  0.00e+00  2.50e-02  2.04e-02  3.67e+00
      32  3.28e+01  5.71e+00  4.74e+02  6.72e+01  0.00e+00  2.42e-02  1.97e-02  3.67e+00
      33  3.26e+01  5.70e+00  4.74e+02  6.44e+01  0.00e+00  2.34e-02  1.91e-02  3.67e+00
      34  3.25e+01  5.68e+00  4.75e+02  6.18e+01  0.00e+00  2.27e-02  1.85e-02  3.67e+00
      35  3.23e+01  5.67e+00  4.74e+02  5.91e+01  0.00e+00  2.16e-02  1.78e-02  3.67e+00
      36  3.21e+01  5.65e+00  4.72e+02  5.65e+01  0.00e+00  2.10e-02  1.76e-02  3.67e+00
      37  3.18e+01  5.63e+00  4.70e+02  5.39e+01  0.00e+00  2.01e-02  1.72e-02  3.67e+00
      38  3.16e+01  5.62e+00  4.68e+02  5.13e+01  0.00e+00  2.07e-02  1.67e-02  3.34e+00
      39  3.14e+01  5.61e+00  4.67e+02  4.89e+01  0.00e+00  1.97e-02  1.60e-02  3.34e+00
      40  3.12e+01  5.60e+00  4.66e+02  4.66e+01  0.00e+00  1.92e-02  1.56e-02  3.34e+00
      41  3.11e+01  5.59e+00  4.65e+02  4.44e+01  0.00e+00  1.85e-02  1.52e-02  3.34e+00
      42  3.09e+01  5.58e+00  4.64e+02  4.22e+01  0.00e+00  1.79e-02  1.46e-02  3.34e+00
      43  3.07e+01  5.57e+00  4.63e+02  4.02e+01  0.00e+00  1.72e-02  1.41e-02  3.34e+00
      44  3.05e+01  5.56e+00  4.61e+02  3.83e+01  0.00e+00  1.67e-02  1.37e-02  3.34e+00
      45  3.04e+01  5.55e+00  4.60e+02  3.64e+01  0.00e+00  1.60e-02  1.34e-02  3.34e+00
      46  3.02e+01  5.55e+00  4.58e+02  3.46e+01  0.00e+00  1.55e-02  1.32e-02  3.34e+00
      47  3.00e+01  5.54e+00  4.57e+02  3.28e+01  0.00e+00  1.59e-02  1.27e-02  3.04e+00
      48  2.99e+01  5.54e+00  4.57e+02  3.13e+01  0.00e+00  1.54e-02  1.23e-02  3.04e+00
      49  2.98e+01  5.53e+00  4.56e+02  2.99e+01  0.00e+00  1.49e-02  1.17e-02  3.04e+00
      50  2.98e+01  5.52e+00  4.56e+02  2.86e+01  0.00e+00  1.45e-02  1.13e-02  3.04e+00
      51  2.97e+01  5.52e+00  4.56e+02  2.74e+01  0.00e+00  1.41e-02  1.09e-02  3.04e+00
      52  2.95e+01  5.51e+00  4.54e+02  2.61e+01  0.00e+00  1.36e-02  1.06e-02  3.04e+00
      53  2.94e+01  5.51e+00  4.52e+02  2.48e+01  0.00e+00  1.32e-02  1.04e-02  3.04e+00
      54  2.92e+01  5.50e+00  4.51e+02  2.36e+01  0.00e+00  1.29e-02  1.02e-02  3.04e+00
      55  2.91e+01  5.50e+00  4.49e+02  2.24e+01  0.00e+00  1.24e-02  1.00e-02  3.04e+00
      56  2.89e+01  5.50e+00  4.47e+02  2.13e+01  0.00e+00  1.21e-02  9.82e-03  3.04e+00
      57  2.88e+01  5.49e+00  4.46e+02  2.04e+01  0.00e+00  1.18e-02  9.62e-03  3.04e+00
      58  2.87e+01  5.49e+00  4.45e+02  1.95e+01  0.00e+00  1.14e-02  9.31e-03  3.04e+00
      59  2.86e+01  5.49e+00  4.44e+02  1.87e+01  0.00e+00  1.11e-02  9.04e-03  3.04e+00
      60  2.85e+01  5.49e+00  4.43e+02  1.79e+01  0.00e+00  1.08e-02  8.88e-03  3.04e+00
      61  2.84e+01  5.48e+00  4.42e+02  1.72e+01  0.00e+00  1.05e-02  8.60e-03  3.04e+00
      62  2.83e+01  5.48e+00  4.41e+02  1.65e+01  0.00e+00  1.02e-02  8.37e-03  3.04e+00
      63  2.82e+01  5.48e+00  4.39e+02  1.58e+01  0.00e+00  9.90e-03  8.17e-03  3.04e+00
      64  2.81e+01  5.48e+00  4.38e+02  1.51e+01  0.00e+00  9.57e-03  7.90e-03  3.04e+00
      65  2.80e+01  5.48e+00  4.36e+02  1.45e+01  0.00e+00  9.29e-03  7.72e-03  3.04e+00
      66  2.79e+01  5.48e+00  4.35e+02  1.39e+01  0.00e+00  9.02e-03  7.52e-03  3.04e+00
      67  2.78e+01  5.48e+00  4.34e+02  1.34e+01  0.00e+00  8.76e-03  7.32e-03  3.04e+00
      68  2.78e+01  5.48e+00  4.33e+02  1.28e+01  0.00e+00  8.52e-03  7.12e-03  3.04e+00
      69  2.77e+01  5.48e+00  4.32e+02  1.24e+01  0.00e+00  8.29e-03  6.94e-03  3.04e+00
      70  2.76e+01  5.48e+00  4.31e+02  1.19e+01  0.00e+00  8.06e-03  6.82e-03  3.04e+00
      71  2.76e+01  5.47e+00  4.30e+02  1.15e+01  0.00e+00  7.81e-03  6.66e-03  3.04e+00
      72  2.75e+01  5.47e+00  4.29e+02  1.11e+01  0.00e+00  8.06e-03  6.50e-03  2.77e+00
      73  2.75e+01  5.47e+00  4.29e+02  1.08e+01  0.00e+00  7.91e-03  6.39e-03  2.77e+00
      74  2.74e+01  5.47e+00  4.29e+02  1.04e+01  0.00e+00  7.74e-03  6.14e-03  2.77e+00
      75  2.74e+01  5.47e+00  4.28e+02  1.01e+01  0.00e+00  7.56e-03  5.99e-03  2.77e+00
      76  2.74e+01  5.47e+00  4.28e+02  9.83e+00  0.00e+00  7.40e-03  5.85e-03  2.77e+00
      77  2.73e+01  5.47e+00  4.27e+02  9.55e+00  0.00e+00  7.25e-03  5.71e-03  2.77e+00
      78  2.73e+01  5.47e+00  4.27e+02  9.27e+00  0.00e+00  7.08e-03  5.58e-03  2.77e+00
      79  2.72e+01  5.47e+00  4.26e+02  9.01e+00  0.00e+00  6.91e-03  5.44e-03  2.77e+00
      80  2.72e+01  5.47e+00  4.25e+02  8.77e+00  0.00e+00  6.77e-03  5.22e-03  2.77e+00
      81  2.71e+01  5.47e+00  4.25e+02  8.55e+00  0.00e+00  6.59e-03  5.09e-03  2.77e+00
      82  2.71e+01  5.47e+00  4.24e+02  8.33e+00  0.00e+00  6.42e-03  4.99e-03  2.77e+00
      83  2.70e+01  5.47e+00  4.23e+02  8.11e+00  0.00e+00  6.26e-03  4.91e-03  2.77e+00
      84  2.70e+01  5.47e+00  4.22e+02  7.90e+00  0.00e+00  6.12e-03  4.81e-03  2.77e+00
      85  2.69e+01  5.47e+00  4.22e+02  7.70e+00  0.00e+00  5.97e-03  4.71e-03  2.77e+00
      86  2.69e+01  5.47e+00  4.21e+02  7.51e+00  0.00e+00  5.85e-03  4.62e-03  2.77e+00
      87  2.68e+01  5.47e+00  4.20e+02  7.33e+00  0.00e+00  5.72e-03  4.54e-03  2.77e+00
      88  2.68e+01  5.47e+00  4.20e+02  7.16e+00  0.00e+00  5.61e-03  4.45e-03  2.77e+00
      89  2.68e+01  5.47e+00  4.19e+02  7.01e+00  0.00e+00  5.50e-03  4.39e-03  2.77e+00
      90  2.67e+01  5.47e+00  4.19e+02  6.85e+00  0.00e+00  5.37e-03  4.30e-03  2.77e+00
      91  2.67e+01  5.47e+00  4.18e+02  6.72e+00  0.00e+00  5.30e-03  4.15e-03  2.77e+00
      92  2.67e+01  5.47e+00  4.18e+02  6.59e+00  0.00e+00  5.19e-03  4.09e-03  2.77e+00
      93  2.66e+01  5.47e+00  4.17e+02  6.45e+00  0.00e+00  5.08e-03  4.03e-03  2.77e+00
      94  2.66e+01  5.47e+00  4.17e+02  6.32e+00  0.00e+00  4.98e-03  3.96e-03  2.77e+00
    ------------------------------------------------------------------------------------
    ConvBPDN solve time: 47.68s


Reconstruct image from sparse representation.

.. code:: ipython3

    shr = b.reconstruct().squeeze()
    imgr = sl + shr
    print("Reconstruction PSNR: %.2fdB\n" % sm.psnr(img, imgr))


.. parsed-literal::

    Reconstruction PSNR: 37.23dB



Display low pass component and sum of absolute values of coefficient
maps of highpass component.

.. code:: ipython3

    fig = plot.figure(figsize=(14, 7))
    plot.subplot(1, 2, 1)
    plot.imview(sl, title='Lowpass component', fig=fig)
    plot.subplot(1, 2, 2)
    plot.imview(np.sum(abs(X), axis=b.cri.axisM).squeeze(), cmap=plot.cm.Blues,
                title='Sparse representation', fig=fig)
    fig.show()



.. image:: cbpdnin_gry_files/cbpdnin_gry_15_0.png


Show activation of grouped elements column-wise for first four groups.
As mu is lowered, the vertical pairs should look more and more similar.
You will likely need to zoom in to see the activations clearly.

.. code:: ipython3

    fig = plot.figure(figsize=(14, 7))
    for i in range(4):
        plot.subplot(2, 4, i + 1)
        plot.imview(abs(X[:, :, :, :, i]).squeeze(), cmap=plot.cm.Blues,
                    title=f'X[{i}]', fig=fig)
        plot.subplot(2, 4, i + 5)
        plot.imview(abs(X[:, :, :, :, i + 36]).squeeze(), cmap=plot.cm.Blues,
                    title=f'X[{i+36}]', fig=fig)
    fig.show()



.. image:: cbpdnin_gry_files/cbpdnin_gry_17_0.png


Display original and reconstructed images.

.. code:: ipython3

    fig = plot.figure(figsize=(14, 7))
    plot.subplot(1, 2, 1)
    plot.imview(img, title='Original', fig=fig)
    plot.subplot(1, 2, 2)
    plot.imview(imgr, title='Reconstructed', fig=fig)
    fig.show()



.. image:: cbpdnin_gry_files/cbpdnin_gry_19_0.png


Get iterations statistics from solver object and plot functional value,
ADMM primary and dual residuals, and automatically adjusted ADMM penalty
parameter against the iteration number.

.. code:: ipython3

    its = b.getitstat()
    fig = plot.figure(figsize=(20, 5))
    plot.subplot(1, 3, 1)
    plot.plot(its.ObjFun, xlbl='Iterations', ylbl='Functional', fig=fig)
    plot.subplot(1, 3, 2)
    plot.plot(np.vstack((its.PrimalRsdl, its.DualRsdl)).T,
              ptyp='semilogy', xlbl='Iterations', ylbl='Residual',
              lgnd=['Primal', 'Dual'], fig=fig)
    plot.subplot(1, 3, 3)
    plot.plot(its.Rho, xlbl='Iterations', ylbl='Penalty Parameter', fig=fig)
    fig.show()



.. image:: cbpdnin_gry_files/cbpdnin_gry_21_0.png

