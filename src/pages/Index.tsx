
import React, { useState } from 'react';
import Header from '../components/Header';
import ModeSelector from '../components/ModeSelector';
import TradeForm, { TradeInstruction } from '../components/TradeForm';
import BotStrategy from '../components/BotStrategy';
import ActiveTrades from '../components/ActiveTrades';
import StatusBar from '../components/StatusBar';
import { useToast } from '@/hooks/use-toast';

const Index = () => {
  const [mode, setMode] = useState<'manual' | 'bot'>('manual');
  const [activeTrades, setActiveTrades] = useState<TradeInstruction[]>([]);
  const { toast } = useToast();

  const handleTradeSubmit = (trades: TradeInstruction[]) => {
    setActiveTrades(trades);
    
    toast({
      title: "Trades Submitted",
      description: `${trades.length} trade(s) are now being hunted`,
      variant: "default",
    });
  };

  return (
    <div className="flex flex-col min-h-screen">
      <Header />
      
      <div className="flex-1 container py-6">
        <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
          <div className="lg:col-span-2 space-y-6">
            <ModeSelector mode={mode} setMode={setMode} />
            
            {mode === 'manual' ? (
              <TradeForm onTradeSubmit={handleTradeSubmit} />
            ) : (
              <BotStrategy onGenerateTrades={handleTradeSubmit} />
            )}
          </div>
          
          <div>
            <ActiveTrades trades={activeTrades} />
          </div>
        </div>
      </div>
      
      <StatusBar connected={true} broker="MetaTrader 5" />
    </div>
  );
};

export default Index;
