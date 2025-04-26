from helper.logs.loggingHelper import log_info
from parser.update.parserUpdatePipeline import ParserUpdatePipeline


def main():
    """
    Main function for updating the parser
    """

    log_info("Starting updating the parser")
    ParserUpdatePipeline().run_update_pipeline()


if __name__ == "__main__":
    main()
