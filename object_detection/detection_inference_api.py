import tensorflow as tf
import numpy as np
from PIL import Image
import os

from utils import label_map_util

# Truncate any detection that has confidence level under MIN_CONFID
MIN_CONFID = 0.8

# List of strings used to add correct label for each box
PATH_TO_LABELS = os.path.join('data', 'mscoco_label_map.pbtxt')
NUM_CLASSES = 90
IMAGE_SIZE = (20, 16)

label_map = label_map_util.load_labelmap(PATH_TO_LABELS)
categories = label_map_util.convert_label_map_to_categories(label_map, max_num_classes=NUM_CLASSES, use_display_name=True)
category_index = label_map_util.create_category_index(categories)


# API
class ObjectDetection(object):
    def __init__(self):
        PATH_TO_MODEL = 'frozen_inference_graph.pb'
        self.detection_graph = tf.Graph()
        
        with self.detection_graph.as_default():
            od_graph_def = tf.GraphDef()
            
            with tf.gfile.GFile(PATH_TO_MODEL, 'rb') as fid:
                serialized_graph = fid.read()
                od_graph_def.ParseFromString(serialized_graph)
                tf.import_graph_def(od_graph_def, name='')
                
    def detect_boundingbox_inference(self, image):
        with self.detection_graph.as_default():
            with tf.Session() as sess:
                # Get handles to input and output tensors
                ops = tf.get_default_graph().get_operations()
                all_tensor_names = {output.name for op in ops for output in op.outputs}
                tensor_dict = {}
                for key in [
                    'num_detections', 'detection_boxes', 'detection_scores',
                    'detection_classes',
                ]:
                    tensor_name = key + ':0'
                    if tensor_name in all_tensor_names:
                        tensor_dict[key] = tf.get_default_graph().get_tensor_by_name(tensor_name)
                        
                image_tensor = tf.get_default_graph().get_tensor_by_name('image_tensor:0')
                
                # Run inference
                output_dict = sess.run(tensor_dict,
                                       feed_dict={image_tensor: np.expand_dims(image, 0)})

                # all outputs are float32 numpy arrays, so convert types as appropriate
                output_dict['num_detections'] = int(output_dict['num_detections'][0])
                output_dict['detection_classes'] = output_dict[
                    'detection_classes'][0].astype(np.uint8)
                output_dict['detection_boxes'] = output_dict['detection_boxes'][0]
                output_dict['detection_scores'] = output_dict['detection_scores'][0]
                
        return output_dict
    
    def detect_boundingbox_convert(self, output_dict):
        # Convert label_map to indexed category
        categories = label_map_util.convert_label_map_to_categories(label_map, NUM_CLASSES)
        category_index = label_map_util.create_category_index(categories)
                
        # Convert output_dict to API format dictionary
        results = []
        for n in range(output_dict['num_detections']):
            result = {}
            result["name"] = category_index[output_dict["detection_classes"][n]]["name"]
            result["top_left_position"] = (output_dict["detection_boxes"][n][0], output_dict["detection_boxes"][n][1])
            result["bottom_right_position"] = (output_dict["detection_boxes"][n][2], output_dict["detection_boxes"][n][3])
            result["confidence"] = output_dict["detection_scores"][n]
            results.append(result)
                 
        return results
    
    def detect_boundingbox(self, image):
        # Convert image to numpy array
        image_np = np.asarray(image, dtype='int32')
        
        # Call inference function
        output_dict = self.detect_boundingbox_inference(image_np)
        # Convert output_dict to API format
        results = self.detect_boundingbox_convert(output_dict)
        
        # Truncate any detection that has confidence level under MIN_CONFID
        truncated_results = []
        for result in results:
            if result["confidence"] > MIN_CONFID:
                truncated_results.append(result)
        
        return truncated_results
    
