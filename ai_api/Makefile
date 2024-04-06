format:
	cargo fmt --quiet

lint:
	cargo clippy --quiet

test:
	cargo test --quiet

build:
	cargo build

builddocker:
	docker build -t hk_ai_api .

rundocker:
	docker run -it --rm -p 8888:8888 hk_ai_api

run:
	cargo run 

all: format lint build test run