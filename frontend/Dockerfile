FROM node:23-alpine

# Set the working directory in the container
WORKDIR /app

# Copy package.json and package-lock.json (if present) into the container
COPY package*.json ./

# Install dependencies
RUN npm install

# # Check if 'next' is installed correctly
# RUN npm ls next

# # Copy the rest of the app code into the container
COPY . .

# Expose the port that the app will run on
EXPOSE 3000

# # Build the Next.js app
# RUN npm run build


# Start the app
# CMD ["npm", "run", "dev"]


# # RUN npm run build
# # RUN npm install -g serve
# # CMD ["serve", "-s", "out"]
# CMD ["npm", "run", "dev"]