from datetime import datetime

class YourClass:
    def __init__(self):
        self.month_and_year = datetime.now()

    def set_month_beginning(self, selected_date):
        # Set the day to 1 to get the beginning of the month
        selected_date = selected_date.replace(day=1)

        # Format the selected date
        formatted_date = selected_date.strftime("%d/%m/%Y") + '\n' + selected_date.strftime('%A')
        print("Formatted Date (Beginning of the Month):", formatted_date)

# Example usage
your_instance = YourClass()

# For example, let's say the user selected May 15, 2023
user_selected_date = datetime(2023, 5, 15)

# Call the method to set the beginning of the month for the selected date
your_instance.set_month_beginning(user_selected_date)

        x = 15
        y = 75
        gap = 135
        number_days_in_month = self.count_number_month_days()

        for i in range(0, 7):
            if i == 0:
                if len(self.first_date_check) == 0:
                    selected_date = self.first_month_date.strftime("%d/%m/%Y") + '\n' + self.first_month_date.strftime('%A')
                    self.first_date_check.append(selected_date)
                    #print('Selected date - first day: ' + str(selected_date))
                else:
                    selected_date = self.add_day_date()
                    #print('First day exist')
            else:
                selected_date = self.add_day_date()
                #print('Selected day after adding: ' + str(selected_date))

            if len(self.frame_names) == i:
                frame = self.create_frame(i, x, y)
            else:
                pass
            self.button_names[i].configure(text=selected_date)
            x += gap
        
        x = 15
        y = 200
        for i in range(7, 14):
            selected_date = self.add_day_date()
            #print('Selected day after adding: ' + str(selected_date))

            if len(self.frame_names) == i:
                frame = self.create_frame(i, x, y)
            else:
                pass
            self.button_names[i].configure(text=selected_date)
            x += gap

        x = 15
        y = 325
        for i in range(14, 21):
            selected_date = self.add_day_date()
            #print('Selected day after adding: ' + str(selected_date))

            if len(self.frame_names) == i:
                frame = self.create_frame(i, x, y)
            else:
                pass
            self.button_names[i].configure(text=selected_date)
            x += gap

        x = 15
        y = 450
        for i in range(21, 28):
            selected_date = self.add_day_date()
            #print('Selected day after adding: ' + str(selected_date))

            if len(self.frame_names) == i:
                frame = self.create_frame(i, x, y)
            else:
                pass
            self.button_names[i].configure(text=selected_date)
            x += gap

        x = 15
        y = 575
        if number_days_in_month == 28:
            for i in range(28, 31):
                self.frame_name.place_forget()

        elif number_days_in_month == 29:
            for i in range(28, 29):
                self.frame_name.place_forget()
                selected_date = self.add_day_date()
                if len(self.frame_names) == i:
                    frame = self.create_frame(i, x, y)
                else:
                    self.frame_name.place(x, y)
                self.button_names[i].configure(text=selected_date)
                x += gap
            for i in range(29, 31):
                self.frame_name.place_forget()

        elif number_days_in_month == 30:
            for i in range(28, 30):
                self.frame_name.place_forget()
                selected_date = self.add_day_date()
                if len(self.frame_names) == i:
                    frame = self.create_frame(i, x, y)
                else:
                    self.frame_name.place(x, y)
                self.button_names[i].configure(text=selected_date)
                x += gap
            for i in range(30, 31):
                self.frame_name.place_forget()

        elif number_days_in_month == 31:
            for i in range(28, 31):
                selected_date = self.add_day_date()
                if len(self.frame_names) == i:
                    frame = self.create_frame(i, x, y)
                else:
                    self.frame_name.place(x, y)
                self.button_names[i].configure(text=selected_date)
                x += gap