/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    './templates/**/*.html',
    './*/templates/**/*.html'
  ],
  theme: {
    extend: {
      colors: {
        'brand': '#DEAAF2',
        'brand-hv': '#EFC0F9',
        'brand-light':'#F9DFFF',
        'brand-dark': '#201A34',
        'brand-dark-xl': '#141020',
      },
      fontFamily: {
        'poppins': ['Poppins'],
        'handlee': ['Handlee'],
        'pangolin': ['Pangolin'],
     }
    },
  },
  plugins: [],
}

