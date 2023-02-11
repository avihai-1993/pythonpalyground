
def one_d_conv_scaner(oned_data : iter , size_to_scan : int , step : int = 1 , func : callable = None ) :
    N = len(oned_data)
    all_scan_res = []
    start_index = 0
    end_index = size_to_scan
    while True:
        slice_data = oned_data[start_index:end_index]
        if func is not None :
            func(slice_data)
        else:
            all_scan_res.append(slice_data)
        start_index = start_index + step
        end_index = end_index + step
        if end_index > N:
            break

    if func is None :
        return all_scan_res


l = [1,2,3,4,5,6,7,8,9]
s = "123456789"


print(one_d_conv_scaner(l,4))
print(one_d_conv_scaner(s,5))
