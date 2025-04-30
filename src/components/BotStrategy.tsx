
import React, { useState } from 'react';
import { ArrowRight, RefreshCw } from 'lucide-react';
import { TradeInstruction } from './TradeForm';

interface BotStrategyProps {
  onGenerateTrades: (trades: TradeInstruction[]) => void;
}

const BotStrategy = ({ onGenerateTrades }: BotStrategyProps) => {
  const [loading, setLoading] = useState(false);
  const [strategy, setStrategy] = useState('trend');
  
  const strategies = [
    { id: 'trend', name: 'Trend Following', description: 'Enter trades in the direction of the established trend' },
    { id: 'reversal', name: 'Reversal', description: 'Look for potential price reversals at key levels' },
    { id: 'breakout', name: 'Breakout', description: 'Enter when price breaks through significant levels with volume' },
    { id: 'range', name: 'Range Trading', description: 'Trade between established support and resistance levels' }
  ];

  const generateTrades = () => {
    setLoading(true);
    
    // This would normally connect to an API or use algorithmic logic
    // For demo purposes, we'll simulate a delay and generate dummy trades
    setTimeout(() => {
      // Sample generated trades based on selected strategy
      const sampleTrades = [
        {
          id: '1',
          symbol: 'XAUUSD',
          entryPrice: 2345.67,
          exitPrice: 2355.30,
          stopLoss: 2335.80,
          lotSize: 0.05
        },
        {
          id: '2',
          symbol: 'EURUSD',
          entryPrice: 1.0875,
          exitPrice: 1.0925,
          stopLoss: 1.0845,
          lotSize: 0.10
        },
        {
          id: '3',
          symbol: 'GBPJPY',
          entryPrice: 187.450,
          exitPrice: 186.900,
          stopLoss: 187.800,
          lotSize: 0.03
        }
      ];
      
      setLoading(false);
      onGenerateTrades(sampleTrades);
    }, 1500);
  };

  return (
    <div className="hunter-card p-4">
      <h2 className="text-lg font-mono mb-4">BOT STRATEGY</h2>
      
      <div className="mb-6">
        <label className="block text-sm text-hunter-text-muted mb-2">Select Trading Strategy</label>
        <div className="grid grid-cols-2 gap-3">
          {strategies.map((s) => (
            <div
              key={s.id}
              className={`p-3 border rounded-md cursor-pointer transition-all ${
                strategy === s.id
                  ? 'border-hunter-accent2 bg-hunter-accent2/10 hunter-glow-blue'
                  : 'border-hunter-background/50 bg-hunter-background/20 hover:bg-hunter-background/30'
              }`}
              onClick={() => setStrategy(s.id)}
            >
              <h3 className="font-medium mb-1">{s.name}</h3>
              <p className="text-xs text-hunter-text-muted">{s.description}</p>
            </div>
          ))}
        </div>
      </div>

      <div className="mb-6">
        <label className="block text-sm text-hunter-text-muted mb-2">Market Analysis</label>
        <div className="p-3 border border-hunter-background/50 rounded-md bg-hunter-background/20">
          <div className="flex justify-between mb-3">
            <span className="text-xs text-hunter-text-muted">Market Overview</span>
            <span className="text-xs text-hunter-accent2">LIVE</span>
          </div>
          
          <div className="space-y-2 mb-4">
            <div className="flex justify-between">
              <span>XAUUSD</span>
              <span className="font-mono text-hunter-accent">2345.67</span>
            </div>
            <div className="flex justify-between">
              <span>EURUSD</span>
              <span className="font-mono text-hunter-accent">1.0875</span>
            </div>
            <div className="flex justify-between">
              <span>GBPJPY</span>
              <span className="font-mono text-hunter-danger">187.450</span>
            </div>
          </div>
          
          <div className="text-xs text-hunter-text-muted italic">
            Market analysis is performed in real-time using proprietary algorithms.
          </div>
        </div>
      </div>
      
      <button
        className={`hunter-button hunter-button-secondary w-full flex items-center justify-center space-x-2 ${loading ? 'opacity-75' : ''}`}
        onClick={generateTrades}
        disabled={loading}
      >
        {loading ? (
          <>
            <RefreshCw className="w-4 h-4 animate-spin" />
            <span>Analyzing Markets...</span>
          </>
        ) : (
          <>
            <ArrowRight className="w-4 h-4" />
            <span>Generate Trade Signals</span>
          </>
        )}
      </button>
    </div>
  );
};

export default BotStrategy;
