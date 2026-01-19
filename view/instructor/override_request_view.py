class OverrideRequestView:
    def __init__(self, controller):
        self.controller = controller

    def show(self):
        # UC-I3: Review Override Requests
        requests = self.controller.get_override_requests()
        
        if not requests:
            print("\nNo pending override requests.")
            return

        print("\n--- PENDING REQUESTS ---")
        for idx, req in enumerate(requests):
            print(f"{idx + 1}. Student: {req['fullName']} ({req['studentID']}) - Class: {req['sectionCode']} - Date: {req['requestDate']}")

        try:
            choice = int(input("Select request to process (0 to cancel): "))
            if choice <= 0 or choice > len(requests):
                return
            
            selected_req = requests[choice - 1]
            self.process_decision(selected_req)
        except ValueError:
            print("Invalid input.")

    def process_decision(self, request):
        print(f"\nProcessing request for {request['fullName']}...")
        print("1. Approve")
        print("2. Reject")
        action = input("Choose action: ")

        if action == '1':
            if self.controller.process_request(request['waitlistID'], 'approve'):
                print("Request APPROVED.")
            else:
                print("Error processing request.")
        elif action == '2':
            if self.controller.process_request(request['waitlistID'], 'reject'):
                print("Request REJECTED.")
            else:
                print("Error processing request.")
        else:
            print("Cancelled.")