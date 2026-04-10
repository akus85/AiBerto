from transformers import pipeline

classifier = pipeline(
    "sentiment-analysis",
    model="distilbert-base-uncased-finetuned-sst-2-english",
)

result = classifier("I genuinely loved this movie, it was a great experience.")
print(result)