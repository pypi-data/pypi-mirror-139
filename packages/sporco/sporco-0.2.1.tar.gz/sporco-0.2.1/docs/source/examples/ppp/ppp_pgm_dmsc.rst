.. _examples_ppp_ppp_pgm_dmsc:

Plug-and-Play PGM Demosaicing
=============================

This example demonstrates the use of class :class:`.pgm.ppp.PPP` for
solving a raw image demosaicing problem via the PGM Plug and Play Priors
(PPP) algorithm :cite:`kamilov-2017-plugandplay`.

.. code:: ipython3

    from __future__ import print_function
    from builtins import input, range

    import numpy as np

    from bm3d import bm3d_rgb
    try:
        from colour_demosaicing import demosaicing_CFA_Bayer_Menon2007
    except ImportError:
        have_demosaic = False
    else:
        have_demosaic = True

    from sporco.pgm.ppp import PPP
    from sporco.interp import bilinear_demosaic
    from sporco import metric
    from sporco import util
    from sporco import plot
    plot.config_notebook_plotting()

Define demosaicing forward operator and its transpose.

.. code:: ipython3

    def A(x):
        """Map an RGB image to a single channel image with each pixel
        representing a single colour according to the colour filter array.
        """

        y = np.zeros(x.shape[0:2])
        y[1::2, 1::2] = x[1::2, 1::2, 0]
        y[0::2, 1::2] = x[0::2, 1::2, 1]
        y[1::2, 0::2] = x[1::2, 0::2, 1]
        y[0::2, 0::2] = x[0::2, 0::2, 2]
        return y


    def AT(x):
        """Back project a single channel raw image to an RGB image with zeros
        at the locations of undefined samples.
        """

        y = np.zeros(x.shape + (3,))
        y[1::2, 1::2, 0] = x[1::2, 1::2]
        y[0::2, 1::2, 1] = x[0::2, 1::2]
        y[1::2, 0::2, 1] = x[1::2, 0::2]
        y[0::2, 0::2, 2] = x[0::2, 0::2]
        return y

Define baseline demosaicing function. If package
`colour_demosaicing <https://github.com/colour-science/colour-demosaicing>`__
is installed, use the demosaicing algorithm of
:cite:`menon-2007-demosaicing`, othewise use simple bilinear
demosaicing.

.. code:: ipython3

    if have_demosaic:
        def demosaic(cfaimg):
            return demosaicing_CFA_Bayer_Menon2007(cfaimg, pattern='BGGR')
    else:
        def demosaic(cfaimg):
            return bilinear_demosaic(cfaimg)

Load reference image.

.. code:: ipython3

    img = util.ExampleImages().image('kodim23.png', scaled=True,
                                     idxexp=np.s_[160:416,60:316])

Construct test image constructed by colour filter array sampling and
adding Gaussian white noise.

.. code:: ipython3

    np.random.seed(12345)
    s = A(img)
    rgbshp = s.shape + (3,)  # Shape of reconstructed RGB image
    rgbsz = s.size * 3       # Size of reconstructed RGB image
    nsigma = 2e-2            # Noise standard deviation
    sn = s + nsigma * np.random.randn(*s.shape)

Define data fidelity term for PPP problem.

.. code:: ipython3

    def f(x):
        return 0.5 * np.linalg.norm((A(x) - sn).ravel())**2

Define gradient of data fidelity term for PPP problem.

.. code:: ipython3

    def gradf(x):
        return AT(A(x) - sn)

Define proximal operator of (implicit, unknown) regularisation term for
PPP problem. In this case we use BM3D :cite:`dabov-2008-image` as the
denoiser, using the `code <https://pypi.org/project/bm3d>`__ released
with :cite:`makinen-2019-exact`.

.. code:: ipython3

    bsigma = 3.3e-2  # Denoiser parameter

    def proxg(x, L):
        return bm3d_rgb(x, bsigma)

Construct a baseline solution and initaliser for the PPP solution by
BM3D denoising of a simple bilinear demosaicing solution. The
``3 * nsigma`` denoising parameter for BM3D is chosen empirically for
best performance.

.. code:: ipython3

    imgb = bm3d_rgb(demosaic(sn), 3 * nsigma)

Set algorithm options for PPP solver, including use of bilinear
demosaiced solution as an initial solution.

.. code:: ipython3

    opt = PPP.Options({'Verbose': True, 'RelStopTol': 1e-3,
                       'MaxMainIter': 20, 'L': 6.8e-1, 'X0': imgb})

Create solver object and solve, returning the the demosaiced image
``imgp``.

.. code:: ipython3

    b = PPP(img.shape, f, gradf, proxg, opt=opt)
    imgp = b.solve()


.. parsed-literal::

    Itn   FVal      Rsdl
    ------------------------
       0  1.44e+01  1.33e+00
       1  1.39e+01  6.39e-01
       2  1.37e+01  3.63e-01
       3  1.35e+01  2.15e-01
       4  1.35e+01  1.53e-01
       5  1.34e+01  1.29e-01
       6  1.34e+01  1.14e-01
       7  1.34e+01  1.07e-01
       8  1.34e+01  1.04e-01
       9  1.34e+01  9.68e-02
      10  1.34e+01  9.61e-02
      11  1.34e+01  9.49e-02
      12  1.34e+01  9.81e-02
      13  1.34e+01  9.42e-02
      14  1.34e+01  9.26e-02
      15  1.34e+01  9.53e-02
      16  1.34e+01  9.72e-02
      17  1.34e+01  9.59e-02
      18  1.34e+01  9.61e-02
      19  1.34e+01  9.55e-02
    ------------------------


Display solve time and demosaicing performance.

.. code:: ipython3

    print("PPP PGM solve time:        %5.2f s" % b.timer.elapsed('solve'))
    print("Baseline demosaicing PSNR:  %5.2f dB" % metric.psnr(img, imgb))
    print("PPP demosaicing PSNR:       %5.2f dB" % metric.psnr(img, imgp))


.. parsed-literal::

    PPP PGM solve time:        71.54 s
    Baseline demosaicing PSNR:  35.98 dB
    PPP demosaicing PSNR:       36.59 dB


Display reference and demosaiced images.

.. code:: ipython3

    fig, ax = plot.subplots(nrows=1, ncols=3, sharex=True, sharey=True,
                            figsize=(21, 7))
    plot.imview(img, title='Reference', fig=fig, ax=ax[0])
    plot.imview(imgb, title='Baseline demoisac: %.2f (dB)' %
                metric.psnr(img, imgb), fig=fig, ax=ax[1])
    plot.imview(imgp, title='PPP demoisac: %.2f (dB)' %
                metric.psnr(img, imgp), fig=fig, ax=ax[2])
    fig.show()



.. image:: ppp_pgm_dmsc_files/ppp_pgm_dmsc_25_0.png

