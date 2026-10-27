class IBalanceObserver:
    def update(self, balance, transaction):
        """Handle balance updates."""
        raise NotImplementedError("Subclasses must implement update method.")


class PrintObserver(IBalanceObserver):
    def update(self, balance, transaction):
        """Print balance update message."""
        print(f"{transaction} -> Balance: ${balance:.2f}")


class LowBalanceAlertObserver(IBalanceObserver):
    def __init__(self, threshold):
        self.threshold = threshold
        self.alert_triggered = False

    def update(self, balance, transaction):
        """Alert if balance drops below threshold."""
        below_threshold = balance < self.threshold
        if below_threshold and not self.alert_triggered:
            print(f"Low balance alert: ${balance:.2f}")
        self.alert_triggered = below_threshold
