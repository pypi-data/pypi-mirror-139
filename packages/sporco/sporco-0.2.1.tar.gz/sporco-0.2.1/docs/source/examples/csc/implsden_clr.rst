.. _examples_csc_implsden_clr:

Impulse Noise Restoration via CSC
=================================

This example demonstrates the removal of salt & pepper noise from a
colour image using convolutional sparse coding with a colour dictionary
:cite:`wohlberg-2017-sporco`,

.. math:: \mathrm{argmin}_\mathbf{x} \; (1/2) \sum_c \left\| \sum_m \mathbf{d}_{c,m} * \mathbf{x}_m -\mathbf{s}_c \right\|_2^2 + \lambda \sum_m \| \mathbf{x}_m \|_1 + (\mu/2) \sum_i \sum_m \| G_i \mathbf{x}_m \|_2^2

where :math:`\mathbf{d}_{c,m}` is channel :math:`c` of the
:math:`m^{\text{th}}` dictionary filter, :math:`\mathbf{x}_m` is the
coefficient map corresponding to the :math:`m^{\text{th}}` dictionary
filter, :math:`\mathbf{s}_c` is channel :math:`c` of the input image,
and :math:`G_i` is an operator computing the derivative along spatial
index :math:`i`.

.. code:: ipython3

    from __future__ import print_function
    from builtins import input

    import pyfftw   # See https://github.com/pyFFTW/pyFFTW/issues/40
    import numpy as np

    from sporco import util
    from sporco import signal
    from sporco import plot
    plot.config_notebook_plotting()
    import sporco.metric as sm
    import sporco.prox as sp
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

Load a reference image and corrupt it with 33% salt and pepper noise.
(The call to ``np.random.seed`` ensures that the pseudo-random noise is
reproducible.)

.. code:: ipython3

    img = util.ExampleImages().image('monarch.png', zoom=0.5, scaled=True,
                                     idxexp=np.s_[:, 160:672])
    np.random.seed(12345)
    imgn = signal.spnoise(img, 0.33)

We use a colour dictionary. The impulse denoising problem is solved by
appending some additional filters to the learned dictionary ``D0``,
which is one of those distributed with SPORCO. The first of these
additional components is a set of three impulse filters, one per colour
channel, that will represent the impulse noise, and the second is an
identical set of impulse filters that will represent the low frequency
image components when used together with a gradient penalty on the
coefficient maps, as discussed below.

.. code:: ipython3

    D0 = util.convdicts()['RGB:8x8x3x64']
    Di = np.zeros(D0.shape[0:2] + (3, 3))
    np.fill_diagonal(Di[0, 0], 1.0)
    D = np.concatenate((Di, Di, D0), axis=3)

The problem is solved using class
:class:`.admm.cbpdn.ConvBPDNGradReg`, which implements the form of
CBPDN with an additional gradient regularization term, as defined above.
The regularization parameters for the :math:`\ell_1` and gradient terms
are ``lmbda`` and ``mu`` respectively. Setting correct weighting arrays
for these regularization terms is critical to obtaining good
performance. For the :math:`\ell_1` norm, the weights on the filters
that are intended to represent the impulse noise are tuned to an
appropriate value for the impulse noise density (this value sets the
relative cost of representing an image feature by one of the impulses or
by one of the filters in the learned dictionary), the weights on the
filters that are intended to represent low frequency components are set
to zero (we only want them penalised by the gradient term), and the
weights of the remaining filters are set to zero. For the gradient
penalty, all weights are set to zero except for those corresponding to
the filters intended to represent low frequency components, which are
set to unity.

.. code:: ipython3

    lmbda = 2.8e-2
    mu = 3e-1
    w1 = np.ones((1, 1, 1, 1, D.shape[-1]))
    w1[..., 0:3] = 0.33
    w1[..., 3:6] = 0.0
    wg = np.zeros((D.shape[-1]))
    wg[..., 3:6] = 1.0
    opt = cbpdn.ConvBPDNGradReg.Options({'Verbose': True, 'MaxMainIter': 100,
                        'RelStopTol': 5e-3, 'AuxVarObj': False,
                        'L1Weight': w1, 'GradWeight': wg})

Initialise the :class:`.admm.cbpdn.ConvBPDNGradReg` object and call
the ``solve`` method.

.. code:: ipython3

    b = cbpdn.ConvBPDNGradReg(D, pad(imgn), lmbda, mu, opt, dimK=0)
    X = b.solve()


.. parsed-literal::

    Itn   Fnc       DFid      Regℓ1     Regℓ2∇    r         s         ρ
    --------------------------------------------------------------------------
       0  8.93e+03  7.67e+03  3.96e+04  5.00e+02  4.38e-01  6.91e+00  2.40e+00
       1  2.08e+03  4.99e+02  4.46e+04  1.12e+03  9.88e-02  1.85e+00  2.40e+00
       2  2.28e+03  8.35e+01  7.50e+04  3.06e+02  2.03e-01  7.75e-01  5.07e-01
       3  3.19e+03  2.08e+01  1.13e+05  7.34e+01  2.84e-01  3.93e-01  2.37e-01
       4  3.08e+03  9.88e+00  1.09e+05  4.02e+01  2.71e-01  2.80e-01  1.84e-01
       5  2.75e+03  8.30e+00  9.76e+04  3.57e+01  2.36e-01  2.30e-01  1.65e-01
       6  2.25e+03  7.59e+00  7.97e+04  3.64e+01  1.88e-01  1.96e-01  1.65e-01
       7  2.02e+03  7.30e+00  7.17e+04  3.65e+01  1.67e-01  1.70e-01  1.47e-01
       8  1.82e+03  6.79e+00  6.44e+04  3.65e+01  1.46e-01  1.45e-01  1.33e-01
       9  1.55e+03  6.39e+00  5.48e+04  3.62e+01  1.17e-01  1.25e-01  1.33e-01
      10  1.44e+03  6.06e+00  5.08e+04  3.60e+01  1.06e-01  1.09e-01  1.18e-01
      11  1.32e+03  5.80e+00  4.65e+04  3.57e+01  9.43e-02  9.65e-02  1.06e-01
      12  1.21e+03  5.56e+00  4.27e+04  3.56e+01  8.43e-02  8.54e-02  9.58e-02
      13  1.13e+03  5.34e+00  3.98e+04  3.56e+01  7.56e-02  7.32e-02  8.69e-02
      14  1.00e+03  5.16e+00  3.52e+04  3.58e+01  6.32e-02  6.23e-02  8.69e-02
      15  9.03e+02  5.06e+00  3.17e+04  3.59e+01  5.33e-02  5.49e-02  8.69e-02
      16  8.48e+02  5.00e+00  2.97e+04  3.62e+01  4.91e-02  4.93e-02  7.81e-02
      17  8.02e+02  4.94e+00  2.81e+04  3.63e+01  4.53e-02  4.36e-02  7.12e-02
      18  7.39e+02  4.88e+00  2.58e+04  3.65e+01  3.95e-02  3.86e-02  7.12e-02
      19  6.94e+02  4.84e+00  2.42e+04  3.66e+01  3.49e-02  3.48e-02  7.12e-02
      20  6.58e+02  4.81e+00  2.29e+04  3.66e+01  3.13e-02  3.15e-02  7.12e-02
      21  6.39e+02  4.77e+00  2.23e+04  3.66e+01  2.98e-02  2.86e-02  6.47e-02
      22  6.14e+02  4.73e+00  2.14e+04  3.65e+01  2.73e-02  2.60e-02  6.47e-02
      23  5.87e+02  4.71e+00  2.04e+04  3.64e+01  2.51e-02  2.48e-02  6.47e-02
      24  5.63e+02  4.69e+00  1.95e+04  3.64e+01  2.32e-02  2.43e-02  6.47e-02
      25  5.46e+02  4.69e+00  1.89e+04  3.63e+01  2.28e-02  2.36e-02  5.77e-02
      26  5.40e+02  4.68e+00  1.87e+04  3.62e+01  2.28e-02  2.19e-02  5.17e-02
      27  5.39e+02  4.66e+00  1.87e+04  3.62e+01  2.18e-02  1.96e-02  5.17e-02
      28  5.39e+02  4.65e+00  1.87e+04  3.62e+01  2.10e-02  1.78e-02  5.17e-02
      29  5.36e+02  4.65e+00  1.86e+04  3.61e+01  2.01e-02  1.64e-02  5.17e-02
      30  5.28e+02  4.65e+00  1.83e+04  3.61e+01  1.93e-02  1.57e-02  5.17e-02
      31  5.18e+02  4.65e+00  1.79e+04  3.61e+01  1.84e-02  1.53e-02  5.17e-02
      32  5.08e+02  4.66e+00  1.76e+04  3.61e+01  1.77e-02  1.50e-02  5.17e-02
      33  5.02e+02  4.67e+00  1.74e+04  3.61e+01  1.70e-02  1.45e-02  5.17e-02
      34  4.98e+02  4.67e+00  1.72e+04  3.61e+01  1.63e-02  1.39e-02  5.17e-02
      35  4.95e+02  4.67e+00  1.71e+04  3.61e+01  1.58e-02  1.34e-02  5.17e-02
      36  4.91e+02  4.68e+00  1.70e+04  3.62e+01  1.52e-02  1.31e-02  5.17e-02
      37  4.85e+02  4.68e+00  1.68e+04  3.62e+01  1.47e-02  1.29e-02  5.17e-02
      38  4.81e+02  4.69e+00  1.66e+04  3.63e+01  1.42e-02  1.27e-02  5.17e-02
      39  4.77e+02  4.69e+00  1.65e+04  3.63e+01  1.37e-02  1.24e-02  5.17e-02
      40  4.75e+02  4.70e+00  1.64e+04  3.64e+01  1.33e-02  1.19e-02  5.17e-02
      41  4.74e+02  4.70e+00  1.64e+04  3.64e+01  1.30e-02  1.14e-02  5.17e-02
      42  4.73e+02  4.70e+00  1.63e+04  3.64e+01  1.27e-02  1.08e-02  5.17e-02
      43  4.72e+02  4.71e+00  1.63e+04  3.64e+01  1.24e-02  1.03e-02  5.17e-02
      44  4.70e+02  4.71e+00  1.62e+04  3.64e+01  1.21e-02  9.87e-03  5.17e-02
      45  4.68e+02  4.72e+00  1.61e+04  3.65e+01  1.18e-02  9.59e-03  5.17e-02
      46  4.65e+02  4.72e+00  1.61e+04  3.65e+01  1.15e-02  9.41e-03  5.17e-02
      47  4.62e+02  4.73e+00  1.60e+04  3.65e+01  1.12e-02  9.33e-03  5.17e-02
      48  4.59e+02  4.73e+00  1.58e+04  3.66e+01  1.09e-02  9.31e-03  5.17e-02
      49  4.56e+02  4.73e+00  1.57e+04  3.67e+01  1.07e-02  9.29e-03  5.17e-02
      50  4.53e+02  4.74e+00  1.56e+04  3.67e+01  1.04e-02  9.22e-03  5.17e-02
      51  4.50e+02  4.74e+00  1.55e+04  3.68e+01  1.02e-02  9.10e-03  5.17e-02
      52  4.49e+02  4.75e+00  1.55e+04  3.69e+01  9.97e-03  8.87e-03  5.17e-02
      53  4.48e+02  4.75e+00  1.54e+04  3.69e+01  9.80e-03  8.56e-03  5.17e-02
      54  4.48e+02  4.76e+00  1.54e+04  3.69e+01  9.66e-03  8.19e-03  5.17e-02
      55  4.48e+02  4.76e+00  1.54e+04  3.69e+01  9.52e-03  7.83e-03  5.17e-02
      56  4.48e+02  4.76e+00  1.54e+04  3.70e+01  9.37e-03  7.53e-03  5.17e-02
      57  4.47e+02  4.77e+00  1.54e+04  3.70e+01  9.21e-03  7.31e-03  5.17e-02
      58  4.46e+02  4.77e+00  1.54e+04  3.69e+01  9.03e-03  7.19e-03  5.17e-02
      59  4.44e+02  4.78e+00  1.53e+04  3.69e+01  8.85e-03  7.15e-03  5.17e-02
      60  4.42e+02  4.78e+00  1.52e+04  3.70e+01  8.66e-03  7.16e-03  5.17e-02
      61  4.40e+02  4.78e+00  1.52e+04  3.70e+01  8.48e-03  7.15e-03  5.17e-02
      62  4.38e+02  4.79e+00  1.51e+04  3.70e+01  8.32e-03  7.12e-03  5.17e-02
      63  4.37e+02  4.79e+00  1.50e+04  3.70e+01  8.16e-03  7.06e-03  5.17e-02
      64  4.36e+02  4.80e+00  1.50e+04  3.71e+01  8.02e-03  6.95e-03  5.17e-02
      65  4.35e+02  4.80e+00  1.50e+04  3.71e+01  7.90e-03  6.79e-03  5.17e-02
      66  4.35e+02  4.80e+00  1.50e+04  3.72e+01  7.79e-03  6.60e-03  5.17e-02
      67  4.35e+02  4.81e+00  1.50e+04  3.72e+01  7.68e-03  6.40e-03  5.17e-02
      68  4.34e+02  4.81e+00  1.49e+04  3.73e+01  7.58e-03  6.19e-03  5.17e-02
      69  4.34e+02  4.81e+00  1.49e+04  3.73e+01  7.47e-03  6.03e-03  5.17e-02
      70  4.33e+02  4.82e+00  1.49e+04  3.73e+01  7.36e-03  5.91e-03  5.17e-02
      71  4.32e+02  4.82e+00  1.49e+04  3.74e+01  7.25e-03  5.85e-03  5.17e-02
      72  4.31e+02  4.82e+00  1.48e+04  3.74e+01  7.13e-03  5.81e-03  5.17e-02
      73  4.30e+02  4.83e+00  1.48e+04  3.74e+01  7.01e-03  5.79e-03  5.17e-02
      74  4.28e+02  4.83e+00  1.47e+04  3.74e+01  6.89e-03  5.76e-03  5.17e-02
      75  4.27e+02  4.83e+00  1.47e+04  3.74e+01  6.79e-03  5.71e-03  5.17e-02
      76  4.27e+02  4.84e+00  1.47e+04  3.74e+01  6.69e-03  5.63e-03  5.17e-02
      77  4.26e+02  4.84e+00  1.46e+04  3.75e+01  6.60e-03  5.53e-03  5.17e-02
      78  4.26e+02  4.84e+00  1.46e+04  3.75e+01  6.52e-03  5.41e-03  5.17e-02
      79  4.25e+02  4.85e+00  1.46e+04  3.75e+01  6.44e-03  5.29e-03  5.17e-02
      80  4.25e+02  4.85e+00  1.46e+04  3.75e+01  6.36e-03  5.17e-03  5.17e-02
      81  4.24e+02  4.85e+00  1.46e+04  3.75e+01  6.28e-03  5.07e-03  5.17e-02
      82  4.24e+02  4.86e+00  1.46e+04  3.75e+01  6.19e-03  4.99e-03  5.17e-02
      83  4.23e+02  4.86e+00  1.45e+04  3.76e+01  6.11e-03  4.94e-03  5.17e-02
      84  4.22e+02  4.86e+00  1.45e+04  3.76e+01  6.02e-03  4.90e-03  5.17e-02
      85  4.21e+02  4.87e+00  1.45e+04  3.76e+01  5.94e-03  4.87e-03  5.17e-02
      86  4.21e+02  4.87e+00  1.44e+04  3.76e+01  5.85e-03  4.83e-03  5.17e-02
      87  4.20e+02  4.87e+00  1.44e+04  3.77e+01  5.78e-03  4.78e-03  5.17e-02
      88  4.20e+02  4.87e+00  1.44e+04  3.77e+01  5.70e-03  4.71e-03  5.17e-02
      89  4.19e+02  4.88e+00  1.44e+04  3.77e+01  5.64e-03  4.63e-03  5.17e-02
      90  4.19e+02  4.88e+00  1.44e+04  3.77e+01  5.57e-03  4.53e-03  5.17e-02
      91  4.19e+02  4.88e+00  1.44e+04  3.78e+01  5.51e-03  4.45e-03  5.17e-02
      92  4.18e+02  4.89e+00  1.44e+04  3.78e+01  5.44e-03  4.36e-03  5.17e-02
      93  4.18e+02  4.89e+00  1.43e+04  3.78e+01  5.37e-03  4.30e-03  5.17e-02
      94  4.17e+02  4.89e+00  1.43e+04  3.78e+01  5.31e-03  4.25e-03  5.17e-02
      95  4.17e+02  4.89e+00  1.43e+04  3.79e+01  5.24e-03  4.22e-03  5.17e-02
      96  4.16e+02  4.90e+00  1.43e+04  3.79e+01  5.17e-03  4.19e-03  5.17e-02
      97  4.15e+02  4.90e+00  1.43e+04  3.79e+01  5.10e-03  4.17e-03  5.17e-02
      98  4.15e+02  4.90e+00  1.42e+04  3.79e+01  5.04e-03  4.14e-03  5.17e-02
      99  4.14e+02  4.91e+00  1.42e+04  3.79e+01  4.98e-03  4.10e-03  5.17e-02
    --------------------------------------------------------------------------


The denoised estimate of the image is just the reconstruction from all
coefficient maps except those that represent the impulse noise, which is
why we subtract the slice of ``X`` corresponding the impulse noise
representing filters from the result of ``reconstruct``.

.. code:: ipython3

    imgdp = b.reconstruct().squeeze() - X[..., 0, 0:3].squeeze()
    imgd = crop(imgdp)

Keep a copy of the low-frequency component estimate from this solution
for use in the next approach.

.. code:: ipython3

    imglp = X[..., 0, 3:6].squeeze()

Display solve time and denoising performance.

.. code:: ipython3

    print("ConvBPDNGradReg solve time: %5.2f s" % b.timer.elapsed('solve'))
    print("Noisy image PSNR:    %5.2f dB" % sm.psnr(img, imgn))
    print("Denoised image PSNR: %5.2f dB" % sm.psnr(img, imgd))


.. parsed-literal::

    ConvBPDNGradReg solve time: 62.89 s
    Noisy image PSNR:    10.37 dB
    Denoised image PSNR: 26.41 dB


Display the reference, noisy, and denoised images.

.. code:: ipython3

    fig, ax = plot.subplots(nrows=1, ncols=3, figsize=(21, 7))
    fig.suptitle('Method 1 Results')
    plot.imview(img, ax=ax[0], title='Reference', fig=fig)
    plot.imview(imgn, ax=ax[1], title='Noisy', fig=fig)
    plot.imview(imgd, ax=ax[2], title='CSC Result', fig=fig)
    fig.show()



.. image:: implsden_clr_files/implsden_clr_19_0.png


The previous method gave good results, but the weight on the filter
representing the impulse noise is an additional parameter that has to be
tuned. This parameter can be avoided by switching to an :math:`\ell_1`
data fidelity term instead of including dictionary filters to represent
the impulse noise, as in the problem
:cite:`wohlberg-2016-convolutional2`

.. math::

   \mathrm{argmin}_{\{\mathbf{x}_m\}} \;
     \left \|  \sum_m \mathbf{d}_m * \mathbf{x}_m - \mathbf{s}
     \right \|_1 + \lambda \sum_m \| \mathbf{x}_m \|_1 \;.

Ideally we would also include a gradient penalty term to assist in the
representation of the low frequency image component. While this
relatively straightforward, it is a bit more complex to implement, and
is omitted from this example. Instead of including a representation of
the low frequency image component within the optimization, we use the
low frequency component estimated by the previous example, subtracting
it from the signal passed to the CSC algorithm, and adding it back to
the solution of this algorithm.

An algorithm for the problem above is not included in SPORCO, but
:class:`.cbpdn.ConvBPDNMaskDcpl` is easily adapted by deriving a new
class that overrides two of its methods :cite:`wohlberg-2017-sporco`.

.. code:: ipython3

    class ConvRepL1L1(cbpdn.ConvBPDNMaskDcpl):

        def ystep(self):

            AXU = self.AX + self.U
            Y0 = sp.prox_l1(self.block_sep0(AXU) - self.S, (1.0/self.rho)*self.W)
            Y1 = sp.prox_l1(self.block_sep1(AXU), (self.lmbda/self.rho)*self.wl1)
            self.Y = self.block_cat(Y0, Y1)

            super(cbpdn.ConvBPDNMaskDcpl, self).ystep()


        def obfn_g0(self, Y0):

            return np.sum(np.abs(self.W * self.obfn_g0var()))

Set the options for our new class.

.. code:: ipython3

    opt = ConvRepL1L1.Options({'Verbose': True, 'MaxMainIter': 200,
                        'RelStopTol': 5e-3, 'AuxVarObj': False,
                        'rho': 1e1, 'RelaxParam': 1.8})

Initialise the ``ConvRepL1L1`` object and call the ``solve`` method.

.. code:: ipython3

    lmbda = 3.0e0
    b = ConvRepL1L1(D0, pad(imgn) - imglp, lmbda, opt=opt, dimK=0)
    X = b.solve()


.. parsed-literal::

    Itn   Fnc       DFid      Regℓ1     r         s
    ------------------------------------------------------
       0  1.97e+05  2.98e+04  5.56e+04  3.76e-01  2.22e+00
       1  1.93e+05  3.99e+04  5.10e+04  3.13e-01  2.14e+00
       2  1.50e+05  3.78e+04  3.74e+04  2.40e-01  1.84e+00
       3  1.22e+05  3.64e+04  2.87e+04  1.89e-01  1.51e+00
       4  1.05e+05  3.69e+04  2.27e+04  1.53e-01  1.24e+00
       5  9.39e+04  3.68e+04  1.91e+04  1.27e-01  1.05e+00
       6  8.58e+04  3.67e+04  1.63e+04  1.09e-01  9.10e-01
       7  7.95e+04  3.69e+04  1.42e+04  9.47e-02  7.96e-01
       8  7.49e+04  3.71e+04  1.26e+04  8.37e-02  7.01e-01
       9  7.12e+04  3.72e+04  1.13e+04  7.50e-02  6.23e-01
      10  6.82e+04  3.73e+04  1.03e+04  6.78e-02  5.55e-01
      11  6.57e+04  3.73e+04  9.47e+03  6.19e-02  4.99e-01
      12  6.38e+04  3.73e+04  8.82e+03  5.70e-02  4.53e-01
      13  6.20e+04  3.73e+04  8.24e+03  5.29e-02  4.15e-01
      14  6.06e+04  3.73e+04  7.78e+03  4.93e-02  3.79e-01
      15  5.94e+04  3.72e+04  7.39e+03  4.63e-02  3.50e-01
      16  5.84e+04  3.72e+04  7.06e+03  4.37e-02  3.24e-01
      17  5.74e+04  3.72e+04  6.74e+03  4.13e-02  3.03e-01
      18  5.66e+04  3.72e+04  6.48e+03  3.92e-02  2.86e-01
      19  5.59e+04  3.72e+04  6.26e+03  3.74e-02  2.70e-01
      20  5.53e+04  3.71e+04  6.05e+03  3.57e-02  2.58e-01
      21  5.47e+04  3.71e+04  5.86e+03  3.41e-02  2.49e-01
      22  5.41e+04  3.71e+04  5.67e+03  3.27e-02  2.39e-01
      23  5.35e+04  3.70e+04  5.50e+03  3.14e-02  2.28e-01
      24  5.31e+04  3.70e+04  5.38e+03  3.03e-02  2.18e-01
      25  5.28e+04  3.69e+04  5.28e+03  2.92e-02  2.08e-01
      26  5.24e+04  3.69e+04  5.18e+03  2.83e-02  1.99e-01
      27  5.21e+04  3.69e+04  5.07e+03  2.73e-02  1.91e-01
      28  5.17e+04  3.68e+04  4.96e+03  2.65e-02  1.84e-01
      29  5.13e+04  3.68e+04  4.85e+03  2.57e-02  1.78e-01
      30  5.10e+04  3.68e+04  4.76e+03  2.49e-02  1.73e-01
      31  5.08e+04  3.68e+04  4.67e+03  2.42e-02  1.68e-01
      32  5.05e+04  3.68e+04  4.58e+03  2.35e-02  1.63e-01
      33  5.02e+04  3.68e+04  4.48e+03  2.29e-02  1.59e-01
      34  4.99e+04  3.68e+04  4.40e+03  2.22e-02  1.55e-01
      35  4.97e+04  3.68e+04  4.32e+03  2.17e-02  1.50e-01
      36  4.96e+04  3.68e+04  4.26e+03  2.11e-02  1.45e-01
      37  4.94e+04  3.68e+04  4.21e+03  2.06e-02  1.40e-01
      38  4.93e+04  3.68e+04  4.16e+03  2.02e-02  1.36e-01
      39  4.91e+04  3.68e+04  4.10e+03  1.97e-02  1.31e-01
      40  4.90e+04  3.68e+04  4.05e+03  1.93e-02  1.27e-01
      41  4.88e+04  3.68e+04  4.01e+03  1.88e-02  1.24e-01
      42  4.87e+04  3.68e+04  3.95e+03  1.84e-02  1.22e-01
      43  4.85e+04  3.68e+04  3.89e+03  1.80e-02  1.20e-01
      44  4.82e+04  3.68e+04  3.82e+03  1.76e-02  1.18e-01
      45  4.81e+04  3.68e+04  3.76e+03  1.72e-02  1.17e-01
      46  4.79e+04  3.68e+04  3.71e+03  1.69e-02  1.15e-01
      47  4.77e+04  3.67e+04  3.67e+03  1.65e-02  1.12e-01
      48  4.76e+04  3.67e+04  3.62e+03  1.62e-02  1.09e-01
      49  4.75e+04  3.67e+04  3.59e+03  1.59e-02  1.07e-01
      50  4.74e+04  3.67e+04  3.56e+03  1.56e-02  1.04e-01
      51  4.72e+04  3.67e+04  3.52e+03  1.53e-02  1.01e-01
      52  4.71e+04  3.67e+04  3.48e+03  1.50e-02  9.85e-02
      53  4.70e+04  3.66e+04  3.45e+03  1.48e-02  9.63e-02
      54  4.69e+04  3.66e+04  3.42e+03  1.45e-02  9.42e-02
      55  4.68e+04  3.66e+04  3.39e+03  1.43e-02  9.24e-02
      56  4.67e+04  3.66e+04  3.36e+03  1.40e-02  9.09e-02
      57  4.66e+04  3.67e+04  3.32e+03  1.38e-02  8.98e-02
      58  4.65e+04  3.67e+04  3.28e+03  1.35e-02  8.86e-02
      59  4.64e+04  3.67e+04  3.24e+03  1.33e-02  8.73e-02
      60  4.63e+04  3.67e+04  3.21e+03  1.31e-02  8.58e-02
      61  4.62e+04  3.67e+04  3.17e+03  1.28e-02  8.42e-02
      62  4.61e+04  3.67e+04  3.14e+03  1.26e-02  8.24e-02
      63  4.61e+04  3.67e+04  3.12e+03  1.24e-02  8.07e-02
      64  4.60e+04  3.67e+04  3.09e+03  1.22e-02  7.90e-02
      65  4.59e+04  3.67e+04  3.07e+03  1.21e-02  7.75e-02
      66  4.59e+04  3.67e+04  3.05e+03  1.19e-02  7.60e-02
      67  4.58e+04  3.67e+04  3.03e+03  1.17e-02  7.46e-02
      68  4.57e+04  3.67e+04  3.00e+03  1.15e-02  7.35e-02
      69  4.56e+04  3.67e+04  2.98e+03  1.14e-02  7.24e-02
      70  4.55e+04  3.67e+04  2.95e+03  1.12e-02  7.13e-02
      71  4.54e+04  3.67e+04  2.92e+03  1.10e-02  7.01e-02
      72  4.54e+04  3.67e+04  2.90e+03  1.09e-02  6.92e-02
      73  4.53e+04  3.66e+04  2.87e+03  1.07e-02  6.83e-02
      74  4.52e+04  3.66e+04  2.85e+03  1.06e-02  6.75e-02
      75  4.51e+04  3.66e+04  2.83e+03  1.04e-02  6.65e-02
      76  4.51e+04  3.66e+04  2.81e+03  1.03e-02  6.52e-02
      77  4.50e+04  3.66e+04  2.80e+03  1.01e-02  6.40e-02
      78  4.50e+04  3.66e+04  2.78e+03  1.00e-02  6.30e-02
      79  4.49e+04  3.66e+04  2.77e+03  9.87e-03  6.20e-02
      80  4.49e+04  3.66e+04  2.75e+03  9.75e-03  6.11e-02
      81  4.48e+04  3.66e+04  2.74e+03  9.62e-03  6.01e-02
      82  4.48e+04  3.66e+04  2.72e+03  9.50e-03  5.93e-02
      83  4.47e+04  3.66e+04  2.70e+03  9.37e-03  5.84e-02
      84  4.47e+04  3.66e+04  2.68e+03  9.25e-03  5.75e-02
      85  4.46e+04  3.66e+04  2.66e+03  9.13e-03  5.67e-02
      86  4.46e+04  3.66e+04  2.64e+03  9.02e-03  5.59e-02
      87  4.45e+04  3.66e+04  2.63e+03  8.90e-03  5.49e-02
      88  4.45e+04  3.66e+04  2.61e+03  8.80e-03  5.41e-02
      89  4.44e+04  3.67e+04  2.59e+03  8.68e-03  5.33e-02
      90  4.44e+04  3.67e+04  2.57e+03  8.58e-03  5.25e-02
      91  4.43e+04  3.67e+04  2.56e+03  8.47e-03  5.18e-02
      92  4.43e+04  3.67e+04  2.54e+03  8.37e-03  5.10e-02
      93  4.42e+04  3.67e+04  2.53e+03  8.27e-03  5.00e-02
      94  4.42e+04  3.66e+04  2.52e+03  8.18e-03  4.94e-02
      95  4.42e+04  3.66e+04  2.51e+03  8.08e-03  4.88e-02
      96  4.41e+04  3.66e+04  2.49e+03  7.99e-03  4.84e-02
      97  4.41e+04  3.66e+04  2.48e+03  7.89e-03  4.79e-02
      98  4.40e+04  3.66e+04  2.46e+03  7.80e-03  4.74e-02
      99  4.40e+04  3.66e+04  2.45e+03  7.71e-03  4.68e-02
     100  4.39e+04  3.66e+04  2.43e+03  7.62e-03  4.62e-02
     101  4.39e+04  3.66e+04  2.42e+03  7.53e-03  4.56e-02
     102  4.38e+04  3.66e+04  2.41e+03  7.45e-03  4.50e-02
     103  4.38e+04  3.66e+04  2.40e+03  7.37e-03  4.44e-02
     104  4.38e+04  3.66e+04  2.39e+03  7.29e-03  4.36e-02
     105  4.37e+04  3.66e+04  2.38e+03  7.21e-03  4.29e-02
     106  4.37e+04  3.66e+04  2.37e+03  7.14e-03  4.22e-02
     107  4.37e+04  3.66e+04  2.36e+03  7.06e-03  4.15e-02
     108  4.37e+04  3.66e+04  2.35e+03  6.98e-03  4.10e-02
     109  4.36e+04  3.66e+04  2.34e+03  6.91e-03  4.05e-02
     110  4.36e+04  3.66e+04  2.32e+03  6.83e-03  4.00e-02
     111  4.36e+04  3.66e+04  2.31e+03  6.76e-03  3.96e-02
     112  4.35e+04  3.66e+04  2.30e+03  6.68e-03  3.92e-02
     113  4.35e+04  3.66e+04  2.29e+03  6.61e-03  3.88e-02
     114  4.35e+04  3.66e+04  2.28e+03  6.54e-03  3.82e-02
     115  4.34e+04  3.66e+04  2.27e+03  6.47e-03  3.77e-02
     116  4.34e+04  3.66e+04  2.26e+03  6.41e-03  3.71e-02
     117  4.34e+04  3.66e+04  2.25e+03  6.34e-03  3.67e-02
     118  4.34e+04  3.66e+04  2.24e+03  6.28e-03  3.62e-02
     119  4.33e+04  3.66e+04  2.24e+03  6.21e-03  3.58e-02
     120  4.33e+04  3.66e+04  2.23e+03  6.15e-03  3.54e-02
     121  4.33e+04  3.66e+04  2.22e+03  6.08e-03  3.51e-02
     122  4.32e+04  3.66e+04  2.21e+03  6.02e-03  3.47e-02
     123  4.32e+04  3.66e+04  2.20e+03  5.96e-03  3.43e-02
     124  4.32e+04  3.66e+04  2.19e+03  5.90e-03  3.38e-02
     125  4.31e+04  3.66e+04  2.18e+03  5.83e-03  3.34e-02
     126  4.31e+04  3.66e+04  2.17e+03  5.78e-03  3.28e-02
     127  4.31e+04  3.66e+04  2.16e+03  5.72e-03  3.22e-02
     128  4.31e+04  3.66e+04  2.15e+03  5.67e-03  3.17e-02
     129  4.31e+04  3.66e+04  2.15e+03  5.61e-03  3.13e-02
     130  4.30e+04  3.66e+04  2.14e+03  5.56e-03  3.09e-02
     131  4.30e+04  3.66e+04  2.13e+03  5.50e-03  3.05e-02
     132  4.30e+04  3.66e+04  2.13e+03  5.45e-03  3.01e-02
     133  4.30e+04  3.66e+04  2.12e+03  5.40e-03  2.98e-02
     134  4.29e+04  3.66e+04  2.11e+03  5.34e-03  2.96e-02
     135  4.29e+04  3.66e+04  2.10e+03  5.29e-03  2.94e-02
     136  4.29e+04  3.66e+04  2.09e+03  5.24e-03  2.91e-02
     137  4.29e+04  3.66e+04  2.09e+03  5.19e-03  2.88e-02
     138  4.29e+04  3.66e+04  2.08e+03  5.14e-03  2.85e-02
     139  4.28e+04  3.66e+04  2.07e+03  5.09e-03  2.82e-02
     140  4.28e+04  3.66e+04  2.06e+03  5.04e-03  2.78e-02
     141  4.28e+04  3.66e+04  2.06e+03  5.00e-03  2.74e-02
     142  4.28e+04  3.66e+04  2.05e+03  4.95e-03  2.70e-02
     143  4.28e+04  3.66e+04  2.05e+03  4.90e-03  2.66e-02
     144  4.27e+04  3.66e+04  2.04e+03  4.86e-03  2.61e-02
     145  4.27e+04  3.66e+04  2.03e+03  4.81e-03  2.57e-02
     146  4.27e+04  3.66e+04  2.03e+03  4.77e-03  2.53e-02
     147  4.27e+04  3.66e+04  2.02e+03  4.72e-03  2.50e-02
     148  4.27e+04  3.66e+04  2.01e+03  4.68e-03  2.48e-02
     149  4.26e+04  3.66e+04  2.01e+03  4.64e-03  2.46e-02
     150  4.26e+04  3.66e+04  2.00e+03  4.59e-03  2.45e-02
     151  4.26e+04  3.66e+04  1.99e+03  4.55e-03  2.44e-02
     152  4.26e+04  3.66e+04  1.99e+03  4.51e-03  2.43e-02
     153  4.25e+04  3.66e+04  1.98e+03  4.47e-03  2.41e-02
     154  4.25e+04  3.66e+04  1.98e+03  4.43e-03  2.38e-02
     155  4.25e+04  3.66e+04  1.97e+03  4.39e-03  2.35e-02
     156  4.25e+04  3.66e+04  1.97e+03  4.35e-03  2.32e-02
     157  4.25e+04  3.66e+04  1.96e+03  4.31e-03  2.28e-02
     158  4.25e+04  3.66e+04  1.96e+03  4.27e-03  2.24e-02
     159  4.25e+04  3.66e+04  1.95e+03  4.24e-03  2.20e-02
     160  4.24e+04  3.66e+04  1.94e+03  4.20e-03  2.17e-02
     161  4.24e+04  3.66e+04  1.94e+03  4.16e-03  2.14e-02
     162  4.24e+04  3.66e+04  1.93e+03  4.13e-03  2.12e-02
     163  4.24e+04  3.66e+04  1.93e+03  4.09e-03  2.09e-02
     164  4.24e+04  3.66e+04  1.92e+03  4.06e-03  2.07e-02
     165  4.24e+04  3.66e+04  1.92e+03  4.02e-03  2.05e-02
     166  4.23e+04  3.66e+04  1.91e+03  3.99e-03  2.03e-02
     167  4.23e+04  3.66e+04  1.91e+03  3.95e-03  2.01e-02
     168  4.23e+04  3.66e+04  1.90e+03  3.92e-03  2.00e-02
     169  4.23e+04  3.66e+04  1.90e+03  3.88e-03  1.99e-02
     170  4.23e+04  3.66e+04  1.89e+03  3.85e-03  1.98e-02
     171  4.23e+04  3.66e+04  1.89e+03  3.82e-03  1.97e-02
     172  4.23e+04  3.66e+04  1.88e+03  3.78e-03  1.95e-02
     173  4.22e+04  3.66e+04  1.88e+03  3.75e-03  1.93e-02
     174  4.22e+04  3.66e+04  1.87e+03  3.72e-03  1.91e-02
     175  4.22e+04  3.66e+04  1.87e+03  3.69e-03  1.88e-02
     176  4.22e+04  3.66e+04  1.86e+03  3.66e-03  1.86e-02
     177  4.22e+04  3.66e+04  1.86e+03  3.63e-03  1.83e-02
     178  4.22e+04  3.66e+04  1.86e+03  3.61e-03  1.79e-02
     179  4.22e+04  3.66e+04  1.85e+03  3.58e-03  1.76e-02
     180  4.22e+04  3.66e+04  1.85e+03  3.55e-03  1.73e-02
     181  4.21e+04  3.66e+04  1.84e+03  3.52e-03  1.71e-02
     182  4.21e+04  3.66e+04  1.84e+03  3.50e-03  1.70e-02
     183  4.21e+04  3.66e+04  1.84e+03  3.47e-03  1.69e-02
     184  4.21e+04  3.66e+04  1.83e+03  3.44e-03  1.68e-02
     185  4.21e+04  3.66e+04  1.83e+03  3.41e-03  1.68e-02
     186  4.21e+04  3.66e+04  1.82e+03  3.38e-03  1.67e-02
     187  4.21e+04  3.66e+04  1.82e+03  3.35e-03  1.67e-02
     188  4.20e+04  3.66e+04  1.81e+03  3.33e-03  1.66e-02
     189  4.20e+04  3.66e+04  1.81e+03  3.30e-03  1.65e-02
     190  4.20e+04  3.66e+04  1.80e+03  3.27e-03  1.62e-02
     191  4.20e+04  3.66e+04  1.80e+03  3.25e-03  1.60e-02
     192  4.20e+04  3.66e+04  1.80e+03  3.23e-03  1.57e-02
     193  4.20e+04  3.66e+04  1.79e+03  3.21e-03  1.54e-02
     194  4.20e+04  3.66e+04  1.79e+03  3.19e-03  1.51e-02
     195  4.20e+04  3.66e+04  1.79e+03  3.17e-03  1.48e-02
     196  4.20e+04  3.66e+04  1.79e+03  3.15e-03  1.46e-02
     197  4.20e+04  3.66e+04  1.79e+03  3.12e-03  1.45e-02
     198  4.20e+04  3.66e+04  1.78e+03  3.10e-03  1.44e-02
     199  4.19e+04  3.66e+04  1.78e+03  3.08e-03  1.44e-02
    ------------------------------------------------------


Reconstruct the denoised estimate.

.. code:: ipython3

    imgdp = b.reconstruct().squeeze() + imglp
    imgd = crop(imgdp)

Display solve time and denoising performance.

.. code:: ipython3

    print("ConvRepL1L1 solve time: %5.2f s" % b.timer.elapsed('solve'))
    print("Noisy image PSNR:    %5.2f dB" % sm.psnr(img, imgn))
    print("Denoised image PSNR: %5.2f dB" % sm.psnr(img, imgd))


.. parsed-literal::

    ConvRepL1L1 solve time: 146.38 s
    Noisy image PSNR:    10.37 dB
    Denoised image PSNR: 27.39 dB


Display the reference, noisy, and denoised images.

.. code:: ipython3

    fig, ax = plot.subplots(nrows=1, ncols=3, figsize=(21, 7))
    fig.suptitle('Method 2 Results')
    plot.imview(img, ax=ax[0], title='Reference', fig=fig)
    plot.imview(imgn, ax=ax[1], title='Noisy', fig=fig)
    plot.imview(imgd, ax=ax[2], title='CSC Result', fig=fig)
    fig.show()



.. image:: implsden_clr_files/implsden_clr_31_0.png

