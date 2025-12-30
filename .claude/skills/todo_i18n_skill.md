---
description: Provides internationalization (i18n) and localization support for todo application, with special emphasis on Urdu language integration.
responsibilities:
  - Manage translation strings for multiple languages
  - Support Urdu (RTL) text direction and formatting
  - Handle locale-specific date/time/number formats
  - Provide language selection and switching
  - Support right-to-left (RTL) UI for Urdu and other RTL languages
  - Manage translation file loading and fallback
rules:
  - All user-facing text must be localizable
  - RTL languages require proper text alignment
  - Fallback to English when translation missing
  - Preserve bidirectional text properly
scope:
  - Used by: todo-i18n-agent
---

## User Input

```text
$ARGUMENTS
```

## Implementation Requirements

Implement a skill that provides internationalization and localization support.

### Requirements

1. **Translation Management**:
   - Store translations in structured files (JSON/YAML)
   - Support nested translation keys
   - Pluralization rules per language
   - Gender-specific translations
   - Context-aware translations

2. **Language Support**:
   - English (default)
   - Urdu (RTL primary)
   - Arabic (RTL)
   - Hindi, Spanish, French, etc.
   - Easy addition of new languages

3. **Urdu/RTL Support**:
   - Detect RTL languages
   - Mirror UI elements for RTL
   - Proper text alignment (right-aligned)
   - Bidirectional text handling (LTR within RTL)
   - Urdu font support hints
   - Urdu date formatting

4. **Locale Formatting**:
   - Date format by locale (DD/MM/YYYY vs MM/DD/YYYY)
   - Time format (12h/24h based on locale)
   - Number format (decimal separators, digit shapes)
   - Currency format when applicable

5. **Language Selection**:
   - Detect system locale
   - CLI argument override
   - Configuration file setting
   - Runtime switching

6. **Missing Translations**:
   - Fallback to English
   - Log missing keys for translators
   - Show fallback text with marker for debugging

### Output

Return structured results with:
- Translated text for requested key
- Current locale settings
- Available languages list
- RTL status indicator
- Formatted date/number per locale
