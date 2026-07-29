#!/usr/bin/env python3
"""
create_hero_banner.py
Generates a bespoke, highly professional glassmorphism hero banner SVG
for Shubhankar Maity's GitHub Profile README.
"""
import base64

def get_avatar_base64():
    try:
        from PIL import Image
        import io
        img = Image.open("assets/myphoto.png")
        # Crop square character face
        crop_w = int(img.height * 1.0)
        portrait = img.crop((0, 0, crop_w, img.height))
        portrait = portrait.resize((300, 300))
        
        buf = io.BytesIO()
        portrait.save(buf, format="PNG")
        return base64.b64encode(buf.getvalue()).decode("utf-8")
    except Exception as e:
        print("Error processing image:", e)
        return ""

def generate_hero_svg(dark_mode=True):
    avatar_b64 = get_avatar_base64()
    
    bg_gradient_start = "#0d1117" if dark_mode else "#f6f8fa"
    bg_gradient_end = "#161b22" if dark_mode else "#ffffff"
    card_bg = "#161b22" if dark_mode else "#ffffff"
    border_color = "#30363d" if dark_mode else "#d0d7de"
    title_color = "#58a6ff" if dark_mode else "#0969da"
    text_primary = "#f0f6fc" if dark_mode else "#1f2328"
    text_secondary = "#8b949e" if dark_mode else "#656d76"
    badge_bg = "#21262d" if dark_mode else "#f3f4f6"
    badge_text = "#c9d1d9" if dark_mode else "#24292f"
    accent_green = "#3fb950"

    avatar_svg_element = ""
    if avatar_b64:
        avatar_svg_element = f'''
        <g transform="translate(35, 45)">
            <!-- Avatar Frame -->
            <rect x="0" y="0" width="130" height="130" rx="20" fill="{badge_bg}" stroke="{border_color}" stroke-width="2"/>
            <clipPath id="avatar-clip">
                <rect x="4" y="4" width="122" height="122" rx="16"/>
            </clipPath>
            <image href="data:image/png;base64,{avatar_b64}" x="-10" y="-5" width="145" height="145" clip-path="url(#avatar-clip)"/>
            <!-- Status Dot -->
            <circle cx="118" cy="118" r="8" fill="{accent_green}" stroke="{card_bg}" stroke-width="3"/>
        </g>
        '''
    else:
        avatar_svg_element = f'''
        <g transform="translate(35, 45)">
            <rect x="0" y="0" width="130" height="130" rx="20" fill="{badge_bg}" stroke="{border_color}" stroke-width="2"/>
            <text x="65" y="75" font-family="'Segoe UI', Ubuntu, sans-serif" font-size="40" fill="{title_color}" text-anchor="middle">SM</text>
            <circle cx="118" cy="118" r="8" fill="{accent_green}" stroke="{card_bg}" stroke-width="3"/>
        </g>
        '''

    svg_content = f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 800 220" width="100%" height="220">
    <defs>
        <!-- Background Linear Gradient -->
        <linearGradient id="bg-grad" x1="0%" y1="0%" x2="100%" y2="100%">
            <stop offset="0%" stop-color="{bg_gradient_start}" />
            <stop offset="100%" stop-color="{bg_gradient_end}" />
        </linearGradient>

        <!-- Border Glow Gradient -->
        <linearGradient id="border-grad" x1="0%" y1="0%" x2="100%" y2="0%">
            <stop offset="0%" stop-color="#38bdf8" stop-opacity="0.8"/>
            <stop offset="50%" stop-color="#818cf8" stop-opacity="0.3"/>
            <stop offset="100%" stop-color="#c084fc" stop-opacity="0.8"/>
        </linearGradient>

        <!-- Grid Pattern -->
        <pattern id="grid" width="20" height="20" patternUnits="userSpaceOnUse">
            <path d="M 20 0 L 0 0 0 20" fill="none" stroke="{border_color}" stroke-width="0.5" stroke-opacity="0.3"/>
        </pattern>
    </defs>

    <!-- Main Card Container -->
    <rect width="800" height="220" rx="16" fill="url(#bg-grad)"/>
    <rect width="800" height="220" rx="16" fill="url(#grid)"/>
    <rect width="798" height="218" x="1" y="1" rx="15" fill="none" stroke="url(#border-grad)" stroke-width="1.5"/>

    <!-- Terminal Window Buttons -->
    <circle cx="25" cy="22" r="5" fill="#ff5f56"/>
    <circle cx="40" cy="22" r="5" fill="#ffbd2e"/>
    <circle cx="55" cy="22" r="5" fill="#27c93f"/>
    <text x="75" y="26" font-family="'Fira Code', Consolas, monospace" font-size="11" fill="{text_secondary}">shubhankar@devos ~ profile</text>

    <!-- Divider -->
    <line x1="15" y1="36" x2="785" y2="36" stroke="{border_color}" stroke-width="1" stroke-opacity="0.5"/>

    <!-- Avatar Group -->
    {avatar_svg_element}

    <!-- Content Area -->
    <g transform="translate(190, 60)">
        <!-- Name -->
        <text x="0" y="24" font-family="'Segoe UI', Roboto, -apple-system, sans-serif" font-weight="800" font-size="26" fill="{text_primary}">
            Shubhankar Maity
        </text>
        
        <!-- Role -->
        <text x="0" y="48" font-family="'Segoe UI', Roboto, -apple-system, sans-serif" font-weight="600" font-size="14" fill="{title_color}">
            Full-Stack MERN Developer  •  CSE Student
        </text>

        <!-- Bio / Tagline -->
        <text x="0" y="70" font-family="'Segoe UI', Roboto, -apple-system, sans-serif" font-size="12.5" fill="{text_secondary}">
            Building reliable, scalable software with modern web technologies &amp; cloud architecture.
        </text>

        <!-- Skill Pills -->
        <g transform="translate(0, 88)">
            <!-- Pill 1 -->
            <rect x="0" y="0" width="82" height="24" rx="12" fill="{badge_bg}" stroke="{border_color}" stroke-width="1"/>
            <text x="41" y="16" font-family="'Fira Code', monospace" font-size="11" font-weight="600" fill="{badge_text}" text-anchor="middle">⚡ MERN</text>

            <!-- Pill 2 -->
            <rect x="90" y="0" width="85" height="24" rx="12" fill="{badge_bg}" stroke="{border_color}" stroke-width="1"/>
            <text x="132" y="16" font-family="'Fira Code', monospace" font-size="11" font-weight="600" fill="{badge_text}" text-anchor="middle">🐳 Docker</text>

            <!-- Pill 3 -->
            <rect x="183" y="0" width="75" height="24" rx="12" fill="{badge_bg}" stroke="{border_color}" stroke-width="1"/>
            <text x="220" y="16" font-family="'Fira Code', monospace" font-size="11" font-weight="600" fill="{badge_text}" text-anchor="middle">☁️ AWS</text>

            <!-- Pill 4 -->
            <rect x="266" y="0" width="95" height="24" rx="12" fill="{badge_bg}" stroke="{border_color}" stroke-width="1"/>
            <text x="313" y="16" font-family="'Fira Code', monospace" font-size="11" font-weight="600" fill="{badge_text}" text-anchor="middle">☕ Java / C++</text>
        </g>
    </g>

    <!-- Location & Status Badge (Right Aligned) -->
    <g transform="translate(770, 60)" text-anchor="end">
        <text x="0" y="24" font-family="'Segoe UI', Roboto, sans-serif" font-size="12" fill="{text_secondary}">
            📍 West Bengal, India
        </text>
        <text x="0" y="48" font-family="'Segoe UI', Roboto, sans-serif" font-size="11.5" font-weight="600" fill="{accent_green}">
            🟢 Open to Opportunities
        </text>
    </g>
</svg>'''
    return svg_content

def main():
    dark_svg = generate_hero_svg(dark_mode=True)
    light_svg = generate_hero_svg(dark_mode=False)

    with open("hero_dark.svg", "w", encoding="utf-8") as f:
        f.write(dark_svg)
    with open("hero_light.svg", "w", encoding="utf-8") as f:
        f.write(light_svg)
    print("Generated hero_dark.svg and hero_light.svg")

if __name__ == "__main__":
    main()
