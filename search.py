import modules.ColorDescriptor as ColorDescriptor
import modules.Searcher as Searcher
import argparse
import cv2

import modules.user_defined_data_types as udt

args_parser = argparse.ArgumentParser()
args_parser.add_argument("-i", "--index", required=True, help="Path to where the computed index will be stored.")
args_parser.add_argument("-q", "--query", required=True, help="Path to the query image.")
args_parser.add_argument("-r", "--result-path", required=True, help="Path to the result path.")
args = vars(args_parser.parse_args())

''' Khởi tạo ColorDescriptor object '''
cd = ColorDescriptor.ColorDescriptor((8, 12, 13))

''' Load query image và chuyển đổi thành feature vector '''
query_image: udt.Image = cv2.imread(args['query'])
query_feature: list = cd.describe(query_image)

''' Truy cập vào các vector indexing '''
finder = Searcher.Searcher(args['index'])
results = finder.search(query_feature)

''' Hiển thị ảnh truy vấn '''
cv2.imshow('Query image', query_image)

for chi2score, image_uid in results:
    result_image: udt.Image = cv2.resize(cv2.imread(args['result_path'] + '/' + image_uid), (300, 300))
    cv2.imshow('Result image', result_image)
    
    cv2.waitKey(0)