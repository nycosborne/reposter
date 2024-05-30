# Use an official Node.js runtime as the base image
FROM node:16-alpine

# Set the working directory in the Docker image to /app
WORKDIR /app

# Copy package.json and package-lock.json into the image
COPY reposter-react/package*.json ./
#RUN rm -rf node_modules
#RUN rm -rf package-lock.json

# Install the application's dependencies inside the Docker image
RUN npm install

# Copy the rest of the application code into the image
COPY reposter-react/ .

RUN npm install
# Expose port 3000 in the Docker image
EXPOSE 3000

# Define the command that should be executed when the Docker image is run
CMD [ "npm", "start" ]