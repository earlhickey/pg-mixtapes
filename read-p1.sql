CREATE TABLE energy(
   id INTEGER PRIMARY KEY AUTOINCREMENT,
   power_usage_low NUMERIC,
   power_usage_hi NUMERIC,
   power_return_low NUMERIC,
   power_return_hi NUMERIC,
   current_power_usage NUMERIC,
   current_power_return NUMERIC,
   gas_usage NUMERIC,
   datetime TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX datetime_index ON energy (datetime);
