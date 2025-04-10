FROM node:23-alpine

WORKDIR /app

COPY . .

RUN npm install --production
RUN npm install @tailwindcss/postcss
RUN npm run build
EXPOSE 3000

CMD ["npm", "start"]

# # RUN npm run build
# # RUN npm install -g serve
# # CMD ["serve", "-s", "out"]
# CMD ["npm", "run", "dev"]