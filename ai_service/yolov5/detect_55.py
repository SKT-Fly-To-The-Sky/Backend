import argparse
import os
from pathlib import Path

import torch
import torch.backends.cudnn as cudnn
from numpy import random
from PIL import Image
import cv2
from ai_service.yolov5.models.experimental import attempt_load
from ai_service.yolov5.utils.general import check_img_size, non_max_suppression
from ai_service.yolov5.utils.torch_utils import select_device
from ai_service.yolov5.models.yolo import yolo_head
from ai_service.yolov5.utils.general import non_max_suppression
from ai_service.yolov5.utils.torch_utils import select_device

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
    weights = 'yolov5s.pt'  # path to the weights file
    device = select_device('')  # set device to default
    model = torch.load(weights, map_location=device)['model'].float()  # load model
    model.to(device).eval()  # set device and model to evaluation mode
    imgsz = check_img_size(640, s=model.stride.max())  # check image size
    half = device.type != 'cpu'  # set half precision

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
            pred = model(img)
            det = yolo_head(pred, anchors, 80, imgsz)  # YOLO head operation
            det = non_max_suppression(det, conf_thres=0.25, iou_thres=0.45)

        # Process detections
        results = []
        for i, det in enumerate(det):  # detections per image
            if det is not None and len(det):
                det[:, :4] = scale_coords(img.shape[2:], det[:, :4], img.shape[2:]).round()  # rescale boxes
                for *xyxy, conf, cls in reversed(det):
                    label = f'{classes[int(cls)]} {conf:.2f}'
                    results.append({'bbox': xyxy, 'class': classes[int(cls)], 'conf': conf})

        return results

    # Load image
    img0 = cv2.imread(image_path)  # BGR format

    # Inference
    img = img0[:, :, ::-1]  # RGB format
    results = run_inference(img)

    return results

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--image_path', type=str, required=True, help='path to image file')
    args = parser.parse_args()
    detect_ljs(args.image_path)

