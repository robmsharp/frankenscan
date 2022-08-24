import SimpleITK as sitk
import cv2
import ryvencore_qt as rc

from frankenscan.controller.modules.selectFiles.selectFilesWidget import SelectFilesWidget
from frankenscan.controller.modules.values.selectIntWidget import SelectIntWidget


class Create_Int(rc.Node):
    """Outputs an integer"""

    title = 'Integer'

    init_outputs = [
        rc.NodeOutputBP('Integer', type_='data')
    ]

    color = '#000000'

    main_widget_class = SelectIntWidget
    main_widget_pos = 'between ports'

    # Register the widget for this node
    def view_place_event(self):
        self.main_widget().intSelectedSignal.connect(self.registerInt)
        self.update()

    def registerInt(self, myInt):

        self.intSelected = myInt
        self.update()

    def __init__(self, params):
        super().__init__(params)
        self.hasRun = False
        self.filesSelected = None

    def update_event(self, inp=-1):

        #Only update if selected files is not none
        if self.hasRun == False and self.intSelected != None:

            print("Updating the int")
            self.set_output_val(0, self.intSelected)
            self.hasRun = True
