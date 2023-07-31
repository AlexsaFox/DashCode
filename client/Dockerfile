FROM node:20-alpine as builder

ARG API_HOST
ENV VITE_API_HOST $API_HOST

WORKDIR /app
RUN npm install -g pnpm

COPY package.json pnpm*.yaml .npmrc ./
RUN pnpm install --silent 

COPY . .
RUN pnpm build


FROM nginx:1.25.1-alpine-slim
WORKDIR /app
COPY --from=builder /app/dist .
