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

FROM base AS strapi

WORKDIR /opt

# Copy only the packages we need
COPY --from=shared /opt/packages/app-shared ./packages/app-shared
COPY --from=shared /opt/packages/core ./packages/core
COPY --from=shared /opt/packages/data ./packages/data
COPY --from=shared /opt/backend/vaa-strapi ./backend/vaa-strapi

FROM strapi AS development

ARG NODE_ENV=development
ENV NODE_ENV=${NODE_ENV}

EXPOSE 1337

RUN yarn workspace @openvaa/strapi build
CMD yarn workspace @openvaa/strapi dev

FROM strapi AS production

ARG NODE_ENV=production
ENV NODE_ENV=${NODE_ENV}

EXPOSE 1337

RUN yarn workspace @openvaa/strapi build
CMD yarn workspace @openvaa/strapi start
