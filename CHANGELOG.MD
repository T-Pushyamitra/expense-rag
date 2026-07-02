# Changelog

All notable changes to this project will be documented in this file.

## Expense RAG 1.0.2 - 2026-07-02

### Statement Parser Service 0.6.0
#### Changed
- Parser now returns transactions page by page using generators.
- Statement Reader now returns document metadata (`document_id`, `document`, and page information).

### Common Library 0.2.0
#### Changed
- Moved the `Transaction` model to `common-lib`.

### Main Application
#### Added
- Added rabbit mq container

## Expense RAG 1.0.1 - 2026-07-01

### Main Application
#### Added
- Added project documentation.
- Added Poetry for dependency management.


## Expense RAG 1.0.0 - 2026-06-30

### Architecture
#### Changed
- Migrated from a monolithic service to a microservices architecture.


## Expense RAG 0.4.1 - 2026-06-28

### Statement Parser Service 0.5.0
#### Fixed
- Fixed static PDF parser table extraction settings.
- Fixed HDFC parser to update the current balance after every transaction.


## Expense RAG 0.4.0 - 2026-06-28

### Statement Parser Service 0.4.0
#### Added
- Added support for Axis Bank statements.
- Added `.env`.
- Added `resources/statements`.

#### Changed
- Updated the PDF parser to accept `None` as the password.


## Expense RAG 0.3.0 - 2026-06-27

### Statement Parser Service 0.3.0
#### Changed
- Completed the HDFC Bank statement parser.


## Expense RAG 0.2.0 - 2026-06-19

### Statement Parser Service 0.2.0
#### Added
- Introduced the initial HDFC Bank statement parser.


## Expense RAG 0.1.0 - 2026-06-14

### Statement Parser Service 0.1.0
#### Added
- Added mypy for static type checking.
- Added `.gitignore`.
- Added `src/parser/parser_impl.py`.