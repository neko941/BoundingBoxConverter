# Installation
```
!git clone https://github.com/neko941/BoundingBoxConverter
```
```
!pip install -r BoundingBoxConverter/requirements.txt
```
```python
from BoundingBoxConverter.BoundingBoxConverter import BoundingBoxConverter
```

# Usage
## Convert BoundingBox from YOLO format to Pascal VOC format 
```python
obj, bbox = BoundingBoxConverter().addBoundingBox(format="YOLO", labelFilePath="/content/Pixiv-84247796_p0.txt").addImageShape(imagePath="/content/Pixiv-84247796_p0.png").export(format="PascalVOC")
```
## Convert BoundingBox from Pascal VOC format to YOLO format and save annotation to a file
```python
obj, bbox = BoundingBoxConverter().addClasses(["without_mask", "with_mask"]).addBoundingBox(format="Pascal VOC", labelFilePath="/content/maksssksksss0.xml").export(format="YOLO", save=True)
```
