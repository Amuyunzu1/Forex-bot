
import React from 'react';
import { Link } from 'react-router-dom';
import { Bot, BarChart2, Cpu, Shield } from 'lucide-react';
import Navigation from '../components/Navigation';

const Landing = () => {
  return (
    <div className="min-h-screen flex flex-col bg-essaypro-blue-50 text-essaypro-blue-900">
      <Navigation />
      
      {/* Hero Section */}
      <section className="py-16 md:py-24 px-4 bg-essaypro-blue-600 text-white">
        <div className="container mx-auto">
          <div className="flex flex-col md:flex-row items-center justify-between">
            <div className="md:w-1/2 mb-8 md:mb-0">
              <h1 className="text-4xl md:text-5xl font-bold mb-6">
                Automated Forex Trading with <span className="text-essaypro-accent">Smart Technology</span>
              </h1>
              <p className="text-xl mb-8">
                Stealth execution system designed for optimal performance in the global forex market.
              </p>
              <div className="flex flex-col sm:flex-row gap-4">
                <Link to="/trade" className="bg-essaypro-accent hover:bg-essaypro-accent/90 text-white py-3 px-8 rounded-md font-semibold transition-all duration-200">
                  Start Trading
                </Link>
                <Link to="/about" className="bg-essaypro-blue-700 hover:bg-essaypro-blue-800 text-white py-3 px-8 rounded-md font-semibold transition-all duration-200">
                  Learn More
                </Link>
              </div>
            </div>
            <div className="md:w-1/2 flex justify-center">
              <img 
                src="https://images.unsplash.com/photo-1488590528505-98d2b5aba04b?ixlib=rb-1.2.1&auto=format&fit=crop&w=600&h=500&q=80" 
                alt="Trading Platform" 
                className="rounded-lg shadow-xl max-w-full h-auto"
              />
            </div>
          </div>
        </div>
      </section>
      
      {/* Features Section */}
      <section className="py-16 px-4 bg-white">
        <div className="container mx-auto">
          <h2 className="text-3xl font-bold text-center mb-12">Key Features</h2>
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-8">
            <FeatureCard 
              icon={<Bot className="w-10 h-10 text-essaypro-accent" />}
              title="AI-Powered Trading"
              description="Advanced algorithms that analyze market conditions in real-time."
            />
            <FeatureCard 
              icon={<BarChart2 className="w-10 h-10 text-essaypro-accent" />}
              title="Market Analysis"
              description="Comprehensive technical and fundamental analysis tools."
            />
            <FeatureCard 
              icon={<Cpu className="w-10 h-10 text-essaypro-accent" />}
              title="Automated Execution"
              description="Execute trades with precision at optimal market conditions."
            />
            <FeatureCard 
              icon={<Shield className="w-10 h-10 text-essaypro-accent" />}
              title="Risk Management"
              description="Advanced protection systems to minimize trading risks."
            />
          </div>
        </div>
      </section>
      
      {/* CTA Section */}
      <section className="py-16 px-4 bg-essaypro-blue-100">
        <div className="container mx-auto text-center">
          <h2 className="text-3xl font-bold mb-6">Ready to Start Trading?</h2>
          <p className="text-xl mb-8 max-w-2xl mx-auto">
            Join thousands of traders who are already using our platform to achieve their financial goals.
          </p>
          <Link to="/trade" className="bg-essaypro-accent hover:bg-essaypro-accent/90 text-white py-3 px-8 rounded-md font-semibold transition-all duration-200">
            Go to Trading Platform
          </Link>
        </div>
      </section>
      
      {/* Footer */}
      <footer className="bg-essaypro-blue-800 text-white py-8">
        <div className="container mx-auto px-4">
          <div className="flex flex-col md:flex-row justify-between items-center">
            <div className="mb-4 md:mb-0">
              <div className="flex items-center">
                <Bot className="w-6 h-6 text-essaypro-accent mr-2" />
                <span className="font-bold text-lg">FOREX HUNTER BOT</span>
              </div>
            </div>
            <div className="text-sm">
              &copy; {new Date().getFullYear()} Forex Hunter. All rights reserved.
            </div>
          </div>
        </div>
      </footer>
    </div>
  );
};

const FeatureCard = ({ icon, title, description }: { icon: React.ReactNode, title: string, description: string }) => {
  return (
    <div className="bg-essaypro-blue-50 p-6 rounded-lg shadow-md hover:shadow-lg transition-shadow duration-200">
      <div className="mb-4">
        {icon}
      </div>
      <h3 className="text-xl font-semibold mb-2">{title}</h3>
      <p className="text-essaypro-blue-700">{description}</p>
    </div>
  );
};

export default Landing;
