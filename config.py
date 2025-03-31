import argparse
import warnings

llm_args = {
    "--load-path": {
        "type": str,
        "default": "data-matches.csv",
        "help": "Path to the input CSV file.",
    },
    "--save-path": {
        "type": str,
        "default": None,
        "help": "Path to the output CSV file.",
    },
    "--batch": {
        "type": int,
        "default": 0,
        "help": "Batch number for processing (0-indexed and 100 items per batch).",
    },
}

cross_check_args = {
    "--host-path": {
        "type": str,
        "default": None,
        "help": "Path to the host CSV file.",
    },
    "--dest-path": {
        "type": str,
        "default": None,
        "help": "Path to the destination CSV file.",
    },
    "--save-path": {
        "type": str,
        "default": None,
        "help": "Path to the output CSV file.",
    },
}


def get_config(type):
    match type:
        case "llm":
            return _process_config(llm_args)
        case "cross_check":
            return _process_config(cross_check_args)
        case _:
            raise ValueError("Invalid configuration type specified.")


def _process_config(args_data):
    parser = argparse.ArgumentParser(description="LLM Configuration")
    for key, value in args_data.items():
        parser.add_argument(
            key,
            help=value["help"],
            type=value["type"],
            required=value["default"] is None,
        )
    args = vars(parser.parse_args())

    for key, value in args_data.items():
        parsed_key = key.lstrip("-").replace("-", "_")
        if args[parsed_key] is None:
            args[parsed_key] = value["default"]
            warnings.warn(f"Default value for {key} is used: {value['default']}")

    return args
