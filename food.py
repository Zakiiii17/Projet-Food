import requests
from bs4 import BeautifulSoup
import csv
import re

BASE_URL = "https://www.infocalories.fr/calories/calories-{}.php"
FAT_THRESHOLD = 20.0  # percentage


class Food:
    """class food"""

    __name = None
    __calories = None
    __fat = None
    __carbs = None
    __proteins = None

    # ── Getters / Setters ────────────────────────────────────────────────────

    def get_name(self):
        return self.__name

    def set_name(self, name):
        self.__name = name

    def get_calories(self):
        return self.__calories

    def set_calories(self, calories):
        self.__calories = calories

    def get_fat(self):
        return self.__fat

    def set_fat(self, fat):
        self.__fat = fat

    def get_carbs(self):
        return self.__carbs

    def set_carbs(self, carbs):
        self.__carbs = carbs

    def get_proteins(self):
        return self.__proteins

    def set_proteins(self, proteins):
        self.__proteins = proteins

    # ── Core methods ─────────────────────────────────────────────────────────

    def retrieve_food_infos(self, food_name):
        """Scrape food nutritional info from infocalories.fr."""
        slug = food_name.strip().lower().replace(" ", "-")
        url = BASE_URL.format(slug)

        response = requests.get(url)

        if not response.ok:
            raise ConnectionError(
                f"Request failed with status code {response.status_code} for '{food_name}'"
            )

        soup = BeautifulSoup(response.text, "html.parser")

        # Récupérer le nom via le h1
        title = soup.find("h1")
        if not title:
            raise ValueError(f"No product found for '{food_name}'")

        # "Calories dans la tomate" -> "Tomate"
        title_text = title.get_text(strip=True)
        if "dans " in title_text.lower():
            name = title_text.split("dans ")[-1].strip()
            # Supprimer les déterminants : le, la, les, l'
            for article in ["les ", "le ", "la ", "l'"]:
                if name.lower().startswith(article):
                    name = name[len(article):]
                    break
            self.set_name(name.capitalize())
        else:
            self.set_name(title_text)

        # Le bloc nutritionnel est dans un <h2> suivi de texte
        # Structure : "Calories : 21 Kcal", "0,8g de protéines", etc.
        page_text = soup.get_text()

        self.set_calories(self.__parse_value(page_text, r"Calories\s*:\s*([\d,\.]+)"))
        self.set_proteins(self.__parse_value(page_text, r"([\d,\.]+)\s*g\s*de\s*prot"))
        self.set_carbs(self.__parse_value(page_text, r"([\d,\.]+)\s*g\s*de\s*glucides"))
        self.set_fat(self.__parse_value(page_text, r"([\d,\.]+)\s*g\s*de\s*lipides"))

    def __parse_value(self, text, pattern):
        """Extract a float value from text using a regex pattern."""
        match = re.search(pattern, text)
        if match:
            return float(match.group(1).replace(",", "."))
        return 0.0

    def display_food_infos(self):
        """Display food properties in a formatted table."""
        separator = "-" * 60
        header = f"{'name':<20} {'calories':<12} {'fat':<8} {'carbs':<8} {'proteins'}"
        row = (
            f"{self.__name:<20} "
            f"{self.__calories:<12} "
            f"{self.__fat:<8} "
            f"{self.__carbs:<8} "
            f"{self.__proteins}"
        )
        print(separator)
        print(header)
        print(row)
        print(separator)

    def save_to_csv_file(self, file_name):
        """Save food properties to a CSV file."""
        with open(file_name, mode="w", newline="", encoding="utf-8") as file:
            writer = csv.writer(file)
            writer.writerow(["name", "calories", "fat", "carbs", "proteins"])
            writer.writerow([
                self.__name,
                self.__calories,
                self.__fat,
                self.__carbs,
                self.__proteins,
            ])

    def is_fat(self):
        """Return True if fat represents more than 20% of calories."""
        if not self.__calories or self.__calories == 0:
            return False
        fat_calories = self.__fat * 9
        fat_percentage = (fat_calories / self.__calories) * 100
        return fat_percentage > FAT_THRESHOLD
