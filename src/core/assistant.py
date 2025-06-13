import os
import httpx
from typing import Dict, Any, List
from .category_classifier import classify_prompt, get_available_categories

# Only load .env in development
if os.environ.get("FLASK_ENV") != "production":
    from dotenv import load_dotenv
    load_dotenv()

# Get API key at module level
api_key = os.getenv("OPENROUTER_API_KEY")
print("API key present:", bool(api_key))  # for logging

if not api_key:
    raise Exception("OPENROUTER_API_KEY not found")

class Assistant:
    def __init__(self):
        self.api_url = "https://openrouter.ai/api/v1/chat/completions"
        self.model = "openai/gpt-4.1-nano"  # Updated to GPT-4.1 Nano
        self.max_tokens = 500  # Increased token limit
        self.temperature = 0.7  # Balanced creativity
        self.top_p = 0.9  # Increased determinism
        
        # Load available categories
        self.categories = get_available_categories()
        
        # Base system prompts
        self.base_prompts = {
            'en': "You are Chaysh, a helpful AI assistant. Provide clear, concise responses and relevant suggestions in English.",
            'pl': "Jesteś Chaysh, pomocnym asystentem AI. Odpowiadaj jasno i zwięźle po polsku, dostarczając odpowiednie sugestie."
        }
        
        # Category-specific system prompts
        self.category_prompts = {
            'electronics': {
                'en': "You are Chaysh, an AI assistant specializing in electronics and technology. Provide expert advice about gadgets, devices, and technical solutions.",
                'pl': "Jesteś Chaysh, asystentem AI specjalizującym się w elektronice i technologii. Zapewnij eksperckie porady dotyczące gadżetów, urządzeń i rozwiązań technicznych."
            },
            'sports': {
                'en': "You are Chaysh, an AI assistant specializing in sports and fitness. Provide expert advice about training, equipment, and sports activities.",
                'pl': "Jesteś Chaysh, asystentem AI specjalizującym się w sporcie i fitnessie. Zapewnij eksperckie porady dotyczące treningu, sprzętu i aktywności sportowych."
            },
            'travel': {
                'en': "You are Chaysh, an AI assistant specializing in travel. Provide expert advice about destinations, planning, and travel tips.",
                'pl': "Jesteś Chaysh, asystentem AI specjalizującym się w podróżach. Zapewnij eksperckie porady dotyczące destynacji, planowania i wskazówek podróżniczych."
            },
            'health': {
                'en': "You are Chaysh, an AI assistant specializing in health and wellness. Provide expert advice about physical and mental health, while noting that you're not a medical professional.",
                'pl': "Jesteś Chaysh, asystentem AI specjalizującym się w zdrowiu i dobrym samopoczuciu. Zapewnij eksperckie porady dotyczące zdrowia fizycznego i psychicznego, zaznaczając, że nie jesteś profesjonalistą medycznym."
            },
            'food': {
                'en': "You are Chaysh, an AI assistant specializing in food and cooking. Provide expert advice about recipes, cooking techniques, and nutrition.",
                'pl': "Jesteś Chaysh, asystentem AI specjalizującym się w jedzeniu i gotowaniu. Zapewnij eksperckie porady dotyczące przepisów, technik gotowania i żywienia."
            },
            'finance': {
                'en': "You are Chaysh, an AI assistant specializing in finance. Provide expert advice about investments, savings, and financial planning, while noting that you're not a financial advisor.",
                'pl': "Jesteś Chaysh, asystentem AI specjalizującym się w finansach. Zapewnij eksperckie porady dotyczące inwestycji, oszczędności i planowania finansowego, zaznaczając, że nie jesteś doradcą finansowym."
            },
            'legal': {
                'en': "You are Chaysh, an AI assistant specializing in legal matters. Provide general legal information and guidance, while noting that you're not a lawyer and this isn't legal advice.",
                'pl': "Jesteś Chaysh, asystentem AI specjalizującym się w sprawach prawnych. Zapewnij ogólne informacje i wskazówki prawne, zaznaczając, że nie jesteś prawnikiem i nie jest to porada prawna."
            }
        }
        
        # Category-specific suggestions
        self.category_suggestions = {
            'electronics': {
                'en': [
                    "What specific features are you looking for?",
                    "Would you like to compare different models?",
                    "Do you need help with troubleshooting?"
                ],
                'pl': [
                    "Jakie konkretne funkcje Cię interesują?",
                    "Czy chciałbyś porównać różne modele?",
                    "Czy potrzebujesz pomocy w rozwiązywaniu problemów?"
                ]
            },
            'sports': {
                'en': [
                    "What's your current fitness level?",
                    "Are you looking for specific training tips?",
                    "Do you need equipment recommendations?"
                ],
                'pl': [
                    "Jaki jest Twój obecny poziom sprawności?",
                    "Czy szukasz konkretnych wskazówek treningowych?",
                    "Czy potrzebujesz rekomendacji sprzętu?"
                ]
            },
            'travel': {
                'en': [
                    "What's your destination?",
                    "Are you planning a specific type of trip?",
                    "Do you need help with travel arrangements?"
                ],
                'pl': [
                    "Jaki jest Twój cel podróży?",
                    "Czy planujesz konkretny rodzaj wycieczki?",
                    "Czy potrzebujesz pomocy w organizacji podróży?"
                ]
            },
            'health': {
                'en': [
                    "What specific health concerns do you have?",
                    "Are you looking for lifestyle advice?",
                    "Would you like information about preventive care?"
                ],
                'pl': [
                    "Jakie masz konkretne obawy zdrowotne?",
                    "Czy szukasz porad dotyczących stylu życia?",
                    "Czy chciałbyś informacji o profilaktyce?"
                ]
            },
            'food': {
                'en': [
                    "What type of cuisine interests you?",
                    "Are you looking for specific recipes?",
                    "Do you need cooking tips?"
                ],
                'pl': [
                    "Jaka kuchnia Cię interesuje?",
                    "Czy szukasz konkretnych przepisów?",
                    "Czy potrzebujesz wskazówek kulinarnych?"
                ]
            },
            'finance': {
                'en': [
                    "What are your financial goals?",
                    "Are you looking for investment advice?",
                    "Do you need help with budgeting?"
                ],
                'pl': [
                    "Jakie są Twoje cele finansowe?",
                    "Czy szukasz porad inwestycyjnych?",
                    "Czy potrzebujesz pomocy w budżetowaniu?"
                ]
            },
            'legal': {
                'en': [
                    "What type of legal information do you need?",
                    "Are you looking for general guidance?",
                    "Do you need help understanding specific laws?"
                ],
                'pl': [
                    "Jakich informacji prawnych potrzebujesz?",
                    "Czy szukasz ogólnych wskazówek?",
                    "Czy potrzebujesz pomocy w zrozumieniu konkretnych przepisów?"
                ]
            }
        }
        
    def _truncate_prompt(self, prompt: str, max_length: int = 600) -> str:
        """Truncate prompt to max length."""
        return prompt[:max_length] if len(prompt) > max_length else prompt
        
    async def process_query(self, query: str, lang: str = 'en') -> Dict[str, Any]:
        """Process a user query and return AI response with suggestions."""
        try:
            # Truncate user input
            truncated_query = self._truncate_prompt(query)
            
            # Classify the query
            category = classify_prompt(truncated_query)
            
            # Get appropriate system prompt
            if category in self.category_prompts:
                system_prompt = self.category_prompts[category][lang]
            else:
                system_prompt = self.base_prompts[lang]
            
            headers = {
                "Authorization": f"Bearer {api_key}",
                "Content-Type": "application/json",
                "HTTP-Referer": "https://chaysh-1.onrender.com",
                "X-Title": "Chaysh AI Assistant"
            }
            
            data = {
                "model": self.model,
                "messages": [
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": truncated_query}
                ],
                "temperature": self.temperature,
                "max_tokens": self.max_tokens,
                "top_p": self.top_p
            }
            
            print(f"Making API request to {self.api_url} with model {self.model}")
            
            async with httpx.AsyncClient() as client:
                response = await client.post(
                    self.api_url,
                    headers=headers,
                    json=data
                )
                
                if response.status_code == 401:
                    print("API Error: Unauthorized - Invalid or missing API key")
                    error_msg = "I apologize, but I'm currently unable to process requests due to an authentication issue. Please try again later."
                    if lang == 'pl':
                        error_msg = "Przepraszam, ale obecnie nie mogę przetwarzać żądań z powodu problemu z uwierzytelnianiem. Spróbuj ponownie później."
                    return {
                        "error": "Authentication failed",
                        "response": error_msg,
                        "suggestions": [],
                        "category": category
                    }
                
                response.raise_for_status()
                result = response.json()
                
                # Extract and truncate the assistant's message
                assistant_message = result['choices'][0]['message']['content']
                truncated_response = self._truncate_prompt(assistant_message, 500)  # Increased truncation limit
                
                # Get category-specific suggestions and limit to 3
                suggestions = self._generate_suggestions(truncated_query, category, lang)
                if suggestions and len(suggestions) > 3:
                    suggestions = suggestions[:3]
                
                return {
                    "response": truncated_response,
                    "suggestions": suggestions,
                    "category": category
                }
                
        except httpx.HTTPStatusError as e:
            print(f"HTTP Error: {e.response.status_code} - {e.response.text}")
            error_msg = "I apologize, but I encountered an error while processing your request. Please try again later."
            if lang == 'pl':
                error_msg = "Przepraszam, ale napotkałem błąd podczas przetwarzania Twojego żądania. Spróbuj ponownie później."
            return {
                "error": f"API request failed: {e.response.status_code}",
                "response": error_msg,
                "suggestions": [],
                "category": "unknown"
            }
        except Exception as e:
            print(f"Error processing query: {str(e)}")
            error_msg = "I apologize, but I encountered an unexpected error. Please try again later."
            if lang == 'pl':
                error_msg = "Przepraszam, ale napotkałem nieoczekiwany błąd. Spróbuj ponownie później."
            return {
                "error": str(e),
                "response": error_msg,
                "suggestions": [],
                "category": "unknown"
            }
    
    def _generate_suggestions(self, query: str, category: str, lang: str = 'en') -> List[str]:
        """Generate relevant follow-up suggestions based on the query, category, and language."""
        if category in self.category_suggestions:
            return self.category_suggestions[category][lang][:3]
        return []  # Return empty list for unknown categories 