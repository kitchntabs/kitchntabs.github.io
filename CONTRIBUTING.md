# Contributing to KitchnTabs Documentation

Thank you for your interest in contributing to KitchnTabs documentation! This guide will help you understand how to contribute effectively.

## 📋 Table of Contents

- [Getting Started](#getting-started)
- [Documentation Standards](#documentation-standards)
- [Style Guide](#style-guide)
- [Submitting Changes](#submitting-changes)
- [Review Process](#review-process)

---

## 🚀 Getting Started

### Prerequisites

- Git
- Ruby (for Jekyll)
- Basic knowledge of Markdown

### Local Setup

```bash
# Clone the repository
git clone https://github.com/kitchntabs/kitchntabs.github.io.git
cd kitchntabs.github.io

# Install dependencies
bundle install

# Run locally
bundle exec jekyll serve

# View at http://localhost:4000
```

---

## 📝 Documentation Standards

### File Structure

```
docs/
├── mall-app/          # Mall application docs
├── customer-app/      # Customer app docs
├── staff-app/         # Staff app docs
└── tech/              # Technical documentation
    ├── features/      # Feature documentation
    ├── architecture/  # System architecture
    └── toolchain/     # Build & deployment
```

### Naming Conventions

- **Files**: Use kebab-case: `my-document.md`
- **Directories**: Use lowercase with hyphens: `my-feature/`
- **Images**: Store in `/assets/` with descriptive names

### Front Matter

All documentation files should include YAML front matter:

```yaml
---
title: Document Title
layout: default
nav_order: 1
parent: Parent Section (optional)
---
```

---

## 🎨 Style Guide

### Markdown Formatting

#### Headers

```markdown
# H1 - Document Title (only one per page)
## H2 - Main Section
### H3 - Subsection
#### H4 - Minor Section
```

#### Code Blocks

Always specify the language for syntax highlighting:

\`\`\`bash
curl https://api.kitchntabs.com/api/orders
\`\`\`

\`\`\`php
public function index()
{
    return response()->json(['status' => 'ok']);
}
\`\`\`

\`\`\`typescript
const handleClick = () => {
    console.log('clicked');
};
\`\`\`

#### Links

- Use relative links for internal documentation: `[See Architecture](../architecture/ARCHITECTURE.html)`
- Use full URLs for external links: `[Laravel Docs](https://laravel.com/docs)`

#### Tables

Always use tables for structured data:

```markdown
| Column 1 | Column 2 | Column 3 |
|----------|----------|----------|
| Value 1  | Value 2  | Value 3  |
```

#### Images

```markdown
![Alt Text](../assets/image-name.png)
```

### API References

When documenting API endpoints, use this format:

```markdown
### Endpoint Name

**Method**: `POST`  
**URL**: `https://api.kitchntabs.com/api/endpoint`  
**Auth**: Required

#### Request Body

\`\`\`json
{
    "field1": "value1",
    "field2": "value2"
}
\`\`\`

#### Response

\`\`\`json
{
    "status": "success",
    "data": {}
}
\`\`\`
```

### Security Guidelines

**❌ Never include:**
- API keys
- Passwords
- Private tokens
- Production credentials
- Personal information

**✅ Use instead:**
- Placeholders: `YOUR_API_KEY`
- Example values: `example@email.com`
- Redacted values: `***REDACTED***`

### Domain References

Always use the production API domain:

```
https://api.kitchntabs.com
```

❌ Don't use:
- `localhost`
- `127.0.0.1`
- `ngrok` domains
- `example.com` (except in general examples)

---

## 📤 Submitting Changes

### Workflow

1. **Fork the Repository**
   ```bash
   git fork https://github.com/kitchntabs/kitchntabs.github.io.git
   ```

2. **Create a Branch**
   ```bash
   git checkout -b feature/update-documentation
   ```

3. **Make Changes**
   - Edit/create documentation files
   - Follow style guide
   - Test locally

4. **Commit Changes**
   ```bash
   git add .
   git commit -m "docs: update mall app architecture"
   ```

5. **Push to Fork**
   ```bash
   git push origin feature/update-documentation
   ```

6. **Create Pull Request**
   - Go to GitHub
   - Create PR from your fork
   - Fill in PR template

### Commit Message Format

Use conventional commits:

```
docs: add new section on authentication
fix: correct API endpoint in examples
style: improve code block formatting
refactor: reorganize architecture documentation
```

### Pull Request Template

```markdown
## Description
Brief description of changes

## Type of Change
- [ ] New documentation
- [ ] Update existing docs
- [ ] Fix typo/error
- [ ] Improve formatting
- [ ] Add examples

## Checklist
- [ ] Followed style guide
- [ ] No sensitive data included
- [ ] Links work correctly
- [ ] Images display properly
- [ ] Tested locally
- [ ] Updated sitemap if needed
```

---

## 🔍 Review Process

### What We Look For

✅ **Content Quality**
- Accurate information
- Clear explanations
- Proper examples
- No sensitive data

✅ **Formatting**
- Consistent style
- Proper Markdown
- Working links
- Appropriate code blocks

✅ **Structure**
- Logical organization
- Proper headers
- Front matter included
- Navigation clarity

### Review Timeline

- Initial review: 1-3 business days
- Feedback provided via PR comments
- Updates requested if needed
- Merge upon approval

---

## 📚 Additional Resources

- [Markdown Guide](https://www.markdownguide.org/)
- [Jekyll Documentation](https://jekyllrb.com/docs/)
- [GitHub Pages Guide](https://docs.github.com/en/pages)
- [KitchnTabs Sitemap](SITEMAP.md)

---

## 💬 Questions?

If you have questions about contributing:

1. Check existing documentation
2. Review closed pull requests for examples
3. Open an issue with your question
4. Contact the documentation team

---

## 📄 License

By contributing to KitchnTabs documentation, you agree that your contributions will be licensed under the same terms as the project.

---

<p align="center">
  <strong>Thank you for contributing! 🎉</strong><br>
  Your contributions help make KitchnTabs documentation better for everyone.
</p>
