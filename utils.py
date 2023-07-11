

def progress_bar(current, total, bar_length=40):
    progress = current / total
    filled_length = int(bar_length * progress)
    bar = '=' * (filled_length - 1) + '>' + '-' * (bar_length - filled_length)
    percentage = round(progress * 100, 2)
    print(f'[{bar}] {percentage}% complete', end='\r')