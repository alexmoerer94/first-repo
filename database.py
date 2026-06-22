import sqlite3
from datetime import datetime, date
from typing import List, Dict, Optional
import os

DATABASE_PATH = 'activity_tracker.db'

class ActivityDatabase:
    """Manages all database operations for activities"""
    
    def __init__(self):
        self.db_path = DATABASE_PATH
        self.init_database()
    
    def init_database(self):
        """Initialize the database with required tables"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Create activities table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS activities (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                timestamp TEXT NOT NULL,
                date TEXT NOT NULL,
                hour INTEGER NOT NULL,
                description TEXT NOT NULL,
                category TEXT NOT NULL,
                notes TEXT,
                created_at TEXT NOT NULL
            )
        ''')
        
        conn.commit()
        conn.close()
    
    def add_activity(self, description: str, category: str, notes: str = "") -> Dict:
        """Add a new activity to the database"""
        try:
            now = datetime.now()
            activity = {
                'timestamp': now.isoformat(),
                'date': now.strftime('%Y-%m-%d'),
                'hour': now.hour,
                'description': description,
                'category': category,
                'notes': notes,
                'created_at': now.isoformat()
            }
            
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            cursor.execute('''
                INSERT INTO activities 
                (timestamp, date, hour, description, category, notes, created_at)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            ''', (
                activity['timestamp'],
                activity['date'],
                activity['hour'],
                activity['description'],
                activity['category'],
                activity['notes'],
                activity['created_at']
            ))
            
            activity['id'] = cursor.lastrowid
            conn.commit()
            conn.close()
            
            return activity
        except Exception as e:
            print(f"Error adding activity: {e}")
            raise
    
    def get_todays_activities(self) -> List[Dict]:
        """Get all activities for today"""
        today = date.today().strftime('%Y-%m-%d')
        return self.get_activities_by_date(today)
    
    def get_activities_by_date(self, date_str: str) -> List[Dict]:
        """Get activities for a specific date"""
        try:
            conn = sqlite3.connect(self.db_path)
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()
            
            cursor.execute('''
                SELECT * FROM activities 
                WHERE date = ?
                ORDER BY timestamp DESC
            ''', (date_str,))
            
            rows = cursor.fetchall()
            activities = [dict(row) for row in rows]
            conn.close()
            
            return activities
        except Exception as e:
            print(f"Error getting activities: {e}")
            return []
    
    def get_all_activities(self) -> List[Dict]:
        """Get all activities from database"""
        try:
            conn = sqlite3.connect(self.db_path)
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()
            
            cursor.execute('''
                SELECT * FROM activities 
                ORDER BY timestamp DESC
            ''')
            
            rows = cursor.fetchall()
            activities = [dict(row) for row in rows]
            conn.close()
            
            return activities
        except Exception as e:
            print(f"Error getting all activities: {e}")
            return []
    
    def delete_activity(self, activity_id: int) -> bool:
        """Delete an activity by ID"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            cursor.execute('DELETE FROM activities WHERE id = ?', (activity_id,))
            conn.commit()
            conn.close()
            
            return True
        except Exception as e:
            print(f"Error deleting activity: {e}")
            return False
    
    def update_activity(self, activity_id: int, description: str, 
                       category: str, notes: str) -> Optional[Dict]:
        """Update an activity"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            cursor.execute('''
                UPDATE activities 
                SET description = ?, category = ?, notes = ?
                WHERE id = ?
            ''', (description, category, notes, activity_id))
            
            conn.commit()
            conn.close()
            
            return self.get_activity_by_id(activity_id)
        except Exception as e:
            print(f"Error updating activity: {e}")
            return None
    
    def get_activity_by_id(self, activity_id: int) -> Optional[Dict]:
        """Get a specific activity by ID"""
        try:
            conn = sqlite3.connect(self.db_path)
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()
            
            cursor.execute('SELECT * FROM activities WHERE id = ?', (activity_id,))
            row = cursor.fetchone()
            conn.close()
            
            return dict(row) if row else None
        except Exception as e:
            print(f"Error getting activity: {e}")
            return None
    
    def get_activity_stats(self, date_str: str) -> Dict:
        """Get statistics for activities on a specific date"""
        try:
            activities = self.get_activities_by_date(date_str)
            
            stats = {
                'total_activities': len(activities),
                'categories': {},
                'timeline': {}
            }
            
            for activity in activities:
                # Count categories
                category = activity['category']
                stats['categories'][category] = stats['categories'].get(category, 0) + 1
                
                # Create timeline by hour
                hour = activity['hour']
                stats['timeline'][hour] = stats['timeline'].get(hour, 0) + 1
            
            return stats
        except Exception as e:
            print(f"Error getting stats: {e}")
            return {
                'total_activities': 0,
                'categories': {},
                'timeline': {}
            }
    
    def clear_all_activities(self) -> bool:
        """Delete all activities from database"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            cursor.execute('DELETE FROM activities')
            conn.commit()
            conn.close()
            return True
        except Exception as e:
            print(f"Error clearing database: {e}")
            return False
    
    def export_to_json(self) -> str:
        """Export all activities as JSON string"""
        import json
        activities = self.get_all_activities()
        return json.dumps(activities, indent=2)
