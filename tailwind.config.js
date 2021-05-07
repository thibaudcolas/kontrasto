const brandColors = {
  "pale-blue": "#bac7da",
  "dark-blue": "#242526",
  "dark-turquoise": "#263347",
  "snake-green": "#00BC74",
};

const grayScale = {
  white: "#FFFFFF",
  "gray-light": "#F5F5F5",
  "gray-light-mid": "#D8D8D8",
  "gray-mid": "#949494",
  "gray-mid-dark": "#6F6F6F",
  "gray-dark": "#222222",
  black: "#000000",
};

module.exports = {
  mode: "jit",
  purge: [
    "./kontrasto/**/*.{js,ts,jsx,tsx,py,html}",
    "./demo/**/*.{js,ts,jsx,tsx,py,html}",
  ],
  darkMode: false, // or 'media' or 'class'
  theme: {
    colors: {
      ...brandColors,
      ...grayScale,
      transparent: "transparent",
      current: "currentColor",
    },
    fontWeight: {
      // thin: 100,
      // extralight: 200,
      // light: 300,
      normal: 400,
      // medium: 500,
      // semibold: 600,
      bold: 700,
      // extrabold: 800,
      // black: 900,
    },
    extend: {
      screens: {
        print: { raw: "print" },
      },
    },
  },
  variants: {
    extend: {},
  },
  plugins: [require("tailwindcss-rtl")],
};
