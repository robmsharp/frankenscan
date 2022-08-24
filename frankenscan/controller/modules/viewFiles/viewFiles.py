import ryvencore_qt as rc

from frankenscan.controller.modules.viewFiles.dataLoaderViewer import DataLoaderViewer
from frankenscan.controller.modules.viewFiles.headerViewer import HeaderViewer
from frankenscan.controller.modules.viewFiles.arrayViewer import ArrayViewer
from frankenscan.controller.modules.viewFiles.imageViewer import ImageViewer


class View_Confusion_Matrix(rc.Node):
    """Views Confusion Matrix"""

    title = 'View Confusion Matrix'

    init_inputs = [
        rc.NodeInputBP('Predicted labels', type_='data'),
        rc.NodeInputBP('True labels', type_='data')
    ]
    color = '#000000'

    def __init__(self, params):
        super().__init__(params)
        self.hasRun = False

    def update_event(self, inp=-1):
        if self.hasRun == False and self.input(0)!=None:
            print("Viewing dataLoader")
            data = self.input(0)
            try:
                DataLoaderViewer(self, data)
            except Exception as e:
                print(e)
            self.run = True

class View_Data_Loader(rc.Node):
    """Views labelled MRI images"""

    title = 'View Data Loader'

    init_inputs = [
        rc.NodeInputBP('Data loader', type_='data')
    ]
    color = '#000000'

    def __init__(self, params):
        super().__init__(params)
        self.hasRun = False

    def update_event(self, inp=-1):
        if self.hasRun == False and self.input(0)!=None:
            print("Viewing dataLoader")
            data = self.input(0)
            try:
                DataLoaderViewer(self, data)
            except Exception as e:
                print(e)
            self.run = True

class View_Image(rc.Node):
    """Views images"""

    title = 'View Image'

    init_inputs = [
        rc.NodeInputBP('Images', type_='data')
    ]
    color = '#000000'

    def __init__(self, params):
        super().__init__(params)
        self.hasRun = False

    def update_event(self, inp=-1):
        if self.hasRun == False and self.input(0)!=None:
            print("Viewing images")
            data = self.input(0)
            ImageViewer(self, data)
            self.run = True

class View_Header(rc.Node):
    """Views header information"""

    title = 'View header information'

    init_inputs = [
        rc.NodeInputBP('Headers', type_='data')
    ]

    color = '#000000'

    def __init__(self, params):
        super().__init__(params)
        self.hasRun = False

    def update_event(self, inp=-1):
        if self.hasRun == False and self.input(0)!=None:
            data = self.input(0)
            print("Viewing headers")
            HeaderViewer(self, data)
            self.run = True

class View_Numpy_Array(rc.Node):
    """Views numpy arrays"""

    title = 'View Numpy Arrays'

    init_inputs = [
        rc.NodeInputBP('Numpy Arrays', type_='data')
    ]
    color = '#000000'

    def __init__(self, params):
        super().__init__(params)
        self.hasRun = False

    def update_event(self, inp=-1):
        if self.hasRun == False and self.input(0)!=None:
            print("Viewing numpy arrays")
            data = self.input(0)
            ArrayViewer(self, data)
            self.run = True