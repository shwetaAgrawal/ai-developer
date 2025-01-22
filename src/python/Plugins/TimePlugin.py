from typing import TypedDict, Annotated, Optional
from datetime import datetime
import logging
from semantic_kernel.functions import kernel_function

class TimePlugin:
    def __init__(self, logger = None):
        if logger is not None:
            self.logger = logger

    @kernel_function(description="Gets the current time")
    async def get_current_time(self):
        self.logger.log(logging.INFO, "get_current_time invoked")
        return  datetime.now().strftime("%d-%m-%Y %H:%M:%S")
    
    @kernel_function(description="Gets the year from a date")
    async def get_year_date(self, date:Annotated[str, "The date in format dd-mm-yyyy"]):
        self.logger.log(logging.INFO, "get_year_date invoked")
        return datetime.strptime(date, "%d-%m-%Y").year
    
    @kernel_function(description="Gets the month from a date")
    async def get_month_date(self, date:Annotated[str, "The date in format dd-mm-yyyy"]):
        self.logger.log(logging.INFO, "get_month_date invoked")
        return datetime.strptime(date, "%d-%m-%Y").month
    
    @kernel_function(description="Gets the day of week from a date")
    async def get_dayofweek_date(self, date:Annotated[str, "The date in format dd-mm-yyyy"]):
        self.logger.log(logging.INFO, "get_dayofweek_date invoked")
        return datetime.strptime(date, "%d-%m-%Y").weekday()
        