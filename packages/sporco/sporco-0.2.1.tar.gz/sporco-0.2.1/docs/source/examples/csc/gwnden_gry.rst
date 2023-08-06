.. _examples_csc_gwnden_gry:

Gaussian White Noise Restoration via CSC
========================================

This example demonstrates the removal of Gaussian white noise from a
greyscale image using the CSC problem

.. math:: \mathrm{argmin}_\mathbf{x} \; (1/2) \sum_c \left\| \sum_m \mathbf{d}_{c,m} * \mathbf{x}_m -\mathbf{s}_c \right\|_2^2 + \lambda \sum_m \| \mathbf{x}_m \|_1 \;,

where :math:`\mathbf{d}_m` is the :math:`m^{\text{th}}` dictionary
filter, :math:`\mathbf{x}_m` is the coefficient map corresponding to the
:math:`m^{\text{th}}` dictionary filter, :math:`\mathbf{s}` is the input
image.

.. code:: ipython3

    from __future__ import print_function
    from builtins import input

    import pyfftw   # See https://github.com/pyFFTW/pyFFTW/issues/40
    import numpy as np

    from sporco import util
    from sporco import signal
    from sporco import fft
    from sporco import metric
    from sporco import plot
    plot.config_notebook_plotting()
    from sporco.admm import cbpdn

Boundary artifacts are handled by performing a symmetric extension on
the image to be denoised and then cropping the result to the original
image support. This approach is simpler than the boundary handling
strategies that involve the insertion of a spatial mask into the data
fidelity term, and for many problems gives results of comparable
quality. The functions defined here implement symmetric extension and
cropping of images.

.. code:: ipython3

    def pad(x, n=8):

        if x.ndim == 2:
            return np.pad(x, n, mode='symmetric')
        else:
            return np.pad(x, ((n, n), (n, n), (0, 0)), mode='symmetric')


    def crop(x, n=8):

        return x[n:-n, n:-n]

Load a reference image and corrupt it with Gaussian white noise with
:math:`\sigma = 0.1`. (The call to ``numpy.random.seed`` ensures that
the pseudo-random noise is reproducible.)

.. code:: ipython3

    img = util.ExampleImages().image('monarch.png', zoom=0.5, scaled=True,
                                     gray=True, idxexp=np.s_[:, 160:672])
    np.random.seed(12345)
    imgn = img + np.random.normal(0.0, 0.1, img.shape).astype(np.float32)

Highpass filter test image.

.. code:: ipython3

    npd = 16
    fltlmbd = 5.0
    imgnl, imgnh = signal.tikhonov_filter(imgn, fltlmbd, npd)

Load dictionary.

.. code:: ipython3

    D = util.convdicts()['G:8x8x128']

Set solver options. See Section 8 of
:cite:`wohlberg-2017-convolutional2` for details of construction of
:math:`\ell_1` weighting matrix :math:`W`.

.. code:: ipython3

    imgnpl, imgnph = signal.tikhonov_filter(pad(imgn), fltlmbd, npd)
    W = fft.irfftn(np.conj(fft.rfftn(D, imgnph.shape, (0, 1))) *
                   fft.rfftn(imgnph[..., np.newaxis], None, (0, 1)),
                   imgnph.shape, (0,1))
    W = W**2
    W = 1.0/(np.maximum(np.abs(W), 1e-8))

    lmbda = 4.8e-2

    opt = cbpdn.ConvBPDN.Options({'Verbose': True, 'MaxMainIter': 250,
                'HighMemSolve': True, 'RelStopTol': 3e-3, 'AuxVarObj': False,
                'L1Weight': W, 'AutoRho': {'Enabled': False}, 'rho': 4e2*lmbda})

Initialise the :class:`.admm.cbpdn.ConvBPDN` object and call the
``solve`` method.

.. code:: ipython3

    b = cbpdn.ConvBPDN(D, pad(imgnh), lmbda, opt, dimK=0)
    X = b.solve()


.. parsed-literal::

    Itn   Fnc       DFid      Regℓ1     r         s
    ------------------------------------------------------
       0  2.11e+07  4.04e+01  4.39e+08  9.77e-01  1.21e-01
       1  9.07e+06  1.43e+02  1.89e+08  7.52e-01  2.18e-01
       2  5.38e+06  1.86e+02  1.12e+08  3.36e-01  1.98e-01
       3  4.58e+06  2.12e+02  9.54e+07  2.41e-01  1.19e-01
       4  3.64e+06  2.28e+02  7.58e+07  1.87e-01  1.03e-01
       5  3.15e+06  2.42e+02  6.55e+07  1.50e-01  9.11e-02
       6  2.80e+06  2.53e+02  5.84e+07  1.27e-01  6.88e-02
       7  2.57e+06  2.61e+02  5.36e+07  1.05e-01  5.40e-02
       8  2.36e+06  2.68e+02  4.91e+07  8.55e-02  4.80e-02
       9  2.17e+06  2.72e+02  4.52e+07  7.04e-02  4.44e-02
      10  2.00e+06  2.75e+02  4.16e+07  5.93e-02  3.99e-02
      11  1.84e+06  2.77e+02  3.83e+07  5.10e-02  3.51e-02
      12  1.68e+06  2.78e+02  3.51e+07  4.43e-02  3.14e-02
      13  1.54e+06  2.80e+02  3.21e+07  3.88e-02  2.85e-02
      14  1.42e+06  2.81e+02  2.95e+07  3.43e-02  2.62e-02
      15  1.30e+06  2.82e+02  2.72e+07  3.05e-02  2.40e-02
      16  1.21e+06  2.83e+02  2.51e+07  2.74e-02  2.19e-02
      17  1.11e+06  2.84e+02  2.32e+07  2.46e-02  2.03e-02
      18  1.03e+06  2.85e+02  2.14e+07  2.21e-02  1.89e-02
      19  9.50e+05  2.85e+02  1.98e+07  2.01e-02  1.78e-02
      20  8.78e+05  2.86e+02  1.83e+07  1.83e-02  1.67e-02
      21  8.13e+05  2.86e+02  1.69e+07  1.67e-02  1.57e-02
      22  7.52e+05  2.86e+02  1.57e+07  1.54e-02  1.49e-02
      23  6.99e+05  2.86e+02  1.46e+07  1.42e-02  1.41e-02
      24  6.50e+05  2.86e+02  1.35e+07  1.32e-02  1.34e-02
      25  6.06e+05  2.86e+02  1.26e+07  1.23e-02  1.27e-02
      26  5.65e+05  2.86e+02  1.18e+07  1.14e-02  1.22e-02
      27  5.28e+05  2.87e+02  1.10e+07  1.07e-02  1.16e-02
      28  4.93e+05  2.87e+02  1.03e+07  1.01e-02  1.11e-02
      29  4.62e+05  2.87e+02  9.62e+06  9.49e-03  1.06e-02
      30  4.32e+05  2.87e+02  9.00e+06  8.95e-03  1.02e-02
      31  4.06e+05  2.87e+02  8.44e+06  8.46e-03  9.81e-03
      32  3.80e+05  2.87e+02  7.90e+06  8.01e-03  9.44e-03
      33  3.56e+05  2.87e+02  7.40e+06  7.61e-03  9.11e-03
      34  3.33e+05  2.87e+02  6.93e+06  7.24e-03  8.80e-03
      35  3.12e+05  2.87e+02  6.49e+06  6.90e-03  8.50e-03
      36  2.92e+05  2.87e+02  6.08e+06  6.60e-03  8.22e-03
      37  2.74e+05  2.87e+02  5.71e+06  6.31e-03  7.98e-03
      38  2.58e+05  2.87e+02  5.37e+06  6.05e-03  7.73e-03
      39  2.43e+05  2.87e+02  5.05e+06  5.80e-03  7.50e-03
      40  2.28e+05  2.87e+02  4.75e+06  5.57e-03  7.28e-03
      41  2.15e+05  2.87e+02  4.47e+06  5.37e-03  7.08e-03
      42  2.03e+05  2.87e+02  4.22e+06  5.17e-03  6.90e-03
      43  1.91e+05  2.87e+02  3.97e+06  4.98e-03  6.72e-03
      44  1.80e+05  2.87e+02  3.75e+06  4.80e-03  6.54e-03
      45  1.70e+05  2.87e+02  3.55e+06  4.65e-03  6.38e-03
      46  1.61e+05  2.87e+02  3.35e+06  4.49e-03  6.23e-03
      47  1.53e+05  2.87e+02  3.18e+06  4.35e-03  6.08e-03
      48  1.45e+05  2.87e+02  3.01e+06  4.22e-03  5.93e-03
      49  1.37e+05  2.87e+02  2.86e+06  4.09e-03  5.79e-03
      50  1.30e+05  2.87e+02  2.71e+06  3.97e-03  5.65e-03
      51  1.24e+05  2.87e+02  2.58e+06  3.85e-03  5.52e-03
      52  1.18e+05  2.87e+02  2.45e+06  3.74e-03  5.40e-03
      53  1.12e+05  2.87e+02  2.34e+06  3.64e-03  5.28e-03
      54  1.07e+05  2.87e+02  2.23e+06  3.54e-03  5.16e-03
      55  1.02e+05  2.87e+02  2.13e+06  3.45e-03  5.07e-03
      56  9.79e+04  2.87e+02  2.03e+06  3.37e-03  4.97e-03
      57  9.38e+04  2.87e+02  1.95e+06  3.28e-03  4.88e-03
      58  8.99e+04  2.87e+02  1.87e+06  3.20e-03  4.78e-03
      59  8.61e+04  2.87e+02  1.79e+06  3.13e-03  4.69e-03
      60  8.25e+04  2.87e+02  1.71e+06  3.05e-03  4.60e-03
      61  7.92e+04  2.87e+02  1.64e+06  2.98e-03  4.52e-03
      62  7.60e+04  2.87e+02  1.58e+06  2.91e-03  4.43e-03
      63  7.30e+04  2.87e+02  1.52e+06  2.85e-03  4.34e-03
      64  7.02e+04  2.87e+02  1.46e+06  2.78e-03  4.26e-03
      65  6.76e+04  2.87e+02  1.40e+06  2.72e-03  4.18e-03
      66  6.50e+04  2.87e+02  1.35e+06  2.66e-03  4.11e-03
      67  6.27e+04  2.87e+02  1.30e+06  2.61e-03  4.04e-03
      68  6.06e+04  2.87e+02  1.26e+06  2.55e-03  3.97e-03
      69  5.85e+04  2.87e+02  1.21e+06  2.50e-03  3.90e-03
      70  5.66e+04  2.87e+02  1.17e+06  2.45e-03  3.83e-03
      71  5.46e+04  2.87e+02  1.13e+06  2.40e-03  3.76e-03
      72  5.29e+04  2.87e+02  1.10e+06  2.35e-03  3.70e-03
      73  5.12e+04  2.87e+02  1.06e+06  2.30e-03  3.64e-03
      74  4.96e+04  2.87e+02  1.03e+06  2.26e-03  3.58e-03
      75  4.81e+04  2.87e+02  9.97e+05  2.22e-03  3.52e-03
      76  4.67e+04  2.87e+02  9.67e+05  2.18e-03  3.47e-03
      77  4.53e+04  2.87e+02  9.38e+05  2.14e-03  3.42e-03
      78  4.40e+04  2.87e+02  9.11e+05  2.10e-03  3.37e-03
      79  4.27e+04  2.87e+02  8.84e+05  2.06e-03  3.31e-03
      80  4.15e+04  2.87e+02  8.59e+05  2.03e-03  3.27e-03
      81  4.04e+04  2.87e+02  8.35e+05  1.99e-03  3.22e-03
      82  3.93e+04  2.87e+02  8.13e+05  1.96e-03  3.18e-03
      83  3.82e+04  2.87e+02  7.90e+05  1.93e-03  3.13e-03
      84  3.72e+04  2.87e+02  7.69e+05  1.90e-03  3.09e-03
      85  3.62e+04  2.87e+02  7.48e+05  1.87e-03  3.05e-03
      86  3.53e+04  2.87e+02  7.29e+05  1.84e-03  3.01e-03
      87  3.44e+04  2.87e+02  7.11e+05  1.81e-03  2.97e-03
    ------------------------------------------------------


The denoised estimate of the image is just the reconstruction from the
coefficient maps.

.. code:: ipython3

    imgdp = b.reconstruct().squeeze()
    imgd = np.clip(crop(imgdp) + imgnl, 0, 1)

Display solve time and denoising performance.

.. code:: ipython3

    print("ConvBPDN solve time: %5.2f s" % b.timer.elapsed('solve'))
    print("Noisy image PSNR:    %5.2f dB" % metric.psnr(img, imgn))
    print("Denoised image PSNR: %5.2f dB" % metric.psnr(img, imgd))


.. parsed-literal::

    ConvBPDN solve time: 39.48 s
    Noisy image PSNR:    18.97 dB
    Denoised image PSNR: 26.08 dB


Display the reference, noisy, and denoised images.

.. code:: ipython3

    fig = plot.figure(figsize=(21, 7))
    plot.subplot(1, 3, 1)
    plot.imview(img, title='Reference', fig=fig)
    plot.subplot(1, 3, 2)
    plot.imview(imgn, title='Noisy', fig=fig)
    plot.subplot(1, 3, 3)
    plot.imview(imgd, title='CSC Result', fig=fig)
    fig.show()



.. image:: gwnden_gry_files/gwnden_gry_19_0.png


Plot functional evolution during ADMM iterations.

.. code:: ipython3

    its = b.getitstat()
    plot.plot(its.ObjFun, xlbl='Iterations', ylbl='Functional')



.. image:: gwnden_gry_files/gwnden_gry_21_0.png


Plot evolution of ADMM residuals and ADMM penalty parameter.

.. code:: ipython3

    plot.plot(np.vstack((its.PrimalRsdl, its.DualRsdl)).T,
              ptyp='semilogy', xlbl='Iterations', ylbl='Residual',
              lgnd=['Primal', 'Dual'])
    plot.plot(its.Rho, xlbl='Iterations', ylbl='Penalty Parameter')



.. image:: gwnden_gry_files/gwnden_gry_23_0.png



.. image:: gwnden_gry_files/gwnden_gry_23_1.png

