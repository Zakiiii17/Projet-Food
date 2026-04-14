import unittest
from unittest.mock import patch, MagicMock
from food import Food


class TestFood(unittest.TestCase):
    """class test food"""

    def test_get_name(self):
        """test_get_name"""
        print('test_get_name')
        food_one = Food()
        food_two = Food()

        food_two.set_name('coconut')

        self.assertEqual(food_one.get_name(), None)
        self.assertEqual(food_two.get_name(), 'coconut')

    def test_is_fat(self):
        """test_is_fat
        you may test 3 different foods
        """
        print('test_is_fat')

        # Aliment gras : beurre (750 kcal, 83g lipides -> ~99% > 20%)
        beurre = Food()
        beurre.set_calories(750.0)
        beurre.set_fat(83.0)
        self.assertTrue(beurre.is_fat())

        # Aliment non gras : tomate (21 kcal, 0.3g lipides -> ~12% < 20%)
        tomate = Food()
        tomate.set_calories(21.0)
        tomate.set_fat(0.3)
        self.assertFalse(tomate.is_fat())

        # Cas limite : calories à zéro -> pas de division par zéro
        empty = Food()
        empty.set_calories(0)
        empty.set_fat(10.0)
        self.assertFalse(empty.is_fat())

    def test_get_calories(self):
        """test_get_calories"""
        print('test_get_calories')
        food_one = Food()
        food_two = Food()

        food_two.set_calories(21.0)

        self.assertEqual(food_one.get_calories(), None)
        self.assertEqual(food_two.get_calories(), 21.0)

    def test_get_fat(self):
        """test_get_fat"""
        print('test_get_fat')
        food_one = Food()
        food_two = Food()

        food_two.set_fat(0.3)

        self.assertEqual(food_one.get_fat(), None)
        self.assertEqual(food_two.get_fat(), 0.3)

    def test_get_carbs(self):
        """test_get_carbs"""
        print('test_get_carbs')
        food_one = Food()
        food_two = Food()

        food_two.set_carbs(4.6)

        self.assertEqual(food_one.get_carbs(), None)
        self.assertEqual(food_two.get_carbs(), 4.6)

    def test_get_proteins(self):
        """test_get_proteins"""
        print('test_get_proteins')
        food_one = Food()
        food_two = Food()

        food_two.set_proteins(0.8)

        self.assertEqual(food_one.get_proteins(), None)
        self.assertEqual(food_two.get_proteins(), 0.8)

    def test_retrieve_food_infos(self):
        """test_retrieve_food_infos"""
        print('test_retrieve_food_infos')

        fake_html = """
        <html><body>
            <h1>Tomate</h1>
            <p>Calories : 21 Kcal</p>
            <p>0,8g de protéines</p>
            <p>4,6g de glucides</p>
            <p>0,3g de lipides</p>
        </body></html>
        """
        mock_response = MagicMock()
        mock_response.ok = True
        mock_response.text = fake_html

        food_one = Food()
        with patch("food.requests.get", return_value=mock_response):
            food_one.retrieve_food_infos("tomate")

        self.assertEqual(food_one.get_name(), "Tomate")
        self.assertEqual(food_one.get_calories(), 21.0)
        self.assertEqual(food_one.get_proteins(), 0.8)
        self.assertEqual(food_one.get_carbs(), 4.6)
        self.assertEqual(food_one.get_fat(), 0.3)

    def test_retrieve_food_infos_connection_error(self):
        """test_retrieve_food_infos avec une erreur HTTP 404"""
        print('test_retrieve_food_infos_connection_error')

        mock_response = MagicMock()
        mock_response.ok = False
        mock_response.status_code = 404

        food_one = Food()
        with patch("food.requests.get", return_value=mock_response):
            with self.assertRaises(ConnectionError):
                food_one.retrieve_food_infos("alimentinconnu")

    def test_display_food_infos(self):
        """test_display_food_infos"""
        print('test_display_food_infos')

        food_one = Food()
        food_one.set_name("tomate")
        food_one.set_calories(21.0)
        food_one.set_fat(0.3)
        food_one.set_carbs(4.6)
        food_one.set_proteins(0.8)

        with patch("builtins.print") as mock_print:
            food_one.display_food_infos()
            printed = " ".join(str(c) for c in mock_print.call_args_list)
            self.assertIn("tomate", printed)
            self.assertIn("21.0", printed)

    def test_save_to_csv_file(self):
        """test_save_to_csv_file"""
        print('test_save_to_csv_file')
        import csv
        import os

        food_one = Food()
        food_one.set_name("tomate")
        food_one.set_calories(21.0)
        food_one.set_fat(0.3)
        food_one.set_carbs(4.6)
        food_one.set_proteins(0.8)

        test_file = "test_output.csv"
        food_one.save_to_csv_file(test_file)

        with open(test_file, newline="", encoding="utf-8") as f:
            reader = list(csv.reader(f))

        self.assertEqual(reader[0], ["name", "calories", "fat", "carbs", "proteins"])
        self.assertEqual(reader[1], ["tomate", "21.0", "0.3", "4.6", "0.8"])

        os.remove(test_file)  # Nettoyage après le test


if __name__ == '__main__':
    unittest.main()