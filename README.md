# OpenVAA Talentia

This repository contains a customized Voting Advice Application (VAA) for Talentia, based on the OpenVAA open-source platform.

## Overview

The application adapts OpenVAA for Talentia's elections and voting advice needs.

The implementation includes:

- a voter-facing Voting Advice Application
- election, candidate and question data managed with Strapi
- import of candidate and election data from external sources
- Talentia-specific content, visual customization and configuration
- OpenVAA's matching and data-processing functionality

Candidate responses can be collected externally and imported into the application. The implementation does not require OpenVAA's candidate application.

## Background

The project is based on the OpenVAA platform, an open-source framework for building Voting Advice Applications.

Original OpenVAA repository:

https://github.com/OpenVAA/voting-advice-application

OpenVAA documentation:

https://openvaa.org/

## Technology

The application uses the technologies and monorepo architecture provided by OpenVAA. Key components include:

- **Frontend:** Svelte / SvelteKit
- **Backend:** Strapi (headless CMS)
- **Database:** PostgreSQL
- **Infrastructure:** Docker and Docker Compose
- **Package management:** Yarn
- **Unit testing:** Vitest

## Repository Structure

The repository follows the OpenVAA monorepo structure. The main areas relevant to the Talentia implementation include:

- `frontend/` – voter-facing application and Talentia-specific UI customization
- `backend/vaa-strapi/` – Strapi backend, content management and data model
- `packages/` – shared OpenVAA packages and application logic

## Data and Content

Election-related content is managed through Strapi and imported data sources.

The repository contains application code and configuration. Production data, credentials, secrets and other environment-specific information are managed separately from the source code.

## OpenVAA

This project is a customized implementation of OpenVAA. For general information about OpenVAA's architecture, development and deployment, refer to the upstream OpenVAA documentation and repository.