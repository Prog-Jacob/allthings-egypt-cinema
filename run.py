from config import get_config


args = get_config()
__import__(args.experiment).main(vars(args))
