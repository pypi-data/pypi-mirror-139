.. _examples_csc_cbpdn_ams_gry:

CSC with a Spatial Mask
=======================

This example demonstrates the use of :class:`.cbpdn.AddMaskSim` for
convolutional sparse coding with a spatial mask
:cite:`wohlberg-2016-boundary`. If the ``sporco-cuda`` extension is
installed and a GPU is available, a GPU accelerated version is used. The
example problem is inpainting of randomly distributed corruption of a
greyscale image.

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
    from sporco.admm import tvl2
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
    spad = lambda x:  np.pad(x, pn, mode='symmetric')
    zpad = lambda x:  np.pad(x, pn, mode='constant')
    crop = lambda x: x[pn:-pn, pn:-pn]

Construct padded mask and test image.

.. code:: ipython3

    mskp = zpad(msk)
    imgwp = spad(imgw)

:math:`\ell_2`-TV denoising with a spatial mask as a non-linear lowpass
filter. The highpass component is the difference between the test image
and the lowpass component, multiplied by the mask for faster convergence
of the convolutional sparse coding (see
:cite:`wohlberg-2017-convolutional3`).

.. code:: ipython3

    lmbda = 0.05
    opt = tvl2.TVL2Denoise.Options({'Verbose': False, 'MaxMainIter': 200,
                        'DFidWeight': mskp, 'gEvalY': False,
                        'AutoRho': {'Enabled': True}})
    b = tvl2.TVL2Denoise(imgwp, lmbda, opt)
    sl = b.solve()
    sh = mskp * (imgwp - sl)

Load dictionary.

.. code:: ipython3

    D = util.convdicts()['G:8x8x128']

Set up :class:`.admm.cbpdn.ConvBPDN` options.

.. code:: ipython3

    lmbda = 2e-2
    opt = cbpdn.ConvBPDN.Options({'Verbose': True, 'MaxMainIter': 200,
                        'HighMemSolve': True, 'RelStopTol': 5e-3,
                        'AuxVarObj': False, 'RelaxParam': 1.8,
                        'rho': 5e1*lmbda + 1e-1, 'AutoRho': {'Enabled': False,
                        'StdResiduals': False}})

Construct :class:`.admm.cbpdn.AddMaskSim` wrapper for
:class:`.admm.cbpdn.ConvBPDN` and solve via wrapper. This example
could also have made use of :class:`.admm.cbpdn.ConvBPDNMaskDcpl` (see
example ``cbpdn_md_gry``), which has similar performance in this
application, but :class:`.admm.cbpdn.AddMaskSim` has the advantage of
greater flexibility in that the wrapper can be applied to a variety of
CSC solver objects. If the ``sporco-cuda`` extension is installed and a
GPU is available, use the CUDA implementation of this combination.

.. code:: ipython3

    if cuda.device_count() > 0:
        ams = None
        print('%s GPU found: running CUDA solver' % cuda.device_name())
        tm = util.Timer()
        with sys_pipes(), util.ContextTimer(tm):
            X = cuda.cbpdnmsk(D, sh, mskp, lmbda, opt)
        t = tm.elapsed()
        imgr = crop(sl + np.sum(fftconv(D, X, axes=(0, 1)), axis=-1))
    else:
        ams = cbpdn.AddMaskSim(cbpdn.ConvBPDN, D, sh, mskp, lmbda, opt=opt)
        X = ams.solve()
        t = ams.timer.elapsed('solve')
        imgr = crop(sl + ams.reconstruct().squeeze())


.. parsed-literal::

    GeForce RTX 2080 Ti GPU found: running CUDA solver
    Itn   Fnc       DFid      Regℓ1     r         s         ρ
    ----------------------------------------------------------------
       0  3.07e+01  4.16e-02  1.53e+03  9.94e-01  1.85e-01  1.10e+00
       1  2.69e+01  2.13e-01  1.33e+03  8.05e-01  2.20e-01  1.10e+00
       2  2.51e+01  3.39e-01  1.24e+03  4.52e-01  1.83e-01  1.10e+00
       3  2.41e+01  4.19e-01  1.19e+03  3.05e-01  1.48e-01  1.10e+00
       4  2.34e+01  4.80e-01  1.14e+03  2.30e-01  1.24e-01  1.10e+00
       5  2.29e+01  5.29e-01  1.12e+03  1.87e-01  1.07e-01  1.10e+00
       6  2.27e+01  5.69e-01  1.11e+03  1.60e-01  9.26e-02  1.10e+00
       7  2.26e+01  6.02e-01  1.10e+03  1.41e-01  8.09e-02  1.10e+00
       8  2.25e+01  6.33e-01  1.09e+03  1.27e-01  7.18e-02  1.10e+00
       9  2.24e+01  6.61e-01  1.09e+03  1.17e-01  6.47e-02  1.10e+00
      10  2.22e+01  6.88e-01  1.07e+03  1.09e-01  5.94e-02  1.10e+00
      11  2.19e+01  7.15e-01  1.06e+03  1.02e-01  5.54e-02  1.10e+00
      12  2.16e+01  7.42e-01  1.04e+03  9.68e-02  5.24e-02  1.10e+00
      13  2.13e+01  7.68e-01  1.03e+03  9.21e-02  5.03e-02  1.10e+00
      14  2.10e+01  7.92e-01  1.01e+03  8.81e-02  4.86e-02  1.10e+00
      15  2.08e+01  8.13e-01  9.99e+02  8.45e-02  4.73e-02  1.10e+00
      16  2.05e+01  8.33e-01  9.86e+02  8.13e-02  4.61e-02  1.10e+00
      17  2.03e+01  8.50e-01  9.74e+02  7.84e-02  4.52e-02  1.10e+00
      18  2.02e+01  8.66e-01  9.64e+02  7.56e-02  4.40e-02  1.10e+00
      19  2.00e+01  8.82e-01  9.57e+02  7.31e-02  4.23e-02  1.10e+00
      20  1.99e+01  8.97e-01  9.51e+02  7.08e-02  4.06e-02  1.10e+00
      21  1.97e+01  9.13e-01  9.40e+02  6.85e-02  3.89e-02  1.10e+00
      22  1.94e+01  9.30e-01  9.24e+02  6.63e-02  3.74e-02  1.10e+00
      23  1.90e+01  9.47e-01  9.03e+02  6.41e-02  3.61e-02  1.10e+00
      24  1.86e+01  9.66e-01  8.80e+02  6.20e-02  3.50e-02  1.10e+00
      25  1.81e+01  9.85e-01  8.56e+02  5.99e-02  3.37e-02  1.10e+00
      26  1.77e+01  1.00e+00  8.33e+02  5.79e-02  3.24e-02  1.10e+00
      27  1.73e+01  1.02e+00  8.13e+02  5.60e-02  3.12e-02  1.10e+00
      28  1.69e+01  1.04e+00  7.95e+02  5.42e-02  3.00e-02  1.10e+00
      29  1.67e+01  1.06e+00  7.80e+02  5.24e-02  2.88e-02  1.10e+00
      30  1.64e+01  1.08e+00  7.66e+02  5.08e-02  2.79e-02  1.10e+00
      31  1.62e+01  1.10e+00  7.54e+02  4.92e-02  2.69e-02  1.10e+00
      32  1.60e+01  1.11e+00  7.44e+02  4.77e-02  2.61e-02  1.10e+00
      33  1.58e+01  1.12e+00  7.35e+02  4.63e-02  2.53e-02  1.10e+00
      34  1.57e+01  1.14e+00  7.27e+02  4.50e-02  2.45e-02  1.10e+00
      35  1.55e+01  1.15e+00  7.20e+02  4.37e-02  2.37e-02  1.10e+00
      36  1.54e+01  1.16e+00  7.13e+02  4.26e-02  2.30e-02  1.10e+00
      37  1.53e+01  1.17e+00  7.06e+02  4.15e-02  2.23e-02  1.10e+00
      38  1.51e+01  1.17e+00  6.98e+02  4.04e-02  2.17e-02  1.10e+00
      39  1.50e+01  1.18e+00  6.89e+02  3.94e-02  2.11e-02  1.10e+00
      40  1.48e+01  1.19e+00  6.79e+02  3.84e-02  2.06e-02  1.10e+00
      41  1.46e+01  1.20e+00  6.69e+02  3.74e-02  2.02e-02  1.10e+00
      42  1.44e+01  1.21e+00  6.60e+02  3.65e-02  1.98e-02  1.10e+00
      43  1.42e+01  1.22e+00  6.51e+02  3.56e-02  1.93e-02  1.10e+00
      44  1.41e+01  1.23e+00  6.44e+02  3.48e-02  1.88e-02  1.10e+00
      45  1.40e+01  1.23e+00  6.37e+02  3.40e-02  1.83e-02  1.10e+00
      46  1.39e+01  1.24e+00  6.31e+02  3.32e-02  1.78e-02  1.10e+00
      47  1.37e+01  1.25e+00  6.25e+02  3.24e-02  1.73e-02  1.10e+00
      48  1.36e+01  1.25e+00  6.19e+02  3.17e-02  1.68e-02  1.10e+00
      49  1.35e+01  1.26e+00  6.14e+02  3.10e-02  1.64e-02  1.10e+00
      50  1.34e+01  1.27e+00  6.08e+02  3.03e-02  1.61e-02  1.10e+00
      51  1.33e+01  1.27e+00  6.03e+02  2.96e-02  1.57e-02  1.10e+00
      52  1.32e+01  1.28e+00  5.97e+02  2.90e-02  1.54e-02  1.10e+00
      53  1.31e+01  1.28e+00  5.92e+02  2.83e-02  1.51e-02  1.10e+00
      54  1.30e+01  1.28e+00  5.87e+02  2.77e-02  1.48e-02  1.10e+00
      55  1.29e+01  1.29e+00  5.82e+02  2.72e-02  1.45e-02  1.10e+00
      56  1.28e+01  1.29e+00  5.78e+02  2.66e-02  1.42e-02  1.10e+00
      57  1.28e+01  1.29e+00  5.73e+02  2.61e-02  1.39e-02  1.10e+00
      58  1.27e+01  1.30e+00  5.69e+02  2.56e-02  1.36e-02  1.10e+00
      59  1.26e+01  1.30e+00  5.64e+02  2.52e-02  1.33e-02  1.10e+00
      60  1.25e+01  1.30e+00  5.60e+02  2.47e-02  1.30e-02  1.10e+00
      61  1.24e+01  1.30e+00  5.56e+02  2.43e-02  1.28e-02  1.10e+00
      62  1.23e+01  1.31e+00  5.51e+02  2.38e-02  1.25e-02  1.10e+00
      63  1.22e+01  1.31e+00  5.47e+02  2.34e-02  1.23e-02  1.10e+00
      64  1.22e+01  1.31e+00  5.42e+02  2.30e-02  1.21e-02  1.10e+00
      65  1.21e+01  1.31e+00  5.38e+02  2.26e-02  1.19e-02  1.10e+00
      66  1.20e+01  1.32e+00  5.33e+02  2.22e-02  1.17e-02  1.10e+00
      67  1.19e+01  1.32e+00  5.29e+02  2.18e-02  1.15e-02  1.10e+00
      68  1.18e+01  1.32e+00  5.25e+02  2.14e-02  1.13e-02  1.10e+00
      69  1.18e+01  1.32e+00  5.22e+02  2.11e-02  1.11e-02  1.10e+00
      70  1.17e+01  1.33e+00  5.19e+02  2.07e-02  1.10e-02  1.10e+00
      71  1.16e+01  1.33e+00  5.16e+02  2.04e-02  1.08e-02  1.10e+00
      72  1.16e+01  1.33e+00  5.13e+02  2.01e-02  1.05e-02  1.10e+00
      73  1.15e+01  1.34e+00  5.11e+02  1.98e-02  1.03e-02  1.10e+00
      74  1.15e+01  1.34e+00  5.08e+02  1.95e-02  1.01e-02  1.10e+00
      75  1.15e+01  1.34e+00  5.06e+02  1.92e-02  9.91e-03  1.10e+00
      76  1.14e+01  1.34e+00  5.03e+02  1.89e-02  9.72e-03  1.10e+00
      77  1.13e+01  1.34e+00  5.00e+02  1.86e-02  9.54e-03  1.10e+00
      78  1.13e+01  1.35e+00  4.97e+02  1.83e-02  9.38e-03  1.10e+00
      79  1.12e+01  1.35e+00  4.94e+02  1.80e-02  9.24e-03  1.10e+00
      80  1.12e+01  1.35e+00  4.90e+02  1.77e-02  9.10e-03  1.10e+00
      81  1.11e+01  1.35e+00  4.87e+02  1.74e-02  8.98e-03  1.10e+00
      82  1.10e+01  1.36e+00  4.84e+02  1.71e-02  8.87e-03  1.10e+00
      83  1.10e+01  1.36e+00  4.81e+02  1.69e-02  8.75e-03  1.10e+00
      84  1.09e+01  1.36e+00  4.78e+02  1.66e-02  8.63e-03  1.10e+00
      85  1.09e+01  1.36e+00  4.75e+02  1.64e-02  8.50e-03  1.10e+00
      86  1.08e+01  1.36e+00  4.73e+02  1.61e-02  8.36e-03  1.10e+00
      87  1.08e+01  1.37e+00  4.71e+02  1.59e-02  8.23e-03  1.10e+00
      88  1.07e+01  1.37e+00  4.68e+02  1.57e-02  8.10e-03  1.10e+00
      89  1.07e+01  1.37e+00  4.66e+02  1.54e-02  7.97e-03  1.10e+00
      90  1.07e+01  1.37e+00  4.64e+02  1.52e-02  7.84e-03  1.10e+00
      91  1.06e+01  1.37e+00  4.62e+02  1.50e-02  7.71e-03  1.10e+00
      92  1.06e+01  1.38e+00  4.60e+02  1.48e-02  7.59e-03  1.10e+00
      93  1.05e+01  1.38e+00  4.58e+02  1.46e-02  7.47e-03  1.10e+00
      94  1.05e+01  1.38e+00  4.56e+02  1.44e-02  7.35e-03  1.10e+00
      95  1.05e+01  1.38e+00  4.54e+02  1.42e-02  7.23e-03  1.10e+00
      96  1.04e+01  1.38e+00  4.53e+02  1.40e-02  7.12e-03  1.10e+00
      97  1.04e+01  1.39e+00  4.51e+02  1.38e-02  7.00e-03  1.10e+00
      98  1.04e+01  1.39e+00  4.49e+02  1.36e-02  6.90e-03  1.10e+00
      99  1.03e+01  1.39e+00  4.47e+02  1.34e-02  6.79e-03  1.10e+00
     100  1.03e+01  1.39e+00  4.46e+02  1.32e-02  6.68e-03  1.10e+00
     101  1.03e+01  1.39e+00  4.44e+02  1.30e-02  6.58e-03  1.10e+00
     102  1.02e+01  1.39e+00  4.42e+02  1.28e-02  6.48e-03  1.10e+00
     103  1.02e+01  1.39e+00  4.41e+02  1.27e-02  6.39e-03  1.10e+00
     104  1.02e+01  1.40e+00  4.39e+02  1.25e-02  6.31e-03  1.10e+00
     105  1.01e+01  1.40e+00  4.37e+02  1.23e-02  6.23e-03  1.10e+00
     106  1.01e+01  1.40e+00  4.35e+02  1.21e-02  6.16e-03  1.10e+00
     107  1.01e+01  1.40e+00  4.33e+02  1.20e-02  6.09e-03  1.10e+00
     108  1.00e+01  1.40e+00  4.32e+02  1.18e-02  6.01e-03  1.10e+00
     109  1.00e+01  1.40e+00  4.30e+02  1.17e-02  5.94e-03  1.10e+00
     110  9.97e+00  1.40e+00  4.28e+02  1.15e-02  5.87e-03  1.10e+00
     111  9.93e+00  1.40e+00  4.27e+02  1.14e-02  5.80e-03  1.10e+00
     112  9.90e+00  1.40e+00  4.25e+02  1.12e-02  5.72e-03  1.10e+00
     113  9.87e+00  1.40e+00  4.23e+02  1.11e-02  5.65e-03  1.10e+00
     114  9.85e+00  1.41e+00  4.22e+02  1.09e-02  5.57e-03  1.10e+00
     115  9.82e+00  1.41e+00  4.21e+02  1.08e-02  5.49e-03  1.10e+00
     116  9.79e+00  1.41e+00  4.19e+02  1.07e-02  5.41e-03  1.10e+00
     117  9.76e+00  1.41e+00  4.18e+02  1.05e-02  5.34e-03  1.10e+00
     118  9.74e+00  1.41e+00  4.16e+02  1.04e-02  5.27e-03  1.10e+00
     119  9.71e+00  1.41e+00  4.15e+02  1.03e-02  5.20e-03  1.10e+00
     120  9.69e+00  1.41e+00  4.14e+02  1.01e-02  5.13e-03  1.10e+00
     121  9.66e+00  1.41e+00  4.13e+02  1.00e-02  5.06e-03  1.10e+00
     122  9.64e+00  1.41e+00  4.11e+02  9.88e-03  4.99e-03  1.10e+00
     123  9.61e+00  1.41e+00  4.10e+02  9.75e-03  4.93e-03  1.10e+00
     124  9.59e+00  1.41e+00  4.09e+02  9.63e-03  4.87e-03  1.10e+00
     125  9.57e+00  1.41e+00  4.08e+02  9.51e-03  4.81e-03  1.10e+00
     126  9.54e+00  1.41e+00  4.06e+02  9.40e-03  4.75e-03  1.10e+00
     127  9.52e+00  1.42e+00  4.05e+02  9.28e-03  4.69e-03  1.10e+00
     128  9.50e+00  1.42e+00  4.04e+02  9.17e-03  4.63e-03  1.10e+00
     129  9.47e+00  1.42e+00  4.03e+02  9.05e-03  4.57e-03  1.10e+00
     130  9.45e+00  1.42e+00  4.02e+02  8.95e-03  4.51e-03  1.10e+00
     131  9.43e+00  1.42e+00  4.00e+02  8.84e-03  4.46e-03  1.10e+00
     132  9.41e+00  1.42e+00  3.99e+02  8.73e-03  4.40e-03  1.10e+00
     133  9.38e+00  1.42e+00  3.98e+02  8.62e-03  4.35e-03  1.10e+00
     134  9.36e+00  1.42e+00  3.97e+02  8.52e-03  4.30e-03  1.10e+00
     135  9.34e+00  1.42e+00  3.96e+02  8.42e-03  4.24e-03  1.10e+00
     136  9.32e+00  1.42e+00  3.95e+02  8.32e-03  4.19e-03  1.10e+00
     137  9.30e+00  1.42e+00  3.94e+02  8.22e-03  4.13e-03  1.10e+00
     138  9.29e+00  1.42e+00  3.93e+02  8.13e-03  4.08e-03  1.10e+00
     139  9.27e+00  1.42e+00  3.92e+02  8.03e-03  4.03e-03  1.10e+00
     140  9.25e+00  1.42e+00  3.91e+02  7.94e-03  3.98e-03  1.10e+00
     141  9.23e+00  1.43e+00  3.90e+02  7.85e-03  3.93e-03  1.10e+00
     142  9.21e+00  1.43e+00  3.89e+02  7.76e-03  3.89e-03  1.10e+00
     143  9.20e+00  1.43e+00  3.88e+02  7.67e-03  3.84e-03  1.10e+00
     144  9.18e+00  1.43e+00  3.88e+02  7.58e-03  3.80e-03  1.10e+00
     145  9.16e+00  1.43e+00  3.87e+02  7.50e-03  3.75e-03  1.10e+00
     146  9.14e+00  1.43e+00  3.86e+02  7.41e-03  3.71e-03  1.10e+00
     147  9.12e+00  1.43e+00  3.85e+02  7.33e-03  3.67e-03  1.10e+00
     148  9.10e+00  1.43e+00  3.84e+02  7.25e-03  3.63e-03  1.10e+00
     149  9.09e+00  1.43e+00  3.83e+02  7.16e-03  3.59e-03  1.10e+00
     150  9.07e+00  1.43e+00  3.82e+02  7.08e-03  3.56e-03  1.10e+00
     151  9.05e+00  1.43e+00  3.81e+02  7.00e-03  3.52e-03  1.10e+00
     152  9.03e+00  1.43e+00  3.80e+02  6.93e-03  3.48e-03  1.10e+00
     153  9.02e+00  1.43e+00  3.79e+02  6.85e-03  3.45e-03  1.10e+00
     154  9.00e+00  1.43e+00  3.78e+02  6.77e-03  3.41e-03  1.10e+00
     155  8.99e+00  1.43e+00  3.78e+02  6.70e-03  3.37e-03  1.10e+00
     156  8.97e+00  1.43e+00  3.77e+02  6.63e-03  3.33e-03  1.10e+00
     157  8.96e+00  1.43e+00  3.76e+02  6.55e-03  3.29e-03  1.10e+00
     158  8.94e+00  1.43e+00  3.75e+02  6.48e-03  3.25e-03  1.10e+00
     159  8.93e+00  1.44e+00  3.75e+02  6.41e-03  3.21e-03  1.10e+00
     160  8.92e+00  1.44e+00  3.74e+02  6.35e-03  3.18e-03  1.10e+00
     161  8.90e+00  1.44e+00  3.73e+02  6.28e-03  3.14e-03  1.10e+00
     162  8.89e+00  1.44e+00  3.73e+02  6.21e-03  3.10e-03  1.10e+00
     163  8.88e+00  1.44e+00  3.72e+02  6.15e-03  3.06e-03  1.10e+00
     164  8.86e+00  1.44e+00  3.71e+02  6.08e-03  3.03e-03  1.10e+00
     165  8.85e+00  1.44e+00  3.71e+02  6.02e-03  2.99e-03  1.10e+00
     166  8.84e+00  1.44e+00  3.70e+02  5.95e-03  2.96e-03  1.10e+00
     167  8.82e+00  1.44e+00  3.69e+02  5.89e-03  2.93e-03  1.10e+00
     168  8.81e+00  1.44e+00  3.69e+02  5.83e-03  2.90e-03  1.10e+00
     169  8.80e+00  1.44e+00  3.68e+02  5.77e-03  2.87e-03  1.10e+00
     170  8.79e+00  1.44e+00  3.67e+02  5.70e-03  2.84e-03  1.10e+00
     171  8.77e+00  1.44e+00  3.67e+02  5.64e-03  2.81e-03  1.10e+00
     172  8.76e+00  1.44e+00  3.66e+02  5.58e-03  2.79e-03  1.10e+00
     173  8.75e+00  1.44e+00  3.65e+02  5.52e-03  2.76e-03  1.10e+00
     174  8.73e+00  1.44e+00  3.65e+02  5.47e-03  2.73e-03  1.10e+00
     175  8.72e+00  1.44e+00  3.64e+02  5.41e-03  2.71e-03  1.10e+00
     176  8.71e+00  1.44e+00  3.63e+02  5.36e-03  2.68e-03  1.10e+00
     177  8.70e+00  1.44e+00  3.63e+02  5.30e-03  2.64e-03  1.10e+00
     178  8.69e+00  1.44e+00  3.62e+02  5.25e-03  2.61e-03  1.10e+00
     179  8.68e+00  1.44e+00  3.62e+02  5.20e-03  2.58e-03  1.10e+00
     180  8.67e+00  1.44e+00  3.61e+02  5.15e-03  2.55e-03  1.10e+00
     181  8.66e+00  1.44e+00  3.61e+02  5.10e-03  2.51e-03  1.10e+00
     182  8.65e+00  1.44e+00  3.61e+02  5.05e-03  2.48e-03  1.10e+00
     183  8.64e+00  1.44e+00  3.60e+02  5.00e-03  2.46e-03  1.10e+00
    ----------------------------------------------------------------


Display solve time and reconstruction performance.

.. code:: ipython3

    print("AddMaskSim wrapped ConvBPDN solve time: %.2fs" % t)
    print("Corrupted image PSNR: %5.2f dB" % metric.psnr(img, imgw))
    print("Recovered image PSNR: %5.2f dB" % metric.psnr(img, imgr))


.. parsed-literal::

    AddMaskSim wrapped ConvBPDN solve time: 1.49s
    Corrupted image PSNR:  9.10 dB
    Recovered image PSNR: 24.56 dB


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



.. image:: cbpdn_ams_gry_files/cbpdn_ams_gry_21_0.png


Display lowpass component and sparse representation

.. code:: ipython3

    fig = plot.figure(figsize=(14, 7))
    plot.subplot(1, 2, 1)
    plot.imview(sl, cmap=plot.cm.Blues, title='Lowpass component', fig=fig)
    plot.subplot(1, 2, 2)
    plot.imview(np.sum(abs(X).squeeze(), axis=-1), cmap=plot.cm.Blues,
                title='Sparse representation', fig=fig)
    fig.show()



.. image:: cbpdn_ams_gry_files/cbpdn_ams_gry_23_0.png


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
