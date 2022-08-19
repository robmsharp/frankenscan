import SimpleITK as sitk
import cv2
import ryvencore_qt as rc

from frankenscan.controller.modules.selectFiles.selectFilesWidget import SelectFilesWidget

class Read_Image_Files(rc.Node):
    """Reads NIFTI (.nii) files into headers and numpy arrays"""

    title = 'Read image files'

    init_inputs = [
        rc.NodeInputBP('Selected image files', type_='data')
    ]

    init_outputs = [
        rc.NodeOutputBP('Image data', type_='data')
    ]

    color = '#000000'

    def __init__(self, params):
        super().__init__(params)
        self.hasRun = False

    def update_event(self, inp=-1):

        if self.hasRun == False and self.input(0)!=None:
            print("Reading selected image files")

            #Read the files
            images = []

            #Get the selected files
            selectedFiles = self.input(0)

            for file in selectedFiles:
                #Source: https://github.com/MLDawn/MLDawn-Projects/blob/main/Pytorch/Brain-Tumor-Detector/MRI-Brain-Tumor-Detecor.ipynb
                img = cv2.imread(file)
                b, g, r = cv2.split(img)
                img = cv2.merge([r,g,b])
                images.append(img)

            print("Updating read image node outputs")
            self.set_output_val(0, images)
            self.hasRun = True

class Read_nii_Files(rc.Node):
    """Reads NIFTI (.nii) files into headers and numpy arrays"""

    title = 'Read NIFTI (.nii) files'

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

        if self.hasRun == False and self.input(0)!=None:
            print("Reading selected .nii files")

            #Read the files
            headers = []
            arrays = []

            #Get the selected files
            selectedFiles = self.input(0)

            for file in selectedFiles:
                #Ensure file type is correct
                assert(file[-3:].lower() == "nii")

                # Read the .nii image containing the volume with SimpleITK:
                data = sitk.ReadImage(file)

                listOfMetaInformation = []
                for key in data.GetMetaDataKeys():
                    listOfMetaInformation.append(str(key)+": "+str(data.GetMetaData(key)))

                #Access the numpy array:
                array = sitk.GetArrayFromImage(data)
                header = listOfMetaInformation

                arrays.append(array)
                headers.append(header)

            print("Updating read files node outputs")
            self.set_output_val(1, arrays)
            self.set_output_val(0, headers)
            self.hasRun = True