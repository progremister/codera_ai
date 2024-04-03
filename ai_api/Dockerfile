FROM rust:latest

WORKDIR /app

COPY Cargo.toml ./
RUN cargo build --release

COPY . .

EXPOSE 8888

CMD ["./target/release/ai_api"]