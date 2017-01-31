create database climate_analysis character set 'utf8mb4' collate 'utf8mb4_unicode_ci';

create user climate_analysis@'localhost' identified by 'climate_analysis';

grant all privileges on climate_analysis.* to climate_analysis@'localhost';