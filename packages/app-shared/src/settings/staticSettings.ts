import type { StaticSettings } from './staticSettings.type';

export const staticSettings: StaticSettings = {
  admin: {
    email: 'first.last@openvaa.org'
  },
  appVersion: {
    version: 1,
    requireUserDataVersion: 1,
    source: 'https://github.com/OpenVAA/voting-advice-application'
  },
  dataAdapter: {
    type: 'strapi',
    supportsCandidateApp: true,
    supportsAdminApp: true
  },
  colors: {
    light: {
      primary: '#febe10',
      'primary-content': '#231f20',
      secondary: '#666666',
      accent: '#0a716b',
      neutral: '#333333',
      'base-100': '#ffffff',
      'base-200': '#fff2cf',
      'base-300': '#ffffff',
      warning: '#a82525',
      'line-color': '#d9d9d9'
    },
    dark: {
      primary: '#6887e3',
      'primary-content': '#ffffff',
      secondary: '#8c8c8c',
      accent: '#11a8a0',
      neutral: '#cccccc',
      'base-100': '#000000',
      'base-200': '#101212',
      'base-300': '#1f2324',
      warning: '#e16060',
      'line-color': '#262626'
    }
  },
  font: {
    name: 'Akko Pro',
    url: '/fonts/akko-pro.css',
    style: 'sans'
  },
  supportedLocales: [
    {
      code: 'en',
      name: 'English',
      isDefault: true
    },
    {
      code: 'fi',
      name: 'Suomi'
    },
    {
      code: 'sv',
      name: 'Svenska'
    },
    {
      code: 'da',
      name: 'Dansk'
    }
  ],
  analytics: {
    trackEvents: false
  },
  preRegistration: {
    enabled: false
  }
};
