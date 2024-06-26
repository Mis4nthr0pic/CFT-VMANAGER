CREATE TABLE admins (
    id SERIAL PRIMARY KEY,
    address VARCHAR(42) UNIQUE NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    address VARCHAR(42) UNIQUE NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE virtual_machines (
    id SERIAL PRIMARY KEY,
    id_contract INTEGER NOT NULL UNIQUE,
    id_host INTEGER NOT NULL UNIQUE,
    machine_name VARCHAR(42) NOT NULL,
    owner_address VARCHAR(42) NOT NULL,
    status NUMERIC NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (owner_address) REFERENCES users(address)
);

CREATE TABLE transactions (
    id SERIAL PRIMARY KEY,
    user_address VARCHAR(42) REFERENCES users(address),
    amount NUMERIC NOT NULL,
    transaction_type VARCHAR(10) NOT NULL, 
    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE processed_blocks (
    id SERIAL PRIMARY KEY,
    event_name VARCHAR(42) NOT NULL, 
    block NUMERIC NOT NULL,
    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Indexes
CREATE INDEX idx_admins_address ON admins(address);
CREATE INDEX idx_users_address ON users(address);
CREATE INDEX idx_virtual_machines_owner_address ON virtual_machines(owner_address);
CREATE INDEX idx_virtual_machines_status ON virtual_machines(status);
CREATE INDEX idx_transactions_user_address ON transactions(user_address);
CREATE INDEX idx_transactions_transaction_type ON transactions(transaction_type);
CREATE INDEX idx_processed_blocks_event_name ON processed_blocks(event_name);
