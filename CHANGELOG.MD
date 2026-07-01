# Changelog

All notable changes to this project will be documented in this file.

## statement-parser-service 0.1.0 - 2026-06-14
### Added
- Added mypy to project for checking type hint
- Added .gitignore
- Added src/parser/parser_impl.py

## statement-parser-service 0.2.0 - 2026-06-19
### Added
- Introduced the initial bank statement parser (Step 0) with support for HDFC Bank statements.

## statement-parser-service 0.3.0 - 2026-06-27
### Changed
- Completed parsing HDFC bank statment

## statement-parser-service 0.4.0 - 2026-06-28
### Added 
- Added parser for Axis bank statement
- Add .env, and resource/statements 

### Changed 
- Pdf Parser (pdf_parser) should accept password as none

## statement-parser-service 0.4.1 - 2026-06-28
### Fixed
- Pdf parser table settings were static
- HDFC parser, current balance was not updated after each transaction

## Expense RAG 1.0.0 - 2026-06-30
### Changed 
- Shifted to mono service to microservice

## Expense RAG 1.0.1 - 2026-06-01
### Added
- Added docs
- Added poetry to project