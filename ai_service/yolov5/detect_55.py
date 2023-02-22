import argparse
import os
from pathlib import Path

import torch
import torch.backends.cudnn as cudnn
import numpy as np
from numpy import random
from PIL import Image
import cv2
from ai_service.yolov5.models.experimental import attempt_load
from ai_service.yolov5.utils.general import check_img_size, non_max_suppression
from ai_service.yolov5.utils.torch_utils import select_device
from ai_service.yolov5.utils.general import non_max_suppression
from ai_service.yolov5.utils.torch_utils import select_device
from ai_service.yolov5.utils.augmentations import letterbox

def scale_coords(img_shape, coords, im_shape):
    # Rescale x, y, w, h from [0, 1] to image dimensions
    h, w = img_shape
    gain_w = float(w) / im_shape[0]
    gain_h = float(h) / im_shape[1]
    gain = min(gain_w, gain_h)
    pad_w = (w - im_shape[0] * gain) / 2
    pad_h = (h - im_shape[1] * gain) / 2
    coords[:, 0] = (coords[:, 0] * gain + pad_w).round()
    coords[:, 1] = (coords[:, 1] * gain + pad_h).round()
    coords[:, 2] = (coords[:, 2] * gain + pad_w).round()
    coords[:, 3] = (coords[:, 3] * gain + pad_h).round()
    return coords

def plot_one_box(x, img, color=None, label=None, line_thickness=None):
    tl = line_thickness or round(0.002 * (img.shape[0] + img.shape[1]) / 2) + 1
    c1, c2 = (int(x[0]), int(x[1])), (int(x[2]), int(x[3]))
    cv2.rectangle(img, c1, c2, color, thickness=tl, lineType=cv2.LINE_AA)
    if label:
        tf = max(tl - 1, 1)
        t_size = cv2.getTextSize(label, 0, fontScale=tl / 3, thickness=tf)[0]
        c2 = c1[0] + t_size[0], c1[1] - t_size[1] - 3
        cv2.rectangle(img, c1, c2, color, -1, cv2.LINE_AA)  # filled
        cv2.putText(img, label, (c1[0], c1[1] - 2), 0, tl / 3, [225, 255, 255], thickness=tf, lineType=cv2.LINE_AA)

def detect_ljs(image_path):
    weights = './ai_service/yolov5/yolov5s.pt'  # path to the weights file
    device = select_device('')  # set device to default
    model = attempt_load(weights, device)  # load model
    imgsz = check_img_size(640, s=model.stride.max())  # check image size
    half = device.type != 'cpu'  # set half precision
    classes = model.names

    if half:
        model.half()  # convert model to half-precision floating point for faster inference

    # Define detect function
    def run_inference(img):
        img = torch.from_numpy(img).to(device)  # convert to tensor
        img = img.half() if half else img.float()  # convert to half-precision floating point if needed
        img /= 255.0  # normalize pixel values to [0, 1]
        if img.ndimension() == 3:
            img = img.unsqueeze(0)

        # Inference
        with torch.no_grad():
            pred = model(img, augment=False)[0]  # run inference

        # Apply NMS
        pred = non_max_suppression(pred, conf_thres=0.25, iou_thres=0.45, classes=None, agnostic=False)

        return pred[0] if len(pred) else None

    # Load image
    img0 = cv2.imread(image_path)  # load image using OpenCV
    img = img0[:, :, ::-1]  # BGR to RGB
    img = letterbox(img, new_shape=imgsz)[0]  # resize image to model input size while maintaining aspect ratio
    img = img.transpose(2, 0, 1)  # convert to tensor format
    img = np.ascontiguousarray(img)

    # Run inference
    pred = run_inference(img)

    # Process detection results
    if pred is not None:
        # Rescale coordinates to original image size
        pred[:, :4] = scale_coords(img.shape[2:], pred[:, :4], img0.shape).round()

        # Extract box coordinates, confidence scores, and class IDs
        boxes = pred[:, :4].astype(int)
        scores = pred[:, 4]
        class_ids = pred[:, 5].astype(int)

        # Print results
        for i, (box, score, class_id) in enumerate(zip(boxes, scores, class_ids)):
            print(f'Box {i}: {box}, Class: {classes[class_id]}, Confidence: {score}')

    else:
        print('No objects detected.')


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--image_path', type=str, required=True, help='path to image file')
    args = parser.parse_args()
    detect_ljs(args.image_path)

