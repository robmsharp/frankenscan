import glob

import SimpleITK as sitk
import cv2
import ryvencore_qt as rc
import torch
from torch.utils.data import Dataset, DataLoader, ConcatDataset
import numpy as np
import torch.nn as nn
from sklearn.metrics import accuracy_score, confusion_matrix

from frankenscan.controller.modules.selectFiles.selectFilesWidget import SelectFilesWidget

#Source: https://github.com/rehanfazalkhan/Brain-Tumor-Detection-using-Pytorch-CNN/blob/main/Brain_Tumor_Detection.ipynb
class CNN_Model(nn.Module):

    def __init__(self):
        super(CNN_Model,self).__init__()
        self.cnn_model = nn.Sequential(
            nn.Conv2d(in_channels=3, out_channels=6, kernel_size=5),
            nn.Tanh(),
            nn.AvgPool2d(kernel_size=2, stride=5),
            nn.Conv2d(in_channels=6, out_channels=16, kernel_size=5),
            nn.Tanh(),
            nn.AvgPool2d(kernel_size=2, stride=5))

        self.fc_model = nn.Sequential(
            nn.Linear(in_features=256, out_features=120),
            nn.Tanh(),
            nn.Linear(in_features=120, out_features=84),
            nn.Tanh(),
            nn.Linear(in_features=84, out_features=1))

    def forward(self, x):
        x = self.cnn_model(x)
        x = x.view(x.size(0), -1)
        x = self.fc_model(x)
        x = torch.sigmoid(x)

        return x


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

class Train_Model(rc.Node):
    """Trains the model on the data and outputs the trained model"""

    title = 'Train model'

    init_inputs = [
        rc.NodeInputBP('Untrained model', type_='data'),
        rc.NodeInputBP('Dataloader', type_='data')
    ]

    init_outputs = [
        rc.NodeOutputBP('Trained model', type_='data')
    ]

    color = '#000000'

    def __init__(self, params):
        super().__init__(params)
        self.hasRun = False

    def update_event(self, inp=-1):

        if self.hasRun == False and self.input(0)!=None and self.input(1)!=None:
            print("Training model")

            if torch.cuda.is_available():
                device = torch.device("cuda:0")

            else:
                device = torch.device("cpu")

            model = input(0).to(device)

            data = input(1)

            eta = 0.0001
            EPOCH = 400
            optimizer = torch.optim.Adam(model.parameters(), lr=eta)
            dataloader = DataLoader(data, batch_size=32, shuffle=True)
            model.train()

            for epoch in range(1, EPOCH):
                losses = []
                for D in dataloader:
                    optimizer.zero_grad()
                    data = D['image'].to(device)
                    label = D['label'].to(device)
                    y_hat = model(data)
                    # define loss function
                    error = nn.BCELoss()
                    loss = torch.sum(error(y_hat.squeeze(), label))
                    loss.backward()
                    optimizer.step()
                    losses.append(loss.item())
                if (epoch+1) % 10 == 0:
                    print('Train Epoch: {}\tLoss: {:.6f}'.format(epoch+1, np.mean(losses)))

            print("Outputting trained model")
            self.set_output_val(0, model)
            self.hasRun = True

class Test_Model(rc.Node):
    """Trains the model on the data and outputs the trained model"""

    title = 'Train model'

    init_inputs = [
        rc.NodeInputBP('Trained model', type_='data'),
        rc.NodeInputBP('Dataloader', type_='data')
    ]

    init_outputs = [
        rc.NodeOutputBP('Predicted labels', type_='data'),
        rc.NodeOutputBP('True labels', type_='data')
    ]

    color = '#000000'

    def __init__(self, params):
        super().__init__(params)
        self.hasRun = False

    def update_event(self, inp=-1):

        if self.hasRun == False and self.input(0)!=None and self.input(1)!=None:
            model = self.input(0)
            data = self.input(1)
            model.eval()
            dataloader = DataLoader(data, batch_size=32, shuffle=False)
            outputs=[]
            y_true = []

            if torch.cuda.is_available():
                device = torch.device("cuda:0")

            else:
                device = torch.device("cpu")

            with torch.no_grad():
                for D in dataloader:
                    image =  D['image'].to(device)
                    label = D['label'].to(device)

                    y_hat = model(image)

                    outputs.append(y_hat.cpu().detach().numpy())
                    y_true.append(label.cpu().detach().numpy())

            outputs = np.concatenate( outputs, axis=0 ).squeeze()
            y_true = np.concatenate( y_true, axis=0 ).squeeze()

            threshold=0.50
            minimum=0
            maximum = 1.0
            predicted = np.array(list(outputs))
            predicted[predicted >= threshold] = maximum
            predicted[predicted < threshold] = minimum

            self.set_output_val(0, outputs)
            self.set_output_val(1, y_true)
            self.hasRun = True

class Evaluate_Accuracy(rc.Node):
    """Evaluates the accuracy of the predictions"""

    title = 'Evaluate Accuracy'

    init_inputs = [
        rc.NodeInputBP('Predicted labels', type_='data'),
        rc.NodeInputBP('True labels', type_='data')
    ]

    init_outputs = [
        rc.NodeOutputBP('Accuracy score', type_='data')
    ]

    color = '#000000'

    def __init__(self, params):
        super().__init__(params)
        self.hasRun = False

    def update_event(self, inp=-1):

        if self.hasRun == False and self.input(0)!=None and self.input(1)!=None:
            y_true = self.input(1)
            predicted = self.input(0)
            answer = accuracy_score(y_true, predicted)
            self.set_output_val(0, answer)
            self.hasRun = True

#TODO: remove this
#Note uses hard coded files to save time
#Will not work on other computers
class Dummy_Data_Loader(rc.Node):
    """Loads data and creates labels"""

    title = 'Loads data and creates labels'

    init_outputs = [
        rc.NodeOutputBP('Data loader', type_='data')
    ]

    color = '#000000'

    def __init__(self, params):
        super().__init__(params)
        self.hasRun = False

    def update_event(self, inp=-1):

        if self.hasRun == False:

            healthy = []

            tumor = []

            #Source: https://github.com/MLDawn/MLDawn-Projects/blob/main/Pytorch/Brain-Tumor-Detector/MRI-Brain-Tumor-Detecor.ipynb
            for f in glob.iglob("C:/Users/Robert/IdeaProjects/frankenscan/data/yes/*.jpg"):
                img = cv2.imread(f)
                img = cv2.resize(img,(128,128))
                b, g, r = cv2.split(img)
                img = cv2.merge([r,g,b])
                img = img/255.0
                tumor.append(img)

            for f in glob.iglob("C:/Users/Robert/IdeaProjects/frankenscan/data/no/*.jpg"):
                img = cv2.imread(f)
                img = cv2.resize(img,(128,128))
                b, g, r = cv2.split(img)
                img = cv2.merge([r,g,b])
                img = img/255.0
                healthy.append(img)

            print("Creating dummy data loader")

            dataLoader = MRI(healthy, tumor)

            print("Updating data loader node outputs")
            self.set_output_val(0, dataLoader)
            self.hasRun = True


class CNN(rc.Node):
    """Loads data and creates labels"""

    title = 'Creates model for convolutional neural network'

    init_outputs = [
        rc.NodeOutputBP('Data loader', type_='data')
    ]

    color = '#000000'

    def __init__(self, params):
        super().__init__(params)
        self.hasRun = False

    def update_event(self, inp=-1):

        if self.hasRun == False:

            model = CNN_Model()

            print("Updating model output")
            self.set_output_val(0, model)
            self.hasRun = True


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
