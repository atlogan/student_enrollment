# Student Management System

A Django-based student management system that allows for managing students, instructors, courses, classes, and enrollments. This project implements full CRUD (Create, Read, Update, Delete) operations for the Student model.

## CRUD Implementation

The CRUD operations have been implemented for the `Student` model, which includes the following fields:
- Name
- Major
- Enrollment Date

## Base URL Path

The application's views can be accessed at the root URL `/`. The following endpoints are available:

- List all students: `/`
- View student details: `/<student_id>`
- Create new student: `/create/`
- Update student: `/<student_id>/update/`
- Delete student: `/<student_id>/delete/`

## Navigation Instructions

### Viewing Students
1. Access the home page (`/`) to see a list of all students
2. Click on any student's name to view their details

### Creating a New Student
1. From the student list page, click the "Add Student" button
2. Fill in the required information:
   - Name
   - Major
   - Enrollment Date (e.g. 2023-05-01)
3. Click "Save" to create the new student record

### Updating Student Information
1. From a student's detail page, click the "Edit" button
2. Modify the desired fields
3. Click "Save" to save the changes

### Deleting a Student
1. From a student's detail page, click the "Delete" button
2. Confirm the deletion on the confirmation page

## Project Structure

The project includes the following models:
- Student: For managing student information
- Instructor: For managing instructor information
- Course: For managing course information
- Class: For managing class schedules and assignments
- Enrollment: For managing student enrollments in classes

## Technical Details

- Built with Django 5.2
- Uses Class-Based Generic Views for CRUD operations
- Uses Postgres database 