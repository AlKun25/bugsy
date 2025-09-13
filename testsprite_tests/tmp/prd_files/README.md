# 🐛 Bugsy - AI-Powered Bug Analysis Tool

> Transform bug reports into comprehensive test plans with intelligent analysis and recommendations

## 🎯 Overview

Bugsy is a sophisticated bug analysis tool that leverages AI to convert bug reports into detailed, actionable test plans. It supports both direct file uploads and GitHub issue integration, providing a modern web interface for seamless bug analysis workflows.

## ✨ Key Features

- **🔄 Dual Input Modes**: Support for both file uploads and GitHub issue integration
- **🤖 AI-Powered Analysis**: Intelligent bug report processing with comprehensive test case generation
- **🎨 Modern Web Interface**: Responsive, user-friendly design with real-time feedback
- **📱 Cross-Platform**: Works on desktop, tablet, and mobile devices
- **🔗 GitHub Integration**: Direct analysis of GitHub issues with automatic data fetching
- **📊 Comprehensive Output**: Detailed test plans with 16+ test cases per analysis

## 🏗️ Project Structure

```
bugsy/
├── frontend/                    # Frontend assets and documentation
│   ├── templates/
│   │   └── index.html          # Main web interface
│   ├── static/                 # CSS, JS, and image assets
│   ├── README.md              # Frontend documentation
│   └── INTERFACE_GUIDE.md     # Visual interface guide
│
├── GetTestStripePlan/          # Core analysis engine
│   ├── bug_solver.py          # Main bug analysis logic
│   ├── prompt.txt             # AI analysis prompt template
│   └── test_plan.txt          # Sample output format
│
├── app.py                     # Flask web server
├── main.py                   # CLI interface
└── README.md                 # This file
```

## 🚀 Quick Start

### Prerequisites

- Docker Desktop installed and running
- Docker Compose (included with Docker Desktop)
- Git for cloning the repository

### 🐳 Docker Installation (Recommended)

```bash
# Clone the repository
git clone <repository-url>
cd bugsy

# Set up environment variables
cp .env.example .env
# Edit .env and add your actual API keys:
# OPENAI_API_KEY=your_openai_api_key_here
# TESTSPRITE_API_KEY=your_testsprite_api_key_here

# Build and run with Docker
docker-compose up --build
```

### 🐍 Manual Installation (Alternative)

```bash
# Clone the repository
git clone <repository-url>
cd bugsy

# Install dependencies
pip install flask requests openai python-dotenv python-docx pydantic

# Set up environment variables
cp .env.example .env
# Edit .env and add your API keys

# Run the application
python app.py
```

### Access the Application

- **Local**: http://127.0.0.1:5000
- **Network**: http://[your-ip]:5000

### 🐳 Docker Commands

```bash
# Start services in background
docker-compose up -d

# Stop services
docker-compose down

# View logs
docker-compose logs -f

# Rebuild containers
docker-compose up --build

# Remove everything (containers, networks, volumes)
docker-compose down -v --remove-orphans
```

## 🖥️ Frontend Interface

### Main Interface Layout

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
```

### 📁 File Upload Mode

```
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
└─────────────────────────────────────────────────────────────────┘
```

### 🐙 GitHub Issue Mode

```
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
└─────────────────────────────────────────────────────────────────┘
```

### ✅ Success State

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
```

## 🔄 Usage Workflows

### Method 1: File Upload

1. **Navigate** to http://127.0.0.1:5000
2. **Select** the "📁 File Upload" tab (default)
3. **Upload** your `bug.txt` file via drag-and-drop or file selection
4. **Click** "Upload & Analyze" to process the file
5. **Download** the generated `test_plan.txt` file

### Method 2: GitHub Issue Analysis

1. **Navigate** to http://127.0.0.1:5000
2. **Select** the "🐙 GitHub Issue" tab
3. **Enter** the GitHub repository URL (e.g., `https://github.com/facebook/react`)
4. **Enter** the issue number (e.g., `25123`)
5. **Click** "Analyze GitHub Issue" to fetch and process the issue
6. **Download** the generated test plan

## 🛠️ API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| `GET` | `/` | Main web interface |
| `POST` | `/upload` | File upload processing |
| `POST` | `/github-issue` | GitHub issue analysis |
| `GET` | `/download/<filename>` | Download generated files |

## 🔧 Technical Stack

### Backend
- **Flask**: Web framework
- **Python 3.12**: Core language
- **OpenAI**: AI-powered bug analysis
- **Requests**: HTTP library for GitHub API
- **python-dotenv**: Environment variable management
- **python-docx**: Document processing
- **Pydantic**: Data validation

### Frontend
- **HTML5**: Semantic markup
- **CSS3**: Modern styling with Flexbox/Grid
- **Vanilla JavaScript**: No external dependencies
- **Responsive Design**: Mobile-first approach

### 🐳 Docker Infrastructure
- **Multi-stage Build**: Optimized Python 3.12-slim image
- **Health Checks**: Container monitoring and restart policies
- **Volume Mounts**: Persistent data storage
- **Network Isolation**: Secure container networking
- **Environment Management**: Secure API key handling

## 🐳 Docker Setup Details

### Container Architecture

- **Base Image**: `python:3.12-slim` for optimal size and security
- **Working Directory**: `/app` inside container
- **Exposed Port**: `5000` (Flask development server)
- **Health Check**: HTTP endpoint monitoring with automatic restarts
- **Network**: Custom bridge network `bugsy_bugsy-network`

### Volume Mounts

```yaml
volumes:
  - ./get_test_stripe_plan:/app/get_test_stripe_plan  # Test data
  - ./templates:/app/templates                        # HTML templates
```

### Environment Variables

| Variable | Description | Required |
|----------|-------------|----------|
| `OPENAI_API_KEY` | OpenAI API key for AI analysis | Yes |
| `TESTSPRITE_API_KEY` | TestSprite API key | Yes |
| `FLASK_ENV` | Flask environment (development/production) | No |
| `PYTHONUNBUFFERED` | Python output buffering control | No |

### Docker Files Overview

- **`Dockerfile`**: Multi-stage build configuration
- **`docker-compose.yml`**: Service orchestration and networking
- **`.dockerignore`**: Build context optimization
- **`.env`**: Environment variables (create from `.env.example`)
- **`DOCKER_README.md`**: Detailed Docker documentation

### Troubleshooting

#### Docker Daemon Issues
```bash
# Check if Docker is running
docker --version
docker info

# Start Docker Desktop (macOS/Windows)
# Or start Docker service (Linux)
sudo systemctl start docker
```

#### Container Issues
```bash
# Check container status
docker-compose ps

# View detailed logs
docker-compose logs bugsy-flask-app

# Restart specific service
docker-compose restart bugsy-flask-app

# Rebuild without cache
docker-compose build --no-cache
```

#### Network Issues
```bash
# Check network connectivity
docker network ls
docker network inspect bugsy_bugsy-network

# Test container connectivity
docker-compose exec bugsy-flask-app curl http://localhost:5000/health
```

## 📊 Sample Output

Bugsy generates comprehensive test plans including:

- **Functional Test Cases**: Core functionality validation
- **Edge Case Testing**: Boundary condition analysis
- **Error Handling**: Exception and error scenarios
- **Integration Testing**: Component interaction validation
- **Performance Testing**: Load and stress test recommendations
- **Security Testing**: Vulnerability assessment guidelines

## 🔒 Security Features

- **Input Validation**: File type and size restrictions
- **API Rate Limiting**: GitHub API usage optimization
- **Error Sanitization**: Safe error message handling
- **Environment Variables**: Secure API key management via .env files
- **Container Isolation**: Docker security boundaries
- **No Secrets in Images**: API keys excluded from Docker builds
- **Health Monitoring**: Container health checks and automatic restarts

## 📱 Responsive Design

The interface adapts to different screen sizes:

- **Mobile** (< 768px): Single-column layout
- **Tablet** (768px - 1024px): Optimized touch interface
- **Desktop** (> 1024px): Full-width layout with optimal spacing

## 🚨 Error Handling

### File Upload Errors
- Invalid file type notifications
- File size limit warnings
- Network connectivity issues
- Processing timeout handling

### GitHub Integration Errors
- Repository not found (404)
- Issue not found notifications
- API rate limit warnings
- Invalid URL format alerts

## 🔮 Future Enhancements

- [ ] **Dark Mode**: Toggle between light and dark themes
- [ ] **Batch Processing**: Multiple file/issue analysis
- [ ] **Real-time Progress**: WebSocket-based updates
- [ ] **GitHub Auth**: Private repository support
- [ ] **Export Options**: PDF, JSON, CSV formats
- [ ] **Analytics Dashboard**: Usage insights and statistics

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🆘 Support

For support, please:
1. Check the [Frontend Documentation](frontend/README.md)
2. Review the [Interface Guide](frontend/INTERFACE_GUIDE.md)
3. Open an issue on GitHub

---

**Made with ❤️ for better bug analysis and testing workflows**