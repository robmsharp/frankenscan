import SimpleITK as sitk
import cv2
import ryvencore_qt as rc

from frankenscan.controller.modules.selectFiles.selectFilesWidget import SelectFilesWidget

class Rescale_Image_Files(rc.Node):
    """Rescales the image files"""

    title = 'Rescale image files'

    init_inputs = [
        rc.NodeInputBP('Image data', type_='data')
    ]

    init_outputs = [
        rc.NodeOutputBP('Rescaled image data', type_='data')
    ]

    color = '#000000'

    def __init__(self, params):
        super().__init__(params)
        self.hasRun = False

    def update_event(self, inp=-1):

        if self.hasRun == False and self.input(0)!=None:
            print("Rescaling image files")

            #Read the files
            images = []

            #Get the selected files
            originalImages = self.input(0)

            for image in originalImages:
                #Source: https://github.com/MLDawn/MLDawn-Projects/blob/main/Pytorch/Brain-Tumor-Detector/MRI-Brain-Tumor-Detecor.ipynb
                rescaledImage = cv2.resize(image,(128,128))
                images.append(rescaledImage)

            print("Updating rescale image node outputs")
            self.set_output_val(0, images)
            self.hasRun = True
