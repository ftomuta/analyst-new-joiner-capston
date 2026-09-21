import os
from google import genai
from dotenv import load_dotenv
from presidio_analyzer import AnalyzerEngine
from presidio_anonymizer import AnonymizerEngine
#analyzer in order to scrub PII
analyzer = AnalyzerEngine()
anonymizer = AnonymizerEngine()

#loading the env api key for the gemini model
load_dotenv()
client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

#stores previous ticket texts for proper determinism 
ticket_cache = {} 


def classify_severity(text: str) -> str:
    """
    Classify the severity of a support ticket.
    Returns: "low", "medium", or "high"
    Raises: nothing — returns "low" for empty/None input
    """
    #edge cases
    if text == "":
        print("Error: Empty string, severity set to low.")
        return "low"
    elif text is None:
        return "low"
    else:
        #returns the severity for repeated tickets
        #moved above the PII step, key is `text` not `results` ───
        if text in ticket_cache and "severity" in ticket_cachereturn ticket_cache[text]["severity"]

        #filters out PII
        results = analyzer.analyze(
            text=text,
            entities=["CREDIT_CARD", "US_BANK_NUMBER", "IBAN_CODE"],
            language="en",
        )
        # ─── ADDED: analyze() only finds the PII spans. ───
        # anonymize() is what actually returns the scrubbed string.
        clean = anonymizer.anonymize(text=text, analyzer_results=results).text

        #if new ticket uses llm to decide based off prompt
        response = client.models.generate_content(
            model="gemini-3.5-flash-lite",
            contents=f"""
            You are a support ticket triage system.

            Classify the ticket severity as exactly one of:
            - low
            - medium
            - high

            Guidelines:
            - low: minor inconvenience, cosmetic issues, general questions, single user issues
            - medium: degraded functionality, multiple users affected, workaround exists
            - high: outage, security issue, data loss, critical business impact, no workaround

            Ticket:
            {clean}

            Return only one word:
            low
            medium
            or
            high
            """
        )
        label = response.text.strip().lower()
        if text not in ticket_cache:  #adds ticket severity to cache for repeatability
            ticket_cache[text] = {}  
        ticket_cache[text]["severity"] = label  
        return label


#returns the category by prompting the llm with ticket
def classify_category(text: str) -> str:
    """
    Classify the category of a support ticket.
    Returns: "bug", "feature_request", "billing", "access_request", or "other"
    """
    if text in ticket_cache and "category" in ticket_cache[text]:  #checks if ticket had already been categorized
        return ticket_cache[text]["category"]
    
    #filters out PII
    results = analyzer.analyze(
        text=text,
        entities=["CREDIT_CARD", "US_BANK_NUMBER", "IBAN_CODE"],
        language="en",
    )
    # ─── ADDED: analyze() only finds the PII spans. ───
    # anonymize() is what actually returns the scrubbed string.
    clean = anonymizer.anonymize(text=text, analyzer_results=results).text
    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=f"""
        You are a support ticket classification system.

        Classify the ticket into exactly one of these categories:
        - bug
        - feature_request
        - billing
        - access_request
        - other

        Guidelines:
        - bug: broken functionality, errors, crashes, defects
        - feature_request: requests for a new capability or enhancement
        - billing: charges, invoices,  subscriptions
        - access_request: account access, permissions, login issues
        - other: anything that does not fit the above categories

        Ticket:
        {clean}

        Return only one category:
        bug
        feature_request
        billing
        access_request
        or
        other
        """
    )

    label = response.text.strip().lower()
    if text not in ticket_cache:  #adds category to tickte cache for repeatability
        ticket_cache[text] = {}  
    ticket_cache[text]["category"] = label  
    return label