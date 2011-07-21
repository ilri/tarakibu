-- Clear the base data from the database
-- We want to have a clean version of the sampler, so lets delete all the unnecessary data

-- clear samples
truncate samples;

-- clear sample_reads
truncate sample_reads;

-- clear animal_reads
truncate animal_reads;

-- clear gps_data
truncate gps_data;
