from PySide2.QtWidgets import QWidget, QTextEdit
from ryvencore_qt import MWB
import ryvencore_qt as rc

from frankenscan.controller.modules.selectFiles.selectFilesWidget import SelectFilesWidget

class Select_nii_Files(rc.Node):
    """Selects NIFTI (.nii) files specified by user"""

    title = 'Select NIFTI (.nii) files'

    init_outputs = [
        rc.NodeOutputBP('Selected .nii files', type_='data')
    ]
    color = '#000000'

    main_widget_class = SelectFilesWidget
    main_widget_pos = 'between ports'

    def __init__(self, params):
        super().__init__(params)
        self.hasRun = False

    def update_event(self, inp=-1):
        if self.hasRun == False:
            self.run = True