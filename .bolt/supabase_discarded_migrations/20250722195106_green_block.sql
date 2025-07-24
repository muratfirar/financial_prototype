-- Initialize database for Financial Risk Management Platform
CREATE DATABASE financial_risk_db;
CREATE USER financial_user WITH PASSWORD 'financial_password';
GRANT ALL PRIVILEGES ON DATABASE financial_risk_db TO financial_user;