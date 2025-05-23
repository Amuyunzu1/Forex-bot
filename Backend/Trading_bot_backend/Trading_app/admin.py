from django.contrib import admin
from .models import (
    CurrencyPair,
    MarketData,
    TradeSignal,
    ExecutedTrade,
    ModelPerformance
)

@admin.register(CurrencyPair)
class CurrencyPairAdmin(admin.ModelAdmin):
    list_display = ('symbol', 'description')
    search_fields = ('symbol',)


@admin.register(MarketData)
class MarketDataAdmin(admin.ModelAdmin):
    list_display = ('currency_pair', 'timestamp', 'open_price', 'close_price', 'volume')
    list_filter = ('currency_pair', 'timestamp')
    search_fields = ('currency_pair__symbol',)


@admin.register(TradeSignal)
class TradeSignalAdmin(admin.ModelAdmin):
    list_display = ('currency_pair', 'timestamp', 'signal', 'confidence', 'model_name')
    list_filter = ('signal', 'model_name')
    search_fields = ('currency_pair__symbol', 'model_name')


@admin.register(ExecutedTrade)
class ExecutedTradeAdmin(admin.ModelAdmin):
    list_display = ('signal', 'entry_price', 'exit_price', 'profit_loss', 'executed_at')
    list_filter = ('executed_at',)
    search_fields = ('signal_currency_pair_symbol',)


@admin.register(ModelPerformance)
class ModelPerformanceAdmin(admin.ModelAdmin):
    list_display = ('model_name', 'evaluated_at', 'accuracy', 'precision', 'recall', 'f1_score')
    list_filter = ('model_name', 'evaluated_at')
    search_fields = ('model_name',)
