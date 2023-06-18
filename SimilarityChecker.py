import numpy as np
import nltk


class SimilarityChecker:

    def levenshtein_distance(self, str1, str2):
        # Compute the Levenshtein distance between the two strings
        len1, len2 = len(str1), len(str2)
        dp = [[0] * (len2 + 1) for _ in range(len1 + 1)]
        for i in range(len1 + 1):
            dp[i][0] = i
        for j in range(len2 + 1):
            dp[0][j] = j
        for i in range(1, len1 + 1):
            for j in range(1, len2 + 1):
                cost = 0 if str1[i - 1] == str2[j - 1] else 1
                dp[i][j] = min(dp[i - 1][j] + 1, dp[i][j - 1] + 1, dp[i - 1][j - 1] + cost)
        levenshtein_distance = dp[len1][len2]

        # Compute the percentage of similarity
        max_length = max(len1, len2)
        similarity = 1 - levenshtein_distance / max_length
        return similarity

    def jaccard_similarity(self, str1, str2):
        tokenizer = nltk.tokenize.RegexpTokenizer(r'\w+')
        words1 = set(tokenizer.tokenize(str1.lower()))
        words2 = set(tokenizer.tokenize(str2.lower()))
        intersection = len(words1.intersection(words2))
        union = len(words1.union(words2))
        return intersection / union

    def cosine_similarity(self, str1, str2):
        tokenizer = nltk.tokenize.RegexpTokenizer(r'\w+')
        words1 = tokenizer.tokenize(str1.lower())
        words2 = tokenizer.tokenize(str2.lower())
        all_words = list(set(words1 + words2))
        vector1 = np.array([words1.count(w) for w in all_words])
        vector2 = np.array([words2.count(w) for w in all_words])
        return np.dot(vector1, vector2) / (np.linalg.norm(vector1) * np.linalg.norm(vector2))

    def hamming_distance(self, str1, str2):
        strminlen = 0
        strmaxlen = 0
        if len(str1) != len(str2):
            strminlen = min(len(str1),len(str2))
            strmaxlen = max(len(str1),len(str2))
        return sum(1 for i in range(strminlen) if str1[i] != str2[i])/strmaxlen


    def __call__(self,str1,str2,threshold = 0.4,w1 = 1,w2 = 1,w3 = 1,w4 = 1,):
        l = [w1 * self.hamming_distance(str1,str2),
             w2 * self.levenshtein_distance(str1,str2),
             w3 * self.cosine_similarity(str1,str2),
             w4 * self.jaccard_similarity(str1,str2)]
        x = np.average(l)
        return x ,threshold < x

