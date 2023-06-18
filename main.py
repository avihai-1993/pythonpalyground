
# Import the class
from SimilarityChecker import SimilarityChecker

# Create an instance of the class
similarity_checker = SimilarityChecker()

# Define two strings to compare
str1 = "Hello, world!"
str2 = "Hello, Python!"

# Calculate the similarity using each method
print("Levenshtein distance:", similarity_checker.levenshtein_distance(str1, str2))
print("Jaccard similarity:", similarity_checker.jaccard_similarity(str1, str2))
print("Cosine similarity:", similarity_checker.cosine_similarity(str1, str2))
print("Hamming distance:", similarity_checker.hamming_distance(str1, str2))
print(similarity_checker(str1,str2))


