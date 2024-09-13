import streamlit as st
from PIL import Image, ImageDraw
import math

# App title
st.title("Interactive Image with Grid-based Popups")

# Instructions
st.write("""
1. Upload an image.
2. Select a grid size (number of rows and columns).
3. Choose which grid squares should have popups.
4. Enter popup text for the selected grid squares.
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

    # Draw the grid on the image for visualization
    grid_img = img.copy()
    draw = ImageDraw.Draw(grid_img)

    for i in range(1, grid_cols):
        # Vertical lines
        x = i * cell_width
        draw.line([(x, 0), (x, img_height)], fill="red", width=2)

    for i in range(1, grid_rows):
        # Horizontal lines
        y = i * cell_height
        draw.line([(0, y), (img_width, y)], fill="red", width=2)

    # Show the image with grid overlay
    st.image(grid_img, caption="Image with Grid", use_column_width=True)

    # Allow the user to select grid squares for popups
    popup_grid_squares = []
    for row in range(grid_rows):
        for col in range(grid_cols):
            if st.checkbox(f"Popup at Grid ({row+1}, {col+1})"):
                popup_text = st.text_input(f"Enter popup text for Grid ({row+1}, {col+1})")
                popup_grid_squares.append({
                    "row": row,
                    "col": col,
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
            </style>
        </head>
        <body>

        <div class="image-container">
            <img src="your-image.jpg" alt="Interactive Image">
        '''

        # Generate popups for each selected grid square
        for square in popup_grid_squares:
            x = square["col"] * cell_width
            y = square["row"] * cell_height
            html_output += f'''
            <div class="popup" style="top: {y}px; left: {x}px;">
                <p>{square["text"]}</p>
            </div>
            '''

        html_output += '''
        <script>
            // JavaScript to toggle popups on hover
            const popups = document.querySelectorAll('.popup');
            document.querySelector('.image-container').addEventListener('mousemove', (event) => {
                popups.forEach(popup => {
                    const rect = popup.getBoundingClientRect();
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
