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
  onBrokenLinks: 'throw',
  onBrokenMarkdownLinks: 'warn',

  i18n: {
    defaultLocale: 'en',
    locales: ['en'],
  },

  presets: [
    [
      'classic',
      /** @type {import('@docusaurus/preset-classic').Options} */
      ({
        docs: {
          routeBasePath: "/",
          sidebarPath: require.resolve('./sidebars.js'),
          editUrl:
            'https://github.com/acorn-io/rubra-docs/tree/main',
        },
        blog: false,
        theme: {
          customCss: require.resolve('./src/css/custom.css'),
        },
      }),
    ],
  ],

  themeConfig:
    /** @type {import('@docusaurus/preset-classic').ThemeConfig} */
    ({
      navbar: {
        title: 'Docs',
        style: 'dark',
        logo: {
          alt: 'Acorn Logo',
          src: 'img/logo.svg',
        },
        items: [
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
