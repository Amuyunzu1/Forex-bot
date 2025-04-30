
import React, { useState } from 'react';
import { Plus, X } from 'lucide-react';

export interface TradeInstruction {
  id: string;
  symbol: string;
  entryPrice: number;
  exitPrice: number;
  stopLoss: number;
  lotSize: number;
}

interface TradeFormProps {
  onTradeSubmit: (trades: TradeInstruction[]) => void;
}

const TradeForm = ({ onTradeSubmit }: TradeFormProps) => {
  const [trades, setTrades] = useState<TradeInstruction[]>([
    { id: '1', symbol: '', entryPrice: 0, exitPrice: 0, stopLoss: 0, lotSize: 0.01 }
  ]);

  const addTrade = () => {
    const newId = String(trades.length + 1);
    setTrades([
      ...trades,
      { id: newId, symbol: '', entryPrice: 0, exitPrice: 0, stopLoss: 0, lotSize: 0.01 }
    ]);
  };

  const removeTrade = (id: string) => {
    if (trades.length <= 1) return;
    setTrades(trades.filter((trade) => trade.id !== id));
  };

  const updateTrade = (id: string, field: keyof TradeInstruction, value: string | number) => {
    setTrades(
      trades.map((trade) => {
        if (trade.id === id) {
          return { ...trade, [field]: value };
        }
        return trade;
      })
    );
  };

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    onTradeSubmit(trades);
  };

  return (
    <div className="hunter-card p-4">
      <h2 className="text-lg font-mono mb-4">TRADE INSTRUCTIONS</h2>
      
      <form onSubmit={handleSubmit}>
        {trades.map((trade, index) => (
          <div 
            key={trade.id} 
            className={`mb-4 p-4 border border-hunter-background/70 rounded-md ${
              index % 2 === 0 ? 'bg-hunter-background/10' : 'bg-hunter-background/20'
            }`}
          >
            <div className="flex justify-between items-center mb-4">
              <h3 className="font-mono text-hunter-accent">TRADE #{trade.id}</h3>
              {trades.length > 1 && (
                <button 
                  type="button" 
                  onClick={() => removeTrade(trade.id)}
                  className="text-hunter-text-muted hover:text-hunter-danger transition-colors"
                >
                  <X className="w-4 h-4" />
                </button>
              )}
            </div>
            
            <div className="grid grid-cols-2 gap-4">
              <div>
                <label className="block text-sm text-hunter-text-muted mb-1">Symbol</label>
                <input
                  type="text"
                  className="hunter-input w-full"
                  placeholder="e.g. XAUUSD"
                  value={trade.symbol}
                  onChange={(e) => updateTrade(trade.id, 'symbol', e.target.value)}
                  required
                />
              </div>
              <div>
                <label className="block text-sm text-hunter-text-muted mb-1">Lot Size</label>
                <input
                  type="number"
                  step="0.01"
                  min="0.01"
                  className="hunter-input w-full"
                  value={trade.lotSize}
                  onChange={(e) => updateTrade(trade.id, 'lotSize', parseFloat(e.target.value))}
                  required
                />
              </div>
              <div>
                <label className="block text-sm text-hunter-text-muted mb-1">Entry Price</label>
                <input
                  type="number"
                  step="0.00001"
                  className="hunter-input w-full"
                  value={trade.entryPrice || ''}
                  onChange={(e) => updateTrade(trade.id, 'entryPrice', parseFloat(e.target.value))}
                  required
                />
              </div>
              <div>
                <label className="block text-sm text-hunter-text-muted mb-1">Exit Price (TP)</label>
                <input
                  type="number"
                  step="0.00001"
                  className="hunter-input w-full"
                  value={trade.exitPrice || ''}
                  onChange={(e) => updateTrade(trade.id, 'exitPrice', parseFloat(e.target.value))}
                  required
                />
              </div>
              <div>
                <label className="block text-sm text-hunter-text-muted mb-1">Stop Loss</label>
                <input
                  type="number"
                  step="0.00001"
                  className="hunter-input w-full"
                  value={trade.stopLoss || ''}
                  onChange={(e) => updateTrade(trade.id, 'stopLoss', parseFloat(e.target.value))}
                  required
                />
              </div>
              <div className="flex items-end">
                <div className={`py-1 px-2 rounded text-xs ${
                  trade.exitPrice > trade.entryPrice 
                    ? 'bg-hunter-accent/20 text-hunter-accent' 
                    : trade.exitPrice < trade.entryPrice 
                      ? 'bg-hunter-danger/20 text-hunter-danger'
                      : 'bg-hunter-text-muted/20 text-hunter-text-muted'
                }`}>
                  {trade.exitPrice > trade.entryPrice 
                    ? 'BUY (LONG)' 
                    : trade.exitPrice < trade.entryPrice 
                      ? 'SELL (SHORT)' 
                      : 'UNDEFINED'}
                </div>
              </div>
            </div>
          </div>
        ))}
        
        <div className="flex justify-between mt-6">
          <button
            type="button"
            className="hunter-button flex items-center space-x-2"
            onClick={addTrade}
          >
            <Plus className="w-4 h-4" />
            <span>Add Trade</span>
          </button>
          
          <button
            type="submit"
            className="hunter-button hunter-button-primary"
          >
            Submit Trades
          </button>
        </div>
      </form>
    </div>
  );
};

export default TradeForm;
