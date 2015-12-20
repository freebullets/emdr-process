# EMDR Processor

This project was created to aid traders in the popular MMO, EVE Online. It connects to relays running the [EVE market data relay](https://github.com/gtaylor/EVE-Market-Data-Relay) service, parses the data, and stores it in a MySQL database. The EMDR relays are run by volunteered servers, and in-game market data is read from the game's cache and uploaded to a relay. The project also contains a simple web interface created with Bootstrap and Django. 

## Features

 - Subscribes to the EMDR relay service
 - Parses the incoming data stream and stores it in a MySQL database
 - The Django website sends queries based on the item and region input and displays its data

## TODO

 - Display historic data with fancy graphs
 - Create more ways of visualizing market data
 - Create an arbitrage view to analyze opportunities to trade items between locations for quick profit
 - Create manufacturing & invention views to find profitable items to make
 - Create a route planning view to collect purchased items (using TSP algorithms)
 - Create a trade management view to analyze which items are most profitable
 - Reimplement backend in Go

## Live demo
https://evetools.xyz (soon)

## Stack
### Frontend
 - Django
 - Bootstrap
 - Twitter's autocomplete
### Backend
 - ZeroMQ
 - MariaDB
 - Python
   - HotQueue
 - Node.js
   - Kue

## Performance

The project's backend was originally implemented in Python, but it was migrated to Node.js for performance reasons. Because the data stream receives around 10,000 data points per minute, performance-tuning was a challenge. 

The first challenge was to design efficient indices on the database tables. There are two types of data stored: a current snapshot of the market and the daily market stats of each item and region combination. These datasets currently comprise about 2 million and 42 million records respectively. Indices were chosen in order to balance optimizing planned queries and efficiently storing the data.

The second challenge was to implement a script to insert the data into the database. HotQueue, a Python queuing system, was used in order to store incoming orders, as the network socket would otherwise be blocked and data lost. Given that Python is normally a single-threaded language, a pseudo-multithreading library called gevent was used to perform more work while MySQL was busy. Unfortunately, after lots of Python profiling, the backend was migrated to Node.js which miraculously reduced CPU usage to single-digits.
