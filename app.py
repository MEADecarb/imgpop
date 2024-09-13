import streamlit as st
from PIL import Image, ImageDraw, ImageFont

# App title
st.title("Interactive Image with Axis-based Popups and HTML Generation")

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
  grid_cols = st.number_input("Select number of grid columns", min_value=2, max_value=26, value=5)  # Max 26 for A-Z

  # Calculate the grid cell dimensions based on the image size
  cell_width = img_width / grid_cols
  cell_height = img_height / grid_rows

  # Create two copies of the image: one for grid preview and one for final output
  grid_img = img.copy()
  final_img = img.copy()

  draw_grid = ImageDraw.Draw(grid_img)
  draw_final = ImageDraw.Draw(final_img)

  # Load a font for axis labels with size 22
  try:
      font = ImageFont.truetype("arial.ttf", 22)  # Use your system font here, size 22
  except IOError:
      font = ImageFont.load_default()  # Use default if the specified font is not found

  # Draw grid and add axes on the grid image
  for row in range(grid_rows + 1):
      y = row * cell_height
      draw_grid.line([(0, y), (img_width, y)], fill="red", width=2)
      
      if row < grid_rows:  # Don't draw label for the last line
          # Draw y-axis labels (numbers)
          label = str(grid_rows - row)
          label_width, label_height = draw_grid.textsize(label, font=font)
          label_x = -label_width - 5  # Position labels to the left of the image
          label_y = y + (cell_height - label_height) / 2
          draw_grid.text((label_x, label_y), label, font=font, fill="black")

  for col in range(grid_cols + 1):
      x = col * cell_width
      draw_grid.line([(x, 0), (x, img_height)], fill="red", width=2)
      
      if col < grid_cols:  # Don't draw label for the last line
          # Draw x-axis labels (letters)
          label = chr(65 + col)  # A, B, C, ...
          label_width, label_height = draw_grid.textsize(label, font=font)
          label_x = x + (cell_width - label_width) / 2
          label_y = img_height + 5  # Position labels below the image
          draw_grid.text((label_x, label_y), label, font=font, fill="black")

  # Create a new image with extra space for axis labels
  padding = 30  # Adjust this value to increase/decrease padding around the image
  new_width = img_width + padding * 2
  new_height = img_height + padding * 2
  padded_grid_img = Image.new("RGB", (new_width, new_height), color="white")
  padded_grid_img.paste(grid_img, (padding, padding))

  # Display the image with the grid and axes
  st.image(padded_grid_img, caption="Image with Grid and Axes (Preview)", use_column_width=True)

  # Allow the user to select grid squares for popups
  popup_grid_squares = []
  for row in range(grid_rows):
      for col in range(grid_cols):
          if st.checkbox(f"Popup at Grid {chr(65 + col)}{grid_rows - row}"):
              popup_title = st.text_input(f"Enter popup title for Grid {chr(65 + col)}{grid_rows - row}")
              popup_text = st.text_area(f"Enter popup text for Grid {chr(65 + col)}{grid_rows - row}")
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
              "x": x_center + padding,  # Add padding to account for the new image size
              "y": y_center + padding,  # Add padding to account for the new image size
              "title": square["title"],
              "text": square["text"]
          })

      # Create a new final image with extra space for axis labels
      padded_final_img = Image.new("RGB", (new_width, new_height), color="white")
      padded_final_img.paste(final_img, (padding, padding))

      # Display the final image (with star icons but no grid lines or labels)
      st.image(padded_final_img, caption="Final Image with Vector Icons", use_column_width=True)

      # Generate and display a popup preview
      if popup_grid_squares:
          st.write("**Popup Preview**")

          for square in popup_grid_squares:
              st.markdown(f"### {square['title']}")
              st.write(square['text'])

          st.write("This is a preview of how the popups will look when a user hovers over the vector icons.")

      # Save the final image as a downloadable file
      padded_final_img.save("final_image_with_icons.png")
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
          <style>
              .image-container {{
                  position: relative;
                  display: inline-block;
              }}
              .icon {{
                  position: absolute;
                  width: 20px;
                  height: 20px;
                  cursor: pointer;
              }}
              .popup {{
                  display: none;
                  position: absolute;
                  background-color: white;
                  border: 1px solid black;
                  padding: 10px;
                  z-index: 1;
              }}
          </style>
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
