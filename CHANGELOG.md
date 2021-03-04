# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).


## [UNRELEASED]

### Added

- Matrix model from scratch.
- Perfect matrix validation for the values given.
- Option for making a matrix with a given dimension and fill value.
- Dynamic representation of the matrix.
- Tests for ensuring the matrix model works well.
- Added support for operations between matrices:
  - `+`: Addition
  - `-`: Subtraction
  - `*`: Multiplication
  - `/`: Division
  - `@`: For Matrix multiplications.
- An easier shortcut for accessing elements, and setting values:
  - Setting elements: `matrix[0, 0] = 4.3`
  - Getting elements: `matrix[1, 1]`

### Fixed

- Matrix accepting string values, or a list of string values.
- Matrix accepting a list of numbers, a.k.a vectors without filtering them.
- Matrix not functioning for single values like `Matrix(1)`.


[UNRELEASED]: https://github.com/janaSunrise/HypeMaths/releases/tag/v0.1.0
