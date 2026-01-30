import numpy as np

employee_data = [
    [101, 25, 2, 7, 1],
    [102, 30, 3, 8, 2],
    [103, 28, '', 6, 1],
    [104, '', 5, 9, 3],
    [105, 35, 7, 10, 2],
    [106, 26, 1, 0, 1],
    [107, 40, 10, 8, 3],
    [108, 29, '', 5, 2],
    [109, 33, 4, 7, 1],
    [110, 27, 2, -1, 2]
]

print(employee_data)
# data = np.array(employee_data, dtype=object)
#
# def to_float(col):
#     out = np.empty(len(col), dtype=float)
#     for i, v in enumerate(col):
#         try:
#             out[i] = float(v)
#         except:
#             out[i] = np.nan
#     return out
#
# employee_data[:,1] = np.where(np.isnan(employee_data[:,1]),30, employee_data[:,1])
# employee_data[:,2] = np.where(np.isnan(employee_data[:,2]),10, employee_data[:,2])
# print(employee_data)
