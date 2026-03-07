# Dashboard & UI Terms Guide

## MAIN DASHBOARD ELEMENTS & TERMS

### Dashboard
- **What:** Main control center/home page after login
- **Shows:** Overview of all operations, key metrics, recent activity
- **Purpose:** Quick status check for entire logistics operation

### Sidebar
- **What:** Left navigation menu
- **Contains:** Links to different sections (Shipments, Vehicles, Tracking, Analytics, etc.)
- **Purpose:** Easy navigation between different parts of the system

### Widgets / Cards
- **What:** Individual boxes/panels showing specific information
- **Examples:** "Total Shipments Today", "Active Vehicles", "On-Time Delivery %"
- **Interactive:** Can click for more details

### KPI (Key Performance Indicators)
- **What:** Important metrics that measure system performance
- **Examples:**  
  - On-time delivery rate: 96%
  - Average delivery time: 2.5 hours
  - Vehicle utilization: 85%
  - Customer satisfaction: 4.8/5

### Real-Time Map
- **What:** Interactive map showing live vehicle locations
- **Shows:** Shipment locations, delivery routes, traffic
- **Updates:** Continuously as vehicles move
- **Markers:** Different colors for different statuses

---

## SHIPMENTS PAGE TERMS

### Shipment List
- **What:** Table showing all shipments with key info
- **Columns:** Tracking number, origin, destination, status, priority, ETA, driver, vehicle
- **Sortable:** Click column headers to sort by date, status, priority
- **Filterable:** Filter by status, priority, date range

### Create Shipment
- **What:** Form to add new shipment to system
- **Required Fields:**
  - Origin address (pickup location)
  - Destination address (delivery location)
  - Weight
  - Priority level
  - Customer information

### Shipment Details View
- **What:** Full page showing all shipment information
- **Shows:**
  - Tracking number
  - Origin & destination with coordinates
  - Current status
  - Assigned driver & vehicle
  - Timeline (created, in-transit, delivered)
  - Real-time location on map
  - Tracking history (all updates)

### Search
- **What:** Find specific shipments
- **Search By:** Tracking number, customer name, or address
- **Results:** Instant matching shipments

### Bulk Actions
- **What:** Operations on multiple shipments at once
- **Examples:** Assign to vehicle, change priority, cancel shipment

---

## VEHICLES PAGE TERMS

### Vehicle Fleet
- **What:** List of all vehicles in the system
- **Shows:** Plate number, vehicle type, capacity, fuel level, status, current location, assigned driver

### Vehicle Status
- **Available:** Ready for new assignments
- **In Transit:** Currently delivering shipments
- **Maintenance:** Out of service (being repaired)
- **Status Color Coding:**
  - 🟢 Green = Available
  - 🟡 Yellow = In Transit
  - 🔴 Red = Maintenance

### Fuel Level
- **What:** Current fuel percentage
- **Display:** Progress bar (0-100%)
- **Alert:** Warning when below 15%
- **Purpose:** Know when vehicle needs refueling

### Vehicle Details
- **Plate Number:** Vehicle registration
- **Type:** Truck, Van, Bike
- **Capacity:** Max weight in kg
- **Mileage:** Total distance traveled
- **Fuel Type:** Diesel, Petrol, Electric
- **Driver:** Currently assigned driver
- **Current Location:** GPS coordinates

### Vehicle Assignment
- **What:** Assigning driver to vehicle
- **Shows:** Who is driving what
- **Updates:** When driver starts/ends shift

### Route Map
- **What:** Visual line showing vehicle's planned delivery route
- **Stops:** Each delivery point marked
- **Order:** Sequential delivery order
- **ETA for Each:** Time to arrive at each stop

---

## TRACKING PAGE TERMS

### Live Tracking
- **What:** Real-time visualization of shipment in transit
- **Shows:** Current GPS location on interactive map
- **Updates:** Every 1-2 minutes as vehicle moves

### Tracking History
- **What:** List of all location updates for a shipment
- **Shows:** Timestamp, latitude, longitude, status at each point
- **Useful For:** Seeing entire journey path

### Tracking Timeline
- **What:** Visual representation of shipment progress
- **Events:**
  - Pickup (picked up from origin)
  - In Transit (traveling)
  - Out for Delivery (arrived at destination area)
  - Delivered (successfully delivered)

### GPS Breadcrumb Trail
- **What:** Line/path showing everywhere vehicle has been
- **Visual:** Continuous line from origin to current location
- **Purpose:** See actual route taken (may differ from planned)

### Last Update
- **What:** Most recent timestamp of location
- **Shows:** "Last updated 2 minutes ago"
- **Important:** Know how fresh the data is

### Geofencing
- **What:** Virtual boundary around delivery area
- **Trigger:** Alert when vehicle enters/exits geofence
- **Use:** Know when driver is near delivery location

---

## ANALYTICS PAGE TERMS

### Dashboard View
- **What:** Single page with all important metrics at a glance
- **Shows:** Charts, graphs, and number cards

### Reports
- **What:** Historical analysis and trends
- **Types:**
  - Daily summary
  - Weekly performance
  - Monthly trends
  - Seasonal analysis

### Metrics / Indicators
- **Total Shipments:** Count of all shipments (all-time or date range)
- **Pending:** Shipments waiting assignment (percent or count)
- **In Transit:** Currently being delivered
- **Delivered:** Successfully completed
- **Cancelled:** Orders that were cancelled
- **On-Time %:** Percentage delivered by ETA
- **Late %:** Percentage delivered after ETA
- **Average Delivery Time:** Mean hours from origin to destination
- **Vehicle Utilization:** Average percentage of vehicle capacity used
- **Routes/Day:** Average number of delivery routes per day
- **Cost per Delivery:** Average cost per shipment
- **Fuel Efficiency:** Average km per liter

### Chart Types
- **Bar Chart:** Compare values (e.g., shipments by priority)
- **Line Chart:** Trend over time (e.g., daily deliveries)
- **Pie Chart:** Proportions (e.g., % by priority)
- **Heat Map:** Intensity of activity by location/time

### Date Range Picker
- **What:** Select time period for analysis
- **Options:** Today, This Week, This Month, Custom Range
- **Updates:** Charts refresh based on selected period

### Export Report
- **What:** Download analytics as PDF or Excel
- **Purpose:** Share with stakeholders or save for records

### Performance Comparison
- **What:** Compare metrics across different periods
- **Example:** "This week vs last week", "This month vs same month last year"
- **Shows:** Improvement or decline

---

## ROUTE OPTIMIZATION PAGE TERMS

### Optimize Route
- **What:** Button/action to calculate optimal delivery sequence
- **Input:** Select shipments and vehicles
- **Output:** Ordered list of stops, distance, estimated time

### Route Visualization
- **What:** Map showing planned delivery route
- **Shows:**
  - Depot (starting point)
  - Numbered stops (1, 2, 3...)
  - Connecting lines (the route)
  - Markers with addresses

### Route Details
- **Total Distance:** Sum of all segments in km
- **Estimated Duration:** Total time including delivery time at each stop
- **Number of Stops:** Count of delivery points
- **Vehicle Used:** Which vehicle is assigned
- **Optimized Time:** How long optimization calculation took

### Stop Sequence
- **What:** Order to visit delivery locations
- **Shows:** Number, customer name, address, time window
- **Changeable:** Can be manually reordered if needed

---

## NOTIFICATIONS PAGE TERMS

### Notification List
- **What:** All notifications/alerts for the user
- **Shows:** Message title, timestamp, read/unread status
- **Sortable:** By newest, oldest, status

### Read / Unread
- **Read:** User has viewed the notification
- **Unread:** New notification not yet seen (shown in bold or special color)
- **Mark as Read:** Action to acknowledge notification

### Notification Types
- **Dispatch:** "Shipment 123 assigned to driver John - vehicle truck-01"
- **Delivery:** "Shipment 123 successfully delivered to customer"
- **Delay:** "Shipment 123 running late - new ETA 4:30 PM"
- **System:** "Maintenance alert - Vehicle 5 offline for service"

### Notification Badge
- **What:** Number shown on Notifications icon/link
- **Shows:** Count of unread notifications
- **Updates:** In real-time when new notifications arrive

### Notification Settings
- **What:** Enable/disable notification types
- **Options:** Notification preferences (email, push, SMS)

---

## DEMAND FORECAST PAGE TERMS

### Forecast Chart
- **What:** Graph showing predicted shipment volume
- **X-axis:** Date/Time
- **Y-axis:** Predicted number of shipments
- **Line:** Forecast trend

### Historical Data
- **What:** Past shipment data shown for comparison
- **Shows:** Actual shipment counts from previous periods
- **Purpose:** Validate forecast accuracy

### Forecast Accuracy
- **What:** Percentage of predictions that were correct
- **Shows:** "90% accurate" or similar metric
- **Improves:** As system collects more real delivery data

### Predicted Demand
- **What:** AI prediction for future shipment volume
- **Example:** "Expect 250 shipments tomorrow, 300 next week"
- **Use:** Plan resources (drivers, vehicles, warehouse staff)

### Seasonal Trends
- **What:** Patterns that repeat (daily, weekly, monthly, yearly)
- **Examples:**
  - More deliveries on weekdays
  - Peak season in holiday months
  - Lower volume on weekends
- **Shows:** As visual pattern on chart

### Peak Hours
- **What:** Times with highest projected shipments
- **Shows:** Usually morning or evening for e-commerce
- **Use:** Schedule drivers during peak hours

---

## USERS / TEAM PAGE TERMS

### User List
- **What:** Table of all users in the system
- **Shows:** Name, email, phone, role, status, join date
- **Actions:** Edit, disable, delete accounts

### Role
- **Admin:** Full system access
- **Manager:** Operational oversight
- **Driver:** Makes deliveries
- **Customer:** Places orders and tracks

### User Status
- **Active:** Account is enabled (can login and use system)
- **Inactive:** Account disabled (cannot login)

### Driver Management
- **Assigned Vehicle:** Which vehicle is driver using
- **Active Deliveries:** How many shipments currently assigned
- **Total Deliveries:** Career statistics
- **Rating:** Customer satisfaction rating (if applicable)

### Create User
- **What:** Add new team member
- **Required:** Name, email, password, phone, role
- **Auto-email:** Login credentials sent to new user

---

## LOGIN & AUTHENTICATION TERMS

### Login Page
- **What:** First page, requires credentials
- **Fields:** Username/Email, Password
- **Button:** "Login" or "Sign In"

### Authentication
- **What:** Verification of user identity
- **Process:** Username/email + password checked against database
- **Result:** Access granted with session token

### Protected Route
- **What:** Pages only accessible after login
- **Examples:** Dashboard, Vehicles, Shipments
- **If Not Logged In:** Redirected to login page

### Unauthorized
- **What:** Trying to access page without proper permissions
- **Error:** "You don't have permission to view this page"

---

## LAYOUT & NAVIGATION TERMS

### Header / Top Bar
- **What:** Top section of page
- **Shows:** System logo, user profile, logout button, notifications icon
- **Always Visible:** On every page

### Main Content Area
- **What:** Central area where page content displays
- **Changes:** Shows different content based on selected menu

### Footer
- **What:** Bottom section (if present)
- **Shows:** Copyright, version, links

### Breadcrumb
- **What:** Navigation path showing current location
- **Example:** "Home > Shipments > SHP-001-ABC"
- **Use:** Easy navigation back to parent pages

### Loading State
- **What:** Page is fetching data from server
- **Shows:** Spinner/loading animation
- **Wait:** Data will appear shortly

### Error Message
- **What:** Something went wrong
- **Examples:** "Shipment not found", "Permission denied"
- **Action:** Follow instructions or contact admin

### Success Message
- **What:** Action completed successfully
- **Examples:** "Shipment created successfully", "Changes saved"
- **Dismissible:** Can close notification

---

## SEARCH & FILTER TERMS

### Search Bar
- **What:** Text input to find specific items
- **Searches:** Tracking numbers, names, addresses
- **Real-time:** Results update as you type

### Filter
- **What:** Narrow down displayed items by criteria
- **Filter By:** Status, priority, date range, driver, vehicle type
- **Multiple Filters:** Can combine (e.g., "In Transit + High Priority")

### Sort
- **What:** Arrange items in specific order
- **Options:**
  - Sort A-Z (alphabetical)
  - Sort Z-A (reverse alphabetical)
  - Sort by date (newest/oldest)
  - Sort by status

### Pagination
- **What:** Breaking long lists into pages (10 items per page)
- **Shows:** Current page, total pages, navigation buttons
- **Purpose:** Keep pages fast and readable

---

## COMMON DASHBOARD TROUBLESHOOTING TERMS

### "Page is loading forever"
- Network issue or server problem
- Try refreshing browser (F5)
- Check internet connection

### "Data seems outdated"
- Real-time updates have delay
- Click refresh button
- Check last updated timestamp

### "Map not showing vehicle location"
- GPS signal lost or weak
- Vehicle sending updates every 1-2 minutes normally
- Refresh page to get latest position

### "Button is disabled/grayed out"
- You don't have permission for this action
- Or the action isn't valid in current state
- Example: Can't optimize route if no pending shipments

### "Notification not appearing"
- Check if notifications are enabled in settings
- Check user notifications are enabled for this type
- Check if you're logged in (notifications only show to logged-in users)

---

**Tip for Moderators:** Familiarize yourself with the sidebar navigation. Each section (Shipments, Vehicles, Tracking, Analytics) has its own purpose and metrics. They work together to give a complete operations picture.
