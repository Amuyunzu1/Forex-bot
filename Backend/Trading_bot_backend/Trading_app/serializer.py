from rest_framework import serializers
from .models import CurrencyPair, MarketData, TradeSignal, ExecutedTrade, ModelPerformance

class CurrencyPairSerializer(serializers.ModelSerializer):
    class Meta:
        model = CurrencyPair
        fields = ['id', 'symbol', 'description']

class MarketDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = MarketData
        fields = [
            'id', 'currency_pair', 'timestamp',
            'open_price', 'high_price', 'low_price',
            'close_price', 'volume'
        ]

class TradeSignalSerializer(serializers.ModelSerializer):
    class Meta:
        model = TradeSignal
        fields = [
            'id', 'currency_pair', 'timestamp',
            'signal', 'confidence', 'model_name'
        ]

class ExecutedTradeSerializer(serializers.ModelSerializer):
    class Meta:
        model = ExecutedTrade
        fields = [
            'id', 'signal', 'entry_price',
            'exit_price', 'profit_loss', 'executed_at'
        ]

class ModelPerformanceSerializer(serializers.ModelSerializer):
    class Meta:
        model = ModelPerformance
        fields = [
            'id', 'model_name', 'evaluated_at',
            'accuracy', 'precision', 'recall', 'f1_score'
        ]