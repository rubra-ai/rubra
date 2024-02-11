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
            'https://github.com/acorn-io/rubra/tree/main/docs',
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
          alt: 'Acorn Logo',
          src: 'img/logo.svg',
        },
        items: [
          {
            type: 'docSidebar',
            sidebarId: 'sidebar',
            position: 'left',
            label: 'Docs',
          },
          { to: "/api", label: "API Reference", position: "left" },
          {
            to: 'https://rubra.ai',
            label: 'Rubra Home',
            position: 'right',
            target: '_self',
          },
          {
            to: 'https://github.com/acorn-io/rubra',
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
            to: 'https://github.com/acorn-io/runtime',
          },
          {
            label: 'Users Slack',
            to: 'https://slack.acorn.io',
          },
          {
            label: 'Twitter',
            to: 'https://twitter.com/acornlabs',
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
    }),
};

export default config;
