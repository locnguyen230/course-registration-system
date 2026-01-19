class ExportRosterView:
    def __init__(self, controller):
        self.controller = controller

    def show_export_option(self, section_id):
        # UC-I2: Export Roster
        choice = input("\nDo you want to export this roster? (y/n): ")
        if choice.lower() == 'y':
            filename = input("Enter filename (default: roster.csv): ") or f"roster_{section_id}.csv"
            if not filename.endswith('.csv'):
                filename += '.csv'
                
            success, message = self.controller.export_roster_to_csv(section_id, filename)
            print(f"System: {message}")