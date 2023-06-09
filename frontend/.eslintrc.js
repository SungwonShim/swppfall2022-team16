module.exports = {
  env: {
    browser: true,
    es2021: true,
    node: true,
    jest: true
  },
  extends: [
    'plugin:react/recommended',
    'standard-with-typescript'
  ],
  overrides: [
  ],
  parserOptions: {
    ecmaVersion: 'latest',
    sourceType: 'module',
    project: ['./tsconfig.json'],
    tsconfigRootDir: __dirname
  },
  plugins: [
    'react'
  ],
  ignorePatterns: [
    'react-app-env.d.ts',
    'setupTests.ts',
    'mock.tsx',
    'reportWebVitals.ts',
    '*.test.tsx'
  ],
  rules: {
  }
}
