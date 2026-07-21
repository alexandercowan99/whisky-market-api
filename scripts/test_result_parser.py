from app.services.cleaning import parse_lot_result_string


def main():
    examples = [
        "RESULT £450 SOLD",
        "RESULT\n$18,000\nSOLD",
        "RESULT UNSOLD",
        "",
        None,
    ]

    for example in examples:
        print("Input:")
        print(example)
        print("Parsed:")
        print(parse_lot_result_string(example))
        print("-" * 40)


if __name__ == "__main__":
    main()