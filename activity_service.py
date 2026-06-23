from database import ActivityDatabase
from datetime import datetime, date

class ActivityService:
    def __init__(self):
        self.db = ActivityDatabase()

    def log_activity(self, description, category, notes=""):
        return self.db.add_activity(description, category, notes)

    def get_today(self):
        return self.db.get_todays_activities()

    def get_history(self):
        return self.db.get_all_activities()

    def get_stats(self):
        today = date.today().strftime('%Y-%m-%d')
        return self.db.get_activity_stats(today)

    def delete(self, activity_id):
        return self.db.delete_activity(activity_id)

    def clear_all(self):
        return self.db.clear_all_activities()