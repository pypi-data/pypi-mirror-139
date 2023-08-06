.. _examples_csc_implsden_grd_pd_dct:

Impulse Noise Restoration via CSC
=================================

This example demonstrates the removal of salt & pepper noise from a
hyperspectral image using convolutional sparse coding, with a product
dictionary :cite:`garcia-2018-convolutional2` and with an
:math:`\ell_1` data fidelity term, an :math:`\ell_1` regularisation
term, and an additional gradient regularization term
:cite:`wohlberg-2016-convolutional2`

.. math:: \mathrm{argmin}_X \; \left\| D X B^T - S \right\|_1 + \lambda \| X \|_1 + (\mu / 2) \sum_i \| G_i X \|_2^2

where :math:`D` is a convolutional dictionary, :math:`B` is a standard
dictionary, :math:`G_i` is an operator that computes the gradient along
array axis :math:`i`, and :math:`S` is a multi-channel input image.

This example uses the GPU accelerated version of :mod:`.admm.pdcsc`
within the :mod:`sporco.cupy` subpackage.

.. code:: ipython3

    from __future__ import print_function
    from builtins import input

    import os.path
    import tempfile
    import pyfftw   # See https://github.com/pyFFTW/pyFFTW/issues/40
    import numpy as np
    import scipy.io as sio

    from sporco import util
    from sporco import signal
    from sporco import plot
    plot.config_notebook_plotting()
    from sporco.metric import psnr
    from sporco.cupy import (cupy_enabled, np2cp, cp2np, select_device_by_load,
                             gpu_info)
    from sporco.cupy.admm import pdcsc
    from sporco.dictlrn import bpdndl

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

Load a reference hyperspectral image and corrupt it with 33% salt and
pepper noise. (The call to ``np.random.seed`` ensures that the
pseudo-random noise is reproducible.)

.. code:: ipython3

    pth = os.path.join(tempfile.gettempdir(), 'Indian_pines.mat')
    if not os.path.isfile(pth):
        url = 'http://www.ehu.eus/ccwintco/uploads/2/22/Indian_pines.mat'
        vid = util.netgetdata(url)
        f = open(pth, 'wb')
        f.write(vid.read())
        f.close()

    img = sio.loadmat(pth)['indian_pines'].astype(np.float32)
    img = img[16:-17, 16:-17, 0:200:2]
    img /= img.max()

    np.random.seed(12345)
    imgn = signal.spnoise(img, 0.33)

We use a product dictionary :cite:`garcia-2018-convolutional2`
constructed from a single-channel convolutional dictionary for the
spatial axes of the image, and a standard (non-convolutional) dictionary
for the spectral axis of the image. The impulse denoising problem is
solved by appending an additional filter to the learned dictionary
``D0``, which is one of those distributed with SPORCO. This additional
component consist of an impulse filters that will represent the low
frequency image components when used together with a gradient penalty on
the coefficient maps, as discussed below. The spectral axis dictionary
is learned from the noise-free ground-truth image since the primary
purpose of this script is as a code usage example: in a real
application, this dictionary would be estimated from a relevant
noise-free image.

.. code:: ipython3

    D0 = util.convdicts()['G:8x8x32']
    Di = np.zeros(D0.shape[0:2] + (1,), dtype=np.float32)
    Di[0, 0] = 1.0
    D = np.concatenate((Di, D0), axis=2)

    S = img.reshape((-1, img.shape[-1])).T
    np.random.seed(12345)
    B0 = np.random.randn(S.shape[0], 20)
    lmbda = 0.02
    opt = bpdndl.BPDNDictLearn.Options({'Verbose': True, 'MaxMainIter': 100,
                                        'BPDN': {'rho': 10.0*lmbda + 0.1},
                                        'CMOD': {'rho': S.shape[1] / 2e2}})

    d = bpdndl.BPDNDictLearn(B0, S, lmbda, opt)
    B = d.solve()


.. parsed-literal::

    Itn   Fnc       DFid      ℓ1        Cnstr     r_X       s_X       ρ_X       r_D       s_D       ρ_D
    --------------------------------------------------------------------------------------------------------
       0  5.87e+04  5.76e+04  5.79e+04  9.34e-01  3.76e-01  5.61e+00  3.00e-01  2.84e-01  1.22e+00  6.27e+01
       1  3.80e+03  2.54e+03  6.26e+04  4.80e-01  1.34e-01  2.03e+00  3.00e-01  1.42e-01  7.57e-01  6.27e+01
       2  2.22e+03  1.32e+03  4.50e+04  3.17e-01  1.27e-01  1.75e+00  3.00e-01  8.21e-02  2.94e-01  6.27e+01
       3  1.26e+03  2.34e+02  5.12e+04  2.56e-01  6.20e-02  8.46e-01  3.00e-01  6.53e-02  2.25e-01  6.27e+01
       4  1.13e+03  2.44e+02  4.45e+04  1.67e-01  5.30e-02  7.08e-01  3.00e-01  4.23e-02  1.34e-01  6.27e+01
       5  1.01e+03  6.79e+01  4.73e+04  1.64e-01  3.35e-02  4.58e-01  3.00e-01  4.10e-02  1.18e-01  6.27e+01
       6  9.72e+02  8.04e+01  4.46e+04  1.18e-01  2.94e-02  3.71e-01  3.00e-01  2.92e-02  8.80e-02  6.27e+01
       7  9.48e+02  4.00e+01  4.54e+04  1.11e-01  1.95e-02  2.59e-01  3.00e-01  2.89e-02  9.25e-02  6.27e+01
       8  9.35e+02  4.75e+01  4.44e+04  9.05e-02  1.66e-02  2.17e-01  3.00e-01  2.32e-02  7.01e-02  6.27e+01
       9  9.28e+02  3.84e+01  4.45e+04  8.71e-02  1.22e-02  1.70e-01  3.00e-01  2.30e-02  7.18e-02  6.27e+01
      10  9.21e+02  3.98e+01  4.41e+04  6.99e-02  1.76e-02  1.28e-01  1.50e-01  2.00e-02  7.42e-02  6.27e+01
      11  9.16e+02  3.84e+01  4.39e+04  6.92e-02  1.54e-02  1.09e-01  1.50e-01  2.02e-02  7.62e-02  6.27e+01
      12  9.11e+02  3.74e+01  4.37e+04  5.38e-02  1.46e-02  1.03e-01  1.50e-01  1.73e-02  7.10e-02  6.27e+01
      13  9.07e+02  3.66e+01  4.35e+04  4.38e-02  1.32e-02  9.14e-02  1.50e-01  1.59e-02  7.07e-02  6.27e+01
      14  9.04e+02  3.59e+01  4.34e+04  3.20e-02  1.25e-02  8.76e-02  1.50e-01  1.39e-02  6.59e-02  6.27e+01
      15  9.01e+02  3.54e+01  4.33e+04  2.68e-02  1.14e-02  8.07e-02  1.50e-01  1.30e-02  6.35e-02  6.27e+01
      16  8.98e+02  3.48e+01  4.32e+04  2.17e-02  1.07e-02  7.71e-02  1.50e-01  1.21e-02  6.04e-02  6.27e+01
      17  8.96e+02  3.44e+01  4.31e+04  1.81e-02  1.00e-02  7.21e-02  1.50e-01  1.16e-02  5.83e-02  6.27e+01
      18  8.95e+02  3.41e+01  4.30e+04  1.65e-02  9.43e-03  6.78e-02  1.50e-01  1.12e-02  5.60e-02  6.27e+01
      19  8.93e+02  3.38e+01  4.30e+04  1.45e-02  8.84e-03  6.34e-02  1.50e-01  1.08e-02  5.41e-02  6.27e+01
      20  8.91e+02  3.35e+01  4.29e+04  1.41e-02  8.30e-03  5.97e-02  1.50e-01  1.06e-02  5.25e-02  6.27e+01
      21  8.90e+02  3.33e+01  4.28e+04  1.31e-02  7.83e-03  5.64e-02  1.50e-01  1.03e-02  5.11e-02  6.27e+01
      22  8.89e+02  3.30e+01  4.28e+04  1.24e-02  7.43e-03  5.36e-02  1.50e-01  1.01e-02  4.97e-02  6.27e+01
      23  8.87e+02  3.27e+01  4.27e+04  1.12e-02  7.09e-03  5.11e-02  1.50e-01  9.85e-03  4.84e-02  6.27e+01
      24  8.86e+02  3.24e+01  4.27e+04  1.08e-02  6.80e-03  4.91e-02  1.50e-01  9.63e-03  4.70e-02  6.27e+01
      25  8.85e+02  3.21e+01  4.26e+04  1.03e-02  6.55e-03  4.71e-02  1.50e-01  9.41e-03  4.58e-02  6.27e+01
      26  8.84e+02  3.19e+01  4.26e+04  9.80e-03  6.32e-03  4.53e-02  1.50e-01  9.18e-03  4.44e-02  6.27e+01
      27  8.83e+02  3.16e+01  4.26e+04  9.42e-03  6.09e-03  4.35e-02  1.50e-01  8.94e-03  4.30e-02  6.27e+01
      28  8.82e+02  3.13e+01  4.25e+04  9.13e-03  5.87e-03  4.16e-02  1.50e-01  8.70e-03  4.15e-02  6.27e+01
      29  8.81e+02  3.11e+01  4.25e+04  8.86e-03  5.63e-03  3.97e-02  1.50e-01  8.45e-03  4.00e-02  6.27e+01
      30  8.81e+02  3.08e+01  4.25e+04  8.76e-03  5.39e-03  3.78e-02  1.50e-01  8.19e-03  3.85e-02  6.27e+01
      31  8.80e+02  3.06e+01  4.25e+04  8.80e-03  5.16e-03  3.61e-02  1.50e-01  7.95e-03  3.70e-02  6.27e+01
      32  8.79e+02  3.03e+01  4.24e+04  8.73e-03  4.94e-03  3.45e-02  1.50e-01  7.72e-03  3.56e-02  6.27e+01
      33  8.79e+02  3.01e+01  4.24e+04  8.72e-03  4.72e-03  3.30e-02  1.50e-01  7.48e-03  3.42e-02  6.27e+01
      34  8.78e+02  2.99e+01  4.24e+04  8.62e-03  4.52e-03  3.15e-02  1.50e-01  7.26e-03  3.29e-02  6.27e+01
      35  8.77e+02  2.97e+01  4.24e+04  8.60e-03  4.33e-03  3.01e-02  1.50e-01  7.05e-03  3.16e-02  6.27e+01
      36  8.77e+02  2.95e+01  4.24e+04  8.63e-03  4.15e-03  2.89e-02  1.50e-01  6.85e-03  3.05e-02  6.27e+01
      37  8.76e+02  2.94e+01  4.24e+04  8.62e-03  3.99e-03  2.77e-02  1.50e-01  6.66e-03  2.94e-02  6.27e+01
      38  8.76e+02  2.92e+01  4.23e+04  8.60e-03  3.83e-03  2.66e-02  1.50e-01  6.49e-03  2.83e-02  6.27e+01
      39  8.76e+02  2.91e+01  4.23e+04  8.61e-03  3.69e-03  2.56e-02  1.50e-01  6.33e-03  2.73e-02  6.27e+01
      40  8.75e+02  2.89e+01  4.23e+04  8.59e-03  3.56e-03  2.47e-02  1.50e-01  6.17e-03  2.64e-02  6.27e+01
      41  8.75e+02  2.88e+01  4.23e+04  8.55e-03  3.44e-03  2.38e-02  1.50e-01  6.03e-03  2.56e-02  6.27e+01
      42  8.74e+02  2.87e+01  4.23e+04  8.52e-03  3.34e-03  2.30e-02  1.50e-01  5.89e-03  2.48e-02  6.27e+01
      43  8.74e+02  2.86e+01  4.23e+04  8.51e-03  3.24e-03  2.23e-02  1.50e-01  5.76e-03  2.40e-02  6.27e+01
      44  8.74e+02  2.85e+01  4.23e+04  8.48e-03  3.15e-03  2.16e-02  1.50e-01  5.64e-03  2.33e-02  6.27e+01
      45  8.73e+02  2.84e+01  4.22e+04  8.45e-03  3.07e-03  2.11e-02  1.50e-01  5.53e-03  2.27e-02  6.27e+01
      46  8.73e+02  2.83e+01  4.22e+04  8.42e-03  2.99e-03  2.05e-02  1.50e-01  5.43e-03  2.21e-02  6.27e+01
      47  8.73e+02  2.82e+01  4.22e+04  8.39e-03  2.93e-03  2.01e-02  1.50e-01  5.33e-03  2.15e-02  6.27e+01
      48  8.72e+02  2.82e+01  4.22e+04  8.38e-03  2.87e-03  1.96e-02  1.50e-01  5.24e-03  2.09e-02  6.27e+01
      49  8.72e+02  2.81e+01  4.22e+04  8.36e-03  2.82e-03  1.93e-02  1.50e-01  5.15e-03  2.04e-02  6.27e+01
      50  8.72e+02  2.80e+01  4.22e+04  8.34e-03  2.77e-03  1.90e-02  1.50e-01  5.07e-03  2.00e-02  6.27e+01
      51  8.71e+02  2.80e+01  4.22e+04  8.33e-03  2.72e-03  1.86e-02  1.50e-01  4.99e-03  1.95e-02  6.27e+01
      52  8.71e+02  2.79e+01  4.22e+04  8.31e-03  2.68e-03  1.84e-02  1.50e-01  4.92e-03  1.90e-02  6.27e+01
      53  8.71e+02  2.78e+01  4.21e+04  8.29e-03  2.64e-03  1.81e-02  1.50e-01  4.85e-03  1.86e-02  6.27e+01
      54  8.70e+02  2.78e+01  4.21e+04  8.28e-03  2.61e-03  1.79e-02  1.50e-01  4.78e-03  1.82e-02  6.27e+01
      55  8.70e+02  2.77e+01  4.21e+04  8.27e-03  2.58e-03  1.77e-02  1.50e-01  4.71e-03  1.78e-02  6.27e+01
      56  8.70e+02  2.76e+01  4.21e+04  8.25e-03  2.55e-03  1.75e-02  1.50e-01  4.65e-03  1.75e-02  6.27e+01
      57  8.70e+02  2.76e+01  4.21e+04  8.24e-03  2.52e-03  1.73e-02  1.50e-01  4.60e-03  1.71e-02  6.27e+01
      58  8.69e+02  2.75e+01  4.21e+04  8.22e-03  2.50e-03  1.72e-02  1.50e-01  4.54e-03  1.68e-02  6.27e+01
      59  8.69e+02  2.75e+01  4.21e+04  8.20e-03  2.48e-03  1.70e-02  1.50e-01  4.49e-03  1.65e-02  6.27e+01
      60  8.69e+02  2.74e+01  4.21e+04  8.19e-03  2.46e-03  1.69e-02  1.50e-01  4.44e-03  1.61e-02  6.27e+01
      61  8.69e+02  2.73e+01  4.21e+04  8.18e-03  2.44e-03  1.68e-02  1.50e-01  4.39e-03  1.59e-02  6.27e+01
      62  8.68e+02  2.73e+01  4.20e+04  8.16e-03  2.42e-03  1.67e-02  1.50e-01  4.34e-03  1.56e-02  6.27e+01
      63  8.68e+02  2.72e+01  4.20e+04  8.15e-03  2.40e-03  1.66e-02  1.50e-01  4.29e-03  1.53e-02  6.27e+01
      64  8.68e+02  2.72e+01  4.20e+04  8.13e-03  2.38e-03  1.65e-02  1.50e-01  4.25e-03  1.50e-02  6.27e+01
      65  8.67e+02  2.71e+01  4.20e+04  8.11e-03  2.37e-03  1.64e-02  1.50e-01  4.21e-03  1.48e-02  6.27e+01
      66  8.67e+02  2.70e+01  4.20e+04  8.11e-03  2.35e-03  1.64e-02  1.50e-01  4.17e-03  1.46e-02  6.27e+01
      67  8.67e+02  2.70e+01  4.20e+04  8.10e-03  2.34e-03  1.63e-02  1.50e-01  4.13e-03  1.43e-02  6.27e+01
      68  8.67e+02  2.69e+01  4.20e+04  8.08e-03  2.33e-03  1.63e-02  1.50e-01  4.10e-03  1.41e-02  6.27e+01
      69  8.66e+02  2.69e+01  4.20e+04  8.07e-03  2.32e-03  1.62e-02  1.50e-01  4.07e-03  1.39e-02  6.27e+01
      70  8.66e+02  2.68e+01  4.20e+04  8.07e-03  2.30e-03  1.61e-02  1.50e-01  4.03e-03  1.37e-02  6.27e+01
      71  8.66e+02  2.67e+01  4.20e+04  8.05e-03  2.29e-03  1.61e-02  1.50e-01  4.00e-03  1.35e-02  6.27e+01
      72  8.66e+02  2.67e+01  4.19e+04  8.05e-03  2.28e-03  1.60e-02  1.50e-01  3.98e-03  1.34e-02  6.27e+01
      73  8.65e+02  2.66e+01  4.19e+04  8.03e-03  2.27e-03  1.60e-02  1.50e-01  3.95e-03  1.32e-02  6.27e+01
      74  8.65e+02  2.65e+01  4.19e+04  8.03e-03  2.26e-03  1.59e-02  1.50e-01  3.93e-03  1.31e-02  6.27e+01
      75  8.65e+02  2.65e+01  4.19e+04  8.02e-03  2.25e-03  1.59e-02  1.50e-01  3.91e-03  1.29e-02  6.27e+01
      76  8.64e+02  2.64e+01  4.19e+04  8.02e-03  2.24e-03  1.58e-02  1.50e-01  3.89e-03  1.28e-02  6.27e+01
      77  8.64e+02  2.63e+01  4.19e+04  8.01e-03  2.23e-03  1.58e-02  1.50e-01  3.87e-03  1.26e-02  6.27e+01
      78  8.64e+02  2.62e+01  4.19e+04  8.00e-03  2.22e-03  1.57e-02  1.50e-01  3.85e-03  1.25e-02  6.27e+01
      79  8.64e+02  2.62e+01  4.19e+04  7.99e-03  2.21e-03  1.57e-02  1.50e-01  3.83e-03  1.24e-02  6.27e+01
      80  8.63e+02  2.61e+01  4.19e+04  7.99e-03  2.20e-03  1.56e-02  1.50e-01  3.82e-03  1.23e-02  6.27e+01
      81  8.63e+02  2.60e+01  4.19e+04  7.98e-03  2.18e-03  1.55e-02  1.50e-01  3.80e-03  1.22e-02  6.27e+01
      82  8.63e+02  2.59e+01  4.18e+04  7.96e-03  2.17e-03  1.55e-02  1.50e-01  3.79e-03  1.21e-02  6.27e+01
      83  8.63e+02  2.58e+01  4.18e+04  7.96e-03  2.16e-03  1.54e-02  1.50e-01  3.77e-03  1.20e-02  6.27e+01
      84  8.62e+02  2.58e+01  4.18e+04  7.92e-03  2.14e-03  1.54e-02  1.50e-01  3.76e-03  1.19e-02  6.27e+01
      85  8.62e+02  2.57e+01  4.18e+04  7.91e-03  2.13e-03  1.53e-02  1.50e-01  3.75e-03  1.18e-02  6.27e+01
      86  8.62e+02  2.56e+01  4.18e+04  7.91e-03  2.11e-03  1.53e-02  1.50e-01  3.74e-03  1.17e-02  6.27e+01
      87  8.62e+02  2.55e+01  4.18e+04  7.89e-03  2.10e-03  1.52e-02  1.50e-01  3.73e-03  1.16e-02  6.27e+01
      88  8.61e+02  2.55e+01  4.18e+04  7.88e-03  2.08e-03  1.51e-02  1.50e-01  3.72e-03  1.15e-02  6.27e+01
      89  8.61e+02  2.54e+01  4.18e+04  7.86e-03  2.07e-03  1.51e-02  1.50e-01  3.70e-03  1.14e-02  6.27e+01
      90  8.61e+02  2.53e+01  4.18e+04  7.85e-03  2.05e-03  1.50e-02  1.50e-01  3.70e-03  1.13e-02  6.27e+01
      91  8.61e+02  2.52e+01  4.18e+04  7.81e-03  2.04e-03  1.49e-02  1.50e-01  3.69e-03  1.12e-02  6.27e+01
      92  8.60e+02  2.52e+01  4.18e+04  7.81e-03  2.02e-03  1.49e-02  1.50e-01  3.68e-03  1.12e-02  6.27e+01
      93  8.60e+02  2.51e+01  4.18e+04  7.78e-03  2.01e-03  1.48e-02  1.50e-01  3.67e-03  1.11e-02  6.27e+01
      94  8.60e+02  2.50e+01  4.17e+04  7.76e-03  1.99e-03  1.47e-02  1.50e-01  3.66e-03  1.10e-02  6.27e+01
      95  8.60e+02  2.49e+01  4.17e+04  7.73e-03  1.98e-03  1.46e-02  1.50e-01  3.65e-03  1.09e-02  6.27e+01
      96  8.59e+02  2.49e+01  4.17e+04  7.71e-03  1.96e-03  1.46e-02  1.50e-01  3.64e-03  1.09e-02  6.27e+01
      97  8.59e+02  2.48e+01  4.17e+04  7.70e-03  1.95e-03  1.45e-02  1.50e-01  3.64e-03  1.08e-02  6.27e+01
      98  8.59e+02  2.47e+01  4.17e+04  7.67e-03  1.94e-03  1.44e-02  1.50e-01  3.64e-03  1.07e-02  6.27e+01
      99  8.59e+02  2.47e+01  4.17e+04  7.66e-03  1.93e-03  1.43e-02  1.50e-01  3.63e-03  1.07e-02  6.27e+01
    --------------------------------------------------------------------------------------------------------


The problem is solved using class
:class:`.admm.pdcsc.ConvProdDictL1L1Grd`, which implements a
convolutional sparse coding problem with a product dictionary
:cite:`garcia-2018-convolutional2`, an :math:`\ell_1` data fidelity
term, an :math:`\ell_1` regularisation term, and an additional
gradient regularization term :cite:`wohlberg-2016-convolutional2`, as
defined above. The regularization parameters for the :math:`\ell_1` and
gradient terms are ``lmbda`` and ``mu`` respectively. Setting correct
weighting arrays for these regularization terms is critical to obtaining
good performance. For the :math:`\ell_1` norm, the weights on the
filters that are intended to represent low frequency components are set
to zero (we only want them penalised by the gradient term), and the
weights of the remaining filters are set to zero. For the gradient
penalty, all weights are set to zero except for those corresponding to
the filters intended to represent low frequency components, which are
set to unity.

.. code:: ipython3

    lmbda = 1.4e0
    mu = 9e0

Set up weights for the :math:`\ell_1` norm to disable regularization of
the coefficient map corresponding to the impulse filter.

.. code:: ipython3

    wl1 = np.ones((1,)*4 + (D.shape[2],), dtype=np.float32)
    wl1[..., 0] = 0.0

Set of weights for the :math:`\ell_2` norm of the gradient to disable
regularization of all coefficient maps except for the one corresponding
to the impulse filter.

.. code:: ipython3

    wgr = np.zeros((D.shape[2]), dtype=np.float32)
    wgr[0] = 1.0

Set :class:`.admm.pdcsc.ConvProdDictL1L1Grd` solver options.

.. code:: ipython3

    opt = pdcsc.ConvProdDictL1L1Grd.Options(
        {'Verbose': True, 'MaxMainIter': 100, 'RelStopTol': 5e-3,
         'AuxVarObj': False, 'rho': 1e1, 'RelaxParam': 1.8,
         'L1Weight': np2cp(wl1), 'GradWeight': np2cp(wgr)})

Initialise the :class:`.admm.pdcsc.ConvProdDictL1L1Grd` object and
call the ``solve`` method.

.. code:: ipython3

    if not cupy_enabled():
        print('CuPy/GPU device not available: running without GPU acceleration\n')
    else:
        id = select_device_by_load()
        info = gpu_info()
        if info:
            print('Running on GPU %d (%s)\n' % (id, info[id].name))

    b = pdcsc.ConvProdDictL1L1Grd(np2cp(D), np2cp(B), np2cp(pad(imgn)),
                                  lmbda, mu, opt=opt, dimK=0)
    X = cp2np(b.solve())


.. parsed-literal::

    Running on GPU 1 (NVIDIA GeForce RTX 2080 Ti)

    Itn   Fnc       DFid      Regℓ1     Regℓ2∇    r         s
    ----------------------------------------------------------------
       0  4.99e+05  3.07e+05  1.37e+05  4.12e+01  4.09e-01  2.45e+00
       1  4.74e+05  3.09e+05  1.17e+05  1.00e+02  3.44e-01  1.64e+00
       2  4.23e+05  2.97e+05  8.95e+04  1.04e+02  2.70e-01  1.56e+00
       3  4.03e+05  2.98e+05  7.39e+04  1.02e+02  2.14e-01  1.20e+00
       4  3.74e+05  2.91e+05  5.86e+04  9.88e+01  1.70e-01  1.02e+00
       5  3.56e+05  2.88e+05  4.82e+04  1.02e+02  1.36e-01  8.31e-01
       6  3.41e+05  2.85e+05  3.98e+04  1.11e+02  1.09e-01  7.19e-01
       7  3.32e+05  2.83e+05  3.37e+04  1.19e+02  8.80e-02  6.19e-01
       8  3.23e+05  2.81e+05  2.91e+04  1.28e+02  7.12e-02  5.46e-01
       9  3.17e+05  2.80e+05  2.52e+04  1.36e+02  5.78e-02  4.74e-01
      10  3.11e+05  2.79e+05  2.20e+04  1.43e+02  4.73e-02  4.20e-01
      11  3.07e+05  2.78e+05  1.94e+04  1.47e+02  3.89e-02  3.77e-01
      12  3.03e+05  2.78e+05  1.74e+04  1.50e+02  3.22e-02  3.42e-01
      13  3.00e+05  2.77e+05  1.57e+04  1.51e+02  2.70e-02  3.18e-01
      14  2.98e+05  2.77e+05  1.43e+04  1.52e+02  2.29e-02  2.94e-01
      15  2.96e+05  2.76e+05  1.33e+04  1.52e+02  1.96e-02  2.77e-01
      16  2.95e+05  2.76e+05  1.24e+04  1.52e+02  1.71e-02  2.62e-01
      17  2.94e+05  2.76e+05  1.17e+04  1.52e+02  1.51e-02  2.48e-01
      18  2.92e+05  2.76e+05  1.09e+04  1.52e+02  1.35e-02  2.34e-01
      19  2.91e+05  2.76e+05  1.03e+04  1.52e+02  1.22e-02  2.24e-01
      20  2.91e+05  2.75e+05  9.76e+03  1.52e+02  1.11e-02  2.17e-01
      21  2.90e+05  2.75e+05  9.32e+03  1.52e+02  1.02e-02  2.10e-01
      22  2.89e+05  2.75e+05  8.92e+03  1.52e+02  9.42e-03  2.04e-01
      23  2.88e+05  2.75e+05  8.50e+03  1.52e+02  8.76e-03  1.99e-01
      24  2.88e+05  2.75e+05  8.05e+03  1.53e+02  8.19e-03  1.93e-01
      25  2.87e+05  2.75e+05  7.64e+03  1.53e+02  7.70e-03  1.87e-01
      26  2.86e+05  2.75e+05  7.29e+03  1.53e+02  7.27e-03  1.82e-01
      27  2.86e+05  2.75e+05  6.98e+03  1.53e+02  6.88e-03  1.78e-01
      28  2.85e+05  2.75e+05  6.70e+03  1.53e+02  6.52e-03  1.74e-01
      29  2.85e+05  2.75e+05  6.44e+03  1.54e+02  6.20e-03  1.71e-01
      30  2.85e+05  2.74e+05  6.20e+03  1.54e+02  5.91e-03  1.69e-01
      31  2.84e+05  2.74e+05  5.95e+03  1.55e+02  5.64e-03  1.66e-01
      32  2.84e+05  2.74e+05  5.72e+03  1.56e+02  5.38e-03  1.64e-01
      33  2.83e+05  2.74e+05  5.53e+03  1.56e+02  5.15e-03  1.61e-01
      34  2.83e+05  2.74e+05  5.39e+03  1.57e+02  4.95e-03  1.59e-01
      35  2.83e+05  2.74e+05  5.25e+03  1.58e+02  4.75e-03  1.57e-01
      36  2.83e+05  2.74e+05  5.11e+03  1.58e+02  4.56e-03  1.55e-01
      37  2.83e+05  2.74e+05  4.96e+03  1.59e+02  4.38e-03  1.54e-01
      38  2.82e+05  2.74e+05  4.82e+03  1.59e+02  4.20e-03  1.53e-01
      39  2.82e+05  2.74e+05  4.67e+03  1.60e+02  4.03e-03  1.52e-01
      40  2.82e+05  2.74e+05  4.52e+03  1.60e+02  3.87e-03  1.51e-01
      41  2.82e+05  2.74e+05  4.36e+03  1.61e+02  3.72e-03  1.50e-01
      42  2.81e+05  2.74e+05  4.21e+03  1.61e+02  3.57e-03  1.49e-01
      43  2.81e+05  2.74e+05  4.09e+03  1.62e+02  3.43e-03  1.48e-01
      44  2.81e+05  2.74e+05  3.99e+03  1.62e+02  3.31e-03  1.47e-01
      45  2.81e+05  2.74e+05  3.90e+03  1.62e+02  3.19e-03  1.46e-01
      46  2.81e+05  2.74e+05  3.79e+03  1.63e+02  3.08e-03  1.45e-01
      47  2.81e+05  2.74e+05  3.68e+03  1.63e+02  2.97e-03  1.44e-01
      48  2.80e+05  2.74e+05  3.58e+03  1.63e+02  2.87e-03  1.44e-01
      49  2.80e+05  2.74e+05  3.50e+03  1.64e+02  2.78e-03  1.43e-01
      50  2.80e+05  2.74e+05  3.44e+03  1.64e+02  2.69e-03  1.43e-01
      51  2.80e+05  2.74e+05  3.38e+03  1.64e+02  2.61e-03  1.42e-01
      52  2.80e+05  2.74e+05  3.31e+03  1.65e+02  2.53e-03  1.42e-01
      53  2.80e+05  2.74e+05  3.23e+03  1.65e+02  2.45e-03  1.41e-01
      54  2.80e+05  2.74e+05  3.16e+03  1.65e+02  2.38e-03  1.41e-01
      55  2.80e+05  2.74e+05  3.10e+03  1.65e+02  2.30e-03  1.40e-01
      56  2.80e+05  2.74e+05  3.03e+03  1.66e+02  2.24e-03  1.40e-01
      57  2.79e+05  2.74e+05  2.97e+03  1.66e+02  2.17e-03  1.40e-01
      58  2.79e+05  2.74e+05  2.90e+03  1.66e+02  2.10e-03  1.39e-01
      59  2.79e+05  2.74e+05  2.84e+03  1.66e+02  2.04e-03  1.39e-01
      60  2.79e+05  2.74e+05  2.79e+03  1.66e+02  1.99e-03  1.39e-01
      61  2.79e+05  2.74e+05  2.74e+03  1.67e+02  1.93e-03  1.38e-01
      62  2.79e+05  2.74e+05  2.69e+03  1.67e+02  1.88e-03  1.38e-01
      63  2.79e+05  2.74e+05  2.64e+03  1.67e+02  1.83e-03  1.38e-01
      64  2.79e+05  2.74e+05  2.60e+03  1.67e+02  1.78e-03  1.38e-01
      65  2.79e+05  2.74e+05  2.57e+03  1.67e+02  1.74e-03  1.38e-01
      66  2.79e+05  2.74e+05  2.53e+03  1.68e+02  1.70e-03  1.37e-01
      67  2.79e+05  2.74e+05  2.49e+03  1.68e+02  1.65e-03  1.37e-01
      68  2.79e+05  2.74e+05  2.45e+03  1.68e+02  1.61e-03  1.37e-01
      69  2.79e+05  2.74e+05  2.41e+03  1.68e+02  1.57e-03  1.37e-01
      70  2.79e+05  2.74e+05  2.37e+03  1.68e+02  1.53e-03  1.37e-01
      71  2.79e+05  2.74e+05  2.34e+03  1.69e+02  1.50e-03  1.36e-01
      72  2.78e+05  2.74e+05  2.32e+03  1.69e+02  1.47e-03  1.36e-01
      73  2.78e+05  2.74e+05  2.29e+03  1.69e+02  1.43e-03  1.36e-01
      74  2.78e+05  2.74e+05  2.27e+03  1.69e+02  1.40e-03  1.36e-01
      75  2.78e+05  2.74e+05  2.24e+03  1.69e+02  1.37e-03  1.36e-01
      76  2.78e+05  2.74e+05  2.21e+03  1.69e+02  1.34e-03  1.36e-01
      77  2.78e+05  2.74e+05  2.19e+03  1.70e+02  1.31e-03  1.36e-01
      78  2.78e+05  2.74e+05  2.16e+03  1.70e+02  1.29e-03  1.36e-01
      79  2.78e+05  2.74e+05  2.13e+03  1.70e+02  1.26e-03  1.36e-01
      80  2.78e+05  2.74e+05  2.11e+03  1.70e+02  1.23e-03  1.35e-01
      81  2.78e+05  2.74e+05  2.09e+03  1.70e+02  1.21e-03  1.35e-01
      82  2.78e+05  2.74e+05  2.06e+03  1.70e+02  1.18e-03  1.35e-01
      83  2.78e+05  2.74e+05  2.04e+03  1.70e+02  1.16e-03  1.35e-01
      84  2.78e+05  2.74e+05  2.02e+03  1.71e+02  1.14e-03  1.35e-01
      85  2.78e+05  2.74e+05  2.00e+03  1.71e+02  1.11e-03  1.35e-01
      86  2.78e+05  2.74e+05  1.98e+03  1.71e+02  1.09e-03  1.35e-01
      87  2.78e+05  2.74e+05  1.96e+03  1.71e+02  1.07e-03  1.35e-01
      88  2.78e+05  2.74e+05  1.94e+03  1.71e+02  1.05e-03  1.35e-01
      89  2.78e+05  2.74e+05  1.93e+03  1.71e+02  1.03e-03  1.35e-01
      90  2.78e+05  2.74e+05  1.91e+03  1.71e+02  1.01e-03  1.35e-01
      91  2.78e+05  2.74e+05  1.89e+03  1.71e+02  9.92e-04  1.35e-01
      92  2.78e+05  2.74e+05  1.88e+03  1.72e+02  9.74e-04  1.35e-01
      93  2.78e+05  2.74e+05  1.86e+03  1.72e+02  9.56e-04  1.35e-01
      94  2.78e+05  2.74e+05  1.84e+03  1.72e+02  9.39e-04  1.34e-01
      95  2.78e+05  2.74e+05  1.83e+03  1.72e+02  9.22e-04  1.34e-01
      96  2.78e+05  2.74e+05  1.81e+03  1.72e+02  9.06e-04  1.34e-01
      97  2.78e+05  2.74e+05  1.80e+03  1.72e+02  8.91e-04  1.34e-01
      98  2.78e+05  2.74e+05  1.79e+03  1.72e+02  8.75e-04  1.34e-01
      99  2.78e+05  2.74e+05  1.77e+03  1.72e+02  8.60e-04  1.34e-01
    ----------------------------------------------------------------


The denoised estimate of the image is just the reconstruction from all
coefficient maps.

.. code:: ipython3

    imgdp = cp2np(b.reconstruct().squeeze())
    imgd = crop(imgdp)

Display solve time and denoising performance.

.. code:: ipython3

    print("ConvProdDictL1L1Grd solve time: %5.2f s" % b.timer.elapsed('solve'))
    print("Noisy image PSNR:    %5.2f dB" % psnr(img, imgn))
    print("Denoised image PSNR: %5.2f dB" % psnr(img, imgd))


.. parsed-literal::

    ConvProdDictL1L1Grd solve time: 11.30 s
    Noisy image PSNR:     8.75 dB
    Denoised image PSNR: 38.15 dB


Display the reference, noisy, and denoised images.

.. code:: ipython3

    fig, ax = plot.subplots(nrows=1, ncols=3, figsize=(21, 7))
    fig.suptitle('ConvProdDictL1L1GrdJoint Results (false colour, '
                 'bands 10, 20, 30)')
    plot.imview(img[..., 10:40:10], title='Reference', ax=ax[0], fig=fig)
    plot.imview(imgn[..., 10:40:10], title='Noisy', ax=ax[1], fig=fig)
    plot.imview(imgd[..., 10:40:10], title='Denoised', ax=ax[2], fig=fig)
    fig.show()



.. image:: implsden_grd_pd_dct_files/implsden_grd_pd_dct_23_0.png


Get iterations statistics from solver object and plot functional value,
ADMM primary and dual residuals, and automatically adjusted ADMM penalty
parameter against the iteration number.

.. code:: ipython3

    its = b.getitstat()
    ObjFun = [float(x) for x in its.ObjFun]
    PrimalRsdl = [float(x) for x in its.PrimalRsdl]
    DualRsdl = [float(x) for x in its.DualRsdl]
    fig = plot.figure(figsize=(20, 5))
    plot.subplot(1, 3, 1)
    plot.plot(ObjFun, xlbl='Iterations', ylbl='Functional', fig=fig)
    plot.subplot(1, 3, 2)
    plot.plot(np.vstack((PrimalRsdl, DualRsdl)).T,
              ptyp='semilogy', xlbl='Iterations', ylbl='Residual',
              lgnd=['Primal', 'Dual'], fig=fig)
    plot.subplot(1, 3, 3)
    plot.plot(its.Rho, xlbl='Iterations', ylbl='Penalty Parameter', fig=fig)
    fig.show()



.. image:: implsden_grd_pd_dct_files/implsden_grd_pd_dct_25_0.png

