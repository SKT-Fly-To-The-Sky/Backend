import argparse
import os
from pathlib import Path

import torch
import torch.backends.cudnn as cudnn
from numpy import random
from PIL import Image

from ai_service.yolov5.models.experimental import attempt_load
from ai_service.yolov5.utils.general import check_img_size, non_max_suppression, scale_coords
from ai_service.yolov5.utils.plots import plot_one_box
from ai_service.yolov5.utils.torch_utils import select_device


def detect_ljs(image_path):
    weights = './ai_service/yolov5/best_hoon.pt'  # path to the weights file
    device = select_device('')  # set device to default
    model = attempt_load(weights, device)  # load model
    imgsz = check_img_size(640, s=model.stride.max())  # check image size
    half = device.type != 'cpu'  # set half precision to True if using GPU
    if half:
        model.half()  # convert to half precision
    img = Image.open(image_path)  # load image
    img_tensor = torch.from_numpy(img).to(device)  # convert image to tensor
    img_tensor = img_tensor.half() if half else img_tensor.float()  # convert to half precision if necessary
    img_tensor /= 255.0  # normalize pixel values
    if img_tensor.ndimension() == 3:
        img_tensor = img_tensor.unsqueeze(0)  # add batch dimension if necessary
    pred = model(img_tensor)[0]  # make prediction
    pred = non_max_suppression(pred, 0.4, 0.5)  # apply non-max suppression
    result = []
    for det in pred:
        if det is not None and len(det):
            det[:, :4] = scale_coords(img_tensor.shape[2:], det[:, :4], img.size).round()
            for *xyxy, conf, cls in reversed(det):
                result.append((int(xyxy[0]), int(xyxy[1]), int(xyxy[2]), int(xyxy[3]), conf, cls))
                label = f'{model.names[int(cls)]} {conf:.2f}'
                plot_one_box(xyxy, img, label=label, color=random.choice(colors), line_thickness=3)
    return result
if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--image_path', type=str, required=True, help='path to image file')
    args = parser.parse_args()
    detect(args.image_path)

