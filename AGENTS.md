# MyStory Agent Protocol & MDX Conventions

This document serves as a standard ruleset for any developers or AI agents interacting with my personal storytelling platform. It explains the core rendering logic, MDX syntax, and folder structuring necessary to maintain my ecosystem.

## 0. READ RULES FIRST, before editing or writing any content.

Rules path: `content/stories/kisho/docs/rules.md`

## 1. Architecture: Books & Chapters

The system operates strictly on a hierarchical **Books and Pages** approach located at `content/stories/`.

- **Books (Folders):** Every subfolder inside the `content/stories/` directory acts as a discrete "Book".
  - The folder's name acts as the system's `bookSlug` (e.g., `the-wizard-of-oz`).
  - The platform automatically formats this slug into a readable title ("The Wizard Of Oz") for the Library UI.
- **Chapters Subfolder:** Finished `.mdx` chapter files live inside a `chapters/` subfolder of each book (e.g., `content/stories/kisho/chapters/chapter1.mdx`).
  - The file name acts as the `pageSlug` (e.g., `chapter1.mdx` -> `chapter1`).
  - The system recursively scans book folders for `.mdx` files, skipping `docs/`, `library/`, and `assets/` directories.
  - Prefixing file names with logical numbers enables natural sorting for the Table of Contents & Pagination.

## 2. Frontmatter Properties

All `.mdx` content files MUST begin with a YAML Frontmatter block delineated by triple dashes (`---`). The parser does not use `gray-matter`, but instead relies on a lightweight browser-safe regex implementation inside `utils/markdown.ts`.

### Core Properties

```yaml
---
title: "Chapter 1: An Expected Journey"
cover: "url_to_image"
---
```

## 3. Yerelleştirme (Localization):

- **Yerelleştirme (Localization):** Sadece dil çevirisi yapmakla kalmayıp, içeriği hedef kitlenin kültürüne, geleneklerine, deyimlerine ve günlük alışkanlıklarına (örneğin ölçü birimleri, mizah, kültürel referanslar) uygun hale getirme işlemidir. İçeriğin o kültüre aitmiş gibi doğal hissettirmesini sağlar.

