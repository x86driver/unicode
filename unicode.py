import sys
from fontTools.ttLib import TTFont

def list_unicode_ranges(ttf_file):
    try:
        font = TTFont(ttf_file)
        
        cmap = font['cmap']
        glyph_set = font.getGlyphSet()
        unicode_list = []

        for table in cmap.tables:
            if table.isUnicode():
                unicode_list.extend(table.cmap.keys())
        
        unicode_list = sorted(set(unicode_list))

        valid_unicode = []
        for codepoint in unicode_list:
            glyph_name = cmap.getBestCmap().get(codepoint)
            if glyph_name in glyph_set:
                valid_unicode.append(codepoint)

        ranges = []
        start = None
        end = None

        for codepoint in valid_unicode:
            if start is None:
                start = end = codepoint
            elif codepoint == end + 1:
                end = codepoint
            else:
                if start == end:
                    ranges.append(f"{start:04X}")
                else:
                    ranges.append(f"{start:04X}-{end:04X}")
                start = end = codepoint

        if start is not None:
            if start == end:
                ranges.append(f"{start:04X}")
            else:
                ranges.append(f"{start:04X}-{end:04X}")

        print(f"Valid Unicode ranges in {ttf_file}:")
        print(",".join(ranges))

    except Exception as e:
        print(f"Error processing file {ttf_file}: {e}")

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: ", sys.argv[0], "font.ttf")
        sys.exit(1)
    ttf_path = sys.argv[1]
    list_unicode_ranges(ttf_path)

