from PySide2.QtWidgets import QWidget, QTextEdit
from ryvencore_qt import MWB
import ryvencore_qt as rc

from frankenscan.controller.modules.selectFiles.selectFilesWidget import SelectFilesWidget

class Select_Image_Files(rc.Node):
    """Selects image files specified by user"""

    title = 'Select image files'

    init_outputs = [
        rc.NodeOutputBP('Selected image files', type_='data')
    ]
    color = '#000000'

    main_widget_class = SelectFilesWidget
    main_widget_pos = 'between ports'

    # Register the widget for this node
    def view_place_event(self):
        self.main_widget().filesSelectedSignal.connect(self.registerSelection)
        self.main_widget().setFileTypeList(["Image (*.jpg *.png *.gif)"])
        self.update()

    def registerSelection(self, files):

        self.filesSelected = files
        self.update()

    def __init__(self, params):
        super().__init__(params)
        self.hasRun = False
        self.filesSelected = None

    def update_event(self, inp=-1):

        #Only update if selected files is not none
        if self.hasRun == False and self.filesSelected != None:

            print("Updating select images node output")
            self.set_output_val(0, self.filesSelected)
            self.hasRun = True

class Select_nii_Files(rc.Node):
    """Selects NIFTI (.nii) files specified by user"""

    title = 'Select NIFTI (.nii) files'

    init_outputs = [
        rc.NodeOutputBP('Selected .nii files', type_='data')
    ]
    color = '#000000'

    main_widget_class = SelectFilesWidget
    main_widget_pos = 'between ports'

    # Register the widget for this node
    def view_place_event(self):
        self.main_widget().filesSelectedSignal.connect(self.registerSelection)
        self.main_widget().setFileTypeList(["NIFTI format image (*.nii)"])
        self.update()

    def registerSelection(self, files):

        self.filesSelected = files
        self.update()

    def __init__(self, params):
        super().__init__(params)
        self.hasRun = False
        self.filesSelected = None

    def update_event(self, inp=-1):

        #Only update if selected files is not none
        if self.hasRun == False and self.filesSelected != None:

            print("Updating select .nii node output")
            self.set_output_val(0, self.filesSelected)
            self.hasRun = True