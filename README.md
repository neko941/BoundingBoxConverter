# 1.Installation
```
!git clone https://github.com/neko941/BoundingBoxConverter
```
```
!pip install -r BoundingBoxConverter/requirements.txt
```

# 2.File Format

![image](https://user-images.githubusercontent.com/42170045/178405899-a89586cb-e68f-46fe-9cad-e8f482e6c64c.png)


### YOLO
File: `*.txt`  
Content:
```
2 0.181640625 0.33469945355191255 0.05859375 0.10109289617486339
0 0.3994140625 0.33060109289617484 0.080078125 0.12021857923497267
2 0.6669921875 0.3128415300546448 0.068359375 0.13934426229508196
```
```
<label> <xCenterScaled> <yCenterScaled> <widthScaled> <heightScaled>  
```


# 3. Usage
```python
from BoundingBoxConverter.BoundingBoxConverter import BoundingBoxConverter
```
### Convert BoundingBox from YOLO format to Pascal VOC format 
```python
obj, bbox = BoundingBoxConverter().addBoundingBox(format="YOLO", labelFilePath="/content/Pixiv-84247796_p0.txt").addImageShape(imagePath="/content/Pixiv-84247796_p0.png").export(format="PascalVOC")
```
```python
obj = BoundingBoxConverter()
obj.addBoundingBox(format="YOLO", bbox=["2 0.485802 0.230366 0.258025 0.218150", "3 0.5802 0.2303 0.2525 0.2180"])
obj.addImageShape(imagePath="/content/Pixiv-84247796_p0.png")
obj, bbox = obj.export(format="PascalVOC")
```
```python
obj = BoundingBoxConverter()
obj.addBoundingBox(format="YOLO", bbox=[[2, 0.485802, 0.230366, 0.258025, 0.218150], [3, 0.5802, 0.2303, 0.2525, 0.2180]])
obj.addImageShape(imagePath="/content/Pixiv-84247796_p0.png")
obj, bbox = obj.export(format="PascalVOC")
```
### Convert BoundingBox from Pascal VOC format to YOLO format and save annotation to a file
```python
obj, bbox = BoundingBoxConverter().addClasses(["without_mask", "with_mask"]).addBoundingBox(format="Pascal VOC", labelFilePath="/content/maksssksksss0.xml").export(format="YOLO", save=True)
```
