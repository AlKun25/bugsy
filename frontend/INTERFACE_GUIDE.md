# Frontend Interface Visual Guide

## Main Interface Layout

```
┌─────────────────────────────────────────────────────────────────┐
│                        🐛 Bugsy Bug Analyzer                    │
│                                                                 │
│    Transform bug reports into comprehensive test plans with     │
│              AI-powered analysis and recommendations            │
└─────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────┐
│  [📁 File Upload]     [🐙 GitHub Issue]                        │
│   ▲ Active Tab         Inactive Tab                            │
└─────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────┐
│                     FILE UPLOAD MODE                           │
│                                                                 │
│  ┌───────────────────────────────────────────────────────────┐  │
│  │                                                           │  │
│  │              📄 Drag & Drop Area                         │  │
│  │                                                           │  │
│  │     Drag your bug.txt file here or click to select       │  │
│  │                                                           │  │
│  │                   [Choose File]                          │  │
│  │                                                           │  │
│  └───────────────────────────────────────────────────────────┘  │
│                                                                 │
│  📋 File Info: No file selected                                │
│                                                                 │
│                    [Upload & Analyze]                          │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

## GitHub Issue Mode Interface

```
┌─────────────────────────────────────────────────────────────────┐
│                        🐛 Bugsy Bug Analyzer                    │
│                                                                 │
│    Transform bug reports into comprehensive test plans with     │
│              AI-powered analysis and recommendations            │
└─────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────┐
│  [📁 File Upload]     [🐙 GitHub Issue]                        │
│   Inactive Tab         ▲ Active Tab                            │
└─────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────┐
│                    GITHUB ISSUE MODE                           │
│                                                                 │
│  Repository URL:                                                │
│  ┌───────────────────────────────────────────────────────────┐  │
│  │ https://github.com/owner/repo                             │  │
│  └───────────────────────────────────────────────────────────┘  │
│                                                                 │
│  Issue Number:                                                  │
│  ┌───────────────────────────────────────────────────────────┐  │
│  │ 123                                                       │  │
│  └───────────────────────────────────────────────────────────┘  │
│                                                                 │
│                  [Analyze GitHub Issue]                        │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

## File Upload States

### 1. Initial State (No File Selected)
```
┌───────────────────────────────────────────────────────────┐
│                                                           │
│              📄 Drag & Drop Area                         │
│                                                           │
│     Drag your bug.txt file here or click to select       │
│                                                           │
│                   [Choose File]                          │
│                                                           │
└───────────────────────────────────────────────────────────┘

📋 File Info: No file selected
```

### 2. File Selected State
```
┌───────────────────────────────────────────────────────────┐
│                                                           │
│              ✅ File Selected                            │
│                                                           │
│                    bug.txt                                │
│                   (2.5 KB)                               │
│                                                           │
│                 [Change File]                            │
│                                                           │
└───────────────────────────────────────────────────────────┘

📋 File Info: bug.txt (2.5 KB) - Ready to upload
```

### 3. Processing State
```
┌───────────────────────────────────────────────────────────┐
│                                                           │
│              ⏳ Processing...                            │
│                                                           │
│         Analyzing bug report and generating               │
│              comprehensive test plan                      │
│                                                           │
│              ████████░░░░ 80%                           │
│                                                           │
└───────────────────────────────────────────────────────────┘

📋 Status: Processing bug report...
```

### 4. Success State
```
┌───────────────────────────────────────────────────────────┐
│                                                           │
│              ✅ Analysis Complete!                       │
│                                                           │
│         Your test plan has been generated successfully    │
│                                                           │
│              [📥 Download test_plan.txt]                 │
│                                                           │
└───────────────────────────────────────────────────────────┘

📋 Result: Test plan generated with 16 comprehensive test cases
```

## GitHub Issue Processing States

### 1. Form Filled State
```
┌─────────────────────────────────────────────────────────────────┐
│  Repository URL:                                                │
│  ┌───────────────────────────────────────────────────────────┐  │
│  │ https://github.com/facebook/react                        │  │
│  └───────────────────────────────────────────────────────────┘  │
│                                                                 │
│  Issue Number:                                                  │
│  ┌───────────────────────────────────────────────────────────┐  │
│  │ 25123                                                     │  │
│  └───────────────────────────────────────────────────────────┘  │
│                                                                 │
│                  [Analyze GitHub Issue]                        │
└─────────────────────────────────────────────────────────────────┘
```

### 2. Fetching Issue State
```
┌─────────────────────────────────────────────────────────────────┐
│                                                                 │
│              🔄 Fetching GitHub Issue...                       │
│                                                                 │
│         Connecting to GitHub API and retrieving                │
│              issue #25123 from facebook/react                  │
│                                                                 │
│                    ████████████ 100%                          │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

### 3. Processing Issue State
```
┌─────────────────────────────────────────────────────────────────┐
│                                                                 │
│              ⚙️ Analyzing Issue Content...                     │
│                                                                 │
│         Processing issue description, comments, and            │
│              generating comprehensive test plan                 │
│                                                                 │
│                    ██████░░░░░░ 60%                           │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

### 4. GitHub Success State
```
┌─────────────────────────────────────────────────────────────────┐
│                                                                 │
│              ✅ GitHub Issue Analyzed!                         │
│                                                                 │
│         Issue #25123 from facebook/react has been              │
│              successfully analyzed and processed                │
│                                                                 │
│              [📥 Download test_plan.txt]                       │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

## Error States

### File Upload Error
```
┌───────────────────────────────────────────────────────────┐
│                                                           │
│              ❌ Upload Failed                            │
│                                                           │
│         Error: Invalid file type. Please upload          │
│                   a .txt file only.                      │
│                                                           │
│                   [Try Again]                            │
│                                                           │
└───────────────────────────────────────────────────────────┘
```

### GitHub Error
```
┌─────────────────────────────────────────────────────────────────┐
│                                                                 │
│              ❌ GitHub Issue Not Found                         │
│                                                                 │
│         Error: Issue #99999 not found in facebook/react.       │
│              Please check the repository URL and issue number.  │
│                                                                 │
│                        [Try Again]                             │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

## Responsive Design Breakpoints

### Mobile View (< 768px)
```
┌─────────────────────────┐
│    🐛 Bugsy Analyzer    │
│                         │
│  Transform bug reports  │
│   into test plans with  │
│     AI-powered analysis │
├─────────────────────────┤
│ [📁 File] [🐙 GitHub]  │
├─────────────────────────┤
│                         │
│   📄 Drag & Drop Area   │
│                         │
│  Drag your bug.txt file │
│   here or click below   │
│                         │
│     [Choose File]       │
│                         │
├─────────────────────────┤
│ 📋 No file selected     │
│                         │
│   [Upload & Analyze]    │
└─────────────────────────┘
```

### Tablet View (768px - 1024px)
```
┌─────────────────────────────────────────────┐
│           🐛 Bugsy Bug Analyzer             │
│                                             │
│    Transform bug reports into test plans    │
│         with AI-powered analysis            │
├─────────────────────────────────────────────┤
│    [📁 File Upload]  [🐙 GitHub Issue]     │
├─────────────────────────────────────────────┤
│                                             │
│        📄 Drag & Drop Area                  │
│                                             │
│   Drag your bug.txt file here or click     │
│              to select                      │
│                                             │
│            [Choose File]                    │
│                                             │
├─────────────────────────────────────────────┤
│ 📋 File Info: No file selected              │
│                                             │
│           [Upload & Analyze]                │
└─────────────────────────────────────────────┘
```

## Color Scheme Reference

```
Primary Colors:
  🔵 Blue (#007bff)     - Primary buttons, active tabs
  🟢 Green (#28a745)    - Success states, completed actions
  🔴 Red (#dc3545)      - Error states, warnings
  🟡 Orange (#fd7e14)   - Processing states, warnings

Neutral Colors:
  ⚫ Dark Gray (#343a40) - Primary text
  🔘 Medium Gray (#6c757d) - Secondary text
  ⚪ Light Gray (#f8f9fa) - Backgrounds, borders
  ⬜ White (#ffffff)    - Card backgrounds, input fields
```

This visual guide provides a comprehensive overview of the frontend interface states and responsive design considerations for the Bugsy Bug Analyzer application.