
import React from 'react';
import { Bot, Users, TrendingUp, Clock } from 'lucide-react';
import Navigation from '../components/Navigation';

const About = () => {
  return (
    <div className="min-h-screen flex flex-col bg-essaypro-blue-50 text-essaypro-blue-900">
      <Navigation />
      
      {/* Hero Section */}
      <section className="py-16 md:py-24 px-4 bg-essaypro-blue-600 text-white">
        <div className="container mx-auto text-center">
          <h1 className="text-4xl md:text-5xl font-bold mb-6">
            About Forex Hunter Bot
          </h1>
          <p className="text-xl max-w-3xl mx-auto">
            Our mission is to democratize access to advanced trading technologies and help traders of all levels achieve their financial goals.
          </p>
        </div>
      </section>
      
      {/* Story Section */}
      <section className="py-16 px-4 bg-white">
        <div className="container mx-auto">
          <div className="flex flex-col md:flex-row items-center">
            <div className="md:w-1/2 mb-8 md:mb-0">
              <img 
                src="https://images.unsplash.com/photo-1581091226825-a6a2a5aee158?ixlib=rb-1.2.1&auto=format&fit=crop&w=600&h=500&q=80" 
                alt="Our Story" 
                className="rounded-lg shadow-xl max-w-full h-auto"
              />
            </div>
            <div className="md:w-1/2 md:pl-12">
              <h2 className="text-3xl font-bold mb-6">Our Story</h2>
              <p className="mb-6">
                Forex Hunter Bot was created by a team of experienced traders and engineers who recognized a gap in the market for accessible, high-quality trading tools. We combined our expertise in finance, machine learning, and software development to build a platform that could level the playing field for independent traders.
              </p>
              <p>
                Since our launch in 2021, we've helped thousands of traders across the globe improve their trading performance and achieve consistent results in the volatile forex markets. Our team continues to innovate and improve our technology to stay ahead of market changes.
              </p>
            </div>
          </div>
        </div>
      </section>
      
      {/* Values Section */}
      <section className="py-16 px-4 bg-essaypro-blue-100">
        <div className="container mx-auto">
          <h2 className="text-3xl font-bold text-center mb-12">Our Core Values</h2>
          <div className="grid grid-cols-1 md:grid-cols-2 gap-8">
            <ValueCard 
              icon={<Users className="w-8 h-8 text-essaypro-accent" />}
              title="Trader First"
              description="We put the needs of our traders at the center of everything we do. Our success is measured by your success."
            />
            <ValueCard 
              icon={<TrendingUp className="w-8 h-8 text-essaypro-accent" />}
              title="Continuous Improvement"
              description="We're constantly refining our algorithms and adding new features to provide the best possible trading experience."
            />
            <ValueCard 
              icon={<Shield className="w-8 h-8 text-essaypro-accent" />}
              title="Risk Management"
              description="We believe in responsible trading and provide tools to help you manage risk effectively."
            />
            <ValueCard 
              icon={<Clock className="w-8 h-8 text-essaypro-accent" />}
              title="Long-term Focus"
              description="We build strategies for sustainable success, not short-term gains that fade quickly."
            />
          </div>
        </div>
      </section>
      
      {/* Team Section */}
      <section className="py-16 px-4 bg-white">
        <div className="container mx-auto">
          <h2 className="text-3xl font-bold text-center mb-12">Meet Our Team</h2>
          <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-8">
            <TeamMember 
              name="Alex Chen"
              role="Founder & CEO"
              bio="Former quantitative analyst with 15 years of trading experience."
            />
            <TeamMember 
              name="Sarah Johnson"
              role="Head of Development"
              bio="Software engineer specializing in AI and machine learning applications."
            />
            <TeamMember 
              name="Marcus Williams"
              role="Lead Trader"
              bio="Professional forex trader with experience in major financial institutions."
            />
            <TeamMember 
              name="Elena Rodriguez"
              role="Customer Success"
              bio="Dedicated to ensuring our users get the most out of our platform."
            />
          </div>
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

const ValueCard = ({ icon, title, description }: { icon: React.ReactNode, title: string, description: string }) => {
  return (
    <div className="bg-white p-6 rounded-lg shadow-md">
      <div className="flex items-center mb-4">
        {icon}
        <h3 className="text-xl font-semibold ml-4">{title}</h3>
      </div>
      <p className="text-essaypro-blue-700">{description}</p>
    </div>
  );
};

const TeamMember = ({ name, role, bio }: { name: string, role: string, bio: string }) => {
  return (
    <div className="bg-essaypro-blue-50 p-6 rounded-lg shadow-md text-center">
      <div className="w-24 h-24 bg-essaypro-blue-200 rounded-full mx-auto mb-4 flex items-center justify-center">
        <Users className="w-12 h-12 text-essaypro-blue-700" />
      </div>
      <h3 className="text-xl font-semibold mb-1">{name}</h3>
      <p className="text-essaypro-accent font-medium mb-2">{role}</p>
      <p className="text-essaypro-blue-700">{bio}</p>
    </div>
  );
};

export default About;
