from data_fetcher import fetch_data


def skin_types(animals):
    """Store skin types in new list from original animals list"""
    types = {animal.get("characteristics", {}).get("skin_type")
             for animal in animals
             if animal.get("characteristics", {}).get("skin_type")}

    return sorted(types)


def show_skin_types(animals):
    """Print available skin types"""
    for i, skin_type in enumerate(skin_types(animals), start=1):
        print(f"{i}. {skin_type}")


def animals_by_skin_type_serialized(animals, skin_type):
    """Filter animals by skin type and serialize them into an HTML string"""
    matching = [serialize_animal(animal) for animal in animals
                if animal.get("characteristics", {}).get("skin_type", "").lower() == skin_type.lower()]
    return "".join(matching)


def add_card_text_item(title, characteristics, key):
    """Helper function to render a list item (HTML <li> tag)"""
    value = characteristics.get(key)
    if not value:
        return ""
    if isinstance(value, list):
        value = value[0]
    return f"<li><strong>{title}:</strong> {value}</li>"


def serialize_animal(animal):
    """Serialize an animal into an HTML string"""
    characteristics = animal["characteristics"]

    return f"""
        <li class="cards__item">
            <div class="card__title">{animal['name']}</div>
            <div class="card__text">
                <ul>
                    {add_card_text_item("Diet", characteristics, "diet")}
                    {add_card_text_item("Skin Type", characteristics, "skin_type")}
                    {add_card_text_item("Location", animal, "locations")}
                    {add_card_text_item("Lifespan", characteristics, "lifespan")}
                    {add_card_text_item("Type", characteristics, "type")}
                </ul>
            </div>
        </li>
    """


def output_animal_html_file(template_path, output_path, replacements):
    """
    1. Read the HTML template file
    2. Iterate through a dictionary to replace certain strings in the template file with the correct data
    3. Write the HTML output file
    """
    try:
        with open(template_path, "r", encoding="utf-8") as file:
            html = file.read()

        for key, value in replacements.items():
            html = html.replace(key, value)

        with open(output_path, "w", encoding="utf-8") as file:
            file.write(html)

        print("Website was successfully generated to the file animals.html!")

    except FileNotFoundError as e:
        print(f"Template file not found: {e}")

    except PermissionError as e:
        print(f"Permission error: {e}")

    except OSError as e:
        print(f"File system error: {e}")


def main():
    """
    Load animal data from a JSON file, extract unique skin types,
    filter animals based on a user-provided skin type (case-insensitive),
    and generate an HTML file displaying the filtered results.
    """
    animal_name_input = input("Enter a name of an animal: ")

    animals = fetch_data(animal_name_input)

    if not animals:
        return

    skin_type_input = ""

    if len(skin_types(animals)) > 1:
        show_skin_types(animals)
        skin_type_input = input("What skin type do you want to use? ")
    else:
        skin_type_input = skin_types(animals)[0]
        print(f"Only one skin type available: {skin_type_input}. Autoselecting it for you...")

    if skin_type_input.lower() not in [t.lower() for t in skin_types(animals)]:
        print("Skin type not found. Try again...")
        return

    output_animal_html_file(
        "animals_template.html",
        "animals.html",
        {
            "__REPLACE_SUBTITLE_FILTERED_BY_SKIN_TYPE__":
                f"<h2>Animals filtered by skin type: {skin_type_input}</h2>",
            "__REPLACE_ANIMALS_INFO__":
                animals_by_skin_type_serialized(animals, skin_type_input)
        }
    )


if __name__ == "__main__":
    main()