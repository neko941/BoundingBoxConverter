# Usage
## Convert BoundingBox from YOLO format to Pascal VOC format 
```
BoundingBoxConverter().addBoundingBox(format="YOLO", labelPath="/content/Pixiv-84247796_p0.txt").addImageShape(imagePath="/content/Pixiv-84247796_p0.png").export(format="PascalVOC")
```
## Convert BoundingBox from Pascal VOC format to YOLO format and save annotation to a file
```
BoundingBoxConverter().addClasses(["without_mask", "with_mask"]).addBoundingBox(format="Pascal VOC", labelFilePath="/content/maksssksksss0.xml").export(format="YOLO", save=True)
```
