import torch
from transformers import AutoTokenizer, AutoModelForCausalLM
import re
import nltk
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
from nltk.tokenize import word_tokenize

from config import HUGGINGFACE_API_KEY
from knowledge_base import FAQ_DATA

class Chatbot:
    def __init__(self):
        print("Loading DialoGPT model... Please wait...")
        token_kwargs = {}
        if HUGGINGFACE_API_KEY:
            token_kwargs = {"token": HUGGINGFACE_API_KEY}
        else:
            print("Warning: HUGGINGFACE_API_KEY is not set. Proceeding with anonymous Hugging Face access which may be rate limited.")

        self.tokenizer = AutoTokenizer.from_pretrained("microsoft/DialoGPT-small", **token_kwargs)
        self.model = AutoModelForCausalLM.from_pretrained("microsoft/DialoGPT-small", **token_kwargs)
        
        if self.tokenizer.pad_token is None:
            self.tokenizer.pad_token = self.tokenizer.eos_token
        self.model.eval()  
        self.chat_history_ids = None
        self.model_loaded = True

        self._ensure_nltk_resources()
        self.lemmatizer = WordNetLemmatizer()
        self.stop_words = set(stopwords.words("english"))
        self.faq_threshold = 0.35
        self.faq_pairs = [
            {
                **entry,
                "tokens": self._preprocess_text(entry["question"])
            }
            for entry in FAQ_DATA
        ]

    @staticmethod
    def _ensure_nltk_resources():
        required = ["punkt", "punkt_tab", "wordnet", "stopwords"]
        for resource in required:
            try:
                if resource == "punkt":
                    nltk.data.find("tokenizers/punkt")
                elif resource == "punkt_tab":
                    nltk.data.find("tokenizers/punkt_tab")
                else:
                    nltk.data.find(f"corpora/{resource}")
            except LookupError:
                nltk.download(resource, quiet=True)

    def _check_rule_based_response(self, user_text):
        """Handle common questions with rule-based responses"""
        text_lower = user_text.lower().strip()
        text_words = set(text_lower.split())
        
        
        if 'name' in text_lower:
            if any(word in text_lower for word in ['what', 'your', 'who', 'tell', 'say']):
                return "I'm an AI chatbot created to help answer questions and have conversations. You can call me ChatBot!"
        
       
        if ('who' in text_lower and 'you' in text_lower) or ('what' in text_lower and 'you' in text_lower and 'are' in text_lower):
            return "I'm an AI chatbot created to help answer questions and have conversations. You can call me ChatBot!"
        
      
        greeting_words = ['hello', 'hi', 'hey', 'greetings', 'greeting', 'hii', 'hiii']
        if any(word in text_lower for word in greeting_words):
            return "Hello! How can I help you today?"
        
       
        if 'good morning' in text_lower or 'morning' in text_lower:
            return "Good morning! How can I help you today?"
        if 'good afternoon' in text_lower or 'afternoon' in text_lower:
            return "Good afternoon! How can I help you today?"
        if 'good evening' in text_lower or 'evening' in text_lower:
            return "Good evening! How can I help you today?"
        if 'good night' in text_lower or 'night' in text_lower:
            return "Good night! Sleep well!"
        
        
        if 'how' in text_lower and 'you' in text_lower:
            if any(word in text_lower for word in ['are', 'doing', 'feeling']):
                return "I'm doing great, thank you for asking! How are you doing today?"
        
        
        if 'what' in text_lower and 'you' in text_lower:
            if any(word in text_lower for word in ['can', 'do', 'capable', 'help']):
                return "I can have conversations, answer questions, and help with various topics. Feel free to ask me anything!"
        
        
        if any(word in text_lower for word in ['help', 'assist', 'support']):
            return "I'm here to help! You can ask me questions, have a conversation, or just chat. What would you like to know?"
        
        
        if any(word in text_lower for word in ['bye', 'goodbye', 'see you', 'farewell', 'later', 'cya']):
            return "Goodbye! It was nice chatting with you. Have a great day!"
        
        
        if any(word in text_lower for word in ['thank', 'thanks', 'appreciate', 'thx']):
            return "You're welcome! I'm glad I could help. Is there anything else you'd like to know?"
        
        
        if 'age' in text_lower or ('old' in text_lower and 'you' in text_lower):
            return "I'm an AI, so I don't have an age in the traditional sense. I exist in the digital world!"
        
        
        if 'where' in text_lower and 'you' in text_lower:
            return "I exist in the cloud and can be accessed from anywhere! I don't have a physical location."
        
        
        if any(word in text_lower for word in ['created', 'made', 'built', 'developed', 'designed']):
            if 'you' in text_lower:
                return "I was created using advanced AI technology, specifically the DialoGPT model, to help with conversations and questions."
        
        return None  

    def _preprocess_text(self, text):
        tokens = word_tokenize(text.lower())
        cleaned = [
            self.lemmatizer.lemmatize(token)
            for token in tokens
            if token.isalpha() and token not in self.stop_words
        ]
        return set(cleaned)

    def _faq_response(self, user_text):
        user_tokens = self._preprocess_text(user_text)
        if not user_tokens:
            return None

        user_lower = user_text.lower()
        best_score = 0.0
        best_answer = None

        for entry in self.faq_pairs:
            entry_tokens = entry.get("tokens", set())
            if not entry_tokens:
                continue

            intersection = len(user_tokens & entry_tokens)
            union = len(user_tokens | entry_tokens)
            score = intersection / union if union else 0.0

            if any(keyword in user_lower for keyword in entry.get("keywords", [])):
                score += 0.15

            if score > best_score:
                best_score = score
                best_answer = entry["answer"]

        if best_score >= self.faq_threshold:
            print(f"Using FAQ response (score={best_score:.2f})")
            self.chat_history_ids = None
            return best_answer

        return None

    def reset_conversation(self):
        """Reset the conversation history"""
        self.chat_history_ids = None
        print("Conversation history reset")

    def get_response(self, user_text):
        try:
            print(f"Processing message: {user_text}")
            
            rule_response = self._check_rule_based_response(user_text)
            if rule_response:
                print(f"Using rule-based response: {rule_response}")
                
                self.chat_history_ids = None
                return rule_response

            faq_response = self._faq_response(user_text)
            if faq_response:
                print(f"Using FAQ response: {faq_response}")
                return faq_response
            
            print("Using AI model for response...")
            
           
            if self.chat_history_ids is not None and self.chat_history_ids.shape[-1] > 256:
                print("Resetting conversation history (too long)")
                self.chat_history_ids = None
            
            new_ids = self.tokenizer.encode(user_text + self.tokenizer.eos_token, return_tensors='pt')
            print(f"Encoded input, shape: {new_ids.shape}")

            if self.chat_history_ids is not None:
                bot_input = torch.cat([self.chat_history_ids, new_ids], dim=-1)
            else:
                bot_input = new_ids

            print("Generating response...")
            with torch.no_grad():  
                self.chat_history_ids = self.model.generate(
                    bot_input,
                    max_new_tokens=40,  
                    pad_token_id=self.tokenizer.pad_token_id,
                    do_sample=True,
                    top_k=30, 
                    top_p=0.85,  
                    temperature=0.7,  
                    num_return_sequences=1,
                    no_repeat_ngram_size=3,  
                    repetition_penalty=1.3  
                )

            print("Decoding response...")
            bot_reply = self.tokenizer.decode(
                self.chat_history_ids[:, bot_input.shape[-1]:][0],
                skip_special_tokens=True
            )

          
            bot_reply = bot_reply.strip()
            
           
            bad_indicators = ['add me', 'plz', 'pls', 'homie', 'gotchu', 'lol', 'xd', 'edit', 'stats']
            if any(indicator in bot_reply.lower() for indicator in bad_indicators):
                print("Detected poor quality response, using fallback")
                bot_reply = "I'm not sure how to respond to that. Could you rephrase your question?"
            
            
            if bot_reply:
                
                sentences = re.split(r'[.!?]+', bot_reply)
                if sentences and sentences[0].strip():
                    bot_reply = sentences[0].strip()
                    
                    if len(bot_reply) > 5 and not bot_reply.endswith(('.', '!', '?')):
                        bot_reply += '.'
                else:
                    bot_reply = "That's an interesting question! Could you tell me more?"

            print(f"Generated reply: {bot_reply}")

           
            if not bot_reply or len(bot_reply.strip()) < 3:
                bot_reply = "That's an interesting question! Could you tell me more about what you're looking for?"

            return bot_reply
        except Exception as e:
            import traceback
            error_msg = f"Sorry, I encountered an error: {str(e)}"
            print(f"Error in get_response: {error_msg}")
            print(traceback.format_exc())
            return error_msg