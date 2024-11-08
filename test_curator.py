# test_nemo_curator.py

# Import the NeMo Curator Normalizer from the NeMo NLP collection
from nemo.collections.nlp.data.text_normalization import Normalizer

def main():
    # Initialize the NeMo Normalizer
    normalizer = Normalizer()

    # Define a sample text for normalization
    sample_text = "I'm testing NeMo Curator's text normalization capability! Let's see if it works."

    # Perform normalization on the sample text
    normalized_text = normalizer.normalize(sample_text)

    # Output the results
    print("Original Text:", sample_text)
    print("Normalized Text:", normalized_text)

if __name__ == "__main__":
    main()