from datetime import datetime

class BaseFormatter():
    TELEGRAM_MAX_MESSAGE_LENGTH = 4096
    
    def _timestamp_to_readable_format(self,timestamp:float) -> str:
        """
        Converts a timestamp to a human-readable date and time format.

        Args:
            timestamp (float): The timestamp to convert.

        Returns:
            str: A string representing the formatted date and time.
        """
        return  datetime.fromtimestamp(timestamp).strftime('%A %H:%M:%S %Y-%m-%d')


    