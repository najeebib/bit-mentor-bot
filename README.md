# Bit Mentor Bot

## Table of Contents
- [Team Members](#team-members)
- [Overview](#overview)
- [Architecture](#architecture)
- [Technologies](#technologies)
- [Workflow](#workflow)

## Team Members
- **Muhammad Sarahni**
- **Adam Kaabiya**
- **Najeeb Ibrahim**
- **Maysa Zbidat**
- **Aseel Khamis**

## Overview
The Bit Mentor Bot is a Telegram bot designed to interact with users by asking questions and providing answers in a multiple-choice question (MCQ) format. It communicates with a backend server to fetch questions and submit answers.

## Architecture

### Components
1. **python-telegram-bot**:
    - A Python library that allows the bot to interact with Telegram users, handling messaging and commands.
2. **FastAPI Server**:
    - The backend server that the bot communicates with to fetch and submit questions and answers. (Hosted in a separate repository)

### Diagram
The bot part is our reposotory, but the diagram entails the entire project
![bot](https://github.com/user-attachments/assets/8f0ff1d0-58c1-48ef-a2dc-343d8de97c26)



### General Architecture
- **Telegram Bot**: Interacts with users, sending and receiving messages through the `python-telegram-bot` library.
- **FastAPI Server**: Handles requests from the Telegram bot, processes them, and returns appropriate responses (detailed in the separate server repository).

## Workflow

1. **User Interaction**:
    - Users interact with the Telegram bot by sending messages and commands.
2. **API Requests**:
    - The Telegram bot sends API requests to the FastAPI server to fetch questions and submit answers.
3. **Response**:
    - The FastAPI server processes these requests and sends appropriate responses back to the Telegram bot, which then communicates these responses to the user.

## Technologies

- **Bot Framework**: [python-telegram-bot](https://python-telegram-bot.org/)
- **Backend Server**: [FastAPI](https://fastapi.tiangolo.com/) (details in separate repository)
- **Hosting**: [AWS](https://aws.amazon.com/)

