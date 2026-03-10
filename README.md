# Jekyll SEO News Theme V2

A professional, modern Jekyll theme for news and blog websites, fully optimized for Bing & Google SEO.

## ✨ Features

### SEO Optimization
- Full TDK support (Title, Description, Keywords)
- Open Graph tags (og:title, og:description, og:image, og:url, og:type)
- Twitter Card meta tags
- Canonical URL
- Robots meta tag
- JSON-LD Structured Data: NewsArticle, BreadcrumbList, Organization, WebSite, FAQ
- Auto-generated sitemap.xml
- robots.txt

### IndexNow Auto Push
- Automatic URL submission to Bing & Yandex via IndexNow API
- Script: `/scripts/indexnow.js`
- Configured for: `clashwindow.github.io`

### Article Features
- Auto-generated Table of Contents (H2/H3)
- Breadcrumb navigation
- Related posts
- Author box
- Publish date & last modified date
- Tags & categories
- FAQ schema markup support
- Internal linking based on tags/categories

### Social Share Buttons
Twitter · Facebook · Telegram · Reddit · WhatsApp · Copy Link

### Performance
- TailwindCSS for styling
- Lazy loading images
- Minified CSS/JS
- Preload fonts
- Responsive design (mobile-first)

### Jekyll Plugins
```
- jekyll-seo-tag
- jekyll-sitemap
- jekyll-feed
- jekyll-paginate
- jekyll-last-modified-at
- jekyll-archives
```

## 🚀 Quick Start

```bash
# Install dependencies
bundle install
npm install

# Build TailwindCSS
npm run build:css

# Start development server
bundle exec jekyll serve
```

## ⚙️ Configuration

Edit `_config.yml`:

```yaml
title: Your Site Title
description: Your site description
url: https://clashwindow.github.io
baseurl: ""

indexnow:
  key: 8575fe8139f14b2da85e40bbc8b86ce2
  host: clashwindow.github.io
```

## 📝 Creating Posts

```yaml
---
layout: post
title: "Your Post Title"
date: 2026-03-10
last_modified_at: 2026-03-10
categories: [technology]
tags: [jekyll, seo]
author: Your Name
image: /assets/images/post-image.jpg
description: "Post meta description"
faq:
  - question: "What is Jekyll?"
    answer: "Jekyll is a static site generator."
---
```

## 🗂️ Project Structure

```
├── _layouts/          # Page layouts
├── _includes/         # Reusable components
├── _posts/            # Blog posts
├── _sass/             # SCSS styles
├── assets/            # CSS, JS, images
├── scripts/           # IndexNow push script
├── categories/        # Category pages
├── tags/              # Tag pages
├── _config.yml        # Site configuration
├── Gemfile            # Ruby dependencies
├── package.json       # Node dependencies
├── tailwind.config.js # TailwindCSS config
└── robots.txt         # SEO robots file
```

## 📄 License

MIT License

---

Built with ❤️ for SEO-optimized Jekyll sites.
