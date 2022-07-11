import cv2
import numpy as np
from pathlib import Path
from xml.dom import minidom

class BoundingBoxConverter():
    def __init__(self) -> None:
        """ Pascal VOC Format """
        self.xTopLefts = []
        self.yTopLefts = []
        self.xBottomRights = []
        self.yBottomRights = []

        """ YOLO Format """
        self.xCenterScaled = []
        self.yCenterScaled = []
        self.widthScaled = []
        self.heightScaled = []

        """ Image """
        self.width = None
        self.height = None
        self.imagePath = None

        """ Label """
        self.labels = []
        self.classes = []
        self.labelFilePath = None
        self.labelFileName = None

    def YOLO_to_PascalVOC(self):
        self.xTopLefts.extend([0 if (x - w / 2) * self.width < 0 else int((x - w / 2) * self.width) + 1 for x, w in zip(self.xCenterScaled, self.widthScaled)])
        self.xBottomRights.extend([self.width - 1 if (x + w / 2) * self.width > self.width - 1 else int((x + w / 2) * self.width) + 1 for x, w in zip(self.xCenterScaled, self.widthScaled)])
        self.yTopLefts.extend([0 if (y - h / 2) * self.height < 0 else int((y - h / 2) * self.height) + 1 for y, h in zip(self.yCenterScaled, self.heightScaled)])
        self.yBottomRights.extend([self.height - 1 if (y + h / 2) * self.height > self.height - 1 else int((y + h / 2) * self.height) + 1 for y, h in zip(self.yCenterScaled, self.heightScaled)])

    def PascalVOC_to_YOLO(self):
        self.xCenterScaled.extend([((x1 + x2)/2.0 - 1) * (1./self.width) for x1, x2 in zip(self.xTopLefts, self.xBottomRights)])
        self.yCenterScaled.extend([(x2 - x1) * (1./self.width) for x1, x2 in zip(self.xTopLefts, self.xBottomRights)])
        self.widthScaled.extend([((y1 + y2)/2.0 - 1) * (1./self.height) for y1, y2 in zip(self.yTopLefts, self.yBottomRights)])
        self.heightScaled.extend([(y2 - y1) * (1./self.width) for y1, y2 in zip(self.yTopLefts, self.yBottomRights)])

    def addBoundingBox(self, format, labelFilePath=None):
        self.labelFilePath = labelFilePath
        self.labelFileName = Path(labelFilePath).stem

        if format.lower().replace(" ", "") == "yolo":
            if labelFilePath and labelFilePath.endswith(".txt"):
                lines = open(labelFilePath, "r").readlines()
                lines = np.array([line.strip().split(" ") for line in lines], dtype=float)

                self.labels.extend([int(label) for label in lines[:, 0]])
                self.xCenterScaled.extend(lines[:, 1])
                self.yCenterScaled.extend(lines[:, 2])
                self.widthScaled.extend(lines[:, 3])
                self.heightScaled.extend(lines[:, 4])
        
        elif format.lower().replace(" ", "") == "pascalvoc":
            if labelFilePath and labelFilePath.endswith(".xml"):
                file = minidom.parse(labelFilePath)
                
                self.labels.extend([l.firstChild.data for l in list(file.getElementsByTagName('name'))])
                self.xTopLefts.extend([int(x1.firstChild.data) for x1 in list(file.getElementsByTagName('xmin'))])
                self.yTopLefts.extend([int(y1.firstChild.data) for y1 in list(file.getElementsByTagName('ymin'))])
                self.xBottomRights.extend([int(x2.firstChild.data) for x2 in list(file.getElementsByTagName('xmax'))])
                self.yBottomRights.extend([int(y2.firstChild.data) for y2 in list(file.getElementsByTagName('ymax'))])

                self.width = int(list(file.getElementsByTagName('width'))[0].firstChild.data)
                self.height = int(list(file.getElementsByTagName('height'))[0].firstChild.data)

        return self

    def addImageShape(self, imagePath=None, size=None):
        if imagePath:
            img = cv2.imread(imagePath)[:,:,::-1]
            self.width, self.height = img.shape[1], img.shape[0]

        if size:
            self.width = size[0]
            self.height = size[1]
        
        return self

    def save(self, format):
        if format.lower() == "yolo":
            file = open(f"{self.labelFileName}.txt", "w")
            file.writelines([f"{l} {x} {y} {w} {h}\n" for l, x, y, w, h in zip(self.labels, self.xCenterScaled, self.yCenterScaled, self.widthScaled, self.heightScaled)])

    def addClasses(self, classes):
        self.classes.extend(classes)
        return self

    def retrieveLabelIndex(self, label):
        return self.classes.index(label)

    def export(self, format, save=False):
        if format.lower() == "pascalvoc":
            assert (all([self.width, self.height, self.xCenterScaled, self.yCenterScaled, self.widthScaled, self.heightScaled]))
            self.YOLO_to_PascalVOC()
            return self, [(x1, y1, x2, y2) for x1, y1, x2, y2 in zip(self.xTopLefts, self.yTopLefts, self.xBottomRights, self.yBottomRights)]

        if format.lower() == "yolo":
            if all([self.xTopLefts, self.yTopLefts, self.xBottomRights, self.yBottomRights]):
                assert all([self.width, self.height, self.xTopLefts, self.yTopLefts, self.xBottomRights, self.yBottomRights])
                self.PascalVOC_to_YOLO()
                if save:
                    for index, l in enumerate(self.labels):
                        self.labels[index] = self.retrieveLabelIndex(l) 
                    self.save(format=format)
            return self, [(x, y, w, h) for x, y, w, h in zip(self.xCenterScaled, self.yCenterScaled, self.widthScaled, self.heightScaled)]
