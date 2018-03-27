#                                                            _
# chris_test ds app
#
# (c) 2016 Fetal-Neonatal Neuroimaging & Developmental Science Center
#                   Boston Children's Hospital
#
#              http://childrenshospital.org/FNNDSC/
#                        dev@babyMRI.org
#

import os
import numpy as np
import sys

# import the Chris app superclass
from chrisapp.base import ChrisApp


class Chris_test(ChrisApp):
    """
    Chris Hackathon test app.
    """
    AUTHORS         = 'AWC (aiwern.chung@childrens.harvard.edu)'
    SELFPATH        = os.path.dirname(os.path.abspath(__file__))
    SELFEXEC        = os.path.basename(__file__)
    EXECSHELL       = 'python3'
    TITLE           = 'Chris Container Hackathon'
    CATEGORY        = 'Test'
    TYPE            = 'ds'
    DESCRIPTION     = 'Chris Hackathon test app'
    DOCUMENTATION   = 'http://wiki'
    VERSION         = '0.1'
    LICENSE         = 'Opensource (MIT)'
    MAX_NUMBER_OF_WORKERS = 1  # Override with integer value
    MIN_NUMBER_OF_WORKERS = 1  # Override with integer value
    MAX_CPU_LIMIT         = '' # Override with millicore value as string, e.g. '2000m'
    MIN_CPU_LIMIT         = '' # Override with millicore value as string, e.g. '2000m'
    MAX_MEMORY_LIMIT      = '' # Override with string, e.g. '1Gi', '2000Mi'
    MIN_MEMORY_LIMIT      = '' # Override with string, e.g. '1Gi', '2000Mi'
    MIN_GPU_LIMIT         = 0  # Override with the minimum number of GPUs, as an integer, for your plugin
    MAX_GPU_LIMIT         = 0  # Override with the maximum number of GPUs, as an integer, for your plugin

    # Fill out this with key-value output descriptive info (such as an output file path
    # relative to the output dir) that you want to save to the output meta file when
    # called with the --saveoutputmeta flag
    OUTPUT_META_DICT = {}
 
    def define_parameters(self):
        """
        Define the CLI arguments accepted by this plugin app.
        """

        self.add_argument('--bvec', dest='bvec', type=str, optional=False,
                          help='bvec file to rotate')
        self.add_argument('--rot',
                          dest='rot',
                          type=str,
                          optional=False,
                          help='File containing rotation matrix')
        self.add_argument('--outstr', dest='outstr', type=str, optional=False,
                          help='Output file name')


    def run(self, options):
        """
        Define the code to be run by this plugin app.
        """
        #options.outputdir

        instrRot = '%s/%s' % (options.inputdir, options.rot)
        rots = np.loadtxt(instrRot)  # rots.shape = (nDirs, 16)
        instrbvec = '%s/%s' % (options.inputdir, options.bvec)
        bvecs = np.loadtxt(instrbvec)

        nDir = bvecs.shape[1]
        rotBvec = np.zeros((bvecs.shape))

        # If dealing with fsl's eddy output of rotations
        if (instrRot.split('.')[-1] == 'eddy_parameters'):

            # eddy x-, y-, z- rotations (in radians) are store in columns 4-6 of this fsl edd output textfile
            # Cols 1:3 are the translations in x,y,z, 4:6 are rotations, and 7: are warp params
            rots = rots[:, 3:6]  # nDirs x [x,y,z]

        else:
            sys.stderr.write('\tFunction image_processing_utils.rotate_bvecs:\n\n')
            sys.stderr.write('\t\tDealing with rotation file that is as yet unrecognised. Need to add code!')
            sys.stderr.write('\t\tReturning exit code = 1\n\n')


        # An assumption is made here that the first volume is b0- and is that all other volumes were registered to by eddy
        for i in range(nDir):
            origVec = bvecs[:, i]  # Get original gradient
            rot = rots[i, :]  # Get rotations
            rotationMats = np.zeros((3, 3, 3))

            # For x-rotation
            rotationMats[0, 0, 0] = np.cos(rot[0])
            rotationMats[0, 1, 0] = np.sin(rot[0])
            rotationMats[1, 0, 0] = -np.sin(rot[0])
            rotationMats[1, 1, 0] = np.cos(rot[0])
            rotationMats[2, 2, 0] = 1

            # For y-rotation
            rotationMats[0, 0, 1] = np.cos(rot[1])
            rotationMats[0, 1, 1] = np.sin(rot[1])
            rotationMats[1, 0, 1] = -np.sin(rot[1])
            rotationMats[1, 1, 1] = np.cos(rot[1])
            rotationMats[2, 2, 1] = 1

            # For z-rotation
            rotationMats[0, 0, 2] = np.cos(rot[2])
            rotationMats[0, 1, 2] = np.sin(rot[2])
            rotationMats[1, 0, 2] = -np.sin(rot[2])
            rotationMats[1, 1, 2] = np.cos(rot[2])
            rotationMats[2, 2, 2] = 1

            # x' = (R_x R_y R_z)^-1 x
            temp = np.dot(np.linalg.inv(rotationMats[:, :, 0] * rotationMats[:, :, 1] * rotationMats[:, :, 2]),
                          origVec)
            rotBvec[:, i] = temp

        # Output and save
        ostr='%s/%s' % (option.outputdir, option.outstr)
        np.savetxt(ostr, rotBvec, fmt='%0.7f', delimiter='\t')



# ENTRYPOINT
if __name__ == "__main__":
    app = Chris_test()
    app.launch()
