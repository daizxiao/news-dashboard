import re
from simhash import Simhash, SimhashIndex

class NewsDeduplicator:
    def __init__(self, k=3):
        """
        k: Hamming distance threshold (default is 3, below which content is considered duplicate)
        """
        self.k = k
        self.index = SimhashIndex([], k=k)

    def _preprocess(self, text):
        """
        Tokenize and clean text (simple whitespace and regex for now)
        """
        # Remove special characters and lowercase
        text = re.sub(r'[^\w\s]', '', text).lower()
        return text.split()

    def is_duplicate(self, text, add_if_unique=True):
        """
        Checks if text is a duplicate.
        """
        s = Simhash(self._preprocess(text))
        dups = self.index.get_near_dups(s)
        
        if dups:
            return True
        
        if add_if_unique:
            # Using text as key (can be ID in production)
            self.index.add(str(hash(text)), s)
            
        return False

# Example usage (can be scaled with Redis-based SimHash implementation)
if __name__ == "__main__":
    dedup = NewsDeduplicator()
    text1 = "Bloomberg: Fed might pause rate hikes next month due to slowing inflation."
    text2 = "Reuters: Inflation slows down, Fed likely to pause rate increases in the coming month."
    
    print(f"Text 1 duplicate: {dedup.is_duplicate(text1)}")
    print(f"Text 2 duplicate: {dedup.is_duplicate(text2)}") # Should be True if k is appropriate
