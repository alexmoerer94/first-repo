# Activity Tracker - Python Mobile App

A Python-based mobile application that tracks your daily activities by asking you hourly what you did in the previous hour.

## Features

✅ **Hourly Notifications** - Get reminded every hour to log your activities
✅ **Activity Logging** - Quick and easy logging with categories and notes
✅ **Activity History** - View all past activities organized by date
✅ **Statistics** - Track your activity patterns
✅ **Data Export** - Export your data as JSON
✅ **Local Storage** - All data stored locally using SQLite

## Tech Stack

- **Python 3.8+** - Core application language
- **Kivy 2.2.1** - Cross-platform mobile UI framework
- **SQLite3** - Local database for activity storage
- **Plyer** - Platform-independent notifications

## Project Structure

```
activity-tracker/
├── main.py                 # Main application entry point
├── database.py             # SQLite database management
├── notifications.py        # Notification handling
├── activity_tracker.kv     # Kivy UI layout (optional)
├── requirements.txt        # Python dependencies
├── buildozer.spec         # Build configuration for mobile
└── README.md              # This file
```

## Installation

### Prerequisites
- Python 3.8 or higher
- pip (Python package manager)

### Setup

1. **Clone the repository**
   ```bash
   git clone https://github.com/alexmoerer94/activity-tracker.git
   cd activity-tracker
   ```

2. **Create a virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

## Running the App

### Desktop (Testing)
```bash
python main.py
```

### Mobile (Android/iOS)

Using Buildozer:
```bash
buildozer android debug
buildozer ios debug
```

## Usage

### Logging Activities

1. Open the app and go to the **"Log Activity"** tab
2. Enter what you did in the past hour
3. Select a category (Work, Break, Exercise, Social, Learning, Other)
4. Add optional notes
5. Tap **"Log Activity"**

### Viewing History

- Navigate to the **"History"** tab to see all your logged activities
- Activities are organized by date
- Click **"Delete"** on any activity to remove it

### Settings

In the **"Settings"** tab you can:
- View statistics about your activities
- Send a test notification
- Export your data as JSON
- Clear all data

## Database Schema

### Activities Table
```sql
CREATE TABLE activities (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    timestamp TEXT NOT NULL,           -- ISO format timestamp
    date TEXT NOT NULL,                 -- YYYY-MM-DD format
    hour INTEGER NOT NULL,              -- Hour (0-23)
    description TEXT NOT NULL,          -- Activity description
    category TEXT NOT NULL,             -- Activity category
    notes TEXT,                         -- Optional notes
    created_at TEXT NOT NULL            -- Creation timestamp
);
```

## API Reference

### Database Operations

```python
from database import ActivityDatabase

db = ActivityDatabase()

# Add activity
activity = db.add_activity(
    description="Team meeting",
    category="work",
    notes="Discussed Q2 goals"
)

# Get today's activities
today_activities = db.get_todays_activities()

# Get activities by date
activities = db.get_activities_by_date('2024-01-15')

# Get all activities
all_activities = db.get_all_activities()

# Delete activity
db.delete_activity(activity_id)

# Get statistics
stats = db.get_activity_stats('2024-01-15')

# Export as JSON
json_data = db.export_to_json()
```

### Notifications

```python
from notifications import NotificationManager

notif_manager = NotificationManager()

# Start hourly notifications
notif_manager.start_hourly_notifications()

# Send test notification
notif_manager.send_test_notification()

# Stop notifications
notif_manager.stop_hourly_notifications()
```

## Categories

The app includes 6 default activity categories:
- **Work** - Professional tasks
- **Break** - Relaxation and downtime
- **Exercise** - Physical activity
- **Social** - Time with others
- **Learning** - Educational activities
- **Other** - Miscellaneous

## Data Export

Your activities can be exported as JSON for backup or analysis:
```json
[
    {
        "id": 1,
        "timestamp": "2024-01-15T10:30:00",
        "date": "2024-01-15",
        "hour": 10,
        "description": "Team meeting",
        "category": "work",
        "notes": "Discussed Q2 goals",
        "created_at": "2024-01-15T10:30:00"
    }
]
```

## Troubleshooting

### Notifications not working
- Check that notifications are enabled in system settings
- On Linux: ensure `notify-send` is installed
- On macOS: check system notification preferences

### Database errors
- Delete `activity_tracker.db` to reset the database
- Ensure write permissions in the app directory

### Build issues
- Run `buildozer clean` before building
- Check that Android SDK/NDK are properly installed
- For iOS, ensure Xcode is installed

## Future Enhancements

- [ ] Analytics dashboard with charts
- [ ] Weekly/monthly reports
- [ ] Cloud sync functionality
- [ ] Multiple user accounts
- [ ] Activity templates/quick actions
- [ ] Dark mode
- [ ] Export to CSV/PDF
- [ ] Activity goal tracking

## License

MIT License - See LICENSE file for details

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## Author

Created by alexmoerer94

## Support

For issues or questions, please open an issue on the GitHub repository.
