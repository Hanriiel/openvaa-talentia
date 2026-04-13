FROM node:20 AS base

COPY certs/cisco-umbrella-root.crt /usr/local/share/ca-certificates/cisco-umbrella-root.crt
RUN apt-get update && apt-get install -y ca-certificates && update-ca-certificates

WORKDIR /opt

# Setup env variable for yarn
ENV YARN_VERSION=4.6
ENV NODE_EXTRA_CA_CERTS=/usr/local/share/ca-certificates/cisco-umbrella-root.crt

# install and use yarn 4.x
RUN corepack enable && corepack prepare yarn@${YARN_VERSION}

# Skip Husky installation in Docker
ENV HUSKY=0

COPY package.json yarn.lock .yarnrc.yml ./
COPY .yarn ./.yarn
# To be able to use --immutable, we need to copy all the packages in the workspace
COPY backend backend
COPY docs docs
COPY frontend frontend
COPY packages packages
RUN yarn install --immutable

FROM base AS shared

WORKDIR /opt

# Build all shared modules
RUN yarn build:shared

FROM base AS frontend

WORKDIR /opt

# Copy only the packages we need
COPY --from=shared /opt/packages packages
COPY --from=shared /opt/frontend frontend

FROM frontend AS development

WORKDIR /opt

EXPOSE 5173
CMD yarn workspace @openvaa/frontend dev --host

FROM frontend AS production

ARG NODE_ENV=production
ENV NODE_ENV=${NODE_ENV}

WORKDIR /opt

RUN yarn workspace @openvaa/frontend build

EXPOSE 3000
CMD node ./frontend/build/index.js