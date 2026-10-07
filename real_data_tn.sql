-- real_data_tn.sql
-- GOVERNMENT REFERENCE DATA — Tamil Nadu
-- Real, open-source farm cost data for the Farmer Input Cost Analyzer.
--
-- DATA SOURCE AND PROVENANCE
--   Official source : Directorate of Economics and Statistics, Tamil Nadu
--                     (tnagriculture.in dashboard)
--   Table           : "XI.1: Cost of Cultivation for Principal Agricultural Crops"
--   URL             : https://www.tnagriculture.in/dashboard/report/11_01.pdf
--   Unit            : rupees per hectare (state-average cost of cultivation)
--
-- FIELD MAPPING (project schema <- official table rows):
--   farm_id         <- "TN-<CROP>" (identifier only; see statement below)
--   crop            <- crop name from the source table
--   seed_cost       <- official "IV Seed"
--   fertilizer_cost <- official "V Fertilizer & Manure" TOTAL
--                      (chemical fertilizer + organic manure, as grouped
--                      in the source table)
--   labour_cost     <- official "I Human Labour" TOTAL
--                      (casual + attached + family labour)
--   irrigation_cost <- 0 (see note below)
--
-- FIELDS OMITTED (present in the official table but outside this project's
-- four-category schema): bullock labour, machine labour, insecticides,
-- interest on working capital, and fixed costs (rental value of owned land,
-- land revenue/cesses, depreciation, interest on fixed capital).
--
-- WHY IRRIGATION IS ZERO: the source table reports no separate irrigation
-- charge for these crops (Tamil Nadu provides free electricity for
-- agriculture, so the charge is negligible and subsumed under machine
-- labour). It is recorded as 0 rather than inventing a number.
--
-- TERMINOLOGY: the program's "Total Cost" for these records is the
-- "Project Input Cost" (sum of the four project categories only). It is NOT
-- the official total cost of cultivation, which includes the additional
-- components listed above.
--
-- EXPLICIT STATEMENT: these figures are published crop-level
-- averages/reference values from a government table. They are NOT individual
-- surveyed farms, NOT our own field survey, and are used only to
-- validate/demonstrate the implementation.
--
-- Load with:  python load_real_data.py
-- (Safe to re-run: existing farm IDs are skipped.)

INSERT INTO farm_expenses (farm_id, crop, seed_cost, fertilizer_cost, labour_cost, irrigation_cost)
VALUES ('TN-PADDY', 'Paddy', 2491, 12314, 26860, 0);

INSERT INTO farm_expenses (farm_id, crop, seed_cost, fertilizer_cost, labour_cost, irrigation_cost)
VALUES ('TN-SORGHUM', 'Sorghum', 1560, 7446, 23094, 0);

INSERT INTO farm_expenses (farm_id, crop, seed_cost, fertilizer_cost, labour_cost, irrigation_cost)
VALUES ('TN-MAIZE', 'Maize', 6041, 15298, 30364, 0);

INSERT INTO farm_expenses (farm_id, crop, seed_cost, fertilizer_cost, labour_cost, irrigation_cost)
VALUES ('TN-BLACKGRAM', 'Black gram', 2598, 6627, 16909, 0);

INSERT INTO farm_expenses (farm_id, crop, seed_cost, fertilizer_cost, labour_cost, irrigation_cost)
VALUES ('TN-GROUNDNUT', 'Groundnut', 10599, 13542, 31561, 0);

INSERT INTO farm_expenses (farm_id, crop, seed_cost, fertilizer_cost, labour_cost, irrigation_cost)
VALUES ('TN-GINGELLY', 'Gingelly', 1079, 8902, 25837, 0);

INSERT INTO farm_expenses (farm_id, crop, seed_cost, fertilizer_cost, labour_cost, irrigation_cost)
VALUES ('TN-COTTON', 'Cotton', 3196, 16301, 57126, 0);

INSERT INTO farm_expenses (farm_id, crop, seed_cost, fertilizer_cost, labour_cost, irrigation_cost)
VALUES ('TN-SUGARCANE', 'Sugarcane', 26122, 30265, 124237, 0);
