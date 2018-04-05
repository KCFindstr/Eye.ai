from PIL import Image
from detection_inference_api import ObjectDetection

image_path = "image_test.jpeg"
image = Image.open(image_path)
image.load()

detection = ObjectDetection()
result = detection.detect_boundingbox(image)