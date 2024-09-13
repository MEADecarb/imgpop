import streamlit as st
from PIL import Image, ImageDraw, ImageFont
import math

# App title
st.title("Interactive Image with Grid-based Popups")

# Instructions
st.write("""
1. Upload an image.
2. Select a grid size (number of rows and columns).
3. Choose which grid squares should have popups.
4. Enter popup title and text for the selected grid squares.
5. A star icon will appear on the grid areas that contain a popup.
""")

# Upload image file
uploaded_file = st.file_uploader("Choose an image...", type=["jpg", "png", "jpeg"])

if uploaded_file is not None:
    # Load the uploaded image
    img = Image.open(uploaded_file)

    # Display the uploaded image
    st.image(img, caption="Uploaded Image", use_column_width=True)

    # Allow the user to define the grid size
    grid_rows = st.number_input("Select number of grid rows", min_value=2, max_value=20, value=5)
    grid_cols = st.number_input("Select number of grid columns", min_value=2, max_value=20, value=5)

    # Calculate the grid cell dimensions based on the image size
    img_width, img_height = img.size
    cell_width = img_width / grid_cols
    cell_height = img_height / grid_rows

    # Create a copy of the image and draw the grid on it
    grid_img = img.copy()
    draw = ImageDraw.Draw(grid_img)

    # Draw grid and add labels
    for row in range(grid_rows):
        for col in range(grid_cols):
            # Draw grid lines
            x = col * cell_width
            y = row * cell_height
            draw.rectangle([x, y, x + cell_width, y + cell_height], outline="red", width=2)

            # Add grid labels (e.g., A1, B1, etc.)
            label = f"{chr(65 + row)}{col+1}"
            label_x = x + cell_width / 2 - 10
            label_y = y + cell_height / 2 - 10
            draw.text((label_x, label_y), label, fill="blue")

    # Display the image with grid and labels
    st.image(grid_img, caption="Image with Grid and Labels", use_column_width=True)

    # Allow the user to select grid squares for popups
    popup_grid_squares = []
    for row in range(grid_rows):
        for col in range(grid_cols):
            if st.checkbox(f"Popup at Grid {chr(65 + row)}{col+1}"):
                popup_title = st.text_input(f"Enter popup title for Grid {chr(65 + row)}{col+1}")
                popup_text = st.text_area(f"Enter popup text for Grid {chr(65 + row)}{col+1}")
                popup_grid_squares.append({
                    "row": row,
                    "col": col,
                    "title": popup_title,
                    "text": popup_text
                })

    # Button to generate HTML code for the popups
    if st.button("Generate Interactive HTML"):
        html_output = '''
        <!DOCTYPE html>
        <html lang="en">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>Interactive Grid Popup</title>
            <style>
                body {
                    font-family: Arial, sans-serif;
                }
                .image-container {
                    position: relative;
                    display: inline-block;
                }
                .image-container img {
                    width: 600px;
                    height: auto;
                }
                .popup {
                    display: none;
                    position: absolute;
                    background-color: rgba(0, 0, 0, 0.7);
                    color: #fff;
                    padding: 10px;
                    border-radius: 5px;
                    width: 200px;
                }
                .popup-visible {
                    display: block;
                }
                .icon {
                    position: absolute;
                    width: 20px;
                    height: 20px;
                    background-color: red;
                    clip-path: polygon(50% 0%, 61% 35%, 98% 35%, 68% 57%, 79% 91%, 50% 70%, 21% 91%, 32% 57%, 2% 35%, 39% 35%);
                    border: 1px solid black;
                }
            </style>
        </head>
        <body>

        <div class="image-container">
            <img src="your-image.jpg" alt="Interactive Image">
        '''

        # Generate popups and star icons for each selected grid square
        for square in popup_grid_squares:
            x = square["col"] * cell_width + cell_width / 2 - 10  # Center the icon in the grid square
            y = square["row"] * cell_height + cell_height / 2 - 10

            # Popup content
            html_output += f'''
            <div class="popup" style="top: {y}px; left: {x}px;">
                <h2>{square['title']}</h2>
                <p>{square['text']}</p>
            </div>
            '''

            # Star icon for the grid area with a popup
            html_output += f'''
            <div class="icon" style="top: {y}px; left: {x}px;"></div>
            '''

        html_output += '''
        <script>
            // JavaScript to toggle popups on hover
            const popups = document.querySelectorAll('.popup');
            const icons = document.querySelectorAll('.icon');
            document.querySelector('.image-container').addEventListener('mousemove', (event) => {
                popups.forEach((popup, index) => {
                    const rect = icons[index].getBoundingClientRect();
                    if (event.clientX >= rect.left && event.clientX <= rect.right &&
                        event.clientY >= rect.top && event.clientY <= rect.bottom) {
                        popup.classList.add('popup-visible');
                    } else {
                        popup.classList.remove('popup-visible');
                    }
                });
            });
        </script>
        </body>
        </html>
        '''

        # Display the generated HTML
        st.code(html_output, language='html')

        # Save the HTML to file
        with open("interactive_image_grid.html", "w") as f:
            f.write(html_output)

        st.success("HTML file generated! You can now upload this to GitHub Pages.")
