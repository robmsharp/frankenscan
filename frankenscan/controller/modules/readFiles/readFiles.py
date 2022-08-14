import SimpleITK as sitk
import ryvencore_qt as rc

from frankenscan.controller.modules.selectFiles.selectFilesWidget import SelectFilesWidget

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