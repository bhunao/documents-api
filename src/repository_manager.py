import apps


app_list = []
for key, val in apps.__dict__.items():
    if hasattr(val, "__path__"):
        app_list.append(val)
