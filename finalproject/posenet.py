from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import argparse
import io
import time
import numpy as np
import picamera

from PIL import Image
from tflite_runtime.interpreter import Interpreter

import numpy as np
import tflite_runtime.interpreter as tflite


# Dictionary mapping name of body part to its index
indexOf = {
    "nose" : 0,
	"leftEye" : 1,
	"rightEye" : 2,
	"leftEar" : 3,
	"rightEar" : 4,
	"leftShoulder" : 5,
	"rightShoulder" : 6,
	"leftElbow" : 7,
	"rightElbow" : 8,
	"leftWrist" : 9,
	"rightWrist" : 10, 
	"leftHip" : 11,
	"rightHip" : 12,
	"leftKnee" : 13,
	"rightKnee" : 14,
	"leftAnkle" : 15,
	"rightAnkle" : 16
}


class Position: 
	x = 0
	y = 0

class KeyPoint:
	bodyPart = indexOf["nose"]
	position = Position()
	score = 0.0

class Person: 
	keyPoints = []   # To add, keyPoints.append("KP")
	score = 0.0


def set_input_tensor(interpreter, image):
	tensor_index = interpreter.get_input_details()[0]['index']
	input_tensor = interpreter.tensor(tensor_index)()[0]
	input_tensor[:, :] = image

def detect_positions(interpreter, image, top_k=1):
	set_input_tensor(interpreter, image)
	interpreter.invoke()
	output_details = interpreter.get_output_details()[0]
	# for i in range(len(interpreter.get_output_details())):
	# 	print(interpreter.get_output_details()[i]['shape'])


	output = np.squeeze(interpreter.get_tensor(output_details['index']))
	ordered = np.argpartition(-output, top_k)
	print(output[2])
	print(ordered[2])

	return [(i, output[i]) for i in range(9)]


def init_output_map(interpreter):
	output_map = {}

	output_details = interpreter.get_output_details()

	# Heatmaps 1x9x9x17
	output_map[0] = np.zeros((output_details[0]['shape'][0], output_details[0]['shape'][1], output_details[0]['shape'][2], output_details[0]['shape'][3]))

	# Offsets  1x9x9x34
	output_map[1] = np.zeros((output_details[1]['shape'][0], output_details[1]['shape'][1], output_details[1]['shape'][2], output_details[1]['shape'][3]))

	# Forward Displacements
	#          1x9x9x32
	output_map[2] = np.zeros((output_details[2]['shape'][0], output_details[2]['shape'][1], output_details[2]['shape'][2], output_details[2]['shape'][3]))

	# Backward Displacements
	#          1x9x9x32
	output_map[3] = np.zeros((output_details[3]['shape'][0], output_details[3]['shape'][1], output_details[3]['shape'][2], output_details[3]['shape'][3]))

	return output_map

kp = KeyPoint()
print (kp.bodyPart)
print (kp.position.x)

def main():
	parser = argparse.ArgumentParser(
		formatter_class=argparse.ArgumentDefaultsHelpFormatter)
	parser.add_argument(
		'--model', help='File path of .tflite file.', required=False)
	parser.add_argument(
		'--labels', help='File path of labels file.', required=False)
	args = parser.parse_args()

	# labels = load_labels(args.labels)


	# Load TFLite model and allocate tensors.
	interpreter = tflite.Interpreter(model_path="./posenet_mobilenet_v1_100_257x257_multi_kpt_stripped.tflite")
	interpreter.allocate_tensors()

	# Get input tensors.
	input_details = interpreter.get_input_details()
	_, height, width, _ = input_details[0]['shape']

	# Test model on random input data.
	input_shape = input_details[0]['shape']
	# input_data = np.array(np.random.random_sample(input_shape), dtype=np.float32)
	# interpreter.set_tensor(input_details[0]['index'], input_data)

	# # Create an array representing a 1280x720 image of
	# # a cross through the center of the display. The shape of
	# # the array must be of the form (height, width, color)
	# a = np.zeros((640, 480, 3), dtype=np.uint8)
	# a[320, :, :] = 0xff
	# a[:, 240, :] = 0xff
	output = init_output_map(interpreter)

	with picamera.PiCamera(resolution=(640, 480), framerate=30) as camera:
		camera.start_preview()
		# o = camera.add_overlay(a.tobytes(), layer=3, alpha=64)

		try:
			stream = io.BytesIO()
			for _ in camera.capture_continuous(
				stream, format='jpeg', use_video_port=True):
				stream.seek(0)
				image = Image.open(stream).convert('RGB').resize((width, height),
																Image.ANTIALIAS)
				start_time = time.time()
				results = detect_positions(interpreter, image)
				elapsed_ms = (time.time() - start_time) * 1000
				label_id, prob = results[0]
				stream.seek(0)
				stream.truncate()
				camera.annotate_text = '%s \n%.1fms' % (label_id,
														elapsed_ms)

		finally:
			camera.stop_preview()


if __name__ == '__main__':
  main()
