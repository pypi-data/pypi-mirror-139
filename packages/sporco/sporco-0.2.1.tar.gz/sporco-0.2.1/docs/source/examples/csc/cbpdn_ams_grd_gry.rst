.. _examples_csc_cbpdn_ams_grd_gry:

CSC with a Spatial Mask
=======================

This example demonstrates the use of :class:`.cbpdn.AddMaskSim` for
convolutional sparse coding with a spatial mask
:cite:`wohlberg-2016-boundary`. If the ``sporco-cuda`` extension is
installed and a GPU is available, a GPU accelerated version is used. The
example problem is inpainting of randomly distributed corruption of a
greyscale image. This is the same problem solved by example
``cbpdn_ams_gry``, but with a different approach to handling of the
lowpass image components. In this example, instead of pre-processing
with a non-linear lowpass filter, the lowpass components are represented
within the main optimisation problem via an impulse filter with gradient
regularization on the corresponding coefficient map (see Sec. 3 and Sec.
4 of :cite:`wohlberg-2016-convolutional2`).

.. code:: ipython3

    from __future__ import print_function
    from builtins import input

    import pyfftw   # See https://github.com/pyFFTW/pyFFTW/issues/40
    import numpy as np

    from sporco import util
    from sporco import signal
    from sporco import metric
    from sporco import plot
    plot.config_notebook_plotting()
    from sporco.admm import cbpdn
    from sporco.fft import fftconv
    from sporco import cuda

    # If running in a notebook, try to use wurlitzer so that output from the CUDA
    # code will be properly captured in the notebook.
    sys_pipes = util.notebook_system_output()

Load a reference image.

.. code:: ipython3

    img = util.ExampleImages().image('monarch.png', zoom=0.5, scaled=True,
                                     gray=True, idxexp=np.s_[:, 160:672])

Create random mask and apply to reference image to obtain test image.
(The call to ``numpy.random.seed`` ensures that the pseudo-random noise
is reproducible.)

.. code:: ipython3

    np.random.seed(12345)
    frc = 0.5
    msk = signal.rndmask(img.shape, frc, dtype=np.float32)
    imgw = msk * img

Define pad and crop functions.

.. code:: ipython3

    pn = 8
    spad = lambda x: np.pad(x, pn, mode='symmetric')
    zpad = lambda x: np.pad(x, pn, mode='constant')
    crop = lambda x: x[pn:-pn, pn:-pn]

Construct padded mask and test image.

.. code:: ipython3

    mskp = zpad(msk)
    imgwp = spad(imgw)

Load dictionary.

.. code:: ipython3

    D = util.convdicts()['G:8x8x128']
    di = np.zeros(D.shape[0:2] + (1,), dtype=np.float32)
    di[0, 0] = 1
    Di = np.dstack((di, D))

Set up weights for the :math:`\ell_1` norm to disable regularization of
the coefficient map corresponding to the impulse filter intended to
represent lowpass image components (not to be confused with the AMS
impulse filter used to implement spatial masking).

.. code:: ipython3

    wl1 = np.ones((1,)*2 + (Di.shape[2:]), dtype=np.float32)
    wl1[..., 0] = 0.0
    wl1i = np.concatenate((wl1, np.zeros(wl1.shape[0:-1] + (1,))), axis=-1)

When representing lowpass image components using an impulse filter
together with an :math:`\ell_2` norm on the gradient of its coefficient
map, we usually want to set the weight array for this norm (specified by
the ``GradWeight`` option) to disable regularization of all coefficient
maps except for the one corresponding to that impulse filter (not to be
confused with the AMS impulse filter used to implement spatial masking).
In this case set a non-zero value for the weights of the other
coefficient maps size this improves performance in this inpainting
problem.

.. code:: ipython3

    #wgr = np.zeros((Di.shape[2]), dtype=np.float32)
    wgr = 2e-1 * np.ones((Di.shape[2]), dtype=np.float32)
    wgr[0] = 1.0
    wgri = np.hstack((wgr, np.zeros((1,))))

Set up :class:`.admm.cbpdn.ConvBPDNGradReg` options.

.. code:: ipython3

    lmbda = 1e-2
    mu = 2e-1
    opt = cbpdn.ConvBPDNGradReg.Options({'Verbose': True, 'MaxMainIter': 200,
                        'HighMemSolve': True, 'RelStopTol': 5e-3,
                        'AuxVarObj': False, 'RelaxParam': 1.8,
                        'rho': 5e1*lmbda + 1e-1, 'L1Weight': wl1,
                        'GradWeight': wgr, 'AutoRho': {'Enabled': False,
                        'StdResiduals': False}})

Construct :class:`.admm.cbpdn.AddMaskSim` wrapper for
:class:`.admm.cbpdn.ConvBPDNGradReg` and solve via wrapper. If the
``sporco-cuda`` extension is installed and a GPU is available, use the
CUDA implementation of this combination.

.. code:: ipython3

    if cuda.device_count() > 0:
        opt['L1Weight'] = wl1
        opt['GradWeight'] = wgr
        ams = None
        print('%s GPU found: running CUDA solver' % cuda.device_name())
        tm = util.Timer()
        with sys_pipes(), util.ContextTimer(tm):
            X = cuda.cbpdngrdmsk(Di, imgwp, mskp, lmbda, mu, opt)
        t = tm.elapsed()
        imgr = crop(np.sum(fftconv(Di, X, axes=(0, 1)), axis=-1))
    else:
        opt['L1Weight'] = wl1i
        opt['GradWeight'] = wgri
        ams = cbpdn.AddMaskSim(cbpdn.ConvBPDNGradReg, Di, imgwp, mskp, lmbda, mu,
                               opt=opt)
        X = ams.solve().squeeze()
        t = ams.timer.elapsed('solve')
        imgr = crop(ams.reconstruct().squeeze())


.. parsed-literal::

    GeForce RTX 2080 Ti GPU found: running CUDA solver
    Itn   Fnc       DFid      Regℓ1     Regℓ2∇     r         s         ρ
    --------------------------------------------------------------------------
       0  3.55e+02  1.60e+02  1.87e+04  3.89e+01  5.80e-01  1.48e+00  6.00e-01
       1  2.80e+02  2.58e+01  2.34e+04  9.95e+01  3.81e-01  6.79e-01  6.00e-01
       2  2.62e+02  2.97e+01  2.07e+04  1.27e+02  2.64e-01  9.15e-01  6.00e-01
       3  1.74e+02  1.15e+01  1.44e+04  9.41e+01  1.35e-01  4.51e-01  6.00e-01
       4  1.61e+02  4.48e+00  1.39e+04  8.77e+01  1.06e-01  2.41e-01  6.00e-01
       5  1.41e+02  3.15e+00  1.20e+04  8.79e+01  7.19e-02  2.65e-01  6.00e-01
       6  1.29e+02  3.39e+00  1.08e+04  8.37e+01  5.07e-02  1.96e-01  6.00e-01
       7  1.13e+02  2.49e+00  9.54e+03  7.77e+01  4.22e-02  1.63e-01  6.00e-01
       8  1.05e+02  1.99e+00  8.84e+03  7.39e+01  3.54e-02  1.56e-01  6.00e-01
       9  9.92e+01  2.14e+00  8.29e+03  7.05e+01  3.05e-02  1.41e-01  6.00e-01
      10  9.19e+01  2.05e+00  7.63e+03  6.77e+01  2.72e-02  1.37e-01  6.00e-01
      11  8.95e+01  1.84e+00  7.46e+03  6.50e+01  2.51e-02  1.29e-01  6.00e-01
      12  8.49e+01  1.81e+00  7.06e+03  6.24e+01  2.30e-02  1.25e-01  6.00e-01
      13  8.02e+01  1.73e+00  6.65e+03  5.97e+01  2.14e-02  1.22e-01  6.00e-01
      14  7.67e+01  1.66e+00  6.36e+03  5.73e+01  2.00e-02  1.18e-01  6.00e-01
      15  7.39e+01  1.62e+00  6.12e+03  5.51e+01  1.89e-02  1.15e-01  6.00e-01
      16  7.12e+01  1.56e+00  5.90e+03  5.31e+01  1.79e-02  1.12e-01  6.00e-01
      17  6.82e+01  1.51e+00  5.64e+03  5.13e+01  1.69e-02  1.10e-01  6.00e-01
      18  6.53e+01  1.47e+00  5.39e+03  4.94e+01  1.61e-02  1.09e-01  6.00e-01
      19  6.31e+01  1.43e+00  5.21e+03  4.77e+01  1.54e-02  1.07e-01  6.00e-01
      20  6.12e+01  1.38e+00  5.06e+03  4.61e+01  1.48e-02  1.05e-01  6.00e-01
      21  5.91e+01  1.34e+00  4.88e+03  4.45e+01  1.42e-02  1.04e-01  6.00e-01
      22  5.70e+01  1.31e+00  4.71e+03  4.31e+01  1.36e-02  1.02e-01  6.00e-01
      23  5.52e+01  1.27e+00  4.56e+03  4.16e+01  1.31e-02  1.01e-01  6.00e-01
      24  5.35e+01  1.24e+00  4.42e+03  4.03e+01  1.26e-02  9.98e-02  6.00e-01
      25  5.18e+01  1.21e+00  4.28e+03  3.90e+01  1.22e-02  9.86e-02  6.00e-01
      26  5.02e+01  1.18e+00  4.14e+03  3.78e+01  1.18e-02  9.75e-02  6.00e-01
      27  4.87e+01  1.15e+00  4.02e+03  3.67e+01  1.14e-02  9.64e-02  6.00e-01
      28  4.72e+01  1.12e+00  3.89e+03  3.56e+01  1.10e-02  9.55e-02  6.00e-01
      29  4.57e+01  1.09e+00  3.77e+03  3.46e+01  1.07e-02  9.45e-02  6.00e-01
      30  4.44e+01  1.06e+00  3.66e+03  3.36e+01  1.03e-02  9.36e-02  6.00e-01
      31  4.31e+01  1.03e+00  3.56e+03  3.27e+01  1.00e-02  9.26e-02  6.00e-01
      32  4.20e+01  1.01e+00  3.46e+03  3.18e+01  9.72e-03  9.16e-02  6.00e-01
      33  4.09e+01  9.83e-01  3.37e+03  3.09e+01  9.44e-03  9.06e-02  6.00e-01
      34  3.98e+01  9.58e-01  3.28e+03  3.02e+01  9.17e-03  8.97e-02  6.00e-01
      35  3.88e+01  9.33e-01  3.20e+03  2.94e+01  8.91e-03  8.87e-02  6.00e-01
      36  3.79e+01  9.08e-01  3.12e+03  2.87e+01  8.66e-03  8.77e-02  6.00e-01
      37  3.70e+01  8.84e-01  3.05e+03  2.80e+01  8.43e-03  8.67e-02  6.00e-01
      38  3.62e+01  8.60e-01  2.99e+03  2.74e+01  8.21e-03  8.57e-02  6.00e-01
      39  3.54e+01  8.37e-01  2.92e+03  2.68e+01  7.99e-03  8.46e-02  6.00e-01
      40  3.47e+01  8.14e-01  2.87e+03  2.62e+01  7.79e-03  8.35e-02  6.00e-01
      41  3.41e+01  7.92e-01  2.81e+03  2.57e+01  7.59e-03  8.24e-02  6.00e-01
      42  3.35e+01  7.71e-01  2.76e+03  2.52e+01  7.40e-03  8.13e-02  6.00e-01
      43  3.29e+01  7.50e-01  2.72e+03  2.47e+01  7.22e-03  8.01e-02  6.00e-01
      44  3.23e+01  7.31e-01  2.67e+03  2.42e+01  7.04e-03  7.90e-02  6.00e-01
      45  3.17e+01  7.12e-01  2.63e+03  2.38e+01  6.87e-03  7.78e-02  6.00e-01
      46  3.12e+01  6.94e-01  2.58e+03  2.34e+01  6.71e-03  7.66e-02  6.00e-01
      47  3.07e+01  6.77e-01  2.54e+03  2.30e+01  6.54e-03  7.54e-02  6.00e-01
      48  3.02e+01  6.61e-01  2.50e+03  2.27e+01  6.39e-03  7.42e-02  6.00e-01
      49  2.98e+01  6.46e-01  2.46e+03  2.24e+01  6.23e-03  7.30e-02  6.00e-01
      50  2.93e+01  6.32e-01  2.43e+03  2.21e+01  6.08e-03  7.18e-02  6.00e-01
      51  2.89e+01  6.18e-01  2.39e+03  2.18e+01  5.94e-03  7.05e-02  6.00e-01
      52  2.84e+01  6.06e-01  2.35e+03  2.15e+01  5.79e-03  6.93e-02  6.00e-01
      53  2.80e+01  5.94e-01  2.31e+03  2.13e+01  5.65e-03  6.81e-02  6.00e-01
      54  2.76e+01  5.83e-01  2.28e+03  2.11e+01  5.52e-03  6.69e-02  6.00e-01
      55  2.72e+01  5.72e-01  2.24e+03  2.09e+01  5.39e-03  6.57e-02  6.00e-01
      56  2.68e+01  5.63e-01  2.21e+03  2.07e+01  5.26e-03  6.45e-02  6.00e-01
      57  2.64e+01  5.53e-01  2.17e+03  2.05e+01  5.13e-03  6.33e-02  6.00e-01
      58  2.60e+01  5.44e-01  2.14e+03  2.04e+01  5.01e-03  6.20e-02  6.00e-01
      59  2.57e+01  5.36e-01  2.11e+03  2.03e+01  4.89e-03  6.08e-02  6.00e-01
      60  2.53e+01  5.28e-01  2.07e+03  2.01e+01  4.78e-03  5.97e-02  6.00e-01
      61  2.50e+01  5.21e-01  2.04e+03  2.00e+01  4.66e-03  5.85e-02  6.00e-01
      62  2.46e+01  5.13e-01  2.01e+03  1.99e+01  4.56e-03  5.73e-02  6.00e-01
      63  2.43e+01  5.07e-01  1.98e+03  1.98e+01  4.45e-03  5.62e-02  6.00e-01
      64  2.40e+01  5.00e-01  1.96e+03  1.97e+01  4.35e-03  5.51e-02  6.00e-01
      65  2.37e+01  4.94e-01  1.93e+03  1.97e+01  4.25e-03  5.39e-02  6.00e-01
      66  2.34e+01  4.88e-01  1.90e+03  1.96e+01  4.15e-03  5.29e-02  6.00e-01
      67  2.32e+01  4.82e-01  1.88e+03  1.95e+01  4.06e-03  5.18e-02  6.00e-01
      68  2.29e+01  4.76e-01  1.86e+03  1.95e+01  3.97e-03  5.07e-02  6.00e-01
      69  2.27e+01  4.71e-01  1.83e+03  1.94e+01  3.88e-03  4.97e-02  6.00e-01
      70  2.25e+01  4.66e-01  1.81e+03  1.94e+01  3.80e-03  4.86e-02  6.00e-01
      71  2.22e+01  4.61e-01  1.79e+03  1.93e+01  3.72e-03  4.76e-02  6.00e-01
      72  2.20e+01  4.56e-01  1.77e+03  1.93e+01  3.64e-03  4.67e-02  6.00e-01
      73  2.18e+01  4.52e-01  1.75e+03  1.92e+01  3.56e-03  4.57e-02  6.00e-01
      74  2.16e+01  4.48e-01  1.73e+03  1.92e+01  3.48e-03  4.48e-02  6.00e-01
      75  2.14e+01  4.44e-01  1.71e+03  1.92e+01  3.41e-03  4.39e-02  6.00e-01
      76  2.12e+01  4.40e-01  1.69e+03  1.91e+01  3.34e-03  4.30e-02  6.00e-01
      77  2.10e+01  4.37e-01  1.67e+03  1.91e+01  3.27e-03  4.21e-02  6.00e-01
      78  2.08e+01  4.34e-01  1.65e+03  1.91e+01  3.20e-03  4.13e-02  6.00e-01
      79  2.06e+01  4.31e-01  1.63e+03  1.90e+01  3.13e-03  4.05e-02  6.00e-01
      80  2.04e+01  4.28e-01  1.62e+03  1.90e+01  3.07e-03  3.97e-02  6.00e-01
      81  2.02e+01  4.25e-01  1.60e+03  1.90e+01  3.00e-03  3.89e-02  6.00e-01
      82  2.00e+01  4.22e-01  1.58e+03  1.89e+01  2.94e-03  3.81e-02  6.00e-01
      83  1.98e+01  4.20e-01  1.56e+03  1.89e+01  2.88e-03  3.74e-02  6.00e-01
      84  1.97e+01  4.18e-01  1.55e+03  1.89e+01  2.82e-03  3.67e-02  6.00e-01
      85  1.95e+01  4.16e-01  1.53e+03  1.88e+01  2.76e-03  3.60e-02  6.00e-01
      86  1.93e+01  4.14e-01  1.52e+03  1.88e+01  2.70e-03  3.54e-02  6.00e-01
      87  1.92e+01  4.12e-01  1.50e+03  1.88e+01  2.65e-03  3.47e-02  6.00e-01
      88  1.90e+01  4.10e-01  1.48e+03  1.87e+01  2.59e-03  3.41e-02  6.00e-01
      89  1.88e+01  4.08e-01  1.47e+03  1.87e+01  2.54e-03  3.35e-02  6.00e-01
      90  1.87e+01  4.07e-01  1.45e+03  1.87e+01  2.49e-03  3.30e-02  6.00e-01
      91  1.85e+01  4.05e-01  1.44e+03  1.87e+01  2.44e-03  3.24e-02  6.00e-01
      92  1.84e+01  4.04e-01  1.43e+03  1.86e+01  2.39e-03  3.18e-02  6.00e-01
      93  1.82e+01  4.02e-01  1.41e+03  1.86e+01  2.34e-03  3.13e-02  6.00e-01
      94  1.81e+01  4.01e-01  1.40e+03  1.86e+01  2.29e-03  3.07e-02  6.00e-01
      95  1.80e+01  4.00e-01  1.39e+03  1.85e+01  2.25e-03  3.02e-02  6.00e-01
      96  1.78e+01  3.98e-01  1.37e+03  1.85e+01  2.20e-03  2.96e-02  6.00e-01
      97  1.77e+01  3.97e-01  1.36e+03  1.84e+01  2.16e-03  2.91e-02  6.00e-01
      98  1.76e+01  3.96e-01  1.35e+03  1.84e+01  2.12e-03  2.85e-02  6.00e-01
      99  1.75e+01  3.95e-01  1.34e+03  1.84e+01  2.08e-03  2.80e-02  6.00e-01
     100  1.74e+01  3.94e-01  1.33e+03  1.83e+01  2.04e-03  2.74e-02  6.00e-01
     101  1.73e+01  3.93e-01  1.32e+03  1.83e+01  2.00e-03  2.69e-02  6.00e-01
     102  1.72e+01  3.92e-01  1.32e+03  1.83e+01  1.96e-03  2.63e-02  6.00e-01
     103  1.71e+01  3.91e-01  1.31e+03  1.82e+01  1.93e-03  2.58e-02  6.00e-01
     104  1.70e+01  3.90e-01  1.30e+03  1.82e+01  1.89e-03  2.52e-02  6.00e-01
     105  1.70e+01  3.89e-01  1.29e+03  1.82e+01  1.86e-03  2.47e-02  6.00e-01
     106  1.69e+01  3.88e-01  1.29e+03  1.81e+01  1.82e-03  2.42e-02  6.00e-01
     107  1.68e+01  3.88e-01  1.28e+03  1.81e+01  1.79e-03  2.37e-02  6.00e-01
     108  1.67e+01  3.87e-01  1.27e+03  1.80e+01  1.76e-03  2.32e-02  6.00e-01
     109  1.66e+01  3.87e-01  1.27e+03  1.80e+01  1.73e-03  2.27e-02  6.00e-01
     110  1.66e+01  3.86e-01  1.26e+03  1.80e+01  1.69e-03  2.23e-02  6.00e-01
     111  1.65e+01  3.86e-01  1.25e+03  1.79e+01  1.66e-03  2.18e-02  6.00e-01
     112  1.64e+01  3.85e-01  1.24e+03  1.79e+01  1.63e-03  2.14e-02  6.00e-01
     113  1.63e+01  3.85e-01  1.24e+03  1.79e+01  1.60e-03  2.10e-02  6.00e-01
     114  1.62e+01  3.85e-01  1.23e+03  1.78e+01  1.57e-03  2.07e-02  6.00e-01
     115  1.62e+01  3.84e-01  1.22e+03  1.78e+01  1.54e-03  2.03e-02  6.00e-01
     116  1.61e+01  3.84e-01  1.21e+03  1.78e+01  1.51e-03  2.00e-02  6.00e-01
     117  1.60e+01  3.84e-01  1.21e+03  1.78e+01  1.48e-03  1.97e-02  6.00e-01
     118  1.59e+01  3.84e-01  1.20e+03  1.77e+01  1.45e-03  1.94e-02  6.00e-01
     119  1.58e+01  3.83e-01  1.19e+03  1.77e+01  1.43e-03  1.91e-02  6.00e-01
     120  1.58e+01  3.83e-01  1.19e+03  1.77e+01  1.40e-03  1.88e-02  6.00e-01
     121  1.57e+01  3.83e-01  1.18e+03  1.76e+01  1.37e-03  1.85e-02  6.00e-01
     122  1.56e+01  3.83e-01  1.17e+03  1.76e+01  1.35e-03  1.82e-02  6.00e-01
     123  1.56e+01  3.83e-01  1.17e+03  1.76e+01  1.32e-03  1.79e-02  6.00e-01
     124  1.55e+01  3.83e-01  1.16e+03  1.76e+01  1.30e-03  1.77e-02  6.00e-01
     125  1.54e+01  3.83e-01  1.16e+03  1.75e+01  1.28e-03  1.74e-02  6.00e-01
     126  1.54e+01  3.82e-01  1.15e+03  1.75e+01  1.26e-03  1.71e-02  6.00e-01
     127  1.53e+01  3.82e-01  1.15e+03  1.75e+01  1.23e-03  1.69e-02  6.00e-01
     128  1.53e+01  3.82e-01  1.14e+03  1.75e+01  1.21e-03  1.66e-02  6.00e-01
     129  1.52e+01  3.82e-01  1.14e+03  1.74e+01  1.19e-03  1.64e-02  6.00e-01
     130  1.52e+01  3.82e-01  1.13e+03  1.74e+01  1.17e-03  1.61e-02  6.00e-01
     131  1.51e+01  3.82e-01  1.13e+03  1.74e+01  1.16e-03  1.59e-02  6.00e-01
     132  1.51e+01  3.81e-01  1.12e+03  1.74e+01  1.14e-03  1.56e-02  6.00e-01
     133  1.50e+01  3.81e-01  1.12e+03  1.74e+01  1.12e-03  1.54e-02  6.00e-01
     134  1.50e+01  3.81e-01  1.11e+03  1.73e+01  1.10e-03  1.51e-02  6.00e-01
     135  1.49e+01  3.81e-01  1.11e+03  1.73e+01  1.09e-03  1.49e-02  6.00e-01
     136  1.49e+01  3.81e-01  1.11e+03  1.73e+01  1.07e-03  1.47e-02  6.00e-01
     137  1.49e+01  3.80e-01  1.10e+03  1.73e+01  1.05e-03  1.45e-02  6.00e-01
     138  1.48e+01  3.80e-01  1.10e+03  1.72e+01  1.04e-03  1.43e-02  6.00e-01
     139  1.48e+01  3.80e-01  1.09e+03  1.72e+01  1.02e-03  1.41e-02  6.00e-01
     140  1.47e+01  3.80e-01  1.09e+03  1.72e+01  1.01e-03  1.39e-02  6.00e-01
     141  1.47e+01  3.79e-01  1.09e+03  1.72e+01  9.91e-04  1.37e-02  6.00e-01
     142  1.46e+01  3.79e-01  1.08e+03  1.72e+01  9.76e-04  1.35e-02  6.00e-01
     143  1.46e+01  3.79e-01  1.08e+03  1.71e+01  9.62e-04  1.33e-02  6.00e-01
     144  1.46e+01  3.79e-01  1.08e+03  1.71e+01  9.48e-04  1.31e-02  6.00e-01
     145  1.45e+01  3.79e-01  1.07e+03  1.71e+01  9.34e-04  1.30e-02  6.00e-01
     146  1.45e+01  3.78e-01  1.07e+03  1.71e+01  9.20e-04  1.28e-02  6.00e-01
     147  1.44e+01  3.78e-01  1.07e+03  1.71e+01  9.06e-04  1.26e-02  6.00e-01
     148  1.44e+01  3.78e-01  1.06e+03  1.70e+01  8.93e-04  1.25e-02  6.00e-01
     149  1.44e+01  3.78e-01  1.06e+03  1.70e+01  8.79e-04  1.23e-02  6.00e-01
     150  1.43e+01  3.77e-01  1.06e+03  1.70e+01  8.66e-04  1.21e-02  6.00e-01
     151  1.43e+01  3.77e-01  1.05e+03  1.70e+01  8.54e-04  1.20e-02  6.00e-01
     152  1.43e+01  3.77e-01  1.05e+03  1.69e+01  8.41e-04  1.18e-02  6.00e-01
     153  1.42e+01  3.77e-01  1.05e+03  1.69e+01  8.29e-04  1.17e-02  6.00e-01
     154  1.42e+01  3.77e-01  1.04e+03  1.69e+01  8.16e-04  1.16e-02  6.00e-01
     155  1.42e+01  3.77e-01  1.04e+03  1.69e+01  8.05e-04  1.14e-02  6.00e-01
     156  1.41e+01  3.76e-01  1.04e+03  1.69e+01  7.93e-04  1.13e-02  6.00e-01
     157  1.41e+01  3.76e-01  1.03e+03  1.68e+01  7.82e-04  1.12e-02  6.00e-01
     158  1.41e+01  3.76e-01  1.03e+03  1.68e+01  7.70e-04  1.10e-02  6.00e-01
     159  1.40e+01  3.76e-01  1.03e+03  1.68e+01  7.59e-04  1.09e-02  6.00e-01
     160  1.40e+01  3.76e-01  1.03e+03  1.68e+01  7.49e-04  1.08e-02  6.00e-01
     161  1.40e+01  3.76e-01  1.02e+03  1.67e+01  7.38e-04  1.07e-02  6.00e-01
     162  1.39e+01  3.76e-01  1.02e+03  1.67e+01  7.28e-04  1.05e-02  6.00e-01
     163  1.39e+01  3.76e-01  1.02e+03  1.67e+01  7.18e-04  1.04e-02  6.00e-01
     164  1.39e+01  3.75e-01  1.02e+03  1.67e+01  7.09e-04  1.03e-02  6.00e-01
     165  1.39e+01  3.75e-01  1.01e+03  1.67e+01  6.99e-04  1.02e-02  6.00e-01
     166  1.38e+01  3.75e-01  1.01e+03  1.66e+01  6.90e-04  1.01e-02  6.00e-01
     167  1.38e+01  3.75e-01  1.01e+03  1.66e+01  6.81e-04  9.96e-03  6.00e-01
     168  1.38e+01  3.75e-01  1.01e+03  1.66e+01  6.73e-04  9.85e-03  6.00e-01
     169  1.38e+01  3.75e-01  1.01e+03  1.66e+01  6.64e-04  9.74e-03  6.00e-01
     170  1.37e+01  3.75e-01  1.00e+03  1.66e+01  6.56e-04  9.63e-03  6.00e-01
     171  1.37e+01  3.75e-01  1.00e+03  1.65e+01  6.48e-04  9.52e-03  6.00e-01
     172  1.37e+01  3.75e-01  1.00e+03  1.65e+01  6.39e-04  9.41e-03  6.00e-01
     173  1.37e+01  3.75e-01  1.00e+03  1.65e+01  6.32e-04  9.30e-03  6.00e-01
     174  1.36e+01  3.75e-01  9.98e+02  1.65e+01  6.24e-04  9.19e-03  6.00e-01
     175  1.36e+01  3.75e-01  9.96e+02  1.65e+01  6.16e-04  9.08e-03  6.00e-01
     176  1.36e+01  3.75e-01  9.95e+02  1.64e+01  6.08e-04  8.98e-03  6.00e-01
     177  1.36e+01  3.74e-01  9.93e+02  1.64e+01  6.01e-04  8.88e-03  6.00e-01
     178  1.36e+01  3.74e-01  9.92e+02  1.64e+01  5.93e-04  8.78e-03  6.00e-01
     179  1.36e+01  3.74e-01  9.90e+02  1.64e+01  5.86e-04  8.68e-03  6.00e-01
     180  1.35e+01  3.74e-01  9.88e+02  1.64e+01  5.78e-04  8.59e-03  6.00e-01
     181  1.35e+01  3.74e-01  9.87e+02  1.64e+01  5.71e-04  8.49e-03  6.00e-01
     182  1.35e+01  3.74e-01  9.85e+02  1.63e+01  5.64e-04  8.40e-03  6.00e-01
     183  1.35e+01  3.74e-01  9.84e+02  1.63e+01  5.56e-04  8.31e-03  6.00e-01
     184  1.35e+01  3.74e-01  9.82e+02  1.63e+01  5.49e-04  8.23e-03  6.00e-01
     185  1.34e+01  3.74e-01  9.80e+02  1.63e+01  5.42e-04  8.14e-03  6.00e-01
     186  1.34e+01  3.74e-01  9.79e+02  1.63e+01  5.35e-04  8.06e-03  6.00e-01
     187  1.34e+01  3.74e-01  9.77e+02  1.63e+01  5.28e-04  7.98e-03  6.00e-01
     188  1.34e+01  3.74e-01  9.76e+02  1.62e+01  5.22e-04  7.90e-03  6.00e-01
     189  1.34e+01  3.74e-01  9.74e+02  1.62e+01  5.15e-04  7.83e-03  6.00e-01
     190  1.33e+01  3.74e-01  9.73e+02  1.62e+01  5.09e-04  7.75e-03  6.00e-01
     191  1.33e+01  3.74e-01  9.71e+02  1.62e+01  5.02e-04  7.67e-03  6.00e-01
     192  1.33e+01  3.74e-01  9.70e+02  1.62e+01  4.96e-04  7.59e-03  6.00e-01
     193  1.33e+01  3.73e-01  9.69e+02  1.62e+01  4.90e-04  7.52e-03  6.00e-01
     194  1.33e+01  3.73e-01  9.67e+02  1.62e+01  4.84e-04  7.44e-03  6.00e-01
     195  1.33e+01  3.73e-01  9.66e+02  1.61e+01  4.79e-04  7.37e-03  6.00e-01
     196  1.32e+01  3.73e-01  9.65e+02  1.61e+01  4.73e-04  7.29e-03  6.00e-01
     197  1.32e+01  3.73e-01  9.64e+02  1.61e+01  4.67e-04  7.21e-03  6.00e-01
     198  1.32e+01  3.73e-01  9.63e+02  1.61e+01  4.62e-04  7.14e-03  6.00e-01
     199  1.32e+01  3.73e-01  9.62e+02  1.61e+01  4.57e-04  7.06e-03  6.00e-01
    --------------------------------------------------------------------------


Display solve time and reconstruction performance.

.. code:: ipython3

    print("AddMaskSim wrapped ConvBPDN solve time: %.2fs" % t)
    print("Corrupted image PSNR: %5.2f dB" % metric.psnr(img, imgw))
    print("Recovered image PSNR: %5.2f dB" % metric.psnr(img, imgr))


.. parsed-literal::

    AddMaskSim wrapped ConvBPDN solve time: 1.57s
    Corrupted image PSNR:  9.10 dB
    Recovered image PSNR: 25.51 dB


Display reference, test, and reconstructed image

.. code:: ipython3

    fig = plot.figure(figsize=(21, 7))
    plot.subplot(1, 3, 1)
    plot.imview(img, title='Reference image', fig=fig)
    plot.subplot(1, 3, 2)
    plot.imview(imgw, title='Corrupted image', fig=fig)
    plot.subplot(1, 3, 3)
    plot.imview(imgr, title='Reconstructed image', fig=fig)
    fig.show()



.. image:: cbpdn_ams_grd_gry_files/cbpdn_ams_grd_gry_23_0.png


Display lowpass component and sparse representation

.. code:: ipython3

    fig = plot.figure(figsize=(14, 7))
    plot.subplot(1, 2, 1)
    plot.imview(X[..., 0], cmap=plot.cm.Blues, title='Lowpass component', fig=fig)
    plot.subplot(1, 2, 2)
    plot.imview(np.sum(abs(X[..., 1:]).squeeze(), axis=-1), cmap=plot.cm.Blues,
                title='Sparse representation', fig=fig)
    fig.show()



.. image:: cbpdn_ams_grd_gry_files/cbpdn_ams_grd_gry_25_0.png


Plot functional value, residuals, and rho (not available if GPU
implementation used).

.. code:: ipython3

    if ams is not None:
        its = ams.getitstat()
        fig = plot.figure(figsize=(21, 7))
        plot.subplot(1, 3, 1)
        plot.plot(its.ObjFun, xlbl='Iterations', ylbl='Functional', fig=fig)
        plot.subplot(1, 3, 2)
        plot.plot(np.vstack((its.PrimalRsdl, its.DualRsdl)).T, ptyp='semilogy',
                  xlbl='Iterations', ylbl='Residual', lgnd=['Primal', 'Dual'],
                  fig=fig)
        plot.subplot(1, 3, 3)
        plot.plot(its.Rho, xlbl='Iterations', ylbl='Penalty Parameter', fig=fig)
        fig.show()
