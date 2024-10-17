



class ProgressBar():
    def __init__(self, total_items, bar_width=30):
        self.bar_width = bar_width
        self.total_items = []
        self.completed_items = []
        
        # used to avoid spamming the stdout with updates if the percent hasn't changed
        self.last_percent = 0
        self.last_bar_width = 0
        
        self.push_subproblem(total_items)
        
        self.update(items_completed=0)


    def _calculate_completed_fraction(self, subprob_idx=0):
        if subprob_idx >= len(self.completed_items):
            return 0
        
        problem_total_items = self.total_items[subprob_idx]
        problem_completed_items = self.completed_items[subprob_idx]

        return ((problem_completed_items + self._calculate_completed_fraction(subprob_idx=subprob_idx+1)) / problem_total_items)


    def update(self, items_completed=1):
        
        if len(self.total_items) != len(self.completed_items):
            raise Exception("Progress bar in bad state")
        
        if len(self.total_items) == 0:
            return
        
        self.completed_items[-1] += items_completed
        
        fraction_complete = self._calculate_completed_fraction()
        percent = int(fraction_complete * 100)
        show_bar_width = int(fraction_complete * self.bar_width)
        
        percent = min(percent, 99)
        show_bar_width = min(show_bar_width, (self.bar_width-1))
        
        if percent == self.last_percent and show_bar_width == self.last_bar_width:
            return
        
        print("[{}] {:3}%".format(
            "#" * show_bar_width + " " * (self.bar_width - show_bar_width),
            percent
        ), end='\r')
        
        self.last_percent = percent
        self.last_bar_width = show_bar_width
    
    def push_subproblem(self, num_items):
        self.total_items.append(num_items)
        self.completed_items.append(0)
        
    def complete_subproblem(self):
        self.completed_items.pop()
        self.total_items.pop()
        if len(self.total_items) == 0:
            self.complete()
    
    def complete(self):
        self.completed_items = []
        self.total_items = []
        print("[{}] {:3}%".format(
            "#" * self.bar_width ,
            100
        ))
        
        
        