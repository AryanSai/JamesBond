from datetime import datetime
import pytz

current_date = datetime.now(pytz.timezone('GMT'))
print(int(current_date.timestamp()))