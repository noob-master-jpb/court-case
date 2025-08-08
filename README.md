# 🏛️ Court Case Management System



A modern web application for searching and managing **[Delhi High Court]** case information with automated PDF generation and professional reporting features.

## 🌟 Features

- **🔍 Case Search**: Search cases by type, number, and year
- **📊 Interactive Dashboard**: Modern UI with dark theme and responsive design
- **🤖 Automated Web Scraping**: Real-time data extraction from Delhi High Court website
- **📄 PDF Generation**: Professional PDF reports with clickable links
- **⚡ Debounced Search**: Prevents spam with intelligent form submission

## 🛠️ Tech Stack

### Backend
- **Flask** - Python web framework
- **Selenium** - Web automation and scraping
- **BeautifulSoup** - HTML parsing
- **FPDF** - PDF generation
- **SQLAlchemy** - Database ORM
- **SQLite** - Database 

### Frontend
- **Svelte** - Reactive UI framework
- **CSS Grid** - Modern layouts
- **JavaScript ES6+** - Frontend logic


## 🚀 Quick Start

### Prerequisites
```bash
Python 3.9+
Node.js 14+
Firefox/Chromium browser
```

### 1. Clone the Repository
```bash
git clone https://github.com/noob-master-jpb/court-case.git
cd court-case
```

### 2. Backend Setup
```bash
# Initialize database
python config.py
```

# Create environment file
cp .env.example .env

### 3. Frontend Setup
> **Note**: Frontend setup is optional as the application includes a pre-built frontend.

```bash
cd frontend
npm install
npm run build
cd ..
```

### 4. Run the Application
```bash
python app.py
```

Visit `http://localhost:8080` to access the application.

## 📁 Project Structure

```
court-case/
├── app.py                 # Main Flask application
├── functions.py           # Web scraping and PDF generation
├── model.py              # Database models
├── config.py             # Configuration setup
├── requirements.txt      # Python dependencies
├── clist.json           # Case types data
├── .env.example         # Environment variables template
│
├── frontend/            # Svelte frontend
│   ├── src/
│   │   ├── App.svelte          # Main application component
│   │   ├── dashboard.svelte    # Dashboard component
│   │   └── main.js            # Entry point
│   ├── public/                # Built assets
│   └── package.json           # Frontend dependencies
│
├── instance/            # Database files
└── templates/           # HTML templates

```

## ⚙️ Configuration

### Environment Variables
Create a `.env` file with the following:

```bash
SQLALCHEMY_DATABASE_URI=sqlite:///main.db
SECRET_KEY=your_super_secret_key_here
DEBUG=False
PORT=8080
HOST=0.0.0.0

```


## 🔧 API Endpoints

### POST `/data`
Search for case information
```json
{
  "case_type": "EXAMPLE",
  "case_number": "EXAMPLE",
  "case_year": "EXAMPLE"
}
```

### POST `/download_pdf`
Generate and download PDF report
```json
{
  "case_type": "EXAMPLE",
  "case_number": "EXAMPLE",
  "case_year": "EXAMPLE",
  "status": "Pending",
  "petitioner": "John Doe",
  "respondent": "Example Respondent",
}
```


## 📊 Database Schema

### Query Table
```sql
CREATE TABLE query (
    id INTEGER PRIMARY KEY,
    case_type VARCHAR(100) NOT NULL,
    case_number INTEGER NOT NULL,
    case_year INTEGER NOT NULL
);
```

### Case Table
```sql
CREATE TABLE case (
    id INTEGER PRIMARY KEY,
    query_id INTEGER REFERENCES query(id),
    case_type VARCHAR(100) NOT NULL,
    case_number INTEGER NOT NULL,
    case_year INTEGER NOT NULL,
    status VARCHAR(200),
    filing_date VARCHAR(20),
    next_date VARCHAR(20),
    last_date VARCHAR(20),
    petitioner TEXT,
    respondent TEXT,
    order_link TEXT,
    orders JSON
);
```

## 🎯 Features Overview

### Web Scraping
- Automated form filling with CAPTCHA handling
- Multi-source data extraction from Delhi High Court websites
- Robust error handling and retry mechanisms
- Support for different case types and years

### PDF Generation
- Professional formatting with sections
- Clickable links to court orders
- Automatic filename generation
- In-memory generation for serverless environments

### User Interface
- Modern Svelte-based frontend
- Responsive design with CSS Flexbox
- Dark theme with professional styling
- Real-time form validation
- Loading states and error handling

## 🔒 Security Features

- Input validation and sanitization
- SQL injection prevention with SQLAlchemy ORM
- Environment variable configuration

## 🚨 Troubleshooting

### Common Issues

**Chrome/Selenium Issues:**
```bash
sudo apt-get update
sudo apt-get install -y google-chrome-stable
```

**Database Issues:**
```bash
rm instance/main.db
python config.py
```

**Frontend Build Issues:**
```bash
cd frontend
rm -rf node_modules
npm install
npm run build
```

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 👨‍💻 Author

Created by **noob-master-jpb**


