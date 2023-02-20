import cv2
import numpy as np

def yolo_to_bbox(yolo_coords, img_width, img_height):
    # yolo_coords: [x_center, y_center, width, height]
    x_center, y_center, width, height = yolo_coords

    # Compute x_min, y_min, x_max, y_max
    x_min = int((x_center - (width / 2)) * img_width)
    y_min = int((y_center - (height / 2)) * img_height)
    x_max = int((x_center + (width / 2)) * img_width)
    y_max = int((y_center + (height / 2)) * img_height)

    # Return bbox coordinates
    return (x_min, y_min, x_max, y_max)

def masking(img, yolo_coords): # 이미지 파일을 넣음 (not bytes, not path)
    img_width = img.shape[1]
    img_height = img.shape[0]

    x_min, y_min, x_max, y_max = yolo_to_bbox(yolo_coords, img_width, img_height)

    # 경계박스 그리기
    cv2.rectangle(img, (x_min, y_min), (x_max, y_max), (0, 255, 0), 2)

    # 경계박스 영역을 제외한 나머지 영역 검은색으로 채우기
    mask = np.zeros_like(img)
    cv2.rectangle(mask, (x_min, y_min), (x_max, y_max), (255, 255, 255), -1)
    result = np.bitwise_and(img, mask)

    return result

img_url = '1.jpg'

img = cv2.imread(img_url) # 이미지를 numpy.ndarray로 입력받음 양추정에서 np.array(Image.open(io.BytesIO(img)))로 받아올 예정

# print(type(img)) #<class 'numpy.ndarray'>

yolo_coords = [[0.436262, 0.474010, 0.383663, 0.178218], [0.236262, 0.174010, 0.283663, 0.078218]] # 테스트용 욜로 좌표 2개를 입력값으로 사용
# 2차원 리스트로 입력받을 예정
masking_list = [] # 마스킹된 이미지들의 numpy 배열 정보를 담을 리스트
for coord in yolo_coords:
    masking_list.append(masking(img, coord))

for array in masking_list:
    cv2.imshow("result", array)

    cv2.waitKey(0)
    cv2.destroyAllWindows()

# 이하 하나의 리스트로 입력받는 경우

# yolo_coords = [0.436262, 0.474010, 0.383663, 0.178218]
# masking_output = masking(img, yolo_coords) # masking output type numpy.ndarray

# cv2.imshow("result", masking_output) # 마스킹된 이미지 확인
# cv2.waitKey(0)
# cv2.destroyAllWindows()

# print()



# yolo_coords = [0.436262, 0.474010, 0.383663, 0.178218]

# # img_width = 720
# # img_height = 481

# img_path = '1.jpg'

# img = cv2.imread(img_path)

# img_width = img.shape[1]
# img_height = img.shape[0]

# print(yolo_to_bbox(yolo_coords, img_width, img_height))