import SimpleITK as sitk
import cv2
import ryvencore_qt as rc
import torch
from torch.utils.data import Dataset, DataLoader, ConcatDataset
import numpy as np

from frankenscan.controller.modules.selectFiles.selectFilesWidget import SelectFilesWidget

#This class extends pytorch class Dataset
class MRI(Dataset):
    def __init__(self,  healthy, tumor):

        reshapedTumor = []
        reshapedHealthy = []

        #Reshape as in tutoria: https://github.com/MLDawn/MLDawn-Projects/blob/main/Pytorch/Brain-Tumor-Detector/MRI-Brain-Tumor-Detecor.ipynb
        for tumorImage in tumor:
            reshapedTumorImage = tumorImage.reshape((tumorImage.shape[2],tumorImage.shape[0],tumorImage.shape[1]))
            reshapedTumor.append(reshapedTumorImage)

        for healthyImage in healthy:
            reshapedHealthyImage = healthyImage.reshape((healthyImage.shape[2],healthyImage.shape[0],healthyImage.shape[1]))
            reshapedHealthy.append(reshapedHealthyImage)

        # our images
        reshapedTumor = np.array(reshapedTumor,dtype=np.float32)
        reshapedHealthy = np.array(reshapedHealthy,dtype=np.float32)

        # our labels
        tumorLabel = np.ones(reshapedTumor.shape[0], dtype=np.float32)
        healthyLabel = np.zeros(reshapedHealthy.shape[0], dtype=np.float32)

        # Concatenates
        self.images = np.concatenate((reshapedTumor, reshapedHealthy), axis=0)
        self.labels = np.concatenate((tumorLabel, healthyLabel))

    def __len__(self):
        return self.images.shape[0]

    def __getitem__(self, index):

        sample = {'image': self.images[index], 'label':self.labels[index]}

        return sample

class Data_Loader(rc.Node):
    """Loads data and creates labels"""

    title = 'Loads data and creates labels'

    init_inputs = [
        rc.NodeInputBP('Healthy image data', type_='data'),
        rc.NodeInputBP('Tumour image data', type_='data')
    ]

    init_outputs = [
        rc.NodeOutputBP('Data loader', type_='data')
    ]

    color = '#000000'

    def __init__(self, params):
        super().__init__(params)
        self.hasRun = False

    def update_event(self, inp=-1):

        if self.hasRun == False and self.input(0)!=None and self.input(1)!=None:
            print("Creating data loader")

            dataLoader = MRI(self.input(0), self.input(1))

            print("Updating data loader node outputs")
            self.set_output_val(0, dataLoader)
            self.hasRun = True
