from src.core.cli import CommandLineInterface
from src.logger.setup_logger import logger

def main() -> None:
    """
    Точка входа

    :returns: Ничего не возвращает
    :rtype: None
    """
    try:
        cli = CommandLineInterface()
        cli.start_cli()

    except KeyboardInterrupt:
        print('\nExit')
        logger.info('Exit')

    except Exception as e:
        print(f'Unexpected error: {e}')
        logger.error(f'Critical error: {e}')

if __name__ == '__main__':
    main()
