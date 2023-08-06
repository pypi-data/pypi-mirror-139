.. _examples_csc_gwnden_clr:

Gaussian White Noise Restoration via CSC
========================================

This example demonstrates the removal of Gaussian white noise from a
colour image using convolutional sparse coding
:cite:`wohlberg-2016-convolutional`,

.. math:: \mathrm{argmin}_\mathbf{x} \; (1/2) \sum_c \left\| \sum_m \mathbf{d}_{m} * \mathbf{x}_{c,m} -\mathbf{s}_c \right\|_2^2 + \lambda \sum_m \| \mathbf{x}_m \|_1 + \mu \| \{ \mathbf{x}_{c,m} \} \|_{2,1}

where :math:`\mathbf{d}_m` is the :math:`m^{\text{th}}` dictionary
filter, :math:`\mathbf{x}_{c,m}` is the coefficient map corresponding to
the :math:`c^{\text{th}}` colour band and :math:`m^{\text{th}}`
dictionary filter, and :math:`\mathbf{s}_c` is colour band :math:`c` of
the input image.

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
    from sporco.cupy import (cupy_enabled, np2cp, cp2np, select_device_by_load,
                             gpu_info)
    from sporco.cupy.admm import cbpdn

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
                                     idxexp=np.s_[:, 160:672])
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
    W = fft.irfftn(np.conj(fft.rfftn(D[..., np.newaxis, :], imgnph.shape[0:2],
                   (0, 1))) * fft.rfftn(imgnph[..., np.newaxis], None, (0, 1)),
                   imgnph.shape[0:2], (0, 1))
    W = 1.0/(np.maximum(np.abs(W), 1e-8))

    lmbda = 1.5e-2
    mu = 2.7e-1

    opt = cbpdn.ConvBPDNJoint.Options({'Verbose': True, 'MaxMainIter': 250,
                'HighMemSolve': True, 'RelStopTol': 3e-3, 'AuxVarObj': False,
                'L1Weight': np2cp(W), 'AutoRho': {'Enabled': False},
                'rho': 1e3*lmbda})

Initialise a ``sporco.cupy`` version of a
:class:`.admm.cbpdn.ConvBPDNJoint` object and call the ``solve``
method.

.. code:: ipython3

    if not cupy_enabled():
        print('CuPy/GPU device not available: running without GPU acceleration\n')
    else:
        id = select_device_by_load()
        info = gpu_info()
        if info:
            print('Running on GPU %d (%s)\n' % (id, info[id].name))

    b = cbpdn.ConvBPDNJoint(np2cp(D), np2cp(pad(imgnh)), lmbda, mu, opt, dimK=0)
    X = cp2np(b.solve())


.. parsed-literal::

    Running on GPU 1 (NVIDIA GeForce RTX 2080 Ti)

    Itn   Fnc       DFid      Regℓ1     Regℓ2,1   r         s
    ----------------------------------------------------------------
       0  2.43e+04  9.36e+01  1.38e+06  1.27e+04  9.99e-01  9.51e-03
       1  1.27e+04  3.54e+02  6.74e+05  8.42e+03  9.89e-01  3.68e-02
       2  7.80e+03  5.10e+02  3.70e+05  6.45e+03  8.93e-01  8.22e-02
       3  6.58e+03  6.27e+02  3.04e+05  5.15e+03  4.77e-01  1.12e-01
       4  6.19e+03  6.89e+02  2.82e+05  4.70e+03  2.80e-01  9.83e-02
       5  5.92e+03  7.26e+02  2.64e+05  4.57e+03  2.10e-01  6.67e-02
       6  5.30e+03  7.54e+02  2.30e+05  4.06e+03  1.70e-01  5.64e-02
       7  4.75e+03  7.82e+02  2.02e+05  3.46e+03  1.42e-01  5.29e-02
       8  4.35e+03  8.08e+02  1.82e+05  3.04e+03  1.23e-01  4.45e-02
       9  4.04e+03  8.31e+02  1.64e+05  2.79e+03  1.06e-01  3.51e-02
      10  3.81e+03  8.51e+02  1.50e+05  2.59e+03  9.07e-02  2.88e-02
      11  3.57e+03  8.67e+02  1.37e+05  2.42e+03  7.64e-02  2.60e-02
      12  3.37e+03  8.78e+02  1.26e+05  2.27e+03  6.46e-02  2.46e-02
      13  3.20e+03  8.87e+02  1.15e+05  2.16e+03  5.53e-02  2.31e-02
      14  3.06e+03  8.93e+02  1.07e+05  2.09e+03  4.81e-02  2.10e-02
      15  2.93e+03  8.97e+02  9.90e+04  2.03e+03  4.24e-02  1.88e-02
      16  2.83e+03  9.00e+02  9.35e+04  1.96e+03  3.77e-02  1.70e-02
      17  2.72e+03  9.03e+02  8.68e+04  1.89e+03  3.37e-02  1.58e-02
      18  2.62e+03  9.05e+02  8.13e+04  1.82e+03  3.02e-02  1.49e-02
      19  2.52e+03  9.08e+02  7.59e+04  1.75e+03  2.73e-02  1.40e-02
      20  2.45e+03  9.10e+02  7.19e+04  1.70e+03  2.49e-02  1.30e-02
      21  2.38e+03  9.13e+02  6.81e+04  1.66e+03  2.27e-02  1.21e-02
      22  2.32e+03  9.14e+02  6.45e+04  1.63e+03  2.08e-02  1.12e-02
      23  2.26e+03  9.16e+02  6.06e+04  1.60e+03  1.91e-02  1.05e-02
      24  2.18e+03  9.17e+02  5.62e+04  1.57e+03  1.75e-02  9.92e-03
      25  2.12e+03  9.18e+02  5.24e+04  1.55e+03  1.62e-02  9.43e-03
      26  2.06e+03  9.18e+02  4.82e+04  1.53e+03  1.50e-02  8.98e-03
      27  2.00e+03  9.18e+02  4.46e+04  1.52e+03  1.39e-02  8.54e-03
      28  1.94e+03  9.18e+02  4.14e+04  1.50e+03  1.29e-02  8.11e-03
      29  1.90e+03  9.18e+02  3.89e+04  1.48e+03  1.21e-02  7.70e-03
      30  1.86e+03  9.18e+02  3.65e+04  1.47e+03  1.13e-02  7.33e-03
      31  1.82e+03  9.18e+02  3.43e+04  1.45e+03  1.06e-02  6.98e-03
      32  1.80e+03  9.18e+02  3.27e+04  1.43e+03  9.95e-03  6.68e-03
      33  1.77e+03  9.19e+02  3.13e+04  1.42e+03  9.36e-03  6.38e-03
      34  1.75e+03  9.19e+02  2.98e+04  1.41e+03  8.82e-03  6.13e-03
      35  1.72e+03  9.19e+02  2.84e+04  1.39e+03  8.33e-03  5.86e-03
      36  1.70e+03  9.20e+02  2.71e+04  1.38e+03  7.89e-03  5.63e-03
      37  1.68e+03  9.20e+02  2.58e+04  1.37e+03  7.47e-03  5.42e-03
      38  1.66e+03  9.20e+02  2.47e+04  1.36e+03  7.10e-03  5.23e-03
      39  1.64e+03  9.21e+02  2.35e+04  1.35e+03  6.75e-03  5.05e-03
      40  1.62e+03  9.21e+02  2.26e+04  1.35e+03  6.43e-03  4.87e-03
      41  1.61e+03  9.21e+02  2.16e+04  1.34e+03  6.13e-03  4.71e-03
      42  1.59e+03  9.21e+02  2.06e+04  1.33e+03  5.86e-03  4.56e-03
      43  1.58e+03  9.21e+02  1.97e+04  1.33e+03  5.61e-03  4.41e-03
      44  1.56e+03  9.21e+02  1.88e+04  1.32e+03  5.37e-03  4.27e-03
      45  1.55e+03  9.21e+02  1.79e+04  1.32e+03  5.15e-03  4.14e-03
      46  1.53e+03  9.21e+02  1.70e+04  1.31e+03  4.95e-03  4.02e-03
      47  1.52e+03  9.22e+02  1.61e+04  1.31e+03  4.75e-03  3.91e-03
      48  1.50e+03  9.22e+02  1.52e+04  1.30e+03  4.58e-03  3.80e-03
      49  1.49e+03  9.22e+02  1.45e+04  1.30e+03  4.41e-03  3.69e-03
      50  1.48e+03  9.22e+02  1.38e+04  1.29e+03  4.25e-03  3.59e-03
      51  1.47e+03  9.22e+02  1.32e+04  1.29e+03  4.10e-03  3.49e-03
      52  1.46e+03  9.22e+02  1.26e+04  1.29e+03  3.96e-03  3.40e-03
      53  1.45e+03  9.22e+02  1.21e+04  1.28e+03  3.83e-03  3.31e-03
      54  1.44e+03  9.22e+02  1.16e+04  1.28e+03  3.70e-03  3.23e-03
      55  1.43e+03  9.22e+02  1.11e+04  1.28e+03  3.58e-03  3.14e-03
      56  1.43e+03  9.22e+02  1.07e+04  1.27e+03  3.47e-03  3.06e-03
      57  1.42e+03  9.23e+02  1.04e+04  1.27e+03  3.36e-03  2.99e-03
      58  1.41e+03  9.23e+02  9.92e+03  1.27e+03  3.26e-03  2.92e-03
      59  1.41e+03  9.23e+02  9.63e+03  1.27e+03  3.16e-03  2.85e-03
      60  1.40e+03  9.23e+02  9.28e+03  1.26e+03  3.07e-03  2.78e-03
      61  1.40e+03  9.23e+02  9.02e+03  1.26e+03  2.99e-03  2.72e-03
    ----------------------------------------------------------------


The denoised estimate of the image is just the reconstruction from the
coefficient maps.

.. code:: ipython3

    imgdp = cp2np(b.reconstruct().squeeze())
    imgd = np.clip(crop(imgdp) + imgnl, 0, 1)

Display solve time and denoising performance.

.. code:: ipython3

    print("ConvBPDNJoint solve time: %5.2f s" % b.timer.elapsed('solve'))
    print("Noisy image PSNR:    %5.2f dB" % metric.psnr(img, imgn))
    print("Denoised image PSNR: %5.2f dB" % metric.psnr(img, imgd))


.. parsed-literal::

    ConvBPDNJoint solve time: 10.19 s
    Noisy image PSNR:    20.47 dB
    Denoised image PSNR: 28.15 dB


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



.. image:: gwnden_clr_files/gwnden_clr_19_0.png


Plot functional evolution during ADMM iterations.

.. code:: ipython3

    its = b.getitstat()
    ObjFun = [float(x) for x in its.ObjFun]
    plot.plot(ObjFun, xlbl='Iterations', ylbl='Functional')



.. image:: gwnden_clr_files/gwnden_clr_21_0.png


Plot evolution of ADMM residuals and ADMM penalty parameter.

.. code:: ipython3

    PrimalRsdl = [float(x) for x in its.PrimalRsdl]
    DualRsdl = [float(x) for x in its.DualRsdl]
    plot.plot(np.vstack((PrimalRsdl, DualRsdl)).T,
              ptyp='semilogy', xlbl='Iterations', ylbl='Residual',
              lgnd=['Primal', 'Dual'])
    plot.plot(its.Rho, xlbl='Iterations', ylbl='Penalty Parameter')



.. image:: gwnden_clr_files/gwnden_clr_23_0.png



.. image:: gwnden_clr_files/gwnden_clr_23_1.png

