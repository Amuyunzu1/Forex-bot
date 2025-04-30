
import React from 'react';
import { CheckCircle, AlertCircle } from 'lucide-react';
import { TradeInstruction } from './TradeForm';

interface ActiveTradesProps {
  trades: TradeInstruction[];
}

const ActiveTrades = ({ trades }: ActiveTradesProps) => {
  if (trades.length === 0) {
    return (
      <div className="hunter-card p-4">
        <h2 className="text-lg font-mono mb-4">ACTIVE HUNTS</h2>
        <div className="text-center text-hunter-text-muted py-8">
          <p>No active trades</p>
          <p className="text-sm mt-2">Submit trades to begin hunting</p>
        </div>
      </div>
    );
  }

  return (
    <div className="hunter-card p-4">
      <h2 className="text-lg font-mono mb-4">ACTIVE HUNTS</h2>
      <div className="space-y-4">
        {trades.map((trade) => {
          const isLong = trade.exitPrice > trade.entryPrice;
          const direction = isLong ? 'LONG' : 'SHORT';
          const directionColor = isLong ? 'text-hunter-accent' : 'text-hunter-danger';
          const isBuyReady = Math.random() > 0.5; // Simulate some trades being ready for execution
          
          return (
            <div key={trade.id} className="border border-hunter-background/70 rounded-md overflow-hidden">
              <div className="bg-hunter-background/30 py-2 px-3 flex justify-between items-center">
                <div className="flex items-center space-x-2">
                  <span className="font-mono text-hunter-text">{trade.symbol}</span>
                  <span className={`text-xs font-semibold ${directionColor}`}>{direction}</span>
                </div>
                <div className="flex items-center space-x-2">
                  <span className="text-xs text-hunter-text-muted">Lot: {trade.lotSize}</span>
                  {isBuyReady ? (
                    <div className="hunter-badge hunter-badge-success flex items-center space-x-1">
                      <CheckCircle className="w-3 h-3" />
                      <span>READY</span>
                    </div>
                  ) : (
                    <div className="hunter-badge hunter-badge-warning flex items-center space-x-1">
                      <AlertCircle className="w-3 h-3" />
                      <span>HUNTING</span>
                    </div>
                  )}
                </div>
              </div>
              
              <div className="p-3">
                <div className="grid grid-cols-3 gap-2 text-xs">
                  <div>
                    <div className="text-hunter-text-muted mb-1">Entry</div>
                    <div className="font-mono">{trade.entryPrice}</div>
                  </div>
                  <div>
                    <div className="text-hunter-text-muted mb-1">Take Profit</div>
                    <div className="font-mono text-hunter-accent">{trade.exitPrice}</div>
                  </div>
                  <div>
                    <div className="text-hunter-text-muted mb-1">Stop Loss</div>
                    <div className="font-mono text-hunter-danger">{trade.stopLoss}</div>
                  </div>
                </div>
                
                {isBuyReady && (
                  <div className="mt-3">
                    <button className="w-full py-1 bg-hunter-accent hover:bg-hunter-accent/90 text-black text-sm font-medium rounded transition-colors">
                      EXECUTE NOW
                    </button>
                  </div>
                )}
              </div>
            </div>
          );
        })}
      </div>
    </div>
  );
};

export default ActiveTrades;
