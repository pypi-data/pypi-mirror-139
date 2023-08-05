from pyworkflow.protocol.params import (
    PointerParam, FloatParam, LEVEL_ADVANCED)
from pyworkflow.utils import Message
from pwem.objects import Volume
from pwem.protocols import ProtAnalysis3D

import mrcfile

from ucm.computations import occupancy


class ProtLocOccupancy(ProtAnalysis3D):
    """
    Given a map and a mask, the protocol computes the local occupancy map.
    """
    _label = 'local occupancy'

    def _defineParams(self, form):
        "Add parameters to the form in the scipion gui for the protocol"
        form.addSection(label=Message.LABEL_INPUT)

        add = form.addParam  # shortcut

        add('vol', PointerParam, pointerClass='Volume',
            label='Map', important=True,
            help='Map for determining its local occupancy.')

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

        add('protein_threshold', FloatParam, expertLevel=LEVEL_ADVANCED,
            label='Protein threshold',
            default=0.25,
            help='Percentile to select a typical protein signal.')

        add('f_voxel_width', FloatParam, expertLevel=LEVEL_ADVANCED,
            label='Frequency selection width in bins',
            default=4.8,
            help='Number of frequency bins used for the width of the bandpass '
                 'filter applied in Fourier Space.')

    def _insertAllSteps(self):
        "State the name of the functions that will be called to run the method"
        self._insertFunctionStep('computeOccupancyStep')
        self._insertFunctionStep('createOutputStep')

    def computeOccupancyStep(self):
        "Generate an occupancy map as an mrc file"
        # Read form parameters.
        volume_path = self.vol.get().getFileName()
        vol = mrcfile.open(volume_path).data

        mask_path = self.mask_in_molecule.get().getFileName()
        mask = mrcfile.open(mask_path).data.astype(bool)

        voxel_size = self.vol.get().getSamplingRate()
        min_res = self.min_res.get()
        max_res = self.max_res.get()
        protein_threshold = self.protein_threshold.get()
        f_voxel_width = self.f_voxel_width.get()

        # Call the main function to do the work.
        omap = occupancy(vol, mask, voxel_size, min_res, max_res,
                         protein_threshold, f_voxel_width)

        # Save the omap as an mrc file.
        omap_path = self._getExtraPath('omap.mrc')

        with mrcfile.new(omap_path) as mrc:
            mrc.set_data(omap)
            mrc.voxel_size = voxel_size

    def createOutputStep(self):
        "Create a scipion volume related to the output mrc file"
        omap = Volume()
        omap.setFileName(self._getExtraPath('omap.mrc'))
        omap.setSamplingRate(self.vol.get().getSamplingRate())
        self._defineOutputs(omap=omap)
        self._defineSourceRelation(self.vol, omap)
