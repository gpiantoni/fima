from bidso import file_Core


def make_name(filename, event_type):
    f = file_Core(filename)
    return f'{f.subject}_run-{f.run}_{f.acquisition}_{event_type}.html'
