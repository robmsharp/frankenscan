from PySide2.QtWidgets import QWidget, QTextEdit
from ryvencore_qt import MWB
import ryvencore_qt as rc

from frankenscan.controller.modules.selectFiles.selectFilesWidget import SelectFilesWidget

class Read_nii_Files(rc.Node):
    """Reads NIFTI (.nii) files into headers and numpy arrays"""

    title = 'Reads NIFTI (.nii) files'

    init_inputs = [
        rc.NodeInputBP('Selected .nii files', type_='data')
    ]

    init_outputs = [
        rc.NodeOutputBP('Headers', type_='data'),
        rc.NodeOutputBP('Numpy arrays', type_='data')
    ]

    color = '#000000'

    def __init__(self, params):
        super().__init__(params)
        self.hasRun = False

    def update_event(self, inp=-1):
        if self.hasRun == False:
            self.run = True