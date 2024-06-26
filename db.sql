#todo: setup foreing keys
CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    address VARCHAR(42) UNIQUE NOT NULL,
    minute_credits NUMERIC NOT NULL
)
CREATE TABLE virtual_machines (
    id SERIAL PRIMARY KEY,
	id_contract SERIAL NOT NULL UNIQUE,
	id_host SERIAL NOT NULL UNIQUE,
    machine_name VARCHAR(42) NOT NULL, -- e.g., "deposit"
    owner_address VARCHAR(42),
    status numeric NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP	
);

CREATE TABLE transactions (
    id SERIAL PRIMARY KEY,
    user_address VARCHAR(42) REFERENCES users(address),
    amount NUMERIC NOT NULL,
    transaction_type VARCHAR(10) NOT NULL, -- e.g., "deposit"
    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE processed_blocks (
    id SERIAL PRIMARY KEY,
    event_name VARCHAR(42) NOT NULL, -- e.g., "deposit"
    block numeric NOT NULL,
    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);