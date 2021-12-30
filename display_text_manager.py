from display import Display, TextRow
from string import printable

class DisplayTextManager():
    def __init__(self, display: Display, text_spacing: int = 3) -> None:
        self._display = display
        self._text_spacing = text_spacing
        self._texts = {}

    def text_spacing(self) -> int:
        return self._text_spacing

    def set_text_spacing(self, new_spacing: int) -> None:
        self._text_spacing = new_spacing
    
    def set_text(self, text: str, row: TextRow) -> None:
        text = ''.join(filter(lambda x: x in printable, text))
        if len(text) > self._display.text_line_capacity():
            text += ' ' * self.text_spacing()
        self._texts[row] = {'text': text, 'position': 0}

    def remove_text_row(self, row: TextRow) -> bool:
        if row in self._texts:
            del self._texts[row]
            return True

        return False
    
    # This method scrolls texts, and returns them
    # to default position when scrolled to the end
    def loop_texts(self) -> None:
        for row, text_data in self._texts.items():
            text = text_data['text']
            position = text_data['position']
            text_length = len(text)
            row_capacity = self._display.text_line_capacity()

            # first, we check if the text fits on screen.
            # If it does, we do nothing. If it doesn't, we scroll
            if text_length > row_capacity:
                # let's scroll the text by one char, or return to
                # default position if scrolled to the maximum
                new_position = position + 1
                if new_position == text_length:
                    new_position = 0
                
                text_data['position'] = new_position
                       
    
    def update_display(self) -> None:
        for row, text_data in self._texts.items():
            text = text_data['text']
            position = int(text_data['position'])
            remaining_length = int(len(text) - position)
            row_capacity = int(self._display.text_line_capacity())
            free_spaces = int(row_capacity - remaining_length)
            
            # Here's the tricky part. The text is supposed to be
            # looped, and we have to do the loop logic here.

            if free_spaces > 0 and position != 0:
                # In case we have some free space for more characters, we draw them.
                looped_text = text[position:] + text[:free_spaces]
                self._display.draw_text_in_row(looped_text, row)
            else:
                # If the text is not scrolled past-end (last char is not yet)
                # on screen), including spacing, just draw it normally
                self._display.draw_text_in_row(text[position:], row)