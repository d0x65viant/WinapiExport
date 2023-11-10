class Progress:
    def __init__(self, total_iterations):
        self.ti = total_iterations
        self.bar_width = 50
        self.count = 0

    def next(self):
        if self.count < self.ti:
            # Расчет прогресса в псевдографике
            progress = int((self.count + 1) / self.ti * self.bar_width)
            bar = '█' * progress + '-' * (self.bar_width - progress)
            print(f"\r"+f'[{bar}] {self.count+1}/{self.ti}', end="")
            self.count += 1

        if self.count >= self.ti:
            self.count = 0
            print(" ")
            return 0
