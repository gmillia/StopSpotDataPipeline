import sys
from datetime import datetime
from datetime import date

class Checkpoint:
    def __init__(self):
        self._file = "./assets/checkpoint.txt"

    # This function will write to the checkpoint file
    # if there is an existing checkpoint it will overwrite that checkpoint
    # date_to_checkpoint : Will be the date of the last row processed, this should be a string from a row entry
    # end_date: Will be the ending date for the range of entries being queried, this should be a string from a row entry
    def write_to_file(self, date_to_checkpoint, end_date):
        with open(self._file, "w") as fstream:
            fstream.write(date_to_checkpoint + "," + end_date)

    # This function will read from the checkpoint file, it will get the last date that was checkpointed
    def read_from_file(self):
        dates = None
        try:
            with open(self._file, "r") as fstream:
                for line in fstream:
                    dates = line.split(",")

            # date_tuple is a tuple of datetime objects, this is to match the implementation within process_data() in main.py
            date_tuple = (datetime.strptime(dates[0], '%Y-%m-%d').date(), datetime.strptime(dates[1], '%Y-%m-%d').date())
            return date_tuple
        except EnvironmentError:  # found on stack overflow that EnvironmentError is the parent of IOError, OSError, and WindowsError
            print("checkpoint.txt not found. Creating checkpoint.txt with today's date as a range")
            today = date.today()
            self.write_to_file(today.strftime("%Y-%m-%d"), today.strftime("%Y-%m-%d"))
            return self.read_from_file()

    # This function will rerun to enter all the data from the checkpoint date to the current date
    def rerun_from_checkpoint(self):
        checkpoint_date = self.read_from_file()  # Date to run from
        # Need to figure out what function we need to call to rerun the stuffz