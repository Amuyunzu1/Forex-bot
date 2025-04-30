
import React from 'react';
import { NavLink } from 'react-router-dom';
import { useIsMobile } from '@/hooks/use-mobile';
import { Menu, X } from 'lucide-react';

const Navigation = () => {
  const isMobile = useIsMobile();
  const [isMenuOpen, setIsMenuOpen] = React.useState(false);

  const toggleMenu = () => {
    setIsMenuOpen(!isMenuOpen);
  };

  return (
    <nav className="bg-hunter-darker border-b border-hunter-accent/20 py-2 px-6">
      <div className="container mx-auto flex justify-between items-center">
        {/* Logo */}
        <NavLink to="/" className="flex items-center space-x-2">
          <span className="text-lg font-semibold text-hunter-accent">FOREX HUNTER</span>
        </NavLink>

        {/* Desktop Navigation */}
        {!isMobile && (
          <div className="flex space-x-8">
            <NavLink 
              to="/" 
              end
              className={({ isActive }) => 
                isActive 
                  ? "text-hunter-accent font-medium" 
                  : "text-hunter-text hover:text-hunter-accent/80 transition-colors"
              }
            >
              Home
            </NavLink>
            <NavLink 
              to="/trade" 
              className={({ isActive }) => 
                isActive 
                  ? "text-hunter-accent font-medium" 
                  : "text-hunter-text hover:text-hunter-accent/80 transition-colors"
              }
            >
              Trade
            </NavLink>
            <NavLink 
              to="/about" 
              className={({ isActive }) => 
                isActive 
                  ? "text-hunter-accent font-medium" 
                  : "text-hunter-text hover:text-hunter-accent/80 transition-colors"
              }
            >
              About
            </NavLink>
          </div>
        )}

        {/* Mobile Menu Button */}
        {isMobile && (
          <button 
            onClick={toggleMenu} 
            className="text-hunter-text p-2"
            aria-label="Toggle menu"
          >
            {isMenuOpen ? (
              <X className="w-6 h-6" />
            ) : (
              <Menu className="w-6 h-6" />
            )}
          </button>
        )}
      </div>

      {/* Mobile Menu */}
      {isMobile && isMenuOpen && (
        <div className="container mx-auto py-4 flex flex-col space-y-4 bg-hunter-darker">
          <NavLink 
            to="/" 
            end
            className={({ isActive }) => 
              isActive 
                ? "text-hunter-accent font-medium px-4 py-2" 
                : "text-hunter-text hover:text-hunter-accent/80 px-4 py-2 transition-colors"
            }
            onClick={() => setIsMenuOpen(false)}
          >
            Home
          </NavLink>
          <NavLink 
            to="/trade" 
            className={({ isActive }) => 
              isActive 
                ? "text-hunter-accent font-medium px-4 py-2" 
                : "text-hunter-text hover:text-hunter-accent/80 px-4 py-2 transition-colors"
            }
            onClick={() => setIsMenuOpen(false)}
          >
            Trade
          </NavLink>
          <NavLink 
            to="/about" 
            className={({ isActive }) => 
              isActive 
                ? "text-hunter-accent font-medium px-4 py-2" 
                : "text-hunter-text hover:text-hunter-accent/80 px-4 py-2 transition-colors"
            }
            onClick={() => setIsMenuOpen(false)}
          >
            About
          </NavLink>
        </div>
      )}
    </nav>
  );
};

export default Navigation;
