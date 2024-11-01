#!/usr/local/bin/python3
__author__ = 'Louis Volant'
__version__ = 1.0

import argparse, logging, os
from datetime import datetime
from src.services.cover_letter_generator import CoverLetterGenerator

# README
# Beware : need an OpenAI API key
# export OPENAI_API_KEY='your-api-key'
# execute with
# python3 -m venv myenv
# source myenv/bin/activate
# pip install -r requirements.txt
# python3 main.py -cv mon_cv.tex -of job-opening-position.txt -cl Lettre-de-Motivation-Entreprise-A.txt Lettre-de-Motivation-Entreprise-B.txt
# Once finished, simply desactivate the virtual environment using "deactivate"


def main():
    # Générer le nom du fichier avec la date et l'heure actuelles
    timestamp = datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
    default_output = f'lettre_motivation_generee_{timestamp}.txt'

    parser = argparse.ArgumentParser(description='Générateur de lettre de motivation')
    parser.add_argument('-cv', required=True, help='Chemin vers le CV (format .tex)')
    parser.add_argument('-of', required=True, help='Chemin vers l\'offre d\'emploi (format .txt)')
    parser.add_argument('-cl', required=True, nargs='+',
                        help='Chemins vers les lettres de motivation existantes (format .txt)')
    parser.add_argument('--output', default=default_output,
                        help='Chemin du fichier de sortie')

    args = parser.parse_args()

    # Vérification de la clé API
    api_key = os.getenv('OPENAI_API_KEY')
    if not api_key:
        raise ValueError("La clé API OpenAI n'est pas définie dans les variables d'environnement.")

    generator = CoverLetterGenerator("gpt-3.5-turbo",  # Au lieu de "gpt-4-turbo-preview"
        api_key)

    # Lecture des fichiers
    cv_content = generator.read_tex_file(args.cv)
    job_offer = generator.read_txt_file(args.of)
    existing_letters = [generator.read_txt_file(path) for path in args.cl]

    # Génération de la nouvelle lettre
    new_letter = generator.generate_cover_letter(cv_content, job_offer, existing_letters)

    # Sauvegarde du résultat
    with open(args.output, 'w', encoding='utf-8') as f:
        f.write(new_letter)

    print(f"Lettre de motivation générée et sauvegardée dans : {args.output}")


if __name__ == '__main__':
    ## Initialize logging before hitting main, in case we need extra debuggability
    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(funcName)s - %(levelname)s - %(message)s')
    main()