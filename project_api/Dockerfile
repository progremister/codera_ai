FROM openjdk:21-slim

WORKDIR /app

COPY pom.xml ./

COPY . .

RUN mvn package

EXPOSE 5432