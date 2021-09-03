import numpy as np
import cv2
import imutils

from typing import Tuple, List
import modules.user_defined_data_types as udt


class ColorDescriptor:
    def __init__(self, pbins: Tuple[int, int, int]):
        """
        Constructor

        Args:
            * pbins (Tuple[int, int, int]): Số bins trong histogram mà muốn chia cho `len(pbins)`
                kênh màu.
        """
        self.ibins: Tuple[int, int, int] = pbins
        
        
    def describe(self, pimage: udt.Image) -> (list):
        ''' Ép dtype sang unsigned integer 8 bit '''
        image: udt.Image = pimage.astype(np.uint8)
        ''' Chuyển từ hệ màu BGR sang HSV '''
        image: udt.Image = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
        features = [] # lưu các np array 1 dim về color feature
        
        height: int = image.shape[0] # lấy chiều cao của anh
        width: int = image.shape[1] # lấy chiều rộng của ảnh
        centre_height: int = int(height * .5) # lấy trung điểm theo chiều cao của ảnh_
        centre_width: int = int(width * .5) # lấy trung điểm chiều rộng của ảnh
        
        ''' Chia ảnh thành 4 vùng, lần lượt là: top-left, top-right, bottom-left, bottom-right '''
        region_coors = [
            (0, centre_width, 0, centre_height),
            (centre_width, width, 0, centre_height),
            (0, centre_height, centre_height, height),
            (centre_width, width, centre_height, height)
        ]
        ''' Trung tâm của ảnh là một hình eclipse '''
        centre_width_radius: int = int(width * .75) // 2 # lấy 75% chiều rộng ảnh làm vùng trung tâm
        centre_height_radius: int = int(height * .75) // 2 # lấy 75% chiều cao ảnh làm vùng trung tâm
        ellipse_mask: udt.Matrix = np.zeros(image.shape[:2], dtype=np.uint8)
        ''' Vẽ hình ellipse ở trung tâm tấm ảnh'''
        cv2.ellipse(ellipse_mask, (centre_width, centre_height), 
                    (centre_width_radius, centre_height_radius), 0, 0, 360, 255, -1)
        
        for x1, x2, y1, y2 in region_coors:
            ''' Xây dựng một mặt nạ từ 4 góc '''
            corner_mask: udt.Matrix = np.zeros(image.shape[:2], dtype=np.uint8)
            cv2.rectangle(corner_mask, (x1, y1), (x2, y2), 255, -1)
            ''' corner_mask = corner_mast - intersection(corner_mask, ellipse_mask) '''
            corner_mask: udt.Matrix = cv2.subtract(corner_mask, ellipse_mask)
            
            ''' Xây dựng histogram cho tương ứng cho corner_mask sau đó tính feature vector '''
            hist = self.histogram(image, corner_mask)
            features.extend(hist)
            
        ''' Xây dựng histogram cho vùng trung tâm sau đó tính feature vector '''
        hist = self.histogram(image, ellipse_mask)
        features.extend(hist)

        return features
                
    
    def histogram(self, pimage: udt.Image, pmask: udt.Matrix) -> (List[float]):
        ''' Tính toán lược đồ màu cho ko gian HSV, hist trả vè là np array với shape = self.bins'''
        hist: udt.Histo = cv2.calcHist([pimage], [0, 1, 2], pmask, self.ibins, [0, 180, 0, 256, 0, 256])
            
        ''' Normalize histogram '''
        hist: List[float] = cv2.normalize(hist, hist).flatten()
        
        return hist