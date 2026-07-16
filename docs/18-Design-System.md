```
Document ID:    VM-018
Document:       Design System Specification
Project:        VineMind AI
Version:        1.0
Status:         Draft
Author:         Jeffrey Moepi
Hackathon:      TerraClim ET-GEO Hackathon 2026
Last Updated:   16 July 2026
```

---

# 18. Design System Specification

## 18.1 Introduction

This document defines the complete design system for VineMind AI — tokens, typography, colour, spacing, components, layout, and theme. It serves as the single source of truth for all visual and interaction design decisions, ensuring consistency across the React frontend and any future mobile application.

---

## 18.2 Design Principles

| Principle | Description | Example |
|-----------|-------------|---------|
| **Decision First** | The most important information is always the recommended action | Irrigation priority sits above all other data |
| **Explain Before Display** | Every visual element has a rationale — show evidence, not just numbers | Stress score accompanied by contributor breakdown |
| **Progressive Disclosure** | Summary first, detail on demand | Dashboard shows score → click shows full DEP |
| **Consistent Language** | Colours, icons, and patterns mean the same thing everywhere | Red always means high stress or critical action |
| **Accessible by Default** | Every design works for users with colour vision deficiency, low vision, and keyboard-only navigation | 4.5:1 contrast minimum, icons supplement colour |

---

## 18.3 Design Tokens

### 18.3.1 Colour — Stress Palette (Semantic)

| Token | Hex | RGB | Usage |
|-------|-----|-----|-------|
| `stress.healthy` | `#22C55E` | 34, 197, 94 | Healthy blocks (0–20) |
| `stress.monitor` | `#EAB308` | 234, 179, 8 | Monitor blocks (21–40) |
| `stress.moderate` | `#F97316` | 249, 115, 22 | Moderate blocks (41–60) |
| `stress.high` | `#EF4444` | 239, 68, 68 | High stress blocks (61–80) |
| `stress.critical` | `#DC2626` | 220, 38, 38 | Critical blocks (81–100) |
| `stress.nodata` | `#9CA3AF` | 156, 163, 175 | Missing or stale data |

### 18.3.2 Colour — Primary

| Token | Light Theme | Dark Theme | Usage |
|-------|-------------|------------|-------|
| `primary.50` | `#F0FDF4` | `#052E16` | Hover backgrounds |
| `primary.100` | `#DCFCE7` | `#14532D` | Active backgrounds |
| `primary.500` | `#22C55E` | `#22C55E` | Primary actions, links |
| `primary.600` | `#16A34A` | `#4ADE80` | Primary hover |
| `primary.700` | `#15803D` | `#86EFAC` | Primary active |

### 18.3.3 Colour — Neutral

| Token | Light Theme | Dark Theme | Usage |
|-------|-------------|------------|-------|
| `neutral.0` | `#FFFFFF` | `#09090B` | Background |
| `neutral.50` | `#FAFAFA` | `#18181B` | Card background |
| `neutral.100` | `#F4F4F5` | `#27272A` | Borders, dividers |
| `neutral.200` | `#E4E4E7` | `#3F3F46` | Subtle borders |
| `neutral.400` | `#A1A1AA` | `#71717A` | Placeholder text |
| `neutral.500` | `#71717A` | `#A1A1AA` | Secondary text |
| `neutral.700` | `#3F3F46` | `#D4D4D8` | Body text |
| `neutral.900` | `#18181B` | `#FAFAFA` | Headings |

### 18.3.4 Colour — Feedback

| Token | Hex | Usage |
|-------|-----|-------|
| `feedback.success` | `#22C55E` | Confirmed actions, completed |
| `feedback.warning` | `#EAB308` | Caution, degraded state |
| `feedback.error` | `#EF4444` | Errors, failed operations |
| `feedback.info` | `#3B82F6` | Informational, neutral updates |

### 18.3.5 Colour — Map Layers

| Token | Hex | Usage |
|-------|-----|-------|
| `map.polygon.fill` | `rgba(34, 197, 94, 0.3)` | Block polygon default fill |
| `map.polygon.stroke` | `#15803D` | Block polygon border |
| `map.polygon.hover` | `rgba(34, 197, 94, 0.5)` | Block polygon hover fill |
| `map.polygon.selected` | `rgba(59, 130, 246, 0.4)` | Selected block fill |
| `map.overlay.stress` | Stress palette | Stress colour overlay on blocks |
| `map.label` | `#18181B` | Block name labels on map |

---

### 18.3.6 Typography

| Token | Font | Size | Weight | Line Height | Usage |
|-------|------|------|--------|-------------|-------|
| `heading.1` | Inter | 30px | 700 | 36px | Page titles |
| `heading.2` | Inter | 24px | 600 | 32px | Section headings |
| `heading.3` | Inter | 20px | 600 | 28px | Card headings |
| `heading.4` | Inter | 16px | 600 | 24px | Sub-headings |
| `body.large` | Inter | 16px | 400 | 24px | Card descriptions |
| `body.default` | Inter | 14px | 400 | 20px | Body text |
| `body.small` | Inter | 12px | 400 | 16px | Captions, labels |
| `mono.default` | JetBrains Mono | 14px | 400 | 20px | Code, scores, data |
| `mono.large` | JetBrains Mono | 20px | 600 | 28px | Stress score display |

### 18.3.7 Spacing (8px Grid)

| Token | Value | Usage |
|-------|-------|-------|
| `space.0` | 0px | Reset |
| `space.1` | 4px | Tight inner padding |
| `space.2` | 8px | Icon gaps, small padding |
| `space.3` | 12px | Inner card padding |
| `space.4` | 16px | Card padding, component gaps |
| `space.5` | 20px | Section gaps |
| `space.6` | 24px | Card gaps in grid |
| `space.8` | 32px | Page section spacing |
| `space.10` | 40px | Large section gaps |
| `space.12` | 48px | Page-level spacing |
| `space.16` | 64px | Major section breaks |

### 18.3.8 Border Radius

| Token | Value | Usage |
|-------|-------|-------|
| `radius.none` | 0px | — |
| `radius.sm` | 4px | Badges, small chips |
| `radius.md` | 8px | Buttons, inputs |
| `radius.lg` | 12px | Cards |
| `radius.xl` | 16px | Modals, large cards |
| `radius.full` | 9999px | Pill shapes, circular avatars |

### 18.3.9 Shadows

| Token | Value | Usage |
|-------|-------|-------|
| `shadow.sm` | `0 1px 2px rgba(0,0,0,0.05)` | Subtle elevation |
| `shadow.md` | `0 4px 6px -1px rgba(0,0,0,0.1)` | Card default |
| `shadow.lg` | `0 10px 15px -3px rgba(0,0,0,0.1)` | Dropdown, popover |
| `shadow.xl` | `0 20px 25px -5px rgba(0,0,0,0.1)` | Modal |

### 18.3.10 Breakpoints

| Token | Value | Target |
|-------|-------|--------|
| `bp.sm` | 640px | Mobile landscape |
| `bp.md` | 768px | Tablet portrait |
| `bp.lg` | 1024px | Tablet landscape / small desktop |
| `bp.xl` | 1280px | Desktop |
| `bp.2xl` | 1536px | Large desktop |

### 18.3.11 Z-Index

| Token | Value | Usage |
|-------|-------|-------|
| `z.base` | 0 | Default |
| `z.dropdown` | 50 | Dropdowns, tooltips |
| `z.sticky` | 100 | Sticky header |
| `z.map-controls` | 200 | Map layer controls |
| `z.modal-backdrop` | 300 | Modal backdrop |
| `z.modal` | 400 | Modal content |
| `z.copilot` | 500 | AI Copilot panel |
| `z.toast` | 600 | Toast notifications |
| `z.tooltip` | 700 | Tooltips |

---

## 18.4 Component Library

### 18.4.1 Component Inventory

| Category | Component | Variant | Status |
|----------|-----------|---------|--------|
| **Primitives** | Button | primary, secondary, ghost, destructive | To build |
| | Input | text, number, search | To build |
| | Select | single, multi | To build |
| | Badge | status, category, count | To build |
| | Card | default, highlighted, interactive | To build |
| | Dialog | modal, alert | To build |
| | Toast | success, error, info, warning | To build |
| | Skeleton | text, card, chart | To build |
| **Data Display** | MetricCard | score, trend, comparison | To build |
| | DataTable | sortable, filterable, paginated | To build |
| | ChartCard | line, bar, area | To build |
| | Timeline | chronological, event-based | To build |
| | EmptyState | illustration + message + action | To build |
| **Domain-Specific** | StressBadge | colour-coded score indicator | To build |
| | RecommendationCard | action, priority, explanation | To build |
| | EvidenceTimeline | DEP contributors in order | To build |
| | ConfidenceBadge | visual confidence indicator | To build |
| | PriorityQueue | ranked irrigation queue | To build |
| | BlockCard | mini block summary with map thumbnail | To build |
| | WeatherWidget | current + forecast | To build |
| | PhenologyBadge | growth stage indicator | To build |
| **Layout** | AppShell | sidebar + header + main | To build |
| | Sidebar | navigation, collapsible | To build |
| | Header | breadcrumb, user menu, notifications | To build |
| | PageLayout | content + right panel | To build |
| | Grid | responsive 12-column grid | To build |
| **Map** | MapView | interactive map container | To build |
| | BlockOverlay | stress-coloured polygons | To build |
| | LayerControl | toggle map layers | To build |
| | BlockTooltip | hover info card | To build |
| **AI Copilot** | ChatPanel | message list + input | To build |
| | MessageBubble | user + assistant messages | To build |
| | EvidenceCard | cited DEP in conversation | To build |

### 18.4.2 Component Specifications

#### StressBadge

```
┌─────────────────────────────────────────────────┐
│  StressBadge                                     │
│                                                  │
│  Props:                                          │
│    score: number (0-100)                         │
│    size: 'sm' | 'md' | 'lg'                     │
│    showLabel: boolean                            │
│                                                  │
│  States:                                         │
│    sm: [● 74]         (dot + number)            │
│    md: [● 74/100]     (dot + score + max)       │
│    lg: [● 74/100      (dot + score + category)  │
│         High Stress]                             │
│                                                  │
│  Colour mapping:                                 │
│    0-20  → stress.healthy   "Healthy"            │
│    21-40 → stress.monitor   "Monitor"            │
│    41-60 → stress.moderate  "Moderate"           │
│    61-80 → stress.high      "High Stress"        │
│    81-100→ stress.critical  "Critical"           │
└─────────────────────────────────────────────────┘
```

#### RecommendationCard

```
┌─────────────────────────────────────────────────┐
│  RecommendationCard                              │
│                                                  │
│  ┌──────────────────────────────────────────┐   │
│  │ ● Block A                    [74/100]     │   │
│  │ Irrigate Tonight                         │   │
│  │ ─────────────────────────────────────    │   │
│  │ Confidence: 87%  │  Est. Volume: 4,500 L │   │
│  │ Priority: #1 of 8 blocks                 │   │
│  │                                           │   │
│  │ [View Explanation]  [Approve]  [Dismiss] │   │
│  └──────────────────────────────────────────┘   │
│                                                  │
│  Props:                                          │
│    blockName: string                             │
│    stressScore: number                           │
│    recommendation: string                        │
│    confidence: number                            │
│    estimatedVolume: number                       │
│    priority: number                              │
│    totalBlocks: number                           │
│    onApprove: () => void                         │
│    onDismiss: () => void                         │
│    onViewEvidence: () => void                    │
└─────────────────────────────────────────────────┘
```

#### MetricCard

```
┌─────────────────────────────────────────────────┐
│  MetricCard                                      │
│                                                  │
│  ┌─────────────┐  ┌─────────────┐               │
│  │  Water      │  │  ETa        │               │
│  │  Stress     │  │  (Today)    │               │
│  │  ────────   │  │  ────────   │               │
│  │  ● 74/100   │  │  3.2 mm     │               │
│  │  High       │  │  ▼ -8%      │               │
│  └─────────────┘  └─────────────┘               │
│                                                  │
│  Props:                                          │
│    label: string                                 │
│    value: string | number                        │
│    unit?: string                                 │
│    trend?: { value: number, direction: 'up'|'down'|'stable' }
│    stressLevel?: 'healthy'|'monitor'|'moderate'|'high'|'critical'
│    icon?: ReactNode                              │
└─────────────────────────────────────────────────┘
```

---

## 18.5 Layout System

### 18.5.1 App Shell

```
┌─────────────────────────────────────────────────────────────┐
│  Header (sticky, h=64px)                                    │
│  ┌──────────────────────────────────────────────────────┐   │
│  │ 🌿 VineMind AI    [Breadcrumbs]    [🔔] [👤 ▼]     │   │
│  └──────────────────────────────────────────────────────┘   │
│  ┌──────┬─────────────────────────────────────────────────┐ │
│  │ Side │                                                 │ │
│  │ bar  │              Main Content Area                  │ │
│  │      │                                                 │ │
│  │ w=   │  ┌─────────────────────────────────────────┐   │ │
│  │ 240  │  │                                         │   │ │
│  │ px   │  │         Page Content                     │   │ │
│  │      │  │                                         │   │ │
│  │ (col │  │                                         │   │ │
│  │ lapse│  └─────────────────────────────────────────┘   │ │
│  │ d=   │                                                 │ │
│  │ 64)  │                                                 │ │
│  └──────┴─────────────────────────────────────────────────┘ │
└─────────────────────────────────────────────────────────────┘
```

### 18.5.2 Sidebar Navigation

```
┌──────────────┐
│ 🌿 VineMind  │
│              │
│ 📊 Dashboard │ ← active
│ 🗺️ Explorer  │
│ 🎯 Decisions │
│ 📈 Analytics │
│ 📄 Reports   │
│ 🤖 Copilot   │
│              │
│ ─────────── │
│ ⚙️ Settings  │
│ ❓ Help      │
└──────────────┘
```

### 18.5.3 Page Grid

| Page | Layout | Grid |
|------|--------|------|
| Dashboard | 12-col grid | 4+4+4 (metrics) / 8+4 (chart + priority) |
| Vineyard Explorer | Full-width map | Map fills entire main area |
| Block Details | 2-col split | 7 (details) + 5 (evidence panel) |
| Decision Centre | List + detail | 8 (list) + 4 (selected detail) |
| Analytics | Dashboard grid | 6+6 (charts), full-width (trends) |
| Reports | Centered content | 8-col centered |
| AI Copilot | Split panel | 7 (content) + 5 (copilot panel) |

---

## 18.6 Theme System

### 18.6.1 Light Theme (Default)

```css
:root {
  --bg-primary: #FFFFFF;
  --bg-secondary: #FAFAFA;
  --bg-tertiary: #F4F4F5;
  --text-primary: #18181B;
  --text-secondary: #3F3F46;
  --text-muted: #71717A;
  --border-default: #E4E4E7;
  --border-subtle: #F4F4F5;
}
```

### 18.6.2 Dark Theme

```css
:root.dark {
  --bg-primary: #09090B;
  --bg-secondary: #18181B;
  --bg-tertiary: #27272A;
  --text-primary: #FAFAFA;
  --text-secondary: #D4D4D8;
  --text-muted: #A1A1AA;
  --border-default: #3F3F46;
  --border-subtle: #27272A;
}
```

### 18.6.3 Theme Toggle

The theme toggle is accessible from the header user menu. Theme preference persists in `localStorage` and respects `prefers-color-scheme` on first visit.

---

## 18.7 Motion & Animation

| Token | Value | Usage |
|-------|-------|-------|
| `duration.fast` | 100ms | Button hover, focus ring |
| `duration.normal` | 200ms | Panel transitions, dropdowns |
| `duration.slow` | 300ms | Page transitions, modals |
| `easing.default` | `cubic-bezier(0.4, 0, 0.2, 1)` | General transitions |
| `easing.in` | `cubic-bezier(0.4, 0, 1, 1)` | Entering elements |
| `easing.out` | `cubic-bezier(0, 0, 0.2, 1)` | Exiting elements |

**Reduced Motion:** All animations respect `prefers-reduced-motion: reduce`. When enabled, transitions are instant and animations are disabled.

---

## 18.8 Accessibility

| Requirement | Implementation |
|-------------|----------------|
| Colour contrast | Minimum 4.5:1 for text, 3:1 for UI components |
| Keyboard navigation | Tab order follows visual layout, all interactive elements focusable |
| Focus indicators | 2px solid primary ring with 2px offset |
| Screen reader | All images have alt text, ARIA labels on interactive elements |
| Colour not sole indicator | Stress levels use colour + icon + text label |
| Responsive text | Minimum 12px, scalable with user preferences |
| Semantic HTML | Correct heading hierarchy, landmarks, lists |
| Motion | Respects `prefers-reduced-motion` |
