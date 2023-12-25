import datetime

def epoch_to_human_readable(epoch_timestamp, timezone='GMT'):
    # Convert the epoch timestamp to a datetime object
    dt_object = datetime.datetime.utcfromtimestamp(epoch_timestamp)
    
    # Format the datetime object to a human-readable string
    if timezone == 'GMT':
        date_str = dt_object.strftime("GMT: %A, %B %d, %Y %I:%M:%S %p")
    elif timezone == 'EST':
        dt_object -= datetime.timedelta(hours=4)  # Subtract 5 hours from GMT to get EST
        date_str = dt_object.strftime("EST: %A, %B %d, %Y %I:%M:%S %p")
    else:
        raise ValueError("Unsupported timezone!")
    
    return date_str

epoch_timestamp = 1697528478724
print(epoch_to_human_readable(epoch_timestamp))
print(epoch_to_human_readable(epoch_timestamp, 'EST'))