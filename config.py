import argparse
import warnings

warnings.formatwarning = lambda message, *_, **__: f"{message}\n"

save_path_args = {
    "type": str,
    "default": None,
    "help": "Path to the output CSV file.",
}

franco_args = {
    "--load-path": {
        "type": str,
        "default": "data-matches.csv",
        "help": "Path to the input CSV file.",
    },
    "--save-path": save_path_args,
    "--batch": {
        "type": int,
        "default": 0,
        "help": "Batch number for processing (0-indexed and 100 items per batch).",
    },
}

cross_check_args = {
    "--first-path": {
        "type": str,
        "default": None,
        "help": "Path to the first CSV file. Must have column 'Name'.",
    },
    "--second-path": {
        "type": str,
        "default": None,
        "help": "Path to the second CSV file. Must have column 'Title'.",
    },
    "--first-key": {
        "type": str,
        "default": "Name",
        "help": "Column name to use as the key in the first CSV file.",
    },
    "--second-key": {
        "type": str,
        "default": "Title",
        "help": "Column name to use as the key in the second CSV file.",
    },
    "--save-path": save_path_args,
    "--join-type": {
        "type": str,
        "default": "inner-right",
        "choices": ["inner-left", "inner-right", "outer", "left-outer", "right-outer"],
        "help": "Type of join to perform.",
    },
    "--is-fuzzy": {
        "type": bool,
        "default": False,
        "help": "If True, fuzzy matching will be used.",
    },
}

tmdb_discover_args = {
    "--save-path": save_path_args,
    "--exclude-movies": {
        "type": bool,
        "default": False,
        "help": "If True, no movies will be discovered.",
    },
    "--exclude-tv-shows": {
        "type": bool,
        "default": False,
        "help": "If True, no TV shows will be discovered.",
    },
}

tmdb_search_args = {
    "--save-path": save_path_args,
    "--query": {
        "type": str,
        "default": None,
        "help": "Search query for TMDB API.",
    },
}

llm_args = {
    "--system-message": {
        "type": str,
        "default": "You are a helpful assistant. Format your responses using Markdown when necessary.",
        "help": 'Define the behavior of the LLM. Example: "You are a movie expert. Answer the user\'s questions about movies."',
    },
    "--user-messages": {
        "nargs": "+",
        "type": str,
        "default": None,
        "help": "Say what you gotta say to the LLM model.",
    },
}


def get_config():
    parser = argparse.ArgumentParser(
        description="Experiments and Configuration for the Allthings Egypt Project."
    )
    experiment_subparsers = parser.add_subparsers(
        dest="experiment", required=True, help="Specify which script to run."
    )

    # Franco converters
    convert_franco_parser = experiment_subparsers.add_parser(
        "convert-franco",
        help="Convert Franco movie titles to their Arabic counterparts.",
    )
    convert_franco_parser.set_defaults(func=_set_defaults(franco_args))
    _add_arguments(convert_franco_parser, franco_args)

    is_franco_parser = experiment_subparsers.add_parser(
        "is-franco",
        help="Check whether movie titles are in Franco or Arabic (responds with NO) or not (responds with YES).",
    )
    is_franco_parser.set_defaults(func=_set_defaults(franco_args))
    _add_arguments(is_franco_parser, franco_args)

    # Cross-check
    cross_check_parser = experiment_subparsers.add_parser(
        "cross-check",
        help="Find movies in the destination CSV file, which the host CSV file doesn't contain.",
    )
    cross_check_parser.set_defaults(func=_set_defaults(cross_check_args))
    _add_arguments(cross_check_parser, cross_check_args)

    # TMDB API
    tmdb_parser = experiment_subparsers.add_parser(
        "tmdb-api",
        help="Discover or search Egyptian movies and TV shows in the TMDB API.",
    )
    tmdb_calls_parser = tmdb_parser.add_subparsers(
        dest="action", required=True, help="Choose TMDB action."
    )

    discover_parser = tmdb_calls_parser.add_parser(
        "discover", help="Discover Egyptian movies and TV shows."
    )
    _add_arguments(discover_parser, tmdb_discover_args)
    discover_parser.set_defaults(func=_set_defaults(tmdb_discover_args))

    search_parser = tmdb_calls_parser.add_parser(
        "search", help="Search for movies and TV shows given a query."
    )
    _add_arguments(search_parser, tmdb_search_args)
    search_parser.set_defaults(func=_set_defaults(tmdb_search_args))

    # LLM
    llm_parser = experiment_subparsers.add_parser(
        "LLM", help="Ask the running local LLM server any number of questions."
    )
    llm_parser.set_defaults(func=_set_defaults(llm_args))
    _add_arguments(llm_parser, llm_args)

    args = parser.parse_args()
    args.func(args)
    return args


def _add_arguments(parser, args_data):
    """Add arguments from dict configs, with autocomplete support if choices exist."""
    for key, value in args_data.items():
        parser.add_argument(
            key,
            help=value["help"],
            type=value["type"],
            nargs=value.get("nargs", None),
            required=value["default"] is None,
            choices=value.get("choices", None),
        )


def _set_defaults(args_defaults):
    def _process_args(args):
        for key, value in args_defaults.items():
            parsed_key = key.lstrip("-").replace("-", "_")
            if getattr(args, parsed_key) is None:
                setattr(args, parsed_key, value["default"])
                warnings.warn(f'Default value for {key} is used: "{value["default"]}"')

    return _process_args
