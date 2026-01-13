/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx}",
  ],
  theme: {
    screens: {
      'xs': '375px',     // iPhone SE, iPhone 12 mini
      'sm': '640px',     // iPhone 12/13/14 Pro Max (portrait)
      'md': '768px',     // iPad mini (portrait)
      'lg': '1024px',    // iPad (portrait)
      'xl': '1280px',    // Desktop
      '2xl': '1536px',   // Large desktop
    },
    extend: {
      spacing: {
        'safe-top': 'env(safe-area-inset-top)',
        'safe-bottom': 'env(safe-area-inset-bottom)',
        'safe-left': 'env(safe-area-inset-left)',
        'safe-right': 'env(safe-area-inset-right)',
      },
      minHeight: {
        'screen-safe': 'calc(100vh - env(safe-area-inset-top) - env(safe-area-inset-bottom))',
      },
      fontSize: {
        'xs-mobile': ['0.75rem', { lineHeight: '1rem' }],     // 12px
        'sm-mobile': ['0.875rem', { lineHeight: '1.25rem' }], // 14px
        'base-mobile': ['1rem', { lineHeight: '1.5rem' }],    // 16px
        'lg-mobile': ['1.125rem', { lineHeight: '1.75rem' }], // 18px
        'xl-mobile': ['1.25rem', { lineHeight: '1.75rem' }],  // 20px
        '2xl-mobile': ['1.5rem', { lineHeight: '2rem' }],     // 24px
        '3xl-mobile': ['1.875rem', { lineHeight: '2.25rem' }], // 30px
        '4xl-mobile': ['2.25rem', { lineHeight: '2.5rem' }],   // 36px
        '5xl-mobile': ['3rem', { lineHeight: '1' }],          // 48px
        '6xl-mobile': ['3.75rem', { lineHeight: '1' }],        // 60px
      },
      fontFamily: {
        'destiny': ['"Noto Serif SC"', 'serif'], // 中文字体
        'destiny-en': ['"Playfair Display"', 'serif'], // 英文字体
      },
      animation: {
        'fade-in': 'fadeIn 0.5s ease-in-out',
        'slide-up': 'slideUp 0.3s ease-out',
        'slide-up-mobile': 'slideUp 0.4s ease-out', // 移动端稍慢的动画
        'pulse-slow': 'pulse 2s cubic-bezier(0.4, 0, 0.6, 1) infinite',
        'bounce-subtle': 'bounce 0.6s ease-in-out', // 移动端更柔和的弹跳
      },
      keyframes: {
        fadeIn: {
          '0%': { opacity: '0' },
          '100%': { opacity: '1' },
        },
        slideUp: {
          '0%': { transform: 'translateY(20px)', opacity: '0' },
          '100%': { transform: 'translateY(0)', opacity: '1' },
        },
      },
    },
  },
  plugins: [],
}