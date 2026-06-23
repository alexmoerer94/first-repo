from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.scrollview import ScrollView
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.uix.popup import Popup
# from kivy.core.window import Window (ChatGPT suggestion)
from kivy.uix.tabbedpanel import TabbedPanel, TabbedPanelItem
# from kivy.garden.matplotlib.backend_kivyagg import FigureCanvasKivyAgg
from datetime import datetime, date
# import json (ChatGPT suggestion) 

from database import ActivityDatabase
from notifications import NotificationManager

# Set window size for desktop testing (Paused now bc of ChatGPT)
# Window.size = (400, 800)
import os
from kivy.core.window import Window

if os.environ.get("KIVY_ENV") != "android":
    Window.size = (400, 800)
    
class ActivityTrackerApp(App):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.db = ActivityDatabase()
        self.notification_manager = NotificationManager(
            on_notification_callback=self.on_notification
        )
        self.current_category = 'work'
        self.categories = {
            'work': (1, 0.42, 0.42, 1),
            'break': (0.31, 0.8, 0.77, 1),
            'exercise': (0.27, 0.72, 0.82, 1),
            'social': (1, 0.63, 0.48, 1),
            'learning': (0.59, 0.85, 0.78, 1),
            'other': (0.58, 0.88, 0.83, 1),
        }

    def build(self):
        """Build the main app UI"""
        self.title = 'Activity Tracker'
        
        # Start notifications
        self.notification_manager.start_hourly_notifications()
        
        # Create tabbed interface
        tab_panel = TabbedPanel()
        tab_panel.default_tab_text = 'Home'
        
        # Home tab
        home_tab = TabbedPanelItem(text='Home')
        home_tab.content = self.build_home_screen()
        tab_panel.add_widget(home_tab)
        
        # Log Activity tab
        log_tab = TabbedPanelItem(text='Log Activity')
        log_tab.content = self.build_log_screen()
        tab_panel.add_widget(log_tab)
        
        # History tab
        history_tab = TabbedPanelItem(text='History')
        history_tab.content = self.build_history_screen()
        tab_panel.add_widget(history_tab)
        
        # Settings tab
        settings_tab = TabbedPanelItem(text='Settings')
        settings_tab.content = self.build_settings_screen()
        tab_panel.add_widget(settings_tab)
        
        return tab_panel

    def build_home_screen(self):
        """Build the home/dashboard screen"""
        layout = BoxLayout(orientation='vertical', padding=15, spacing=10)
        
        # Title
        title = Label(text="Today's Summary", size_hint_y=0.1, bold=True, font_size='24sp')
        layout.add_widget(title)
        
        # Stats grid
        stats_layout = GridLayout(cols=3, spacing=10, size_hint_y=0.15)
        
        today_activities = self.db.get_todays_activities()
        stats = self.db.get_activity_stats(date.today().strftime('%Y-%m-%d'))
        
        # Activities count
        activities_box = BoxLayout(orientation='vertical', padding=10)
        activities_box.add_widget(Label(text=str(stats['total_activities']), bold=True, font_size='24sp', color=(0, 0.48, 1, 1)))
        activities_box.add_widget(Label(text='Activities', font_size='12sp', color=(0.4, 0.4, 0.4, 1)))
        stats_layout.add_widget(activities_box)
        
        # Missing hours count
        missing_hours = self._calculate_missing_hours(today_activities)
        missing_box = BoxLayout(orientation='vertical', padding=10)
        missing_box.add_widget(Label(text=str(len(missing_hours)), bold=True, font_size='24sp', color=(0, 0.48, 1, 1)))
        missing_box.add_widget(Label(text='Hours Missing', font_size='12sp', color=(0.4, 0.4, 0.4, 1)))
        stats_layout.add_widget(missing_box)
        
        # Categories count
        categories_box = BoxLayout(orientation='vertical', padding=10)
        categories_box.add_widget(Label(text=str(len(stats['categories'])), bold=True, font_size='24sp', color=(0, 0.48, 1, 1)))
        categories_box.add_widget(Label(text='Categories', font_size='12sp', color=(0.4, 0.4, 0.4, 1)))
        stats_layout.add_widget(categories_box)
        
        layout.add_widget(stats_layout)
        
        # Activities list header
        header_box = BoxLayout(size_hint_y=0.08, spacing=10)
        header_box.add_widget(Label(text="Today's Activities", bold=True, font_size='18sp'))
        layout.add_widget(header_box)
        
        # Activities list
        scroll = ScrollView(size_hint_y=0.67)
        activities_container = GridLayout(cols=1, spacing=8, size_hint_y=None)
        activities_container.bind(minimum_height=activities_container.setter('height'))
        
        if today_activities:
            for activity in today_activities:
                activity_card = self._create_activity_card(activity)
                activities_container.add_widget(activity_card)
        else:
            activities_container.add_widget(Label(text='No activities logged yet', size_hint_y=None, height=50))
        
        scroll.add_widget(activities_container)
        layout.add_widget(scroll)
        
        return layout

    def build_log_screen(self):
        """Build the activity logging screen"""
        layout = BoxLayout(orientation='vertical', padding=15, spacing=10)
        
        scroll = ScrollView()
        scroll_layout = GridLayout(cols=1, spacing=15, size_hint_y=None)
        scroll_layout.bind(minimum_height=scroll_layout.setter('height'))
        
        # Current hour display
        current_hour = datetime.now().hour
        hour_box = BoxLayout(orientation='vertical', padding=15, size_hint_y=None, height=100)
        hour_box.add_widget(Label(text='Logging activity for hour:', color=(1, 1, 1, 1)))
        hour_box.add_widget(Label(text=f'{current_hour}:00', bold=True, font_size='48sp', color=(1, 1, 1, 1)))
        scroll_layout.add_widget(hour_box)
        
        # Description input
        description_label = Label(text='What did you do? *', bold=True, font_size='14sp', size_hint_y=None, height=30)
        scroll_layout.add_widget(description_label)
        
        self.description_input = TextInput(
            multiline=True,
            hint_text='e.g., Attended team meeting, went for a run...',
            size_hint_y=None,
            height=100
        )
        scroll_layout.add_widget(self.description_input)
        
        # Category selection
        category_label = Label(text='Category', bold=True, font_size='14sp', size_hint_y=None, height=30)
        scroll_layout.add_widget(category_label)
        
        category_grid = GridLayout(cols=3, spacing=5, size_hint_y=None, height=80)
        for category in ['work', 'break', 'exercise', 'social', 'learning', 'other']:
            btn = Button(text=category.capitalize())
            btn.bind(on_press=lambda instance, cat=category: self.set_category(cat))
            category_grid.add_widget(btn)
        scroll_layout.add_widget(category_grid)
        
        # Notes input
        notes_label = Label(text='Notes (Optional)', bold=True, font_size='14sp', size_hint_y=None, height=30)
        scroll_layout.add_widget(notes_label)
        
        self.notes_input = TextInput(
            multiline=True,
            hint_text='Add any additional details...',
            size_hint_y=None,
            height=80
        )
        scroll_layout.add_widget(self.notes_input)
        
        # Log button
        log_btn = Button(text='Log Activity', size_hint_y=None, height=60)
        log_btn.bind(on_press=self.log_activity)
        scroll_layout.add_widget(log_btn)
        
        scroll.add_widget(scroll_layout)
        layout.add_widget(scroll)
        
        return layout

    def build_history_screen(self):
        """Build the activity history screen"""
        layout = BoxLayout(orientation='vertical', padding=15, spacing=10)
        
        title = Label(text='Activity History', bold=True, font_size='24sp', size_hint_y=0.1)
        layout.add_widget(title)
        
        scroll = ScrollView()
        history_container = GridLayout(cols=1, spacing=10, size_hint_y=None)
        history_container.bind(minimum_height=history_container.setter('height'))
        
        all_activities = self.db.get_all_activities()
        
        if all_activities:
            # Group by date
            dates_dict = {}
            for activity in all_activities:
                date_str = activity['date']
                if date_str not in dates_dict:
                    dates_dict[date_str] = []
                dates_dict[date_str].append(activity)
            
            # Display each date group
            for date_str in sorted(dates_dict.keys(), reverse=True):
                date_label = Label(text=f'{date_str}', bold=True, size_hint_y=None, height=30)
                history_container.add_widget(date_label)
                
                for activity in dates_dict[date_str]:
                    card = self._create_activity_card(activity, show_delete=True)
                    history_container.add_widget(card)
        else:
            history_container.add_widget(Label(text='No activities yet', size_hint_y=None, height=50))
        
        scroll.add_widget(history_container)
        layout.add_widget(scroll)
        
        return layout

    def build_settings_screen(self):
        """Build the settings screen"""
        layout = BoxLayout(orientation='vertical', padding=15, spacing=10)
        
        scroll = ScrollView()
        scroll_layout = GridLayout(cols=1, spacing=15, size_hint_y=None)
        scroll_layout.bind(minimum_height=scroll_layout.setter('height'))
        
        # Statistics
        stats_label = Label(text='Statistics', bold=True, font_size='18sp', size_hint_y=None, height=40)
        scroll_layout.add_widget(stats_label)
        
        all_activities = self.db.get_all_activities()
        stats_text = Label(text=f'Total Activities: {len(all_activities)}\nApp Version: 1.0.0', size_hint_y=None, height=60)
        scroll_layout.add_widget(stats_text)
        
        # Notifications
        notif_label = Label(text='Notifications', bold=True, font_size='18sp', size_hint_y=None, height=40)
        scroll_layout.add_widget(notif_label)
        
        test_notif_btn = Button(text='Test Notification', size_hint_y=None, height=50)
        test_notif_btn.bind(on_press=self.send_test_notification)
        scroll_layout.add_widget(test_notif_btn)
        
        # Data Management
        data_label = Label(text='Data Management', bold=True, font_size='18sp', size_hint_y=None, height=40)
        scroll_layout.add_widget(data_label)
        
        export_btn = Button(text='Export Data (JSON)', size_hint_y=None, height=50)
        export_btn.bind(on_press=self.export_data)
        scroll_layout.add_widget(export_btn)
        
        clear_btn = Button(text='Clear All Data', size_hint_y=None, height=50)
        clear_btn.bind(on_press=self.clear_data)
        scroll_layout.add_widget(clear_btn)
        
        scroll.add_widget(scroll_layout)
        layout.add_widget(scroll)
        
        return layout

    def _create_activity_card(self, activity, show_delete=False):
        """Create a card widget for an activity"""
        card = BoxLayout(orientation='vertical', padding=10, spacing=5, size_hint_y=None, height=120)
        
        # Header with hour and category
        header = BoxLayout(size_hint_y=0.3, spacing=10)
        header.add_widget(Label(text=f"{activity['hour']}:00", bold=True, font_size='16sp'))
        category_btn = Button(
            text=activity['category'].capitalize(),
            size_hint_x=0.3,
            background_color=self.categories.get(activity['category'], (0.5, 0.5, 0.5, 1))
        )
        header.add_widget(category_btn)
        card.add_widget(header)
        
        # Description
        card.add_widget(Label(text=activity['description'], size_hint_y=0.3))
        
        # Notes if present
        if activity.get('notes'):
            card.add_widget(Label(text=f"Notes: {activity['notes']}", size_hint_y=0.2))
        
        # Timestamp
        card.add_widget(Label(text=activity['timestamp'][:10], font_size='10sp', size_hint_y=0.1))
        
        # Delete button if requested
        if show_delete:
            delete_btn = Button(text='Delete', size_hint_y=0.2, background_color=(1, 0.42, 0.42, 1))
            delete_btn.bind(on_press=lambda x: self.delete_activity(activity['id']))
            card.add_widget(delete_btn)
        
        return card

    def set_category(self, category):
        """Set the current activity category"""
        self.current_category = category
        print(f"Category set to: {category}")

    def log_activity(self, instance):
        """Log a new activity"""
        description = self.description_input.text.strip()
        notes = self.notes_input.text.strip()

        # (ChatGPT suggestion)
        #def refresh_ui(self):
    #"""Refresh all tab contents"""
    #self.root.tab_list[0].content = self.build_home_screen()
    #self.root.tab_list[1].content = self.build_log_screen()
    #self.root.tab_list[2].content = self.build_history_screen()
    #self.root.tab_list[3].content = self.build_settings_screen()
    # End Chat GPT suggestion
        
        if not description:
            self._show_popup('Error', 'Please describe your activity')
            return
        
        try:
            self.db.add_activity(description, self.current_category, notes)
            self._show_popup('Success', 'Activity logged successfully!')
            #chatGPT suggestion
            #def refresh_ui(self):
    #"""Refresh all tab contents"""
    #self.root.tab_list[0].content = self.build_home_screen()
    #self.root.tab_list[1].content = self.build_log_screen()
    #self.root.tab_list[2].content = self.build_history_screen()
    #self.root.tab_list[3].content = self.build_settings_screen()
    #end chatGPT suggestion
            self.description_input.text = ''
            self.notes_input.text = ''
            self.current_category = 'work'
        except Exception as e:
            self._show_popup('Error', f'Failed to log activity: {str(e)}')

    def delete_activity(self, activity_id):
        """Delete an activity"""
        self.db.delete_activity(activity_id)
        self._show_popup('Success', 'Activity deleted')
        def refresh_ui(self):
            #chat GPT suggestion
    #"""Refresh all tab contents"""
    #self.root.tab_list[0].content = self.build_home_screen()
    #self.root.tab_list[1].content = self.build_log_screen()
    #self.root.tab_list[2].content = self.build_history_screen()
    #self.root.tab_list[3].content = self.build_settings_screen()
    #end chatGPT suggestion
        # Refresh history screen
        self.root.current_tab.content = self.build_history_screen()

    def export_data(self, instance):
        """Export all activities as JSON"""
        try:
            json_data = self.db.export_to_json()
            with open('activities_export.json', 'w') as f:
                f.write(json_data)
            self._show_popup('Success', 'Data exported to activities_export.json')
        except Exception as e:
            self._show_popup('Error', f'Failed to export data: {str(e)}')

    def clear_data(self, instance):
        """Clear all data with confirmation"""
        content = BoxLayout(orientation='vertical', spacing=10, padding=10)
        content.add_widget(Label(text='Are you sure you want to delete all activities?'))
        
        btn_layout = BoxLayout(spacing=10, size_hint_y=0.3)
        
        def confirm_clear(instance):
            self.db.clear_all_activities()
            popup.dismiss()
            self._show_popup('Success', 'All data cleared')
            #chatGPT suggestion
            #def refresh_ui(self):
    #"""Refresh all tab contents"""
    #self.root.tab_list[0].content = self.build_home_screen()
    #self.root.tab_list[1].content = self.build_log_screen()
    #self.root.tab_list[2].content = self.build_history_screen()
    #self.root.tab_list[3].content = self.build_settings_screen()
    #end chatGPT suggestion
        
        def cancel(instance):
            popup.dismiss()
        
        btn_layout.add_widget(Button(text='Cancel', on_press=cancel))
        btn_layout.add_widget(Button(text='Clear', on_press=confirm_clear, background_color=(1, 0.42, 0.42, 1)))
        content.add_widget(btn_layout)
        
        popup = Popup(title='Clear All Data', content=content, size_hint=(0.9, 0.3))
        popup.open()

    def send_test_notification(self, instance):
        """Send a test notification"""
        self.notification_manager.send_test_notification()
        self._show_popup('Info', 'Test notification sent')

    def on_notification(self):
        """Called when a notification is triggered"""
        print("Notification triggered - time to log activity!")

    def _calculate_missing_hours(self, activities):
        """Calculate which hours don't have logged activities"""
        logged_hours = set(activity['hour'] for activity in activities)
        now = datetime.now()
        missing = []
        
        for hour in range(now.hour):
            if hour not in logged_hours:
                missing.append(hour)
        
        return missing

    def _show_popup(self, title, message):
        """Show a simple popup message"""
        content = BoxLayout(orientation='vertical', spacing=10, padding=10)
        content.add_widget(Label(text=message))
        close_btn = Button(text='OK', size_hint_y=0.3)
        content.add_widget(close_btn)
        
        popup = Popup(title=title, content=content, size_hint=(0.9, 0.3))
        close_btn.bind(on_press=popup.dismiss)
        popup.open()

if __name__ == '__main__':
    app = ActivityTrackerApp()
    app.run()
