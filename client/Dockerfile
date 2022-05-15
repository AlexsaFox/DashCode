FROM node:latest as builder

ARG API_HOST
ENV VITE_API_HOST $API_HOST

WORKDIR /app
RUN npm install -g pnpm

COPY package.json pnpm*.yaml .npmrc ./
RUN pnpm install --silent

COPY . .
RUN pnpm build


FROM nginx
WORKDIR /app
COPY --from=builder /app/dist .
