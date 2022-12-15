/* eslint-disable @typescript-eslint/no-var-requires */
/* eslint-disable no-undef */

const colors = require("tailwindcss/colors")

/** @type {import('tailwindcss').Config} */
module.exports = {
  content: ["./snd-client/index.html", "./snd-client/src/**/*.{js,ts,jsx,tsx}"],
  theme: {
    extend: {
      colors: {
        color: {
          primary: colors.slate["900"],
          secondary: colors.slate["400"],
          "secondary-lessish": colors.slate["200"],
          "secondary-less": colors.slate["50"],
          active: colors.sky["500"],
          "active-lessish": colors.sky["300"],
          "active-less": colors.sky["100"],
          background: colors.neutral["50"],
        },
      },
    },
  },
  plugins: [],
}
