def parser(config_file: str) -> dict:
    config: dict = {}
    errors = []

    required = {
        "width": int,
        "height": int,
        "entry": tuple,
        "exit": tuple,
        "output_file": str,
        "perfect": bool,
    }

    try:
        with open(config_file, "r") as f:
            for lineno, line in enumerate(f, start=1):
                raw = line.strip()

                if not raw or raw.startswith("#"):
                    continue

                if "=" not in raw:
                    errors.append(f"Line {lineno}: missing '='")
                    continue

                key, value = raw.split("=", 1)
                key = key.strip().lower()
                value_str = value.strip()

                if key not in required:
                    errors.append(f"Line {lineno}: unknown key '{key}'")
                    continue

                if key in config:
                    errors.append(f"Line {lineno}: duplicate key '{key}'")
                    continue

                expected = required[key]

                if expected is tuple:
                    try:
                        parts = value_str.split(",")
                        if len(parts) != 2:
                            raise ValueError
                        parsed_value: tuple | int | bool | str = tuple(
                            int(p.strip()) for p in parts
                        )
                    except ValueError:
                        errors.append(
                            f"Line {lineno}: '{key}' must be 'int,int'"
                        )
                        continue

                elif expected is int:
                    try:
                        parsed_value = int(value_str)
                    except ValueError:
                        errors.append(
                            f"Line {lineno}: '{key}' must be integer"
                        )
                        continue

                elif expected is bool:
                    if value_str.lower() == "true":
                        parsed_value = True
                    elif value_str.lower() == "false":
                        parsed_value = False
                    else:
                        errors.append(
                            f"Line {lineno}: '{key}' must be true/false"
                        )
                        continue

                elif expected is str:
                    parsed_value = value_str

                config[key] = parsed_value

        for key in required:
            if key not in config:
                errors.append(f"Missing required key '{key}'")

        if errors:
            print("❌ Config file errors:")
            for err in errors:
                print("  -", err)
            return {}

        return config

    except FileNotFoundError:
        print("❌ Config file not found")
        return {}

    except Exception as e:
        print(f"❌ Unexpected error: {e}")
        return {}
