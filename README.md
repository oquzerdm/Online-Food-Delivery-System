# Online Food Delivery System
## Description
Designing a data system for a food delivery platform like Yemeksepeti. Users include customers, admins, managers, and deliverers. The system manages restaurant details, products, and order statuses. Admins handle restaurants and regions, while managers oversee products.

## Prerequisites
Before running this project, make sure you have the following requirements installed:

- Python (>=3.6)
- PySimpleGUI library

## Installation
- Clone the repository to your local machine.
- Make sure you have Python installed.
- Install the required library using the following command
  
   ```pip install PySimpleGUI ```

## Usage

To run the system, execute the following command in your terminal:

```bash
python Code.py
```

Users of this system include customers, system admins, restaurant managers, and deliverers. Each user type has specific functionalities and actions they can perform.

### Customers
Customers interact with the system to place orders. Here's how a customer can use the system:

1. **Register/Login:**
   - Customers can register with their unique GSM number, name, surname, and delivery address.
   - Logging in is done with the registered GSM number and password.

2. **Place Orders:**
   - Customers can browse restaurants, view products, and place orders for multiple products.
   - Each order includes details such as a unique order number, date and time of request, status ("New" initially), and total price.

### System Admins
System admins have administrative control over the entire system. Their actions include:

1. **Manage Restaurants:**
   - Add or delete restaurants from the system.
   - Update information related to existing restaurants.

2. **Manage Regions:**
   - Add new regions to the system.

### Restaurant Managers
Restaurant managers oversee the products and information related to their respective restaurants. Their actions include:

1. **Manage Products:**
   - Add or delete products to the system.
   - Update information for existing products.

2. **Manage Orders:**
   - Assign orders to deliverers.
   - Update order status to "Shipping" when assigned.
   - Update order status to "Delivered" upon successful delivery.

### Deliverers
Deliverers handle the delivery process. Here's how they use the system:

1. **View Assigned Orders:**
   - Deliverers can view orders assigned to them by restaurant managers.

2. **Update Order Status:**
   - Change the order status to "Shipping" when starting the delivery.
   - Change the order status to "Delivered" upon completing the delivery.

## Features

- **User Authentication**
- **Dynamic GUI**
- **Order Management**
- **Admin Controls**
- **Product Management**
- **Delivery Tracking**
- **Multi-role Access**

## Database
The system uses a SQLite database named ```muhtesemotesi.db``` to store user and company information, product details, and funding transactions.

## Contributions
Contributions to this project are welcome. Feel free to fork the repository, make improvements, and create pull requests.

## Author
Oguz Erdem

## Acknowledgments
Special thanks to my project group (Umarbek Guvercin, Hasan Murtaza Kolomuç, Ahmet Buğra Dilci, Atakan Başaran) for their contributions to the project.
