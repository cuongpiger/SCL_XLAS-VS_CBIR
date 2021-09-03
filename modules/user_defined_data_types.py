# USER DEFINED DATA TYPE ANNOTATIONS _______________________________________________________________
Image = """
    - Một numpy array có shape = (width, height, channels) với:
      * width (int): là chiều rộng của ảnh.
      * height (int): là chiều cao của ảnh.
      * channels (int): là số kênh màu dùng để biểu diễn ảnh.
"""

Matrix = """
    - Một numpy array có shape = (width, height)
"""

Histo = """
    - Một numpy array có số chiều là `len(self.ibins)`.
    - Ví dụ self.ibins: Tuple[8, 12, 13] thì Histo có shape=(8, 12, 13)
"""
#___________________________________________________________________________________________________
