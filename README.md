🥕 AGRIHUB: SMART AGRICULTURAL MARKETPLACE


📝 PROJECT OVERVIEW

AgriHub is a B2C (Business-to-Consumer) e-commerce marketplace built
using the Django framework. The project's core mission is to eliminate the
agricultural supply chain middlemen, directly connecting verified local
Farmers with end consumers.

This platform demonstrates robust full-stack development skills, complex 
Database Integration, and professional Role-Based Access Control (RBAC)
to ensure a transparent and efficient marketplace.




✨ KEY FEATURES 


The following features showcase the complexity and business logic
implemented:

Role-Based Access Control (RBAC): Users are authenticated as either
a Buyer/Consumer or a Verified Producer (Farmer), offering two entirely 
different user experiences.

Dedicated Farmer Dashboard: A unique YIELD MANAGER section allows Farmers
to perform full CRUD (Create, Read, Update, Delete) operations on their
inventory in real-time.

End-to-End E-commerce Flow: Features include a dynamic shopping cart,
order quantity updates, detailed checkout, and order history tracking.

Status-Based Order Tracking: Orders move through defined stages
(Pending, Accepted, Packed, Shipped), which are managed by the 
Administrator from the backend.

Responsive UI/UX: Built with Bootstrap and custom CSS for a professional,
mobile-friendly design.

Secure Authentication: Utilizes Django's built-in authentication system
for secure user management.




📸 PROJECT VISUALS





🚀 GETTING STARTED (INSTALLATION GUIDE) 


Follow these steps to set up and run the project locally.

Prerequisites
Python 3.8+
Git
pip (Python package installer)




INSTALLATION


1.Clone the Repository:
git clone https://github.com/AmaiTechPro/AgriHubProject

2.Create and Activate Virtual Environment:
python -m venv venv
source venv/bin/activate  # On Windows, use: venv\Scripts\activate

3.Install Dependencies:
pip install -r requirements.txt

4.Database Setup:
python manage.py makemigrations
python manage.py migrate

5.Create Superuser (Admin Access):
python manage.py createsuperuser




USAGE


1.Run the Development Server:
python manage.py runserver

2.Access the Site: Open your web browser and navigate to
http://127.0.0.1:8000/.




🛠️ BUILT WITH


Backend Framework: Django (Python)

Database: SQLite (Default for development)

Frontend: HTML5, CSS3, JavaScript

Styling: Bootstrap 5



📧 CONTACT

Brian David Amai

LinkedIn: https://www.linkedin.com/in/brian-tech-networkingpro/

Email: amaibrian2@gmail.com

