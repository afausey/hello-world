# ADV OU Knowledge Base - UI/UX Design Specification
**Version 1.0** | Created: February 2, 2026

This document provides comprehensive design specifications for redesigning the ADV OU Knowledge Base web application. All specifications are implementation-ready for Claude Code.

---

## Table of Contents
1. [Design Philosophy](#design-philosophy)
2. [Project File Structure](#project-file-structure)
3. [Color System](#color-system)
4. [Typography](#typography)
5. [Spacing System](#spacing-system)
6. [Component Specifications](#component-specifications)
7. [Layout Specifications](#layout-specifications)
8. [Sprite Integration](#sprite-integration)
9. [Animation Guidelines](#animation-guidelines)
10. [Responsive Behavior](#responsive-behavior)
11. [Implementation Phases](#implementation-phases)
12. [Code Examples](#code-examples)

---

## Design Philosophy

### Core Principles
1. **Competitive Toolkit, Not Wiki** - This feels like a professional tool for competitive analysis, not a documentation site
2. **Data-First Typography** - Monospace for technical data (stats, EVs, calcs), readable sans for explanations
3. **Minimal but Polished** - Subtle animations, clean interactions, no unnecessary flourish
4. **Mobile-First** - Designed for on-the-go theorycrafting and quick reference
5. **Gen 3 Identity** - Color palette inspired by Ruby/Sapphire/Emerald, not generic

### Differentiation from Smogon
- **Color Scheme**: Navy + Sapphire/Emerald accents (NOT Smogon's purple/orange)
- **Typography**: Monospace hybrid approach (NOT all-Roboto)
- **Layout**: Card-based with breathing room (NOT dense tables)
- **Navigation**: Top tabs, mobile-first (NOT sidebar)
- **Aesthetic**: Modern dark competitive tool (NOT wiki database)

---

## Project File Structure

```
~/adv-ou-project/
├── index.html                 # Main HTML file (single-page app)
├── css/
│   ├── reset.css              # CSS reset/normalize
│   ├── variables.css          # CSS custom properties (colors, spacing, etc.)
│   ├── typography.css         # Font imports and text styles
│   ├── components.css         # Reusable components (buttons, cards, etc.)
│   ├── layout.css             # Grid systems, sections, navigation
│   └── utilities.css          # Helper classes (text-center, mb-4, etc.)
├── js/
│   ├── main.js                # Tab switching, navigation logic
│   ├── tooltip.js             # Pokepaste tooltips for team cards
│   └── sprites.js             # Sprite loading/fallback logic
├── data/
│   ├── pokemon.json           # Pokemon data (names, types, sprites)
│   ├── metagame.json          # Metagame overview content
│   ├── archetypes.json        # Team archetype descriptions
│   ├── cores.json             # 2-Pokemon cores data
│   ├── sample_teams.json      # Full sample teams with pokepastes
│   ├── speed_tiers.json       # Speed benchmark data
│   └── calculator_data.json   # Damage calculator base stats/formulas
├── assets/
│   ├── sprites/               # Pokemon sprites (Gen 3)
│   │   ├── tyranitar.png
│   │   ├── salamence.png
│   │   └── ...
│   └── icons/                 # UI icons (if needed)
├── fonts/                     # Self-hosted fonts (optional)
│   ├── JetBrainsMono/
│   └── Inter/
├── README.md                  # Project documentation
└── design-spec.md             # This file (for reference)
```

### Build Approach
**Keep it simple** - No build step required initially:
- Vanilla HTML/CSS/JS
- No bundlers, no transpilers
- Could add Vite/Parcel later for optimization, but not required for v1

---

## Color System

### Base Palette

#### Background Layers
```css
--color-bg-primary: #0a1929;      /* Main background - deep navy */
--color-bg-surface: #1e2936;      /* Cards, elevated elements */
--color-bg-surface-hover: #253645; /* Hover state for interactive surfaces */
--color-border: #2d3748;          /* Subtle borders, dividers */
--color-border-hover: #3d4f5f;    /* Hover state borders */
```

#### Brand/Accent Colors
```css
--color-sapphire: #457b9d;        /* PRIMARY - buttons, active states, highlights */
--color-emerald: #2a9d8f;         /* Success, positive, balanced archetypes */
--color-electric: #ffb703;        /* Speed indicators, warnings, attention */
--color-ruby: #e63946;            /* CONTEXTUAL ONLY - damage, super effective, negative */
```

#### Text Colors
```css
--color-text-primary: #e2e8f0;    /* High contrast, main content */
--color-text-secondary: #94a3b8;  /* Muted, less important content */
--color-text-tertiary: #64748b;   /* Very muted, metadata */
--color-link: #60a5fa;            /* Links, clickable text */
--color-link-hover: #93c5fd;      /* Link hover state */
```

#### Pokemon Type Colors (for badges)
Use standard Pokemon type colors but desaturated 20% for dark theme compatibility:
```css
--type-normal: #a8a878;
--type-fire: #f08030;
--type-water: #6890f0;
--type-electric: #f8d030;
--type-grass: #78c850;
--type-ice: #98d8d8;
--type-fighting: #c03028;
--type-poison: #a040a0;
--type-ground: #e0c068;
--type-flying: #a890f0;
--type-psychic: #f85888;
--type-bug: #a8b820;
--type-rock: #b8a038;
--type-ghost: #705898;
--type-dragon: #7038f8;
--type-dark: #705848;
--type-steel: #b8b8d0;
```

### Color Usage Rules

#### Ruby Red - RESTRICTED USE ONLY
**ONLY use Ruby Red for:**
- Super effective damage indicators
- KO notifications
- "Weak to" labels in Pokemon/core descriptions
- Critical warnings
- Negative connotations

**NEVER use Ruby Red for:**
- UI buttons or primary actions
- Archetype labels (even "offense")
- Headers or section titles
- General highlighting

#### Sapphire Blue - Primary Brand Color
**Use Sapphire for:**
- Primary buttons
- Active tab indicators
- Selected states
- Links and interactive elements
- "Defensive" archetype labels
- Main brand accents

#### Emerald Green - Success/Positive
**Use Emerald for:**
- Success states (damage calc results that KO)
- "Balanced" archetype labels
- Positive indicators
- Confirmation messages
- Growth/progress indicators

#### Electric Yellow - Attention/Speed
**Use Electric for:**
- Speed tier numbers (the actual speed stat)
- "Fast" or "Hyper Offense" archetype labels
- Warning states (not errors)
- Highlight/focus states
- Call-to-action secondary buttons

### Color Combinations
```css
/* Safe combinations with good contrast */
Sapphire on Surface:  #457b9d on #1e2936  ✓
Emerald on Surface:   #2a9d8f on #1e2936  ✓
Electric on Surface:  #ffb703 on #1e2936  ✓
Ruby on Surface:      #e63946 on #1e2936  ✓

/* Text on backgrounds */
Primary text on BG:   #e2e8f0 on #0a1929  ✓ (WCAG AAA)
Secondary on BG:      #94a3b8 on #0a1929  ✓ (WCAG AA)
```

---

## Typography

### Font Stack

#### Primary Fonts
```css
--font-mono: 'JetBrains Mono', 'Fira Code', 'Courier New', monospace;
--font-sans: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
```

#### Font Imports (Google Fonts)
```html
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&family=JetBrains+Mono:wght@400;500;600;700&display=swap" rel="stylesheet">
```

### Typography Scale

#### Headings (JetBrains Mono)
```css
--text-h1: 2.5rem;      /* 40px - Main page titles */
--text-h2: 2rem;        /* 32px - Section headers */
--text-h3: 1.5rem;      /* 24px - Subsection headers */
--text-h4: 1.25rem;     /* 20px - Card titles */
--text-h5: 1.125rem;    /* 18px - Small headers */

/* Line heights for headings */
--line-height-heading: 1.2;

/* Example heading styles */
h1, h2, h3, h4, h5 {
  font-family: var(--font-mono);
  font-weight: 600;
  line-height: var(--line-height-heading);
  color: var(--color-text-primary);
  letter-spacing: -0.02em;
}
```

#### Body Text (Inter)
```css
--text-base: 1rem;      /* 16px - Standard body */
--text-sm: 0.875rem;    /* 14px - Small text */
--text-xs: 0.75rem;     /* 12px - Tiny text (metadata) */
--text-lg: 1.125rem;    /* 18px - Large body text */

/* Line heights for body */
--line-height-body: 1.6;
--line-height-tight: 1.4;

/* Example body styles */
p, li, td, .body-text {
  font-family: var(--font-sans);
  font-weight: 400;
  line-height: var(--line-height-body);
  color: var(--color-text-primary);
}
```

#### Technical Text (JetBrains Mono)
```css
/* Pokemon names, stats, EVs, speed numbers, calculations */
.pokemon-name,
.stat-value,
.speed-number,
.ev-spread,
.damage-calc {
  font-family: var(--font-mono);
  font-weight: 500;
  letter-spacing: -0.01em;
}

/* Example: Speed tier display */
.speed-number {
  font-size: var(--text-lg);
  color: var(--color-electric);
  font-variant-numeric: tabular-nums; /* Monospace numbers */
}
```

### Typography Usage Rules

#### Use JetBrains Mono for:
- All headings (h1-h5)
- Pokemon names
- Move names
- Ability names
- Item names
- EV/IV spreads (e.g., "252 HP / 168 Atk / 88 Spe")
- Speed numbers (e.g., "406", "328")
- Damage calculations
- Any numerical data

#### Use Inter for:
- Body text / paragraphs
- Descriptions
- Team strategy explanations
- List item descriptions
- Button labels (when text, not numbers)
- Navigation labels
- Helper text / tooltips

### Font Weights
```css
--font-weight-normal: 400;
--font-weight-medium: 500;
--font-weight-semibold: 600;
--font-weight-bold: 700;

/* Usage */
Headings:        600 (semibold)
Pokemon names:   500 (medium)
Body text:       400 (normal)
Button labels:   500 (medium)
Stats/numbers:   500 (medium)
```

---

## Spacing System

### Base Unit
```css
--space-unit: 0.25rem; /* 4px base unit */
```

### Spacing Scale
```css
--space-1: calc(var(--space-unit) * 1);   /* 4px */
--space-2: calc(var(--space-unit) * 2);   /* 8px */
--space-3: calc(var(--space-unit) * 3);   /* 12px */
--space-4: calc(var(--space-unit) * 4);   /* 16px */
--space-5: calc(var(--space-unit) * 5);   /* 20px */
--space-6: calc(var(--space-unit) * 6);   /* 24px */
--space-8: calc(var(--space-unit) * 8);   /* 32px */
--space-10: calc(var(--space-unit) * 10); /* 40px */
--space-12: calc(var(--space-unit) * 12); /* 48px */
--space-16: calc(var(--space-unit) * 16); /* 64px */
--space-20: calc(var(--space-unit) * 20); /* 80px */
```

### Common Spacing Patterns
```css
/* Component padding */
--padding-card: var(--space-6);           /* 24px inside cards */
--padding-button: var(--space-3) var(--space-5); /* 12px vertical, 20px horizontal */
--padding-section: var(--space-8);        /* 32px section padding */

/* Component gaps */
--gap-list: var(--space-3);               /* 12px between list items */
--gap-grid: var(--space-4);               /* 16px between grid items */
--gap-inline: var(--space-2);             /* 8px between inline elements (sprite + name) */

/* Margins */
--margin-heading: var(--space-6);         /* 24px below headings */
--margin-section: var(--space-10);        /* 40px between major sections */
```

### Utility Classes (Create These)
```css
/* Margin utilities */
.m-0 { margin: 0; }
.m-1 { margin: var(--space-1); }
.m-2 { margin: var(--space-2); }
/* ... up to m-20 */

.mt-4 { margin-top: var(--space-4); }
.mb-4 { margin-bottom: var(--space-4); }
/* ... all directional spacing utilities */

/* Padding utilities */
.p-4 { padding: var(--space-4); }
.px-6 { padding-left: var(--space-6); padding-right: var(--space-6); }
.py-4 { padding-top: var(--space-4); padding-bottom: var(--space-4); }

/* Gap utilities */
.gap-2 { gap: var(--space-2); }
.gap-4 { gap: var(--space-4); }
```

---

## Component Specifications

### 1. Navigation Tabs

#### Desktop Design
```
┌────────────────────────────────────────────────────────────────┐
│  Pokemon    Metagame    Archetypes    Cores    Sample Teams    │
│  ────────                                                       │  ← Active indicator
└────────────────────────────────────────────────────────────────┘
```

#### Specifications
```css
.nav-tabs {
  display: flex;
  gap: var(--space-6); /* 24px between tabs */
  padding: var(--space-4) var(--space-6); /* 16px vertical, 24px horizontal */
  background: var(--color-bg-surface);
  border-bottom: 1px solid var(--color-border);
  position: sticky;
  top: 0;
  z-index: 100;
}

.nav-tab {
  font-family: var(--font-mono);
  font-size: var(--text-base);
  font-weight: 500;
  color: var(--color-text-secondary);
  padding: var(--space-3) 0;
  border-bottom: 3px solid transparent;
  cursor: pointer;
  transition: color 200ms ease, border-color 200ms ease;
  text-decoration: none;
}

.nav-tab:hover {
  color: var(--color-text-primary);
}

.nav-tab.active {
  color: var(--color-sapphire);
  border-bottom-color: var(--color-sapphire);
}
```

#### Mobile Design (horizontal scroll)
```css
@media (max-width: 768px) {
  .nav-tabs {
    overflow-x: auto;
    scrollbar-width: none; /* Hide scrollbar */
    -ms-overflow-style: none;
    padding: var(--space-3) var(--space-4);
  }
  
  .nav-tabs::-webkit-scrollbar {
    display: none;
  }
  
  .nav-tab {
    white-space: nowrap;
    font-size: var(--text-sm);
  }
}
```

---

### 2. Cards

#### Base Card Component
```css
.card {
  background: var(--color-bg-surface);
  border: 1px solid var(--color-border);
  border-radius: 8px;
  padding: var(--padding-card); /* 24px */
  transition: border-color 200ms ease, box-shadow 200ms ease;
}

.card:hover {
  border-color: var(--color-border-hover);
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
}

.card-title {
  font-family: var(--font-mono);
  font-size: var(--text-h4); /* 20px */
  font-weight: 600;
  color: var(--color-text-primary);
  margin-bottom: var(--space-4);
}

.card-body {
  font-family: var(--font-sans);
  font-size: var(--text-base);
  color: var(--color-text-primary);
  line-height: var(--line-height-body);
}
```

#### Team Card (Sample Teams Section)
```css
.team-card {
  background: var(--color-bg-surface);
  border: 1px solid var(--color-border);
  border-radius: 8px;
  padding: var(--space-6);
  cursor: pointer;
  transition: all 200ms ease;
  position: relative;
}

.team-card:hover {
  border-color: var(--color-sapphire);
  box-shadow: 0 6px 16px rgba(69, 123, 157, 0.2); /* Sapphire glow */
  transform: translateY(-2px);
}

.team-card-header {
  margin-bottom: var(--space-4);
}

.team-card-title {
  font-family: var(--font-mono);
  font-size: var(--text-h4);
  font-weight: 600;
  color: var(--color-text-primary);
  margin-bottom: var(--space-2);
}

.team-card-meta {
  font-family: var(--font-sans);
  font-size: var(--text-sm);
  color: var(--color-text-secondary);
  display: flex;
  gap: var(--space-3);
  align-items: center;
}

.team-card-sprites {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: var(--space-3);
  margin: var(--space-4) 0;
}

.team-card-sprite {
  width: 48px;
  height: 48px;
  display: flex;
  align-items: center;
  justify-content: center;
  background: var(--color-bg-primary);
  border-radius: 4px;
}

.team-card-sprite img {
  max-width: 100%;
  max-height: 100%;
  image-rendering: pixelated; /* Crisp pixel art */
}
```

#### Archetype Badge
```css
.archetype-badge {
  display: inline-block;
  font-family: var(--font-mono);
  font-size: var(--text-xs);
  font-weight: 600;
  text-transform: uppercase;
  letter-spacing: 0.05em;
  padding: var(--space-1) var(--space-3);
  border-radius: 4px;
  background: var(--color-bg-primary);
}

/* Variant colors */
.archetype-badge.defensive {
  color: var(--color-sapphire);
  border: 1px solid var(--color-sapphire);
}

.archetype-badge.offensive {
  color: var(--color-electric);
  border: 1px solid var(--color-electric);
}

.archetype-badge.balanced {
  color: var(--color-emerald);
  border: 1px solid var(--color-emerald);
}

.archetype-badge.beginner {
  color: var(--color-emerald);
  border: 1px solid var(--color-emerald);
}
```

---

### 3. Lists with Inline Sprites

#### Pokemon List Item
```css
.pokemon-list {
  display: flex;
  flex-direction: column;
  gap: var(--gap-list); /* 12px between items */
}

.pokemon-list-item {
  display: flex;
  align-items: center;
  gap: var(--gap-inline); /* 8px between sprite and text */
  padding: var(--space-3) var(--space-4);
  background: var(--color-bg-surface);
  border: 1px solid var(--color-border);
  border-radius: 6px;
  transition: border-color 200ms ease;
  cursor: pointer;
}

.pokemon-list-item:hover {
  border-color: var(--color-sapphire);
}

.pokemon-sprite-inline {
  width: 32px;
  height: 32px;
  flex-shrink: 0;
  image-rendering: pixelated;
}

.pokemon-info {
  flex: 1;
}

.pokemon-name {
  font-family: var(--font-mono);
  font-size: var(--text-base);
  font-weight: 500;
  color: var(--color-text-primary);
  margin-bottom: var(--space-1);
}

.pokemon-types {
  font-family: var(--font-sans);
  font-size: var(--text-sm);
  color: var(--color-text-secondary);
}

.pokemon-stat {
  font-family: var(--font-mono);
  font-size: var(--text-base);
  font-weight: 500;
  color: var(--color-text-primary);
  margin-left: auto; /* Push to right */
}
```

#### Speed Tier Item
```css
.speed-tier-item {
  display: flex;
  align-items: center;
  gap: var(--space-3);
  padding: var(--space-3) var(--space-4);
  background: var(--color-bg-surface);
  border-left: 3px solid var(--color-electric); /* Yellow accent */
  margin-bottom: var(--space-2);
}

.speed-tier-sprite {
  width: 32px;
  height: 32px;
  flex-shrink: 0;
  image-rendering: pixelated;
}

.speed-tier-pokemon {
  font-family: var(--font-mono);
  font-size: var(--text-base);
  font-weight: 500;
  color: var(--color-text-primary);
  min-width: 120px;
}

.speed-tier-details {
  font-family: var(--font-sans);
  font-size: var(--text-sm);
  color: var(--color-text-secondary);
  flex: 1;
}

.speed-tier-number {
  font-family: var(--font-mono);
  font-size: var(--text-lg);
  font-weight: 600;
  color: var(--color-electric);
  margin-left: auto;
}
```

---

### 4. Core Display (Two Pokemon Side-by-Side)

```css
.core-card {
  background: var(--color-bg-surface);
  border: 1px solid var(--color-border);
  border-radius: 8px;
  padding: var(--space-6);
  margin-bottom: var(--space-4);
}

.core-header {
  display: flex;
  align-items: center;
  gap: var(--space-4);
  margin-bottom: var(--space-4);
}

.core-pokemon-pair {
  display: flex;
  align-items: center;
  gap: var(--space-3);
}

.core-sprite {
  width: 48px;
  height: 48px;
  image-rendering: pixelated;
}

.core-plus {
  font-family: var(--font-mono);
  font-size: var(--text-h3);
  color: var(--color-text-secondary);
  font-weight: 300;
}

.core-badge {
  /* Use archetype-badge styles from above */
}

.core-description {
  font-family: var(--font-sans);
  font-size: var(--text-base);
  color: var(--color-text-primary);
  line-height: var(--line-height-body);
  margin-bottom: var(--space-4);
}

.core-weaknesses {
  font-family: var(--font-sans);
  font-size: var(--text-sm);
  color: var(--color-text-secondary);
}

.core-weaknesses strong {
  color: var(--color-ruby); /* Red for "Weaknesses:" label only */
  font-weight: 600;
}
```

---

### 5. Buttons

#### Primary Button
```css
.btn {
  font-family: var(--font-sans);
  font-size: var(--text-base);
  font-weight: 500;
  padding: var(--padding-button); /* 12px 20px */
  border-radius: 6px;
  border: none;
  cursor: pointer;
  transition: all 200ms ease;
  text-decoration: none;
  display: inline-block;
  text-align: center;
}

.btn-primary {
  background: var(--color-sapphire);
  color: white;
}

.btn-primary:hover {
  background: #5a8fb0; /* Lighter sapphire */
  box-shadow: 0 4px 8px rgba(69, 123, 157, 0.3);
}

.btn-secondary {
  background: var(--color-bg-surface);
  color: var(--color-text-primary);
  border: 1px solid var(--color-border);
}

.btn-secondary:hover {
  border-color: var(--color-sapphire);
  color: var(--color-sapphire);
}

.btn-success {
  background: var(--color-emerald);
  color: white;
}

.btn-warning {
  background: var(--color-electric);
  color: var(--color-bg-primary); /* Dark text on yellow */
}
```

---

### 6. Type Badges

```css
.type-badge {
  display: inline-block;
  font-family: var(--font-mono);
  font-size: var(--text-xs);
  font-weight: 600;
  text-transform: uppercase;
  padding: var(--space-1) var(--space-2);
  border-radius: 3px;
  color: white;
  text-shadow: 0 1px 2px rgba(0, 0, 0, 0.3); /* Readability */
}

/* Type-specific colors */
.type-fire { background: var(--type-fire); }
.type-water { background: var(--type-water); }
.type-grass { background: var(--type-grass); }
.type-electric { background: var(--type-electric); }
.type-rock { background: var(--type-rock); }
.type-ground { background: var(--type-ground); }
.type-dragon { background: var(--type-dragon); }
.type-dark { background: var(--type-dark); }
.type-steel { background: var(--type-steel); }
.type-psychic { background: var(--type-psychic); }
.type-ghost { background: var(--type-ghost); }
.type-flying { background: var(--type-flying); }
.type-normal { background: var(--type-normal); }
.type-fighting { background: var(--type-fighting); }
.type-poison { background: var(--type-poison); }
.type-bug { background: var(--type-bug); }
.type-ice { background: var(--type-ice); }
```

---

### 7. Tooltip (for Pokepaste on Team Cards)

```css
.tooltip {
  position: absolute;
  background: var(--color-bg-primary);
  border: 1px solid var(--color-sapphire);
  border-radius: 6px;
  padding: var(--space-4);
  box-shadow: 0 8px 24px rgba(0, 0, 0, 0.4);
  z-index: 1000;
  max-width: 300px;
  opacity: 0;
  pointer-events: none;
  transition: opacity 150ms ease;
}

.tooltip.active {
  opacity: 1;
  pointer-events: auto;
}

.tooltip-title {
  font-family: var(--font-mono);
  font-size: var(--text-sm);
  font-weight: 600;
  color: var(--color-text-primary);
  margin-bottom: var(--space-2);
}

.tooltip-link {
  font-family: var(--font-sans);
  font-size: var(--text-sm);
  color: var(--color-link);
  text-decoration: none;
  display: inline-flex;
  align-items: center;
  gap: var(--space-2);
}

.tooltip-link:hover {
  color: var(--color-link-hover);
  text-decoration: underline;
}
```

---

### 8. Section Headers

```css
.section {
  margin-bottom: var(--margin-section); /* 40px */
}

.section-header {
  font-family: var(--font-mono);
  font-size: var(--text-h2); /* 32px */
  font-weight: 600;
  color: var(--color-text-primary);
  margin-bottom: var(--space-6); /* 24px */
  padding-bottom: var(--space-3);
  border-bottom: 2px solid var(--color-border);
}

.section-subheader {
  font-family: var(--font-mono);
  font-size: var(--text-h3); /* 24px */
  font-weight: 600;
  color: var(--color-text-primary);
  margin-top: var(--space-8);
  margin-bottom: var(--space-4);
}
```

---

## Layout Specifications

### Page Structure
```html
<body>
  <!-- Sticky Navigation -->
  <nav class="nav-tabs">
    <a class="nav-tab active" data-tab="pokemon">Pokemon</a>
    <a class="nav-tab" data-tab="metagame">Metagame</a>
    <!-- ... more tabs -->
  </nav>

  <!-- Main Content Area -->
  <main class="main-content">
    <div class="container">
      <!-- Tab content goes here -->
      <div class="tab-pane active" id="pokemon-tab">
        <!-- Pokemon content -->
      </div>
      <!-- ... more tab panes -->
    </div>
  </main>
</body>
```

### Container & Grid
```css
.main-content {
  background: var(--color-bg-primary);
  min-height: calc(100vh - 60px); /* Full height minus nav */
}

.container {
  max-width: 1200px;
  margin: 0 auto;
  padding: var(--space-8) var(--space-6);
}

@media (max-width: 768px) {
  .container {
    padding: var(--space-6) var(--space-4);
  }
}

/* Grid for team cards */
.team-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(320px, 1fr));
  gap: var(--space-6);
}

@media (max-width: 640px) {
  .team-grid {
    grid-template-columns: 1fr;
  }
}
```

### Tab Panes
```css
.tab-pane {
  display: none;
}

.tab-pane.active {
  display: block;
  animation: fadeIn 200ms ease;
}

@keyframes fadeIn {
  from { opacity: 0; }
  to { opacity: 1; }
}
```

---

## Sprite Integration

### Sprite Sources
1. **Primary**: PokéAPI - https://pokeapi.co/api/v2/pokemon/{id}
   - Sprites at: `data.sprites.versions['generation-iii']['emerald'].front_default`
2. **Fallback**: Smogon sprite repo (if needed)
3. **Local Cache**: Store in `/assets/sprites/` for offline access

### Sprite Sizes
- **Inline (lists, speed tiers)**: 32x32px
- **Team cards**: 48x48px
- **Pokemon detail pages**: 64x64px (if implemented)

### Sprite Implementation
```html
<!-- Inline sprite example -->
<div class="pokemon-list-item">
  <img 
    src="assets/sprites/tyranitar.png" 
    alt="Tyranitar"
    class="pokemon-sprite-inline"
    loading="lazy"
    onerror="this.src='assets/sprites/fallback.png'"
  >
  <div class="pokemon-info">
    <div class="pokemon-name">Tyranitar</div>
    <div class="pokemon-types">Rock / Dark</div>
  </div>
  <div class="pokemon-stat">221</div>
</div>
```

### Sprite Loading Strategy
```javascript
// sprites.js - Basic fallback handler
document.addEventListener('DOMContentLoaded', () => {
  const sprites = document.querySelectorAll('img[data-pokemon]');
  
  sprites.forEach(sprite => {
    sprite.addEventListener('error', function() {
      // Fallback to Pokemon name text if sprite fails
      this.style.display = 'none';
      const fallbackText = document.createElement('span');
      fallbackText.textContent = this.alt.charAt(0); // First letter
      fallbackText.className = 'sprite-fallback';
      this.parentNode.insertBefore(fallbackText, this);
    });
  });
});
```

```css
.sprite-fallback {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  width: 32px;
  height: 32px;
  background: var(--color-bg-primary);
  border: 1px solid var(--color-border);
  border-radius: 4px;
  font-family: var(--font-mono);
  font-weight: 600;
  color: var(--color-text-secondary);
}
```

### Image Rendering
```css
/* Ensure pixel art stays crisp */
img {
  image-rendering: pixelated;
  image-rendering: -moz-crisp-edges;
  image-rendering: crisp-edges;
}
```

---

## Animation Guidelines

### Principle: Minimal but Polished
- **Duration**: 150-200ms for most transitions
- **Easing**: `ease` or `ease-in-out` (no bounce/elastic)
- **What to animate**: Colors, borders, opacity, small transforms
- **What NOT to animate**: Layout shifts, sprites, text content

### Allowed Animations

#### 1. Tab Switching
```css
.tab-pane {
  animation: fadeIn 200ms ease;
}

@keyframes fadeIn {
  from {
    opacity: 0;
  }
  to {
    opacity: 1;
  }
}
```

#### 2. Hover States
```css
.card,
.pokemon-list-item,
.team-card {
  transition: border-color 200ms ease, box-shadow 200ms ease;
}

.team-card:hover {
  transform: translateY(-2px);
  transition: all 200ms ease;
}
```

#### 3. Tooltip Appearance
```css
.tooltip {
  opacity: 0;
  transition: opacity 150ms ease;
}

.tooltip.active {
  opacity: 1;
}
```

### Disallowed Animations
- ❌ Sprite animations (keep static)
- ❌ Slide-in from side (too dramatic)
- ❌ Bounce/spring effects
- ❌ Rotating elements
- ❌ Scale transforms > 1.05x
- ❌ Parallax scrolling effects

### Performance
```css
/* Use transform and opacity for GPU acceleration */
.card:hover {
  transform: translateY(-2px); /* GPU accelerated ✓ */
  /* Instead of: margin-top: -2px; ✗ */
}

/* Will-change for frequently animated elements */
.nav-tab.active {
  will-change: border-color;
}
```

---

## Responsive Behavior

### Breakpoints
```css
/* Mobile first approach */
:root {
  --breakpoint-sm: 640px;   /* Small tablets */
  --breakpoint-md: 768px;   /* Tablets */
  --breakpoint-lg: 1024px;  /* Laptops */
  --breakpoint-xl: 1280px;  /* Desktops */
}
```

### Mobile (<640px)
- Navigation tabs scroll horizontally
- Single column layout for all grids
- Reduced padding (16px instead of 24px)
- Smaller font sizes for headings
- Sprites remain same size (32px inline, 48px cards)
- Touch targets minimum 44x44px

```css
@media (max-width: 640px) {
  .nav-tabs {
    overflow-x: auto;
    padding: var(--space-3) var(--space-4);
  }
  
  .container {
    padding: var(--space-6) var(--space-4);
  }
  
  .section-header {
    font-size: var(--text-h3); /* Smaller on mobile */
  }
  
  .team-grid {
    grid-template-columns: 1fr; /* Single column */
  }
  
  /* Ensure touch targets are large enough */
  .nav-tab,
  .btn,
  .pokemon-list-item {
    min-height: 44px;
  }
}
```

### Tablet (640px - 1024px)
- Two-column grid for team cards
- Full navigation visible
- Standard padding

```css
@media (min-width: 640px) and (max-width: 1024px) {
  .team-grid {
    grid-template-columns: repeat(2, 1fr);
  }
}
```

### Desktop (>1024px)
- Three-column grid for team cards
- Maximum container width of 1200px
- Hover states fully active

```css
@media (min-width: 1024px) {
  .team-grid {
    grid-template-columns: repeat(3, 1fr);
  }
  
  /* Only show hover effects on devices that support hover */
  @media (hover: hover) {
    .card:hover {
      box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
    }
  }
}
```

---

## Implementation Phases

### Phase 1: Foundation (Do This First)
**Goal**: Set up architecture and base styles

1. **File Structure**
   - Create folder structure as specified
   - Set up index.html with semantic HTML
   - Create all CSS files (variables.css, typography.css, etc.)

2. **CSS Variables**
   - Implement complete color system
   - Set up spacing scale
   - Define typography scale
   - Import fonts (Google Fonts)

3. **Base Styles**
   - CSS reset
   - Global body/html styles
   - Typography base styles
   - Utility classes

**Deliverable**: Working HTML with proper structure, all colors/fonts defined

---

### Phase 2: Components (Do This Second)
**Goal**: Build reusable components

1. **Navigation**
   - Tab component with active state
   - Sticky positioning
   - Tab switching JavaScript

2. **Cards**
   - Base card component
   - Team card variant
   - Core card variant

3. **Lists**
   - Pokemon list with inline sprites
   - Speed tier list
   - Type badges

4. **Buttons**
   - Primary, secondary, success variants
   - Hover states

**Deliverable**: All components working in isolation (can test with dummy content)

---

### Phase 3: Content Integration (Do This Third)
**Goal**: Connect components to actual data

1. **Data Structure**
   - Create JSON files for Pokemon, teams, cores, etc.
   - Implement data loading logic

2. **Tab Content**
   - Build out each tab with real content
   - Connect to data sources
   - Add sprite images

3. **Interactions**
   - Team card tooltips (pokepaste links)
   - Pokemon detail navigation (if implemented)
   - Search functionality (if implemented)

**Deliverable**: Fully functional app with real content

---

### Phase 4: Polish (Do This Last)
**Goal**: Refinements and optimization

1. **Animations**
   - Tab transitions
   - Hover effects
   - Tooltip animations

2. **Responsive**
   - Test on mobile devices
   - Adjust spacing/sizing
   - Fix any layout issues

3. **Performance**
   - Lazy load sprites
   - Optimize images
   - Minify CSS if needed

4. **Accessibility**
   - Keyboard navigation
   - ARIA labels
   - Color contrast check

**Deliverable**: Production-ready application

---

## Code Examples

### Example 1: Complete Tab System

#### HTML Structure
```html
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>ADV OU Knowledge Base</title>
  
  <!-- Fonts -->
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&family=JetBrains+Mono:wght@400;500;600;700&display=swap" rel="stylesheet">
  
  <!-- CSS -->
  <link rel="stylesheet" href="css/reset.css">
  <link rel="stylesheet" href="css/variables.css">
  <link rel="stylesheet" href="css/typography.css">
  <link rel="stylesheet" href="css/components.css">
  <link rel="stylesheet" href="css/layout.css">
  <link rel="stylesheet" href="css/utilities.css">
</head>
<body>
  <!-- Navigation -->
  <nav class="nav-tabs">
    <a href="#" class="nav-tab active" data-tab="pokemon">Pokemon</a>
    <a href="#" class="nav-tab" data-tab="metagame">Metagame</a>
    <a href="#" class="nav-tab" data-tab="archetypes">Archetypes</a>
    <a href="#" class="nav-tab" data-tab="cores">Cores</a>
    <a href="#" class="nav-tab" data-tab="sample-teams">Sample Teams</a>
    <a href="#" class="nav-tab" data-tab="speed-tiers">Speed Tiers</a>
    <a href="#" class="nav-tab" data-tab="calculator">Calculator</a>
  </nav>

  <!-- Main Content -->
  <main class="main-content">
    <div class="container">
      <!-- Pokemon Tab -->
      <div class="tab-pane active" id="pokemon-tab">
        <h1 class="section-header">Pokemon</h1>
        <!-- Content here -->
      </div>

      <!-- Metagame Tab -->
      <div class="tab-pane" id="metagame-tab">
        <h1 class="section-header">Metagame</h1>
        <!-- Content here -->
      </div>

      <!-- More tabs... -->
    </div>
  </main>

  <!-- JavaScript -->
  <script src="js/main.js"></script>
  <script src="js/tooltip.js"></script>
  <script src="js/sprites.js"></script>
</body>
</html>
```

#### JavaScript (main.js)
```javascript
// Tab switching logic
document.addEventListener('DOMContentLoaded', () => {
  const tabs = document.querySelectorAll('.nav-tab');
  const panes = document.querySelectorAll('.tab-pane');

  tabs.forEach(tab => {
    tab.addEventListener('click', (e) => {
      e.preventDefault();
      
      // Remove active class from all tabs and panes
      tabs.forEach(t => t.classList.remove('active'));
      panes.forEach(p => p.classList.remove('active'));
      
      // Add active class to clicked tab
      tab.classList.add('active');
      
      // Show corresponding pane
      const targetTab = tab.dataset.tab;
      const targetPane = document.getElementById(`${targetTab}-tab`);
      if (targetPane) {
        targetPane.classList.add('active');
      }
    });
  });
});
```

---

### Example 2: Team Card with Tooltip

#### HTML
```html
<div class="team-card" data-pokepaste="https://pokepast.es/f6229d2c867e21d6">
  <div class="team-card-header">
    <h3 class="team-card-title">Big 5 + Starmie (Beerlover)</h3>
    <div class="team-card-meta">
      <span class="archetype-badge defensive">TSS Balance</span>
      <span class="archetype-badge beginner">Beginner-Friendly</span>
    </div>
  </div>
  
  <div class="team-card-sprites">
    <div class="team-card-sprite">
      <img src="assets/sprites/skarmory.png" alt="Skarmory">
    </div>
    <div class="team-card-sprite">
      <img src="assets/sprites/blissey.png" alt="Blissey">
    </div>
    <div class="team-card-sprite">
      <img src="assets/sprites/tyranitar.png" alt="Tyranitar">
    </div>
    <div class="team-card-sprite">
      <img src="assets/sprites/swampert.png" alt="Swampert">
    </div>
    <div class="team-card-sprite">
      <img src="assets/sprites/gengar.png" alt="Gengar">
    </div>
    <div class="team-card-sprite">
      <img src="assets/sprites/starmie.png" alt="Starmie">
    </div>
  </div>
  
  <p class="team-card-description">
    The quintessential TSS style. Features bulky physical Tyranitar breaking cores with Spikes support.
  </p>
</div>

<!-- Tooltip (hidden by default) -->
<div class="tooltip" id="team-tooltip">
  <div class="tooltip-title">View Pokepaste</div>
  <a href="#" class="tooltip-link" target="_blank">
    Open in new tab →
  </a>
</div>
```

#### JavaScript (tooltip.js)
```javascript
document.addEventListener('DOMContentLoaded', () => {
  const teamCards = document.querySelectorAll('.team-card');
  const tooltip = document.getElementById('team-tooltip');
  const tooltipLink = tooltip.querySelector('.tooltip-link');
  
  teamCards.forEach(card => {
    let tapCount = 0;
    let tapTimer = null;
    
    // Desktop: Click to show tooltip, double-click to navigate
    card.addEventListener('click', (e) => {
      const pokepaste = card.dataset.pokepaste;
      
      // Mobile: Handle double-tap
      if ('ontouchstart' in window) {
        tapCount++;
        
        if (tapCount === 1) {
          // First tap: Show tooltip
          showTooltip(e, pokepaste);
          tapTimer = setTimeout(() => {
            tapCount = 0;
          }, 300);
        } else if (tapCount === 2) {
          // Second tap: Navigate to Pokemon page (implement later)
          clearTimeout(tapTimer);
          tapCount = 0;
          // navigateToPokemonPage(card);
        }
      } else {
        // Desktop: Single click shows tooltip
        showTooltip(e, pokepaste);
      }
    });
    
    // Desktop: Double-click to navigate
    card.addEventListener('dblclick', (e) => {
      if (!('ontouchstart' in window)) {
        // navigateToPokemonPage(card);
      }
    });
  });
  
  function showTooltip(event, pokepasteUrl) {
    tooltipLink.href = pokepasteUrl;
    tooltip.classList.add('active');
    
    // Position tooltip near cursor/tap
    tooltip.style.left = event.pageX + 'px';
    tooltip.style.top = event.pageY + 'px';
  }
  
  // Hide tooltip when clicking outside
  document.addEventListener('click', (e) => {
    if (!e.target.closest('.team-card') && !e.target.closest('.tooltip')) {
      tooltip.classList.remove('active');
    }
  });
});
```

---

### Example 3: Speed Tier List

#### HTML
```html
<div class="section">
  <h2 class="section-header">Practical Speed Tiers</h2>
  
  <h3 class="section-subheader">400+ - Boosted Sweepers Only</h3>
  
  <div class="speed-tier-list">
    <div class="speed-tier-item">
      <img src="assets/sprites/salamence.png" alt="Salamence" class="speed-tier-sprite">
      <span class="speed-tier-pokemon">Salamence</span>
      <span class="speed-tier-details">+1 Dragon Dance, Adamant 140 EVs</span>
      <span class="speed-tier-number">406</span>
    </div>
    
    <div class="speed-tier-item">
      <img src="assets/sprites/ludicolo.png" alt="Ludicolo" class="speed-tier-sprite">
      <span class="speed-tier-pokemon">Ludicolo</span>
      <span class="speed-tier-details">Swift Swim in rain, Modest 104 EVs</span>
      <span class="speed-tier-number">404</span>
    </div>
    
    <div class="speed-tier-item">
      <img src="assets/sprites/heracross.png" alt="Heracross" class="speed-tier-sprite">
      <span class="speed-tier-pokemon">Heracross</span>
      <span class="speed-tier-details">+1 Salac Berry, Adamant max</span>
      <span class="speed-tier-number">403</span>
    </div>
  </div>
</div>
```

---

### Example 4: CSS Variables File

#### css/variables.css
```css
:root {
  /* Colors - Base */
  --color-bg-primary: #0a1929;
  --color-bg-surface: #1e2936;
  --color-bg-surface-hover: #253645;
  --color-border: #2d3748;
  --color-border-hover: #3d4f5f;
  
  /* Colors - Brand */
  --color-sapphire: #457b9d;
  --color-emerald: #2a9d8f;
  --color-electric: #ffb703;
  --color-ruby: #e63946;
  
  /* Colors - Text */
  --color-text-primary: #e2e8f0;
  --color-text-secondary: #94a3b8;
  --color-text-tertiary: #64748b;
  --color-link: #60a5fa;
  --color-link-hover: #93c5fd;
  
  /* Colors - Pokemon Types */
  --type-normal: #a8a878;
  --type-fire: #f08030;
  --type-water: #6890f0;
  --type-electric: #f8d030;
  --type-grass: #78c850;
  --type-ice: #98d8d8;
  --type-fighting: #c03028;
  --type-poison: #a040a0;
  --type-ground: #e0c068;
  --type-flying: #a890f0;
  --type-psychic: #f85888;
  --type-bug: #a8b820;
  --type-rock: #b8a038;
  --type-ghost: #705898;
  --type-dragon: #7038f8;
  --type-dark: #705848;
  --type-steel: #b8b8d0;
  
  /* Typography */
  --font-mono: 'JetBrains Mono', 'Fira Code', 'Courier New', monospace;
  --font-sans: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
  
  --text-h1: 2.5rem;
  --text-h2: 2rem;
  --text-h3: 1.5rem;
  --text-h4: 1.25rem;
  --text-h5: 1.125rem;
  --text-base: 1rem;
  --text-sm: 0.875rem;
  --text-xs: 0.75rem;
  --text-lg: 1.125rem;
  
  --line-height-heading: 1.2;
  --line-height-body: 1.6;
  --line-height-tight: 1.4;
  
  --font-weight-normal: 400;
  --font-weight-medium: 500;
  --font-weight-semibold: 600;
  --font-weight-bold: 700;
  
  /* Spacing */
  --space-unit: 0.25rem;
  --space-1: calc(var(--space-unit) * 1);
  --space-2: calc(var(--space-unit) * 2);
  --space-3: calc(var(--space-unit) * 3);
  --space-4: calc(var(--space-unit) * 4);
  --space-5: calc(var(--space-unit) * 5);
  --space-6: calc(var(--space-unit) * 6);
  --space-8: calc(var(--space-unit) * 8);
  --space-10: calc(var(--space-unit) * 10);
  --space-12: calc(var(--space-unit) * 12);
  --space-16: calc(var(--space-unit) * 16);
  --space-20: calc(var(--space-unit) * 20);
  
  /* Common Patterns */
  --padding-card: var(--space-6);
  --padding-button: var(--space-3) var(--space-5);
  --padding-section: var(--space-8);
  
  --gap-list: var(--space-3);
  --gap-grid: var(--space-4);
  --gap-inline: var(--space-2);
  
  --margin-heading: var(--space-6);
  --margin-section: var(--space-10);
  
  /* Breakpoints */
  --breakpoint-sm: 640px;
  --breakpoint-md: 768px;
  --breakpoint-lg: 1024px;
  --breakpoint-xl: 1280px;
}
```

---

## Testing Checklist

### Visual Testing
- [ ] All colors match specification
- [ ] Typography uses correct fonts (JetBrains Mono + Inter)
- [ ] Spacing is consistent across components
- [ ] Sprites load and display correctly (32px inline, 48px cards)
- [ ] Type badges show correct colors
- [ ] Hover states work on desktop
- [ ] Active tab indicator is visible

### Functional Testing
- [ ] Tab switching works
- [ ] Team card tooltips appear on single tap/click
- [ ] Pokepaste links open correctly
- [ ] All sections display content
- [ ] Sprite fallbacks work when images fail to load
- [ ] Search functionality (if implemented)

### Responsive Testing
- [ ] Mobile: Navigation scrolls horizontally
- [ ] Mobile: Single column layout for grids
- [ ] Mobile: Touch targets are 44x44px minimum
- [ ] Tablet: Two-column grid works
- [ ] Desktop: Three-column grid works
- [ ] All breakpoints tested (640px, 768px, 1024px)

### Performance Testing
- [ ] Sprites lazy load below fold
- [ ] No layout shift on page load
- [ ] Animations run at 60fps
- [ ] CSS is minified (optional for v1)
- [ ] Total page size < 2MB

### Accessibility Testing
- [ ] Keyboard navigation works
- [ ] Tab order is logical
- [ ] ARIA labels present where needed
- [ ] Color contrast meets WCAG AA (minimum)
- [ ] Focus indicators visible

---

## Final Notes for Claude Code

### Key Priorities
1. **Get variables.css right first** - Everything else builds on this
2. **Mobile-first approach** - Write CSS for mobile, then add desktop media queries
3. **Component isolation** - Build and test components independently before integrating
4. **Real content early** - Don't spend too long on dummy data; use real Pokemon/teams ASAP

### Common Pitfalls to Avoid
- ❌ Using red (Ruby) for non-negative UI elements
- ❌ Mixing fonts (only JetBrains Mono + Inter)
- ❌ Over-animating (keep it minimal)
- ❌ Inconsistent spacing (use the spacing scale!)
- ❌ Forgetting image-rendering: pixelated for sprites

### When to Ask Questions
- If the design doesn't account for a specific content type
- If a component needs functionality not specified here
- If there are performance concerns with the approach
- If accessibility requirements conflict with design

### Success Criteria
The redesign is successful if:
1. It looks distinctly different from Smogon at first glance
2. Data (stats, EVs, speed) feels authoritative and clear
3. Navigation is intuitive on mobile
4. The app feels like a professional competitive tool, not a wiki
5. All content from the original site is preserved and accessible

---

**End of Design Specification**
Version 1.0 | February 2, 2026
