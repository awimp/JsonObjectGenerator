import json
import random
import string

def load_json_schema_from_file(file_path):
    with open(file_path, 'r') as file:
        schema = json.load(file)
    return schema

def generate_random_object(schema):
    def generate_value(property_schema):
        if "type" not in property_schema and "anyOf" not in property_schema:
            return None
        
        if "anyOf" in property_schema:
            # Вибираємо варіант, який не є null
            non_null_options = [opt for opt in property_schema["anyOf"] if opt.get("type") != "null"]
            if not non_null_options:
                return None  # Якщо немає інших варіантів, повертаємо None
            chosen_schema = random.choice(non_null_options)
            return generate_value(chosen_schema)
        
        prop_type = property_schema.get("type")
        
        if prop_type == "string":
            length = property_schema.get("minLength", 5)
            return ''.join(random.choices(string.ascii_letters + string.digits, k=length))
        
        elif prop_type == "integer":
            minimum = property_schema.get("minimum", 0)
            maximum = property_schema.get("maximum", 100)
            return random.randint(minimum, maximum)
        
        elif prop_type == "number":
            minimum = property_schema.get("minimum", 0.0)
            exclusive_minimum = property_schema.get("exclusiveMinimum", None)
            if exclusive_minimum is not None:
                minimum = exclusive_minimum
            maximum = property_schema.get("maximum", 100.0)
            return round(random.uniform(minimum, maximum), 2)  # Генеруємо число з плаваючою точкою
        
        elif prop_type == "boolean":
            return random.choice([True, False])
        
        elif prop_type == "array":
            items_schema = property_schema.get("items", {})
            length = property_schema.get("minItems", 1)
            generated_items = [generate_value(items_schema) for _ in range(length)]
            # Фільтруємо null значення
            generated_items = [item for item in generated_items if item is not None]
            # Якщо після фільтрації масив порожній або містить null, генеруємо коректний елемент
            if not generated_items or any(item is None for item in generated_items):
                generated_items = [generate_value(items_schema) for _ in range(length) if generate_value(items_schema) is not None]
            return generated_items
        
        elif prop_type == "object":
            return {key: generate_value(value_schema) for key, value_schema in property_schema.get("properties", {}).items()}
        
        elif "enum" in property_schema:
            return random.choice(property_schema["enum"])
        
        return None
    
    return generate_value(schema)

# Завантажуємо схему з локального файлу
schema = load_json_schema_from_file('schema.json')

# Генеруємо випадковий об'єкт на основі схеми
generated_object = generate_random_object(schema)
print(json.dumps(generated_object, indent=2))
