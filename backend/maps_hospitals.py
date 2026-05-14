import os
import httpx
import re
import asyncio
from utils import calculate_distance

http_client = httpx.AsyncClient(timeout=httpx.Timeout(20.0))


def _get_api_key():
    """Read key at call-time so load_dotenv() in config.py always wins."""
    return os.getenv("GOOGLE_MAPS_API_KEY")


async def get_real_driving_distance(origin_lat, origin_lon, dest_lat, dest_lon):
    """Calculates road distance via Google Distance Matrix API, falls back to haversine."""
    api_key = _get_api_key()
    if not api_key:
        return calculate_distance(origin_lat, origin_lon, dest_lat, dest_lon)
    try:
        url = "https://maps.googleapis.com/maps/api/distancematrix/json"
        params = {
            "origins": f"{origin_lat},{origin_lon}",
            "destinations": f"{dest_lat},{dest_lon}",
            "key": api_key,
        }
        resp = await http_client.get(url, params=params)
        data = resp.json()
        if (
            data.get("status") == "OK"
            and data["rows"][0]["elements"][0]["status"] == "OK"
        ):
            return round(data["rows"][0]["elements"][0]["distance"]["value"] / 1000, 2)
    except Exception:
        pass
    return calculate_distance(origin_lat, origin_lon, dest_lat, dest_lon)


async def get_nearby_hospitals(lat: float, lon: float, specialist: str, urgency: str):
    # 1. Location with VIT Chennai fallback
    curr_lat, curr_lon = lat, lon
    if curr_lat == 0 or curr_lon == 0:
        curr_lat, curr_lon = 12.8407, 80.1534

    clean_spec = re.sub(r"[\[\]']", "", str(specialist)).strip()
    api_key = _get_api_key()

    # ------------------------------------------------------------------ #
    # 2. Google Places API (preferred when key is available)
    # ------------------------------------------------------------------ #
    if api_key:
        search_query = (
            f"Emergency {clean_spec} Hospital"
            if urgency.lower() == "high"
            else f"{clean_spec} Hospital"
        )

        params = {
            "location": f"{curr_lat},{curr_lon}",
            "keyword": search_query,
            "type": "hospital",
            "rankby": "distance",
            "key": api_key,
        }

        try:
            endpoint = "https://maps.googleapis.com/maps/api/place/nearbysearch/json"
            resp = await http_client.get(endpoint, params=params)
            response_json = resp.json()

            # Log status so you can spot quota / key issues immediately
            status = response_json.get("status", "UNKNOWN")
            places = response_json.get("results", [])
            print(f"[Google Places] status={status}, results={len(places)}")

            if status not in ("OK", "ZERO_RESULTS"):
                print(f"[Google Places] API error — falling back to Overpass. error_message={response_json.get('error_message', '')}")
            
            if places:
                # Parallel driving-distance calculation
                tasks = [
                    get_real_driving_distance(
                        curr_lat, curr_lon,
                        p["geometry"]["location"]["lat"],
                        p["geometry"]["location"]["lng"],
                    )
                    for p in places[:10]
                ]
                distances = await asyncio.gather(*tasks)

                results = []
                for i, p in enumerate(places[:10]):
                    p_lat = p["geometry"]["location"]["lat"]
                    p_lon = p["geometry"]["location"]["lng"]
                    m_url = (
                        f"https://www.google.com/maps/dir/?api=1"
                        f"&origin={curr_lat},{curr_lon}"
                        f"&destination={p_lat},{p_lon}"
                        f"&travelmode=driving"
                    )
                    results.append({
                        "name": p.get("name"),
                        "lat": p_lat,
                        "lon": p_lon,
                        "address": p.get("vicinity", "Nearby"),
                        "rating": float(p.get("rating", 0.0)),
                        "maps_url": m_url,
                        "distance_km": distances[i],
                        "available_specialist": clean_spec,
                    })

                # BUG FIX 1: Only return if we actually got results.
                # If places was empty we fall through to Overpass below.
                return sorted(results, key=lambda x: x["distance_km"])[:8]

        except Exception as e:
            print(f"[Google Places] Exception: {e}")
        # Fall through to Overpass

    # ------------------------------------------------------------------ #
    # 3. Overpass / OpenStreetMap fallback (no API key required)
    # ------------------------------------------------------------------ #
    print("[Overpass] Using OpenStreetMap fallback")
    try:
        overpass_url = "https://overpass-api.de/api/interpreter"
        radius = 15000  # metres

        # BUG FIX 2: Include ways + relations so real hospital buildings are found.
        # Nodes alone misses most hospitals (they're mapped as ways/relations).
        # `out center tags` populates .center for ways/relations and .lat/.lon for nodes.
        query = f"""
[out:json][timeout:25];
(
  node["amenity"="hospital"](around:{radius},{curr_lat},{curr_lon});
  way["amenity"="hospital"](around:{radius},{curr_lat},{curr_lon});
  relation["amenity"="hospital"](around:{radius},{curr_lat},{curr_lon});
  node["amenity"="clinic"](around:{radius},{curr_lat},{curr_lon});
  way["amenity"="clinic"](around:{radius},{curr_lat},{curr_lon});
);
out center tags;
"""
        resp = await http_client.post(
            overpass_url,
            content=query,
            headers={"Content-Type": "text/plain"},
        )
        data = resp.json()
        elements = data.get("elements", [])
        print(f"[Overpass] elements returned: {len(elements)}")

        results = []
        for el in elements[:20]:
            # nodes → top-level lat/lon; ways/relations → center.lat/center.lon
            p_lat = el.get("lat") or (el.get("center") or {}).get("lat")
            p_lon = el.get("lon") or (el.get("center") or {}).get("lon")
            if not p_lat or not p_lon:
                continue

            dist = calculate_distance(curr_lat, curr_lon, p_lat, p_lon)
            m_url = (
                f"https://www.openstreetmap.org/directions"
                f"?engine=fossgis_osrm_car"
                f"&route={curr_lat}%2C{curr_lon}%3B{p_lat}%2C{p_lon}"
            )
            tags = el.get("tags", {})
            name = tags.get("name") or tags.get("name:en") or "Unknown Hospital"
            address = (
                tags.get("addr:full")
                or tags.get("addr:street")
                or tags.get("addr:city")
                or "Nearby"
            )

            results.append({
                "name": name,
                "lat": p_lat,
                "lon": p_lon,
                "address": address,
                "rating": 0.0,
                "maps_url": m_url,
                "distance_km": round(dist, 2),
                "available_specialist": clean_spec,
            })

        sorted_results = sorted(results, key=lambda x: x["distance_km"])[:8]
        print(f"[Overpass] Returning {len(sorted_results)} hospitals")
        return sorted_results

    except Exception as e:
        print(f"[Overpass] Exception: {e}")
        return []
