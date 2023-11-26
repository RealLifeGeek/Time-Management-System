# an object holding data to give them for further processing - DBManager, DayListManager etc.
class DataForm:
    def __init__(self):
        self.element_id = ""
        self.element = ""
        self.date = None            # Date, Start Date, in Personal Card == day and month of birth
        self.deadline = None        # Deadline, End Date; Not used in Remarks; in Personal Cards this is the Year of Birth
        self.field1 = ""            # Not used in Task
        self.field2 = ""            # in task: Expected Result
        self.field3 = ""            # Time, Start Time
        self.project = ""           # Not used in Remarks, Events, Project (For project category is used only element as name)
        self.delegated = ""         # Not used in Remarks, Events
        self.cooperating = ""       # Not used in Remarks, Events
        self.field4 = ""            # End time, for Personal Card == Company
        self.field5 = ""            # Titles
        self.remarks = ""           # in Personal Cards == e-mail
        self.keywords = ""          # in Personal Cards == phone number
        self.category = ""
        self.done = "No"            # Initially 'No' for everything, when done the field is updated to 'DONE'
