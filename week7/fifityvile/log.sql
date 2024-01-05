-- Keep a log of any SQL queries you execute as you solve the mystery.

--check the reported crimes of the day
SELECT *
FROM crime_scene_reports
WHERE year = 2021
AND month = 7
AND day = 28
AND street = "Humphrey Street";

--view the records of the three witnesses about the robbery
SELECT *
FROM interviews
WHERE year = 2021
AND month = 7
AND day = 28
AND transcript LIKE "%thief%";

--  1.
--  Sometime within ten minutes of the theft, I saw the thief get into a car in the bakery parking lot and drive away.
--  If you have security footage from the bakery parking lot, you might want to look for cars that left the parking lot in that time frame.

SELECT name
FROM people
WHERE license_plate IN
(SELECT license_plate
FROM bakery_security_logs
WHERE year = 2021
AND month = 7
AND day = 28
AND hour = 10
AND minute > 15
AND minute <= 25
AND activity = "exit")
ORDER BY name;

--  2.
--  I don't know the thief's name, but it was someone I recognized.
--  Earlier this morning, before I arrived at Emma's bakery, I was walking by the ATM on Leggett Street and saw the thief there withdrawing some money.

SELECT name
FROM people, bank_accounts
WHERE people.id = bank_accounts.person_id
AND account_number IN
(SELECT account_number
FROM atm_transactions
WHERE year = 2021
AND month = 7
AND day = 28
AND atm_location = "Leggett Street"
AND transaction_type = "withdraw")
ORDER BY name;

3.
-- As the thief was leaving the bakery, they called someone who talked to them for less than a minute.
-- In the call, I heard the thief say that they were planning to take the earliest flight out of Fiftyville tomorrow.
-- The thief then asked the person on the other end of the phone to purchase the flight ticket.

SELECT name
FROM people
WHERE passport_number IN
(SELECT passport_number
FROM passengers
WHERE flight_id IN
(SELECT id
FROM flights
WHERE year = 2021
AND month = 7
AND day = 29
AND origin_airport_id IN
(SELECT id
FROM airports
WHERE city = "Fiftyville")
ORDER BY hour
LIMIT 1))
ORDER BY name;

SELECT name
FROM people
WHERE phone_number IN
(SELECT caller
FROM phone_calls
WHERE year = 2021
AND month = 7
AND day = 28
AND duration < 60)
ORDER BY name;