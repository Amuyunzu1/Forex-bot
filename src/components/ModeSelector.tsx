
import React from 'react';
import { Bot, User } from 'lucide-react';

interface ModeSelectorProps {
  mode: 'manual' | 'bot';
  setMode: (mode: 'manual' | 'bot') => void;
}

const ModeSelector = ({ mode, setMode }: ModeSelectorProps) => {
  return (
    <div className="hunter-card p-4 mb-6">
      <h2 className="text-lg font-mono mb-4">OPERATION MODE</h2>
      <div className="flex rounded-md overflow-hidden">
        <button
          className={`flex-1 py-3 px-4 flex items-center justify-center space-x-2 transition-all ${
            mode === 'manual'
              ? 'bg-hunter-accent text-black font-semibold'
              : 'bg-hunter-background text-hunter-text-muted hover:bg-hunter-background/80'
          }`}
          onClick={() => setMode('manual')}
        >
          <User className="w-4 h-4" />
          <span>MANUAL INPUT</span>
        </button>
        <button
          className={`flex-1 py-3 px-4 flex items-center justify-center space-x-2 transition-all ${
            mode === 'bot'
              ? 'bg-hunter-accent2 text-black font-semibold'
              : 'bg-hunter-background text-hunter-text-muted hover:bg-hunter-background/80'
          }`}
          onClick={() => setMode('bot')}
        >
          <Bot className="w-4 h-4" />
          <span>BOT STRATEGY</span>
        </button>
      </div>
    </div>
  );
};

export default ModeSelector;
