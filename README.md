# Railway Management System API

This API simulates a railway management system, allowing users to check train availability, book seats, and manage user registrations. It features role-based access for users and admins.

## Table of Contents
- [Features](#features)
- [Technologies Used](#technologies-used)
- [Setup Instructions](#setup-instructions)
- [Assumptions](#assumptions)
- [API Documentation](https://docs.google.com/document/d/104uL0bqvzmJ942jmBXius91OBYbPcn07UYp8BEpL8QA/edit?usp=sharing)

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

### Installation Steps
1. **Clone the repository**:
   ```bash
   git clone https://your-repo-url.git
   cd your-repo-directory
   
2. **Set up Environment Variables:**
   ```bash
   export MYSQL_USER= YOUR_SQL_USERNAME
   export MYSQL_PASSWORD= YOUR_SQL_PASSWORD
   export MYSQL_DB=irctc
   export MYSQL_HOST=localhost
   export MYSQL_PORT=3306
   export API_KEY='1A2b3C4d5E6f7G8h9I0j'
   export SECRET_KEY='1234567890abcdef'

  Note that the API_KEY and SECRET_KEY varibales are dummy and just for implementation purpose.

3. **Install required packages:**
     ```bash
     pip3 install -r requirements.txt

4. **Run the application:**
   ```bash
   python3 app.py

The tables will be created automatically upon running the application for the first time.

### Assumptions
- Only the endpoints specified in the requirements are implemented.
- Basic CRUD operations for each role can be added later if necessary.
- Users and admins are managed in the same table using a role column.
- Each booking is connected to a user and a specific train.
- Train information could include more details like departure and arrival times, but is not included in this implementation.
- All functionalities are managed within a single database without sharding or distribution.
