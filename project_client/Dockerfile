FROM node:alpine AS builder

WORKDIR /app

COPY package*.json ./

RUN npm install

# Switch to a smaller runtime image
FROM node:alpine

WORKDIR /app

COPY . .

# Expose port 3000 (default for Next.js)
EXPOSE 3000

# Start the Next.js development server
CMD [ "npm", "run", "dev" ]