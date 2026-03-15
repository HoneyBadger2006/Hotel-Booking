use ll_qpham5;

# Milestone 2
# Problem #2

# Guest table
CREATE TABLE Guest (
	user_ID        BIGINT AUTO_INCREMENT PRIMARY KEY,
	email          VARCHAR(255) NOT NULL UNIQUE,
	password_hash  VARCHAR(255) NOT NULL,
	full_name      VARCHAR(200) NOT NULL,
	phone          VARCHAR(30),
	created_at     DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP
);


# Hotel table
CREATE TABLE Hotel (
	hotel_ID   BIGINT AUTO_INCREMENT PRIMARY KEY,
	name       VARCHAR(200) NOT NULL,
	address    VARCHAR(300) NOT NULL,
	city       VARCHAR(100) NOT NULL,
	state      VARCHAR(100),
	country    VARCHAR(100) NOT NULL
);


# Room Type table
CREATE TABLE Room_Type (
	room_type_ID  BIGINT AUTO_INCREMENT PRIMARY KEY,
	capacity      INT NOT NULL,
	name          VARCHAR(100) NOT NULL,
	price_per_night   DECIMAL(10,2) NOT NULL
);


# Room table
CREATE TABLE Room (
	room_No       INT NOT NULL,
	hotel_ID      BIGINT NOT NULL,
	room_type_ID  BIGINT NOT NULL,
	description   TEXT,

	PRIMARY KEY (room_No, hotel_ID),

	FOREIGN KEY (hotel_ID) REFERENCES Hotel(hotel_ID),
	FOREIGN KEY (room_type_ID) REFERENCES Room_Type(room_type_ID)
);


# Booking table
CREATE TABLE Booking (
	Booking_ID     BIGINT AUTO_INCREMENT PRIMARY KEY,
	user_ID        BIGINT NOT NULL,
	room_No        INT NOT NULL,
	hotel_ID       BIGINT NOT NULL,
	check_in_date  DATE NOT NULL,
	check_out_date DATE NOT NULL,
	status         VARCHAR(20) NOT NULL,
	created_at     DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,

	FOREIGN KEY (user_ID) REFERENCES Guest(user_ID),

	FOREIGN KEY (room_No, hotel_ID)
	REFERENCES Room(room_No, hotel_ID),

	FOREIGN KEY (hotel_ID) REFERENCES Hotel(hotel_ID)
);


# Review table
CREATE TABLE Review (
	review_id   BIGINT AUTO_INCREMENT PRIMARY KEY,
	user_ID     BIGINT NOT NULL,
	hotel_ID    BIGINT NOT NULL,
	rating      INT NOT NULL,
	title       VARCHAR(200),
	body        TEXT,
	created_at  DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,

	FOREIGN KEY (user_ID) REFERENCES Guest(user_ID),
	FOREIGN KEY (hotel_ID) REFERENCES Hotel(hotel_ID)
);


# Amenity table
CREATE TABLE Amenity (
	amenity_ID    BIGINT AUTO_INCREMENT PRIMARY KEY,
	name          VARCHAR(100) NOT NULL,
	description   TEXT,

	UNIQUE (name)
);

# Room Amenity table
CREATE TABLE Room_amenity (
	amenity_ID  BIGINT NOT NULL,
	room_No     INT NOT NULL,
	hotel_ID    BIGINT NOT NULL,
	PRIMARY KEY (amenity_ID, room_No, hotel_ID),
	FOREIGN KEY (amenity_ID) REFERENCES Amenity(amenity_ID),
	FOREIGN KEY (room_No) REFERENCES Room(room_No),
	FOREIGN KEY (hotel_ID) REFERENCES Hotel(hotel_ID)
);
  
INSERT INTO Room_Type VALUES
	(1, 1, 'Single Room', 110.00), #1 couch
	(2, 2, 'Standard Room', 150.00),	#1 queen
	(3, 2, 'Deluxe Room', 170.00),	#1 king
	(4, 4, 'Superior Room', 200.00),	#1 queen and 1 couch
	(5, 4, 'Family Room', 225.00),	#2 queens
	(6, 8, 'Joint Room', 270.00),	#4 queens
	(7, 2, 'Honeymoon Suite', 250.00),	#1 king 1 restroom
	(8, 6, 'Presidential Suite', 350.00), #1 king 1 queen 1 couch 1 kitchen and 2 restroom
	(9, 4, 'Junior Suite', 300.00),	#1 king 1 couch and 1 kitchen
	(10, 2, 'Accessibility Room', 180.00);	#1 queen

INSERT INTO Amenity VALUES
	(1, 'Free WiFi', 'Guests will have access to free WiFi and internet during their stay.'),
	(2, 'Large Bathroom', 'Guests will have access to a large open spaced bathroom for simultaneous multi-user use.'),
	(3, 'Free Toiletries', 'Guests will have access to free toiletries included in their bathroom, such as soap, shampoo, conditioner, etc.'),
	(4, 'Accessibility Accomodation', 'Guests will have access to their room from the first floor and direct access to exits and the parking lot.'),
	(5, 'Folding Couch', 'Guests will have access to a folding couch that extends to create another bed.'),
	(6, 'Kitchen Suite', 'Guests will have access to a full kitchen, including all Food Facilities, stove, freezer, and sink.'),
	(7, 'Air Conditioning', 'Guests will have access to an air conditioning unit to control temperature for the entire room.'),
	(8, 'Scenic View', 'Guests will have access to a beautiful view from their room windows.'),
	(9, 'Work Desk', 'Guests will have access to a full workplace desk setup with a chair, desk, and lamp included.'),
	(10, 'Free Cable', 'Guests will have access to a TV with free cable included.');

INSERT INTO Guest VALUES
	(1, 'oliviabennet@ex.com', '001ob', 'Olivia Bennett', '5827649310', CURRENT_TIMESTAMP),
	(2, 'ethanparker@ex.com', '002ep', 'Ethan Parker', '1938475621', CURRENT_TIMESTAMP),
	(3, 'miarodriguez@ex.com', '003mr', 'Mia Rodriguez', '4082391756', CURRENT_TIMESTAMP),
	(4, 'liamwalker@ex.com', '004lw', 'Liam Walker', '5648392071', CURRENT_TIMESTAMP),
	(5, 'avajohnson@ex.com', '005aj', 'Ava Johnson', '8361204957', CURRENT_TIMESTAMP),
	(6, 'noahgarcia@ex.com', '006ng', 'Noah Garcia', '1947268530', CURRENT_TIMESTAMP),
	(7, 'sophialee@ex.com', '07sl', 'Sophia Lee', '7635219480', CURRENT_TIMESTAMP),
	(8, 'lucasmartinez@ex.com', '008lm', 'Lucas Martinez', '4291856073', CURRENT_TIMESTAMP),
	(9, 'emmataylor@ex.com', '009et', 'Emma Taylor', '6501982745', CURRENT_TIMESTAMP),
	(10, 'jamescooper@ex.com', '010jc', 'James Cooper', '3725016849', CURRENT_TIMESTAMP);

INSERT INTO Hotel VALUES
	(1, 'Hilton Garden Inn', '379 Sea Drive', 'Phoenix', 'Arizona', 'USA'),
	(2, 'Homewood Suites by Hyatt', '742 Oak Street', 'Springfield', 'Illinois', 'USA'),
	(3, 'Hilton Motif', '22 Hauptstrabe', 'Berlin', NULL, 'Germany'),
	(4, 'DoubleTree by Hilton', '452 Pine Avenue', 'Los Angeles', 'California', 'USA'),
	(5, 'Embassy Suites by Hilton', '56 Rue de Rivoli', 'Paris', NULL, 'France'),
	(6, 'Grand Hyatt', '98 Queen Street West', 'Toronto', NULL, 'Canada'),
	(7, 'Hyatt Regency', '101 Riverwood Drive', 'Seattle', 'Washington', 'USA'),
	(8, 'Holiday Inn Express & Suites', '34 Park Lane', 'Mayfair', NULL, 'London'),
	(9, 'Best Western Plus Plaza', '125 George Street', 'Sydney', NULL, 'Australia'),
	(10, 'Courtyard Waterfront by Marriott', '350 Elm Road', 'Miami', 'Florida', 'USA');

INSERT INTO Room VALUES
	(582, 2, 3, 'This Deluxe room features 1 king size bed, free WiFi, and a work desk in the Illinois area.'),
	(149, 10, 10, 'This Accessibility room features 1 queen size bed, free WiFi, and a large bathroom to accomodate guests with disabilities in the Miami area.'),
	(763, 5, 4, 'This Superior room features 1 queen size bed, 1 folding couch, free WiFi, and a scenic view in the Paris area.'),
	(395, 7, 3, 'This Deluxe room features 1 king size bed, free WiFi, a scenic view, and free toiletries in the Seattle area.'),
	(827, 8, 1, 'This Single room features 1 queen size bed and free WiFi in the Mayfair area.'),
	(410, 3, 6, 'This Joint room features 4 queen size beds, free WiFi, and air conditioning in the Berlin area.'),
	(953, 9, 7, 'This Honeymoon suite features 1 king size bed, a large bathroom, a kitchen suite, free WiFi, free toiletries, and a scenic view for couples in the Syndey area.'),
	(672, 1, 5, 'This Family room features 2 queen size beds, free WiFi, free cable, and air conditioning in the Phoenix area.'),
	(283, 4, 8, 'This Presidential Suite features 1 king size bed, 1 queen size bed, 1 folding couch, a kitchen suite, 2 large bathrooms, free WiFi, free cable, free toiletries, air conditioning, and a scenic view in the Los Angeles area.'),
	(518, 6, 2, 'This Standard room features 1 queen size bed, free WiFi, free cable, and a work desk in the Toronto area.');

INSERT INTO Booking VALUES
	(1, 4, 518, 6, '2022-03-15', '2022-03-22', 'Confirmed', CURRENT_TIMESTAMP),
	(2, 2, 395, 7, '2019-11-23', '2019-11-30', 'Completed', CURRENT_TIMESTAMP),
	(3, 6, 672, 1, '2021-08-09', '2021-08-23', 'Refunded', CURRENT_TIMESTAMP),
	(4, 3, 953, 9, '2020-06-17', '2020-06-30', 'Refunded', CURRENT_TIMESTAMP),
	(5, 1, 149, 10, '2023-01-05', '2023-01-20', 'Pending', CURRENT_TIMESTAMP),
	(6, 10, 410, 3, '2018-07-24', '2018-08-07', 'Completed', CURRENT_TIMESTAMP),
	(7, 8, 827, 8, '2022-10-11', '2022-10-14', 'Cancelled', CURRENT_TIMESTAMP),
	(8, 9, 763, 5, '2021-02-19', '2021-02-28', 'Cancelled', CURRENT_TIMESTAMP),
	(9, 5, 283, 4, '2020-12-31', '2021-01-21', 'Completed', CURRENT_TIMESTAMP),
	(10, 7, 582, 2, '2017-05-02', '2017-05-09', 'Refunded', CURRENT_TIMESTAMP);

INSERT INTO Review VALUES
	(1, 4, 2, 7, 'Spacious Room, but Slow Wi-Fi', 'The room was spacious and clean, with modern amenities that made the stay comfortable. However, the Wi-Fi was a bit slow, which was a downside for work purposes.', CURRENT_TIMESTAMP),
	(2, 5, 7, 9, 'Breathtaking View, but Noisy Streets', 'I loved the view from the window—overlooking the city skyline was breathtaking. The bed was comfortable, but the noise from the street outside was disruptive at night.', CURRENT_TIMESTAMP),
	(3, 4, 9, 9, 'Great Location, but Room Needs Updates', 'This hotel has a fantastic location, just steps away from major attractions. The room itself was quite basic, and the bathroom could use some updates.', CURRENT_TIMESTAMP),
	(4, 1, 2, 8, 'Friendly Staff, but Air Conditioning Issues', 'The staff were incredibly friendly and made check-in a breeze. Unfortunately, the air conditioning did not work properly, and the room felt a bit too warm.', CURRENT_TIMESTAMP),
	(5, 2, 6, 6, 'Good Breakfast, but Thin Walls', 'I appreciated the complimentary breakfast, which had a good selection of options. The room was clean, but the walls were thin, and I could hear everything in the hallway.', CURRENT_TIMESTAMP),
	(6, 10, 3, 8, 'Cozy Room, but Low Water Pressure', 'Our room was cozy, with a very comfortable mattress that helped us sleep soundly. On the downside, the shower had low water pressure, which was a bit frustrating.', CURRENT_TIMESTAMP),
	(7, 6, 9, 10, 'Stylish Hotel, but Noisy at Times', 'The hotel had a lovely atmosphere, and the decor was stylish and modern. However, the room wasn’t as quiet as expected, with noise from nearby construction in the morning.', CURRENT_TIMESTAMP),
	(8, 7, 6, 7, 'Convenient Location, but Small Room', 'We had a pleasant stay with easy access to the beach and restaurants nearby. The room was smaller than I anticipated, but it was still comfortable for a short stay.', CURRENT_TIMESTAMP),
	(9, 2, 2, 7, 'Good Value, but Inconsistent Housekeeping', 'Great value for the price, with friendly service and a decent-sized room. The only issue was that the room wasn’t cleaned properly on the second day of our stay.', CURRENT_TIMESTAMP),
	(10, 9, 4, 10, 'Great Amenities, but Odd Smell in Room', 'The hotel had all the amenities I needed, including a gym and pool. My room, however, had an odd smell that lingered throughout the stay, which was off-putting.',CURRENT_TIMESTAMP);

INSERT INTO Room_amenity VALUES
	(1, 582, 2),
	(9, 582, 2),
	(4, 149, 10),
	(1, 149, 10),
	(2, 149, 10),
	(5, 763, 5),
	(1, 763, 5),
	(8, 763, 5),
	(1, 395, 7),
	(8, 395, 7),
	(3, 395, 7),
	(1, 827, 8),
	(1, 410, 3),
	(7, 410, 3),
	(1, 953, 9),
	(2, 953, 9),
	(6, 953, 9),
	(3, 953, 9),
	(8, 953, 9),
	(1, 672, 1),
	(10, 672, 1),
	(7, 672, 1),
	(5, 283, 4),
	(6, 283, 4),
	(2, 283, 4),
	(1, 283, 4),
	(3, 283, 4),
	(7, 283, 4),
	(8, 283, 4),
	(1, 518, 6),
	(10, 518, 6),
	(9, 518, 6);
  
#4(1)
# List each booking with guest name and email, hotel and location,
# room number and type, check in and out dates, and booking status
SELECT
	b.booking_id,
	g.full_name,
	g.email,
	h.name AS hotel_name,
	h.city,
	h.state,
	b.hotel_id,
	b.room_no,
	rt.name AS room_type,
	rt.capacity,
	b.check_in_date,
	b.check_out_date,
	b.status,
	b.created_at
FROM Booking b
JOIN Guest g
ON b.user_id = g.user_id
JOIN Hotel h
ON b.hotel_id = h.hotel_id
JOIN Room r
ON b.hotel_id = r.hotel_id
AND b.room_no  = r.room_no
JOIN Room_Type rt
ON r.room_type_id = rt.room_type_id
ORDER BY b.created_at DESC;


# This SQL statement finds hotels 
# whose average review rating is higher than
# the overall average rating across all reviews.
#4(2)
SELECT
	h.hotel_ID,
	h.name AS hotel_name,
	AVG(r.rating) AS hotel_avg_rating
FROM Hotel h
JOIN Review r
ON r.hotel_ID = h.hotel_ID
GROUP BY h.hotel_ID, h.name
HAVING AVG(r.rating) > (
	SELECT AVG(rating)
	FROM Review
);
 
#4(3)
# This query displays all hotels available in the
# hotel database that do not yet have any reviews.
SELECT hotel_ID
FROM Hotel
WHERE hotel_ID NOT IN (SELECT hotel_ID FROM Review);

# 4(4).
# This SQL statement finds the average review score from users
# who created their account within the past year
SELECT
	g.user_id,
	g.full_name,
	AVG(r.rating) AS avg_rating
FROM Guest g
JOIN Review r
ON r.user_id = g.user_id
WHERE g.created_at >= date_sub(now(), interval 1 year)
GROUP BY g.user_id, g.full_name
ORDER BY avg_rating;

#4(5)
# This SQL statement is a left outer join example
# It lists all hotels and shows booking info if
# they have bookings hotels with no bookings will
# still appear (booking columns will be NULL)
SELECT
	h.hotel_id,
	h.name as hotel_name,
	h.city,
	h.state,
	b.booking_id,
	b.status,
	b.check_in_date,
	b.check_out_date
FROM Hotel h
LEFT JOIN Booking b
	ON b.hotel_id = h.hotel_id
ORDER BY h.hotel_id, b.created_at;



# BELOW CODE FOR QUESTION 5 NOT UPDATED AND DOES NOT FULLY FUNCTION
# 5.

# This SQL statement creates an index
# for Guest.created_at
create index Idx_Guest_CreatedAt on Guest(created_at);

# This SQL statement creates a trigger
# that activates after insert on Booking
# and checks if the new booking conflicts with another
delimiter |

create trigger insert_booking
after insert on Booking

for each row
begin
    if exists (
        select 1
        from Booking B
        where B.hotel_ID = new.hotel_ID
        and B.room_No = new.room_No
        and new.check_in_date < B.check_out_date
        and new.check_out_date > B.check_in_date
    ) then
        delete from Booking B
        where B.Booking_ID = new.Booking_ID;
    end if;
end|
delimiter ;

# This SQL statement creates a stored procedure
# that calculates the total price of a booking
delimiter |
create procedure calcBookingPrice(check_in_date date, check_out_date date, hotel_ID bigint, room_No int, out total_amount decimal(10, 2)) begin
    declare price_per_night decimal(10, 2);
    declare nights int;
    
    SELECT RT.price_per_night
    INTO price_per_night
    FROM Room
    JOIN Room_Type RT using (room_type_ID)
    WHERE  hotel_ID = Room.hotel_ID
    and room_No = Room.room_No;
    
    set nights = datediff(check_out_date, check_in_date);
    
    set total_amount = price_per_night * nights;
end|
delimiter ;

DROP TRIGGER IF EXISTS insert_booking;

use ll_qpham5;

update Booking
set status = 'Cancelled'
where Booking_ID = 1;

use ll_qpham5;

update Booking
set status = 'Cancelled'
where Booking_ID = 1;

select * from Booking;
  
select * from Guest; 
  
  