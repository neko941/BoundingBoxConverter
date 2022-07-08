import cv2
import numpy as np

class BoundingBoxConverter():
    def __init__(self) -> None:
        """ Pascal VOC """
        self.xTopLefts = []
        self.yTopLefts = []
        self.xBottomRights = []
        self.yBottomRights = []

        """ YOLO """
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
        self.labelPath = None

        self.xCenters = None
        self.yCenter = None

    def YOLO_to_PascalVOC(self):
        self.xTopLefts.extend([0 if (x - w / 2) * self.width < 0 else int((x - w / 2) * self.width) + 1 for x, w in zip(self.xCenterScaled, self.widthScaled)])
        self.xBottomRights.extend([self.width - 1 if (x + w / 2) * self.width > self.width - 1 else int((x + w / 2) * self.width) + 1 for x, w in zip(self.xCenterScaled, self.widthScaled)])
        self.yTopLefts.extend([0 if (y - h / 2) * self.height < 0 else int((y - h / 2) * self.height) + 1 for y, h in zip(self.yCenterScaled, self.heightScaled)])
        self.yBottomRights.extend([self.height - 1 if (y + h / 2) * self.height > self.height - 1 else int((y + h / 2) * self.height) + 1 for y, h in zip(self.yCenterScaled, self.heightScaled)])

    def addBoundingBox(self, format, labelPath=None):
        if format.lower() == "yolo":
            if labelPath and labelPath.endswith(".txt"):
                self.labelPath = labelPath
                lines = open(labelPath, "r").readlines()
                lines = np.array([line.strip().split(" ") for line in lines], dtype=float)

                self.labels.extend([int(label) for label in lines[:, 0]])
                self.xCenterScaled.extend(lines[:, 1])
                self.yCenterScaled.extend(lines[:, 2])
                self.widthScaled.extend(lines[:, 3])
                self.heightScaled.extend(lines[:, 4])

        return self

    def addImageShape(self, imagePath=None, size=None):
        if imagePath:
            img = cv2.imread(imagePath)[:,:,::-1]
            self.width, self.height = img.shape[1], img.shape[0]

        if size:
            self.width = size[0]
            self.height = size[1]
        
        return self

    def export(self, format):
        if format.lower() == "pascalvoc":
            if  all([self.xCenterScaled, self.yCenterScaled, self.widthScaled, self.heightScaled]):
                self.YOLO_to_PascalVOC()
            return [(x1, y1, x2, y2) for x1, y1, x2, y2 in zip(self.xTopLefts, self.yTopLefts, self.xBottomRights, self.yBottomRights)]
