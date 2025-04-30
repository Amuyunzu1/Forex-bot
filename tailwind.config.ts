
import type { Config } from "tailwindcss";

export default {
	darkMode: ["class"],
	content: [
		"./pages/**/*.{ts,tsx}",
		"./components/**/*.{ts,tsx}",
		"./app/**/*.{ts,tsx}",
		"./src/**/*.{ts,tsx}",
	],
	prefix: "",
	theme: {
		container: {
			center: true,
			padding: '2rem',
			screens: {
				'2xl': '1400px'
			}
		},
		extend: {
			colors: {
				border: 'hsl(var(--border))',
				input: 'hsl(var(--input))',
				ring: 'hsl(var(--ring))',
				background: 'hsl(var(--background))',
				foreground: 'hsl(var(--foreground))',
				primary: {
					DEFAULT: 'hsl(var(--primary))',
					foreground: 'hsl(var(--primary-foreground))'
				},
				secondary: {
					DEFAULT: 'hsl(var(--secondary))',
					foreground: 'hsl(var(--secondary-foreground))'
				},
				destructive: {
					DEFAULT: 'hsl(var(--destructive))',
					foreground: 'hsl(var(--destructive-foreground))'
				},
				muted: {
					DEFAULT: 'hsl(var(--muted))',
					foreground: 'hsl(var(--muted-foreground))'
				},
				accent: {
					DEFAULT: 'hsl(var(--accent))',
					foreground: 'hsl(var(--accent-foreground))'
				},
				popover: {
					DEFAULT: 'hsl(var(--popover))',
					foreground: 'hsl(var(--popover-foreground))'
				},
				card: {
					DEFAULT: 'hsl(var(--card))',
					foreground: 'hsl(var(--card-foreground))'
				},
				sidebar: {
					DEFAULT: 'hsl(var(--sidebar-background))',
					foreground: 'hsl(var(--sidebar-foreground))',
					primary: 'hsl(var(--sidebar-primary))',
					'primary-foreground': 'hsl(var(--sidebar-primary-foreground))',
					accent: 'hsl(var(--sidebar-accent))',
					'accent-foreground': 'hsl(var(--sidebar-accent-foreground))',
					border: 'hsl(var(--sidebar-border))',
					ring: 'hsl(var(--sidebar-ring))'
				},
				hunter: {
					dark: '#2A3E52', // EssayPro dark blue
					darker: '#1A2A3A', // EssayPro darker blue
					background: '#203044', // Medium blue
					card: '#304B6A', // Lighter blue
					accent: '#00C9B9', // Teal accent
					accent2: '#7382A5', // Secondary accent
					warning: '#FF9C45',
					danger: '#FF5050',
					text: '#FFFFFF', // White text
					'text-muted': '#D1D7E0'
				},
				essaypro: {
					'blue': {
						50: '#F0F4F9',
						100: '#E1E9F3',
						200: '#C3D4E7',
						300: '#A5BEDB',
						400: '#87A9CF',
						500: '#6993C3',
						600: '#4B7DB7',
						700: '#2D68AB',
						800: '#245394',
						900: '#1B407E',
					},
					'accent': '#FF6B35',
					'accent-dark': '#E84F18',
					'gray': {
						100: '#F5F7FA',
						200: '#E9ECF2',
						300: '#D2D7E2',
						400: '#BCC2D1',
						500: '#A5AEC1',
						600: '#8F99B0',
					}
				}
			},
			borderRadius: {
				lg: 'var(--radius)',
				md: 'calc(var(--radius) - 2px)',
				sm: 'calc(var(--radius) - 4px)'
			},
			keyframes: {
				'accordion-down': {
					from: {
						height: '0'
					},
					to: {
						height: 'var(--radix-accordion-content-height)'
					}
				},
				'accordion-up': {
					from: {
						height: 'var(--radix-accordion-content-height)'
					},
					to: {
						height: '0'
					}
				},
				pulse: {
					'0%, 100%': { opacity: '1' },
					'50%': { opacity: '0.5' }
				},
				glow: {
					'0%, 100%': { boxShadow: '0 0 5px rgba(0, 201, 185, 0.5)' },
					'50%': { boxShadow: '0 0 15px rgba(0, 201, 185, 0.8)' }
				},
				fadeIn: {
					'0%': { opacity: '0', transform: 'translateY(10px)' },
					'100%': { opacity: '1', transform: 'translateY(0)' }
				}
			},
			animation: {
				'accordion-down': 'accordion-down 0.2s ease-out',
				'accordion-up': 'accordion-up 0.2s ease-out',
				'pulse-slow': 'pulse 2s infinite',
				'glow': 'glow 1.5s infinite',
				'fade-in': 'fadeIn 0.3s ease-out'
			},
			fontFamily: {
				mono: ['JetBrains Mono', 'Consolas', 'monospace'],
				sans: ['Inter', 'sans-serif']
			}
		}
	},
	plugins: [require("tailwindcss-animate")],
} satisfies Config;
