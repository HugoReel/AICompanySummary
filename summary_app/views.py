from django.shortcuts import render
from duckduckgo_search import DDGS
import os
from dotenv import load_dotenv
import google.generativeai as genai

# Load environment variables from the .env file
load_dotenv()

# Configure the Gemini API with the key stored in .env
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

# Create an instance of the Gemini 1.5 Pro model
model = genai.GenerativeModel("models/gemini-1.5-pro-latest")


def search_duckduckgo(query, max_results):
    """
    Searches DuckDuckGo for a given query and returns a list of snippet bodies.
    """
    results = []
    with DDGS() as ddgs:
        for result in ddgs.text(query, max_results=max_results):
            if 'body' in result:
                results.append(result['body'])  # Add the text body of each result
    return results


def summarise_text_with_gemini(snippets, company_name):
    """
    Sends the combined text snippets to the Gemini model to generate a summary.
    """
    combined_text = "\n".join(snippets)  # Join all snippets into one string
    prompt = (
        f"Provide a short and informative overview about the company '{company_name}' "
        f"based on the following information:\n\n{combined_text} and the year they was established"
    )

    try:
        # Generate the summary using Gemini
        response = model.generate_content(prompt)
        return response.text if hasattr(response, "text") else "No summary text was generated."
    except Exception as e:
        # Handle API or generation errors
        print(f"Error during summarization: {e}")
        return f"There was an error generating the summary: {str(e)}"


def company_input(request):
    """
    Handles the form input from the homepage, performs the search, and displays the summary.
    """
    overview = None

    if request.method == "POST":
        company_name = request.POST.get("company_name")  # Get user input from the form
        snippets = search_duckduckgo(company_name, max_results=5)

        if snippets:
            overview = summarise_text_with_gemini(snippets, company_name)
        else:
            overview = "No relevant search results found."

    # Render the homepage with the summary (if available)
    return render(request, "homepage.html", {"overview": overview})
