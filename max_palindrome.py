def getAllMaxPalindromes(s: str) -> list:
    def isPalindrome(s1: str):
        return s1 == s1[::-1]
    all_max_len_polindomes = []
    number_of_phases = len(s)
    phase = 0
    while phase < number_of_phases and len(all_max_len_polindomes) <= 0:
        start_index = 0
        end_index = (number_of_phases - phase)
        while True:
            slice_str = s[start_index:end_index]
            if isPalindrome(slice_str):
                all_max_len_polindomes.append(slice_str)
            start_index = start_index + 1
            end_index = end_index + 1
            if end_index > number_of_phases:
                break
        phase += 1
    return all_max_len_polindomes

testStr = 'ee2aCbCa2ee'
testStr1 = 'ee2aCbCaggCgg'
testStr2 = 'ee2aCbCatggCggt'
print(getAllMaxPalindromes(testStr))
print(getAllMaxPalindromes(testStr1))
print(getAllMaxPalindromes(testStr2))
