# Site Icon / Favicon

This directory contains all the favicon and site icon files for the website.

## Files

### `favicon.png` (512x512)
- **Purpose**: Main favicon used by modern browsers
- **Used by**: Chrome, Firefox, Safari, Edge (desktop and mobile)
- **Where it appears**: Browser tabs, bookmarks, browser history
- **Configured in**: `_quarto.yml` under `website.favicon`

### `apple-touch-icon.png` (180x180)
- **Purpose**: Icon when website is saved to iOS home screen
- **Used by**: iPhone, iPad, and other Apple devices
- **Where it appears**: Home screen app icon when user "Add to Home Screen"
- **Configured in**:
  - `_quarto.yml` under `project.resources` (to copy file to output)
  - `_quarto.yml` under `format.html.include-in-header` (HTML meta tag)

### `favicon.ico` (multi-size)
- **Purpose**: Legacy favicon format for older browsers
- **Contains**: Multiple sizes (16x16, 32x32, 48x48, 64x64)
- **Used by**: Older browsers, some Windows applications
- **Currently**: Not actively used, but available if needed

### `favicon-32x32.png`
- **Purpose**: Standard 32x32 favicon size
- **Currently**: Not actively used, but available if needed
- **Could be used for**: Explicit size specification in HTML meta tags

## Design

The favicon features the initials **EGMC** with a geometric pattern design:

### Color Scheme
- **Background**: Deep purple/blue `rgb(30, 20, 60)`
- **Accent 1**: Purple `rgb(100, 60, 180)`
- **Accent 2**: Cyan `rgb(60, 180, 200)`
- **Accent 3**: Gold `rgb(255, 200, 80)`
- **Text**: White `rgb(255, 255, 255)`

### Design Elements
- Rotating squares creating a dynamic geometric pattern
- Circular accent outline for depth
- Bold white text with shadow for readability
- Modern, professional aesthetic

## Regenerating Icons

To regenerate the icons (e.g., to change colors or design):

1. Modify the `generate_favicon.py` script if needed
2. Run the script:
   ```bash
   cd files/site_icon
   python3 generate_favicon.py
   ```
3. Rebuild your Quarto site:
   ```bash
   quarto render
   ```

## Configuration in Quarto

The icons are configured in `_quarto.yml`:

```yaml
project:
  resources:
    - files/site_icon/apple-touch-icon.png  # Copies to output

website:
  favicon: files/site_icon/favicon.png      # Main favicon

format:
  html:
    include-in-header:
      text: |
        <link rel="apple-touch-icon" sizes="180x180" href="files/site_icon/apple-touch-icon.png">
```

## Browser Support

| File | Chrome | Firefox | Safari | Edge | iOS Safari | Android |
|------|--------|---------|--------|------|------------|---------|
| favicon.png |  |  |  |  |  |  |
| apple-touch-icon.png | - | - | - | - |  | - |
| favicon.ico |  |  |  |  | - | - |

## Testing

After rebuilding your site, you can test:

1. **Browser tab icon**: Open your site in a browser - the EGMC icon should appear in the tab
2. **iOS home screen**: On an iPhone/iPad, tap Share ’ Add to Home Screen - the 180x180 icon should appear
3. **Bookmarks**: Bookmark your site - the icon should appear next to the bookmark

## Technical Notes

- All icons are generated from a single Python script for consistency
- High-resolution source (512x512) is downscaled for smaller sizes using LANCZOS resampling for quality
- The .ico file contains multiple sizes in one file for maximum compatibility
- Apple touch icons should be 180x180 per Apple's guidelines (though they support other sizes)
