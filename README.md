**Real Estate Property Management System**

A web-based Real Estate Property Management System that helps manage property information, tenants, owners, agents, rentals, payments, and maintenance records efficiently. The system allows users to store, manage, and analyze real estate data through an interactive web interface.

This project demonstrates the practical implementation of **Database Management System (DBMS)** concepts integrated with modern web development technologies.


 **Features**

* Manage property owners
* Manage property locations
* Add and manage properties
* Manage tenants
* Manage real estate agents
* Create and manage rental records
* Record property payments
* Track maintenance requests
* Edit and delete records for all entities
* Run predefined SQL queries for data analysis
* View relationships between owners, tenants, properties, and payments


 **Tech Stack**

 Frontend

* HTML
* CSS
* JavaScript

 Backend

* Python
* Flask

Database

* SQLite


 **Database Design**

The system uses a relational database structure consisting of multiple interconnected tables.

 Owners Table

* id (Primary Key)
* name

 Locations Table

* id (Primary Key)
* city

 Properties Table

* id (Primary Key)
* name
* owner_id (Foreign Key)
* location_id (Foreign Key)

 Tenants Table

* id (Primary Key)
* name

 Agents Table

* id (Primary Key)
* name

 Rentals Table

* id (Primary Key)
* property_id (Foreign Key)
* tenant_id (Foreign Key)

 Payments Table

* id (Primary Key)
* rental_id (Foreign Key)
* amount

 Maintenance Table

* id (Primary Key)
* property_id (Foreign Key)
* description


 **System Architecture**

The system follows a **three-layer architecture**:

 Presentation Layer

Frontend developed using **HTML, CSS, and JavaScript** to provide an interactive user interface.

 Application Layer

Backend implemented using **Python Flask**, which handles application logic, routing, and database operations.

 Database Layer

**SQLite** is used to store all system data including owners, tenants, properties, rentals, payments, and maintenance records.



 **Project Structure**

RealEstateManagementSystem


├── app.py
├── database.db
│
├── templates
│   ├── base.html
│   ├── owners.html
│   ├── locations.html
│   ├── properties.html
│   ├── tenants.html
│   ├── agents.html
│   ├── rentals.html
│   ├── payments.html
│   ├── maintenance.html
│   ├── queries.html
│   ├── edit_owner.html
│   ├── edit_location.html
│   ├── edit_property.html
│   ├── edit_tenant.html
│   ├── edit_agent.html
│   ├── edit_rental.html
│   ├── edit_payment.html
│   └── edit_maintenance.html
│
├── static
│   └── style.css
│
└── README.md



 **Installation**

 Clone the repository

[Link Text](https://github.com/bhavyasrimacharla8-ctrl/Real-Estate-property-management/)

 Navigate to the project folder

 Install dependencies

 Run the application

 Open the browser

[link Text](http://127.0.0.1:5000/)


 **How It Works**

* Users open the web application through the browser.
* The system provides different modules such as Owners, Locations, Properties, Tenants, Agents, Rentals, Payments, and Maintenance.
* Users can add, edit, and delete records for each entity.
* The system stores all information in the **SQLite database**.
* The **Run Queries** page allows users to execute predefined SQL queries to analyze the data.
* The application demonstrates relationships between entities using foreign keys.


 **Learning Outcomes**

This project demonstrates:

* Database design and normalization
* CRUD operations (Create, Read, Update, Delete)
* SQL queries and joins
* Web application development using Flask
* Integration of frontend and backend technologies
* Implementation of relational database concepts



**This project is developed for educational purposes as part of a course project.**
