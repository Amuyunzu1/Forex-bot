from django.db import models

class CurrencyPair(models.Model):
    symbol = models.CharField(max_length=10, unique=True)  # e.g. 'EUR/USD'
    description = models.TextField(blank=True)

    def _str_(self):
        return self.symbol


class MarketData(models.Model):
    currency_pair = models.ForeignKey(CurrencyPair, on_delete=models.CASCADE)
    timestamp = models.DateTimeField()
    open_price = models.FloatField()
    high_price = models.FloatField()
    low_price = models.FloatField()
    close_price = models.FloatField()
    volume = models.FloatField()

    class Meta:
        unique_together = ('currency_pair', 'timestamp')


class TradeSignal(models.Model):
    SIGNAL_CHOICES = [
        ('BUY', 'Buy'),
        ('SELL', 'Sell'),
        ('HOLD', 'Hold'),
    ]
    currency_pair = models.ForeignKey(CurrencyPair, on_delete=models.CASCADE)
    timestamp = models.DateTimeField()
    signal = models.CharField(max_length=10, choices=SIGNAL_CHOICES)
    confidence = models.FloatField()  # from model, e.g., 0.87
    model_name = models.CharField(max_length=100)

    class Meta:
        ordering = ['-timestamp']


class ExecutedTrade(models.Model):
    signal = models.ForeignKey(TradeSignal, on_delete=models.SET_NULL, null=True)
    entry_price = models.FloatField()
    exit_price = models.FloatField(blank=True, null=True)
    profit_loss = models.FloatField(blank=True, null=True)
    executed_at = models.DateTimeField(auto_now_add=True)

    def _str_(self):
        return f"{self.signal} | P/L: {self.profit_loss}"


class ModelPerformance(models.Model):
    model_name = models.CharField(max_length=100)
    evaluated_at = models.DateTimeField(auto_now_add=True)
    accuracy = models.FloatField()
    precision = models.FloatField()
    recall = models.FloatField()
    f1_score = models.FloatField()

    def _str_(self):
        return f"{self.model_name} ({self.evaluated_at.date()})"