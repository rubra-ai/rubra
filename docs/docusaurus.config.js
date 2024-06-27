// @ts-check
// `@type` JSDoc annotations allow editor autocompletion and type checking
// (when paired with `@ts-check`).
// There are various equivalent ways to declare your Docusaurus config.
// See: https://docusaurus.io/docs/api/docusaurus-config

const lightCodeTheme = require('prism-react-renderer').themes.github;
const darkCodeTheme = require('prism-react-renderer').themes.dracula;

/** @type {import('@docusaurus/types').Config} */
const config = {
  title: 'Rubra Docs',
  tagline: 'Welcome to Rubra Docs',
  favicon: 'img/favicon.ico',
  url: 'https://docs.rubra.ai',
  baseUrl: '/',
  onBrokenLinks: 'warn',
  onBrokenMarkdownLinks: 'warn',

  i18n: {
    defaultLocale: 'en',
    locales: ['en'],
  },

  presets: [
    [
      "docusaurus-preset-openapi",
      {
        api: {
          path: require.resolve("./openapi.json"),
          routeBasePath: "/api",
        },
        docs: {
          sidebarPath: require.resolve("./sidebars.js"),
          routeBasePath: "/",
          editUrl:
            'https://github.com/rubra-ai/rubra/tree/main/docs',
        },
        theme: {
          customCss: require.resolve("./src/css/custom.css"),
        },
        blog: {
          showReadingTime: true,
          editUrl:
            'https://github.com/facebook/docusaurus/tree/main/packages/create-docusaurus/templates/shared/',
        },
      },
    ],
  ],

  themeConfig:
    /** @type {import('@docusaurus/preset-classic').ThemeConfig} */
    ({
      navbar: {
        style: 'dark',
        logo: {
          alt: 'Rubra Logo',
          src: 'img/logo.svg',
        },
        items: [
          {
            type: 'docSidebar',
            sidebarId: 'sidebar',
            position: 'left',
            label: 'Docs',
          },
          {
            to: 'https://docs.rubra.ai',
            label: 'Rubra Home',
            position: 'right',
            target: '_self',
          },
          {
            to: 'https://github.com/rubra-ai/rubra',
            label: 'GitHub',
            position: 'right',
          }
        ],
      },
      footer: {
        style: 'dark',
        links: [
          {
            label: 'GitHub',
            to: 'https://github.com/rubra-ai/rubra',
          },
          {
            label: 'Twitter',
            to: 'https://x.com/rubra_ai',
          },
          {
            label: 'Discord',
            to: 'https://discord.gg/swvAH2DXZH',
          },
        ],
        copyright: `Copyright © ${new Date().getFullYear()} Acorn Labs, Inc.`,
      },
      prism: {
        theme: lightCodeTheme,
        darkTheme: darkCodeTheme,
        additionalLanguages: ['cue', 'docker'],
      },
      algolia: {
        appId: 'H0MZLFQYNN',
        apiKey: '05ebe9667b7fbc5770fb052ad945646e',
        indexName: 'rubra',
      }
    }),
};

export default config;
