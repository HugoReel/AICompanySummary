# Company Summary Web App

This Django web application allows users to input a company name and receive an AI-generated summary using live DuckDuckGo search results and Google's Gemini API.

## Features

- Uses DuckDuckGo to search for relevant company information
- Summarizes results using Google Gemini 1.5 Pro
- Simple web interface for input and output

## Tech Stack

- Python & Django
- [duckduckgo-search](https://pypi.org/project/duckduckgo-search/)
- [google-generativeai](https://ai.google.dev/)
- python-dotenv for secure API key handling

## Setting Up the API
To use this app, you need to provide your Google Gemini API key. For security, this key is stored in a `.env` file and loaded using `python-dotenv`.
Create a `.env` file

In the project root directory, create a file named `.env` (if it doesn't already exist).
replace your_gemini_api_key_here with your generated key.
GOOGLE_API_KEY=your_gemini_api_key_here
