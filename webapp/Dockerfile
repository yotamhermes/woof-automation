FROM node:18-alpine as build 

WORKDIR /webapp

COPY package*.json .

RUN npm install

COPY . .

ARG REACT_APP_WOOF_URL
ENV REACT_APP_WOOF_URL $REACT_APP_WOOF_URL

ARG REACT_APP_WOOF_API_KEY
ENV REACT_APP_WOOF_API_KEY $REACT_APP_WOOF_API_KEY

RUN npm run build

FROM nginx:1.19

COPY ./nginx/nginx.conf /etc/nginx/nginx.conf

COPY --from=build /webapp/build /usr/share/nginx/html