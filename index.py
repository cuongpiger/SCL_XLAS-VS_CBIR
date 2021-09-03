import modules.ColorDescriptor as ColorDescriptor
import argparse
import cv2
import glob # using for writing feature vectors to csv file

import modules.user_defined_data_types as udt

args_parser = argparse.ArgumentParser()
args_parser.add_argument("-d", "--dataset", required=True, help="Path to directory that contains images.")
args_parser.add_argument("-i", "--index", required=True, help="Path to where index will be stored.")
args = vars(args_parser.parse_args())

''' Khởi tạo ColorDescriptor object '''
cd = ColorDescriptor.ColorDescriptor((8, 12, 13))

''' File để ghi các feature vector'''
output = open(args['index'], 'w')

''' Lấy tất cả filepath image trong folde dataset '''
for image_path in glob.glob(args['dataset'] + '/*.jpg'):
    image_UID: str = image_path[image_path.rfind('/') + 1:] # lấy filename
    image: udt.Image = cv2.imread(image_path)
    features: list = cd.describe(image) # tính toán feature vector cho `image`
    
    ''' Ép kiểu thành str '''
    features = [str(f) for f in features]
    output.write("%s,%s\n" % (image_UID, ','.join(features)))
    
output.close()