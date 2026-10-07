-- sample_data.sql
-- Sample farm expense records for the Farmer Input Cost Analyzer.
-- Fictional but realistic values. Includes the assignment's sample
-- record (F07, Cotton).
-- Load with:  python load_sample_data.py
-- Or manually: sqlite3 farmer_costs.db < sample_data.sql

INSERT INTO farm_expenses (farm_id, crop, seed_cost, fertilizer_cost, labour_cost, irrigation_cost)
VALUES ('F01', 'Rice',   6000,  9000, 14000, 8000);

INSERT INTO farm_expenses (farm_id, crop, seed_cost, fertilizer_cost, labour_cost, irrigation_cost)
VALUES ('F02', 'Cotton', 9000, 14000, 20000, 6000);

INSERT INTO farm_expenses (farm_id, crop, seed_cost, fertilizer_cost, labour_cost, irrigation_cost)
VALUES ('F03', 'Wheat',  5000,  8000, 10000, 5000);

INSERT INTO farm_expenses (farm_id, crop, seed_cost, fertilizer_cost, labour_cost, irrigation_cost)
VALUES ('F04', 'Tomato', 4000,  7000, 16000, 9000);

INSERT INTO farm_expenses (farm_id, crop, seed_cost, fertilizer_cost, labour_cost, irrigation_cost)
VALUES ('F05', 'Maize',  4500,  6500,  9000, 4000);

INSERT INTO farm_expenses (farm_id, crop, seed_cost, fertilizer_cost, labour_cost, irrigation_cost)
VALUES ('F07', 'Cotton', 8000, 12000, 18000, 7000);
