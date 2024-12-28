import requests
from typing import List, Dict

class ContentGenerator:
    def __init__(self):
        self.base_url = "http://localhost:11434/api/generate"
        self.model = "llama3.2:latest"  # or any other model you have pulled in Ollama
        
        self.base_prompts = {
            'article': """You are an expert English language teacher. Write an article about {topic} suitable for {level} English learners.
                        Requirements:
                        - For A1: Use present simple, common vocabulary, and very basic sentences
                        - For A2: Use present and past simple, everyday vocabulary, and simple sentences
                        - For B1: Use varied tenses, intermediate vocabulary, and mix of simple and complex sentences
                        - For B2: Use advanced vocabulary, complex grammar structures, and sophisticated sentence patterns
                        
                        Write the article now:""",
            
            'story': """You are an expert English language teacher. Write a story about {topic} suitable for {level} English learners.
                       Requirements:
                       - For A1: Use present simple, common vocabulary, and very basic sentences
                       - For A2: Use present and past simple, everyday vocabulary, and simple sentences
                       - For B1: Use varied tenses, intermediate vocabulary, and mix of simple and complex sentences
                       - For B2: Use advanced vocabulary, complex grammar structures, and sophisticated sentence patterns
                       
                       Write the story now:""",
            
            'news': """You are an expert English language teacher. Write a news report about {topic} suitable for {level} English learners.
                      Requirements:
                      - For A1: Use present simple, common vocabulary, and very basic sentences
                      - For A2: Use present and past simple, everyday vocabulary, and simple sentences
                      - For B1: Use varied tenses, intermediate vocabulary, and mix of simple and complex sentences
                      - For B2: Use advanced vocabulary, complex grammar structures, and sophisticated sentence patterns
                      
                      Write the news report now:"""
        }
        
        self.exercise_prompts = {
            'vocabulary': """Based on this text: 
                           {content}
                           
                           Create vocabulary exercises for {level} level English learners.
                           Include:
                           1. 5 key words with definitions
                           2. A matching exercise with 5 words and definitions
                           3. 5 fill-in-the-blank sentences using words from the text
                           
                           Format the response clearly with section headers.""",
            
            'grammar': """Based on this text:
                         {content}
                         
                         Create grammar exercises for {level} level English learners.
                         Include:
                         1. Identify 3 examples of key grammar structures used in the text
                         2. 5 fill-in-the-blank exercises focusing on these grammar points
                         3. 3 sentence transformation exercises
                         
                         Format the response clearly with section headers.""",
            
            'comprehension': """Based on this text:
                              {content}
                              
                              Create comprehension questions for {level} level English learners.
                              Include:
                              1. 5 factual questions about specific details in the text
                              2. 3 inference questions that require deeper understanding
                              3. 2 personal response questions related to the topic
                              
                              Format the response clearly with section headers.""",
            
            'writing': """Based on this text:
                         {content}
                         
                         Create writing exercises for {level} level English learners.
                         Include:
                         1. A guided writing task related to the topic
                         2. 3 preparatory exercises to help with the writing
                         3. A checklist of points to include in the writing
                         
                         Format the response clearly with section headers."""
        }

    def _generate_with_ollama(self, prompt: str) -> str:
        """
        Make a request to Ollama API and return the generated text.
        """
        try:
            response = requests.post(
                self.base_url,
                json={
                    "model": self.model,
                    "prompt": prompt,
                    "stream": False
                }
            )
            response.raise_for_status()
            return response.json()["response"]
        except requests.exceptions.RequestException as e:
            print(f"Error calling Ollama API: {e}")
            return f"Error generating content: {str(e)}"

    def generate_content(self, content_type: str, topic: str, level: str) -> str:
        """
        Generate main content using Ollama.
        """
        prompt = self.base_prompts[content_type].format(topic=topic, level=level)
        return self._generate_with_ollama(prompt)

    def generate_exercises(self, content: str, level: str, exercise_types: List[str]) -> List[Dict]:
        """
        Generate exercises based on the main content using Ollama.
        """
        exercises = []
        for ex_type in exercise_types:
            prompt = self.exercise_prompts[ex_type].format(level=level, content=content)
            exercise_content = self._generate_with_ollama(prompt)
            exercises.append({
                'type': ex_type,
                'content': exercise_content
            })
        return exercises