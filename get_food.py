from food import Food
import argparse
import sys

print("Running script...")

parser = argparse.ArgumentParser("Food Informations")
parser.add_argument('-f', '--food', help="your food name", default='tomate')

# 1. Récupérer les arguments
args = parser.parse_args()

# 2. Récupérer et afficher les infos
food = Food()

try:
    food.retrieve_food_infos(args.food)
except ConnectionError as e:
    print(f"Erreur de connexion : {e}")
    sys.exit(1)
except ValueError as e:
    print(f"Aliment introuvable : {e}")
    sys.exit(1)

food.display_food_infos()

# 3. Afficher si l'aliment est gras
if food.is_fat():
    print(f"⚠️  '{args.food}' est un aliment gras (lipides > {20}% des calories).")
else:
    print(f"✅  '{args.food}' n'est pas considéré comme un aliment gras.")

# 4. Sauvegarder dans le CSV
food.save_to_csv_file("get_food.csv")
print("💾  Informations sauvegardées dans 'get_food.csv'.")