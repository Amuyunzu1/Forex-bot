
import React from 'react';
import { CheckCircle, Server, Activity } from 'lucide-react';

interface StatusBarProps {
  connected: boolean;
  broker: string;
}

const StatusBar = ({ connected, broker }: StatusBarProps) => {
  return (
    <div className="bg-hunter-darker border-t border-hunter-background py-2 px-6 mt-auto">
      <div className="flex items-center justify-between">
        <div className="flex items-center space-x-6">
          <div className="flex items-center space-x-2">
            <Server className="w-4 h-4 text-hunter-accent" />
            <span className="text-sm">{broker}</span>
          </div>
          
          <div className="flex items-center space-x-2">
            {connected ? (
              <>
                <div className="w-2 h-2 rounded-full bg-hunter-accent animate-pulse-slow" />
                <span className="text-sm text-hunter-accent">Connected</span>
              </>
            ) : (
              <>
                <div className="w-2 h-2 rounded-full bg-hunter-danger" />
                <span className="text-sm text-hunter-danger">Disconnected</span>
              </>
            )}
          </div>
        </div>
        
        <div className="flex items-center space-x-2">
          <Activity className="w-4 h-4 text-hunter-text-muted" />
          <span className="text-sm text-hunter-text-muted">Latency: 24ms</span>
        </div>
      </div>
    </div>
  );
};

export default StatusBar;
