from pyworkflow.protocol.params import (
    PointerParam, IntParam, FloatParam, BooleanParam, LEVEL_ADVANCED)
from pyworkflow.utils import Message
from pwem.objects import Volume
from pwem.protocols import ProtAnalysis3D

import mrcfile

from ucm.computations import bfactor


class ProtLocBFactor(ProtAnalysis3D):
    """
    Given a map and a mask the protocol estimates the local B-factor map.
    """
    _label = 'local b-factor'

    def _defineParams(self, form):
        "Add parameters to the form in the scipion gui for the protocol"
        form.addSection(label=Message.LABEL_INPUT)

        add = form.addParam  # shortcut

        add('vol', PointerParam, pointerClass='Volume',
            label='Map', important=True,
            help='Map for determining its local b-factors.')

        add('mask_in_molecule', PointerParam, pointerClass='VolumeMask',
            label='Mask selecting the molecule',
            help='Tight binary map that differenciates between the '
                 'macromolecule (1) and the background (0).')

        add('min_res', FloatParam, expertLevel=LEVEL_ADVANCED,
            label='Minimum resolution',
            default=15,
            help='Minimun resolution of the sweeping resolution range in '
                 'Angstroms. A value of 15-10 Angstroms is normally good.')

        add('max_res', FloatParam,
            label='Maximum resolution',
            help='Maximum resolution (in Angstroms) of the resolution range. '
                 'Provide here the obtained FSC global resolution value.')

        add('num_points', IntParam, expertLevel=LEVEL_ADVANCED,
            label='Number of sampling points',
            default=10,
            help='Number of sampling points in frequency used to fit the '
                 'B-factor. Usually 5-10 points are enough.')

        add('noise_threshold', FloatParam, expertLevel=LEVEL_ADVANCED,
            label='Noise threshold',
            default=0.9,
            help='Percentile of noise used to discriminate signal from noise. '
                 'Good values are 0.9 or 0.95.')

        add('f_voxel_width', FloatParam, expertLevel=LEVEL_ADVANCED,
            label='Frequency selection width in bins',
            default=4.8,
            help='Number of frequency bins used for the width of the bandpass '
                 'filter that selects a frequency.')

        add('only_above_noise', BooleanParam,
            label='Use only points above noise?',
            default=False,
            help='When calculating the B-factors for each voxel using the '
                 'local Guinier plots, you can use all the frequency points '
                 '(the default and fast way), or use only those above the '
                 'noise level. If using only points above noise, the B-factor '
                 'of voxels that cannot be fitted are set to NaN.')

        form.addParallelSection(threads=4, mpi=1)

    def _insertAllSteps(self):
        "State the name of the functions that will be called to run the method"
        self._insertFunctionStep('computeBFactorStep')
        self._insertFunctionStep('createOutputStep')

    def computeBFactorStep(self):
        "Generate a b-factor map as an mrc file"
        # Read form parameters.
        volume_path = self.vol.get().getFileName()
        vol = mrcfile.open(volume_path).data

        mask_path = self.mask_in_molecule.get().getFileName()
        mask = mrcfile.open(mask_path).data.astype(bool)

        voxel_size = self.vol.get().getSamplingRate()
        min_res = self.min_res.get()
        max_res = self.max_res.get()
        num_points = self.num_points.get()
        noise_threshold = self.noise_threshold.get()
        f_voxel_width = self.f_voxel_width.get()
        only_above_noise = self.only_above_noise.get()
        nthreads = max(1, self.numberOfThreads.get() * self.numberOfMpi.get())

        # Call the main function to do the work.
        bmap = bfactor(vol, mask, voxel_size, min_res, max_res,
                       num_points, noise_threshold, f_voxel_width,
                       only_above_noise, nthreads)

        # Save the bmap as an mrc file.
        bmap_path = self._getExtraPath('bmap.mrc')

        with mrcfile.new(bmap_path) as mrc:
            mrc.set_data(bmap)
            mrc.voxel_size = voxel_size

    def createOutputStep(self):
        "Create a scipion volume related to the output mrc file"
        bmap = Volume()
        bmap.setFileName(self._getExtraPath('bmap.mrc'))
        bmap.setSamplingRate(self.vol.get().getSamplingRate())
        self._defineOutputs(bmap=bmap)
        self._defineSourceRelation(self.vol, bmap)
