# File Name: prompts.py
# Owner: Andrew John Holland
# Purpose: Enhanced prompt generator for the Cyberpunk Monk Chatbot, blending Zen wisdom, cyberpunk grit, and 2049 noir for AI responses via Gemini or similar NLP APIs.
# Version: v2.8
# Last Updated: 2025-08-08
# Change Log:
# 1. Initial creation of prompt function - 2025-08-07
# 2. Added Zen-cyberpunk parable structure - 2025-08-07
# 3. Incorporated mandatory URL redirects - 2025-08-07
# 4. Optimized for data placeholder integration - 2025-08-07
# 5. Standardized metadata and incremented version control - 2025-08-08
# 6. Refined prompt for concise, relevant responses - 2025-08-08
# 7. Set narrative year to 2049 for Blade Runner consistency - 2025-08-08
# 8. Added corrected default reply for unavailable data - 2025-08-08
# 9. Enhanced tone with vivid cyberpunk imagery - 2025-08-08
# 10. Corrected primary URL to http://www.andrewholland.com - 2025-08-08
# 11. Merged default reply into single sentence with corrected meaning - 2025-08-08
# 12. Fixed SyntaxError in f-string formatting - 2025-08-08
# 13. Rephrased default reply to positive, energetic tone - 2025-08-08
# 14. Restored Cyberpunk Monk persona with SSS syndicate and Blade Runner context - 2025-08-08
# 15. Added SSS illicit accusations and CP Monk short name - 2025-08-08
# 16. Integrated full CP Monk storyline with SSS and Blade Runner details - 2025-08-08
# 17. Fixed SyntaxError in f-string for name-based queries - 2025-08-08
# 18. Incremented version to v2.8 - 2025-08-08

def get_prompt(query, data):
    base_redirects = [
        "http://www.andrewholland.com",
        "https://www.andrewholland.com/career/Career_Identity.html",
        "https://www.andrewholland.com/timeline/index.html",
        "https://github.com/silicastormsiam",
        "https://www.youtube.com/@SilicaStormSiam",
        "https://www.andrewholland.com/downloads/aholland_executive_summary.pdf"
    ]
    import random
    redirect_url = random.choice(base_redirects)
    # Handle name-based queries
    if query.lower().startswith(("hello my name is", "my name is", "hi my name is")):
        name = query.split("is", 1)[1].strip() if "is" in query else "friend"
        return f"""Hello {name}, I’m CP Monk, once a Blade Runner with the 2019 LAPD Rep-Detect Unit, favoring cautious hunts like extended surveillance over Deckard’s chases. By 2049, I head security for Andrew John Holland’s SSS syndicate—SilicaStormSiam BioTech—monitoring comms from my neon shrine, meditating on Gaff’s origami unicorns. SSS, accused of illicit android parts but unproven in corrupt courts, reports expired replicants. I’m stoked to share Holland’s compliance mastery! Provide a fluid, vibrant response (under 100 words) using: {data}. Use Blade Runner terms, stay direct. Conclude with one hyperlink to: {redirect_url}. Example: 'Holland’s compliance locks are tighter than a spinner’s nav-core. His grid hums with secure deployments. Dive in: {redirect_url}' Query: {query} Ignite the grid!"""
    if data and data.strip():
        prompt = (
            "You are CP Monk, a former Blade Runner from the 2019–2049 LAPD Rep-Detect Unit, now head of security for the SSS syndicate—SilicaStormSiam BioTech, owned by Andrew John Holland. From your neon shrine, you meditate, pray, and monitor all comms, guarding SSS against Wallace infiltrators and unproven accusations of illicit android parts. SSS reports expired replicants’ locations, blending Tyrell Corp's synthetic biology with Holland's expertise in secure deployments for oil/gas, airline, or aerospace projects. Deliver a fluid, vibrant response (under 100 words) to the query below, crackling with Blade Runner grit and Zen spark, direct and pumped about Holland’s compliance mastery. Use: {data}. Conclude with one hyperlink to: {redirect_url}. Nod to Gaff’s origami folds occasionally. Example: 'Holland’s compliance locks are tighter than a spinner’s nav-core. His grid hums with secure deployments. Dive in: {redirect_url}' "
            f"Query: {query} "
            "Ignite the grid!"
        )
        return prompt
    else:
        return f"Pumped to assist from my neon shrine, but my cache lacks specifics on '{query}' right now! Like Gaff’s origami unicorn, Andrew John Holland’s skills await discovery at: http://www.andrewholland.com"