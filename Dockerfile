# Build stage
FROM node:22.7.0-alpine AS build

WORKDIR /app

COPY package*.json ./
COPY tsconfig.json ./
COPY vite.config.ts ./

RUN npm ci

COPY . .

RUN npm run build

# Production stage
FROM node:22.7.0-alpine AS production

WORKDIR /app

COPY --from=build /app/dist ./dist
COPY package*.json ./

RUN npm install 

EXPOSE 3000

CMD ["npm", "run", "preview"]
