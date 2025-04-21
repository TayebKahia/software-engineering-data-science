from src.models.sentiment import extract_sentiment
import pytest
import csv

# Load sentiments from the CSV file
testdata = []

with open('soccer_sentiment_analysis.csv', 'r') as file:
    csv_reader = csv.reader(file)
    next(csv_reader)
    for row in csv_reader:
        testdata.append(row[0])  # Assuming the sentiment text is in the first column
print("Loaded test data:", testdata)
@pytest.mark.parametrize('sample', testdata)
def test_extract_sentiment(sample):
    print("Testing sample:", sample)
    sentiment = extract_sentiment(sample)
    # Test positive or negative sentiment based on the text content in `testdata`
    if "disappointing" in sample or "loss" in sample:
        assert sentiment <= 0
    else:
        assert sentiment > 0


# last one


# def test_extract_positive_sentiment():
#     positive_text = "Barcelona played brilliantly last Wednesday. Raphinha’s hat-trick was pure magic. Visca Barça!"
#     sentiment = extract_sentiment(positive_text)
#     assert sentiment > 0
