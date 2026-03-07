# Smart Logistics Management System - Technical Terms Guide

## Project Overview

**AI Smart Logistics Management System** is an intelligent logistics platform that uses artificial intelligence to optimize delivery routes, forecast demand, predict delivery times (ETA), and manage shipments. It connects drivers, customers, and logistics managers through a real-time tracking and management system.

---

## 1. CORE SYSTEM ARCHITECTURE TERMS

### FastAPI
- **What:** A modern, fast web framework for building APIs with Python
- **Use in Project:** Used as the backend server for all logistics operations
- **Why Moderator Asks:** Understanding what technology powers the backend

### CORS (Cross-Origin Resource Sharing)
- **What:** A security protocol that allows the frontend (React) to communicate with the backend API
- **Configuration:** Allows requests from `http://localhost:5173` and `http://localhost:3000`
- **Why Moderator Asks:** Security and connection issues between frontend and backend

### SQLAlchemy (ORM)
- **What:** Object-Relational Mapping library - allows you to interact with databases using Python objects instead of SQL
- **Use:** Maps database tables to Python classes
- **Why Moderator Asks:** Understanding database operations and how data is structured

### Routers
- **What:** API endpoint groupings that organize related operations
- **Routers in Project:**
  - `auth` - Authentication/Login operations
  - `shipments` - Shipment management
  - `vehicles` - Vehicle fleet management
  - `tracking` - Real-time shipment tracking
  - `ai` - AI predictions and optimizations
  - `analytics` - Data analysis and reporting
  - `notifications` - Alert system
  - `users` - User management
  - `chatbot` - AI chat support

---

## 2. BUSINESS DOMAIN TERMS (LOGISTICS)

### Shipment
- **What:** A package or item being delivered from one location to another
- **Key Attributes:**
  - `tracking_number` - Unique ID to track the package
  - `origin` - Starting location/warehouse
  - `destination` - Final delivery location
  - `weight` - Package weight in kilograms
  - `priority` - Urgency level (Low, Normal, High, Urgent)
  - `status` - Current state
  - `estimated_delivery` - Predicted delivery time
  - `actual_delivery` - Real delivery time

### Shipment Status
- **Pending:** Shipment created but not yet assigned to a vehicle/driver
- **Assigned:** Assigned to a driver and vehicle, ready for pickup
- **In Transit:** Currently being transported from origin to destination
- **Delivered:** Successfully reached the destination
- **Cancelled:** The shipment was cancelled and won't be delivered

### Priority Levels
- **Low:** Non-urgent deliveries, can be delayed
- **Normal:** Standard deliveries
- **High:** Important deliveries, higher priority than normal
- **Urgent:** Time-critical deliveries (e.g., medical supplies, perishables)

### Tracking Number
- **What:** A unique 30-character identifier for each shipment
- **Example:** "SHP-2026-02-26-001ABC"
- **Use:** Customers and drivers use this to track packages

### Transit / In Transit
- **What:** The state when a shipment is actively being transported
- **Related Data:** Current GPS location, time in transit, estimated time remaining

### Vehicle / Fleet
- **What:** Delivery vehicles (trucks, vans, motorcycles) used for transporting shipments
- **Vehicle Types:**
  - **Truck:** Large capacity (2,000-5,000 kg), heavy goods
  - **Van:** Medium capacity (500-2,000 kg), urban/suburban deliveries
  - **Bike/Motorcycle:** Small capacity (10-50 kg), quick local deliveries

### Vehicle Metrics
- **Plate Number:** Unique vehicle identification
- **Capacity:** Maximum weight the vehicle can carry in kilograms
- **Fuel Level:** Current fuel percentage (0-100%)
- **Mileage:** Total distance traveled
- **Status:**
  - `available` - Free to take new shipments
  - `in_transit` - Currently delivering
  - `maintenance` - Out of service for repairs

### Fuel Types
- **Diesel:** Common for trucks and long-distance vehicles
- **Petrol:** Smaller vehicles and vans
- **Electric:** Eco-friendly vehicles for urban delivery

### Route / Route Optimization
- **What:** The optimal path/sequence of delivery stops
- **Related Terms:**
  - **Depot:** Starting point/warehouse
  - **Stop:** Individual delivery location
  - **Polyline:** Visual representation of the route on a map

### Driver
- **What:** Person operating the vehicle and making deliveries
- **Role-based:** Has access to shipment assignments and tracking updates

### Customer
- **What:** Person sending or receiving shipments
- **Information Stored:** Name, contact, email, phone

### Origin/Destination
- **Origin:** Source location where shipment starts (warehouse/customer location)
- **Destination:** Final delivery location
- **Stored Data:** Address + GPS coordinates (latitude, longitude)

### GPS Coordinates
- **Latitude:** North-South position (-90 to +90 degrees)
- **Longitude:** East-West position (-180 to +180 degrees)
- **Example:** New York: 40.7128°N, 74.0060°W
- **Use:** Real-time vehicle and shipment tracking

---

## 3. AI & MACHINE LEARNING TERMS

### Demand Forecasting
- **What:** AI model that predicts future shipment volumes
- **Purpose:** Help logistics managers prepare resources, allocate vehicles, and plan workforce
- **Inputs Considered:**
  - Historical shipment data
  - Day of week
  - Month/seasonality
  - Weekends vs. weekdays
  - Holiday effects
- **Model Used:** Linear Regression and Random Forest
- **Output:** Predicted shipment count for future dates

### ETA (Estimated Time of Arrival)
- **What:** AI-predicted delivery time for a shipment
- **Factors Affecting ETA:**
  - Distance to destination
  - Traffic conditions (traffic factor)
  - Weather conditions (weather factor)
  - Vehicle type (bike is slower than truck)
  - Current load weight (heavier loads = slower)
- **Model Used:** Random Forest Regressor
- **Accuracy:** Helps set customer expectations

### Route Optimization / Vehicle Routing Problem (VRP)
- **What:** AI system that finds the most efficient delivery route
- **Goals:**
  - Minimize total distance traveled
  - Reduce fuel costs
  - Minimize delivery time
  - Respect vehicle capacity limits
- **Algorithm:** Google OR-Tools (Constraint Solver)
- **Output:** Optimal sequence of delivery stops

### Machine Learning Model
- **What:** Trained algorithm that learns patterns from data
- **Models Used in Project:**
  - Linear Regression - Demand forecasting
  - Random Forest - Demand and ETA prediction
  - Constraint Solver - Route optimization
- **Training:** Models are trained on synthetic historical data
- **Persistence:** Models are saved as `.pkl` files in `ml_models/` directory

### Haversine Distance
- **What:** Formula to calculate straight-line distance between two GPS coordinates
- **Result:** Distance in kilometers (great-circle distance)
- **Use:** Creating distance matrix for route optimization

---

## 4. DATA MODEL & DATABASE TERMS

### Database Tables

#### Users Table
- **Fields:** id, username, email, hashed_password, full_name, phone, role, is_active, created_at
- **Role Types:** admin, manager, driver, customer

#### Shipments Table
- **Fields:** tracking_number, origin, destination, origin coordinates, destination coordinates, weight, status, priority, customer_id, driver_id, vehicle_id, created_at, estimated_delivery, actual_delivery
- **Keys:** customer_id and driver_id link to Users; vehicle_id links to Vehicles

#### Vehicles Table
- **Fields:** plate_number, vehicle_type, capacity, fuel_type, fuel_level, mileage, status, current location (lat/lng), assigned_driver_id, created_at

#### Tracking Updates Table
- **What:** Real-time GPS location history of shipments
- **Fields:** id, shipment_id, latitude, longitude, timestamp, status, notes
- **Use:** Shows the journey of each shipment

#### Notifications Table
- **Fields:** id, user_id, title, message, notification_type, is_read, created_at
- **Notification Types:** dispatch, delivery, delay, system

### Primary Key
- **What:** Unique identifier for each record in a table
- Used to reference records from other tables

### Foreign Key
- **What:** A field that links to another table's primary key
- **Examples:** 
  - `customer_id` in Shipments links to Users
  - `vehicle_id` in Shipments links to Vehicles

### Index
- **What:** Database optimization that speeds up searches
- **Applied to:** Frequently searched fields like `tracking_number`, `username`, `email`

---

## 5. USER & ROLE MANAGEMENT TERMS

### Authentication / Auth
- **What:** System to verify user identity and secure access
- **Method:** Username/email + password
- **Output:** Authentication tokens for API requests

### Authorization / Roles
- **Admin:** Full system access, user management, analytics
- **Manager:** Oversee operations, view analytics, manage shipments
- **Driver:** View assigned shipments, update delivery status
- **Customer:** Track their own shipments, create orders

### Hashed Password
- **What:** Encrypted password stored in database
- **Why:** Raw passwords are never stored for security

### Session/Token
- **What:** Proof that user is logged in
- **Use:** Allows API to recognize which user is making requests

---

## 6. REAL-TIME TRACKING TERMS

### Tracking Update
- **What:** A GPS location record sent periodically by a vehicle
- **Data Logged:** Latitude, longitude, timestamp, status, optional notes
- **Frequency:** Updated continuously during transit
- **Use:** Customers and managers monitor live delivery

### Real-Time Tracking
- **What:** Live updates of shipment location as vehicle moves
- **Technology:** GPS coordinates sent from vehicle to server
- **Latency:** Low delay between actual position and displayed position

### Last Known Location
- **What:** Most recent GPS coordinate received from the vehicle
- **Use:** Show current position on map

---

## 7. NOTIFICATION & ALERT TERMS

### Notification Type
- **Dispatch:** Confirmation that shipment was assigned to driver
- **Delivery:** Notification when shipment is delivered
- **Delay:** Alert when shipment will be late
- **System:** General system messages or updates

### Read/Unread
- **What:** Whether user has viewed the notification
- **Use:** Track user engagement and important messages

---

## 8. ANALYTICS & REPORTING TERMS

### Analytics / Dashboard Metrics
- **Total Shipments:** Number of shipments in system
- **Delivery Rate:** Percentage of successfully delivered shipments
- **Average Transit Time:** Mean time from pickup to delivery
- **Vehicle Utilization:** How fully loaded vehicles are
- **On-Time Delivery Rate:** Percentage delivered by estimated time
- **Fuel Efficiency:** Average distance per unit of fuel

### Key Performance Indicators (KPIs)
- **Performance Metrics** used to measure success
- **Examples:** On-time delivery %, cost per km, customer satisfaction

---

## 9. API & TECHNICAL INTEGRATION TERMS

### Endpoint
- **What:** A specific URL that handles a particular operation
- **Example:** `/shipments/{id}` - get details of a shipment
- **RESTful:** Follow REST principles (GET, POST, PUT, DELETE)

### Request/Response
- **Request:** Data sent FROM frontend/client TO backend
- **Response:** Data sent back FROM backend TO frontend
- **Format:** JSON (JavaScript Object Notation)

### Status Code
- **200:** Success
- **400:** Bad request (invalid data)
- **401:** Unauthorized (not logged in)
- **404:** Not found
- **500:** Server error

### Middleware
- **What:** Software that processes requests before reaching endpoints
- **CORS Middleware:** Handles cross-origin requests

### Payload
- **What:** The actual data being sent in a request/response
- **Example:** Shipment details, vehicle information

---

## 10. FRONTEND TERMS (ReactJS)

### Component
- **What:** Reusable UI building block
- **Examples:** Dashboard, Sidebar, ProtectedRoute, Layout

### Context (State Management)
- **What:** Global state management system
- **AuthContext:** Stores login information across the app

### Protected Route
- **What:** Pages only accessible to logged-in users
- **Examples:** Dashboard, Shipments, Vehicles (not available to anonymous users)

### Vite
- **What:** Frontend build tool that runs the React app
- **Dev Server:** Runs on `http://localhost:5173`

### Tailwind CSS
- **What:** Utility-based CSS framework for styling
- **Used for:** Dashboard layout, buttons, forms, responsive design

---

## 11. SECURITY TERMS

### JWT (JSON Web Tokens)
- **What:** Secure token format for authentication
- **Use:** Passed in `Authorization` header of API requests

### Hashing
- **What:** One-way encryption of passwords
- **Benefit:** Even admins can't recover original passwords

### HTTPS
- **What:** Secure version of HTTP with encryption
- **Importance:** Protects data during transmission

---

## 12. COMMON QUESTIONS MODERATORS MAY ASK

### "What is the difference between a Shipment and a Tracking Update?"
**Answer:** A Shipment is the order/package being delivered with fixed properties (origin, destination, weight, priority). A Tracking Update is a real-time GPS location record showing where the shipment currently is. One Shipment has many Tracking Updates.

### "How does Route Optimization work?"
**Answer:** The system uses Google OR-Tools to analyze all pending shipments and available vehicles, then calculates the most efficient sequence of delivery stops considering distance, vehicle capacity, and delivery time to minimize fuel costs and improve on-time delivery.

### "What's the difference between ETA and Estimated Delivery?"
**Answer:** ETA (Estimated Time of Arrival) is the AI-predicted time a shipment will arrive at its destination. Estimated Delivery is when the system schedules the delivery. ETA is more granular and updates based on current conditions.

### "Why is Priority important?"
**Answer:** Priority determines delivery urgency. Urgent shipments (like medical items) are assigned to vehicles first and optimized to reach faster, even if it means delaying lower-priority shipments.

### "What happens when a vehicle runs out of capacity?"
**Answer:** The system won't assign more shipments to it until capacity is freed (shipments are delivered). Route optimization ensures no vehicle exceeds its weight limit.

### "How accurate is the Demand Forecast?"
**Answer:** The Random Forest model considers seasonality, day-of-week patterns, holidays, and weekends. Accuracy improves as the system collects more real historical data to train on.

### "Can customers access real-time tracking?"
**Answer:** Yes, customers can track their shipments by tracking_number. They see real-time GPS location, current status, and updated ETA.

### "What's the difference between a Driver and a Customer?"
**Answer:** A Driver is a user role that operates vehicles and makes deliveries. A Customer is a user role that places shipment orders and receives packages. Different system access and permissions.

---

## 13. PROJECT FEATURES OVERVIEW

### Dashboard
- View key metrics (total shipments, delivery rate, pending orders)
- Monitor vehicle fleet status
- See live shipment tracking
- Access analytics and reports

### Shipment Management
- Create/update shipment orders
- Assign shipments to drivers and vehicles
- Update delivery status
- View shipment history

### Vehicle Management
- Track available vehicles
- Monitor fuel levels and mileage
- Assign drivers to vehicles
- Maintenance alerts

### Route Optimization
- Calculate optimal delivery routes
- Minimize distance and fuel costs
- Respect vehicle capacity constraints
- Provide turn-by-turn directions (mapped)

### Demand Forecasting
- Predict future shipment volumes
- Plan resource allocation
- Seasonal demand analysis
- Historical trend visualization

### Real-Time Tracking
- Live GPS location of active shipments
- Tracking history with timestamps
- Delivery progress updates
- Alert on delays

### Notifications
- Real-time alerts to users
- Dispatch confirmations
- Delivery confirmations
- Delay warnings

### Analytics & Reporting
- Performance metrics (on-time delivery %)
- KPI dashboard
- Vehicle utilization reports
- Cost analysis

### AI Chatbot
- Customer support
- Shipment inquiries
- FAQ answers
- Order assistance

---

## 14. QUICK REFERENCE GLOSSARY

| Term | Definition |
|------|-----------|
| **API** | Application Programming Interface - way frontend talks to backend |
| **Backend** | Server-side code (Python/FastAPI) |
| **Frontend** | Client-side code (React/JavaScript) |
| **Database** | Where all data is stored (SQLAlchemy) |
| **Shipment** | Package being delivered |
| **Tracking Number** | Unique ID for shipment |
| **Vehicle** | Truck, van, or bike for delivery |
| **Driver** | Person operating vehicle |
| **Route** | Sequence of delivery stops |
| **ETA** | Estimated time of arrival |
| **In Transit** | Currently being transported |
| **Delivered** | Successfully arrived at destination |
| **GPS** | Global Positioning System coordinates |
| **Real-time** | Live, immediate updates |
| **AI** | Artificial Intelligence for predictions |
| **ML Model** | Machine Learning algorithm |
| **Optimization** | Finding the best solution |
| **CORS** | Security protocol for cross-origin requests |
| **Token** | Authentication credential |
| **Notification** | Alert message to user |

---

**Last Updated:** February 26, 2026
**Project:** AI Smart Logistics Management System v1.0.0
