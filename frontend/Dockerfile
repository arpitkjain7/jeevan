FROM node:20.5-alpine
WORKDIR /app
COPY package.json .
RUN npm install
COPY . .


RUN npm run build:production

FROM nginx

COPY nginx.conf /etc/nginx/conf.d/default.conf

COPY --from=build /app/build /usr/share/nginx/html

EXPOSE 4200
