from multiprocessing import Pool

import numpy as np
from numpy import abs, sqrt, exp, log
from numpy.fft import fftn, ifftn


def fftnfreq(n, d=1):
    "Return the Discrete Fourier Transform sample frequencies"
    f = np.fft.fftfreq(n, d)
    return np.meshgrid(f, f, f)


def shell(f):
    "Return a normalized shell of spatial frequencies, around frequency f"
    global f_norm, f_width
    S = exp(- (f_norm - f)**2 / (2 * f_width**2))
    return S / np.sum(S)


def spiral_filter(voxel_n, voxel_size):
    "Return the freq-domain spiral filter for the three dimensions (x, y, z)"
    fx, fy, fz = fftnfreq(voxel_n, d=voxel_size)
    f_norm = sqrt(fx**2 + fy**2 + fz**2)

    def H(fi):
        return -1j * np.nan_to_num(fi / f_norm)

    with np.errstate(invalid='ignore'):  # ignore divide-by-0 warning in one bin
        return H(fx), H(fy), H(fz)


def mask_in_sphere(n):
    "Return a mask selecting voxels of the biggest sphere inside a n*n*n grid"
    coords = np.r_[:n] - n/2
    x, y, z = np.meshgrid(coords, coords, coords)
    r = sqrt(x**2 + y**2 + z**2)
    return r < n/2


def linear_fit_params(x, y):
    "Return the parameters a[...], b[...] when fitting y[:,...] to a+b*x[:]"
    # See https://en.wikipedia.org/wiki/Ordinary_least_squares#Matrix/vector_formulation
    X = np.column_stack((np.ones(len(x)), x))
    return np.tensordot(np.linalg.pinv(X), y, 1)


def amplitude(f):
    "Return the amplitude map corresponding to the given frequency f"
    global FV, Hx, Hy, Hz

    SFV = shell(f) * FV  # volume in frequency space, at frequency f

    v0 = ifftn(SFV)  # volume "at frequency f"

    vx = ifftn(Hx * SFV)  # conjugate volumes at this frequency
    vy = ifftn(Hy * SFV)
    vz = ifftn(Hz * SFV)

    return sqrt(abs(v0)**2 + abs(vx)**2 + abs(vy)**2 + abs(vz)**2)


def weighted_log_amplitude_and_noise(f):
    "Return the weighted log amplitude map and noise at frequency f"
    global mask_background, threshold

    m = amplitude(f)
    noise = np.quantile(m[mask_background], threshold)

    # Something related to the SNR (all noise = 0.5 < Cref < 1 = no noise).
    Cref = m / (m + noise)  # will be used to weight m

    # (log of) weighted amplitude map and noise at the corresponding frequency.
    return log(Cref * m), log(noise)


def get_voxels(V):
    "Yield triplets (i,j,k) that travel thru all voxels of volume V"
    index_iterator = np.nditer(V, flags=['multi_index'])
    for x in index_iterator:
        yield index_iterator.multi_index


def find_b(voxel):
    "Return the b-factor as computed for the given voxel"
    global mods, noises, f2

    i, j, k = voxel
    mod_f = mods[:,i,j,k]

    valid_points = np.where(mod_f > noises)
    f2_valid = f2[valid_points]
    mod_f_valid = mod_f[valid_points]

    if len(f2_valid) > 2:
        return 4 * linear_fit_params(f2_valid, mod_f_valid)[1]
    else:
        return np.nan


def bfactor(vol, mask_in_molecule, voxel_size, min_res=15, max_res=2.96,
            num_points=10, noise_threshold=0.9, f_voxel_width=4.8,
            only_above_noise=False, nthreads=None):
    "Return a map with the local b-factors at each voxel"
    global FV, Hx, Hy, Hz, mask_background, threshold, f_norm, f_width, \
        mods, noises, f2

    voxel_n, _, _ = vol.shape  # vol is a 3d array n*n*n

    # Set some global variables.
    FV = fftn(vol)  # precompute the volume's Fourier transform
    threshold = noise_threshold  # to use in amplitude_map()

    # To select voxels with background data (used in the quantile evaluation).
    mask_background = np.logical_and(~mask_in_molecule, mask_in_sphere(voxel_n))

    # Get ready to select frequencies (using a shell in frequency space).
    fx, fy, fz = fftnfreq(voxel_n, d=voxel_size)
    f_norm = sqrt(fx**2 + fy**2 + fz**2)
    f_width = f_voxel_width / (voxel_n * voxel_size)  # frequency width

    # Define the spiral filter in frequency space.
    Hx, Hy, Hz = spiral_filter(voxel_n, voxel_size)

    # Compute amplitude maps at frequencies between min and max resolution.
    freqs = np.linspace(1/min_res, 1/max_res, num_points)

    with Pool(nthreads) as pool:
        mods, noises = zip(*pool.map(weighted_log_amplitude_and_noise, freqs))

    mods = np.array(mods)
    noises = np.array(noises)

    # Compute the local b-factor map.
    f2 = freqs**2

    if not only_above_noise:
        a_b = linear_fit_params(f2, mods)  # contains fit parameters per voxel
        bmap = 4 * a_b[1,:,:,:]  # the 2nd parameter of the fit is ~ the "b" map
    else:
        with Pool(nthreads) as pool:
            bmap = np.array(pool.map(find_b, get_voxels(vol)))
        bmap.shape = vol.shape  # reshape all voxels into a n*n*n volume

    return bmap.astype(np.float32)


def occupancy(vol, mask_in_molecule, voxel_size, min_res=20, max_res=3,
              protein_threshold=0.25, f_voxel_width=4.6):
    "Return a map with the local occupancy at each voxel"
    global FV, Hx, Hy, Hz, f_norm, f_width

    voxel_n, _, _ = vol.shape  # vol is a 3d array n*n*n
    FV = fftn(vol)  # precompute the volume's Fourier transform

    # Get ready to select frequencies (using a shell in frequency space).
    fx, fy, fz = fftnfreq(voxel_n, d=voxel_size)
    f_norm = sqrt(fx**2 + fy**2 + fz**2)
    f_width = f_voxel_width / (voxel_n * voxel_size)  # frequency width

    # Define the spiral filter in frequency space.
    Hx, Hy, Hz = spiral_filter(voxel_n, voxel_size)

    # Compute occupancy maps at frequencies between min and max resolution.
    f_min, f_max = 1/min_res, 1/max_res
    num_points = max(1, int((f_max - f_min) / f_width))
    freqs = np.linspace(f_min, f_max, num_points)

    omap = np.zeros_like(vol)
    for f in freqs:
        m = amplitude(f)
        q = np.quantile(m[mask_in_molecule], protein_threshold)  # signal level
        omap += (m >= q)  # add 1 to voxels above that quantile
    omap /= len(freqs)  # omap is the average occupancy map for the freqs

    return omap.astype(np.float32)
