



class ProgressBar():
    def __init__(self, total_items, bar_width=30):
        self.bar_width = bar_width
        self.total_items = total_items
        self.completed_items = 0
        self.last_percent = 0 # used to avoid spamming the stdout with updates if the percent hasn't changed
        
        self.update(items_completed=0)
    
    def update(self, items_completed=1):
        self.completed_items += items_completed
        
        percent = int((self.completed_items / self.total_items) * 100)
        show_bar_width = int((self.completed_items / self.total_items) * self.bar_width)
        
        if self.completed_items < self.total_items:
            percent = min(percent, 99)
            show_bar_width = min(show_bar_width, (self.bar_width-1))
        
        if percent == self.last_percent:
            return
        
        print("[{}] {:3}%".format(
            "#" * show_bar_width + " " * (self.bar_width - show_bar_width),
            percent
        ), end='\r')
        
        self.last_percent = percent
        
    def complete(self):
        print("[{}] {:3}%".format(
            "#" * self.bar_width ,
            100
        ))
        
        
        