.. _examples_csc_cbpdn_md_gry:

CSC with a Spatial Mask
=======================

This example demonstrates the use of :class:`.cbpdn.ConvBPDNMaskDcpl`
for convolutional sparse coding with a spatial mask
:cite:`heide-2015-fast`. The example problem is inpainting of randomly
distributed corruption of a greyscale image.

.. code:: ipython3

    from __future__ import print_function
    from builtins import input

    import pyfftw   # See https://github.com/pyFFTW/pyFFTW/issues/40
    import numpy as np

    from sporco.admm import tvl2
    from sporco.admm import cbpdn
    from sporco import util
    from sporco import signal
    from sporco import metric
    from sporco import plot
    plot.config_notebook_plotting()

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

Set up :class:`.admm.cbpdn.ConvBPDNMaskDcpl` options.

.. code:: ipython3

    lmbda = 2e-2
    opt = cbpdn.ConvBPDNMaskDcpl.Options({'Verbose': True, 'MaxMainIter': 200,
                        'HighMemSolve': True, 'RelStopTol': 3e-2,
                        'AuxVarObj': False, 'RelaxParam': 1.8,
                        'rho': 5e1*lmbda + 1e-1, 'AutoRho': {'Enabled': False,
                        'StdResiduals': False}})

Construct :class:`.admm.cbpdn.ConvBPDNMaskDcpl` object and solve.

.. code:: ipython3

    b = cbpdn.ConvBPDNMaskDcpl(D, sh, lmbda, mskp, opt=opt)
    X = b.solve()


.. parsed-literal::

    Itn   Fnc       DFid      Regℓ1     r         s
    ------------------------------------------------------
       0  3.28e+01  2.86e-02  1.64e+03  1.34e-01  1.07e+00
       1  2.81e+01  1.61e-01  1.40e+03  1.20e-01  1.25e+00
       2  2.64e+01  2.74e-01  1.31e+03  1.13e-01  1.13e+00
       3  2.57e+01  3.48e-01  1.27e+03  1.08e-01  9.51e-01
       4  2.50e+01  4.06e-01  1.23e+03  1.04e-01  8.06e-01
       5  2.45e+01  4.54e-01  1.20e+03  9.77e-02  6.92e-01
       6  2.44e+01  4.97e-01  1.20e+03  9.25e-02  5.98e-01
       7  2.44e+01  5.39e-01  1.19e+03  8.78e-02  5.19e-01
       8  2.43e+01  5.80e-01  1.19e+03  8.37e-02  4.55e-01
       9  2.43e+01  6.17e-01  1.18e+03  8.01e-02  4.00e-01
      10  2.41e+01  6.49e-01  1.17e+03  7.68e-02  3.55e-01
      11  2.39e+01  6.79e-01  1.16e+03  7.40e-02  3.18e-01
      12  2.37e+01  7.07e-01  1.15e+03  7.14e-02  2.90e-01
      13  2.34e+01  7.33e-01  1.13e+03  6.91e-02  2.71e-01
      14  2.32e+01  7.58e-01  1.12e+03  6.70e-02  2.57e-01
      15  2.29e+01  7.79e-01  1.11e+03  6.51e-02  2.49e-01
      16  2.27e+01  7.99e-01  1.09e+03  6.33e-02  2.42e-01
      17  2.25e+01  8.16e-01  1.08e+03  6.16e-02  2.37e-01
      18  2.24e+01  8.32e-01  1.08e+03  6.00e-02  2.31e-01
      19  2.23e+01  8.48e-01  1.07e+03  5.86e-02  2.27e-01
      20  2.22e+01  8.65e-01  1.07e+03  5.72e-02  2.23e-01
      21  2.20e+01  8.82e-01  1.06e+03  5.58e-02  2.19e-01
      22  2.17e+01  9.01e-01  1.04e+03  5.44e-02  2.16e-01
      23  2.13e+01  9.21e-01  1.02e+03  5.30e-02  2.13e-01
      24  2.09e+01  9.42e-01  9.98e+02  5.16e-02  2.09e-01
      25  2.05e+01  9.63e-01  9.75e+02  5.03e-02  2.06e-01
      26  2.00e+01  9.85e-01  9.53e+02  4.91e-02  2.02e-01
      27  1.97e+01  1.01e+00  9.34e+02  4.79e-02  1.98e-01
      28  1.94e+01  1.03e+00  9.16e+02  4.68e-02  1.94e-01
      29  1.91e+01  1.04e+00  9.02e+02  4.57e-02  1.89e-01
      30  1.89e+01  1.06e+00  8.90e+02  4.47e-02  1.85e-01
      31  1.87e+01  1.08e+00  8.80e+02  4.38e-02  1.81e-01
      32  1.85e+01  1.09e+00  8.71e+02  4.29e-02  1.77e-01
      33  1.84e+01  1.11e+00  8.62e+02  4.20e-02  1.73e-01
      34  1.82e+01  1.12e+00  8.56e+02  4.12e-02  1.69e-01
      35  1.81e+01  1.13e+00  8.50e+02  4.05e-02  1.66e-01
      36  1.80e+01  1.14e+00  8.44e+02  3.98e-02  1.62e-01
      37  1.79e+01  1.15e+00  8.38e+02  3.91e-02  1.59e-01
      38  1.78e+01  1.16e+00  8.30e+02  3.84e-02  1.56e-01
      39  1.76e+01  1.17e+00  8.22e+02  3.78e-02  1.54e-01
      40  1.74e+01  1.18e+00  8.12e+02  3.71e-02  1.52e-01
      41  1.72e+01  1.19e+00  8.02e+02  3.65e-02  1.50e-01
      42  1.70e+01  1.19e+00  7.93e+02  3.59e-02  1.48e-01
      43  1.69e+01  1.20e+00  7.85e+02  3.53e-02  1.45e-01
      44  1.68e+01  1.21e+00  7.78e+02  3.47e-02  1.43e-01
      45  1.67e+01  1.22e+00  7.72e+02  3.42e-02  1.40e-01
      46  1.66e+01  1.23e+00  7.66e+02  3.37e-02  1.38e-01
      47  1.65e+01  1.23e+00  7.61e+02  3.32e-02  1.36e-01
      48  1.64e+01  1.24e+00  7.56e+02  3.27e-02  1.34e-01
      49  1.63e+01  1.25e+00  7.50e+02  3.22e-02  1.32e-01
      50  1.61e+01  1.25e+00  7.44e+02  3.17e-02  1.30e-01
      51  1.60e+01  1.26e+00  7.39e+02  3.12e-02  1.28e-01
      52  1.59e+01  1.26e+00  7.33e+02  3.07e-02  1.27e-01
      53  1.58e+01  1.27e+00  7.28e+02  3.03e-02  1.25e-01
      54  1.57e+01  1.27e+00  7.23e+02  2.98e-02  1.23e-01
      55  1.56e+01  1.28e+00  7.18e+02  2.94e-02  1.22e-01
      56  1.56e+01  1.28e+00  7.14e+02  2.90e-02  1.20e-01
      57  1.55e+01  1.28e+00  7.10e+02  2.87e-02  1.18e-01
      58  1.54e+01  1.28e+00  7.05e+02  2.83e-02  1.16e-01
      59  1.53e+01  1.28e+00  7.01e+02  2.79e-02  1.15e-01
      60  1.52e+01  1.29e+00  6.96e+02  2.76e-02  1.13e-01
      61  1.51e+01  1.29e+00  6.92e+02  2.72e-02  1.12e-01
      62  1.50e+01  1.29e+00  6.87e+02  2.69e-02  1.11e-01
      63  1.50e+01  1.29e+00  6.83e+02  2.66e-02  1.10e-01
      64  1.49e+01  1.30e+00  6.78e+02  2.63e-02  1.09e-01
      65  1.48e+01  1.30e+00  6.73e+02  2.59e-02  1.08e-01
      66  1.47e+01  1.30e+00  6.68e+02  2.56e-02  1.07e-01
      67  1.46e+01  1.30e+00  6.64e+02  2.53e-02  1.06e-01
      68  1.45e+01  1.31e+00  6.59e+02  2.50e-02  1.05e-01
      69  1.44e+01  1.31e+00  6.55e+02  2.48e-02  1.04e-01
      70  1.44e+01  1.31e+00  6.52e+02  2.45e-02  1.03e-01
      71  1.43e+01  1.32e+00  6.49e+02  2.42e-02  1.02e-01
      72  1.42e+01  1.32e+00  6.46e+02  2.40e-02  1.00e-01
      73  1.42e+01  1.32e+00  6.44e+02  2.37e-02  9.91e-02
      74  1.42e+01  1.32e+00  6.41e+02  2.35e-02  9.78e-02
      75  1.41e+01  1.33e+00  6.39e+02  2.32e-02  9.66e-02
      76  1.41e+01  1.33e+00  6.36e+02  2.30e-02  9.55e-02
      77  1.40e+01  1.33e+00  6.33e+02  2.28e-02  9.44e-02
      78  1.39e+01  1.33e+00  6.29e+02  2.25e-02  9.35e-02
      79  1.38e+01  1.34e+00  6.25e+02  2.23e-02  9.27e-02
      80  1.38e+01  1.34e+00  6.21e+02  2.20e-02  9.19e-02
      81  1.37e+01  1.34e+00  6.17e+02  2.18e-02  9.11e-02
      82  1.36e+01  1.34e+00  6.14e+02  2.15e-02  9.03e-02
      83  1.36e+01  1.34e+00  6.10e+02  2.13e-02  8.95e-02
      84  1.35e+01  1.35e+00  6.07e+02  2.11e-02  8.87e-02
      85  1.34e+01  1.35e+00  6.05e+02  2.09e-02  8.78e-02
      86  1.34e+01  1.35e+00  6.02e+02  2.07e-02  8.69e-02
      87  1.33e+01  1.35e+00  5.99e+02  2.05e-02  8.60e-02
      88  1.33e+01  1.35e+00  5.97e+02  2.03e-02  8.52e-02
      89  1.32e+01  1.36e+00  5.94e+02  2.01e-02  8.43e-02
      90  1.32e+01  1.36e+00  5.91e+02  1.99e-02  8.34e-02
      91  1.31e+01  1.36e+00  5.88e+02  1.97e-02  8.26e-02
      92  1.31e+01  1.36e+00  5.86e+02  1.95e-02  8.17e-02
      93  1.30e+01  1.37e+00  5.83e+02  1.93e-02  8.08e-02
      94  1.30e+01  1.37e+00  5.80e+02  1.91e-02  7.99e-02
      95  1.29e+01  1.37e+00  5.78e+02  1.89e-02  7.90e-02
      96  1.29e+01  1.37e+00  5.76e+02  1.88e-02  7.80e-02
      97  1.29e+01  1.37e+00  5.74e+02  1.86e-02  7.71e-02
      98  1.28e+01  1.38e+00  5.72e+02  1.84e-02  7.63e-02
      99  1.28e+01  1.38e+00  5.71e+02  1.83e-02  7.55e-02
     100  1.28e+01  1.38e+00  5.69e+02  1.81e-02  7.49e-02
     101  1.27e+01  1.38e+00  5.67e+02  1.79e-02  7.43e-02
     102  1.27e+01  1.38e+00  5.65e+02  1.77e-02  7.38e-02
     103  1.26e+01  1.38e+00  5.62e+02  1.76e-02  7.34e-02
     104  1.26e+01  1.38e+00  5.59e+02  1.74e-02  7.30e-02
     105  1.25e+01  1.39e+00  5.57e+02  1.72e-02  7.26e-02
     106  1.25e+01  1.39e+00  5.54e+02  1.71e-02  7.22e-02
     107  1.24e+01  1.39e+00  5.51e+02  1.69e-02  7.17e-02
     108  1.24e+01  1.39e+00  5.49e+02  1.68e-02  7.12e-02
     109  1.23e+01  1.39e+00  5.47e+02  1.66e-02  7.06e-02
     110  1.23e+01  1.39e+00  5.45e+02  1.65e-02  7.00e-02
     111  1.23e+01  1.39e+00  5.43e+02  1.63e-02  6.93e-02
     112  1.22e+01  1.39e+00  5.42e+02  1.62e-02  6.87e-02
     113  1.22e+01  1.39e+00  5.40e+02  1.61e-02  6.81e-02
     114  1.22e+01  1.39e+00  5.38e+02  1.59e-02  6.75e-02
     115  1.21e+01  1.39e+00  5.36e+02  1.58e-02  6.69e-02
     116  1.21e+01  1.40e+00  5.34e+02  1.56e-02  6.64e-02
     117  1.20e+01  1.40e+00  5.32e+02  1.55e-02  6.58e-02
     118  1.20e+01  1.40e+00  5.30e+02  1.54e-02  6.54e-02
     119  1.20e+01  1.40e+00  5.29e+02  1.53e-02  6.49e-02
     120  1.19e+01  1.40e+00  5.27e+02  1.51e-02  6.45e-02
     121  1.19e+01  1.40e+00  5.25e+02  1.50e-02  6.40e-02
     122  1.19e+01  1.40e+00  5.24e+02  1.49e-02  6.36e-02
     123  1.18e+01  1.40e+00  5.22e+02  1.47e-02  6.32e-02
     124  1.18e+01  1.40e+00  5.20e+02  1.46e-02  6.27e-02
     125  1.18e+01  1.40e+00  5.18e+02  1.45e-02  6.23e-02
     126  1.17e+01  1.40e+00  5.17e+02  1.44e-02  6.18e-02
     127  1.17e+01  1.40e+00  5.15e+02  1.43e-02  6.13e-02
     128  1.17e+01  1.40e+00  5.13e+02  1.41e-02  6.09e-02
     129  1.16e+01  1.41e+00  5.12e+02  1.40e-02  6.04e-02
     130  1.16e+01  1.41e+00  5.10e+02  1.39e-02  5.99e-02
     131  1.16e+01  1.41e+00  5.09e+02  1.38e-02  5.94e-02
     132  1.16e+01  1.41e+00  5.07e+02  1.37e-02  5.88e-02
     133  1.15e+01  1.41e+00  5.06e+02  1.36e-02  5.83e-02
     134  1.15e+01  1.41e+00  5.04e+02  1.35e-02  5.79e-02
     135  1.15e+01  1.41e+00  5.02e+02  1.34e-02  5.74e-02
     136  1.14e+01  1.41e+00  5.01e+02  1.33e-02  5.70e-02
     137  1.14e+01  1.41e+00  4.99e+02  1.31e-02  5.67e-02
     138  1.14e+01  1.41e+00  4.97e+02  1.30e-02  5.63e-02
     139  1.13e+01  1.41e+00  4.96e+02  1.29e-02  5.60e-02
     140  1.13e+01  1.41e+00  4.94e+02  1.28e-02  5.56e-02
     141  1.13e+01  1.41e+00  4.93e+02  1.27e-02  5.53e-02
     142  1.13e+01  1.41e+00  4.92e+02  1.27e-02  5.49e-02
     143  1.12e+01  1.41e+00  4.91e+02  1.26e-02  5.45e-02
     144  1.12e+01  1.41e+00  4.90e+02  1.25e-02  5.40e-02
     145  1.12e+01  1.41e+00  4.88e+02  1.24e-02  5.36e-02
     146  1.12e+01  1.42e+00  4.87e+02  1.23e-02  5.32e-02
     147  1.11e+01  1.42e+00  4.86e+02  1.22e-02  5.28e-02
     148  1.11e+01  1.42e+00  4.85e+02  1.21e-02  5.25e-02
     149  1.11e+01  1.42e+00  4.83e+02  1.20e-02  5.22e-02
     150  1.11e+01  1.42e+00  4.82e+02  1.19e-02  5.19e-02
     151  1.10e+01  1.42e+00  4.80e+02  1.18e-02  5.17e-02
     152  1.10e+01  1.42e+00  4.79e+02  1.17e-02  5.15e-02
     153  1.10e+01  1.42e+00  4.78e+02  1.17e-02  5.12e-02
     154  1.09e+01  1.42e+00  4.76e+02  1.16e-02  5.10e-02
     155  1.09e+01  1.42e+00  4.75e+02  1.15e-02  5.07e-02
     156  1.09e+01  1.42e+00  4.74e+02  1.14e-02  5.04e-02
     157  1.09e+01  1.42e+00  4.72e+02  1.13e-02  5.01e-02
     158  1.08e+01  1.42e+00  4.71e+02  1.13e-02  4.98e-02
     159  1.08e+01  1.42e+00  4.70e+02  1.12e-02  4.94e-02
     160  1.08e+01  1.42e+00  4.69e+02  1.11e-02  4.90e-02
     161  1.08e+01  1.42e+00  4.68e+02  1.10e-02  4.86e-02
     162  1.08e+01  1.43e+00  4.67e+02  1.09e-02  4.81e-02
     163  1.07e+01  1.43e+00  4.66e+02  1.09e-02  4.77e-02
     164  1.07e+01  1.43e+00  4.65e+02  1.08e-02  4.73e-02
     165  1.07e+01  1.43e+00  4.64e+02  1.07e-02  4.69e-02
     166  1.07e+01  1.43e+00  4.63e+02  1.07e-02  4.65e-02
     167  1.07e+01  1.43e+00  4.62e+02  1.06e-02  4.62e-02
     168  1.07e+01  1.43e+00  4.61e+02  1.05e-02  4.59e-02
     169  1.06e+01  1.43e+00  4.60e+02  1.04e-02  4.57e-02
     170  1.06e+01  1.43e+00  4.59e+02  1.04e-02  4.55e-02
     171  1.06e+01  1.43e+00  4.58e+02  1.03e-02  4.53e-02
     172  1.06e+01  1.43e+00  4.57e+02  1.02e-02  4.51e-02
     173  1.05e+01  1.43e+00  4.55e+02  1.01e-02  4.49e-02
     174  1.05e+01  1.43e+00  4.54e+02  1.00e-02  4.47e-02
     175  1.05e+01  1.43e+00  4.53e+02  9.98e-03  4.45e-02
     176  1.05e+01  1.43e+00  4.52e+02  9.91e-03  4.42e-02
     177  1.05e+01  1.43e+00  4.51e+02  9.85e-03  4.39e-02
     178  1.04e+01  1.43e+00  4.50e+02  9.79e-03  4.36e-02
     179  1.04e+01  1.43e+00  4.50e+02  9.73e-03  4.32e-02
     180  1.04e+01  1.43e+00  4.49e+02  9.67e-03  4.29e-02
     181  1.04e+01  1.43e+00  4.48e+02  9.61e-03  4.25e-02
     182  1.04e+01  1.43e+00  4.48e+02  9.55e-03  4.22e-02
     183  1.04e+01  1.43e+00  4.47e+02  9.49e-03  4.20e-02
     184  1.04e+01  1.43e+00  4.46e+02  9.43e-03  4.18e-02
     185  1.03e+01  1.43e+00  4.45e+02  9.36e-03  4.16e-02
     186  1.03e+01  1.44e+00  4.44e+02  9.30e-03  4.14e-02
     187  1.03e+01  1.44e+00  4.43e+02  9.23e-03  4.13e-02
     188  1.03e+01  1.44e+00  4.42e+02  9.17e-03  4.12e-02
     189  1.02e+01  1.44e+00  4.41e+02  9.10e-03  4.11e-02
     190  1.02e+01  1.44e+00  4.40e+02  9.04e-03  4.10e-02
     191  1.02e+01  1.44e+00  4.39e+02  8.98e-03  4.08e-02
     192  1.02e+01  1.44e+00  4.38e+02  8.93e-03  4.07e-02
     193  1.02e+01  1.44e+00  4.37e+02  8.87e-03  4.05e-02
     194  1.02e+01  1.44e+00  4.36e+02  8.81e-03  4.03e-02
     195  1.01e+01  1.44e+00  4.35e+02  8.76e-03  4.00e-02
     196  1.01e+01  1.44e+00  4.34e+02  8.70e-03  3.98e-02
     197  1.01e+01  1.44e+00  4.34e+02  8.65e-03  3.96e-02
     198  1.01e+01  1.44e+00  4.33e+02  8.60e-03  3.93e-02
     199  1.01e+01  1.44e+00  4.32e+02  8.54e-03  3.90e-02
    ------------------------------------------------------


Reconstruct from representation.

.. code:: ipython3

    imgr = crop(sl + b.reconstruct().squeeze())

Display solve time and reconstruction performance.

.. code:: ipython3

    print("ConvBPDNMaskDcpl solve time: %.2fs" % b.timer.elapsed('solve'))
    print("Corrupted image PSNR: %5.2f dB" % metric.psnr(img, imgw))
    print("Recovered image PSNR: %5.2f dB" % metric.psnr(img, imgr))


.. parsed-literal::

    ConvBPDNMaskDcpl solve time: 155.42s
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



.. image:: cbpdn_md_gry_files/cbpdn_md_gry_23_0.png


Display lowpass component and sparse representation

.. code:: ipython3

    fig = plot.figure(figsize=(14, 7))
    plot.subplot(1, 2, 1)
    plot.imview(sl, cmap=plot.cm.Blues, title='Lowpass component', fig=fig)
    plot.subplot(1, 2, 2)
    plot.imview(np.squeeze(np.sum(abs(X), axis=b.cri.axisM)),
                cmap=plot.cm.Blues, title='Sparse representation', fig=fig)
    fig.show()



.. image:: cbpdn_md_gry_files/cbpdn_md_gry_25_0.png


Plot functional value, residuals, and rho

.. code:: ipython3

    its = b.getitstat()
    fig = plot.figure(figsize=(21, 7))
    plot.subplot(1, 3, 1)
    plot.plot(its.ObjFun, xlbl='Iterations', ylbl='Functional', fig=fig)
    plot.subplot(1, 3, 2)
    plot.plot(np.vstack((its.PrimalRsdl, its.DualRsdl)).T,
              ptyp='semilogy', xlbl='Iterations', ylbl='Residual',
              lgnd=['Primal', 'Dual'], fig=fig)
    plot.subplot(1, 3, 3)
    plot.plot(its.Rho, xlbl='Iterations', ylbl='Penalty Parameter', fig=fig)
    fig.show()



.. image:: cbpdn_md_gry_files/cbpdn_md_gry_27_0.png

