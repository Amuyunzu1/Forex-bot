
import React from 'react';
import { Bot, Settings } from 'lucide-react';
import { Link } from 'react-router-dom';

const Header = () => {
  return (
    <header className="bg-hunter-darker border-b border-hunter-accent/20 py-4 px-6">
      <div className="container mx-auto flex items-center justify-between">
        <Link to="/trade" className="flex items-center space-x-3">
          <Bot className="w-7 h-7 text-hunter-accent" />
          <div className="flex flex-col">
            <h1 className="text-xl font-semibold font-mono text-hunter-accent">
              FOREX HUNTER BOT
            </h1>
            <p className="text-xs text-hunter-text-muted">Stealth Execution System v1.0</p>
          </div>
        </Link>
        <button className="hunter-button p-2 rounded-full">
          <Settings className="w-5 h-5" />
        </button>
      </div>
    </header>
  );
};

export default Header;
