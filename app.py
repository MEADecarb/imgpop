import streamlit as st
from PIL import Image, ImageDraw, ImageFont

# App title
st.title("Interactive Image with Grid-based Popups and HTML Generation")

# Instructions
st.write("""
1. Upload an image.
2. Select a grid size (number of rows and columns).
3. Choose which grid squares should have popups.
4. Enter popup title and text for the selected grid squares.
5. Preview the final image with vector icons and download the HTML for your GitHub-hosted interactive page.
""")

# Upload image file
uploaded_file = st.file_uploader("Choose an image...", type=["jpg", "png", "jpeg"])

if uploaded_file is not None:
  # Load the uploaded image
  img = Image.open(uploaded_file)
  img_width, img_height = img.size

  # Allow the user to define the grid size
  grid_rows = st.number_input("Select number of grid rows", min_value=2, max_value=20, value=5)
  grid_cols = st.number_input("Select number of grid columns", min_value=2, max_value=20, value=5)

  # Calculate the grid cell dimensions based on the image size
  cell_width = img_width / grid_cols
  cell_height = img_height / grid_rows

  # Create two copies of the image: one for grid preview and one for final output
  grid_img = img.copy()
  final_img = img.copy()

  draw_grid = ImageDraw.Draw(grid_img)
  draw_final = ImageDraw.Draw(final_img)

  # Load a font for grid labels with size 22
  try:
      font = ImageFont.truetype("arial.ttf", 22)  # Use your system font here, size 22
  except IOError:
      font = ImageFont.load_default()  # Use default if the specified font is not found

  # Draw grid and add labels on the grid image
  for row in range(grid_rows):
      for col in range(grid_cols):
          # Coordinates of the grid cell
          x = col * cell_width
          y = row * cell_height

          # Draw the grid on the preview image
          draw_grid.rectangle([x, y, x + cell_width, y + cell_height], outline="red", width=2)

          # Add grid labels (e.g., A1, B2, etc.)
          label = f"{chr(65 + row)}{col+1}"
          label_x = x + cell_width / 2 - 11  # Adjusted for smaller font size
          label_y = y + cell_height / 2 - 11  # Adjusted for smaller font size

          # Draw white halo (outline) and then the black text for readability
          for dx in [-1, 1]:
              for dy in [-1, 1]:
                  draw_grid.text((label_x + dx, label_y + dy), label, font=font, fill="white")
          draw_grid.text((label_x, label_y), label, font=font, fill="black")

  # Display the image with the grid and labels
  st.image(grid_img, caption="Image with Grid and Labels (Preview)", use_column_width=True)

  # The rest of the code remains the same...

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

  # Button to generate preview and final image
  if st.button("Generate Final Image, HTML, and Preview"):
      # Add vector star icons in the final image at the selected grid locations
      html_icon_positions = []  # For HTML generation
      for square in popup_grid_squares:
          # Calculate the center of the grid cell for the star placement
          x_center = square["col"] * cell_width + cell_width / 2
          y_center = square["row"] * cell_height + cell_height / 2

          # Draw the star icon in the final image
          draw_final.polygon(
              [(x_center, y_center - 10), (x_center + 6, y_center - 3),
               (x_center + 10, y_center + 8), (x_center, y_center + 3),
               (x_center - 10, y_center + 8), (x_center - 6, y_center - 3)],
              fill="red", outline="black", width=1
          )

          # Store the coordinates for the HTML
          html_icon_positions.append({
              "x": x_center,
              "y": y_center,
              "title": square["title"],
              "text": square["text"]
          })

      # Display the final image (with star icons but no grid lines or labels)
      st.image(final_img, caption="Final Image with Vector Icons", use_column_width=True)

      # Generate and display a popup preview
      if popup_grid_squares:
          st.write("**Popup Preview**")

          for square in popup_grid_squares:
              st.markdown(f"### {square['title']}")
              st.write(square['text'])

          st.write("This is a preview of how the popups will look when a user hovers over the vector icons.")

      # Save the final image as a downloadable file
      final_img.save("final_image_with_icons.png")
      with open("final_image_with_icons.png", "rb") as file:
          btn = st.download_button(
              label="Download Final Image",
              data=file,
              file_name="final_image_with_icons.png",
              mime="image/png"
          )

      # Generate HTML code for GitHub Pages-hosted interactive webpage
      html_code = f'''
      <!DOCTYPE html>
      <html lang="en">
      <head>
          <meta charset="UTF-8">
          <meta name="viewport" content="width=device-width, initial-scale=1.0">
          <title>Interactive Image with Popups</title>
          
      </head>
      <body>

      <div class="image-container">
          <img src="final_image_with_icons.png" alt="Interactive Image">
      '''
      
      # Insert the icons and popup divs into the HTML
      for icon in html_icon_positions:
          html_code += f'''
          <div class="icon" style="top: {icon['y']}px; left: {icon['x']}px;" 
               onmouseover="document.getElementById('popup-{icon['x']}-{icon['y']}').style.display='block'"
               onmouseout="document.getElementById('popup-{icon['x']}-{icon['y']}').style.display='none'">
          </div>
          <div id="popup-{icon['x']}-{icon['y']}" class="popup" style="top: {icon['y'] + 25}px; left: {icon['x']}px;">
              <h2>{icon['title']}</h2>
              <p>{icon['text']}</p>
          </div>
          '''

      html_code += '''
      </div>
      </body>
      </html>
      '''

      # Display the generated HTML code
      st.code(html_code, language="html")

      # Save the HTML code as a downloadable file
      with open("interactive_image.html", "w") as file:
          file.write(html_code)
      with open("interactive_image.html", "rb") as file:
          btn = st.download_button(
              label="Download HTML for GitHub Pages",
              data=file,
              file_name="interactive_image.html",
              mime="text/html"
          )

# Created/Modified files during execution:
print("final_image_with_icons.png")
print("interactive_image.html")
