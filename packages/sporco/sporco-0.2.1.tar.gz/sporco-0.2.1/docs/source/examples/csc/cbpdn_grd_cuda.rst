.. _examples_csc_cbpdn_grd_cuda:

CUDA Convolutional Sparse Coding with Gradient Term
===================================================

This example demonstrates the use of the interface to the CUDA CSC
solver extension package, with a test for the availablity of a GPU that
runs the Python version of the ConvBPDNGradReg solver if one is not
available, or if the extension package is not installed.

.. code:: ipython3

    from __future__ import print_function
    from builtins import input

    import pyfftw   # See https://github.com/pyFFTW/pyFFTW/issues/40
    import numpy as np

    from sporco import util
    from sporco import fft
    from sporco import metric
    from sporco import plot
    plot.config_notebook_plotting()
    from sporco import cuda
    from sporco.admm import cbpdn

    # If running in a notebook, try to use wurlitzer so that output from the CUDA
    # code will be properly captured in the notebook.
    sys_pipes = util.notebook_system_output()

Load example image.

.. code:: ipython3

    img = util.ExampleImages().image('barbara.png', scaled=True, gray=True,
                                     idxexp=np.s_[10:522, 100:612])

Load main dictionary and prepend an impulse filter for lowpass component
representation.

.. code:: ipython3

    Db = util.convdicts()['G:12x12x36']
    di = np.zeros(Db.shape[0:2] + (1,), dtype=np.float32)
    di[0, 0] = 1
    D = np.concatenate((di, Db), axis=2)

Set up weights for the :math:`\ell_1` norm to disable regularization of
the coefficient map corresponding to the impulse filter.

.. code:: ipython3

    wl1 = np.ones((1,)*2 + (D.shape[2:]), dtype=np.float32)
    wl1[..., 0] = 0.0

Set of weights for the :math:`\ell_2` norm of the gradient to disable
regularization of all coefficient maps except for the one corresponding
to the impulse filter.

.. code:: ipython3

    wgr = np.zeros((D.shape[2]), dtype=np.float32)
    wgr[0] = 1.0

Set up :class:`.admm.cbpdn.ConvBPDNGradReg` options.

.. code:: ipython3

    lmbda = 1e-2
    mu = 5e-1
    opt = cbpdn.ConvBPDNGradReg.Options({'Verbose': True, 'MaxMainIter': 250,
                        'HighMemSolve': True, 'RelStopTol': 5e-3,
                        'AuxVarObj': False, 'AutoRho': {'Enabled': False},
                        'rho': 0.5, 'L1Weight': wl1, 'GradWeight': wgr})

If GPU available, run CUDA ConvBPDNGradReg solver, otherwise run
standard Python version.

.. code:: ipython3

    if cuda.device_count() > 0:
        print('%s GPU found: running CUDA solver' % cuda.device_name())
        tm = util.Timer()
        with sys_pipes(), util.ContextTimer(tm):
            X = cuda.cbpdngrd(D, img, lmbda, mu, opt)
        t = tm.elapsed()
    else:
        print('GPU not found: running Python solver')
        c = cbpdn.ConvBPDNGradReg(D, img, lmbda, mu, opt)
        X = c.solve().squeeze()
        t = c.timer.elapsed('solve')
    print('Solve time: %.2f s' % t)


.. parsed-literal::

    GeForce RTX 2080 Ti GPU found: running CUDA solver
    Itn   Fnc       DFid      Regℓ1     Regℓ2∇     r         s         ρ
    --------------------------------------------------------------------------
       0  2.68e+07  1.30e+07  4.85e+04  2.76e+07  4.45e-01  9.48e+00  5.00e-01
       1  6.94e+07  3.32e+07  4.50e+04  7.26e+07  1.19e-01  2.28e+00  5.00e-01
       2  5.95e+07  2.79e+07  3.49e+04  6.33e+07  6.07e-02  7.70e-01  5.00e-01
       3  6.15e+07  2.87e+07  2.79e+04  6.57e+07  4.56e-02  5.12e-01  5.00e-01
       4  6.17e+07  2.87e+07  2.27e+04  6.59e+07  3.64e-02  4.01e-01  5.00e-01
       5  6.17e+07  2.87e+07  1.93e+04  6.60e+07  3.00e-02  3.33e-01  5.00e-01
       6  6.21e+07  2.90e+07  1.65e+04  6.62e+07  2.50e-02  2.85e-01  5.00e-01
       7  6.21e+07  2.89e+07  1.43e+04  6.64e+07  2.09e-02  2.53e-01  5.00e-01
       8  6.22e+07  2.90e+07  1.26e+04  6.66e+07  1.78e-02  2.24e-01  5.00e-01
       9  6.23e+07  2.89e+07  1.12e+04  6.67e+07  1.52e-02  2.01e-01  5.00e-01
      10  6.24e+07  2.90e+07  1.01e+04  6.68e+07  1.32e-02  1.80e-01  5.00e-01
      11  6.24e+07  2.89e+07  9.22e+03  6.69e+07  1.16e-02  1.60e-01  5.00e-01
      12  6.24e+07  2.90e+07  8.53e+03  6.69e+07  1.03e-02  1.43e-01  5.00e-01
      13  6.25e+07  2.90e+07  7.96e+03  6.70e+07  9.15e-03  1.29e-01  5.00e-01
      14  6.26e+07  2.90e+07  7.43e+03  6.71e+07  8.19e-03  1.18e-01  5.00e-01
      15  6.26e+07  2.90e+07  6.99e+03  6.71e+07  7.37e-03  1.09e-01  5.00e-01
      16  6.26e+07  2.91e+07  6.63e+03  6.71e+07  6.68e-03  1.00e-01  5.00e-01
      17  6.27e+07  2.91e+07  6.37e+03  6.71e+07  6.10e-03  9.21e-02  5.00e-01
      18  6.27e+07  2.91e+07  6.15e+03  6.72e+07  5.60e-03  8.43e-02  5.00e-01
      19  6.27e+07  2.91e+07  5.95e+03  6.72e+07  5.16e-03  7.72e-02  5.00e-01
      20  6.27e+07  2.91e+07  5.77e+03  6.72e+07  4.77e-03  7.11e-02  5.00e-01
      21  6.27e+07  2.91e+07  5.60e+03  6.72e+07  4.41e-03  6.61e-02  5.00e-01
      22  6.27e+07  2.91e+07  5.46e+03  6.72e+07  4.09e-03  6.18e-02  5.00e-01
      23  6.27e+07  2.91e+07  5.33e+03  6.72e+07  3.81e-03  5.77e-02  5.00e-01
      24  6.27e+07  2.91e+07  5.23e+03  6.72e+07  3.56e-03  5.36e-02  5.00e-01
      25  6.27e+07  2.91e+07  5.13e+03  6.72e+07  3.33e-03  4.98e-02  5.00e-01
      26  6.27e+07  2.91e+07  5.04e+03  6.72e+07  3.12e-03  4.64e-02  5.00e-01
      27  6.27e+07  2.91e+07  4.96e+03  6.72e+07  2.93e-03  4.34e-02  5.00e-01
      28  6.27e+07  2.91e+07  4.89e+03  6.72e+07  2.76e-03  4.06e-02  5.00e-01
      29  6.27e+07  2.91e+07  4.82e+03  6.72e+07  2.60e-03  3.82e-02  5.00e-01
      30  6.27e+07  2.91e+07  4.76e+03  6.72e+07  2.45e-03  3.60e-02  5.00e-01
      31  6.27e+07  2.91e+07  4.70e+03  6.72e+07  2.32e-03  3.42e-02  5.00e-01
      32  6.27e+07  2.91e+07  4.64e+03  6.72e+07  2.19e-03  3.27e-02  5.00e-01
      33  6.27e+07  2.91e+07  4.59e+03  6.72e+07  2.07e-03  3.12e-02  5.00e-01
      34  6.27e+07  2.91e+07  4.55e+03  6.72e+07  1.96e-03  2.95e-02  5.00e-01
      35  6.27e+07  2.91e+07  4.51e+03  6.72e+07  1.86e-03  2.78e-02  5.00e-01
      36  6.27e+07  2.91e+07  4.48e+03  6.72e+07  1.77e-03  2.61e-02  5.00e-01
      37  6.27e+07  2.91e+07  4.44e+03  6.72e+07  1.69e-03  2.47e-02  5.00e-01
      38  6.27e+07  2.91e+07  4.41e+03  6.72e+07  1.61e-03  2.34e-02  5.00e-01
      39  6.27e+07  2.91e+07  4.38e+03  6.72e+07  1.53e-03  2.23e-02  5.00e-01
      40  6.27e+07  2.91e+07  4.34e+03  6.72e+07  1.46e-03  2.13e-02  5.00e-01
      41  6.27e+07  2.91e+07  4.31e+03  6.72e+07  1.39e-03  2.04e-02  5.00e-01
      42  6.27e+07  2.91e+07  4.29e+03  6.72e+07  1.33e-03  1.95e-02  5.00e-01
      43  6.27e+07  2.91e+07  4.26e+03  6.72e+07  1.27e-03  1.87e-02  5.00e-01
      44  6.27e+07  2.91e+07  4.24e+03  6.72e+07  1.21e-03  1.78e-02  5.00e-01
      45  6.27e+07  2.91e+07  4.22e+03  6.72e+07  1.16e-03  1.70e-02  5.00e-01
      46  6.27e+07  2.91e+07  4.20e+03  6.72e+07  1.11e-03  1.62e-02  5.00e-01
      47  6.27e+07  2.91e+07  4.18e+03  6.72e+07  1.06e-03  1.55e-02  5.00e-01
      48  6.27e+07  2.91e+07  4.16e+03  6.72e+07  1.02e-03  1.49e-02  5.00e-01
      49  6.27e+07  2.91e+07  4.14e+03  6.72e+07  9.72e-04  1.43e-02  5.00e-01
      50  6.27e+07  2.91e+07  4.12e+03  6.72e+07  9.31e-04  1.37e-02  5.00e-01
      51  6.27e+07  2.91e+07  4.10e+03  6.72e+07  8.91e-04  1.32e-02  5.00e-01
      52  6.27e+07  2.91e+07  4.09e+03  6.72e+07  8.55e-04  1.27e-02  5.00e-01
      53  6.27e+07  2.91e+07  4.07e+03  6.72e+07  8.20e-04  1.21e-02  5.00e-01
      54  6.27e+07  2.91e+07  4.06e+03  6.72e+07  7.88e-04  1.16e-02  5.00e-01
      55  6.27e+07  2.91e+07  4.05e+03  6.72e+07  7.57e-04  1.11e-02  5.00e-01
      56  6.27e+07  2.91e+07  4.03e+03  6.72e+07  7.28e-04  1.06e-02  5.00e-01
      57  6.27e+07  2.91e+07  4.02e+03  6.72e+07  6.99e-04  1.02e-02  5.00e-01
      58  6.27e+07  2.91e+07  4.01e+03  6.72e+07  6.71e-04  9.83e-03  5.00e-01
      59  6.27e+07  2.91e+07  4.00e+03  6.72e+07  6.45e-04  9.46e-03  5.00e-01
      60  6.27e+07  2.91e+07  3.99e+03  6.72e+07  6.20e-04  9.11e-03  5.00e-01
      61  6.27e+07  2.91e+07  3.98e+03  6.72e+07  5.97e-04  8.76e-03  5.00e-01
      62  6.27e+07  2.91e+07  3.97e+03  6.72e+07  5.74e-04  8.42e-03  5.00e-01
      63  6.27e+07  2.91e+07  3.96e+03  6.72e+07  5.53e-04  8.11e-03  5.00e-01
      64  6.27e+07  2.91e+07  3.95e+03  6.72e+07  5.32e-04  7.83e-03  5.00e-01
      65  6.27e+07  2.91e+07  3.94e+03  6.72e+07  5.12e-04  7.56e-03  5.00e-01
      66  6.27e+07  2.91e+07  3.93e+03  6.72e+07  4.93e-04  7.29e-03  5.00e-01
      67  6.27e+07  2.91e+07  3.93e+03  6.72e+07  4.75e-04  7.03e-03  5.00e-01
      68  6.27e+07  2.91e+07  3.92e+03  6.72e+07  4.58e-04  6.77e-03  5.00e-01
      69  6.27e+07  2.91e+07  3.91e+03  6.72e+07  4.42e-04  6.50e-03  5.00e-01
      70  6.27e+07  2.91e+07  3.91e+03  6.72e+07  4.27e-04  6.26e-03  5.00e-01
      71  6.27e+07  2.91e+07  3.90e+03  6.72e+07  4.12e-04  6.04e-03  5.00e-01
      72  6.27e+07  2.91e+07  3.89e+03  6.72e+07  3.97e-04  5.84e-03  5.00e-01
      73  6.27e+07  2.91e+07  3.89e+03  6.72e+07  3.83e-04  5.65e-03  5.00e-01
      74  6.27e+07  2.91e+07  3.88e+03  6.72e+07  3.70e-04  5.47e-03  5.00e-01
      75  6.27e+07  2.91e+07  3.87e+03  6.72e+07  3.57e-04  5.29e-03  5.00e-01
      76  6.27e+07  2.91e+07  3.87e+03  6.72e+07  3.45e-04  5.11e-03  5.00e-01
      77  6.27e+07  2.91e+07  3.86e+03  6.72e+07  3.33e-04  4.95e-03  5.00e-01
    --------------------------------------------------------------------------
    Solve time: 0.98 s


Reconstruct the image from the sparse representation.

.. code:: ipython3

    imgr = np.sum(fft.fftconv(D, X, axes=(0, 1)), axis=2)
    print("Reconstruction PSNR: %.2fdB\n" % metric.psnr(img, imgr))


.. parsed-literal::

    Reconstruction PSNR: 45.50dB



Display representation and reconstructed image.

.. code:: ipython3

    fig = plot.figure(figsize=(14, 14))
    plot.subplot(2, 2, 1)
    plot.imview(X[..., 0].squeeze(), title='Lowpass component', fig=fig)
    plot.subplot(2, 2, 2)
    plot.imview(np.sum(abs(X[..., 1:]), axis=2).squeeze(),
                cmap=plot.cm.Blues, title='Main representation', fig=fig)
    plot.subplot(2, 2, 3)
    plot.imview(imgr, title='Reconstructed image', fig=fig)
    plot.subplot(2, 2, 4)
    plot.imview(imgr - img, fltscl=True, title='Reconstruction difference',
                fig=fig)
    fig.show()



.. image:: cbpdn_grd_cuda_files/cbpdn_grd_cuda_17_0.png

