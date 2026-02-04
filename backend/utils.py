



import re, json, hashlib, math

def calculate_distance(lat1, lon1, lat2, lon2):
    R = 6371.0
    phi1, phi2 = math.radians(lat1), math.radians(lat2)
    dlat, dlon = math.radians(lat2-lat1), math.radians(lon2-lon1)
    a = math.sin(dlat/2)**2 + math.cos(phi1)*math.cos(phi2)*math.sin(dlon/2)**2
    return round(R * (2 * math.atan2(math.sqrt(a), math.sqrt(1-a))), 2)

def clean_ai_json(text: str):
    """Attempt robust JSON extraction from model output.

    1. Strip markdown fences (``` or ```json)
    2. Try direct json.loads
    3. Fallback to finding the first {...} block and load
    4. If that fails, try ast.literal_eval to handle single quotes
    """
    try:
        if not text or not isinstance(text, str):
            return None

        # 1. Strip markdown fences
        cleaned = re.sub(r"```(?:json)?\s?|\s?```", "", text).strip()

        # 2. Try direct JSON
        try:
            data = json.loads(cleaned)
        except Exception:
            # 3. Extract first JSON-like block
            start = cleaned.find('{')
            end = cleaned.rfind('}')
            if start == -1 or end == -1 or end <= start:
                data = None
            else:
                snippet = cleaned[start:end+1]
                try:
                    data = json.loads(snippet)
                except Exception:
                    # 4. Try ast.literal_eval as a last resort (handles single quotes)
                    import ast
                    try:
                        data = ast.literal_eval(snippet)
                    except Exception:
                        data = None

        if not data:
            return None

        if "specialist" in data:
            spec = data["specialist"]
            data["specialist"] = spec[0] if isinstance(spec, list) else spec

        return data
    except Exception:
        return None

def generate_cache_key(symptoms: str, latitude: float):
    symp_hash = hashlib.md5(symptoms.lower().strip().encode()).hexdigest()
    return f"triage_{symp_hash}_{round(latitude, 2)}"