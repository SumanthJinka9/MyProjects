import sqlite3

conn = sqlite3.connect('database.db')
print("Connected to database successfully")

c = conn.cursor()

c.execute("""
DROP TABLE IF EXISTS popular_courses
""")

c.execute("""
CREATE TABLE popular_courses (
    id TEXT, 
    image TEXT, 
    name TEXT, 
    description TEXT, 
    price TEXT, 
    discounted_price TEXT, 
    rating TEXT)
""")

popular_courses = [
        (
          '1',
          '../static/images/Course1.png',
          'The Complete React Bootcamp From Zero to Hero',
          'Learn Python the Right Way Beginning with the fundamentals, work your way up to developing your own software and games.',
          '$100', 
          '$90',
          '5'
        ),
        (
            '2',
            '../static/images/Course2.png',
            'Javascript for Beginners - Complete Guide',
            'With this Javascript for beginners training course, you can learn javascript online and improve your web design.',
            '$100',
            '$90',
            '4.5'
        ),
        (
            '3',
            '../static/images/Course3.png',
            'Introduction to Cloud Computing with Azure',
            'Master Cloud Computing Concepts and Microsoft Azure fundamentals to start your cloud transformation journey.',
            '$100',
            '$90',
            '4.5'
        ),
        (
            '4',
            '../static/images/Course4.png',
            'Data Science: Machine Learning with Python',
            'Learn Data Science with Data Parsing, Data Visualization, Data Processing, Supervised & Unsupervised Machine Learning.',
            '$100',
            '$90',
            '4.5'
        ),
    ]

c.executemany("""
INSERT INTO popular_courses 
VALUES 
(?, ?, ?, ?, ?, ?, ?)
""", popular_courses)

conn.commit()

print("Created popular_courses table successfully!")

c.execute("""
DROP TABLE IF EXISTS courses;
""")

c.execute("""
CREATE TABLE courses (
    id TEXT, 
    image TEXT, 
    name TEXT, 
    description TEXT, 
    price TEXT, 
    discounted_price TEXT, 
    rating TEXT)
""")

courses = [
        (
          '1',
          '../static/images/Course1.png',
          'Javascript for Beginners',
          'With this Javascript for beginners training search-course, you can learn javascript online and improve your web design.',
          '$100', 
          '$90',
          '5'
        ),
        (
            '2',
            '../static/images/Course2.png',
            'Javascript for Beginners - Complete Guide',
            'Learn Python the Right Way Beginning with the fundamentals, work your way up to developing your own software and games.',
            '$100',
            '$90',
            '4.5'
        ),
        (
            '3',
            '../static/images/Course3.png',
            'Introduction to Cloud Computing with Azure',
            'Master Cloud Computing Concepts and Microsoft Azure fundamentals to start your cloud transformation journey.',
            '$100',
            '$90',
            '4.5'
        ),
        (
            '4',
            '../static/images/Course4.png',
            'Data Science: Machine Learning with Python',
            'Learn Data Science with Data Parsing, Data Visualization, Data Processing, Supervised & Unsupervised Machine Learning.',
            '$100',
            '$90',
            '4.5'
        ),
        (
            '5',
            '../static/images/Course5.png',
            'Python Programming for beginners',
            'A practical Python masterclass that teaches the fundamentals of the language using real-world examples, projects, and reference code.',
            '$100',
            '$90',
            '4.5'
        ),
        (
            '6',
            '../static/images/Course6.png',
            'The Complete SQL Bootcamp',
            'This search-course teaches the fundamentals of SQL using real-world examples, projects, starting from beginner level.',
            '$100',
            '$90',
            '4.5'
        ),
        (
            '7',
            '../static/images/Course7.png',
            'SQL for Developers and Analysts with MS SQL Server',
            'Guide for beginners to intermediate using real life examples. Hands-on learning of SQL and databases using Microsoft SQL Server.',
            '$100',
            '$90',
            '4.5'
        ),
        (
            '8',
            '../static/images/Course8.png',
            'C# Basics for Beginners: Learn C# Fundamentals by Coding',
            'Learn the fundamentals of C# and .NET Framework. Master C# fundamentals and debug C# applications effectively',
            '$100',
            '$90',
            '4.5'
        ),
    ]

c.executemany("""
INSERT INTO courses 
VALUES 
(?, ?, ?, ?, ?, ?, ?)
""", courses)

conn.commit()

print("Created courses table successfully!")

c.execute("""
DROP TABLE IF EXISTS users;
""")

c.execute("""
CREATE TABLE users (
    name TEXT, 
    email TEXT, 
    password TEXT
    )
""")

conn.commit()

print("Created users table successfully!")

c.execute("""
DROP TABLE IF EXISTS leads;
""")

c.execute("""
CREATE TABLE leads (
    name TEXT, 
    email TEXT, 
    subject TEXT,
    message TEXT
    )
""")

conn.commit()

print("Created leads table successfully!")

c.execute("""
DROP TABLE IF EXISTS cart;
""")

c.execute("""
CREATE TABLE cart (
    id TEXT, 
    image TEXT, 
    name TEXT, 
    description TEXT, 
    price TEXT, 
    discounted_price TEXT, 
    rating TEXT)
""")


conn.close()