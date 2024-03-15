
from sklearn.preprocessing import LabelEncoder
from transformers import BertTokenizer
import torch
from sklearn.model_selection import train_test_split
from transformers import BertForSequenceClassification, Trainer, TrainingArguments
from torch.utils.data import Dataset
import joblib
from transformers import get_linear_schedule_with_warmup
from sklearn.metrics import accuracy_score, precision_recall_fscore_support

tokenizer = BertTokenizer.from_pretrained('bert-base-uncased')

queries = [
    "Find me a hotel in New York",
    "What are the local transport options in New York?",


    "What are the luxury accommodations available in Manhattan?",
    "Are there any budget hotels in Midtown with free Wi-Fi?",
    "Show me mid-range hotels in Hell's Kitchen that include a spa",
    "Can I find a hotel near Times Square with a rating of 5 stars?",
    "List all accommodations in Lower East Side that have a bar and restaurant",
    "What are the subway options available in New York?",
    "What are the bus services available until 1:00 AM?",
    "Can you give me information on metered taxi services?",
    "I'm looking for bike rental services available all day in New York",
    "What's the price of renting bike per hour?",
    "Tell me about the entrance fee and operating hours for the Statue of Liberty",
    "What are the free points of interest open 24 hours in Manhattan?",
    "I want to visit the Empire State Building. How much is the ticket?",
    "Provide details on Broadway Theaters and their show times",
    "Give me information on the Metropolitan Museum of Art's visiting hours",
    "Book a bus ticket with Greyhound for March 15th at 8:00 AM",
    "What are the flight options to Los Angeles on Delta Airlines for March 15th?",
    "Show me car rental options that allow flexible timings",
    "I need a train to Boston on March 15th. What are my options with Amtrak?",
    "Find me the cheapest transport option to Chicago on March 15th",

    "Give me hotels in New York with free WiFi.",
    "Find accommodations near Central Park that offer breakfast.",
    "List luxury hotels in Manhattan with a gym.",
    "What are the subway options available in New York?",

    "Guide me to bike rentals available in Brooklyn.",
    "Find me a taxi service that operates in Queens.",
    "Tell me about the museums I can visit in New York.",

"Show parks in New York suitable for picnics.",
"What are the historical sites in New York?",

"I want to book a flight from Boston to New York for next Monday.",

"What are the train services from Boston to New York?",
"Find me the cheapest bus ticket from Boston to New York.",
"Suggest family-friendly hotels in Brooklyn.",
"Where can I stay in New York with a great view of the skyline?",
"List pet-friendly accommodations in Queens.",
"Show hotels near JFK Airport with shuttle service.",
"Find boutique hotels in Greenwich Village with a rooftop bar.",
"What subway line gets me to the Metropolitan Museum of Art?",
"Guide me on using the ferry service from Manhattan to Staten Island.",
"List bike-sharing services available in Central Park.",
"How do I travel from Times Square to Wall Street by bus?",
"Are there any 24-hour taxi services in Manhattan?",
"What are the must-visit attractions in New York for first-time visitors?",
"Show historical landmarks in Lower Manhattan.",
"Find kid-friendly parks in New York for a family day out.",
"Locate art galleries in Chelsea worth visiting.",
"Guide me to jazz clubs in Harlem for live music.",
"Book the earliest train to Boston from Penn Station.",
"How can I travel from Boston to New York"


]

intents = [
    "find_accommodation",
    "query_local_transport",
    "find_accommodation",
    "find_accommodation",
    "find_accommodation",
    "find_accommodation",
    "find_accommodation",
    "query_local_transport",
    "query_local_transport",
    "query_local_transport",
    "query_local_transport",
    "query_local_transport",
    "find_poi",
    "find_poi",
    "find_poi",
    "find_poi",
    "find_poi",
    "book_transport",
    "book_transport",
    "book_transport",
    "book_transport",
    "book_transport",
    "find_accommodation",
    "find_accommodation",
    "find_accommodation",
    "query_local_transport",
    "query_local_transport",
    "query_local_transport",
    "find_poi",
    "find_poi",
    "find_poi",
    "book_transport",
    "book_transport",
    "book_transport",
    "find_accommodation",
    "find_accommodation",
    "find_accommodation",
    "find_accommodation",
    "find_accommodation",
    "query_local_transport",
    "query_local_transport",
    "query_local_transport",
    "query_local_transport",
    "query_local_transport",
    "find_poi",
    "find_poi",
    "find_poi",
    "find_poi",
    "find_poi",
"book_transport",
"book_transport",


    
]

label_encoder = LabelEncoder()
intents_encoded = label_encoder.fit_transform(intents)
tokenizer = BertTokenizer.from_pretrained('bert-base-uncased')
encoded_inputs = tokenizer(queries, padding=True, truncation=True, return_tensors="pt", max_length=512)
print(len(encoded_inputs['input_ids']), len(intents_encoded))

from sklearn.model_selection import train_test_split

# Split input_ids and attention_mask separately but synchronously
train_inputs, val_inputs, train_labels, val_labels = train_test_split(
    encoded_inputs['input_ids'], intents_encoded, test_size=0.1, random_state=42
)
train_masks, val_masks, _, _ = train_test_split(
    encoded_inputs['attention_mask'], intents_encoded, test_size=0.1, random_state=42
)


model = BertForSequenceClassification.from_pretrained('bert-base-uncased', num_labels=len(set(intents_encoded)))
print(encoded_inputs.keys())
class QueriesDataset(Dataset):
    def __init__(self, encodings,masks, labels):
        self.encodings = encodings
        self.masks = masks
        self.labels = labels

    def __getitem__(self, idx):
        item = {
            'input_ids': torch.tensor(self.encodings[idx], dtype=torch.long).clone().detach(),
            'attention_mask': torch.tensor(self.masks[idx], dtype=torch.long).clone().detach(),
            'labels': torch.tensor(self.labels[idx], dtype=torch.long).clone().detach()
        }
        return item

    def __len__(self):
        return len(self.labels)

# Create dataset objects
train_dataset = QueriesDataset(train_inputs, train_masks, train_labels)
val_dataset = QueriesDataset(val_inputs, val_masks, val_labels)

def compute_metrics(pred):
    labels = pred.label_ids
    preds = pred.predictions.argmax(-1)
    precision, recall, f1, _ = precision_recall_fscore_support(labels, preds, average='weighted')
    acc = accuracy_score(labels, preds)
    return {
        'accuracy': acc,
        'f1': f1,
        'precision': precision,
        'recall': recall,
    }


training_args = TrainingArguments(
    output_dir='./results',
    num_train_epochs=50,
    per_device_train_batch_size=8,
    learning_rate=5e-5,
    weight_decay=0.01,
    logging_dir='./logs',
    evaluation_strategy="steps",
    eval_steps=50,
    save_steps=50,
    warmup_steps=500, 
)

trainer = Trainer(
    model=model,
    args=training_args,
    train_dataset=train_dataset,
    eval_dataset=val_dataset,
    compute_metrics=compute_metrics,  
)

trainer.train()
results = trainer.evaluate()
print(results)


model_dir = './model_directory'

# Save the model
model.save_pretrained(model_dir)

# Save the tokenizer
tokenizer.save_pretrained(model_dir)
label_encoder_file = './model_directory/label_encoder.joblib'
joblib.dump(label_encoder, label_encoder_file)