#!/bin/bash

# Load NVM
export NVM_DIR="$HOME/.nvm"
[ -s "$NVM_DIR/nvm.sh" ] && \. "$NVM_DIR/nvm.sh"
[ -s "$NVM_DIR/bash_completion" ] && \. "$NVM_DIR/bash_completion"

# Install and use the desired Node.js version
nvm install --lts
nvm use --lts

# Install Yarn
npm install -g yarn

# Navigate to website directory
cd website

# Install dependencies
yarn install --frozen-lockfile --ignore-engines
pydoc-markdown

# Run Yarn server in the background
yarn start --port 3000 --host 0.0.0.0 &

# Wait a moment for the server to start
sleep 5

# Replace script with an interactive bash shell
exec bash
