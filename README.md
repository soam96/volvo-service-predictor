# 🚘 Volvo Service Time Predictor

A Flask web application that predicts service times for Volvo cars in India using machine learning and real-time inventory management.

🌐 **Live Demo**: [https://volvo-service-predictor.onrender.com](https://volvo-service-predictor.onrender.com)

## ✨ Features

- **🤖 ML-Powered Predictions**: Accurate service time predictions based on car details and selected tasks
- **📊 Real-time Inventory**: Live parts availability checking for different Volvo models
- **🎯 Task Selection**: Interactive task selection with time estimates
- **📈 Workload Monitoring**: Real-time service center workload and queue position
- **📱 Responsive Design**: Beautiful, mobile-friendly interface
- **⚡ Fast Deployment**: Built with Flask and deployed on Render

## 🚀 Live Deployment

The application is successfully deployed and available at:

### **🌐 Primary URL**: [https://volvo-service-predictor.onrender.com](https://volvo-service-predictor.onrender.com)

### Additional Endpoints:
- **Health Check**: `https://volvo-service-predictor.onrender.com/health`
- **Test Endpoint**: `https://volvo-service-predictor.onrender.com/test`
- **Inventory API**: `https://volvo-service-predictor.onrender.com/api/inventory`
- **System Status**: `https://volvo-service-predictor.onrender.com/api/system/status`

## 🛠️ Technology Stack

### Backend
- **Python 3.11** - Core programming language
- **Flask 3.0.0** - Web framework
- **Gunicorn** - WSGI HTTP Server
- **Flask-CORS** - Cross-origin resource sharing

### Frontend
- **HTML5** - Markup
- **CSS3** - Styling with animations
- **JavaScript (ES6+)** - Client-side functionality
- **Font Awesome** - Icons

### Deployment
- **Render** - Cloud platform
- **GitHub** - Version control and CI/CD

## 📋 How to Use

1. **Visit the Application**: Go to [https://volvo-service-predictor.onrender.com](https://volvo-service-predictor.onrender.com)

2. **Fill Service Details**:
   - Enter car number plate (e.g., MH12AB1234)
   - Select car model (XC90, XC60, XC40, S90, V90, S60)
   - Choose manufacture year, fuel type, and service type
   - Select last service date

3. **Choose Service Tasks**:
   - Engine & Performance (Oil change, Air filter, Spark plugs)
   - Brakes & Safety (Brake pads, Brake fluid)
   - Wheels & Alignment (Wheel alignment, Tire rotation)
   - AC & Cooling (AC service, AC filter)
   - Electrical & Battery
   - Additional Services

4. **Get Prediction**:
   - Click "Predict Service Time"
   - View predicted service time, workload level, queue position, and parts availability

## 🔧 API Endpoints

### Main Endpoints
- `GET /` - Main application interface
- `POST /predict` - Predict service time
- `GET /api/inventory` - Get current inventory status
- `GET /api/system/status` - Get system queue information
- `GET /api/tasks` - Get available service tasks

### Utility Endpoints
- `GET /health` - Health check and system status
- `GET /test` - Test endpoint for server verification

## 🏗️ Project Structure
volvo-service-predictor/
├── app.py # Main Flask application
├── requirements.txt # Python dependencies
├── render.yaml # Render deployment configuration
├── Procfile # Process file for deployment
├── inventory.json # Parts inventory data
├── templates/
│ └── index.html # Main HTML template
├── static/
│ ├── css/
│ │ └── style.css # Styling with animations
│ └── js/
│ └── script.js # Frontend functionality
└── utils/
├── inventory_manager.py # Inventory management
├── service_center.py # Queue management
├── model_predictor.py # ML prediction logic
├── data_validator.py # Input validation
└── helpers.py # Utility functions

## 🚀 Deployment Details

### Platform: Render
- **Service Type**: Web Service
- **Environment**: Python 3.11
- **Plan**: Free Tier
- **Build Command**: `pip install -r requirements.txt`
- **Start Command**: `gunicorn app:app --bind 0.0.0.0:$PORT --timeout 120`

### Automatic Deployments
- Connected to GitHub repository
- Automatic deployments on `git push` to main branch
- Build status monitoring
- Live logs available in Render dashboard

## 🎯 Key Features Implemented

### Prediction Engine
- Rule-based service time calculation
- Task-specific time adjustments
- Workload-based scaling
- Car age and mileage considerations

### Inventory Management
- Real-time parts tracking
- Model-specific inventory
- Low stock warnings
- Service type requirements

### User Experience
- Animated form interactions
- Real-time task selection
- Progress indicators
- Responsive design
- Error handling and validation

## 🔄 Development

### Local Development
```bash
# Clone repository
git clone https://github.com/soam96/volvo-service-predictor.git
cd volvo-service-predictor

# Install dependencies
pip install -r requirements.txt

# Run locally
python app.py

# Visit http://localhost:5000
Environment Variables
PORT - Server port (default: 5000)

DEBUG - Debug mode (default: False)

📊 Performance Notes
Free Tier Limitations:

750 hours/month free usage

Automatic sleep after 15 minutes inactivity

Wakes up on new requests (30-60 second delay)

Cold Start: First request after inactivity may be slower

Auto-scaling: Handles multiple concurrent users

🤝 Contributing
Fork the repository

Create a feature branch

Make your changes

Test locally

Submit a pull request

📞 Support
For issues or questions:

Check Render deployment logs

Verify all endpoints are accessible

Test with the health check endpoint

Review browser console for frontend errors

📄 License
This project is open source and available under the MIT License.

Developed with ❤️ for Volvo Service Centers in India
