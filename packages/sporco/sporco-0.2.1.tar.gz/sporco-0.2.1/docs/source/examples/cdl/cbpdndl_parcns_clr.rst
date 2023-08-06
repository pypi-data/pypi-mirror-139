.. _examples_cdl_cbpdndl_parcns_clr:

Convolutional Dictionary Learning
=================================

This example demonstrates the use of
:class:`.prlcnscdl.ConvBPDNDictLearn_Consensus` for learning a
convolutional dictionary from a set of colour training images
:cite:`wohlberg-2016-convolutional`. The dictionary learning algorithm
is based on the ADMM consensus dictionary update
:cite:`sorel-2016-fast` :cite:`garcia-2018-convolutional1`.

.. code:: ipython3

    from __future__ import print_function
    from builtins import input

    import pyfftw   # See https://github.com/pyFFTW/pyFFTW/issues/40
    import numpy as np

    from sporco.dictlrn import prlcnscdl
    from sporco import util
    from sporco import signal
    from sporco import plot
    plot.config_notebook_plotting()

Load training images.

.. code:: ipython3

    exim = util.ExampleImages(scaled=True, zoom=0.25)
    S1 = exim.image('barbara.png', idxexp=np.s_[10:522, 100:612])
    S2 = exim.image('kodim23.png', idxexp=np.s_[:, 60:572])
    S3 = exim.image('monarch.png', idxexp=np.s_[:, 160:672])
    S4 = exim.image('sail.png', idxexp=np.s_[:, 210:722])
    S5 = exim.image('tulips.png', idxexp=np.s_[:, 30:542])
    S = np.stack((S1, S2, S3, S4, S5), axis=3)

Highpass filter training images.

.. code:: ipython3

    npd = 16
    fltlmbd = 5
    sl, sh = signal.tikhonov_filter(S, fltlmbd, npd)

Construct initial dictionary.

.. code:: ipython3

    np.random.seed(12345)
    D0 = np.random.randn(8, 8, 3, 64)

Set regularization parameter and options for dictionary learning solver.

.. code:: ipython3

    lmbda = 0.2
    opt = prlcnscdl.ConvBPDNDictLearn_Consensus.Options({'Verbose': True,
                            'MaxMainIter': 200,
                            'CBPDN': {'rho': 50.0*lmbda + 0.5},
                            'CCMOD': {'rho': 1.0, 'ZeroMean': True}})

Create solver object and solve.

.. code:: ipython3

    d = prlcnscdl.ConvBPDNDictLearn_Consensus(D0, sh, lmbda, opt)
    D1 = d.solve()
    print("ConvBPDNDictLearn_Consensus solve time: %.2fs" %
          d.timer.elapsed('solve'))


.. parsed-literal::

    Itn   Fnc       DFid      Regℓ1
    ----------------------------------
       0  1.24e+03  1.19e+03  2.83e+02
       1  9.43e+02  6.77e+02  1.33e+03
       2  8.82e+02  4.16e+02  2.33e+03
       3  8.43e+02  3.10e+02  2.66e+03
       4  7.71e+02  2.67e+02  2.52e+03
       5  7.29e+02  2.69e+02  2.30e+03
       6  7.10e+02  2.73e+02  2.19e+03
       7  6.98e+02  2.65e+02  2.17e+03
       8  6.89e+02  2.51e+02  2.19e+03
       9  6.82e+02  2.39e+02  2.21e+03
      10  6.76e+02  2.32e+02  2.22e+03
      11  6.72e+02  2.29e+02  2.21e+03
      12  6.68e+02  2.28e+02  2.20e+03
      13  6.64e+02  2.28e+02  2.18e+03
      14  6.61e+02  2.28e+02  2.17e+03
      15  6.58e+02  2.27e+02  2.16e+03
      16  6.56e+02  2.25e+02  2.15e+03
      17  6.54e+02  2.24e+02  2.15e+03
      18  6.52e+02  2.23e+02  2.15e+03
      19  6.50e+02  2.22e+02  2.14e+03
      20  6.49e+02  2.21e+02  2.14e+03
      21  6.47e+02  2.20e+02  2.14e+03
      22  6.46e+02  2.19e+02  2.13e+03
      23  6.45e+02  2.19e+02  2.13e+03
      24  6.44e+02  2.18e+02  2.13e+03
      25  6.42e+02  2.18e+02  2.12e+03
      26  6.41e+02  2.18e+02  2.12e+03
      27  6.40e+02  2.17e+02  2.12e+03
      28  6.39e+02  2.17e+02  2.11e+03
      29  6.39e+02  2.17e+02  2.11e+03
      30  6.38e+02  2.16e+02  2.11e+03
      31  6.37e+02  2.16e+02  2.10e+03
      32  6.36e+02  2.16e+02  2.10e+03
      33  6.35e+02  2.15e+02  2.10e+03
      34  6.35e+02  2.15e+02  2.10e+03
      35  6.34e+02  2.15e+02  2.10e+03
      36  6.33e+02  2.15e+02  2.09e+03
      37  6.33e+02  2.15e+02  2.09e+03
      38  6.32e+02  2.14e+02  2.09e+03
      39  6.32e+02  2.14e+02  2.09e+03
      40  6.31e+02  2.14e+02  2.09e+03
      41  6.31e+02  2.14e+02  2.08e+03
      42  6.30e+02  2.14e+02  2.08e+03
      43  6.30e+02  2.14e+02  2.08e+03
      44  6.29e+02  2.13e+02  2.08e+03
      45  6.29e+02  2.13e+02  2.08e+03
      46  6.28e+02  2.13e+02  2.08e+03
      47  6.28e+02  2.13e+02  2.07e+03
      48  6.27e+02  2.13e+02  2.07e+03
      49  6.27e+02  2.13e+02  2.07e+03
      50  6.27e+02  2.13e+02  2.07e+03
      51  6.26e+02  2.13e+02  2.07e+03
      52  6.26e+02  2.12e+02  2.07e+03
      53  6.26e+02  2.12e+02  2.07e+03
      54  6.25e+02  2.12e+02  2.07e+03
      55  6.25e+02  2.12e+02  2.06e+03
      56  6.25e+02  2.12e+02  2.06e+03
      57  6.24e+02  2.12e+02  2.06e+03
      58  6.24e+02  2.12e+02  2.06e+03
      59  6.24e+02  2.12e+02  2.06e+03
      60  6.23e+02  2.12e+02  2.06e+03
      61  6.23e+02  2.12e+02  2.06e+03
      62  6.23e+02  2.12e+02  2.06e+03
      63  6.22e+02  2.11e+02  2.06e+03
      64  6.22e+02  2.11e+02  2.05e+03
      65  6.22e+02  2.11e+02  2.05e+03
      66  6.22e+02  2.11e+02  2.05e+03
      67  6.21e+02  2.11e+02  2.05e+03
      68  6.21e+02  2.11e+02  2.05e+03
      69  6.21e+02  2.11e+02  2.05e+03
      70  6.21e+02  2.11e+02  2.05e+03
      71  6.21e+02  2.11e+02  2.05e+03
      72  6.20e+02  2.11e+02  2.05e+03
      73  6.20e+02  2.11e+02  2.05e+03
      74  6.20e+02  2.11e+02  2.05e+03
      75  6.20e+02  2.11e+02  2.05e+03
      76  6.20e+02  2.11e+02  2.04e+03
      77  6.19e+02  2.11e+02  2.04e+03
      78  6.19e+02  2.10e+02  2.04e+03
      79  6.19e+02  2.10e+02  2.04e+03
      80  6.19e+02  2.10e+02  2.04e+03
      81  6.19e+02  2.10e+02  2.04e+03
      82  6.18e+02  2.10e+02  2.04e+03
      83  6.18e+02  2.10e+02  2.04e+03
      84  6.18e+02  2.10e+02  2.04e+03
      85  6.18e+02  2.10e+02  2.04e+03
      86  6.18e+02  2.10e+02  2.04e+03
      87  6.18e+02  2.10e+02  2.04e+03
      88  6.17e+02  2.10e+02  2.04e+03
      89  6.17e+02  2.10e+02  2.04e+03
      90  6.17e+02  2.10e+02  2.04e+03
      91  6.17e+02  2.10e+02  2.04e+03
      92  6.17e+02  2.10e+02  2.04e+03
      93  6.17e+02  2.10e+02  2.03e+03
      94  6.17e+02  2.10e+02  2.03e+03
      95  6.16e+02  2.10e+02  2.03e+03
      96  6.16e+02  2.10e+02  2.03e+03
      97  6.16e+02  2.10e+02  2.03e+03
      98  6.16e+02  2.10e+02  2.03e+03
      99  6.16e+02  2.10e+02  2.03e+03
     100  6.16e+02  2.10e+02  2.03e+03
     101  6.16e+02  2.10e+02  2.03e+03
     102  6.16e+02  2.10e+02  2.03e+03
     103  6.15e+02  2.09e+02  2.03e+03
     104  6.15e+02  2.09e+02  2.03e+03
     105  6.15e+02  2.09e+02  2.03e+03
     106  6.15e+02  2.09e+02  2.03e+03
     107  6.15e+02  2.09e+02  2.03e+03
     108  6.15e+02  2.09e+02  2.03e+03
     109  6.15e+02  2.09e+02  2.03e+03
     110  6.15e+02  2.09e+02  2.03e+03
     111  6.14e+02  2.09e+02  2.03e+03
     112  6.14e+02  2.09e+02  2.03e+03
     113  6.14e+02  2.09e+02  2.02e+03
     114  6.14e+02  2.09e+02  2.02e+03
     115  6.14e+02  2.09e+02  2.02e+03
     116  6.14e+02  2.09e+02  2.02e+03
     117  6.14e+02  2.09e+02  2.02e+03
     118  6.14e+02  2.09e+02  2.02e+03
     119  6.14e+02  2.09e+02  2.02e+03
     120  6.13e+02  2.09e+02  2.02e+03
     121  6.13e+02  2.09e+02  2.02e+03
     122  6.13e+02  2.09e+02  2.02e+03
     123  6.13e+02  2.09e+02  2.02e+03
     124  6.13e+02  2.09e+02  2.02e+03
     125  6.13e+02  2.09e+02  2.02e+03
     126  6.13e+02  2.09e+02  2.02e+03
     127  6.13e+02  2.09e+02  2.02e+03
     128  6.13e+02  2.09e+02  2.02e+03
     129  6.13e+02  2.09e+02  2.02e+03
     130  6.13e+02  2.09e+02  2.02e+03
     131  6.12e+02  2.09e+02  2.02e+03
     132  6.12e+02  2.09e+02  2.02e+03
     133  6.12e+02  2.09e+02  2.02e+03
     134  6.12e+02  2.09e+02  2.02e+03
     135  6.12e+02  2.09e+02  2.02e+03
     136  6.12e+02  2.09e+02  2.02e+03
     137  6.12e+02  2.09e+02  2.02e+03
     138  6.12e+02  2.09e+02  2.02e+03
     139  6.12e+02  2.09e+02  2.02e+03
     140  6.12e+02  2.08e+02  2.02e+03
     141  6.12e+02  2.08e+02  2.02e+03
     142  6.11e+02  2.08e+02  2.02e+03
     143  6.11e+02  2.08e+02  2.01e+03
     144  6.11e+02  2.08e+02  2.01e+03
     145  6.11e+02  2.08e+02  2.01e+03
     146  6.11e+02  2.08e+02  2.01e+03
     147  6.11e+02  2.08e+02  2.01e+03
     148  6.11e+02  2.08e+02  2.01e+03
     149  6.11e+02  2.08e+02  2.01e+03
     150  6.11e+02  2.08e+02  2.01e+03
     151  6.11e+02  2.08e+02  2.01e+03
     152  6.11e+02  2.08e+02  2.01e+03
     153  6.11e+02  2.08e+02  2.01e+03
     154  6.11e+02  2.08e+02  2.01e+03
     155  6.11e+02  2.08e+02  2.01e+03
     156  6.10e+02  2.08e+02  2.01e+03
     157  6.10e+02  2.08e+02  2.01e+03
     158  6.10e+02  2.08e+02  2.01e+03
     159  6.10e+02  2.08e+02  2.01e+03
     160  6.10e+02  2.08e+02  2.01e+03
     161  6.10e+02  2.08e+02  2.01e+03
     162  6.10e+02  2.08e+02  2.01e+03
     163  6.10e+02  2.08e+02  2.01e+03
     164  6.10e+02  2.08e+02  2.01e+03
     165  6.10e+02  2.08e+02  2.01e+03
     166  6.10e+02  2.08e+02  2.01e+03
     167  6.10e+02  2.08e+02  2.01e+03
     168  6.10e+02  2.08e+02  2.01e+03
     169  6.10e+02  2.08e+02  2.01e+03
     170  6.10e+02  2.08e+02  2.01e+03
     171  6.09e+02  2.08e+02  2.01e+03
     172  6.09e+02  2.08e+02  2.01e+03
     173  6.09e+02  2.08e+02  2.01e+03
     174  6.09e+02  2.08e+02  2.01e+03
     175  6.09e+02  2.08e+02  2.01e+03
     176  6.09e+02  2.08e+02  2.01e+03
     177  6.09e+02  2.08e+02  2.01e+03
     178  6.09e+02  2.08e+02  2.01e+03
     179  6.09e+02  2.08e+02  2.01e+03
     180  6.09e+02  2.08e+02  2.01e+03
     181  6.09e+02  2.08e+02  2.01e+03
     182  6.09e+02  2.08e+02  2.01e+03
     183  6.09e+02  2.08e+02  2.01e+03
     184  6.09e+02  2.08e+02  2.01e+03
     185  6.09e+02  2.08e+02  2.01e+03
     186  6.09e+02  2.08e+02  2.01e+03
     187  6.09e+02  2.08e+02  2.01e+03
     188  6.09e+02  2.08e+02  2.01e+03
     189  6.08e+02  2.08e+02  2.00e+03
     190  6.08e+02  2.07e+02  2.00e+03
     191  6.08e+02  2.07e+02  2.00e+03
     192  6.08e+02  2.07e+02  2.00e+03
     193  6.08e+02  2.07e+02  2.00e+03
     194  6.08e+02  2.07e+02  2.00e+03
     195  6.08e+02  2.07e+02  2.00e+03
     196  6.08e+02  2.07e+02  2.00e+03
     197  6.08e+02  2.07e+02  2.00e+03
     198  6.08e+02  2.07e+02  2.00e+03
     199  6.08e+02  2.07e+02  2.00e+03
    ----------------------------------
    ConvBPDNDictLearn_Consensus solve time: 75.80s


Display initial and final dictionaries.

.. code:: ipython3

    D1 = D1.squeeze()
    fig = plot.figure(figsize=(14, 7))
    plot.subplot(1, 2, 1)
    plot.imview(util.tiledict(D0), title='D0', fig=fig)
    plot.subplot(1, 2, 2)
    plot.imview(util.tiledict(D1), title='D1', fig=fig)
    fig.show()



.. image:: cbpdndl_parcns_clr_files/cbpdndl_parcns_clr_13_0.png


Get iterations statistics from solver object and plot functional value

.. code:: ipython3

    its = d.getitstat()
    plot.plot(its.ObjFun, xlbl='Iterations', ylbl='Functional')



.. image:: cbpdndl_parcns_clr_files/cbpdndl_parcns_clr_15_0.png

