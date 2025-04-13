FROM node:18-alpine

WORKDIR /miniapp_frontend

COPY /frontend/package*.json ./

RUN npm install

COPY /frontend .

ENV VITE_DISABLE_DEVTOOLS=true
ENV CHOKIDAR_USEPOLLING=true

EXPOSE 5173

CMD ["npm", "run", "dev", "--", "--host", "--port", "5173"]
