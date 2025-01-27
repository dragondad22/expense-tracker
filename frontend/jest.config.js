const nextJest = require('next/jest');

const createJestConfig = nextJest({
  dir: './',
});

const customJestConfig = {
  testEnvironment: 'jest-environment-jsdom', // Explicitly set the test environment
  transform: {
    '^.+\\.(js|jsx|ts|tsx)$': 'babel-jest', // Transform ES Modules with Babel
  },
  moduleDirectories: ['node_modules', '<rootDir>/'],
};

module.exports = createJestConfig(customJestConfig);
