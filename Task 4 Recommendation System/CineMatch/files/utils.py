import os
from PIL import Image, ImageDraw, ImageFont
import customtkinter as ctk

def get_movie_poster(movie_title, size=(150, 225), callback=None):
    """
    Generates a fallback movie poster image using PIL if no real poster is present.
    Creates a Netflix-style dark placeholder with the movie title.
    """
    safe_title = "".join([c for c in movie_title if c.isalpha() or c.isdigit() or c==' ']).strip()
    posters_dir = os.path.join(os.path.dirname(__file__), "posters")
    os.makedirs(posters_dir, exist_ok=True)
    poster_path = os.path.join(posters_dir, f"{safe_title}.jpg")
    
    def _create_placeholder():
        # Generate fallback
        bg_color = "#2b2b2b"
        img = Image.new('RGB', size, color=bg_color)
        draw = ImageDraw.Draw(img)
        
        try:
            font = ImageFont.truetype("arial.ttf", int(size[0] * 0.12))
        except IOError:
            font = ImageFont.load_default()
            
        import textwrap
        lines = textwrap.wrap(movie_title, width=15)
        
        total_height = 0
        line_heights = []
        for line in lines:
            try:
                bbox = draw.textbbox((0, 0), line, font=font)
                h = bbox[3] - bbox[1]
            except AttributeError:
                _, h = draw.textsize(line, font=font)
            line_heights.append(h + 5)
            total_height += h + 5
            
        y = (size[1] - total_height) / 2
        
        for i, line in enumerate(lines):
            try:
                bbox = draw.textbbox((0, 0), line, font=font)
                w = bbox[2] - bbox[0]
            except AttributeError:
                w, _ = draw.textsize(line, font=font)
                
            x = (size[0] - w) / 2
            draw.text((x, y), line, fill=(255, 255, 255), font=font)
            y += line_heights[i]
            
        return ctk.CTkImage(light_image=img, dark_image=img, size=size)

    if os.path.exists(poster_path):
        try:
            img = Image.open(poster_path)
            return ctk.CTkImage(light_image=img, dark_image=img, size=size)
        except Exception:
            pass

        
    placeholder_img = _create_placeholder()
    
    if callback is not None:
        import threading
        import urllib.request
        import json
        
        def fetch_poster():
            # If already exists, we handled it. If not, fetch it.
            if not os.path.exists(poster_path):
                try:
                    # Search TMDB
                    api_key = "8265bd1679663a7ea12ac168da84d2e8"
                    query = urllib.parse.quote(movie_title)
                    url = f"https://api.themoviedb.org/3/search/movie?api_key={api_key}&query={query}"
                    
                    req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
                    with urllib.request.urlopen(req, timeout=3) as resp:
                        data = json.loads(resp.read())
                        if data.get('results') and data['results'][0].get('poster_path'):
                            p_path = data['results'][0]['poster_path']
                            img_url = f"https://image.tmdb.org/t/p/w500{p_path}"
                            
                            req_img = urllib.request.Request(img_url, headers={'User-Agent': 'Mozilla/5.0'})
                            with urllib.request.urlopen(req_img, timeout=5) as img_resp:
                                with open(poster_path, 'wb') as f:
                                    f.write(img_resp.read())
                except Exception:
                    return # Keep placeholder
                    
            if os.path.exists(poster_path):
                try:
                    img = Image.open(poster_path)
                    new_ctk_img = ctk.CTkImage(light_image=img, dark_image=img, size=size)
                    callback(new_ctk_img)
                except Exception:
                    pass
                    
        threading.Thread(target=fetch_poster, daemon=True).start()

    return placeholder_img
