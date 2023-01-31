from skynamo import getCustomers,getOrders,getStockLevels
from datetime import datetime,timedelta
from skynamoInstanceDataClasses.Customer import Customer

def getCustomerCodesOfActiveCustomersWithOrdersInTheLast30Days():
	# Get all customers
	customers = getCustomers()
	# Get all orders
	orders = getOrders()
	# Get customer codes of customers with orders in the last 30 days
	customerCodesWithOrdersInTheLast30Days = [order.customer_code for order in orders if order.date >= datetime.now() - timedelta(days=30)]
	# Get all customer codes of active customers with orders in the last 30 days
	result = []
	for customer in customers:
		if customer.active and customer.code in customerCodesWithOrdersInTheLast30Days:
			result.append(customer.code)
	# Return the list of customer codes
	return result

def getTotalStockLeftForTheMostPopularProductInTheLastMonth():
	# Get all orders
	orders = getOrders()
	# Get all stock levels
	stockLevels = getStockLevels()
	# Get the most valueable product code in the last month
	valuePerProductCodeForLastMonth = {}
	for order in orders:
		if order.date >= datetime.now() - timedelta(days=30):
			for orderLine in order.items:
				valueInOrder=orderLine.quantity*orderLine.unit_price
				if orderLine.product_code in valuePerProductCodeForLastMonth:
					valuePerProductCodeForLastMonth[orderLine.product_code] +=valueInOrder
				else:
					valuePerProductCodeForLastMonth[orderLine.product_code] = valueInOrder
	mostValueableProductCode = None
	mostValueableProductValue = 0
	for productCode in valuePerProductCodeForLastMonth:
		if valuePerProductCodeForLastMonth[productCode] > mostValueableProductValue:
			mostValueableProductCode = productCode
			mostValueableProductValue = valuePerProductCodeForLastMonth[productCode]

	# Get the stock level for the most valueable product
	for stockLevel in stockLevels:
		if stockLevel.product_code == mostValueableProductCode:
			return stockLevel.stock_level