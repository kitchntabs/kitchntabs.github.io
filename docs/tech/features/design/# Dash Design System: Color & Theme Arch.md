# Dash Design System: Color & Theme Architecture

## Overview

The Dash Design System uses a flexible, scalable approach to theming and color management, supporting both **light** and **dark** modes, as well as domain-specific overrides. This system is built on top of [LESS](https://lesscss.org/) and CSS custom properties (variables), making it easy to maintain, extend, and override at any level.

---

## 1. **Color Variable Structure**

All color variables are defined in LESS files and mapped to CSS custom properties. Each color variable can have:

- **Default (light) value:**  
  `@primary-color`
- **Dark mode value:**  
  `@primary-color--dark`

**Example:**
```less
@primary-color: #8f00cb;           // Light mode
@primary-color--dark: #8f00cb;     // Dark mode
```

---

## 2. **File Organization**

- **Core Variables:**  
  - dash-colors-light.less – Default (light) theme colors  
  - dash-colors-dark.less – Dark theme colors  
  - dash-variables.less – Imports all color, size, and breakpoint variables

- **Domain Overrides:**  
  - dash-variables.less – Project/domain-specific overrides for any variable

- **CSS Variable Mapping:**  
  - dash-css-transformer.less – Maps LESS variables to CSS custom properties for both light and dark modes

---

## 3. **CSS Custom Properties Output**

All LESS variables are mapped to CSS custom properties in `:root` by dash-css-transformer.less:

```less
:root {
  --primary-color--light: @primary-color;
  --primary-color--dark: @primary-color--dark;
  // ...etc
}
```

This allows runtime switching and easy overrides via CSS.

---

## 4. **Theme Switching**

- **Light mode** uses variables with the `--light` suffix (or default if not present).
- **Dark mode** uses variables with the `--dark` suffix.
- The system can switch themes by toggling a class or attribute and updating the relevant CSS variables.

---

## 5. **Domain/Project Overrides**

To customize the theme for a specific project:

1. **Create or edit** dash-variables.less.
2. **Override** any variable (with or without `--dark` suffix).
3. The build process ensures your overrides take precedence.

**Example:**
```less
@primary-color: #ff0000;           // Custom light mode
@primary-color--dark: #00ff00;     // Custom dark mode
```

---

## 6. **Build & Import Order**

- The main Vite config imports:
  1. Core variables
  2. Domain overrides
  3. CSS variable mapping

This ensures domain overrides always win.

---

## 7. **Best Practices**

- **Always use `--light` and `--dark` suffixes** for mode-specific variables.
- **Do not assign both modes to the same variable** (e.g., avoid `@primary-color: @primary-color--dark;`).
- **Use domain overrides** for project-specific branding or color tweaks.

---

## 8. **Extending the System**

- Add new variables in the core files.
- Map them in dash-css-transformer.less.
- Override as needed in your domain file.

---

## 9. **Troubleshooting**

- If both light and dark variables appear the same in the DOM, check:
  - Your domain override file for duplicate assignments.
  - The order of imports in your build config.
  - That you are mapping the correct LESS variables to CSS custom properties.

---

## 10. **Example: Adding a New Color**

1. Add to dash-colors-light.less and dash-colors-dark.less:
   ```less
   @brand-accent: #123456;
   @brand-accent--dark: #abcdef;
   ```
2. Map in dash-css-transformer.less:
   ```less
   --brand-accent--light: @brand-accent;
   --brand-accent--dark: @brand-accent--dark;
   ```
3. (Optional) Override in your domain file.

---

## 11. **Summary**

- **Separation of concerns:** Core, domain, and mapping layers.
- **Easy overrides:** Domain files always win.
- **Scalable:** Add new variables and themes as needed.
- **Consistent:** All colors available as CSS custom properties for runtime use.

---

**For further customization or troubleshooting, consult the comments in each LESS file or reach out to the Dash Design System maintainers.**