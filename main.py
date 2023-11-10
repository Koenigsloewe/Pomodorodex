from app.main_window import main
from app.setup import generate_config_file, generate_stylesheet, generate_db


if __name__ == '__main__':
    generate_config_file()
    generate_stylesheet()
    generate_db()
    main()
