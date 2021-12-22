-- DB1

CREATE TABLE "Users1" (
	user_id VARCHAR(36) NOT NULL, 
	first_name VARCHAR(255) NOT NULL, 
	last_name VARCHAR(255) NOT NULL, 
	address VARCHAR(3000) NOT NULL, 
	phone_code VARCHAR(5) NOT NULL, 
	phone_number VARCHAR(25) NOT NULL, 
	balance INTEGER, 
	PRIMARY KEY (user_id)
)

CREATE TABLE "Shops1" (
	shop_id VARCHAR(36) NOT NULL, 
	shop_name VARCHAR(255) NOT NULL, 
	remaining_prods_num INTEGER, 
	sold_prods_num INTEGER, 
	PRIMARY KEY (shop_id), 
	UNIQUE (shop_name)
)

CREATE TABLE "Products1" (
	product_id VARCHAR(36) NOT NULL, 
	product_name VARCHAR(255) NOT NULL, 
	category VARCHAR(255) NOT NULL, 
	price INTEGER, 
	quantity INTEGER, 
	quantity_in_cart INTEGER, 
	description VARCHAR(3000) NOT NULL, 
	image VARCHAR(1000) NOT NULL, 
	PRIMARY KEY (product_id)
)

CREATE TABLE "Carts1" (
	cart_id VARCHAR(36) NOT NULL, 
	last_updated DATETIME, 
	PRIMARY KEY (cart_id)
)

CREATE TABLE "Orders1" (
	order_id VARCHAR(36) NOT NULL, 
	total_price INTEGER, 
	order_date DATETIME, 
	shipping_address VARCHAR(255) NOT NULL, 
	buyer_phone_number VARCHAR(25) NOT NULL, 
	PRIMARY KEY (order_id)
)

-- DB2

CREATE TABLE "Users2" (
	user_id VARCHAR(36) NOT NULL, 
	email VARCHAR(255) NOT NULL, 
	username VARCHAR(255) NOT NULL, 
	password VARCHAR(255) NOT NULL, 
	PRIMARY KEY (user_id), 
	UNIQUE (email), 
	UNIQUE (username)
)

CREATE TABLE "Shops2" (
	shop_id VARCHAR(36) NOT NULL, 
	user_id VARCHAR(36), 
	PRIMARY KEY (shop_id), 
	FOREIGN KEY(user_id) REFERENCES "Users2" (user_id)
)

CREATE TABLE "Products2" (
	product_id VARCHAR(36) NOT NULL, 
	user_id VARCHAR(36), 
	PRIMARY KEY (product_id), 
	FOREIGN KEY(user_id) REFERENCES "Users2" (user_id)
)

CREATE TABLE "Carts2" (
	cart_id VARCHAR(36) NOT NULL, 
	user_id VARCHAR(36), 
	PRIMARY KEY (cart_id), 
	FOREIGN KEY(user_id) REFERENCES "Users2" (user_id)
)

CREATE TABLE "Orders2" (
	order_id VARCHAR(36) NOT NULL, 
	is_ordered BOOLEAN, 
	is_delivered BOOLEAN, 
	user_id VARCHAR(36), 
	PRIMARY KEY (order_id), 
	FOREIGN KEY(user_id) REFERENCES "Users2" (user_id)
)

CREATE TABLE shop_product (
	shop_id VARCHAR(36), 
	product_id VARCHAR(36), 
	FOREIGN KEY(shop_id) REFERENCES "Shops2" (shop_id), 
	FOREIGN KEY(product_id) REFERENCES "Products2" (product_id)
)

CREATE TABLE cart_product (
	cart_id VARCHAR(36), 
	product_id VARCHAR(36), 
	quantity INTEGER, 
	FOREIGN KEY(cart_id) REFERENCES "Carts2" (cart_id), 
	FOREIGN KEY(product_id) REFERENCES "Products2" (product_id)
)

CREATE TABLE order_product (
	order_id VARCHAR(36), 
	product_id VARCHAR(36), 
	quantity INTEGER, 
	FOREIGN KEY(order_id) REFERENCES "Orders2" (order_id), 
	FOREIGN KEY(product_id) REFERENCES "Products2" (product_id)
)
