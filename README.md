# Talentia Voting Advice Application

This project is a customized Voting Advice Application (VAA) developed for Talentia, built using the OpenVAA open-source platform.

## Overview

The goal of this project is to adapt the OpenVAA platform for Talentia’s use case, particularly for Finnish parliamentary elections (Eduskuntavaalit 2026).

The project focuses on:
- understanding and adapting the OpenVAA data model
- managing election, candidate, and question data via Strapi
- integrating external survey data (e.g. Zeff)
- building a functional and maintainable VAA solution

## Background

The project is developed as part of an internship for Talentia. It is based on the OpenVAA platform, which provides a flexible foundation for building Voting Advice Applications.

Original OpenVAA repository:  
https://github.com/OpenVAA/voting-advice-application

## Tech Stack

- **Frontend:** React (OpenVAA)
- **Backend:** Strapi (Headless CMS)
- **Database:** PostgreSQL
- **Infrastructure:** Docker & Docker Compose
- **Package management:** Yarn (monorepo)

## Project Structure

This repository is based on the OpenVAA monorepo structure, including:

- `frontend/` – VAA user interface
- `backend/vaa-strapi/` – Strapi backend and data model
- `packages/` – shared logic and data handling

## Current Status

The project is currently in the early phase, focusing on:
- understanding the system architecture
- setting up the development environment
- exploring and simplifying the data model

## Future Work

Planned next steps include:
- defining a minimal dataset for a single election
- implementing data import from external sources (e.g. Zeff)
- customizing the frontend for Talentia’s needs
- refining the data model and relationships

## Notes

This repository is a fork of the OpenVAA project and is being adapted to support Talentia-specific requirements. The implementation may diverge from the original project as customization progresses.

---

## About OpenVAA (Original Project)

OpenVAA is a comprehensive open-source framework for building configurable [Voting Advice Applications](https://openvaa.org/publishers-guide/what-are-vaas/intro) (VAAs). It's designed to work in any election context and is fully localisable, accessible, modular and free to use.

OpenVAA was built for two reasons: to offer a transparent alternative for proprietary VAAs, and to kickstart development of more and better VAAs. OpenVAA is built by developers and researchers and maintained by a [Finnish non-profit](https://openvaa.org/about/association) of the same name.
