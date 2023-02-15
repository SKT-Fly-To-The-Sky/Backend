# -*-coding:utf-8-*-
import sys
# sys.path.append('/workspace/ai_service/yolo3/')
# sys.path.append('/workspace/ai_service/yolo3/utils/')
import argparse


from ai_service.yolov3.utils.models import *  # set ONNX_EXPORT in models.py
from ai_service.yolov3.utils.datasets import *
from ai_service.yolov3.utils.utils import *

from xml.etree.ElementTree import Element, SubElement, ElementTree
import numpy as np
import platform as pf
import psutil
import PIL
import pandas as pd
import seaborn as sns
import json
import io

# for parser.parse_arg error
import sys
sys.argv = ['']
del sys


def indent(elem, level=0):  #
    i = "\n" + level * "  "
    if len(elem):
        if not elem.text or not elem.text.strip():
            elem.text = i + "  "
        if not elem.tail or not elem.tail.strip():
            elem.tail = i
        for elem in elem:
            indent(elem, level + 1)
        if not elem.tail or not elem.tail.strip():
            elem.tail = i
    else:
        if level and (not elem.tail or not elem.tail.strip()):
            elem.tail = i

def ToF(file, cat):
    if cat == '00000000':
        output = "N"
    elif str(file).split('_')[2] == cat:
        output = "T"
    else:
        output = "F"
    
    return output
    
def detect(path, img0):
    global opt
    imgsz = (320, 192) if ONNX_EXPORT else opt.img_size  # (320, 192) or (416, 256) or (608, 352) for (height, width)
    out, source, weights, half, view_img, save_txt, save_xml = opt.output, opt.source, opt.weights, opt.half, opt.view_img, opt.save_txt, opt.save_xml
    webcam = source == '0' or source.startswith('rtsp') or source.startswith('http') or source.endswith('.txt')

    # Initialize
    device = torch_utils.select_device(device='cpu' if ONNX_EXPORT else opt.device)
    if os.path.exists(out):
        shutil.rmtree(out)  # delete output folder
    os.makedirs(out)  # make new output folder

    # Initialize model
    model = Darknet(opt.cfg, imgsz)

    # Load weights
    attempt_download(weights)
    if weights.endswith('.pt'):  # pytorch format
        model.load_state_dict(torch.load(weights, map_location=device)['model'], strict=False)
    else:  # darknet format
        load_darknet_weights(model, weights)

    # Second-stage classifier
    classify = False
    if classify:
        modelc = torch_utils.load_classifier(name='resnet101', n=2)  # initialize
        modelc.load_state_dict(torch.load('weights/resnet101.pt', map_location=device)['model'],
                               strict=False)  # load weights
        modelc.to(device).eval()

    # Eval mode
    model.to(device).eval()

    # Fuse Conv2d + BatchNorm2d layers
    # model.fuse()
    

    # Half precision
    half = half and device.type != 'cpu'  # half precision only supported on CUDA
    if half:
        model.half()

    # dataset = LoadImages(source, img_size=imgsz)

    # Get names and colors
    names = load_classes(opt.names)


    # for path, img, im0s, vid_cap in dataset:
    
    img0 = np.array(PIL.Image.open(io.BytesIO(img0)))
    for i in range(len(img0)):
        for j in range(len(img0[0])):
            img0[i][j] = img0[i][j][::-1]

    img = letterbox(img0, new_shape=imgsz)[0]

    # Convert
    img = img[:, :, ::-1].transpose(2, 0, 1)  # BGR to RGB, to 3x416x416
    img = np.ascontiguousarray(img)

    img = torch.from_numpy(img).to(device)
    img = img.half() if half else img.float()  # uint8 to fp16/32
    img /= 255.0  # 0 - 255 to 0.0 - 1.0
    if img.ndimension() == 3:
        img = img.unsqueeze(0)
    # Inference
    pred = model(img, augment=opt.augment)[0]

    # to float
    if half:
        pred = pred.float()

    # Apply NMS
    pred = non_max_suppression(pred, opt.conf_thres, opt.iou_thres,
                               multi_label=False, classes=opt.classes, agnostic=opt.agnostic_nms)

    # Apply Classifier
    if classify:
        pred = apply_classifier(pred, modelc, img, img0)

    # Process detections
    for i, det in enumerate(pred):  # detections for image i
        p, s, im0 = path, '', img0
        

        save_path = str(Path(out) / Path(p).name)

        root = Element('annotation')
        SubElement(root, 'folder').text = str(Path(out))
        SubElement(root, 'filename').text = str(Path(p))
        SubElement(root, 'path').text = save_path

        if det is not None and len(det):
            # Rescale boxes from imgsz to im0 size
            det[:, :4] = scale_coords(img.shape[2:], det[:, :4], im0.shape).round()
            count = 0

            # Print results
            # for c in det[:, -1].unique():
            #     n = (det[:, -1] == c).sum()  # detections per class
            #     s += '%g %s, ' % (n, names[int(c)])  # add to string
            #     s += '%s, ' % (ToF(str(Path(p)), names[int(c)]))  # add True or False

            total = []
            object_names = []
            score=[]
            data = {}
            data["object"] = []

            # Write results
            for *xyxy, conf, cls in reversed(det):
                label = '%s %.2f' % (names[int(cls)], conf)
                score.append(label.split(' ')[1])

                semi = []
                for nums in range(4):
                    str_x = str(xyxy[nums]).split('(')
                    str_x = str_x[1].split('.')
                    semi.append(str_x[0])
                total.append(semi)
                object_names.append(names[int(cls)])
                count = count + 1


            for i in range(count):  ##리스트 두 개 xml파일에 저장
                data["object"].append({
                    "name" : object_names[i],
                    "bndbox":{
                    "xmin": str(total[i][0]),
                    "ymin": str(total[i][1]),
                    "xmax": str(total[i][2]),
                    "ymax": str(total[i][3])
                    },
                    "score":score[i]
                })


            if save_xml:
                with open(save_path[:save_path.rfind('.')] + '.json', 'w') as outfile:
                    json.dump(data, outfile)
    if data:
        return data
    else:
        data["object"].append({
                        "name" : 'unknown',
                        "bndbox":{
                        "xmin": '0',
                        "ymin": '0',
                        "xmax": '0',
                        "ymax": '0'
                        },
                        "score":score[i]
                    })
        return  data

def classification(path, img0):
    global opt
    base_path = '/workspace/ai_service/yolov3/'
    parser = argparse.ArgumentParser()
    parser.add_argument('--cfg', type=str, default=base_path + 'cfg/yolov3-spp-403cls.cfg', help='*.cfg path')
    parser.add_argument('--names', type=str, default=base_path + 'data/403food.names', help='*.names path')
    parser.add_argument('--weights', type=str, default=base_path + 'weights/best_403food_e200b150v2.pt', help='weights path')
    parser.add_argument('--source', type=str, default=base_path + 'data/samples', help='source')  # input file/folder, 0 for webcam
    parser.add_argument('--output', type=str, default=base_path + 'output', help='output folder')  # output folder
    parser.add_argument('--img-size', type=int, default=320, help='inference size (pixels)')
    parser.add_argument('--conf-thres', type=float, default=0.3, help='object confidence threshold')
    parser.add_argument('--iou-thres', type=float, default=0.5, help='IOU threshold for NMS')
    parser.add_argument('--fourcc', type=str, default='mp4v', help='output video codec (verify ffmpeg support)')
    parser.add_argument('--half', action='store_true', help='half precision FP16 inference')
    parser.add_argument('--device', default='', help='device id (i.e. 0 or 0,1) or cpu')
    parser.add_argument('--view-img', action='store_true', help='display results')
    parser.add_argument('--save-txt', action='store_true',default=True, help='save results to *.txt')
    parser.add_argument('--classes', nargs='+', type=int, help='filter by class')
    parser.add_argument('--agnostic-nms', action='store_true', help='class-agnostic NMS')
    parser.add_argument('--augment', action='store_true', help='augmented inference')
    parser.add_argument('--save-xml', action='store_true', default=True, help='save results to *.xml')

    opt = parser.parse_args()

    opt.cfg = check_file(opt.cfg)  # check file
    opt.names = check_file(opt.names)  # check file
    print(os.path.realpath(__file__))
    print(len(os.listdir(opt.source)))

    return detect(path, img0)

    # with torch.no_grad():
    #     print('Session START :', time.strftime('%Y-%m-%d %Z %H:%M:%S', time.localtime(time.time())))
    #     print('command : python3 detect_1231.py --cfg {0} --names {1} --weights {2}'.format(opt.cfg, opt.names, opt.weights))
    #     print('===============================================================')
    #     #print(d.isoformat())
    #     def printOsInfo():
    #         print('GPU                  :\t', torch.cuda.get_device_name(0)) 
    #         print('OS                   :\t', pf.system())
    #         #  print('OS Version           :\t', platform.version())

    #     if __name__ == '__main__':
    #         printOsInfo()

    #     def printSystemInfor():
    #         print('Process information  :\t', pf.processor())
    #         print('Process Architecture :\t', pf.machine())
    #         print('RAM Size             :\t',str(round(psutil.virtual_memory().total / (1024.0 **3)))+"(GB)")
    #         print('===============================================================')
          
    #     if __name__ == '__main__':
    #         printSystemInfor()  

    #     print('Pytorch')
    #     print('torch ' + torch.__version__)
    #     print('numpy ' + np.__version__)
    #     print('torchvision ' + torch.__version__)
    #     print('matplotlib ' + matplotlib.__version__)
    #     print('pillow ' + PIL.__version__)
    #     print('pandas ' + pd.__version__)
    #     print('seaborn ' + sns.__version__)   
    #     print('psutil ' + psutil.__version__) 
    #     print('===============================================================')

if __name__ == '__main__':
    classification()
