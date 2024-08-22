import unittest
from random_object_generator import generate_random_object

class TestRandomObjectGeneration(unittest.TestCase):
    def test_string_generation(self):
        schema = {"type": "string", "minLength": 5}
        generated = generate_random_object(schema)
        self.assertIsInstance(generated, str)
        self.assertGreaterEqual(len(generated), 5)

    def test_integer_generation(self):
        schema = {"type": "integer", "minimum": 10, "maximum": 20}
        generated = generate_random_object(schema)
        self.assertIsInstance(generated, int)
        self.assertGreaterEqual(generated, 10)
        self.assertLessEqual(generated, 20)

    def test_boolean_generation(self):
        schema = {"type": "boolean"}
        generated = generate_random_object(schema)
        self.assertIn(generated, [True, False])

    def test_array_generation(self):
        schema = {
            "type": "array",
            "items": {"type": "integer", "minimum": 1, "maximum": 5},
            "minItems": 3
        }
        generated = generate_random_object(schema)
        self.assertIsInstance(generated, list)
        self.assertGreaterEqual(len(generated), 3)
        for item in generated:
            self.assertIsInstance(item, int)
            self.assertGreaterEqual(item, 1)
            self.assertLessEqual(item, 5)

if __name__ == "__main__":
    unittest.main()
