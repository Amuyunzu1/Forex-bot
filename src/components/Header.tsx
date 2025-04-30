
import React from 'react';
import { Bot, Settings } from 'lucide-react';

const Header = () => {
  return (
    <header className="bg-hunter-darker border-b border-hunter-accent/20 py-4 px-6">
      <div className="flex items-center justify-between">
        <div className="flex items-center space-x-3">
          <Bot className="w-7 h-7 text-hunter-accent" />
          <div className="flex flex-col">
            <h1 className="text-xl font-semibold font-mono text-hunter-accent">
              FOREX HUNTER BOT
            </h1>
            <p className="text-xs text-hunter-text-muted">Stealth Execution System v1.0</p>
          </div>
        </div>
        <button className="hunter-button p-2 rounded-full">
          <Settings className="w-5 h-5" />
        </button>
      </div>
    </header>
  );
};

export default Header;
