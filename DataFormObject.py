# an object holding data to give them for further processing - DBManager, DayListManager etc.
class DataForm:
    def __init__(self):
        self.element_id = ""
        self.element = ""
        self.date = None              # Date, Start Date
        self.deadline = None          # Deadline, End Date; Not used in Remarks
        self.field1 = ""            # Not used in Task
        self.field2 = ""            # in task: Expected Result
        self.field3 = ""            # Time, Start Time
        self.project = ""           # Not used in Remarks, Events, Project (For project category is used only element as name)
        self.delegated = ""         # Not used in Remarks, Events
        self.cooperating = ""       # Not used in Remarks, Events
        self.field4 = ""            # End time
        self.field5 = ""            # Empty field - not used so far
        self.remarks = ""
        self.keywords = ""
        self.category = ""
        self.done = "No"            # Initially 'No' for everything, when done the field is updated to 'DONE'
