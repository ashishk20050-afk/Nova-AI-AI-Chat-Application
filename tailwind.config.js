/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    "./templates/*.html"
  ],
  theme: {
    extend: {
      colors:{
        chatblack:'#343541',
        sidebar:'#202123',
        chatbox:'#444654'
      }
    },
  },
  plugins: [],
}