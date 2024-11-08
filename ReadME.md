***Guide***

Step 1: Basic Tkinter window with a load PDF Button
    - the first step is to create a basic Tkinter window with a button to load a PDF file. This setup will allow us to open the PDF file dialog

Step 2: Load the PDF and Display the First page

    - Load the PDF file selected in the dialog
    - Use PyMuPDF (fitz) to open the PDF
    - Render the first page as an image
    - Display the image on a Tkinter canvas

    Note! 
      
    pix = page.get_pixmap()  
    img = Image.frombytes("RGB", [pix.width, pix.height], pix.samples)
        
    This process converts the PDF page to an image format that Tkinter can display. PyMuPDF's Pixmap cannot directly be shown in Tkinter, but by converting it to a Pillow Image, we gain access to various display and manipulation options.

Step 3: Add navigation Buttons
    - Add "Next" and "Previous" buttons to the interface
    - Update the display_page function to navigate between pages based on the button   click
    - Implement logic to handlethe start and end of the PDF so it doesn't try to go past available pages


Step 4: Error Handling and User Experience Improvements
    - Add error handling to mangage cases like when the user tries to load an invalid or corrupt PDF
    - Add feedback for the user (e.g displaying a message when no PDF is loaded, or when the user reaches the first or last page)
    - Improve the layout to ensure a smooth user experience 
 

 ***Add editing bar***