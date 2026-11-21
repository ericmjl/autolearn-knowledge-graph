import { QuartzConfig } from "./quartz/cfg"
import * as Plugin from "./quartz/plugins"

/**
 * Quartz 4 configuration for the autolearn knowledge wiki.
 * Theme: "Bench Notes", proposed by Inkling 2 Mini (see site/theme.json).
 *
 * This file is copied onto a pinned Quartz v4 checkout at build time. It is
 * not used from ``site/`` directly; see ``site/build.py``.
 *
 * Vault markdown is left in place. Wikilinks use Obsidian's shortest-path
 * format (including ``[[target|alias]]``), matching ``.obsidian/app.json``.
 */
const config: QuartzConfig = {
  configuration: {
    pageTitle: "Building, Evaluating, Securing Agents",
    pageTitleSuffix: "",
    enableSPA: true,
    enablePopovers: true,
    analytics: null,
    locale: "en-US",
    baseUrl: "ericmjl.github.io/autolearn-knowledge-graph",
    ignorePatterns: [".obsidian", ".git", ".github", "private", "templates"],
    defaultDateType: "created",
    theme: {
      fontOrigin: "googleFonts",
      cdnCaching: true,
      typography: {
        header: "Fraunces",
        body: "Source Serif 4",
        code: "IBM Plex Mono",
      },
      colors: {
        lightMode: {
          light: "#f8f7f4",
          lightgray: "#efede7",
          gray: "#d6d3ca",
          darkgray: "#5c5f66",
          dark: "#1f232b",
          secondary: "#0d5c4d",
          tertiary: "#9a4a08",
          highlight: "rgba(245, 158, 11, 0.22)",
          textHighlight: "#f5d48a88",
        },
        darkMode: {
          light: "#15171c",
          lightgray: "#22252c",
          gray: "#3a3e47",
          darkgray: "#a9a69c",
          dark: "#ece9e0",
          secondary: "#7fd8c0",
          tertiary: "#e8b06a",
          highlight: "rgba(232, 176, 106, 0.20)",
          textHighlight: "#b07a2a66",
        },
      },
    },
  },
  plugins: {
    transformers: [
      Plugin.FrontMatter(),
      Plugin.CreatedModifiedDate({
        priority: ["frontmatter", "filesystem"],
      }),
      Plugin.SyntaxHighlighting({
        theme: {
          light: "github-light",
          dark: "github-dark",
        },
        keepBackground: false,
      }),
      Plugin.ObsidianFlavoredMarkdown({ enableInHtmlEmbed: false }),
      Plugin.GitHubFlavoredMarkdown(),
      Plugin.TableOfContents(),
      Plugin.CrawlLinks({ markdownLinkResolution: "shortest" }),
      Plugin.Description(),
      Plugin.Latex({ renderEngine: "katex" }),
    ],
    filters: [Plugin.RemoveDrafts()],
    emitters: [
      Plugin.AliasRedirects(),
      Plugin.ComponentResources(),
      Plugin.ContentPage(),
      Plugin.FolderPage(),
      Plugin.TagPage(),
      Plugin.ContentIndex({
        enableSiteMap: true,
        enableRSS: true,
      }),
      Plugin.Assets(),
      Plugin.Static(),
      Plugin.Favicon(),
      Plugin.NotFoundPage(),
    ],
  },
}

export default config
