# Summer Dance Party School

## File Structure
This project follows the Python "src-layout" convention and separate frontend from backend

```text
my_game_project/
├── run.py                 # Entry point
├── requirements.txt       # Dependencies
├── assets/                # Static files (musics)
└── src/
    └── sdps/           # Main Python package (SummerDancePartySchool)
        ├── config.py      # Global configuration
        ├── backend/       # Animation & music decomposition logic
        ├── frontend/      # Rendering
        └── utils/         # Helper functions