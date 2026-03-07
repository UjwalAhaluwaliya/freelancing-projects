# Technical Terms Cheat Sheet - Quick Reference

## MOST IMPORTANT DASHBOARD TERMS

### Transit / In Transit
- **What:** Shipment is actively being transported by a driver
- **Status:** Active delivery in progress
- **Real Action:** Driver is moving the vehicle with the shipment

### Pending
- **What:** Shipment created but not yet assigned to a driver
- **Status:** Waiting for assignment
- **Action Needed:** System will assign to nearest available driver

### Delivered
- **What:** Shipment successfully reached destination
- **Status:** Complete
- **Proof:** Marked with actual delivery timestamp

### ETA (Estimated Time of Arrival)
- **What:** AI-predicted delivery time
- **Example:** "Your package will arrive by 3:45 PM"
- **Factors:** Distance, traffic, weather, vehicle type, weight

### Shipment Status Flow
```
Pending → Assigned → In Transit → Delivered
                           ↓
                        (if late → Delay notification)
```

### Vehicle Status Types
- **Available** - Ready to take deliveries
- **In Transit** - Currently delivering
- **Maintenance** - Out of service/being repaired

---

## QUICK ANSWERS TO COMMON MODERATOR QUESTIONS

### Q: "What is a Tracking Number?"
A: Unique 30-character ID like "SHP-2026-02-26-001ABC" that customers use to track their package in real-time.

### Q: "How does route optimization work?"
A: AI algorithm analyzes all shipments and vehicles, calculates the shortest route considering distance, vehicle capacity, and time, then provides the most efficient delivery sequence.

### Q: "What's the difference between estimated and actual delivery?"
A: **Estimated** = AI prediction before delivery | **Actual** = Real timestamp when customer received package

### Q: "Why does a shipment have Priority levels?"
A: To prioritize urgent deliveries (medical, perishable) over normal ones. Urgent shipments get assigned to vehicles first.

### Q: "What information is tracked in real-time?"
A: GPS location (lat/lng), current status, timestamp, and optional driver notes - updated continuously during transit.

### Q: "Can customers see live tracking?"
A: Yes, they enter tracking number and see real-time GPS location, status, driver info, and live ETA.

### Q: "How are vehicles assigned to shipments?"
A: Route optimization algorithm assigns shipments to vehicles based on: current location, capacity remaining, vehicle type, and delivery priority.

### Q: "What's the purpose of the Demand Forecast?"
A: Predict future shipment volume so managers can: prepare vehicles, hire drivers, arrange warehouses, plan budgets.

### Q: "How are delays detected?"
A: System compares actual delivery time vs ETA. If significantly late, automatic "delay notification" is sent to customer and manager.

### Q: "What does 'In Transit' mean?"
A: Shipment is physically moving with the driver. GPS updates are being recorded continuously.

---

## USER ROLES & PERMISSIONS

| Role | Can View | Can Create | Can Update | Can Track |
|------|----------|-----------|-----------|-----------|
| **Customer** | Own shipments | Create shipment | Update profile | Own shipments |
| **Driver** | Assigned shipments | - | Delivery status | Own deliveries |
| **Manager** | All shipments | Approve shipments | Shipments/Vehicles | All shipments |
| **Admin** | Everything | Everything | Everything | Everything |

---

## TECHNICAL COMPONENTS EXPLAINED SIMPLY

### API (Application Programming Interface)
- **Simple:** Frontend asks Backend for data using URLs
- **Example:** `/shipments/123` = "Give me data for shipment 123"
- **Response:** Backend sends back JSON with shipment details

### Database
- **Simple:** A secure storage system for all information
- **Stores:** Users, shipments, vehicles, locations, notifications
- **No:** Raw passwords (only encrypted versions)

### AI Models
- **Demand Forecast:** Predicts "You'll get 250 shipments tomorrow"
- **ETA Predictor:** Predicts "This shipment arrives at 3:45 PM"
- **Route Optimizer:** Says "Deliver to stops in this order: A→B→C→D"

### Real-Time Tracking
- **How:** Vehicle sends GPS location every minute to server
- **Server:** Updates shipment's current location in database
- **Customer:** Sees updated location on map instantly

### Notifications
- **Dispatch:** "Your shipment is on the way with driver John"
- **Delivery:** "Your package has been delivered"
- **Delay:** "Your delivery will be 30 minutes late"
- **System:** General updates or alerts

---

## COMMON ABBREVIATIONS

| Abbrev | Full Form | Meaning |
|--------|-----------|---------|
| **ETA** | Estimated Time of Arrival | Predicted delivery time |
| **VRP** | Vehicle Routing Problem | Route optimization challenge |
| **GPS** | Global Positioning System | Location coordinates |
| **API** | Application Programming Interface | Communication method |
| **JSON** | JavaScript Object Notation | Data format |
| **ORM** | Object-Relational Mapping | Database interaction |
| **CORS** | Cross-Origin Resource Sharing | Security for frontend-backend |
| **JWT** | JSON Web Token | Authentication credential |
| **KPI** | Key Performance Indicator | Performance metric |
| **UI** | User Interface | What users see |

---

## SHIPMENT PRIORITIES EXPLAINED

### Low Priority
- Online orders that aren't urgent
- Can be delayed 1-2 days
- Delivered when vehicle has space

### Normal Priority  
- Standard e-commerce deliveries
- Expected delivery in 2-3 days
- Most common shipment type

### High Priority
- Important business documents
- Promised delivery in 1 day
- Gets assigned to vehicles sooner

### Urgent Priority
- Medical supplies, perishables, gifts
- Promised same-day/next-day delivery
- Assigned first, routed faster

---

## VEHICLE TYPES & CAPACITY

| Type | Capacity | Best For | Speed |
|------|----------|----------|-------|
| **Bike** | 10-50 kg | Small local deliveries | Fast, agile |
| **Van** | 500-2,000 kg | Urban/suburban deliveries | Medium speed |
| **Truck** | 2,000-5,000 kg | Long distance, bulk | Slower but more cargo |

---

## GPS COORDINATES QUICK REFERENCE

- **Latitude:** North/South position (-90 to +90°)
- **Longitude:** East/West position (-180 to +180°)
- **Format:** 40.7128, -74.0060 (New York example)
- **Use:** Maps, real-time tracking, distance calculation

---

## SHIPMENT STATUS MEANINGS FOR CUSTOMERS

```
😕 PENDING     = Waiting to be picked up
🚚 IN TRANSIT  = On the way (GPS location showing live)
✅ DELIVERED   = Successfully arrived
❌ CANCELLED   = Order cancelled, won't deliver
⏰ DELAYED     = Running late, new ETA shown
```

---

## KEY METRICS TO KNOW (DASHBOARD)

- **Total Shipments:** Count of all orders in system
- **Pending:** Waiting for assignment (should be low)
- **In Transit:** Currently being delivered (active shipments)
- **Delivered Today:** Completed shipments
- **On-Time Rate:** % of shipments delivered by ETA
- **Average Delivery Time:** How long typical delivery takes
- **Vehicle Utilization:** How full vehicles are (should be high)
- **Fleet Status:** How many vehicles are available vs. in use

---

## WHAT TO TELL MODERATORS

### About Data Security
"All user passwords are encrypted in the database. No one can see raw passwords. User authentication uses secure tokens (JWT)."

### About Real-Time Tracking
"Vehicles send GPS coordinates in real-time. Customers see their shipment location updated continuously on a map during transit."

### About AI Accuracy
"Our AI models learn from historical data. The more deliveries we complete, the more accurate our ETA predictions and demand forecasts become."

### About Route Optimization
"We use Google's OR-Tools algorithm which solves the Vehicle Routing Problem. It considers distance, vehicle capacity, and delivery sequence to find the most efficient routes and reduce fuel costs."

### About Notifications
"Users get automatic alerts for: shipment dispatch, delivery confirmation, and delay warnings. Unread notifications are tracked."

### About Vehicle Management
"We track vehicle fuel level, mileage, and maintenance status. Vehicles can't be assigned to jobs if they're in maintenance."

### About Scaling
"The system can handle multiple drivers, hundreds of shipments, and complex route optimization for the entire fleet simultaneously."

---

## TROUBLESHOOTING TERMS MODERATORS MIGHT MENTION

### "Shipment stuck in Pending"
- Driver/Vehicle not assigned yet
- Check if vehicles are available
- Check vehicle capacity (might be full)

### "ETA keeps changing"
- Normal - recalculated based on traffic, weather, current position
- Gets more accurate as vehicle approaches

### "Vehicle shows wrong location"
- GPS update delay (usually updates every 1 minute)
- Weak signal in rural areas
- Refresh the page

### "Notification not sent"
- Check user's notification settings
- Verify user email/phone is correct
- Check notification status in database

### "Routes not optimized"
- Might be low traffic volume
- Check if multiple vehicles are assigned
- Algorithm works best with 10+ stops per route

---

**Print this sheet and keep it handy during moderator discussions!**
