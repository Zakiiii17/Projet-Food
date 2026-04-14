from flask import Flask, render_template, request
from food import Food

app = Flask(__name__)


@app.route("/", methods=["GET", "POST"])
def index():
    food_data = None
    error = None

    if request.method == "POST":
        food_name = request.form.get("food_name", "").strip()
        if food_name:
            food = Food()
            try:
                food.retrieve_food_infos(food_name)
                food_data = {
                    "name": food.get_name(),
                    "calories": food.get_calories(),
                    "fat": food.get_fat(),
                    "carbs": food.get_carbs(),
                    "proteins": food.get_proteins(),
                }
            except ConnectionError:
                error = f"Aliment '{food_name}' introuvable sur infocalories.fr."
            except ValueError:
                error = f"Impossible de récupérer les informations pour '{food_name}'."

    return render_template("index.html", food_data=food_data, error=error)


if __name__ == "__main__":
    app.run(debug=True)