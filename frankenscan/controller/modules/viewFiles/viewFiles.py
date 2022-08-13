import ryvencore_qt as rc

class View_Header(rc.Node):
    """Views header information"""

    title = 'View header information'

    init_inputs = [
        rc.NodeInputBP('Headers', type_='data')
    ]

    color = '#000000'

    main_widget_pos = 'between ports'

    def __init__(self, params):
        super().__init__(params)
        self.hasRun = False

    def update_event(self, inp=-1):
        if self.hasRun == False:
            self.run = True

class View_Numpy_Array(rc.Node):
    """Views numpy arrays"""

    title = 'View Numpy Arrays'

    init_inputs = [
        rc.NodeInputBP('Numpy Arrays', type_='data')
    ]
    color = '#000000'


    main_widget_pos = 'between ports'

    def __init__(self, params):
        super().__init__(params)
        self.hasRun = False

    def update_event(self, inp=-1):
        if self.hasRun == False:
            self.run = True