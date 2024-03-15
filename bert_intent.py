
from transformers import BertTokenizer, BertForSequenceClassification
import torch
from sklearn.preprocessing import LabelEncoder
import pandas as pd
import joblib
import torch.nn.functional as F
CONFIDENCE_THRESHOLD = 0.7  # Example threshold, adjust based on your model's performance

model_path = './model_directory'
label_encoder_file='./model_directory/label_encoder.joblib'
model = BertForSequenceClassification.from_pretrained(model_path)
tokenizer = BertTokenizer.from_pretrained(model_path)

# Assuming you've saved your LabelEncoder to disk as well
#label_encoder = LabelEncoder()
#label_encoder.classes_ = pd.read_pickle('./model_directory/label_encoder.joblib')
label_encoder = joblib.load(label_encoder_file)

def preprocess_query(query):
    """Tokenizes the query for BERT."""
    return tokenizer(query, padding=True, truncation=True, max_length=512, return_tensors="pt")

def predict_intent(preprocessed_query):
    """Predicts the intent of a preprocessed query using the loaded model."""
    model.eval()  # Put the model in evaluation mode
    with torch.no_grad():
        outputs = model(**preprocessed_query)
        logits = outputs.logits
        probabilities = F.softmax(logits, dim=1)
        max_probs, predictions = torch.max(probabilities, dim=1)
        confidence = max_probs.item()  # Assuming you're dealing with a single query for simplicity
        predicted_intent = predictions.item()  # Convert to Python int
    return predicted_intent, confidence

def get_intent_label(prediction, confidence):
    if confidence < CONFIDENCE_THRESHOLD:
        return "general_intent"  # This could be "general_query" or another suitable label indicating a fallback to a more general response
    else:
        return label_encoder.inverse_transform([prediction])[0] 
