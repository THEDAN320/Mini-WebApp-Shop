module.exports = {
  root: true,
  env: {
    node: true,
  },
  extends: [
    "plugin:vue/vue3-essential",
    "eslint:recommended",
    "@vue/typescript/recommended",
    "plugin:prettier/recommended",
    "plugin:tailwindcss/recommended",
    "prettier",
  ],
  parserOptions: {
    ecmaVersion: 2020,
    // project: "./tsconfig.json", // ???
  },
  rules: {
    "no-console": process.env.NODE_ENV === "production" ? "warn" : "off",
    "no-debugger": process.env.NODE_ENV === "production" ? "warn" : "off",
    "tailwindcss/no-custom-classname": 0,
  },
  plugins: [
    "tailwindcss",
    // "@typescript-eslint" // ??
    "prettier",
  ],
  ignorePatterns: ["node_modules"],
};
