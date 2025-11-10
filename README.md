# SaveTogether - Smart Community Savings Platform

SaveTogether is a full-stack web application that enables friends and family to create shared savings goals, track collective progress, and achieve financial objectives together.

## Features

### Core Features
- **User Authentication**: Secure registration and login system
- **Group Management**: Create and join savings groups with invite codes
- **Progress Tracking**: Visual dashboards with Chart.js integration
- **Contributions**: Manual contribution logging with real-time updates
- **Notifications**: In-app notifications for milestones and updates
- **Mobile Responsive**: Mobile-first design with Bootstrap 5

### Premium Features (19 MAD/month)
- **Data Export**: CSV export functionality for group data
- **Automated Reminders**: Recurring contribution reminders
- **Advanced Analytics**: Enhanced progress tracking and insights

## Tech Stack

- **Backend**: Flask (Python) with Flask-Login for authentication
- **Database**: SQLite with SQLAlchemy-style queries
- **Frontend**: HTML5, CSS3, JavaScript with Bootstrap 5
- **Charts**: Chart.js for data visualization
- **Icons**: Font Awesome 6
- **Security**: Password hashing with Werkzeug

## Installation & Setup

### Prerequisites
- Python 3.7 or higher
- pip (Python package manager)

### Step 1: Clone the Repository
```bash
git clone <repository-url>
cd savetogether
```

### Step 2: Install Dependencies
```bash
pip install -r requirements.txt
```

### Step 3: Run the Application
```bash
python app.py
```

The application will be available at `http://localhost:5000`

## Project Structure

```
savetogether/
├── app.py                 # Main Flask application
├── requirements.txt       # Python dependencies
├── README.md             # Project documentation
├── templates/            # HTML templates
│   ├── base.html         # Base template with navigation
│   ├── index.html        # Landing page
│   ├── login.html        # Login page
│   ├── register.html     # Registration page
│   ├── dashboard.html    # User dashboard
│   ├── create_group.html # Group creation form
│   ├── join_group.html   # Group joining form
│   ├── group_detail.html # Group details and progress
│   ├── contribute.html   # Contribution form
│   ├── pricing.html      # Pricing page
│   └── settings.html     # User settings
├── static/               # Static assets
│   ├── style.css         # Custom CSS styles
│   ├── app.js           # Main JavaScript file
│   └── sw.js            # Service worker for PWA
└── savetogether.db      # SQLite database (created automatically)
```

## Database Schema

### Users Table
- `id`: Primary key
- `username`: Unique username
- `email`: Unique email address
- `password_hash`: Hashed password
- `is_premium`: Premium subscription status
- `created_at`: Account creation timestamp

### Groups Table
- `id`: Primary key
- `name`: Group name
- `description`: Group description
- `target_amount`: Savings target amount
- `deadline`: Target completion date
- `created_by`: Creator user ID
- `invite_code`: Unique invite code
- `created_at`: Group creation timestamp

### Group Members Table
- `id`: Primary key
- `group_id`: Foreign key to groups
- `user_id`: Foreign key to users
- `joined_at`: Membership timestamp

### Contributions Table
- `id`: Primary key
- `group_id`: Foreign key to groups
- `user_id`: Foreign key to users
- `amount`: Contribution amount
- `description`: Contribution description
- `contribution_date`: Contribution timestamp

### Notifications Table
- `id`: Primary key
- `user_id`: Foreign key to users
- `group_id`: Foreign key to groups
- `message`: Notification message
- `is_read`: Read status
- `created_at`: Notification timestamp

## Usage Guide

### Getting Started
1. **Register**: Create a new account on the landing page
2. **Login**: Access your dashboard with your credentials
3. **Create Group**: Start a new savings group or join an existing one
4. **Contribute**: Add contributions to track progress
5. **Monitor**: View progress charts and group statistics

### Creating a Group
1. Navigate to "Create Group" from the dashboard
2. Fill in group details (name, description, target amount, deadline)
3. Share the generated invite code with friends/family
4. Start contributing to reach your shared goal

### Joining a Group
1. Get an invite code from a group creator
2. Use "Join Group" feature to enter the code
3. Become a member and start contributing

### Premium Features
- **Upgrade**: Visit the pricing page to upgrade to Premium
- **Export Data**: Download group data as CSV files
- **Automated Reminders**: Set up recurring contribution reminders

## API Endpoints

### Authentication
- `POST /register` - User registration
- `POST /login` - User login
- `GET /logout` - User logout

### Groups
- `GET /groups/create` - Group creation form
- `POST /groups/create` - Create new group
- `GET /groups/join` - Group joining form
- `POST /groups/join` - Join group with invite code
- `GET /groups/<id>` - Group details and progress

### Contributions
- `GET /groups/<id>/contribute` - Contribution form
- `POST /groups/<id>/contribute` - Add contribution

### API Data
- `GET /api/group_progress/<id>` - JSON progress data for charts

## Security Features

- **Password Hashing**: Secure password storage with Werkzeug
- **Session Management**: Flask-Login for secure sessions
- **Input Validation**: Form validation and sanitization
- **CSRF Protection**: Cross-site request forgery protection
- **Access Control**: Group membership verification

## Mobile Optimization

- **Responsive Design**: Mobile-first Bootstrap 5 layout
- **Touch-Friendly**: Optimized for touch interactions
- **Progressive Web App**: Service worker for offline functionality
- **Fast Loading**: Optimized assets and caching

## Customization

### Styling
- Modify `static/style.css` for custom styling
- Update CSS variables in `:root` for color scheme changes
- Customize Bootstrap components as needed

### Features
- Add new routes in `app.py` for additional functionality
- Extend database schema for new features
- Modify templates for UI changes

## Deployment

### Production Setup
1. Set `app.debug = False` in `app.py`
2. Use a production WSGI server (e.g., Gunicorn)
3. Set up a reverse proxy (e.g., Nginx)
4. Configure environment variables for secrets
5. Use a production database (PostgreSQL recommended)

### Environment Variables
```bash
export FLASK_SECRET_KEY="your-secret-key"
export DATABASE_URL="your-database-url"
```

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Support

For support and questions:
- Create an issue in the repository
- Contact the development team
- Check the documentation

## Roadmap

### Planned Features
- **Payment Integration**: Real payment processing for Premium subscriptions
- **Advanced Analytics**: More detailed progress tracking
- **Social Features**: Comments and discussions within groups
- **Mobile App**: Native mobile applications
- **Integration**: Banking API integration for automatic contributions
- **Multi-language**: Internationalization support

---

**SaveTogether** - Making financial goals achievable together! 💰🤝
