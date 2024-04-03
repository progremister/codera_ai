FROM openjdk:17-slim

WORKDIR /app

COPY pom.xml ./

COPY . .

RUN mvn package -DskipTests  # Build the project using Maven (adjust for Gradle)

EXPOSE 5432
