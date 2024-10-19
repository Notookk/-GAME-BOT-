import random
import os

class WordLoader:
    def __init__(self, data_path: str = "data/"):
        """Initializes the WordLoader with the path to the word files."""
        self.data_path = data_path

    def load_words(self, category: str) -> list[tuple[str, str]]:
        """
        Loads word pairs from the specified category file.

        Args:
            category (str): The category name (e.g., 'sports', 'food').

        Returns:
            list[tuple[str, str]]: A list of word pairs.
        """
        file_path = os.path.join(self.data_path, f"{category}.txt")
        try:
            with open(file_path, 'r') as file:
                word_pairs = [
                    tuple(line.strip().split(" : ")) for line in file.readlines()
                ]
            return word_pairs
        except FileNotFoundError:
            print(f"Error: {category}.txt not found in {self.data_path}.")
            return []

    def get_random_word_pair(self, category: str) -> tuple[str, str]:
        """
        Selects a random word pair from the given category.

        Args:
            category (str): The category name.

        Returns:
            tuple[str, str]: A random word pair.
        """
        words = self.load_words(category)
        if not words:
            raise ValueError(f"No words available for category: {category}")
        return random.choice(words)
