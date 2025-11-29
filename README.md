# AppClockAndRemind 🕐📚

A lightweight desktop application for learning English with a flip clock and reminder system.

## Features

- **Flip Clock Display**: Modern flip clock showing hours, minutes, and seconds
- **Daily Reminders**: Set custom reminders for English learning tasks
- **Lightweight**: Built with Python + PyQt6 for minimal RAM usage (~50-80MB)
- **Simple & Fast**: Intuitive UI with quick performance
- **Cross-Platform**: Works on Windows, macOS, and Linux

## Installation

### Requirements
- Python 3.10+
- PyQt6

### Setup

1. Clone or download the project
2. Install dependencies:
```bash
pip install -r requirements.txt
```

## Running the Application

```bash
python main.py
```

## Project Structure

```
AppClockAndRemind/
├── main.py                 # Entry point
├── requirements.txt        # Python dependencies
├── README.md              # This file
├── assets/                # Images, icons, etc.
└── src/
    ├── ui/
    │   ├── main_window.py # Main application window
    │   └── widgets/
    │       ├── flip_clock.py      # Flip clock widget
    │       └── reminders_panel.py # Reminders panel widget
    └── models/
        └── reminder.py    # Reminder data model
```

## Features Roadmap

- [ ] Sound notifications for reminders
- [ ] Persistent reminder storage (JSON/SQLite)
- [ ] Dark/Light theme support
- [ ] System tray integration
- [ ] Custom sound settings
- [ ] Vocabulary practice mode
- [ ] Statistics dashboard

## Development

To contribute or modify:

1. Edit files in `src/` directory
2. Test changes by running `python main.py`
3. Keep the code lightweight and efficient

## License

MIT License

## Author

Created for English learning enthusiasts who want a simple, lightweight learning companion.
