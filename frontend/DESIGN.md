# Design System Strategy: The Clinical Sanctuary

## 1. Overview & Creative North Star
**Creative North Star: "The Ethereal Clinic"**

This design system moves away from the sterile, rigid, and often anxiety-inducing layouts of traditional medical portals. Instead, it adopts a philosophy of "Ethereal Minimalism." We treat the digital interface as a high-end physical sanctuary—using expansive breathing room, soft tonal layering, and sophisticated editorial typography to convey an atmosphere of calm, professional authority.

By breaking the traditional "box-and-line" grid, we use intentional asymmetry and overlapping "glass" surfaces to create a sense of organic flow. The goal is to make the patient feel cared for before they even step into the clinic, replacing clinical coldness with digital serenity.

---

## 2. Colors: Tonal Architecture
The palette is built on a foundation of clinical purity (`surface_container_lowest`) accented by intellectual blues and restorative greens.

*   **Primary (`#005394`) & Secondary (`#006d3c`):** Use these as "Precision Accents." They are markers of authority. The Primary Blue should be used for critical navigational paths, while the Secondary Green is reserved for wellness-related success states or health-tracking indicators.
*   **The "No-Line" Rule:** To maintain the "Sanctuary" aesthetic, **1px solid borders are strictly prohibited** for sectioning. Structural boundaries must be defined through background shifts. For example, a main content area (`surface`) should sit adjacent to a sidebar or secondary module using `surface_container_low`.
*   **Surface Hierarchy & Nesting:** Treat the UI as stacked sheets of fine vellum.
    *   **Base:** `surface` (#f7fafc)
    *   **Sub-sections:** `surface_container_low` (#f1f4f6)
    *   **Interactive Cards:** `surface_container_lowest` (#ffffff)
*   **The "Glass & Gradient" Rule:** For hero sections or high-impact CTAs, use a subtle linear gradient from `primary` (#005394) to `primary_container` (#2b6cb0) at a 135-degree angle. This adds "soul" and depth that prevents the design from feeling "flat-pack."
*   **Signature Textures:** Use `surface_tint` at 5% opacity as a backdrop for floating modals to ground them in the brand's blue-leaning DNA.

---

## 3. Typography: The Editorial Voice
We utilize a dual-typeface system to balance modern approachable warmth with clinical precision.

*   **Display & Headlines (Manrope):** The high x-height and geometric builds of Manrope convey modern transparency. Use `display-lg` (3.5rem) with tight letter-spacing (-0.02em) for hero headlines to create an editorial, high-end feel.
*   **Body & Titles (Inter):** Inter is used for its unrivaled legibility. Its neutral tone provides the "Trustworthy" anchor required for medical data.
*   **Hierarchy as Comfort:** Always lead with a `headline-md` for section titles, followed by generous `body-lg` (1rem) text. Ensure line-heights for body text are never below 1.6 to ensure readability for patients under stress or with visual impairments.

---

## 4. Elevation & Depth: Tonal Layering
Traditional shadows are too heavy for a medical sanctuary. We use "Ambient Lift."

*   **The Layering Principle:** Depth is achieved by placing `surface_container_lowest` cards on a `surface_container_low` background. This creates a natural "pop" without adding visual noise.
*   **Ambient Shadows:** If a floating element (like a mobile FAB or a dropdown) requires a shadow, use a multi-layered blur: `0px 4px 20px rgba(24, 28, 30, 0.04)`. The shadow is a tinted version of `on_surface`, mimicking natural light passing through a sterile environment.
*   **The "Ghost Border" Fallback:** In high-density data tables where separation is mandatory, use a "Ghost Border": `outline_variant` (#c1c7d2) at 15% opacity.
*   **Glassmorphism:** For top navigation bars or floating action panels, use `surface` with a 0.8 alpha and a `backdrop-filter: blur(20px)`. This keeps the user connected to the content beneath while providing a clear interactive layer.

---

## 5. Components: Soft Precision

### Buttons
*   **Primary:** High-pill shape (`rounded-full`). Use `primary` background with `on_primary` text. Apply a subtle inner-glow (1px top border, white at 10% opacity) for a premium tactile feel.
*   **Secondary:** `secondary_container` background with `on_secondary_container` text. Perfect for "Book Appointment" or "Refill Script" actions.
*   **Tertiary:** No background. Use `primary` text with an underline that only appears on hover.

### Cards & Lists
*   **The Rule of Radii:** All cards must use `xl` (1.5rem) corner radius. This softness reduces the "clinical edge."
*   **No Dividers:** Forbid the use of horizontal rules. Separate list items using `spacing-4` (1.4rem) of vertical white space or by alternating background tones between `surface_container_low` and `surface_container`.

### Input Fields
*   **State:** Use `surface_container_highest` for the input background to make the field feel "recessed" and ready to be filled. 
*   **Focus:** Transition the border to `primary` with a 2px thickness. Labels should use `label-md` and be positioned strictly above the field, never as placeholders.

### Additional Signature Components
*   **The "Wellness Progress" Chip:** A custom chip using `secondary_fixed` background. Used to show recovery milestones or health status.
*   **The Floating Concierge:** A bottom-right glassmorphic card for quick access to "Emergency Contact" or "Nurse Chat."

---

## 6. Do's and Don'ts

### Do:
*   **Do** use asymmetrical spacing. A wider left margin (e.g., `spacing-16`) vs. a tighter right margin creates a sophisticated editorial rhythm.
*   **Do** use "Optical White." Pure white (#ffffff) should only be used for the top-most elevated cards or background highlights. Use `background` (#f7fafc) for the page canvas.
*   **Do** prioritize the `manrope` typeface for all numbers and metrics to ensure they feel modern and clear.

### Don't:
*   **Don't** use "Alert Red" for anything but critical errors. For warnings, use `tertiary` tones to maintain the calm environment.
*   **Don't** use standard 90-degree corners. Even "small" elements like checkboxes should use `sm` (0.25rem) rounding.
*   **Don't** crowd the interface. If a screen feels full, increase the spacing scale by one increment (e.g., move from `spacing-6` to `spacing-8`). Space is a luxury in medical design; provide it to the user.