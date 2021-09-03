import numpy as np
import csv

from typing import List, Dict
import modules.user_defined_data_types as udt

class Searcher:
    def __init__(self, pindexPath):
        self.iindexPath = pindexPath
        
    def search(self, pqueryFeature: List[float], pgetFirst=10) -> (List[str]):
        librarian: Dict[str, float] = {}
        
        with open(self.iindexPath) as f:
            reader: List[str] = csv.reader(f)
        
            for row in reader:
                ''' Lấy các giá trị của feature vector '''
                feature: List[float] = [float(x) for x in row[1:]]
                chi2_distance = self.chiSquareDistance(feature, pqueryFeature) # tính khoảng cách chi square
                
                ''' `row[0]` là uid (unique identifier defined) của hình '''
                librarian[row[0]] = chi2_distance
                
            f.close()
            
        librarian = sorted([(val, key) for key, val in librarian.items()])
        
        return librarian[:min(pgetFirst, len(librarian))]
                
                
        
        
    def chiSquareDistance(self, phistA, phistB, peps=1e-10) -> (float):
        """
        Tính khoảng cách Chi-square, công thức tại:
            https://www.geeksforgeeks.org/chi-square-distance-in-python

        Args:
            phistA ([type]): [description]
            phistB ([type]): [description]
            peps (float, optional): Dùng để tránh lỗi chia cho 0. Defaults to 1e-10.
        """
        ''' Tính khoảng cách chi-square '''
        return .5 * np.sum([(((a - b)**2) / (a + b + peps)) for a, b in zip(phistA, phistB)])
        