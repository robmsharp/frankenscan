from PySide2.QtWidgets import QWidget, QTextEdit
from ryvencore_qt import MWB
import ryvencore_qt as rc

from frankenscan.controller.modules.openFiles.openFilesWidget import OpenFilesWidget

class Open_Files(rc.Node):
    """Outputs files selected by user"""

    title = 'Opens files'

    init_inputs = [
        rc.NodeInputBP('data', type_='data')
    ]
    init_outputs = [
        rc.NodeInputBP('output', type_='data')
    ]
    color = '#000000'

    main_widget_class = OpenFilesWidget
    main_widget_pos = 'between ports'

    def __init__(self, params):
        super().__init__(params)
        self.hasRun = False

    def update_event(self, inp=-1):
        if self.hasRun == False:
            self.run = True