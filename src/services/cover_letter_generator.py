# src/services/cover_letter_generator.py

import re
from typing import List
import openai
from tenacity import (
    retry,
    stop_after_attempt,
    wait_exponential,
    retry_if_exception_type
)


class CoverLetterGenerator:

    def __init__(self, gpt_model: str, api_key: str):
        """Initialise le générateur avec la clé API OpenAI."""
        self.gpt_model = gpt_model  # Stocke le modèle comme attribut d'instance
        openai.api_key = api_key

    @retry(
        retry=retry_if_exception_type((openai.RateLimitError, openai.APIError)),
        wait=wait_exponential(multiplier=1, min=4, max=60),
        stop=stop_after_attempt(5)
    )
    def generate_cover_letter(self, cv_content: str, job_offer: str,
                              existing_letters: List[str]) -> str:
        """Génère une nouvelle lettre de motivation en utilisant GPT avec gestion des limites de taux."""
        try:
            structure = self.extract_cover_letter_structure(existing_letters)

            prompt = f"""En utilisant les informations suivantes :
            # ... reste du prompt inchangé ..."""

            response = openai.chat.completions.create(
                model=self.gpt_model,  # Utilise le modèle stocké
                messages=[{
                    "role": "system",
                    "content": "Vous êtes un expert en rédaction de lettres de motivation professionnelles."
                }, {
                    "role": "user",
                    "content": prompt
                }],
                temperature=0.7,
                max_tokens=1000
            )

            return response.choices[0].message.content

        except openai.RateLimitError as e:
            print(f"Limite de taux atteinte. Nouvelle tentative dans quelques secondes...")
            raise  # Le décorateur retry s'occupera de réessayer

        except openai.APIError as e:
            print(f"Erreur API OpenAI : {str(e)}")
            raise  # Le décorateur retry s'occupera de réessayer

        except Exception as e:
            print(f"Erreur inattendue : {str(e)}")
            raise


    def read_tex_file(self, file_path: str) -> str:
        """Lit et nettoie le contenu d'un fichier TEX."""
        with open(file_path, 'r', encoding='utf-8') as file:
            content = file.read()
            # Supprime les commandes LaTeX basiques
            content = re.sub(r'\\[a-zA-Z]+{([^}]*)}', r'\1', content)
            # Supprime les autres éléments LaTeX
            content = re.sub(r'\\[a-zA-Z]+', ' ', content)
            return content.strip()

    def read_txt_file(self, file_path: str) -> str:
        """Lit le contenu d'un fichier texte."""
        with open(file_path, 'r', encoding='utf-8') as file:
            return file.read().strip()

    def extract_cover_letter_structure(self, cover_letters: List[str]) -> str:
        """Analyse la structure des lettres de motivation existantes."""
        structure = "Structure commune observée:\n"
        for i, letter in enumerate(cover_letters, 1):
            paragraphs = letter.split('\n\n')
            structure += f"\nLettre {i}:\n"
            for j, para in enumerate(paragraphs, 1):
                structure += f"- Paragraphe {j}: {para[:100]}...\n"
        return structure

    def generate_cover_letter(self, cv_content: str, job_offer: str,
                              existing_letters: List[str]) -> str:
        """Génère une nouvelle lettre de motivation en utilisant GPT."""
        structure = self.extract_cover_letter_structure(existing_letters)

        prompt = f"""En utilisant les informations suivantes :

CV :
{cv_content}

Offre d'emploi :
{job_offer}

Structure des lettres de motivation précédentes :
{structure}

Générez une lettre de motivation professionnelle en français qui :
1. Suit une structure similaire aux lettres précédentes
2. Utilise spécifiquement les informations pertinentes du CV, en mentionnant les éléments factuels et eventuellement techniques qui pourraient correspondre aux exigences ou à l'environement mentionné dans l'offre d'emploi
3. Fait référence aux exigences de l'offre d'emploi
4. Est personnalisée et convaincante
"""

        response = openai.chat.completions.create(
            #model="gpt-4-turbo-preview",
            model="gpt-3.5-turbo",
            messages=[{
                "role": "system",
                "content": "Vous êtes un expert en rédaction de lettres de motivation professionnelles."
            }, {
                "role": "user",
                "content": prompt
            }],
            temperature=0.7,
            max_tokens=1000
        )

        return response.choices[0].message.content

