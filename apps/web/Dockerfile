FROM node:20-alpine AS dependencies
WORKDIR /app
COPY package.json package-lock.json ./
COPY apps/web/package.json apps/web/package.json
RUN npm ci

FROM node:20-alpine AS build
WORKDIR /app
ARG CHOICELAB_API_URL=http://api:8000
ARG NEXT_PUBLIC_CHOICELAB_DEMO_MODE=true
ENV CHOICELAB_API_URL=$CHOICELAB_API_URL
ENV NEXT_PUBLIC_CHOICELAB_DEMO_MODE=$NEXT_PUBLIC_CHOICELAB_DEMO_MODE
COPY --from=dependencies /app/node_modules ./node_modules
COPY . .
RUN npm run build

FROM node:20-alpine AS runtime
WORKDIR /app
ENV NODE_ENV=production
COPY --from=build /app/package.json /app/package-lock.json ./
COPY --from=build /app/apps/web ./apps/web
COPY --from=build /app/node_modules ./node_modules
EXPOSE 3000
CMD ["npm", "run", "start"]
