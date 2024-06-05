# Use an official Node.js runtime as the base image
FROM node:alpine

# Set the working directory in the Docker image to /app
WORKDIR /apps/reposter-react

# Copy package.json and package-lock.json into the image
COPY ./reposter-react .

# Install the application's dependencies inside the Docker image
RUN npm install

# Copy the rest of the application code into the image
#COPY reposter-react/ .
# Expose port 3000 in the Docker image
EXPOSE 3000

# Define the command that should be executed when the Docker image is run
CMD [ "npm", "run", "dev" ]