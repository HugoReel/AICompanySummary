from django.shortcuts import render
from duckduckgo_search import DDGS
import os
from dotenv import load_dotenv
import google.generativeai as genai

load_dotenv()


genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
model = genai.GenerativeModel("models/gemini-1.5-pro-latest")

def search_duckduckgo(query, max_results):
    results = []
    with DDGS() as ddgs:
        for result in ddgs.text(query, max_results=max_results):
            if 'body' in result:
                results.append(result['body'])
    return results


def summarise_text_with_gemini(snippets, company_name):
    combined_text = "\n".join(snippets)
    prompt = (
        f"Provide a short and informative overview about the company '{company_name}' "
        f"based on the following information:\n\n{combined_text} and the year they was established"
    )

    try:
        response = model.generate_content(prompt)
        return response.text if hasattr(response, "text") else "No summary text was generated."
    except Exception as e:
        print(f"Error during summarization: {e}")
        return f"There was an error generating the summary: {str(e)}"


def company_input(request):
    overview = None

    if request.method == "POST":
        company_name = request.POST.get("company_name")
        snippets = search_duckduckgo(company_name, max_results=5)

        if snippets:
            overview = summarise_text_with_gemini(snippets, company_name)
        else:
            overview = "No relevant search results found."

    return render(request, "homepage.html", {"overview": overview})

