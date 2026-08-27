from pathlib import Path
import re
import math
import random
from PIL import Image, ImageDraw, ImageFont, ImageFilter

# ==============================
# تنظیمات ثابت
# ==============================
WIDTH = 1080
HEIGHT = 1080
LINE_SPACING_FACTOR = 1.3
INDENT_SIZE = 40
FONT_DIR = Path("fonts/")

# ==============================
# دیکشنری فونت‌ها
# ==============================
FONTS = {
    "fa": {
        "Shabnam": FONT_DIR / "Shabnam.ttf",
        "Shabnam-Bold": FONT_DIR / "Shabnam-Bold.ttf",
        "Shabnam-Light": FONT_DIR / "Shabnam-Light.ttf",
        "Sahel": FONT_DIR / "Sahel.ttf",
        "Sahel-Bold": FONT_DIR / "Sahel-Bold.ttf",
    },
    "en": {
        "Inter": FONT_DIR / "Inter Regular.otf",
        "Inter-Bold": FONT_DIR / "Inter Bold.otf",
        "Merriweather": FONT_DIR / "Merriweather_24pt-Regular.ttf",
        "Merriweather-Bold": FONT_DIR / "Merriweather_24pt-Bold.ttf",
        "JetBrainsMono": FONT_DIR / "JetBrainsMono-VariableFont_wght.ttf",
    }
}

# ==============================
# تم‌ها
# ==============================
THEMES = {
    "Classic Ivory": {
        "bg": (247, 243, 234), "gradient": None,
        "border": (70, 70, 75), "border_width": 3,
        "text": (33, 37, 41), "dots": (220, 210, 190),
        "grain_opacity": 3, "paper_texture": True,
        "font_fa": "Shabnam", "font_en": "Merriweather"
    },
    "Dark": {
        "bg": (22, 24, 29), "gradient": None,
        "border": (192, 154, 74), "border_width": 3,
        "text": (248, 246, 242), "dots": (90, 90, 90),
        "grain_opacity": 0, "gold_lines": True,
        "vignette": (0, 0, 0, 30),
        "font_fa": "Sahel", "font_en": "Inter"
    },
    "Navy": {
        "bg": (16, 40, 78), "gradient": None,
        "border": (90, 200, 255), "border_width": 3,
        "text": (248, 250, 252), "grid": (100, 170, 255),
        "grid_opacity": 10, "accent": (0, 170, 255),
        "font_fa": "Sahel", "font_en": "Inter"
    },
    "Forest": {
        "bg": (24, 53, 42), "gradient": None,
        "border": (114, 160, 132), "border_width": 3,
        "text": (247, 243, 233), "accent": (185, 165, 92),
        "grain_opacity": 5, "paper_texture": True,
        "green_dots": (60, 110, 80),
        "font_fa": "Shabnam", "font_en": "Merriweather"
    },
    "Wine": {
        "bg": (63, 29, 40), "gradient": "radial",
        "gradient_center": (70, 35, 45),
        "gradient_edge": (48, 20, 32),
        "border": (194, 166, 96), "border_width": 3,
        "text": (248, 242, 228), "gold_lines_opacity": 25,
        "font_fa": "Shabnam", "font_en": "Merriweather"
    },
    "Slate": {
        "bg": (236, 239, 241), "gradient": None,
        "border": (96, 125, 139), "border_width": 3,
        "text": (38, 50, 56), "accent": (255, 138, 101),
        "dot_grid": True, "concrete_texture": True,
        "font_fa": "Sahel", "font_en": "Inter"
    },
    "Paper": {
        "bg": (247, 243, 234), "gradient": None,
        "border": (98, 76, 60), "border_width": 3,
        "text": (59, 49, 42), "paper_fibers": True,
        "grain_opacity": 5,
        "font_fa": "Shabnam", "font_en": "Merriweather"
    },
    "Blueprint": {
        "bg": (18, 59, 109), "gradient": None,
        "border": (255, 255, 255), "border_width": 3,
        "text": (250, 250, 250), "accent": (92, 200, 255),
        "grid_size": 40, "dash_lines": True,
        "coordinate_marks": True,
        "font_fa": "Sahel", "font_en": "JetBrainsMono"
    },
    "Monochrome": {
        "bg": (255, 255, 255), "gradient": None,
        "border": (120, 120, 120), "border_width": 3,
        "text": (17, 17, 17), "dot_grid": True,
        "grain_opacity": 4,
        "font_fa": "Shabnam", "font_en": "Inter"
    },
    "Modern Tech": {
        "bg": (250, 250, 250), "gradient": "linear",
        "gradient_top": (252, 252, 252),
        "gradient_bottom": (244, 246, 248),
        "border": (59, 130, 246), "border_width": 3,
        "text": (31, 41, 55), "secondary_text": (107, 114, 128),
        "accent": (96, 165, 250), "dot_grid_opacity": 8,
        "glass_highlight": True,
        "font_fa": "Sahel", "font_en": "Inter"
    }
}

# ==============================
# توابع کمکی
# ==============================
def is_persian(text):
    for char in text:
        if "\u0600" <= char <= "\u06FF":
            return True
    return False

def detect_direction(text):
    """
    اگر حداقل یک کاراکتر فارسی/عربی در متن باشد، 'rtl' برگردان، در غیر این صورت 'ltr'.
    """
    for ch in text:
        if '\u0600' <= ch <= '\u06FF' or '\uFB50' <= ch <= '\uFDFF' or '\uFE70' <= ch <= '\uFEFF':
            return 'rtl'
    return 'ltr'

def prepare_text(text):
    """
    بدون reshape و bidi - فقط متن را برمی‌گرداند
    فونت فارسی خودش حروف را وصل می‌کند
    """
    return text

def get_font_path(text, font_fa_override=None, font_en_override=None, theme=None):
    is_fa = is_persian(text)
    if is_fa:
        if font_fa_override and font_fa_override in FONTS["fa"]:
            return FONTS["fa"][font_fa_override]
        elif theme and theme.get("font_fa") in FONTS["fa"]:
            return FONTS["fa"][theme["font_fa"]]
        else:
            return FONTS["fa"]["Shabnam"]
    else:
        if font_en_override and font_en_override in FONTS["en"]:
            return FONTS["en"][font_en_override]
        elif theme and theme.get("font_en") in FONTS["en"]:
            return FONTS["en"][theme["font_en"]]
        else:
            return FONTS["en"]["Inter"]

def get_line_spacing(font):
    return int(font.size * LINE_SPACING_FACTOR)

def sanitize_theme_name(theme_name):
    return theme_name.replace(" ", "_")

def is_dark_theme(theme):
    bg_color = theme.get("bg", (255, 255, 255))
    brightness = (0.299 * bg_color[0] + 0.587 * bg_color[1] + 0.114 * bg_color[2])
    return brightness < 128

# ==============================
# توابع افکت‌های بصری
# ==============================
def apply_radial_gradient(img, center_color, edge_color):
    pixels = img.load()
    w, h = img.size
    cx, cy = w // 2, h // 2
    max_dist = math.hypot(cx, cy)
    for y in range(h):
        for x in range(w):
            dist = math.hypot(x - cx, y - cy) / max_dist
            dist = min(dist, 1.0)
            r = int(center_color[0] * (1 - dist) + edge_color[0] * dist)
            g = int(center_color[1] * (1 - dist) + edge_color[1] * dist)
            b = int(center_color[2] * (1 - dist) + edge_color[2] * dist)
            pixels[x, y] = (r, g, b)

def add_grain(image, opacity):
    if opacity <= 0:
        return
    pixels = image.load()
    w, h = image.size
    for _ in range(int(w * h * opacity / 100 * 1.5)):
        x, y = random.randint(0, w-1), random.randint(0, h-1)
        r, g, b = pixels[x, y]
        delta = random.randint(-8, 8)
        pixels[x, y] = (max(0,min(255,r+delta)), max(0,min(255,g+delta)), max(0,min(255,b+delta)))

def add_vignette(image, color_tuple):
    if not color_tuple:
        return
    w, h = image.size
    mask = Image.new('L', (w, h), 0)
    mask_draw = ImageDraw.Draw(mask)
    mask_draw.ellipse([(w*0.15, h*0.15), (w*0.85, h*0.85)], fill=255)
    mask = mask.filter(ImageFilter.GaussianBlur(radius=w*0.3))
    dark_layer = Image.new('RGB', (w, h), color_tuple[:3])
    image.paste(dark_layer, (0, 0), mask)

def add_dot_grid(draw, w, h, color, spacing=40, opacity=10):
    color = tuple(list(color) + [int(255 * opacity / 100)])
    for x in range(0, w, spacing):
        for y in range(0, h, spacing):
            draw.point((x, y), fill=color)

def add_border(draw, w, h, color, width=3):
    for i in range(width):
        draw.rectangle([i, i, w-1-i, h-1-i], outline=color)

def add_paper_texture(image):
    add_grain(image, 3)

# ==============================
# توابع شکستن متن
# ==============================
def split_into_sentences(text):
    sentences = re.split(r'(?<=[.!?؟])\s+', text)
    return [s.strip() for s in sentences if s.strip()]

def chunk_text_by_sentences(content, min_words=80, max_words=100):
    raw_lines = content.split('\n')
    items = []
    para_num = 0
    
    for line in raw_lines:
        if line.strip() == "":
            para_num += 1
            continue
        
        sents = split_into_sentences(line)
        if not sents:
            items.append((para_num, line))
        else:
            for sent in sents:
                items.append((para_num, sent))
        para_num += 1
    
    if not items:
        return [(content, [0])]
    
    chunks = []
    current_chunk = []
    current_word_count = 0
    
    for para, sent in items:
        word_count = len(sent.split())
        
        if word_count > max_words:
            if current_chunk:
                chunks.append(current_chunk)
                current_chunk = []
                current_word_count = 0
            chunks.append([(para, sent)])
            continue
        
        if current_chunk and current_word_count + word_count > max_words:
            chunks.append(current_chunk)
            current_chunk = [(para, sent)]
            current_word_count = word_count
        else:
            current_chunk.append((para, sent))
            current_word_count += word_count
    
    if current_chunk:
        if current_word_count < min_words and chunks:
            last_chunk_word_count = sum(len(sent.split()) for _, sent in chunks[-1])
            if last_chunk_word_count + current_word_count <= max_words:
                chunks[-1].extend(current_chunk)
            else:
                chunks.append(current_chunk)
        else:
            chunks.append(current_chunk)
    
    if not chunks:
        chunks = [items]
    
    final_chunks = []
    for chunk in chunks:
        if not chunk:
            continue
        
        chunk_text = ""
        prev_para = chunk[0][0]
        first = True
        para_numbers = []
        
        for para, sent in chunk:
            para_numbers.append(para)
            if first:
                chunk_text = sent
                prev_para = para
                first = False
                continue
            
            if para != prev_para:
                chunk_text += "\n" + sent
                prev_para = para
            else:
                chunk_text += " " + sent
        
        chunk_text = chunk_text.strip()
        final_chunks.append((chunk_text, para_numbers))
    
    if not final_chunks:
        final_chunks = [(content, [0])]
    
    return final_chunks

def protect_number_colon(text):
    """
    الگوی عدد: کلمه را پیدا کرده و بین عدد: و کلمه‌ی بعدی یک ZWNJ (\u200C) قرار می‌دهد
    تا در حین شکستن خط، عدد و دو نقطه از کلمه جدا نشوند.
    مثال: "۱: علت" -> "۱:\u200Cعلت"
    """
    pattern = r'(\d+):\s+(\w+)'
    return re.sub(pattern, r'\1:' + '\u200C' + r'\2', text)

def wrap_text(draw, text, font, max_width):
    # محافظت از الگوی عدد: کلمه
    text = protect_number_colon(text)
    
    paragraphs = text.split("\n")
    final_lines = []
    for paragraph in paragraphs:
        if paragraph.strip() == "":
            final_lines.append("")
            continue
        
        words = paragraph.split()
        line = ""
        for word in words:
            test = word if line == "" else line + " " + word
            rtl = prepare_text(test)
            bbox = draw.textbbox((0, 0), rtl, font=font)
            width = bbox[2] - bbox[0]
            if width <= max_width:
                line = test
            else:
                final_lines.append(line)
                line = word
        if line:
            final_lines.append(line)
    return final_lines

def wrap_text_with_para_numbers(draw, text, font, max_width, para_numbers):
    parts = text.split('\n')
    all_lines = []
    para_index = 0
    
    for part in parts:
        if part.strip() == "":
            continue
        
        if para_index < len(para_numbers):
            current_para = para_numbers[para_index]
        else:
            current_para = para_numbers[-1] if para_numbers else 0
        
        lines = wrap_text(draw, part, font, max_width)
        para_dir = detect_direction(part)
        for line in lines:
            all_lines.append((line, current_para, para_dir))
        para_index += 1
    
    return all_lines

def find_best_font_size(draw, text, font_path, max_width, max_height, min_size=20, max_size=180):
    def fits(size):
        font = ImageFont.truetype(font_path, size)
        lines = wrap_text_with_para_numbers(draw, text, font, max_width, [0] * text.count('\n'))
        line_spacing = get_line_spacing(font)
        total_height = 0
        max_line_width = 0
        for line, _, _ in lines:
            if line.strip() == "":
                total_height += line_spacing
                continue
            rtl = prepare_text(line)
            bbox = draw.textbbox((0, 0), rtl, font=font)
            width = bbox[2] - bbox[0]
            height = bbox[3] - bbox[1]
            max_line_width = max(max_line_width, width)
            total_height += height
        if len(lines) > 1:
            total_height += line_spacing * (len(lines) - 1)
        return (max_line_width <= max_width and total_height <= max_height)

    left, right = min_size, max_size
    best = min_size
    while left <= right:
        mid = (left + right) // 2
        if fits(mid):
            best = mid
            left = mid + 1
        else:
            right = mid - 1
    return best

# ==============================
# تابع تشخیص موضوع (با ollama)
# ==============================
from random import sample
from re import findall

def Categorizing(content):
    topic_and_path = {file[:-4]:str(Path(root) / file) for root, dirs , files in Path('symbols').walk() for file in files}
    try:
        from ollama import chat
        topic_set = set(topic_and_path.keys())
        prompt_base = f'You are an expert in categorizing scientific content. I will send you a piece of scientific content and ask for your help in identifying its subject matter. I will provide a list of permitted topics, and I would like you to select topics relevant to the text. Please note these rules: 1: your response must include just the names. nothing more is acceptable. 2: you must select between 3 and 5 topic.  3: Important: Do NOT use synonyms or related terms. You MUST copy the exact names from the list below. If a concept matches something, but that things is not in the list, you must choose the closest existing name from the list or skip it. Only output the exact strings provided in the list. \n permitted topics: \n {topic_set}'
        special_prompt = f'now, categorize this content: \n {content}'
        messages = [{'role': 'system', 'content': prompt_base},{'role': 'user', 'content': special_prompt}]
        AI_respone = chat(model= 'gemma3:4b', messages= messages ,options={"temperature": 0.0})
        for x in range(3):
            AI_result = str(AI_respone.message.content).split()
            if len(set(AI_result).intersection(topic_set)) < 3:
                print("Invalid response (rule 3):", AI_respone.message.content)
                messages.append({'role':'user','content':f'You have used these topics, but they are not on the approved list: {set(AI_result).difference(topic_set)} Try harder, and this time, use *only* the approved list.'})
                AI_respone = chat(model= 'gemma3:4b', messages= messages ,options={"temperature": 0.0})
            else:
                break
        if len(set(AI_result).intersection(topic_set)) < 3:
            general_science = ({findall(r'symbols[\\/](.*)',str(root))[0]:files for root, dirs , files in Path('symbols').walk() if (findall(r'symbols[\\/](.*)',str(root)))!= []}.get('general_science'))
            random_result = sample(general_science, k=3)
            return[topic_and_path.get(topic[:-4]) for topic in random_result]
        return[topic_and_path.get(topic) for topic in set(AI_result).intersection(topic_set)]
    except Exception as e:
        print("Error occurred:", e)
        general_science = ({findall(r'symbols[\\/](.*)',str(root))[0]:files for root, dirs , files in Path('symbols').walk() if findall(r'symbols[\\/](.*)',str(root))!= []}.get('general_science'))
        random_result = sample(general_science, k=3)
        return[topic_and_path.get(topic[:-4]) for topic in random_result]

# ==============================
# توابع تزئینی (آیکون‌ها)
# ==============================
def get_symbol_area(layout):
    if layout == "image_left":
        return (0, 0, int(WIDTH * 0.35), HEIGHT)
    elif layout == "image_right":
        return (int(WIDTH * 0.65), 0, WIDTH, HEIGHT)
    elif layout == "image_top":
        return (0, 0, WIDTH, int(HEIGHT * 0.30))
    elif layout == "image_bottom":
        return (0, int(HEIGHT * 0.70), WIDTH, HEIGHT)
    else:
        return (0, 0, WIDTH, HEIGHT)

def recolor_symbol(symbol_img, target_color):
    symbol_img = symbol_img.convert("RGBA")
    data = symbol_img.getdata()
    new_data = []
    for item in data:
        if item[3] > 0:
            new_data.append((target_color[0], target_color[1], target_color[2], item[3]))
        else:
            new_data.append(item)
    symbol_img.putdata(new_data)
    return symbol_img

def is_overlapping_text(x, y, size, text_bbox, margin=20):
    icon_bbox = (x - margin, y - margin, x + size + margin, y + size + margin)
    if icon_bbox[0] < text_bbox[2] and icon_bbox[2] > text_bbox[0] and icon_bbox[1] < text_bbox[3] and icon_bbox[3] > text_bbox[1]:
        return True
    return False

def draw_decorative_symbols(img, symbol_paths, text_bbox, theme, layout):
    if not symbol_paths or len(symbol_paths) == 0:
        return
    
    is_dark = is_dark_theme(theme)
    
    if is_dark:
        opacity = 0.55
        theme_name = theme.get("name", "")
        if "Dark" in theme_name:
            target_color = (192, 154, 74)
        elif "Wine" in theme_name:
            target_color = (194, 166, 96)
        elif "Navy" in theme_name:
            target_color = (0, 170, 255)
        elif "Forest" in theme_name:
            target_color = (185, 165, 92)
        elif "Blueprint" in theme_name:
            target_color = (92, 200, 255)
        else:
            target_color = (200, 200, 200)
    else:
        opacity = 0.25
        target_color = None
    
    symbol_area = get_symbol_area(layout)
    area_x1, area_y1, area_x2, area_y2 = symbol_area
    
    symbol_size = 65
    spacing = 25
    margin = 30
    
    cols = int((area_x2 - area_x1 - margin * 2 + spacing) // (symbol_size + spacing))
    rows = int((area_y2 - area_y1 - margin * 2 + spacing) // (symbol_size + spacing))
    
    cols = max(1, min(cols, 8))
    rows = max(1, min(rows, 8))
    
    positions = []
    for row in range(rows):
        for col in range(cols):
            x = area_x1 + margin + col * (symbol_size + spacing)
            y = area_y1 + margin + row * (symbol_size + spacing)
            
            x += random.randint(-8, 8)
            y += random.randint(-8, 8)
            
            x = max(area_x1 + 10, min(area_x2 - symbol_size - 10, x))
            y = max(area_y1 + 10, min(area_y2 - symbol_size - 10, y))
            
            if is_overlapping_text(x, y, symbol_size, text_bbox):
                continue
            
            positions.append((x, y))
    
    if len(positions) < 5:
        positions = []
        step_x = (area_x2 - area_x1 - symbol_size) // 4
        step_y = (area_y2 - area_y1 - symbol_size) // 4
        for row in range(3):
            for col in range(3):
                x = area_x1 + 20 + col * step_x
                y = area_y1 + 20 + row * step_y
                if not is_overlapping_text(x, y, symbol_size, text_bbox):
                    positions.append((x, y))
    
    random.shuffle(positions)
    
    for x, y in positions:
        symbol_path = random.choice(symbol_paths)
        if not Path(symbol_path).exists():
            continue
        
        try:
            symbol_img = Image.open(symbol_path).convert("RGBA")
            symbol_img = symbol_img.resize((symbol_size, symbol_size), Image.Resampling.LANCZOS)
            
            if is_dark and target_color:
                symbol_img = recolor_symbol(symbol_img, target_color)
            
            symbol_data = symbol_img.getdata()
            new_data = []
            for item in symbol_data:
                if item[3] > 0:
                    new_data.append((item[0], item[1], item[2], int(item[3] * opacity)))
                else:
                    new_data.append(item)
            symbol_img.putdata(new_data)
            
            img.paste(symbol_img, (int(x), int(y)), symbol_img)
            
        except Exception as e:
            continue

# ==============================
# توابع کمکی برای تقسیم کلمات به بخش‌های RTL و LTR
# ==============================
def split_words_by_direction(words):
    """
    لیست کلمات را به بخش‌هایی با جهت یکسان تقسیم می‌کند.
    هر بخش شامل کلمات با جهت یکسان است.
    """
    if not words:
        return []
    segments = []
    current_segment = [words[0]]
    current_dir = detect_direction(words[0])
    for word in words[1:]:
        dir_word = detect_direction(word)
        if dir_word == current_dir:
            current_segment.append(word)
        else:
            segments.append((current_segment, current_dir))
            current_segment = [word]
            current_dir = dir_word
    if current_segment:
        segments.append((current_segment, current_dir))
    return segments

# ==============================
# تابع رسم خط (با جاستیفای کامل و ترتیب صحیح برای RTL)
# ==============================
def draw_justified_line(draw, line, font, x_start, y, max_width, text_color,
                        is_last=False, is_first_line=False, direction='rtl'):
    if not line.strip():
        return y

    words = line.split()
    if not words:
        return y

    indent = INDENT_SIZE if is_first_line else 0
    available_width = max_width - indent

    # خط آخر یا تک‌کلمه‌ای → بدون جاستیفای
    if is_last or len(words) == 1:
        full_text = prepare_text(line)
        if direction == 'rtl':
            bbox = draw.textbbox((0, 0), full_text, font=font)
            text_width = bbox[2] - bbox[0]
            x = x_start + available_width - text_width
        else:
            x = x_start + indent
        draw.text((x, y), full_text, fill=text_color, font=font)
        bbox = draw.textbbox((0, 0), full_text, font=font)
        line_height = bbox[3] - bbox[1]
        line_spacing = get_line_spacing(font)
        return y + line_height + line_spacing

    # محاسبه عرض هر کلمه
    word_widths = []
    for word in words:
        rtl_word = prepare_text(word)
        bbox = draw.textbbox((0, 0), rtl_word, font=font)
        word_widths.append(bbox[2] - bbox[0])

    total_word_width = sum(word_widths)
    if total_word_width > available_width:
        full_text = prepare_text(line)
        if direction == 'rtl':
            bbox = draw.textbbox((0, 0), full_text, font=font)
            text_width = bbox[2] - bbox[0]
            x = x_start + available_width - text_width
        else:
            x = x_start + indent
        draw.text((x, y), full_text, fill=text_color, font=font)
        bbox = draw.textbbox((0, 0), full_text, font=font)
        line_height = bbox[3] - bbox[1]
        line_spacing = get_line_spacing(font)
        return y + line_height + line_spacing

    extra_space = available_width - total_word_width
    gaps = len(words) - 1
    space_per_gap = extra_space / gaps if gaps > 0 else 0

    if direction == 'rtl':
        # تقسیم کلمات به بخش‌های RTL و LTR
        segments = split_words_by_direction(words)
        word_to_width = {word: width for word, width in zip(words, word_widths)}
        
        # محاسبه عرض هر بخش
        segment_widths = []
        for seg, dir_seg in segments:
            seg_width = sum(word_to_width[w] for w in seg)
            segment_widths.append(seg_width)
        
        # رسم از راست به چپ با همان ترتیب بخش‌ها (نه معکوس)
        current_x = x_start + available_width
        for idx, (seg, dir_seg) in enumerate(segments):
            seg_width = segment_widths[idx]
            if dir_seg == 'ltr':
                # بخش LTR: کل بخش را یکجا رسم می‌کنیم
                ltr_text = ' '.join(seg)
                rtl_ltr = prepare_text(ltr_text)
                bbox = draw.textbbox((0, 0), rtl_ltr, font=font)
                ltr_width = bbox[2] - bbox[0]
                draw.text((current_x - ltr_width, y), rtl_ltr, fill=text_color, font=font)
                current_x -= (ltr_width + space_per_gap)
            else:
                # بخش RTL: کلمات را از راست به چپ به همان ترتیب رسم می‌کنیم
                for word in seg:
                    word_width = word_to_width[word]
                    rtl_word = prepare_text(word)
                    draw.text((current_x - word_width, y), rtl_word, fill=text_color, font=font)
                    current_x -= (word_width + space_per_gap)
    else:
        current_x = x_start + indent
        for i, word in enumerate(words):
            rtl_word = prepare_text(word)
            draw.text((current_x, y), rtl_word, fill=text_color, font=font)
            if i < gaps:
                current_x += word_widths[i] + space_per_gap
            else:
                current_x += word_widths[i]

    bbox = draw.textbbox((0, 0), prepare_text(words[0]), font=font)
    line_height = bbox[3] - bbox[1]
    line_spacing = get_line_spacing(font)
    return y + line_height + line_spacing

# ==============================
# تابع اصلی ساخت اسلاید
# ==============================
def make_slide(
    text,
    para_numbers,
    output_path,
    theme_name="Classic Ivory",
    slide_number=1,
    total_slides=1,
    layout="image_left",
    font_fa=None,
    font_en=None,
    line_spacing_factor=LINE_SPACING_FACTOR,
    symbol_paths=None
):
    global LINE_SPACING_FACTOR
    LINE_SPACING_FACTOR = line_spacing_factor

    theme = THEMES.get(theme_name, THEMES["Classic Ivory"])
    theme["name"] = theme_name
    
    if layout == "text_only":
        text_left = 40
        text_top = 40
        text_width = WIDTH - 80
        text_height = HEIGHT - 160
    elif layout == "image_left":
        image_width = int(WIDTH * 0.35)
        text_left = image_width + 40
        text_top = 40
        text_width = WIDTH - text_left - 40
        text_height = HEIGHT - 160
    elif layout == "image_right":
        image_width = int(WIDTH * 0.35)
        text_left = 40
        text_top = 40
        text_width = WIDTH - image_width - 80
        text_height = HEIGHT - 160
    elif layout == "image_top":
        image_height = int(HEIGHT * 0.30)
        text_left = 40
        text_top = image_height + 40
        text_width = WIDTH - 80
        text_height = HEIGHT - text_top - 120
    elif layout == "image_bottom":
        image_height = int(HEIGHT * 0.30)
        text_left = 40
        text_top = 40
        text_width = WIDTH - 80
        text_height = HEIGHT - image_height - 160
    else:
        raise ValueError(f"layout نامعتبر: {layout}")
    
    img = Image.new("RGB", (WIDTH, HEIGHT), theme["bg"])
    draw = ImageDraw.Draw(img)
    
    if theme.get("gradient") == "radial":
        apply_radial_gradient(img, theme["gradient_center"], theme["gradient_edge"])
    elif theme.get("gradient") == "linear":
        top = theme["gradient_top"]
        bottom = theme["gradient_bottom"]
        for y in range(HEIGHT):
            ratio = y / HEIGHT
            r = int(top[0]*(1-ratio) + bottom[0]*ratio)
            g = int(top[1]*(1-ratio) + bottom[1]*ratio)
            b = int(top[2]*(1-ratio) + bottom[2]*ratio)
            draw.line([(0, y), (WIDTH, y)], fill=(r,g,b))
    
    if theme.get("dot_grid"):
        color = theme.get("grid", (200,200,200))
        add_dot_grid(draw, WIDTH, HEIGHT, color, spacing=40, opacity=8)
    if theme.get("grain_opacity"):
        add_grain(img, theme["grain_opacity"])
    if theme.get("paper_texture") or theme.get("paper_fibers"):
        add_paper_texture(img)
    if theme.get("vignette"):
        add_vignette(img, theme["vignette"])
    
    text_color = theme["text"]
    font_path = get_font_path(text, font_fa, font_en, theme)
    best_size = find_best_font_size(draw, text, font_path, text_width, text_height)
    font = ImageFont.truetype(font_path, best_size)
    
    lines_with_para = wrap_text_with_para_numbers(draw, text, font, text_width, para_numbers)
    line_spacing = get_line_spacing(font)
    
    total_height = 0
    for line, _, _ in lines_with_para:
        if line.strip() == "":
            total_height += line_spacing
        else:
            rtl = prepare_text(line)
            bbox = draw.textbbox((0, 0), rtl, font=font)
            total_height += bbox[3] - bbox[1]
    if len(lines_with_para) > 1:
        total_height += line_spacing * (len(lines_with_para) - 1)
    
    y = text_top + (text_height - total_height) / 2
    
    final_text_bbox = (text_left, y, text_left + text_width, y + total_height)
    paragraphs = text.split("\n")
    
    for i, (line, para, direction) in enumerate(lines_with_para):
        if line.strip() == "":
            y += line_spacing
            continue
        
        is_first_line = (i == 0) or (lines_with_para[i-1][1] != para)
        is_last_line = (i == len(lines_with_para) - 1) or (lines_with_para[i+1][1] != para)
        
        y = draw_justified_line(
            draw,
            line,
            font,
            text_left,
            y,
            text_width,
            text_color,
            is_last=is_last_line,
            is_first_line=is_first_line,
            direction=direction
        )
    
    if symbol_paths and len(symbol_paths) > 0:
        try:
            draw_decorative_symbols(img, symbol_paths, final_text_bbox, theme, layout)
        except Exception as e:
            print(f"⚠️ خطا در رسم آیکون‌های تزئینی: {e}")
    
    add_border(draw, WIDTH, HEIGHT, theme["border"], theme["border_width"])
    
    footer_font_path = get_font_path("123", font_fa, font_en, theme)
    footer_font = ImageFont.truetype(footer_font_path, 28)
    footer_text = f"{slide_number} / {total_slides}"
    bbox = draw.textbbox((0,0), footer_text, font=footer_font)
    accent = theme.get("accent", theme["border"])
    draw.text(((WIDTH - (bbox[2]-bbox[0]))//2, HEIGHT-70), footer_text, fill=accent, font=footer_font)
    
    img.save(output_path)
    print(f"✅ {output_path.name} ساخته شد با تم '{theme_name}' و چیدمان '{layout}'")

# ==============================
# تابع پردازش فایل
# ==============================
def process_txt_file(
    txt_path,
    theme_name="Classic Ivory",
    min_words=80,
    max_words=100,
    layout="image_left",
    font_fa=None,
    font_en=None,
    line_spacing_factor=LINE_SPACING_FACTOR,
    use_symbols=False,
    manual_split=False
):
    txt_path = Path(txt_path)
    if not txt_path.exists():
        print(f"❌ فایل {txt_path} یافت نشد.")
        return
    
    with open(txt_path, "r", encoding="utf-8") as f:
        content = f.read()
    
    if manual_split:
        print("📌 استفاده از حالت دستی تقسیم اسلایدها (بر اساس \\n\\n)")
        chunks = content.split('\n\n')
        chunks = [chunk.strip() for chunk in chunks if chunk.strip()]
        chunks_with_para = [(chunk, list(range(len(chunk.split('\n'))))) for chunk in chunks]
    else:
        print("📌 استفاده از حالت خودکار تقسیم اسلایدها (بر اساس تعداد کلمات)")
        chunks_with_para = chunk_text_by_sentences(content, min_words, max_words)
    
    if not chunks_with_para:
        print("⚠️ هیچ اسلایدی تولید نشد!")
        return    
    symbol_paths = None
    if use_symbols:
        print("🔍 در حال تحلیل محتوا برای انتخاب نماد مناسب...")
        try:
            symbol_paths = Categorizing(content)
            print(f"✅ {len(symbol_paths)} نماد انتخاب شد: {[Path(p).stem for p in symbol_paths]}")
        except Exception as e:
            print(f"⚠️ خطا در تشخیص نماد: {e}")
            symbol_paths = None
    
    base_dir = txt_path.parent
    base_name = txt_path.stem
    theme_name_sanitized = sanitize_theme_name(theme_name)
    
    for idx, (chunk_text, para_numbers) in enumerate(chunks_with_para, start=1):
        output_filename = f"{base_name}_{theme_name_sanitized}_slide_{idx}.png"
        output_path = base_dir / output_filename
        
        make_slide(
            chunk_text,
            para_numbers,
            output_path,
            theme_name,
            idx,
            len(chunks_with_para),
            layout=layout,
            font_fa=font_fa,
            font_en=font_en,
            line_spacing_factor=line_spacing_factor,
            symbol_paths=symbol_paths
        )
    
    print(f"\n🎉 تمام شد! {len(chunks_with_para)} اسلاید در {base_dir} ذخیره شد.")