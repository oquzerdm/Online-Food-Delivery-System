# -*- coding: utf-8 -*-

import sqlite3
import PySimpleGUI as sg
from datetime import datetime

con = sqlite3.connect('muhtesemotesi.db')
cur = con.cursor()
login_user_id = -1
login_user_name = -1
login_user_surname = -1
login_user_type = -1
sg.change_look_and_feel('DarkRed1') 
def loginwindow():
    layoutlogin=[[sg.Text('Welcome to The BringIT, please log in.')],
                 [sg.Text('ID',size=(10,1)),sg.Input(key='ID', size=(20,1))],
                 [sg.Text('Password',size=(10,1)),sg.Input(key='password',size=(20,1),password_char='*')],
                 [sg.Button('Login'),sg.Exit()]]
    return sg.Window('Login',layoutlogin)

def rmanagerwindow():
    layoutrmanager=[[sg.Text('Welcome '+ str(login_user_name))],
                    [sg.Button('Orders')],
                    [sg.Button("Products")],
                    [sg.Button('Logout')]]
    return sg.Window('Restaurant Manage System',layoutrmanager)


def delivererwindow():
    layoutdeliverer=[[sg.Text('Welcome '+ str(login_user_name))],
                     [sg.Button('Order Menu')],
                     [sg.Button('Logout')]]
    return sg.Window('Deliverer Assign System',layoutdeliverer)

def customerwindow():
    layoutdeliverer=[[sg.Text('Welcome '+ str(login_user_name))],
                     [sg.Button('Restaurants')],
                     [sg.Button('Order History')],
                     [sg.Button('Update Profile')],
                     [sg.Button('Logout')]]
    return sg.Window('Deliverer Assign System',layoutdeliverer)

def systemadminwindow():
    layoutsystemadmin=[[sg.Text('Welcome '+ str(login_user_name))],
                     [sg.Button('Restaurantss')],
                     [sg.Button('Regions')],
                     [sg.Button('Managers')],
                     [sg.Button('Logout')]]
    return sg.Window("System Admin System",layoutsystemadmin)


    ############ BEGIN Order Managment System for MANAGER ############

#Open up window for order assigment functionality.
ordertypes=["show all" ,"delivered", "new", "shipping"]
def orderassigmentwindow():
    orders=[]
    deliverperson=[]
    for row in cur.execute('SELECT DID, dname, dsurname, plate_number FROM Deliverers'):
        deliverperson.append((row[0], row[1], row[2], row[3]))  
    layoutorder = [[sg.Text('Orders:'), sg.Combo(ordertypes, size=(40,20), default_value= 'show all', key='ordertypes'), sg.Button('List Orders')],
                   [sg.Listbox(orders, size=(40,10), key='orders')],
                   [sg.Text('Deliverer:'), sg.Combo(deliverperson, size=(40,20), key='deliverperson'), sg.Button('Assign Deliverer')],
              [sg.Button('Return To Main')]]
    return sg.Window('Order Assign',layoutorder)
#Listing orders by current situation.
def button_list_ordertypes(values):
    ordertypes = values['ordertypes']
    orders=[]
    if ordertypes== 'show all':
         for row in cur.execute('SELECT OrderInfo.orderID, oprice, odate, ostatus FROM OrderInfo, delivery_assign, RManagers, manages WHERE OrderInfo.orderID = delivery_assign.orderID and RManagers.RMID=delivery_assign.RMID and RManagers.RMID = manages.RMID and RManagers.RMID= ?',(login_user_id,)):
            orders.append((row[0], row[1], row[2], row[3]))  
            window.Element('orders').Update(values=orders)
    else:
        for row in cur.execute('SELECT OrderInfo.orderID, oprice, odate, ostatus FROM OrderInfo, delivery_assign, RManagers, manages WHERE OrderInfo.orderID = delivery_assign.orderID and RManagers.RMID=delivery_assign.RMID and RManagers.RMID = manages.RMID and RManagers.RMID= ? and ostatus=?',(login_user_id, ordertypes)):
            orders.append((row[0], row[1], row[2], row[3]))     
            window.Element('orders').Update(values=orders)
            
#Assign deliverers to the orders.
def button_assign_deliverperson(values):
    deliverperson= values['deliverperson']
    orders=values['orders']
    shipping=['shipping']
    if len(orders)==0:
        sg.popup('Please choose an order to assign deliverer!')
    elif deliverperson == '':
        sg.popup('Please choose a deliverer to assign!')
    else:
        index_orders = orders[0][0]
        index_orders_status = orders[0][3]
        index_deliverperson_id = deliverperson[0]
        index_deliverperson_name = deliverperson[1]
        index_shipping=shipping[0]
        if index_orders_status == 'delivered':
            sg.popup('This order has already been delivered.\n\nYou cannot assign a deliverer to delivered orders.\nPlease choose a different order.\n')
        else:
            cur.execute('UPDATE delivery_assign SET DID = ? WHERE orderID = ?', (index_deliverperson_id, index_orders))
            cur.execute('UPDATE OrderInfo SET ostatus = ? WHERE orderID = ?', (index_shipping, index_orders)) 
            window.Element('orders').Update(values=orders)
            con.commit()
            ### BEGIN Callback of active orders function for manager.
            button_list_ordertypes(values)
            ### END Callback of active orders function for manager.
            sg.popup('Deliverer '+str(index_deliverperson_name)+' with ID '+str(index_deliverperson_id)+' is assigned to order '+str(index_orders)+'\n')
    
    ############ END Order Managment System for MANAGER ############








    ############ BEGIN Order Managment System for DELIVERER ############
    
#Open up window for deliverer assigment functionality.
def delivererassigmentwindow():
    deliver_assignedorders=[]
    deliver_assignedorders_past=[]
    for row in cur.execute("SELECT OrderInfo.orderID, odate, ostatus FROM Deliverers, delivery_assign, OrderInfo WHERE Deliverers.DID=delivery_assign.DID and OrderInfo.orderID = delivery_assign.orderID and Deliverers.DID=?",(login_user_id,)):
        if row[2] == "delivered":
            deliver_assignedorders_past.append(row)
        else:
            deliver_assignedorders.append(row)
    layoutdelassign = [[sg.Text('Active Orders:'), sg.Listbox(deliver_assignedorders, size=(25,5), key='deliver_assignedorders'), sg.Button('Set as Delivered')],
                       [sg.Text('Past Orders:'), sg.Listbox(deliver_assignedorders_past, size=(25,5), key='deliver_assignedorders_past')], 
                       [sg.Button('Return To Main')]]
    return sg.Window("Deliverer Interface", layoutdelassign)

#Setting orders as delivered.
def button_set_orderdelivered(values):
    delivered=["delivered"]
    deliver_assignedorders = values['deliver_assignedorders']
    deliver_assignedorders_past = values['deliver_assignedorders_past']
    if len(deliver_assignedorders)==0:
        sg.popup('Please choose an order to set delivered!')
    else:
       index_delivered=delivered[0]
       index_deliver_assignedorders=deliver_assignedorders[0][0]
       cur.execute('UPDATE OrderInfo SET ostatus = ? Where orderID = ?',(index_delivered,index_deliver_assignedorders))
       con.commit()
       
       ### BEGIN Callback of active orders function for deliverer.
       deliver_assignedorders=[]
       deliver_assignedorders_past=[]
       for row in cur.execute("SELECT OrderInfo.orderID, odate, ostatus FROM Deliverers, delivery_assign, OrderInfo WHERE Deliverers.DID=delivery_assign.DID and OrderInfo.orderID = delivery_assign.orderID and Deliverers.DID=?",(login_user_id,)):
           if row[2] == "delivered":
               deliver_assignedorders_past.append(row)
           else:
               deliver_assignedorders.append(row)
       ### END Callback of active orders function for deliverer.
       
       window.Element('deliver_assignedorders').Update(values=deliver_assignedorders)
       window.Element('deliver_assignedorders_past').Update(values=deliver_assignedorders_past)
       sg.popup('Congratulations '+str(login_user_name)+'!\n\nYou succesfully delivered the order number' +str(index_deliver_assignedorders)+'\nKeep going like that.\n')
       ############ END Order Managment System for DELIVERER ############




    ############ BEGIN Order Managment System for CUSTOMER ############
    
#Customer update profile informations.            
def updateprofilewindow():
    customerinfo=[]
    for row in cur.execute("SELECT Customers.CID, User.uname, User.usurname, Customers.CgsmNumber, Customers.delivery_addressID  FROM Customers, User WHERE User.gsmNumber=Customers.CgsmNumber and User.userID = Customers.CID and User.userID=?",(login_user_id,)):
        customerinfo.append((row[0], row[1], row[2], row[3],row[4]))        
    layoutupdateprofile =[[sg.Text('Hello '+str(customerinfo[0][1])+' '+str(customerinfo[0][2])+'!', key='c1')],
                          [sg.Text('Your phone number is '+str(customerinfo[0][3])+' and your region is '+str(customerinfo[0][4])+'.\n', key='c2')],
                          [sg.Text('Change Name: ', size=(20,1)), sg.Input( size=(20,1), key='profile_name')],
                          [sg.Text('Change Surname: ', size=(20,1)), sg.Input(key='profile_surname', size=(20,1))],
                          [sg.Text('Change Phone Number: ', size=(20,1)), sg.Input( size=(20,1), key='profile_phonenumber')],
                          [sg.Text('Change Region: ', size=(20,1)), sg.Input(key='profile_region', size=(20,1))],
                          [sg.Button('Update'), sg.Button('Return To Main')]]

    return sg.Window("Update Profile", layoutupdateprofile)

#Button for update profile informatiıns
def button_update_profile(values):
    customerinfo=[]
    region_ids=['964', '963', '965', '966', '967']
    customerinfo2=[]
    for row in cur.execute("SELECT Customers.CID, User.uname, User.usurname, Customers.CgsmNumber, Customers.delivery_addressID  FROM Customers, User WHERE User.gsmNumber=Customers.CgsmNumber and User.userID = Customers.CID and User.userID=?",(login_user_id,)):
        customerinfo.append((row[0], row[1], row[2], row[3], row[4]))
    updatedname = values['profile_name']
    updatedsurname = values['profile_surname']
    updatedphone = values['profile_phonenumber']
    updatedregion = values['profile_region']
    print (type ("updatedregion"))
    if updatedname == '':
        pass
    elif updatedname == str(customerinfo[0][1]):
        sg.popup('Updated name should be different than exist!')
        
    else:
        if updatedname.isnumeric():
            sg.popup('Name should be string!')
            return
        else:
            cur.execute('UPDATE User SET uname = ? Where userID = ?',(updatedname,login_user_id))
            con.commit()
    if updatedsurname == '':
        pass
    elif updatedsurname == str(customerinfo[0][2]):
        sg.popup('Updated surname should be different than exist!')
    else:
        if updatedsurname.isnumeric():
            sg.popup('Surname should be string!')
            return
        else:
            cur.execute('UPDATE User SET usurname = ? Where userID = ?',(updatedsurname,login_user_id))
            con.commit()
    if updatedphone == '':
        pass
    elif updatedphone == str(customerinfo[0][3]):
        sg.popup('Updated phone number should be different than exist!')
    else:
        if updatedphone.isnumeric():
            cur.execute('UPDATE User SET gsmNumber = ? Where userID = ?',(updatedphone,login_user_id))
            cur.execute('UPDATE Customers SET CgsmNumber = ? Where CID = ?',(updatedphone,login_user_id))
            con.commit()
        else:
            sg.popup('Phone number should be numeric!')
            return
    if updatedregion == '':
        pass
    elif updatedregion == str(customerinfo[0][4]):
        sg.popup('Updated region should be different than exist!')
    else:
        if updatedregion.isnumeric():
            if updatedregion in region_ids:
                print(updatedregion)
                cur.execute('UPDATE Customers SET delivery_addressID = ? Where CID = ?',(updatedregion,login_user_id))
                con.commit()     
            else:
                sg.popup('There is no region with this id.\n\nYou should enter one of the\n following region ids: 963, 964, 965, 966, 967!')
                print(updatedregion)
                print(region_ids)
               
                return
        else:
            sg.popup('Region should be numeric!')
            return
    if updatedname == '' and updatedsurname == '' and updatedphone ==  '' and updatedregion == '' or updatedname == str(customerinfo[0][1]) or updatedsurname == str(customerinfo[0][2]) or updatedphone == str(customerinfo[0][3]) or updatedregion == str(customerinfo[0][4]):
        sg.popup('To update your informations, you need to input different values!')
    else:
        sg.popup('You successfully updated your informations!')
        for row in cur.execute("SELECT Customers.CID, User.uname, User.usurname, Customers.CgsmNumber, Customers.delivery_addressID  FROM Customers, User WHERE User.gsmNumber=Customers.CgsmNumber and User.userID = Customers.CID and User.userID=?",(login_user_id,)):
            customerinfo2.append((row[0], row[1], row[2], row[3],row[4]))
        window.Element('c1').Update(value='Hello '+str(customerinfo2[0][1])+' '+str(customerinfo2[0][2])+'!')
        window.Element('c2').Update(value='Your phone number is '+str(customerinfo2[0][3])+' and your region is '+str(customerinfo2[0][4])+'.\n')

#Open up window for past orders of customer.
def customerpastorders():
    customerpast=[]
    customercurrent = []
    customercurrent_check=[]
    for row in cur.execute("SELECT OrderInfo.OrderID, OrderInfo.oprice, OrderInfo.odate, OrderInfo.ostatus FROM Customers, OrderInfo, orders, User WHERE OrderInfo.ostatus = 'delivered' and orders.OrderID=OrderInfo.orderID and orders.CID = Customers.CID and Customers.CID = User.userID and User.userID=?",(login_user_id,)):        
        customerpast.append((row[0], str(row[1] )+str("TL"), row[2], row[3]))
    for row in cur.execute("SELECT OrderInfo.OrderID, OrderInfo.oprice, OrderInfo.odate, OrderInfo.ostatus FROM Customers, OrderInfo, orders, User WHERE OrderInfo.ostatus != 'delivered' and orders.OrderID=OrderInfo.orderID and orders.CID = Customers.CID and Customers.CID = User.userID and User.userID=?",(login_user_id,)):        
        customercurrent_check.append((row[0], str(row[1] )+str("TL"), row[2], row[3])) 
    if len(customercurrent_check) == 0:
        customercurrent = ["No past orders."]
    else:
        customercurrent = customercurrent_check
         
    layoutpastorders = [[sg.Text('Current Orders:')],
                        [sg.Listbox(customercurrent, size=(35,3), key='customercurrent')],
                        [sg.Text('Past Orders:')],
                        [sg.Listbox(customerpast, size=(35,10), key='customerpast')],
                        [sg.Button('Return To Main')]]
    return sg.Window("Past Orders", layoutpastorders)


filterrestaurants = ["Show All", "Büfe", "Tavukçu", "Hamburgerci", "Köfteci", "Dönerci", "Kebapçı", "Çiğköfteci", "Mantıcı", "Tostçu", "Kokoreççi"]
def restaurantswindow():
    regionrestaurants=[] 
    for row in cur.execute("SELECT Restaurant.rname, Restaurant.rphone_number, Restaurant.rtype, Restaurant.rrating, Restaurant.rworking_hours, Customers.delivery_addressID FROM Restaurant, delivers_to, Customers, User, DeliveryRegion WHERE delivers_to.restaurantID=Restaurant.restaurantID and delivers_to.regionID=DeliveryRegion.regionID and DeliveryRegion.regionID=Customers.delivery_addressID and Customers.CID = User.userID and User.userID=?",(login_user_id,)):
        regionrestaurants.append((  row[0], str('Phone: ')+str(row[1]), row[2], str('Rating: ')+str(row[3]), str('WorkingHours: ')+str(row[4]) ))
    layoutrestaurants = [[sg.Text('Currently available restaurants on your region:'), sg.Combo(filterrestaurants, default_value='Show All', size=(20,5), key='filterrestaurants'), sg.Button('Filter')],
                         [sg.Listbox(regionrestaurants, size=(65,15), key='regionrestaurants')],
                         [sg.Button('Choose'), sg.Button('Return To Main')]]
    return sg.Window('List of Restaurants', layoutrestaurants)


#List restaurant types. 
def button_list_resttypes(values):
    filterrestaurants = values['filterrestaurants']
    regionrestaurants=[]
    if filterrestaurants == "Show All":
        for row in cur.execute('SELECT Restaurant.rname, Restaurant.rphone_number, Restaurant.rtype, Restaurant.rrating, Restaurant.rworking_hours, Customers.delivery_addressID FROM Restaurant, delivers_to, Customers, User, DeliveryRegion WHERE delivers_to.restaurantID=Restaurant.restaurantID and delivers_to.regionID=DeliveryRegion.regionID and DeliveryRegion.regionID=Customers.delivery_addressID and Customers.CID = User.userID and User.userID=?', (login_user_id, )):
            regionrestaurants.append(( row[0], str('Phone: ')+str(row[1]), row[2], str('Rating: ')+str(row[3]), str('WorkingHours: ')+str(row[4]) ))
            window.Element('regionrestaurants').Update(values=regionrestaurants)
    else:
        for row in cur.execute('SELECT Restaurant.rname, Restaurant.rphone_number, Restaurant.rtype, Restaurant.rrating, Restaurant.rworking_hours, Customers.delivery_addressID FROM Restaurant, delivers_to, Customers, User, DeliveryRegion WHERE delivers_to.restaurantID=Restaurant.restaurantID and delivers_to.regionID=DeliveryRegion.regionID and DeliveryRegion.regionID=Customers.delivery_addressID and Customers.CID = User.userID and User.userID=? and Restaurant.rtype=?', (login_user_id, filterrestaurants)):
            regionrestaurants.append(( row[0], str('Phone: ')+str(row[1]), row[2], str('Rating: ')+str(row[3]), str('WorkingHours: ')+str(row[4]) ))  
            window.Element('regionrestaurants').Update(values=regionrestaurants)

        
def afterrestaurantwindow():
    menurestaurant=[]
    basket=[]
    for row in cur.execute("SELECT Products.pdescription, Products.pprice FROM Products, is_in_menu, Restaurant WHERE Products.productsID=is_in_menu.productsID and is_in_menu.restaurantID=Restaurant.restaurantID and Restaurant.rname=?",(selected_restaurant_name,)):        
        menurestaurant.append((row[0], row[1] ))
    layoutafterrestaurant = [[sg.Listbox(menurestaurant, size=(35,10), key='menurestaurant')],
                             [sg.Button('Add Basket'), sg.Button('Preview Order'), sg.Button('Return To Restaurants')]]
                             
    return sg.Window("Menu for Selected Restaurant", layoutafterrestaurant)

totalprice = []
def previeworderwindow():
    for i in range(len(basket)):
        totalprice.append(basket[i][0][1])    
    layoutprevieworder = [[sg.Listbox(basket, size=(20,5), key='basket_key')],
                          [sg.Text('Total price: '+str(sum(totalprice))+' TL')], 
                          [sg.Button('Set Order'), sg.Button('Remove Item')],
                          [sg.Button('Return To Menu')]]
    
    return sg.Window("Preview Order", layoutprevieworder)




basket = []
def button_add_basket(values):
    global basket
    menurestaurant = values['menurestaurant']
    if len(menurestaurant) == 0:
        sg.popup('Please choose an item to add basket!')
    else:        
        basket.append(menurestaurant)    

def button_remove_basket(values):
    global window
    global totalprice
    basket_key = values['basket_key']
    print(basket_key)
    if len(basket_key) == 0:
        sg.popup('Please choose an item to remove from basket!')
    else:
        basket.remove(basket_key[0])
        totalprice = []
        window.close()
        window = previeworderwindow()
    
def button_set_restaurant(values):
    global selected_restaurant_name
    regionrestaurants = values['regionrestaurants']
    if len(regionrestaurants)==0:
        sg.popup('Please choose an restaurant to show menu!')
        selected_restaurant_name = -1
        
    else:
        selected_restaurant_name = regionrestaurants[0][0]
        
def code_omer():
    global window
    global basket
    global login_user_id
    totprice = 0
    parameters_orderInfo = ()
    cur.execute("SELECT Max(orderID) FROM OrderInfo")
    new_id = cur.fetchone()[0] + 1
    parameters_orderInfo = (new_id,) + parameters_orderInfo
    for i in basket: 
       totprice += ( i [0][1]) 
    now = datetime.now()
    dt_str = now.strftime("%d/%m/%Y %H:%M")
    parameters_orderInfo= parameters_orderInfo + (totprice,)
    order_info_remaining = (dt_str,"new")
    parameters_orderInfo = parameters_orderInfo + order_info_remaining
    cur.execute("INSERT INTO OrderInfo VALUES(?,?,?,?)",parameters_orderInfo)
    print (parameters_orderInfo,"an")
    product_name = basket [0][0][0]
    
    print (product_name)
    cur.execute('SELECT restaurantID FROM is_in_menu,Products  Where is_in_menu.productsID = Products.productsID and Products.pdescription = ?',(product_name,))
    rest_id = int(cur.fetchone ()[0])
    parameters_orders = (new_id,login_user_id,rest_id)
    cur.execute("INSERT INTO orders VALUES(?,?,?)",parameters_orders)
    print (parameters_orders)
    print ("za")
    cur.execute('SELECT RMID FROM manages Where restaurantID = ?',(rest_id,))
    manager_id = int(cur.fetchone ()[0])
    parameters_del_ass = (new_id,manager_id)
    cur.execute("INSERT INTO delivery_assign VALUES(?,?,?)",(new_id,manager_id,None))
    print (parameters_del_ass)   
    window.close()
    window=customerwindow()
    con.commit()
    basket = []
       ############ END Order Managment System for CUSTOMER ############
            



        ############ BEGINNING Order Managment System for SYSTEM ADMIN ############
def button_restaurants_for_systemadmin():
    restaurantsirala = []
    for row in cur.execute('SELECT rname, rphone_number, rtype, rrating FROM Restaurant'):
        restaurantsirala.append((row[0], row[1], row[2], row[3]))  
    layoutrestaurantsofadmins = [[sg.Text('Restaurants:')],
                                 [sg.Listbox(restaurantsirala, size=(40,10), key='canbedeleted')],
                                 [sg.Button("Create a Restaurant"), sg.Button("Delete a Restaurant")],
                                 [sg.Button('Return To Main')]]
    return sg.Window('System Admin System', layoutrestaurantsofadmins)

def button_create_a_restaurant():
    paymenttypeke=["Cash","Credit Card","Both"]
    layoutcreaterestaurant = [[sg.Text('Restaurant Name:', size=(20,1)), sg.Input(key='rrname', size=(20,1))],
                                 [sg.Text('Address:', size=(20,1)), sg.Input(key='raddress', size=(20,1))],
                                 [sg.Text('Phone Number:', size=(20,1)), sg.Input(key='phonenumber', size=(20,1))],
                                 [sg.Text('Working hours:', size=(20,1)), sg.Input(key='workinghours', size=(20,1))],
                                 [sg.Text('Payment Type:', size=(20,1)), sg.Combo(paymenttypeke, default_value= '', key='ordertypes')],
                                 [sg.Text('Restaurant Type:', size=(20,1)), sg.Input(key='restype', size=(20,1))],
                                 [sg.Text('Rating:', size=(20,1)), sg.Input(key='rrating', size=(20,1))],
                                 [sg.Button('Insert'), sg.Button("Cancel")]]
    return sg.Window('Creating Restaurant', layoutcreaterestaurant)

def button_saving_new_restaurant(values):
    global window
    parameters=[]
    parameters = (values['rrname'],values['raddress'],values['phonenumber'],values['workinghours'],values['ordertypes'],values['restype'],values["rrating"])
    if parameters[0] == "":
        sg.popup("Restaurant name cannot be empty!")
    elif parameters[1] == "":
        sg.popup("Address cannot be empty!")
    elif parameters[2] == "":
        sg.popup("Phone Number name cannot be empty!")
    elif not parameters[2].isnumeric():
        sg.popup("Phone Number should be numeric!")
    elif not len(parameters[2]) == 10:
        sg.popup("Phone number has not correct digit number. Please insert 10 digits.")   
    elif parameters[3] == "":
        sg.popup("Working hours name cannot be empty!")
    elif parameters[4] == "":
        sg.popup("Payment Type name cannot be empty!")
    elif parameters[5] == "":
        sg.popup("Restaurant Type name cannot be empty!")
    elif parameters[6] == "":
        sg.popup("Rating Type name cannot be empty!")
    elif int(parameters[6]) < 0 or int(parameters[6]) > 5:
        sg.popup("Please enter rating between 0 and 5")
    elif not parameters[6].isnumeric():
        sg.popup("Rating should be numeric!")
    else:
        cur.execute("SELECT Max(restaurantID) FROM Restaurant")
        new_id = cur.fetchone()[0] + 1  
        parameters = (new_id,) + parameters
        cur.execute("INSERT INTO Restaurant VALUES(?,?,?,?,?,?,?,?)",parameters)
        con.commit()
        sg.popup("New Restaurant " + parameters[1]+" with id " + str(parameters[0]))
        window.close()
        window = button_restaurants_for_systemadmin()
        
def button_deleting_restaurant(values):
    if values["canbedeleted"] == []:
        sg.popup("Select restaurant!")
    else:
        willbedeleted2 = values["canbedeleted"][0][0]
        cur.execute("DELETE FROM Restaurant WHERE rname = ?",(willbedeleted2,))
        con.commit()
        sg.popup("Restaurant " + willbedeleted2 +" is deleted.")
        window.close()
    
def button_delete_product(values):
    if values["abcdef"] == []:
        sg.popup("Select product!")
    else:
        willbedeleted2 = values["abcdef"][0][0]
        cur.execute("DELETE FROM Products WHERE pdescription = ?",(willbedeleted2,))
        con.commit()
        sg.popup("Restaurant " + willbedeleted2 +" is deleted.")
        button_products_menu(values)
    

def button_add_rmanager():
    managersirala = []
    for row in cur.execute('SELECT rname, uname, usurname, Rmanagers.RMID FROM Restaurant, User, Rmanagers, manages WHERE Restaurant.restaurantID=manages.restaurantID AND User.UserID=Rmanagers.RMID AND User.UserID=manages.RMID'):
        managersirala.append((row[0], row[1], row[2], row[3]))  
    layoutmanagermenu = [[sg.Text('Managers')],
                                 [sg.Listbox(managersirala, size=(40,10), key='mcanbedeleted')],
                                 [sg.Button("Add a Manager"), sg.Button("Delete a Manager")],
                                 [sg.Button('Return To Main')]]
    return sg.Window('System Admin System', layoutmanagermenu)
def button_add_newmanager():
    layoutaddmanager = [[sg.Text('Manager Name:', size=(20,1)), sg.Input(key='unamem', size=(20,1))],
                                 [sg.Text('Surname:', size=(20,1)), sg.Input(key='usurnamem', size=(20,1))],
                                 [sg.Text('ID:', size=(20,1)), sg.Input(key='userIDm', size=(20,1))],
                                 [sg.Text('Phone Number:', size=(20,1)), sg.Input(key='gsmNumberm', size=(20,1))],
                                 [sg.Text('Password', size=(20,1)), sg.Input(key='Passwordm', size=(20,1))],
                                 [sg.Text('Restaurant ID:', size=(20,1)), sg.Input(key='restaurantIDm', size=(20,1))],
                                 [sg.Button('Add New Manager'), sg.Button("Cancel")]]
    return sg.Window('System Admin System',layoutaddmanager)
def button_insertmanager(values):
    global window
    userval=[]
    rmanagerval=[]
    managesval=[]
    userval=(values['userIDm'],values['unamem'],values['usurnamem'],values['gsmNumberm'],values['Passwordm'])
    rmanagerval=values['userIDm']
    print(len(rmanagerval))
    managesval=(values['userIDm'],values['restaurantIDm'])
    if userval[1] == "":
        sg.popup("Manager name cannot be empty!")
    elif userval[2] == "":
        sg.popup("Manager surname cannot be empty!")
    elif userval[0] == "":
        sg.popup("ID cannot be empty!")
    elif not userval[0].isnumeric():
        sg.popup("ID should be numeric!")
    elif userval[3] == "":
        sg.popup("Phone number cannot be empty!")
    elif not userval[3].isnumeric():
        sg.popup("Phone number should be numeric")
    elif not len(userval[3]) == 10:
        sg.popup("Phone number has not correct digit number. Please insert 10 digits.")
    elif userval[4] == "":
        sg.popup("Password cannot be empty!")
    elif managesval[1] == "":
        sg.popup("Restaurant ID name cannot be empty!")
    elif not managesval[1].isnumeric():
        sg.popup("Restaurant ID should be numeric")
    else:
        cur.execute("INSERT INTO User VALUES(?,?,?,?,?)",userval)
        cur.execute("INSERT INTO Rmanagers VALUES(?)",(rmanagerval,))
        cur.execute("INSERT INTO manages VALUES(?,?)",managesval)
        con.commit()
        sg.popup("New Manager " + userval[1]+" "+userval[2]+ " with ID "+ str(userval[0])+ ", is added to the Restaurant with id " + str(managesval[1]))
        window.close()
        window = button_restaurants_for_systemadmin()
def button_delete_manager(values):
    willbedeletedman = values["mcanbedeleted"][0][-1]
    cur.execute("DELETE FROM Rmanagers WHERE RMID = ?",(willbedeletedman,))
    con.commit()
    sg.popup("Manager " + str(willbedeletedman) +" is deleted.")
    window.close()
    
def button_adding_region():
    layoutaddingregion = [[sg.Text('Average Time:', size=(20,1)), sg.Input(key='averagetimeke', size=(20,1))],
                          [sg.Text('Minimum Order Price:', size=(20,1)), sg.Input(key='minimumorder', size=(20,1))],
                          [sg.Button('Add'), sg.Button("Cancel")]]
    return sg.Window('Adding Region', layoutaddingregion)

def button_add_region(values):
    global window
    parameterss =[]
    parameterss = (values['averagetimeke'],values['minimumorder'])
    if parameterss[0] == "":
        sg.popup("Average Time name cannot be empty!")
    elif not parameterss[0].isnumeric():
        sg.popup("Average Time should be numeric!")
    elif int(parameterss[0]) <= 0:
        sg.popup("Please enter positive number for average time")
    elif parameterss[1] == "":
        sg.popup("Minimum Order Price name cannot be empty!")
    elif not parameterss[1].isnumeric():
        sg.popup("Minimum Order Price should be numeric!")
    elif int(parameterss[1]) <= 0:
        sg.popup("Please enter positive number for minimum order price")
    else:
        cur.execute("SELECT Max(regionID) FROM DeliveryRegion")
        new_idd = cur.fetchone()[0] + 1  
        parameterss = (new_idd,) + parameterss
        cur.execute("INSERT INTO DeliveryRegion VALUES(?,?,?)",parameterss)
        con.commit()
        sg.popup("New Region with id " + str(parameterss[0])+" added.")
        window.close()
        window = button_restaurants_for_systemadmin()
        
def button_products_menu(values):
    global window
    productslist = []
    global login_user_id
    for row in cur.execute("SELECT pdescription, pprice FROM manages, is_in_menu, Products WHERE manages.restaurantID = is_in_menu.restaurantID AND is_in_menu.productsID = Products.productsID AND manages.RMID=?",(login_user_id,)):
        productslist.append((row[0], row[1]))
    layoutproductss = [[sg.Text('Products:')],
                       [sg.Listbox(productslist, size=(30,10), key='abcdef')],
                       [sg.Button("Add Product"), sg.Button("Update Product"), sg.Button("Delete Product")],
                       [sg.Button('Return To Main')]]
    window.close()
    window = sg.Window('Productss Menu', layoutproductss)
    
def button_add_product():
    layoutaddproduct = [[sg.Text('Product Name:', size=(20,1)), sg.Input(key='productname', size=(20,1))],
                                 [sg.Text('Price:', size=(20,1)), sg.Input(key='productprice', size=(20,1))],  
                                 [sg.Button('OK'), sg.Button("Return to Products")]]
    return sg.Window('Add Product', layoutaddproduct)

def button_inserting_product(values):
    global login_user_id
    global window
    parameterske=[]
    parameterske = (values['productname'],values['productprice'])
    if parameterske[0] == "":
        sg.popup("Product name cannot be empty!")
    elif parameterske[1] == "":
        sg.popup("Product Price cannot be empty!")
    elif not parameterske[1].isnumeric():
        sg.popup("Product Price should be numeric!")
    elif int(parameterske[1]) < 0:
        sg.popup("Price should be positive!")
    else:
        cur.execute("SELECT Max(productsID) FROM Products")
        new_iddd = cur.fetchone()[0] + 1 
        print("ajdf")
        parameterske = (new_iddd,) + parameterske
        cur.execute("INSERT INTO Products VALUES(?,?,?)",parameterske)
        con.commit()
        rmidbulucam = []
        for row in cur.execute("SELECT restaurantID FROM manages WHERE RMID=?",(login_user_id,)):
            rmidbulucam.append(row[0])
        cur.execute("INSERT INTO is_in_menu VALUES(?,?)",(parameterske[0],rmidbulucam[0]))
        con.commit()
        sg.popup("New Product " + parameterske[1]+" with id " + str(parameterske[0]))
        button_products_menu(values)
    
def button_update_product(values):
    global window
    productslist = []
    for row in cur.execute("SELECT pdescription FROM manages, is_in_menu, Products WHERE manages.restaurantID = is_in_menu.restaurantID AND is_in_menu.productsID = Products.productsID AND manages.RMID=?",(login_user_id,)):
        productslist.append((row[0]))
    layoutupdateproduct = [[sg.Text('Product:'), sg.Combo(productslist, size=(40,20), default_value= 'show all', key='kgk')],
                          [sg.Text('Amount:'), sg.Input(key='amountke', size=(20,1))],
                           [sg.Button("Update Now")]]
    window.close()
    window = sg.Window('Choice', layoutupdateproduct)

def button_update_now(values):
    if values["amountke"] == "":
        sg.popup("Enter amount!")
    else:
        a = values["amountke"]
        b = values["kgk"]
        cur.execute("UPDATE Products SET pprice = ? WHERE pdescription = ?",(a,b))
        con.commit()
        sg.popup("Product is Updated")
        button_products_menu(values)

def buttonlogin(values):
    global login_user_id
    global login_user_name
    global login_user_type
    global window  
    userid = values['ID']
    userpass = values['password']
    if userid == '' and userpass == '':
        sg.popup('ID and Password cannot be empty!')
    elif userid =='':
        sg.popup('ID cannot be empty!')
    elif userpass=='':
        sg.popup('Password cannot be empty!')
    else:
        cur.execute('SELECT userID, uname FROM User Where userID = ? and Password = ?',(userid,userpass))
        row = cur.fetchone()
        
        if row is None:
            sg.popup('ID or Password is wrong!')
        else:
            login_user_id=row[0]
            login_user_name=row[1]
            # check its restaurant manager
            cur.execute('Select RMID From Rmanagers Where RMID=?',(userid,))
            rowrmanager=cur.fetchone()
            if rowrmanager is None: #check its deliverer
                cur.execute('Select DID From Deliverers Where DID=?',(userid,))
                rowdeliverer=cur.fetchone()
            
                if rowdeliverer is None: #check its customer
                    cur.execute('Select CID From Customers Where CID=?',(userid,))
                    rowcustomer = cur.fetchone()
                    
                    if rowcustomer is None:
                        cur.execute('Select SID From SystemAdmins Where SID=?',(userid,))
                        rowsystemadmin = cur.fetchone()
                        
                        if rowsystemadmin is None: #chect its customer
                            sg.popup("You are not allowed")
                        
                        else:
                            login_user_type = 'Systemadmin'
                            sg.popup('Welcome '+login_user_name+' (Systemadmin)')
                            window.close()
                            window = systemadminwindow()
                            
                    else:
                        login_user_type = 'Customer'
                        sg.popup('Welcome '+login_user_name+' (Customer)')
                        window.close()
                        window = customerwindow()
                else: 
                    login_user_type = 'Deliverer'
                    sg.popup('Welcome '+login_user_name+' (Deliverer)')
                    window.close()
                    window = delivererwindow()
            else:
                login_user_type = 'Restaurant Manager'
                sg.popup('Welcome '+login_user_name+' (Restaurant Manager)')
                window.close()
                window = rmanagerwindow()
                    
window=loginwindow()
while True:
    event, values = window.read()
    if event == 'Login':
        buttonlogin(values)
    elif event == 'Orders':
        window.close()
        window = orderassigmentwindow()
    elif event == 'Order History':
        window.close()
        window = customerpastorders()
    elif event == 'Update Profile':
        window.close()
        window = updateprofilewindow()
    elif event == 'Choose':
        button_set_restaurant(values)
        if selected_restaurant_name == -1:
                print(".")
        else: 
            window.close()
            window = afterrestaurantwindow()
    elif event == 'Return To Restaurants':
        window.close()
        window = restaurantswindow()
        basket = []
        totalprice = []
    elif event == 'Return To Menu':
        window.close()
        window = afterrestaurantwindow()
        totalprice = []
    elif event == 'Add Basket':
        button_add_basket(values)
    elif event == 'Remove Item':        
        button_remove_basket(values)
    elif event == 'Preview Order':
        if basket == []:
            sg.popup('You need to add at least 1 item to basket.')
        else: 
            window.close()
            window = previeworderwindow()
    elif event == 'Filter':
        button_list_resttypes(values)
    elif event == 'Restaurants':
        window.close()
        window = restaurantswindow()
    elif event == 'Assign Deliverer':
        button_assign_deliverperson(values)
    elif event == 'Set Order':
        print(basket)
        if len(basket) == 0: 
            sg.popup('You need to add item to basket to set order.\nPlease turn to restaurant menu to add item.')
        else:
            sg.popup('You succesfully created new order.\nBon Apetit!')
            code_omer() 
            window.close()
            window=customerwindow()
    elif event == 'Update':
        button_update_profile(values)
    elif event == "Order Menu":
        window.close()
        window = delivererassigmentwindow()
    elif event == 'List Orders':
        button_list_ordertypes(values)
    elif event == 'Set as Delivered':
        button_set_orderdelivered(values)
 #murti yeni baslangıc       
    elif event == "Restaurantss":
        window.close()
        window = button_restaurants_for_systemadmin()
    elif event == "Create a Restaurant":
        window.close()
        window = button_create_a_restaurant()
    elif event == "Insert":
        button_saving_new_restaurant(values)  
    elif event == "Cancel":
        window.close()
        window = button_restaurants_for_systemadmin()
    elif event == "Delete a Restaurant":
        button_deleting_restaurant(values)
        window = button_restaurants_for_systemadmin()
    elif event == "Managers":
        window.close()
        window=button_add_rmanager()
    elif event == "Add a Manager":
        window.close()
        window=button_add_newmanager()
    elif event == "Add New Manager":
        button_insertmanager(values)
    elif event == "Delete a Manager":
        button_delete_manager(values)
        window = button_add_rmanager()
    elif event == "Add a region":
        window.close()
        window = button_adding_region()
    elif event =="Add":
        button_add_region(values)
    elif event =="Products":
        window.close()
        button_products_menu(values)
    elif event == "Add Product":
        window.close()
        window = button_add_product()
    elif event == "OK":
        button_inserting_product(values)
    elif event == "Return to Products":
        window.close()
        button_products_menu(values)
    elif event == "Delete Product":
        button_delete_product(values)
    elif event == "Update Product":
        button_update_product(values)
    elif event == "Update Now":
        button_update_now(values)
    elif event == 'Return To Main':
        if login_user_type == 'Restaurant Manager':
            window.close()
            window = rmanagerwindow()
        elif login_user_type == 'Deliverer':
            window.close()
            window = delivererwindow()
        elif login_user_type == 'Customer':
            window.close()
            window = customerwindow()
        elif login_user_type == 'Systemadmin':
            window.close()
            window = systemadminwindow()
        else:
            window.close()
            window = loginwindow()
    elif event == 'Logout':
        login_user_id = -1
        login_user_name = -1
        login_user_type = -1
        window.close()
        window = loginwindow()
    elif event == sg.WIN_CLOSED or event=='Exit':
        break

window.close()

con.commit()
con.close()
    
                
        
    





