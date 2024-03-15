import openai_integration
import spacy
from db_queries import *


openai_integration.api_key = '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'



nlp = spacy.load("en_core_web_sm")
def create_lemma_pairs_and_triplets(doc):
    lemmas = [token.lemma_ for token in doc]
    lemma_pairs = [" ".join(lemmas[i:i+2]) for i in range(len(lemmas)-1)]  # Create pairs
    lemma_triplets = [" ".join(lemmas[i:i+3]) for i in range(len(lemmas)-2)]  # Create triplets
    return lemmas + lemma_pairs + lemma_triplets
    

def recognize_intent(query):
    doc = nlp(query.lower())
    all_lemmas_and_combinations = create_lemma_pairs_and_triplets(doc)
    accommodation_keywords = ["hotel", "accommodation", "place to stay", "lodging","book","stay"]
    transport_keywords = ["transport", "transportation", "how to get", "travel options","how to reach"]
    poi_keywords = ["things to do", "attractions", "sights", "tourist spots","go","visit","see"]
    local_transport_keywords = ["city transport", "local travel", "public transport", "getting around","get around"]

    # Initialize an empty dict to store possible intents based on different criteria
    possible_intents = {}

    for token in doc:

        #if token.ent_type_ == "GPE":
         #   possible_intents["location_based_search"] = token.text

    
        #context = " ".join([child.lemma_ for child in token.children]) + " " + token.lemma_
        #context = " ".join([token.lemma_ for token in doc])

        if any(keyword in all_lemmas_and_combinations for keyword in accommodation_keywords):
            possible_intents["accommodation_search"] = "booking"
        elif any(keyword in all_lemmas_and_combinations for keyword in local_transport_keywords):
            possible_intents["local_transport_search"] = "local_transport"
        elif any(keyword in all_lemmas_and_combinations for keyword in transport_keywords):
            possible_intents["transport_options_search"] = "general_transport"
        elif any(keyword in all_lemmas_and_combinations for keyword in poi_keywords):
            possible_intents["poi_search"] = "point_of_interest"
        print("Possible intents detected:", possible_intents)

    if possible_intents:
        return select_most_relevant_intent(possible_intents)
    return "ask_for_clarification",None

def select_most_relevant_intent(possible_intents):
    for intent in ["accommodation_search", "poi_search", "local_transport_search", "transport_options_search"]:
        if intent in possible_intents:
            return intent, possible_intents[intent]
    return "ask_for_clarification", None

