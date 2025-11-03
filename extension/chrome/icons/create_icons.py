#!/usr/bin/env python3
"""
DualMind Icon Generator
Creates professional extension icons in 3 sizes: 16x16, 48x48, 128x128
"""

try:
    from PIL import Image, ImageDraw, ImageFont
    import os
except ImportError:
    print("❌ Error: Pillow library not found")
    print("📦 Install with: pip3 install Pillow")
    exit(1)

def create_dualmind_icon(size):
    """Create a DualMind icon with brain emoji aesthetic"""
    
    # Create image with transparent background
    img = Image.new('RGBA', (size, size), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)
    
    # DualMind brand colors (purple/blue gradient)
    color1 = (99, 102, 241)    # Indigo
    color2 = (139, 92, 246)    # Purple
    
    # Draw circular gradient background
    center = size // 2
    max_radius = size // 2 - 2
    
    for i in range(max_radius, 0, -1):
        # Calculate gradient color
        ratio = i / max_radius
        r = int(color1[0] * ratio + color2[0] * (1 - ratio))
        g = int(color1[1] * ratio + color2[1] * (1 - ratio))
        b = int(color1[2] * ratio + color2[2] * (1 - ratio))
        
        draw.ellipse(
            [center - i, center - i, center + i, center + i],
            fill=(r, g, b, 255)
        )
    
    # Add white border
    draw.ellipse(
        [2, 2, size - 2, size - 2],
        outline=(255, 255, 255, 200),
        width=max(1, size // 32)
    )
    
    # Draw "brain" symbol (stylized)
    if size >= 48:
        # For larger icons, draw a more detailed brain
        brain_color = (255, 255, 255, 255)
        
        # Left hemisphere
        left_x = center - size // 6
        left_y = center
        left_radius = size // 5
        draw.ellipse(
            [left_x - left_radius, left_y - left_radius, 
             left_x + left_radius, left_y + left_radius],
            fill=brain_color
        )
        
        # Right hemisphere
        right_x = center + size // 6
        right_y = center
        right_radius = size // 5
        draw.ellipse(
            [right_x - right_radius, right_y - right_radius,
             right_x + right_radius, right_y + right_radius],
            fill=brain_color
        )
        
        # Connection (corpus callosum)
        draw.rectangle(
            [left_x, center - size // 12,
             right_x, center + size // 12],
            fill=brain_color
        )
        
        # Add some "folds" for realism
        fold_color = (99, 102, 241, 255)
        for offset in [-size//10, 0, size//10]:
            draw.arc(
                [left_x - left_radius//2, left_y - left_radius//2 + offset,
                 left_x + left_radius//2, left_y + left_radius//2 + offset],
                start=0, end=180,
                fill=fold_color,
                width=max(1, size // 64)
            )
            draw.arc(
                [right_x - right_radius//2, right_y - right_radius//2 + offset,
                 right_x + right_radius//2, right_y + right_radius//2 + offset],
                start=0, end=180,
                fill=fold_color,
                width=max(1, size // 64)
            )
    else:
        # For small icons (16x16), just draw two circles
        brain_color = (255, 255, 255, 255)
        left_x = center - size // 5
        right_x = center + size // 5
        y = center
        radius = size // 4
        
        draw.ellipse(
            [left_x - radius, y - radius, left_x + radius, y + radius],
            fill=brain_color
        )
        draw.ellipse(
            [right_x - radius, y - radius, right_x + radius, y + radius],
            fill=brain_color
        )
    
    return img

def main():
    print("🎨 Creating DualMind Extension Icons...\n")
    
    sizes = [16, 48, 128]
    
    for size in sizes:
        filename = f"icon{size}.png"
        print(f"   Creating {filename} ({size}x{size})...", end=" ")
        
        try:
            icon = create_dualmind_icon(size)
            icon.save(filename, "PNG")
            
            # Verify file was created
            if os.path.exists(filename):
                file_size = os.path.getsize(filename)
                print(f"✅ ({file_size} bytes)")
            else:
                print("❌ Failed to save")
        except Exception as e:
            print(f"❌ Error: {e}")
    
    print("\n✨ Icon generation complete!")
    print("\nGenerated files:")
    for size in sizes:
        filename = f"icon{size}.png"
        if os.path.exists(filename):
            print(f"   ✅ {filename}")
    
    print("\n📝 Next steps:")
    print("   1. Load extension in Chrome (chrome://extensions/)")
    print("   2. Enable Developer mode")
    print("   3. Click 'Load unpacked'")
    print("   4. Select: extension/chrome/")
    print("\n🎉 Your DualMind extension is ready!")

if __name__ == "__main__":
    main()

