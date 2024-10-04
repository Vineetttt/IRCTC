# Railway Management System API

This API simulates a railway management system, allowing users to check train availability, book seats, and manage user registrations. It features role-based access for users and admins.

## Table of Contents
- [Features](#features)
- [Technologies Used](#technologies-used)
- [Setup Instructions](#setup-instructions)

## Features
- User registration and login
- Admin functionalities to add and manage trains
- Check availability of seats between stations
- Book seats on trains
- Get details of specific bookings

## Technologies Used
- **Programming Language**: Python
- **Web Framework**: Flask
- **Database**: MySQL
- **Authentication**: JWT (JSON Web Tokens)
- **Password Hashing**: bcrypt

## Setup Instructions

### Prerequisites
- Python 3.x
- MySQL server running
- Virtual environment (optional but recommended)

### Installation Steps
1. **Clone the repository**:
   ```bash
   git clone https://your-repo-url.git
   cd your-repo-directory
   
2. **Set up Environment Variables:**
   ```bash
   export MYSQL_USER= <YOUR_USERNAME>
   export MYSQL_PASSWORD= <<YOUR_SQL_PASSWORD>
   export MYSQL_DB=irctc
   export MYSQL_HOST=localhost
   export MYSQL_PORT=3306
   export API_KEY='1A2b3C4d5E6f7G8h9I0j'
   export SECRET_KEY='1234567890abcdef'

  Note that the API_KEY and SECRET_KEY varibales are dummy and just for implementation purpose.

