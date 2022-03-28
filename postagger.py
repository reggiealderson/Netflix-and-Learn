pos_tag_colours = {
    "ADJ": "#dbcdf0",
    "ADP": "#f2c6de",
    "ADV": "#faedcb",
    "AUX": "#d6e2e9",
    "CCONJ": "#e2e2df",
    "DET": "#f9c6c9",
    "INTJ": "#fec89a",
    "NOUN": "#f7d9c4",
    "NUM": "#d2d2cf",
    "PART": "#e2cfc4",
    "PRON": "#c6def1",
    "PROPN": "#b9fbc0",
    "SCONJ": "#f8edeb",
    "SYM": "#fadde1",
    "VERB": "#c9e4de",
    }


def annotate_prepare(all_subtitles_tokens_flat, all_subtitles_pos_tags_flat):
    ''' Prepares the data for the required format of Streamlit's annotated text functionality '''
    
    pos_tag_line_items_flat = []
    
    for a, b in zip(all_subtitles_tokens_flat, all_subtitles_pos_tags_flat):
        pos_tag_line_items = []
        for x, y in zip(a, b):
            if y != 'PUNCT' and y != 'X' and y != 'SPACE':
                line_item = f"(' {x}', '{y}', '{pos_tag_colours[y]}')"
            else:
                line_item = f"'{x}'"
            pos_tag_line_items.append(line_item)

        full_pos_tag_line_items = ','.join(pos_tag_line_items)
        pos_tag_line_items_flat.append(full_pos_tag_line_items)
    
    return pos_tag_line_items_flat
