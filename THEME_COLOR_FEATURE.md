# Theme Color Customization for Cards by Club

## Feature Overview
A dynamic theme color picker has been added to the "Tarjetas por Club" (Cards by Club) page, allowing users to customize the color scheme of the player cards and UI elements in real-time.

## What's New

### Color Picker Component
- **Location:** Filter section at the top of the page
- **Type:** HTML5 Color Input
- **Label:** "Color Tema:" (Theme Color)
- **Default Color:** #cb4903 (Original RHC orange)

### Dynamic Color Application
The selected color is applied to:
✅ **Player Cards** - Gradient background (main color to lighter shade)
✅ **Club Section Border** - Left border accent
✅ **Club Titles** - Section headers
✅ **Filter Buttons** - "Filtrar" button styling
✅ **Input Borders** - Club select dropdown border

### Persistent Preferences
- Color selection is saved to browser's **localStorage**
- Theme color persists across page refreshes and sessions
- Each user can have their own preferred color

## How to Use

### Changing the Theme Color
1. Navigate to "Tarjetas por Club" in the menu
2. Locate the "Color Tema:" picker in the filter section
3. Click on the color picker box
4. Choose your desired color from the color picker
5. The page updates immediately with the new theme color

### Available Color Pickers
- Full spectrum of colors available
- Pre-set color swatches (depending on browser)
- Manual hex input on some browsers

### Preset Colors (Suggestions)
- **#cb4903** - Original RHC Orange (default)
- **#1e40af** - Professional Blue
- **#059669** - Fresh Green
- **#dc2626** - Bold Red
- **#7c3aed** - Purple
- **#0891b2** - Cyan
- **#ea580c** - Bright Orange
- **#16a34a** - Green
- **#4f46e5** - Indigo

## Technical Implementation

### CSS Variables (Custom Properties)
```css
:root {
    --theme-color: #cb4903;
    --theme-color-light: #ce791a;
}
```

All theme-dependent elements use these CSS variables instead of hardcoded colors.

### JavaScript Color Calculation
```javascript
function applyThemeColor(color) {
    // Converts hex color to gradient-friendly lighter shade
    // Updates CSS variables dynamically
    // Stores preference in localStorage
}
```

### localStorage Storage
```javascript
localStorage.setItem('cardsThemeColor', selectedColor);
const savedTheme = localStorage.getItem('cardsThemeColor');
```

## Features

✅ **Real-time Updates** - Color changes apply instantly without page reload
✅ **Persistent Storage** - Theme preference saved in browser
✅ **Gradient Generation** - Automatically creates lighter shade for gradients
✅ **Print Compatible** - Theme colors print properly
✅ **Responsive Design** - Color picker works on all devices
✅ **User Friendly** - Simple, intuitive color selection

## Affected Elements

### Visual Elements That Change Color
1. **Player Cards Background** - Gradient using selected color
2. **Club Section Left Border** - Accent border
3. **Club Title Text** - Section headings
4. **Filter Button** - Primary action button
5. **Select Dropdown Border** - Input field borders

### Elements That DON'T Change
- Navigation bar (maintains original styling)
- Page background
- Text content colors (remain white/dark for readability)
- Print button styling

## Browser Compatibility
- **Modern Browsers:** Full support (Chrome, Firefox, Safari, Edge)
- **Internet Explorer:** Not recommended (no localStorage or CSS variables)
- **Mobile Browsers:** Full support with native color pickers

## Color Picker Behavior

### Desktop Browsers
- Click to open full color picker interface
- Supports drag selection and numeric input
- Some browsers show color history

### Mobile/Tablet
- Long-press or tap to open native color picker
- Platform-specific color selection (iOS, Android)

## Code Changes

### JavaScript Added
- Color picker event listener
- localStorage integration
- Dynamic CSS variable updating
- Color lightening algorithm for gradients

### CSS Changes
- CSS variables replaced hardcoded colors
- Added `.theme-color-picker` styling
- Updated all color references to use `var(--theme-color)`

### HTML Changes
- Added color picker input field
- Updated filter section layout with flexbox gap
- Added label and title attributes

## Future Enhancement Ideas
- Preset theme color palette buttons
- Save multiple theme profiles
- Dark mode toggle
- Automatic color contrast adjustment
- Theme sharing via URL parameter
