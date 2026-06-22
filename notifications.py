from datetime import datetime, timedelta, date
from plyer import notification
import threading
import time

class NotificationManager:
    """Manages hourly notifications for activity check-ins"""
    
    def __init__(self, on_notification_callback=None):
        self.notifications_enabled = True
        self.on_notification_callback = on_notification_callback
        self.notification_thread = None
    
    def start_hourly_notifications(self):
        """Start the hourly notification service"""
        if self.notification_thread is None or not self.notification_thread.is_alive():
            self.notification_thread = threading.Thread(
                target=self._notification_loop,
                daemon=True
            )
            self.notification_thread.start()
    
    def stop_hourly_notifications(self):
        """Stop the hourly notification service"""
        self.notifications_enabled = False
    
    def _notification_loop(self):
        """Background thread that sends notifications every hour"""
        self.notifications_enabled = True
        
        while self.notifications_enabled:
            now = datetime.now()
            
            # Calculate seconds until next hour
            next_hour = (now + timedelta(hours=1)).replace(
                minute=0, second=0, microsecond=0
            )
            seconds_until_next = (next_hour - now).total_seconds()
            
            # Wait until next hour (or check every minute for responsiveness)
            check_interval = min(60, seconds_until_next)
            time.sleep(check_interval)
            
            # Send notification if still enabled
            if self.notifications_enabled:
                self._send_notification()
    
    def _send_notification(self):
        """Send an activity check-in notification"""
        try:
            now = datetime.now()
            hour = now.hour
            
            message = f"Time to log what you did in the past hour! ({hour}:00)"
            title = "Activity Check-in"
            
            # Send platform-specific notification
            notification.notify(
                title=title,
                message=message,
                timeout=10
            )
            
            # Call callback if provided
            if self.on_notification_callback:
                self.on_notification_callback()
        
        except Exception as e:
            print(f"Error sending notification: {e}")
    
    def send_test_notification(self):
        """Send a test notification immediately"""
        try:
            notification.notify(
                title="Activity Tracker",
                message="Test notification - App is working!",
                timeout=5
            )
        except Exception as e:
            print(f"Error sending test notification: {e}")
    
    def is_enabled(self) -> bool:
        """Check if notifications are enabled"""
        return self.notifications_enabled
