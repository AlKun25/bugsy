# Frontend Documentation

## Overview

This frontend provides a modern, responsive web interface for the Bugsy bug analysis tool. It supports two input methods for analyzing bugs and generating test plans.

## Project Structure

```
frontend/
├── templates/
│   └── index.html          # Main HTML template with tabbed interface
├── static/
│   ├── css/                # CSS stylesheets (embedded in HTML)
│   ├── js/                 # JavaScript files (embedded in HTML)
│   └── images/             # Static images
└── README.md               # This documentation
```

## Features

### Dual Input Modes

The frontend supports two distinct input methods:

#### 1. 📁 File Upload Mode
- **Purpose**: Direct upload of bug report files
- **Supported Format**: `.txt` files (specifically `bug.txt`)
- **Features**:
  - Drag-and-drop file upload
  - File selection via click
  - Real-time file validation
  - Upload progress feedback
  - File size and type validation

#### 2. 🐙 GitHub Issue Mode
- **Purpose**: Fetch and analyze GitHub issues directly
- **Input Requirements**:
  - GitHub repository URL (e.g., `https://github.com/owner/repo`)
  - Issue number (e.g., `123`)
- **Features**:
  - Automatic GitHub API integration
  - Real-time issue fetching
  - Comprehensive issue data extraction
  - Error handling for invalid URLs/issues

## User Interface Components

### Tab Navigation
- **Design**: Clean, modern tab interface
- **Functionality**: Smooth switching between input modes
- **Styling**: Responsive design with hover effects

### File Upload Area
- **Visual**: Dashed border drop zone
- **Interaction**: Click or drag-and-drop
- **Feedback**: Visual indicators for file selection and upload status

### GitHub Form
- **Fields**:
  - Repository URL input with placeholder
  - Issue number input with validation
- **Validation**: Real-time input validation
- **Submission**: AJAX form submission with progress feedback

### Results Display
- **Success State**: Download link for generated test plan
- **Error State**: Clear error messages with troubleshooting hints
- **Loading State**: Progress indicators during processing

## Technical Implementation

### Frontend Technologies
- **HTML5**: Semantic markup with modern form elements
- **CSS3**: Flexbox layout, transitions, and responsive design
- **Vanilla JavaScript**: No external dependencies for maximum compatibility

### Key JavaScript Functions
- `switchTab(tabName)`: Handles tab navigation
- `handleFileUpload()`: Manages file upload workflow
- `handleGitHubSubmit()`: Processes GitHub issue form submission
- `showResult()`: Displays processing results
- `showError()`: Handles error display

### API Integration
- **File Upload Endpoint**: `POST /upload`
- **GitHub Issue Endpoint**: `POST /github-issue`
- **Response Format**: JSON with download links or error messages

## Styling Guidelines

### Color Scheme
- **Primary**: Blue tones for interactive elements
- **Success**: Green for successful operations
- **Error**: Red for error states
- **Neutral**: Gray tones for text and borders

### Typography
- **Font Family**: System fonts for optimal performance
- **Hierarchy**: Clear heading and body text distinction
- **Readability**: Adequate line spacing and contrast

### Responsive Design
- **Mobile-First**: Optimized for mobile devices
- **Breakpoints**: Responsive layout for tablets and desktops
- **Touch-Friendly**: Adequate touch targets for mobile interaction

## Usage Examples

### File Upload Workflow
1. User selects "📁 File Upload" tab
2. Drags `bug.txt` file to upload area or clicks to select
3. File is validated and uploaded automatically
4. Processing begins with visual feedback
5. Download link appears for `test_plan.txt`

### GitHub Issue Workflow
1. User selects "🐙 GitHub Issue" tab
2. Enters repository URL: `https://github.com/facebook/react`
3. Enters issue number: `25123`
4. Clicks "Analyze GitHub Issue" button
5. System fetches issue data via GitHub API
6. Processing begins with comprehensive issue analysis
7. Download link appears for generated test plan

## Error Handling

### File Upload Errors
- Invalid file type
- File size too large
- Network connectivity issues
- Server processing errors

### GitHub Integration Errors
- Invalid repository URL format
- Repository not found (404)
- Issue not found
- GitHub API rate limiting
- Network connectivity issues

## Performance Considerations

- **Lazy Loading**: Resources loaded only when needed
- **Minimal Dependencies**: No external JavaScript libraries
- **Optimized Assets**: Embedded CSS and JS for reduced HTTP requests
- **Responsive Images**: Scalable vector graphics where possible

## Browser Compatibility

- **Modern Browsers**: Chrome 70+, Firefox 65+, Safari 12+, Edge 79+
- **Features Used**: Fetch API, CSS Grid, Flexbox, ES6+
- **Fallbacks**: Graceful degradation for older browsers

## Future Enhancements

- [ ] Dark mode toggle
- [ ] Multiple file upload support
- [ ] Real-time processing progress
- [ ] GitHub authentication for private repositories
- [ ] Issue search and filtering
- [ ] Export options (PDF, JSON, etc.)
- [ ] Batch processing capabilities