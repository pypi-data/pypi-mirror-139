.. _examples_csc_index:

Convolutional Sparse Coding
===========================

Basic Usage
-----------

Greyscale Images
^^^^^^^^^^^^^^^^

.. toctree::
   :maxdepth: 1

   Convolutional sparse coding (ADMM solver) <cbpdn_gry>
   Convolutional sparse coding using the parallel ADMM solver <parcbpdn_gry>
   Convolutional sparse coding using the CUDA solver <cbpdn_cuda>
   Convolutional sparse coding (PGM solver) <cbpdn_pgm_gry>
   Convolutional sparse coding (constrained data fidelity) <cminl1_gry>
   Convolutional sparse coding (constrained penalty term) <cprjl1_gry>
   Convolutional sparse coding with gradient penalty using the CUDA solver <cbpdn_grd_cuda>
   Convolutional sparse coding with lateral inhibition <cbpdnin_gry>
   Convolutional sparse coding with weighted lateral inhibition <cbpdnin_wgt_gry>


Colour Images
^^^^^^^^^^^^^

.. toctree::
   :maxdepth: 1

   Convolutional sparse coding of a colour image with a colour dictionary <cbpdn_clr_cd>
   Convolutional sparse coding of a colour image with a colour dictionary (PGM solver) <cbpdn_pgm_clr>
   Convolutional sparse coding of a colour image with a greyscale dictionary <cbpdn_clr_gd>
   Convolutional sparse coding of a colour image with a greyscale dictionary and a joint sparsity term <cbpdn_jnt_clr>
   Convolutional sparse coding of a colour image with a product dictionary <cbpdn_clr_pd>


Image Restoration Applications
------------------------------

Denoising (Gaussian White Noise)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. toctree::
   :maxdepth: 1

   Remove Gaussian white noise from a greyscale image using convolutional sparse coding <gwnden_gry>
   Remove Gaussian white noise from a colour image using convolutional sparse coding <gwnden_clr>


Denoising (Impulse Noise)
^^^^^^^^^^^^^^^^^^^^^^^^^

.. toctree::
   :maxdepth: 1

   Remove salt & pepper noise from a colour image using convolutional sparse coding with a colour dictionary <implsden_clr>
   Remove salt & pepper noise from a colour image using convolutional sparse coding with an l1 data fidelity term and an l2 gradient term, with a colour dictionary <implsden_grd_clr>
   Remove salt & pepper noise from a hyperspectral image using convolutional sparse coding with an l1 data fidelity term and an l2 gradient term, with a dictionary consisting of the product of a convolutional dictionary for the spatial axes and a standard dictionary for the spectral axis <implsden_grd_pd_dct>
   Remove salt & pepper noise from a hyperspectral image using convolutional sparse coding with an l1 data fidelity term and an l2 gradient term, with a dictionary consisting of the product of a convolutional dictionary for the spatial axes and a PCA basis for the spectral axis <implsden_grd_pd_pca>


Inpainting
^^^^^^^^^^

.. toctree::
   :maxdepth: 1

   Inpainting of randomly distributed pixel corruption with lowpass image components handled via non-linear filtering (greyscale image) <cbpdn_ams_gry>
   Inpainting of randomly distributed pixel corruption with lowpass image components handled via gradient regularisation of an impulse dictionary filter (greyscale image) <cbpdn_ams_grd_gry>
   Inpainting of randomly distributed pixel corruption (greyscale image) <cbpdn_md_gry>
   Inpainting of randomly distributed pixel corruption (greyscale image) using the parallel ADMM solver <parcbpdn_md_gry>
   Inpainting of randomly distributed pixel corruption (colour image) <cbpdn_ams_clr>
